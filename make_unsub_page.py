#!/usr/bin/env python3
"""Builds unsubscribe.html for a site by reusing its own header/footer,
so the page looks native. Run from inside either site repo root."""
import glob, os, re

# Pick a page that definitely has the full shell
SRC = 'reviews.html' if os.path.exists('reviews.html') else 'contact.html'
s = open(SRC, encoding='utf-8').read()

site = 'hcwa' if 'goldenyearshomecarewa' in s or 'styzbftuzuqcnkwvwpgm' in s else 'main'

m = re.search(r'<main[^>]*>', s)
if not m:
    raise SystemExit('Could not find <main> in ' + SRC)
head = s[:m.start()]
tail = s[s.rindex('</main>') + len('</main>'):]

head = re.sub(r'<title>.*?</title>', '<title>Unsubscribe | Golden Years</title>', head, count=1, flags=re.S)

body = '''<main id="main" style="padding-top:0">
<section class="section" style="padding-top:170px;min-height:52vh">
  <div class="wrap" style="max-width:620px">
    <div class="center">
      <span class="eyebrow center">Email Preferences</span>
      <h1 id="unsubTitle">Unsubscribing…</h1>
      <hr class="gold-rule center">
      <p id="unsubMsg">One moment while we update your preferences.</p>
      <div id="unsubActions" style="display:none;margin-top:26px">
        <a class="btn btn--primary" href="/">Back to Home</a>
      </div>
    </div>
  </div>
</section>
</main>

<script>
(function(){
  var ENDPOINT = 'https://golden-years-websites-admin.vercel.app/api/unsubscribe';
  var SITE = '__SITE__';
  var token = new URLSearchParams(location.search).get('token');
  var title = document.getElementById('unsubTitle');
  var msg   = document.getElementById('unsubMsg');
  var acts  = document.getElementById('unsubActions');

  function done(t, m){ title.textContent = t; msg.innerHTML = m; acts.style.display = 'block'; }

  if(!token){
    done('Link Not Recognised',
      'This unsubscribe link is missing its code. Please email <a href="mailto:contact@goldenyearshomehealthllc.com">contact@goldenyearshomehealthllc.com</a> and we will remove you right away.');
    return;
  }

  fetch(ENDPOINT + '?token=' + encodeURIComponent(token) + '&site=' + SITE, { method: 'POST' })
    .then(function(r){ return r.json(); })
    .then(function(d){
      if(d.ok){
        done('You Have Been Unsubscribed',
          'You will not receive any further marketing emails from us. If this was a mistake, just get in touch on <a href="tel:+12067171234">(206) 717-1234</a> and we can add you back.');
      } else {
        done('Something Went Wrong',
          (d.error || 'Please email <a href="mailto:contact@goldenyearshomehealthllc.com">contact@goldenyearshomehealthllc.com</a> and we will remove you manually.'));
      }
    })
    .catch(function(){
      done('Something Went Wrong',
        'Please email <a href="mailto:contact@goldenyearshomehealthllc.com">contact@goldenyearshomehealthllc.com</a> and we will remove you manually.');
    });
})();
</script>
'''.replace('__SITE__', site)

open('unsubscribe.html', 'w', encoding='utf-8').write(head + body + tail)
print(f"Built unsubscribe.html (detected site: {site}, shell from {SRC})")
