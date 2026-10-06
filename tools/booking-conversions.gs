/**
 * Upcore · Booking conversions (Google Apps Script)
 *
 * Bind this script to a new Google Sheet ("Upcore bookings") owned by the Google
 * account whose calendar hosts the discovery-call appointment schedule.
 * Full setup steps: docs/TRACKING.md, section "Booking conversions".
 *
 * What it does
 *   doPost         Receives booking intents from /api/booking-intent (the email a visitor
 *                  enters before the scheduler) and appends them to the "Intents" sheet.
 *   matchBookings  Runs every 10 minutes. Finds new discovery-call bookings in the calendar,
 *                  matches each booker's email to an intent, then:
 *                    - sends GA4 'booking_completed' via the Measurement Protocol, using the
 *                      visitor's GA client ID (only present if analytics consent was given),
 *                    - appends a Google Ads offline-conversion row when the intent carried a
 *                      gclid and ad consent was not refused (sheet "Ads conversions", formatted
 *                      for a scheduled Google Sheets upload in Google Ads).
 *                  Every detected booking is logged in "Bookings", matched or not.
 *
 * Script properties (Project settings → Script properties)
 *   WEBHOOK_TOKEN        Same value as the Vercel env var BOOKING_WEBHOOK_TOKEN (recommended).
 *   GA4_MEASUREMENT_ID   G-TVRF5M70ES
 *   GA4_API_SECRET       GA4 Admin → Data streams → Web → Measurement Protocol API secrets.
 *   CALENDAR_ID          Calendar that owns the booking page. Blank = the default calendar.
 *   EVENT_TITLE_MATCH    Text that appears in booking event titles, e.g. "Discovery Call".
 *   INTERNAL_DOMAIN      upcoretechnologies.com (guests on this domain are ignored).
 *   ADS_CONVERSION_NAME  Exact name of the Google Ads offline conversion action.
 *   ADS_TIMEZONE         Timezone for Conversion Time, e.g. Asia/Kolkata.
 *   ADS_VALUE            Optional conversion value. ADS_CURRENCY: optional, e.g. USD.
 */

var INTENT_HEADERS = ['Timestamp', 'Email', 'Page', 'CTA section', 'CTA id', 'gclid', 'gbraid', 'wbraid',
  'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'Landing page', 'First touch',
  'GA client ID', 'GA session ID', 'Consent', 'Referrer', 'Country', 'Status', 'Booked at', 'Meeting start', 'Event ID'];
var BOOKING_HEADERS = ['Detected at', 'Event ID', 'Title', 'Meeting start', 'Created', 'Guests', 'Matched intent row', 'GA4 sent', 'Ads row'];
var MATCH_WINDOW_DAYS = 30;   // an intent can match a booking created up to 30 days later
var LOOKBACK_HOURS = 72;      // only bookings created in the last 72h are considered (GA4 MP limit)

function props_() { return PropertiesService.getScriptProperties().getProperties(); }

function sheet_(name, headers) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(name);
  if (!sh) {
    sh = ss.insertSheet(name);
    if (headers) { sh.appendRow(headers); sh.setFrozenRows(1); }
  }
  return sh;
}

// Neutralise spreadsheet formula injection from visitor-supplied values.
function safe_(v) {
  v = v == null ? '' : String(v);
  return /^[=+\-@]/.test(v) ? "'" + v : v;
}

function json_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var d = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    var p = props_();
    if (p.WEBHOOK_TOKEN && d.token !== p.WEBHOOK_TOKEN) return json_({ ok: false, error: 'unauthorized' });
    if (d.type !== 'intent' || !d.email) return json_({ ok: false, error: 'bad request' });
    sheet_('Intents', INTENT_HEADERS).appendRow([
      d.timestamp || new Date().toISOString(), safe_(String(d.email).toLowerCase()), safe_(d.page), safe_(d.ctaSection), safe_(d.ctaId),
      safe_(d.gclid), safe_(d.gbraid), safe_(d.wbraid), safe_(d.utmSource), safe_(d.utmMedium), safe_(d.utmCampaign),
      safe_(d.utmTerm), safe_(d.utmContent), safe_(d.landingPage), safe_(d.firstTouchAt), safe_(d.gaClientId),
      safe_(d.gaSessionId), safe_(d.consent), safe_(d.referrer), safe_(d.country), 'pending', '', '', ''
    ]);
    return json_({ ok: true });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

