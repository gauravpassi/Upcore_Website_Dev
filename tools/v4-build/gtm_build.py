"""Builds tools/gtm-container-upcore-v4.json: an importable GTM container (Admin > Import Container > Merge)."""
import json, time, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'gtm-container-upcore-v4.json')
ACC, CON = '6000000000', '200000000'
FP = str(int(time.time() * 1000))
GA4, AW = 'G-TVRF5M70ES', 'AW-16546427858'

EVENTS = ['cta_click', 'scroll_depth', 'section_view', 'framework_tab_select', 'content_tab_select', 'nav_menu_open',
          'faq_open', 'booking_modal_open', 'booking_calendar_view', 'booking_email_skipped', 'booking_iframe_engaged',
          'booking_iframe_navigated', 'booking_modal_close', 'generate_lead']
PARAMS = ['cta_id', 'cta_type', 'cta_section', 'cta_text', 'cta_url', 'page_path', 'percent_scrolled', 'section_id',
          'section_title', 'tab_id', 'method', 'menu', 'faq_question', 'open_seconds', 'iframe_engaged',
          'seconds_to_engage', 'load_count', 'lead_source']


def t(k, v): return {'type': 'TEMPLATE', 'key': k, 'value': v}
def b(k, v): return {'type': 'BOOLEAN', 'key': k, 'value': 'true' if v else 'false'}
def kv(rows): return [{'type': 'MAP', 'map': [t('parameter', k), t('parameterValue', v)]} for k, v in rows]
def base(**o): return dict(accountId=ACC, containerId=CON, fingerprint=FP, **o)
def cond(kind, a0, a1): return {'type': kind, 'parameter': [t('arg0', a0), t('arg1', a1)]}


GTM_ONLY = cond('EQUALS', '{{DLV - tagging}}', 'gtm')

variables, vid = [], 100
def var(name, typ, params):
    global vid
    vid += 1
    variables.append(base(variableId=str(vid), name=name, type=typ, parameter=params, formatValue={}))
def dlv(name, key):
    var(name, 'v', [{'type': 'INTEGER', 'key': 'dataLayerVersion', 'value': '2'}, b('setDefaultValue', False), t('name', key)])

dlv('DLV - tagging', 'tagging')
dlv('DLV - content_group', 'content_group')
for p in PARAMS:
    dlv(f'DLV - {p}', f'event_params.{p}')
var('JS - traffic_type', 'jsm', [t('javascript', "function(){\n  // Hits from any host other than upcoretech.com (dev, previews, localhost) are tagged\n  // traffic_type=internal; activate GA4's Internal traffic data filter to exclude them.\n  var h = {{Page Hostname}} || '';\n  return /(^|\\.)upcoretech\\.com$/.test(h) ? undefined : 'internal';\n}")])

triggers = [
    base(triggerId='11', name='Init - V4 pages (tagging=gtm)', type='INIT', filter=[GTM_ONLY]),
    base(triggerId='12', name='Page view - V4 pages (tagging=gtm)', type='PAGEVIEW', filter=[GTM_ONLY]),
    base(triggerId='13', name='CE - V4 site events', type='CUSTOM_EVENT',
         customEventFilter=[cond('MATCH_REGEX', '{{_event}}', '^(' + '|'.join(EVENTS) + ')$')], filter=[GTM_ONLY]),
    base(triggerId='14', name='CE - consent_update', type='CUSTOM_EVENT',
         customEventFilter=[cond('EQUALS', '{{_event}}', 'consent_update')], filter=[GTM_ONLY]),
]

CLARITY = ('<script>(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};'
           't=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];'
           'y.parentNode.insertBefore(t,y);})(window,document,"clarity","script","xtvhi9nvqa");</script>')

tags = [
    base(tagId='1', name=f'Google tag - GA4 ({GA4})', type='googtag',
         parameter=[t('tagId', GA4), {'type': 'LIST', 'key': 'configSettingsTable', 'list': kv([
             ('content_group', '{{DLV - content_group}}'), ('traffic_type', '{{JS - traffic_type}}')])}],
         firingTriggerId=['11'], tagFiringOption='ONCE_PER_EVENT', monitoringMetadata={'type': 'MAP'},
         consentSettings={'consentStatus': 'NOT_SET'}),
    base(tagId='2', name=f'Google tag - Google Ads ({AW})', type='googtag',
         parameter=[t('tagId', AW)],
         firingTriggerId=['11'], tagFiringOption='ONCE_PER_EVENT', monitoringMetadata={'type': 'MAP'},
         consentSettings={'consentStatus': 'NOT_SET'}),
    base(tagId='3', name='Conversion Linker', type='gclidw',
         parameter=[b('enableCrossDomain', False), b('enableUrlPassthrough', False), b('enableCookieOverrides', False)],
         firingTriggerId=['11'], tagFiringOption='ONCE_PER_EVENT', monitoringMetadata={'type': 'MAP'},
         consentSettings={'consentStatus': 'NOT_SET'}),
    base(tagId='4', name='GA4 event - site events ({{Event}})', type='gaawe',
         parameter=[b('sendEcommerceData', False), t('eventName', '{{Event}}'), t('measurementIdOverride', GA4),
                    {'type': 'LIST', 'key': 'eventSettingsTable', 'list': kv([(p, '{{DLV - %s}}' % p) for p in PARAMS])}],
         firingTriggerId=['13'], tagFiringOption='ONCE_PER_EVENT', monitoringMetadata={'type': 'MAP'},
         consentSettings={'consentStatus': 'NOT_SET'}),
    base(tagId='5', name='Microsoft Clarity (xtvhi9nvqa)', type='html',
         parameter=[t('html', CLARITY), b('supportDocumentWrite', False)],
         firingTriggerId=['12', '14'], tagFiringOption='ONCE_PER_LOAD', monitoringMetadata={'type': 'MAP'},
         consentSettings={'consentStatus': 'NEEDED', 'consentType': {'type': 'LIST', 'list': [{'type': 'TEMPLATE', 'value': 'analytics_storage'}]}}),
]
tags[3]['name'] = 'GA4 event - V4 site events'

builtins = [base(type=k, name=n) for k, n in [('PAGE_URL', 'Page URL'), ('PAGE_HOSTNAME', 'Page Hostname'), ('PAGE_PATH', 'Page Path'),
                                              ('REFERRER', 'Referrer'), ('EVENT', 'Event')]]
for x in builtins:
    x.pop('fingerprint')

container = {
    'exportFormatVersion': 2,
    'exportTime': time.strftime('%Y-%m-%d %H:%M:%S'),
    'containerVersion': {
        'path': f'accounts/{ACC}/containers/{CON}/versions/0',
        'accountId': ACC, 'containerId': CON, 'containerVersionId': '0',
        'container': {'path': f'accounts/{ACC}/containers/{CON}', 'accountId': ACC, 'containerId': CON,
                      'name': 'upcoretech.com', 'publicId': 'GTM-MH5PB32L', 'usageContext': ['WEB'],
                      'fingerprint': FP, 'tagManagerUrl': '', 'tagIds': ['GTM-MH5PB32L']},
        'tag': tags, 'trigger': triggers, 'variable': variables, 'builtInVariable': builtins,
        'fingerprint': FP,
        'tagManagerUrl': '',
    },
}
json.dump(container, open(OUT, 'w', encoding='utf-8', newline='\n'), indent=2, ensure_ascii=False)
print(len(tags), 'tags', len(triggers), 'triggers', len(variables), 'variables')
