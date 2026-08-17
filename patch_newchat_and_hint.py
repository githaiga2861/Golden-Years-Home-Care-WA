#!/usr/bin/env python3
"""1. Adds a '+' new-chat button to the chat panel header (size unchanged).
   2. Makes the chat hint reappear on later pages, briefly, until the
      visitor actually opens the chat.
Run from inside either site repo root."""
import glob

NEW_BTN = ('<button class="chat-hist-btn" onclick="startNewChat()" aria-label="Start a new chat" title="New chat">'
           '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2" '
           'stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12h14"/></svg></button>')

HIST_BTN_ANCHOR = '<button class="chat-hist-btn" onclick="showChatHistory()"'

# --- new-chat logic, injected into the chat IIFE ---
OLD_RESTORE = """  /* ---- Restore prior conversation + badge on every page load -------- */
  document.addEventListener('DOMContentLoaded', function(){
    setUnread(getUnread());
    if (!chatHistory.length) return;
    var body = document.getElementById('chatBody');
    if (!body) return;
    chatHistory.forEach(function(m){
      if (m.role === 'user') appendUserMsg(m.content);
      else appendBotMsg(m.content);
    });
  });"""

NEW_RESTORE = """  /* ---- Restore prior conversation + badge on every page load -------- */
  var GREETING_HTML = '';
  document.addEventListener('DOMContentLoaded', function(){
    var body = document.getElementById('chatBody');
    if (body) GREETING_HTML = body.innerHTML;   // pristine greeting, before restore
    setUnread(getUnread());
    if (!chatHistory.length || !body) return;
    chatHistory.forEach(function(m){
      if (m.role === 'user') appendUserMsg(m.content);
      else appendBotMsg(m.content);
    });
  });

  /* ---- Start a fresh conversation ----------------------------------
     Past messages are already stored in Supabase as they happen, so the
     old thread simply moves into "past chats" and the view resets. --- */
  window.startNewChat = function(){
    chatHistory = [];
    saveHistory();
    try { sessionStorage.removeItem('gy_session_id'); } catch(e){}
    if (typeof getSessionId === 'function') getSessionId();  // mint a new one
    _liveBodyHTML = null;
    var body = document.getElementById('chatBody');
    if (body && GREETING_HTML) { body.innerHTML = GREETING_HTML; body.scrollTop = 0; }
    var input = document.getElementById('chatInput');
    if (input) { input.value = ''; input.focus(); }
  };"""

# --- replacement hint behaviour ---
OLD_HINT = """  function shouldShowHint(){
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
  });"""

NEW_HINT = """  var HINT_COUNT_KEY = 'gy_chat_hint_count';
  var CHAT_OPENED_KEY = 'gy_chat_opened';

  function chatWasOpened(){
    try { return !!sessionStorage.getItem(CHAT_OPENED_KEY); } catch(e){ return false; }
  }
  function getHintCount(){
    try { return parseInt(sessionStorage.getItem(HINT_COUNT_KEY) || '0', 10) || 0; } catch(e){ return 0; }
  }
  function bumpHintCount(){
    try { sessionStorage.setItem(HINT_COUNT_KEY, String(getHintCount() + 1)); } catch(e){}
  }

  window.dismissChatHint = function(){
    var el = document.getElementById('chatHint');
    if(el) el.classList.remove('show');
  };

  window.tryShowChatHint = function(){
    if(_hintShownThisSession) return;          // once per page load
    if(chatWasOpened()) return;                // never again once chat is used
    var panel = document.getElementById('chatPanel');
    if(panel && panel.classList.contains('open')) return;
    if(!positionHintAboveTrigger()) return;

    var isFirst = getHintCount() === 0;
    var delay    = isFirst ? 0    : 2500;      // later pages wait a little longer
    var duration = isFirst ? 9000 : 4000;      // ...and show only briefly

    _hintShownThisSession = true;
    setTimeout(function(){
      if(chatWasOpened()) return;
      var el = document.getElementById('chatHint');
      if(!el) return;
      positionHintAboveTrigger();
      el.classList.add('show');
      bumpHintCount();
      setTimeout(function(){ window.dismissChatHint(); }, duration);
    }, delay);
  };

  window.addEventListener('resize', function(){
    var hint = document.getElementById('chatHint');
    if(hint && hint.classList.contains('show')) positionHintAboveTrigger();
  });
  document.addEventListener('click', function(e){
    if(e.target.closest('.chat-trigger')){
      try { sessionStorage.setItem(CHAT_OPENED_KEY, '1'); } catch(e){}
      window.dismissChatHint();
    }
  });"""

count = 0
for page in glob.glob('*.html'):
    with open(page, encoding='utf-8') as f:
        s = f.read()
    if 'startNewChat' in s:
        print(f"SKIP (already done): {page}"); continue
    if HIST_BTN_ANCHOR not in s:
        continue

    ok = True
    s = s.replace(HIST_BTN_ANCHOR, NEW_BTN + HIST_BTN_ANCHOR, 1)

    if OLD_RESTORE in s:
        s = s.replace(OLD_RESTORE, NEW_RESTORE, 1)
    else:
        print(f"NO MATCH (restore block): {page}"); ok = False

    if OLD_HINT in s:
        s = s.replace(OLD_HINT, NEW_HINT, 1)
    else:
        print(f"NO MATCH (hint block): {page}"); ok = False

    if not ok:
        continue

    with open(page, 'w', encoding='utf-8') as f:
        f.write(s)
    print(f"UPDATED: {page}")
    count += 1

print(f"\nTotal pages updated: {count}")
print("Now append the CSS:  cat newchat_css.css >> css/styles.css")