function matchBookings() {
  var p = props_();
  var cal = p.CALENDAR_ID ? CalendarApp.getCalendarById(p.CALENDAR_ID) : CalendarApp.getDefaultCalendar();
  if (!cal) throw new Error('Calendar not found: ' + p.CALENDAR_ID);
  var titleMatch = (p.EVENT_TITLE_MATCH || '').toLowerCase();
  var internal = (p.INTERNAL_DOMAIN || 'upcoretechnologies.com').toLowerCase();
  var owner = Session.getEffectiveUser().getEmail().toLowerCase();
  var now = new Date();

  var bookings = sheet_('Bookings', BOOKING_HEADERS);
  var seen = {};
  if (bookings.getLastRow() > 1) {
    bookings.getRange(2, 2, bookings.getLastRow() - 1, 1).getValues().forEach(function (r) { seen[r[0]] = true; });
  }

  var intents = sheet_('Intents', INTENT_HEADERS);
  var data = intents.getLastRow() > 1 ? intents.getRange(2, 1, intents.getLastRow() - 1, INTENT_HEADERS.length).getValues() : [];
  var col = {};
  INTENT_HEADERS.forEach(function (h, i) { col[h] = i; });

  var events = cal.getEvents(new Date(now.getTime() - 2 * 864e5), new Date(now.getTime() + 120 * 864e5));
  events.forEach(function (ev) {
    var id = ev.getId();
    if (seen[id]) return;
    var created = ev.getDateCreated();
    if (now - created > LOOKBACK_HOURS * 3600e3) return;
    if (titleMatch && ev.getTitle().toLowerCase().indexOf(titleMatch) === -1) return;
    var guests = ev.getGuestList().map(function (g) { return g.getEmail().toLowerCase(); })
      .filter(function (m) { return m !== owner && m.split('@')[1] !== internal; });
    if (!guests.length) return;

    // Latest pending intent for any guest, entered before the booking and within the window.
    var hit = -1;
    for (var i = data.length - 1; i >= 0; i--) {
      var r = data[i];
      if (r[col['Status']] !== 'pending') continue;
      if (guests.indexOf(String(r[col['Email']]).replace(/^'/, '')) === -1) continue;
      var t = new Date(r[col['Timestamp']]);
      if (t > created || created - t > MATCH_WINDOW_DAYS * 864e5) continue;
      hit = i; break;
    }

    var ga4 = 'no', ads = 'no';
    if (hit >= 0) {
      var row = data[hit];
      ga4 = sendGa4_(p, row, col, created) ? 'yes' : 'no';
      ads = appendAdsRow_(p, row, col, created) ? 'yes' : 'no';
      var rn = hit + 2;
      intents.getRange(rn, col['Status'] + 1, 1, 4).setValues([['booked', created.toISOString(), ev.getStartTime().toISOString(), id]]);
      data[hit][col['Status']] = 'booked';
    }
    bookings.appendRow([now.toISOString(), id, safe_(ev.getTitle()), ev.getStartTime().toISOString(), created.toISOString(),
      safe_(guests.join(', ')), hit >= 0 ? hit + 2 : 'unmatched', ga4, ads]);
    seen[id] = true;
  });
}

function sendGa4_(p, row, col, created) {
  var cid = String(row[col['GA client ID']] || '').replace(/^'/, '');
  if (!cid || !p.GA4_MEASUREMENT_ID || !p.GA4_API_SECRET) return false;
  var params = {
    booking_source: 'google_calendar',
    cta_section: String(row[col['CTA section']] || ''),
    page_path: String(row[col['Page']] || ''),
    engagement_time_msec: 1
  };
  var sid = String(row[col['GA session ID']] || '').replace(/^'/, '');
  if (sid) params.session_id = sid;
  var res = UrlFetchApp.fetch('https://www.google-analytics.com/mp/collect?measurement_id=' + encodeURIComponent(p.GA4_MEASUREMENT_ID) +
    '&api_secret=' + encodeURIComponent(p.GA4_API_SECRET), {
    method: 'post', contentType: 'application/json', muteHttpExceptions: true,
    payload: JSON.stringify({ client_id: cid, timestamp_micros: created.getTime() * 1000, events: [{ name: 'booking_completed', params: params }] })
  });
  return res.getResponseCode() >= 200 && res.getResponseCode() < 300;
}

function appendAdsRow_(p, row, col, created) {
  var gclid = String(row[col['gclid']] || '').replace(/^'/, '');
  var consent = String(row[col['Consent']] || '');
  if (!gclid || !p.ADS_CONVERSION_NAME) return false;
  if (consent === 'denied' || consent === 'unknown_eu') return false; // respect ad consent
  var tz = p.ADS_TIMEZONE || 'Asia/Kolkata';
  var sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Ads conversions');
  if (!sh) {
    sh = SpreadsheetApp.getActiveSpreadsheet().insertSheet('Ads conversions');
    sh.appendRow(['Parameters:TimeZone=' + tz]);
    sh.appendRow(['Google Click ID', 'Conversion Name', 'Conversion Time', 'Conversion Value', 'Conversion Currency']);
  }
  sh.appendRow([gclid, p.ADS_CONVERSION_NAME, Utilities.formatDate(created, tz, 'yyyy-MM-dd HH:mm:ss'), p.ADS_VALUE || '', p.ADS_CURRENCY || '']);
  return true;
}

/** Run once after pasting the script: creates the sheets and the 10-minute trigger. */
function setup() {
  sheet_('Intents', INTENT_HEADERS);
  sheet_('Bookings', BOOKING_HEADERS);
  ScriptApp.getProjectTriggers().forEach(function (t) { if (t.getHandlerFunction() === 'matchBookings') ScriptApp.deleteTrigger(t); });
  ScriptApp.newTrigger('matchBookings').timeBased().everyMinutes(10).create();
  Logger.log('Sheets ready and matchBookings scheduled every 10 minutes. Now deploy as a Web App (Execute as: Me, Who has access: Anyone).');
}

/** Sends a test event to the GA4 Measurement Protocol validation endpoint and logs the result. */
function testGa4() {
  var p = props_();
  var res = UrlFetchApp.fetch('https://www.google-analytics.com/debug/mp/collect?measurement_id=' + encodeURIComponent(p.GA4_MEASUREMENT_ID) +
    '&api_secret=' + encodeURIComponent(p.GA4_API_SECRET), {
    method: 'post', contentType: 'application/json', muteHttpExceptions: true,
    payload: JSON.stringify({ client_id: '123456789.1234567890', events: [{ name: 'booking_completed', params: { booking_source: 'test' } }] })
  });
  Logger.log(res.getResponseCode() + ' ' + res.getContentText());
}
