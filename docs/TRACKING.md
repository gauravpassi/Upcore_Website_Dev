# Tracking, consent & conversions

How analytics, consent and booking conversions work on upcoretech.com, and the one-time setup each needs. Current as of 2026-10-06 (V4.1 rollout).

---

## 1. Two tagging modes (during the migration)

| Pages | How tags load | Who sends events |
|---|---|---|
| **V4 pages**: `/`, `/ai-native-engineering`, `/who-we-help/*` | **GTM only.** `<head>` sets Consent Mode v2 defaults, `window.upcGTM = true` and pushes `{tagging:'gtm', content_group}` before the GTM loader. No direct `gtag.js`, no inline Clarity. | Site scripts push `{event, event_params}` to `dataLayer`; GTM's GA4 event tag sends them. |
| **Legacy pages** (everything else, incl. LPs) | Direct `gtag.js` (GA4 + Ads) and inline Clarity, plus the GTM loader. | Site scripts call `gtag('event', …)` directly. |

**The `tagging` flag is the safety catch.** Every trigger in the GTM container requires `{{DLV - tagging}} equals gtm`, so publishing the container never adds a second GA4/Ads/Clarity tag to a legacy page. When a legacy page is moved to V4, it gets the flag and stops loading `gtag.js` itself in the same change.

Shared senders (all check `window.upcGTM` first):
- [`cta-tracking.js`](../cta-tracking.js): `cta_click`, plus first-touch attribution (`gclid`/`gbraid`/`wbraid`/`utm_*`, landing page) into `localStorage.upc_attrib`.
- [`js/v4-analytics.js`](../js/v4-analytics.js): engagement events on V4 pages.
- [`chat-widget.js`](../chat-widget.js): chat `generate_lead` and the booking-modal events.

`event_params` is reset (`{event_params: null}`) before every push so GTM's merged data model never carries a value from one event into the next. **No email or other personal data is ever pushed to `dataLayer` or `gtag`.**

## 2. Events

| Event | Fired by | Key params |
|---|---|---|
| `cta_click` | any `[data-gtm-cta]` click | `cta_id`, `cta_type`, `cta_section`, `cta_text`, `cta_url`, `page_path` |
| `scroll_depth` | V4 pages | `percent_scrolled` (25/50/75/90) |
| `section_view` | V4 sections with `aria-labelledby` | `section_id`, `section_title` |
| `framework_tab_select` / `content_tab_select` | V4 tabs | `tab_id`, `method` |
| `nav_menu_open` | V4 nav dropdowns | `menu` |
| `faq_open` | FAQ `<details>` | `faq_question` |
| `booking_modal_open` | booking modal | `cta_id`, `cta_section`, `page_path` |
| `generate_lead` | booking email submitted (`lead_source: booking_modal`), chat question sent (`lead_source: chat_widget`) contact form sent (`lead_source: contact_form`, plus `topic`) or newsletter signup on `/insights` (`lead_source: newsletter`) | `lead_source`, `topic` |
| `booking_email_skipped` | "Skip and go straight to the calendar" | |
| `booking_calendar_view` | calendar shown after the email step | |
| `booking_iframe_engaged` / `booking_iframe_navigated` | first interaction / navigation inside the scheduler | `seconds_to_engage`, `load_count` |
| `booking_modal_close` | modal closed | `open_seconds`, `iframe_engaged` |
| `booking_completed` | **server-side**, Apps Script via GA4 Measurement Protocol (§5) | `booking_source`, `cta_section`, `page_path` |
| `chat_open` / `chat_question` / `chat_action` | website assistant (`chat-widget.js`) | `source` (starter/typed), `mode` (ai/faq), `action` (book/person) |
| `estimator_used` | homepage estimator, first interaction | |
| `consent_update` | cookie banner choice | `consent_choice` (dataLayer only) |

## 3. GTM container: import & publish

File: [`tools/gtm-container-upcore-v4.json`](../tools/gtm-container-upcore-v4.json) (regenerate with `python tools/v4-build/gtm_build.py`).

