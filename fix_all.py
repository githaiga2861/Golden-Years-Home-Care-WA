#!/usr/bin/env python3
"""Fixes 5 issues. Run from inside either SITE repo root (main or HCWA)."""
import glob, os, re

CB = ('<div class="field optin-field">\n'
      '  <label class="optin-label">\n'
      '    <input type="checkbox" id="{id}">\n'
      '    <span><strong>Keep me updated.</strong> Send me occasional care tips, '
      'articles and service updates by email. Unsubscribe anytime.</span>\n'
      '  </label>\n'
      '</div>\n')

changed = 0

# ---------- MAIN SITE contact page ----------
if os.path.exists('contact.html'):
    s = open('contact.html', encoding='utf-8').read()
    if 'cf-optin' not in s and "_gySb.from('enquiries').insert" in s:
        # checkbox before each submit button on the contact page's own forms
        for label in ('Send Message', 'Submit Care Inquiry'):
            btn = f'<button class="btn btn--primary" type="submit" style="width:100%;justify-content:center">{label}</button>'
            if btn in s:
                cid = 'cf-optin-' + re.sub(r'\W+', '', label).lower()
                s = s.replace(btn, CB.format(id=cid) + btn, 1)
        old = """    _gySb.from('enquiries').insert([{
      form_type: formId==='careForm'?'Care Inquiry':'General',
      name:nm, email:em, phone:ph, message:msg, details:det
    }]).then(function(){}, function(){});"""
        new = """    _gySb.from('enquiries').insert([{
      form_type: formId==='careForm'?'Care Inquiry':'General',
      name:nm, email:em, phone:ph, message:msg, details:det
    }]).then(function(){}, function(){});
    var _ob=form.querySelector('.optin-field input[type="checkbox"]');
    if(_ob && _ob.checked && em){
      _gySb.from('subscribers').upsert([{email:em,name:nm,
        interest:(formId==='careForm'?'Care Inquiry':'General'),source:'Contact Page'}],
        {onConflict:'email'}).then(function(){},function(){});
    }"""
        if old in s:
            s = s.replace(old, new, 1)
        open('contact.html', 'w', encoding='utf-8').write(s)
        print("FIXED opt-in: contact.html (main site)")
        changed += 1

    # ---------- HCWA contact page ----------
    elif 'cf-optin' not in s and '_hcSaveLead' in s:
        btn = '<button class="btn btn--primary" type="submit" id="csubmit" style="width:100%;justify-content:center">Send My Request</button>'
        if btn in s:
            s = s.replace(btn, CB.format(id='cf-optin') + btn, 1)
        old = """  var saveP=(typeof _hcSaveLead==='function')?_hcSaveLead('Contact Page',name,email,phone,{'Care For':careFor,'City or ZIP':city,'When Needed':when},msg):Promise.resolve();"""
        new = """  var _cb=document.getElementById('cf-optin');
  if(_cb && _cb.checked && email && typeof _hcSb!=='undefined' && _hcSb){
    _hcSb.from('subscribers').upsert([{email:email,name:name,interest:'Home Care',source:'Contact Page'}],{onConflict:'email'}).then(function(){},function(){});
  }
  var saveP=(typeof _hcSaveLead==='function')?_hcSaveLead('Contact Page',name,email,phone,{'Care For':careFor,'City or ZIP':city,'When Needed':when},msg):Promise.resolve();"""
        if old in s:
            s = s.replace(old, new, 1)
        open('contact.html', 'w', encoding='utf-8').write(s)
        print("FIXED opt-in: contact.html (Home Care WA)")
        changed += 1

# ---------- Chat history: event delegation instead of inline onclick ----------
OLD_ITEM = """          html += '<div class="chat-hist__item" onclick="openChatSession(\\'' + sid + '\\')">' +"""
NEW_ITEM = """          html += '<div class="chat-hist__item" data-sid="' + sid + '">' +"""

DELEGATION = """
  /* Past-chat items are opened via delegation (robust against quoting) */
  document.addEventListener('click', function(e){
    var it = e.target.closest && e.target.closest('.chat-hist__item');
    if(it && it.getAttribute('data-sid')) window.openChatSession(it.getAttribute('data-sid'));
  });
"""

for page in glob.glob('*.html'):
    s = open(page, encoding='utf-8').read()
    if 'chat-hist__item' not in s or 'data-sid' in s:
        continue
    hit = False
    if OLD_ITEM in s:
        s = s.replace(OLD_ITEM, NEW_ITEM, 1); hit = True
    anchor = "  /* Opening the chat marks everything as read */"
    if hit and anchor in s:
        s = s.replace(anchor, DELEGATION + anchor, 1)
    if hit:
        open(page, 'w', encoding='utf-8').write(s)
        print(f"FIXED history clicks: {page}")
        changed += 1

print(f"\nTotal files changed: {changed}")
