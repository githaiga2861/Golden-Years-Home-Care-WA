#!/usr/bin/env python3
"""Fixes three chat-hint/fab bugs:
1. Hint was showing before the quickbar (and its chat icon) was even visible
2. Hint was mis-positioned on desktop (fixed pixel values only worked on mobile)
3. The floating call button overlapped the quickbar on mobile
Run from inside the repo root. Works for BOTH the main site (uses
id="mainQuickbar") and Home Care WA (uses id="quickbar") automatically."""
import glob

def build_patches(quickbar_id):
    old1 = '''  function onQbScroll(){
    var qb=document.getElementById('%s');
    if(qb) qb.classList.toggle('show', window.scrollY>560);
  }
  window.addEventListener('scroll', onQbScroll, {passive:true});
  onQbScroll();
})();
</script>''' % quickbar_id

    new1 = '''  var _mobileQuery = window.matchMedia('(max-width:600px)');
  function onQbScroll(){
    var qb=document.getElementById('%s');
    if(!qb) return;
    var visible = window.scrollY>560;
    qb.classList.toggle('show', visible);
    if(_mobileQuery.matches){
      var fab = document.querySelector('.fab');
      if(fab) fab.style.display = visible ? 'none' : '';
    }
    if(visible && typeof window.tryShowChatHint==='function'){
      setTimeout(window.tryShowChatHint, 600);
    }
  }
  window.addEventListener('scroll', onQbScroll, {passive:true});
  onQbScroll();
})();
</script>''' % quickbar_id

    return old1, new1

OLD2 = '''<script>
(function(){
  function shouldShowHint(){
    try{ return !sessionStorage.getItem('gy_chat_hint_seen'); }catch(e){ return true; }
  }
  window.dismissChatHint = function(){
    var el = document.getElementById('chatHint');
    if(el) el.classList.remove('show');
    try{ sessionStorage.setItem('gy_chat_hint_seen','1'); }catch(e){}
  };
  document.addEventListener('DOMContentLoaded', function(){
    if(!shouldShowHint()) return;
    setTimeout(function(){
      // Don't show if the chat panel is already open, or the quickbar isn't visible yet
      var panel = document.getElementById('chatPanel');
      if(panel && panel.classList.contains('open')) return;
      var el = document.getElementById('chatHint');
      if(el) el.classList.add('show');
      // Auto-dismiss on its own after 9 seconds if the visitor ignores it
      setTimeout(function(){ window.dismissChatHint(); }, 9000);
    }, 4000);
  });
  // If they open the chat, hide the hint immediately and remember it was seen
  var origToggle = window.toggleChatPanel;
  document.addEventListener('click', function(e){
    if(e.target.closest('.chat-trigger')){ window.dismissChatHint(); }
  });
})();
</script>'''

NEW2 = '''<script>
(function(){
  var _hintShownThisSession = false;
  function positionHintAboveTrigger(){
    var trigger = document.querySelector('.chat-trigger');
    var hint = document.getElementById('chatHint');
    if(!trigger || !hint) return false;
    var rect = trigger.getBoundingClientRect();
    if(rect.width === 0 && rect.height === 0) return false;
    var hintWidth = hint.offsetWidth || 220;
    var left = rect.left;
    var maxLeft = window.innerWidth - hintWidth - 12;
    if(left > maxLeft) left = maxLeft;
    if(left < 8) left = 8;
    var bottom = window.innerHeight - rect.top + 12;
    hint.style.left = left + 'px';
    hint.style.bottom = bottom + 'px';
    hint.style.top = 'auto';
    return true;
  }
  function shouldShowHint(){
    try{ return !sessionStorage.getItem('gy_chat_hint_seen'); }catch(e){ return true; }
  }
  window.dismissChatHint = function(){
    var el = document.getElementById('chatHint');
    if(el) el.classList.remove('show');
    try{ sessionStorage.setItem('gy_chat_hint_seen','1'); }catch(e){}
  };
  window.tryShowChatHint = function(){
    if(_hintShownThisSession || !shouldShowHint()) return;
    var panel = document.getElementById('chatPanel');
    if(panel && panel.classList.contains('open')) return;
    if(!positionHintAboveTrigger()) return;
    _hintShownThisSession = true;
    var el = document.getElementById('chatHint');
    if(el) el.classList.add('show');
    setTimeout(function(){ window.dismissChatHint(); }, 9000);
  };
  window.addEventListener('resize', function(){
    var hint = document.getElementById('chatHint');
    if(hint && hint.classList.contains('show')) positionHintAboveTrigger();
  });
  document.addEventListener('click', function(e){
    if(e.target.closest('.chat-trigger')){ window.dismissChatHint(); }
  });
})();
</script>'''

count = 0
EXCLUDE = {'chat_hint_html.html', 'chat_hint_js.html'}
for page in glob.glob('*.html'):
    if page in EXCLUDE: continue
    with open(page, encoding='utf-8') as f:
        s = f.read()
    if 'tryShowChatHint' in s:
        print(f"SKIP (already fixed): {page}"); continue

    changed = False
    for qb_id in ('mainQuickbar', 'quickbar'):
        old1, new1 = build_patches(qb_id)
        if old1 in s:
            s = s.replace(old1, new1, 1)
            changed = True
            break

    if OLD2 in s:
        s = s.replace(OLD2, NEW2, 1)
        changed = True

    if changed:
        with open(page, 'w', encoding='utf-8') as f:
            f.write(s)
        print(f"FIXED: {page}")
        count += 1

print(f"\nTotal pages fixed: {count}")
print("Now append the CSS: cat hint_position_css_fix.css >> css/styles.css")