Contents: Google tag GA4 `G-TVRF5M70ES` (with `content_group` and `traffic_type`), Google tag Ads `AW-16546427858`, Conversion Linker, one GA4 event tag (`{{Event}}`) for every event in §2 except `booking_completed`, Microsoft Clarity (Custom HTML, requires `analytics_storage`, re-fires on `consent_update`), 4 triggers, 25 variables. Regenerated 2026-10-07 with the chat and estimator events: re-import and publish to start sending them.

1. tagmanager.google.com → container **GTM-MH5PB32L** → **Admin → Import container**.
2. Choose the JSON file. Workspace: **New** ("V4 rollout"). Option: **Merge → Rename conflicting tags, triggers and variables**.
3. **Preview** against `https://upcore-website-dev.vercel.app/`. Check: the GA4 and Ads Google tags fire on Initialization; clicking a CTA fires "GA4 event - V4 site events" with `cta_click`; nothing fires on a legacy page such as `/about`.
4. **Submit → Publish.** Do this **before** the V4 pages reach production, or those pages record no analytics at all.

Hits from any host other than `upcoretech.com` carry `traffic_type=internal`. In GA4 **Admin → Data settings → Data filters**, set the **Internal traffic** filter to **Active** so dev/preview traffic is excluded from reports.

### GA4 one-time settings
- **Admin → Custom definitions → Create custom dimension** (event scope) for the params you want in reports: `cta_id`, `cta_section`, `cta_type`, `section_id`, `tab_id`, `faq_question`, `lead_source`, `percent_scrolled` (metric), `booking_source`.
- **Admin → Events → Mark as key event:** `generate_lead`, `booking_completed`.
- **Admin → Data streams → Web → Measurement Protocol API secrets → Create.** Put the value in the Apps Script property `GA4_API_SECRET` (§5). Never commit it.

## 4. Consent (Consent Mode v2)

- Defaults (in `<head>` of V4 pages, before GTM): `ad_storage`, `ad_user_data`, `ad_personalization`, `analytics_storage` **denied** for the EEA, UK and Switzerland; **granted** elsewhere. `ads_data_redaction` is on.
- A stored choice (`localStorage.upc_consent` = `granted`/`denied`) is re-applied on every page load before GTM runs.
- Banner ([`js/upcore-v4.js`](../js/upcore-v4.js), bottom of file): shown automatically when the visitor's timezone is in Europe and no choice is stored; always reachable from **Cookie settings** in the V4 footer. Accept and Decline have equal weight.
- Clarity only loads once `analytics_storage` is granted (GTM consent check).
- Legacy pages have no banner yet; they keep their direct tags until they move to V4.
- Disclosures: [`privacy.html`](../privacy.html) §2 (Analytics, Advertising measurement, Your cookie choices, Calendar bookings), §5, §6, §7. **Have the policy reviewed by counsel before production.**

## 5. Booking conversions

Google Calendar's appointment-scheduling iframe has no "booked" callback, so completion is measured server-side:

```
Book button → modal email step ──► /api/booking-intent ──► Apps Script doPost ──► "Intents" sheet
/assessment form (email already asked) ─┘                                              │
                                     (every 10 min) matchBookings: new calendar events │
                                     → attendee email matches a pending intent ◄───────┘
                                     → GA4 Measurement Protocol: booking_completed (needs GA client ID)
                                     → "Ads conversions" sheet row (needs gclid + ad consent not refused)
                                     → "Bookings" log row (matched or not)
```

Also on each modal email: a FormSubmit notification to gaurav@ (CC saswata@), subject "Discovery call started: <email>", so a started-but-unbooked call can be followed up.

