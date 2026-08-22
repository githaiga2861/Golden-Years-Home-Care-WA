#!/usr/bin/env python3
"""Adds the missing admin email alert when someone submits a review.
Reviews were saving to Supabase but never notifying anyone.
Run from inside either site repo root."""
import glob

OLD = """      var r = await _tSb.from('testimonials').insert([{reviewer_name:name, relationship:rel, review_text:text, rating:rating}]);
      if(r.error) throw r.error;
      document.getElementById('reviewForm').style.display='none';
      document.getElementById('rvThanks').style.display='block';"""

NEW = """      var r = await _tSb.from('testimonials').insert([{reviewer_name:name, relationship:rel, review_text:text, rating:rating}]);
      if(r.error) throw r.error;
      document.getElementById('reviewForm').style.display='none';
      document.getElementById('rvThanks').style.display='block';
      var stars='';
      for(var si=0;si<5;si++){ stars += si<rating ? '\\u2605' : '\\u2606'; }
      fetch('https://api.web3forms.com/submit',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify({
        access_key:'40d97e85-7635-4c96-9e51-7624f70df2b0',
        subject:'New Review Submitted \\u2014 Awaiting Approval',
        from_name:'Golden Years Website',
        'Reviewer Name':name,'Relationship':rel||'Not specified','Rating':stars+' ('+rating+'/5)','Review':text,
        'Manage in Admin':'Approve or unpublish this review from your admin dashboard.'
      })}).catch(function(){});"""

count = 0
for page in glob.glob('*.html'):
    s = open(page, encoding='utf-8').read()
    if OLD not in s or "New Review Submitted" in s:
        continue
    s = s.replace(OLD, NEW, 1)
    open(page, 'w', encoding='utf-8').write(s)
    print(f"FIXED: {page}")
    count += 1

print(f"\nTotal pages fixed: {count}")
