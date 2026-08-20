#!/usr/bin/env python3
"""Adds a marketing opt-in checkbox to the quick-enquiry modal and records
consenting people in the `subscribers` table.
Run from inside either site repo root."""
import glob

CHECKBOX = '''<div class="field" style="margin-top:4px">
          <label style="display:flex;align-items:flex-start;gap:9px;font-weight:500;font-size:.86rem;color:var(--slate);cursor:pointer">
            <input type="checkbox" id="mq-optin" style="width:auto;margin:2px 0 0;flex-shrink:0">
            <span>Yes, send me occasional care tips, articles and updates by email. You can unsubscribe at any time.</span>
          </label>
        </div>
'''

ANCHOR = '''<div class="field"><label for="mq-msg">Anything Else? (optional)</label><textarea id="mq-msg" placeholder="A few details help us prepare…"></textarea></div>
'''

OLD_SAVE = """    var savePromise=_mqSb?_mqSb.from('enquiries').insert([{
      form_type:cat||'Quick Enquiry', name:name, email:email, phone:phone, details:details, message:msg
    }]).then(function(){},function(){}):Promise.resolve();"""

NEW_SAVE = """    var optin=document.getElementById('mq-optin');
    var wantsUpdates=!!(optin&&optin.checked);

    var savePromise=_mqSb?_mqSb.from('enquiries').insert([{
      form_type:cat||'Quick Enquiry', name:name, email:email, phone:phone, details:details, message:msg
    }]).then(function(){},function(){}):Promise.resolve();

    // Marketing list — only when the visitor has explicitly ticked the box
    if(wantsUpdates && email && _mqSb){
      _mqSb.from('subscribers').upsert([{
        email:email, name:name, interest:cat||'General', source:'Quick Enquiry Modal'
      }],{onConflict:'email'}).then(function(){},function(){});
    }"""


# ---------- Home Care WA variant (different field IDs and table) ----------
HCWA_ANCHOR = '''<div class="field"><label for="q-when">When is care needed?</label><select id="q-when" name="When Needed"><option>As soon as possible</option><option>Within 2 weeks</option><option>Within a month</option><option>Just exploring options</option></select></div>
'''

HCWA_CHECKBOX = '''      <div class="field" style="margin-top:4px">
        <label style="display:flex;align-items:flex-start;gap:9px;font-weight:500;font-size:.86rem;color:var(--slate);cursor:pointer">
          <input type="checkbox" id="q-optin" style="width:auto;margin:2px 0 0;flex-shrink:0">
          <span>Yes, send me occasional care tips, articles and updates by email. You can unsubscribe at any time.</span>
        </label>
      </div>
'''

HCWA_OLD = '''function _hcSaveLead(sourcePage,name,email,phone,details,message){
  if(!_hcSb) return Promise.resolve();
  return _hcSb.from('homecare_leads').insert([{source_page:sourcePage,name:name,email:email,phone:phone,details:details,message:message||''}]).then(function(){},function(){});
}'''

HCWA_NEW = '''function _hcSaveLead(sourcePage,name,email,phone,details,message){
  if(!_hcSb) return Promise.resolve();
  var optin=document.getElementById('q-optin');
  if(optin&&optin.checked&&email){
    _hcSb.from('subscribers').upsert([{email:email,name:name,interest:'Home Care',source:sourcePage}],{onConflict:'email'}).then(function(){},function(){});
  }
  return _hcSb.from('homecare_leads').insert([{source_page:sourcePage,name:name,email:email,phone:phone,details:details,message:message||''}]).then(function(){},function(){});
}'''

count = 0
EXCLUDE={'admin.html','404.html','careers-admin.html','publish.html','unsubscribe.html'}
for page in glob.glob('*.html'):
    if page in EXCLUDE: continue
    with open(page, encoding='utf-8') as f:
        s = f.read()
    if 'mq-optin' in s or 'q-optin' in s:
        print(f"SKIP (already done): {page}"); continue

    if ANCHOR in s and OLD_SAVE in s:
        # Main site
        s = s.replace(ANCHOR, ANCHOR + '        ' + CHECKBOX, 1)
        s = s.replace(OLD_SAVE, NEW_SAVE, 1)
    elif HCWA_ANCHOR in s and HCWA_OLD in s:
        # Home Care WA
        s = s.replace(HCWA_ANCHOR, HCWA_ANCHOR + HCWA_CHECKBOX, 1)
        s = s.replace(HCWA_OLD, HCWA_NEW, 1)
    elif HCWA_ANCHOR in s:
        # Sub-page: checkbox only (the shared save function lives on index)
        s = s.replace(HCWA_ANCHOR, HCWA_ANCHOR + HCWA_CHECKBOX, 1)
    else:
        continue
    with open(page, 'w', encoding='utf-8') as f:
        f.write(s)
    print(f"UPDATED: {page}")
    count += 1

print(f"\nTotal pages updated: {count}")