### Setup (once, ~20 minutes)
1. Sign in as the Google account that **owns the discovery-call appointment schedule**. Create a Google Sheet named **Upcore bookings**.
2. **Extensions → Apps Script.** Replace the default code with [`tools/booking-conversions.gs`](../tools/booking-conversions.gs). Save.
3. **Project settings → Script properties**, add:

   | Property | Value |
   |---|---|
   | `WEBHOOK_TOKEN` | a long random string (also goes into Vercel, step 6) |
   | `GA4_MEASUREMENT_ID` | `G-TVRF5M70ES` |
   | `GA4_API_SECRET` | from GA4 (§3) |
   | `CALENDAR_ID` | blank for the default calendar, or the booking calendar's ID |
   | `EVENT_TITLE_MATCH` | text that appears in booking event titles, e.g. the appointment schedule's name |
   | `INTERNAL_DOMAIN` | `upcoretechnologies.com` |
   | `ADS_CONVERSION_NAME` | exact name of the Ads conversion action from step 8, e.g. `Discovery call booked` |
   | `ADS_TIMEZONE` | the Google Ads account timezone, e.g. `Asia/Kolkata` |
   | `ADS_VALUE`, `ADS_CURRENCY` | optional |

4. In the editor, select **`setup`** → **Run** → approve the permissions (Sheets, Calendar, external requests, triggers). This creates the `Intents` and `Bookings` tabs and a 10-minute trigger for `matchBookings`. Optionally run **`testGa4`** and check the log shows no validation messages.
5. **Deploy → New deployment → Web app.** Execute as: **Me**. Who has access: **Anyone**. Copy the URL ending `/exec`.
6. **Vercel → Project → Settings → Environment Variables** (dev project first, then production):
   - `BOOKING_SHEETS_WEBHOOK_URL` = the `/exec` URL
   - `BOOKING_WEBHOOK_TOKEN` = the same value as `WEBHOOK_TOKEN`

   Redeploy. Without these the endpoint returns `202 {stored:false}` and the site keeps working.
7. **Test on dev:** click Book, enter a test email, confirm a row in `Intents`. Book a real slot in the calendar with the same email; within 10 minutes `Bookings` shows it as matched and the intent's Status becomes `booked`. Also confirm both inboxes received the "Discovery call started" FormSubmit email (first-time activation, see [CONVENTIONS.md §8](CONVENTIONS.md#8-forms--email-destinations)). Delete the test rows and cancel the test booking afterwards.
8. **Google Ads → Goals → Conversions → New conversion action → Import → CRMs, files or other data sources → Track conversions from clicks.** Name it exactly as `ADS_CONVERSION_NAME`, category "Book appointment", count **One**. Make it **Primary**. Then **Uploads → Schedules → Google Sheets** → the `Ads conversions` tab, daily.
9. Set the old **"Book governance review"** action (`_Q5SCO7LodgcENLn-dE9`, no longer fires) to **Secondary** or remove it, so bidding isn't starved by a dead primary. Keep **"Lead Tracking"** (assessment form submit) as Secondary.
10. Optional: link GA4 to Ads and import `booking_completed` as a **Secondary** (observation) action. Never make both it and the offline upload Primary, or bookings count twice.

### Notes
- An intent matches a booking created up to 30 days later; only bookings created in the last 72 hours are processed (GA4 Measurement Protocol limit).
- Visitors who decline analytics have no `_ga` cookie, so no GA4 event is sent for them. Intents with consent `denied` or `unknown_eu` (Europe timezone, no choice) never produce an Ads row.
- The Ads sheet covers `gclid` only. iOS `gbraid`/`wbraid` clicks are stored in `Intents` but not uploaded.
- Booking records are kept 12 months (privacy policy §7). Clear older `Intents`/`Bookings` rows on that schedule.

## 6. Troubleshooting

| Symptom | Check |
|---|---|
| No GA4 data from V4 pages | Container published? In Tag Assistant, is `tagging` = `gtm` on the page? Consent denied (EU visitor without a choice)? |
| Double page_views | A page has both the `tagging:'gtm'` flag and a direct `gtag('config', …)`. V4 pages must not load `gtag.js`. |
| `Intents` empty | Vercel env vars set and redeployed? `/api/booking-intent` returns `202 stored:false` when the URL is missing, `502` when the Apps Script fails. Check the token matches. |
| Bookings stay `unmatched` | `EVENT_TITLE_MATCH` too strict? Booker used a different email than the one typed in the modal (it is matched by email only). |
| Ads upload errors | Conversion name mismatch, wrong timezone row, or the click is older than the conversion action's click-through window. |
