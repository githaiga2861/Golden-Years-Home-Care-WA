#!/usr/bin/env python3
"""Adds session-persistent chat history + accurate unread badge.
Run from inside either site repo root."""
import glob

OLD_HEAD = """  var CHAT_SITE = '__SITE__';
  var chatHistory = [];
  var chatBusy = false;
"""

NEW_HEAD = """  var CHAT_SITE = '__SITE__';
  var chatBusy = false;

  /* ---- Session persistence -------------------------------------------
     History survives page-to-page navigation, but is cleared on a refresh
     (the Navigation Timing API tells us which one happened). ---------- */
  var HIST_KEY = 'gy_chat_history';
  var UNREAD_KEY = 'gy_chat_unread';

  function wasReload(){
    try {
      var nav = performance.getEntriesByType('navigation')[0];
      return !!nav && nav.type === 'reload';
    } catch(e){ return false; }
  }
  if (wasReload()){
    try { sessionStorage.removeItem(HIST_KEY); sessionStorage.removeItem(UNREAD_KEY); } catch(e){}
  }

  var chatHistory = [];
  try {
    var _saved = sessionStorage.getItem(HIST_KEY);
    if (_saved) chatHistory = JSON.parse(_saved) || [];
  } catch(e){ chatHistory = []; }

  function saveHistory(){
    try { sessionStorage.setItem(HIST_KEY, JSON.stringify(chatHistory.slice(-20))); } catch(e){}
  }

  /* ---- Unread badge --------------------------------------------------
     Starts at 1 for the greeting. Clears the moment the panel is opened,
     and stays cleared across pages for the rest of the session. ------- */
  function getUnread(){
    try {
      var v = sessionStorage.getItem(UNREAD_KEY);
      return v === null ? 1 : (parseInt(v, 10) || 0);
    } catch(e){ return 1; }
  }
  function setUnread(n){
    try { sessionStorage.setItem(UNREAD_KEY, String(n)); } catch(e){}
    var badge = document.querySelector('.chat-badge');
    if (!badge) return;
    if (n > 0){ badge.textContent = n; badge.style.display = ''; }
    else { badge.style.display = 'none'; }
  }
  window.__gyClearUnread = function(){ setUnread(0); };
"""

OLD_SEND = """    appendUserMsg(text);
    chatHistory.push({role:'user', content:text});
    chatBusy = true;
    showTyping();
"""
NEW_SEND = """    appendUserMsg(text);
    chatHistory.push({role:'user', content:text});
    saveHistory();
    chatBusy = true;
    showTyping();
"""

OLD_REPLY = """          appendBotMsg(res.data.reply);
          chatHistory.push({role:'assistant', content:res.data.reply});"""
NEW_REPLY = """          appendBotMsg(res.data.reply);
          chatHistory.push({role:'assistant', content:res.data.reply});
          saveHistory();
          var _panel = document.getElementById('chatPanel');
          if (!_panel || !_panel.classList.contains('open')) setUnread(getUnread() + 1);"""

RESTORE_BLOCK = """
  /* ---- Restore prior conversation + badge on every page load -------- */
  document.addEventListener('DOMContentLoaded', function(){
    setUnread(getUnread());
    if (!chatHistory.length) return;
    var body = document.getElementById('chatBody');
    if (!body) return;
    chatHistory.forEach(function(m){
      if (m.role === 'user') appendUserMsg(m.content);
      else appendBotMsg(m.content);
    });
  });

  /* Opening the chat marks everything as read */
  document.addEventListener('click', function(e){
    if (e.target.closest('.chat-trigger')) setUnread(0);
  });
})();
</script>"""

count = 0
for page in glob.glob('*.html'):
    with open(page, encoding='utf-8') as f:
        s = f.read()
    if 'gy_chat_history' in s:
        print(f"SKIP (already done): {page}"); continue
    if 'var CHAT_ENDPOINT' not in s:
        continue

    site = 'main' if "CHAT_SITE = 'main'" in s else 'hcwa'
    oh = OLD_HEAD.replace('__SITE__', site)
    nh = NEW_HEAD.replace('__SITE__', site)
    if oh not in s:
        print(f"NO MATCH (head): {page}"); continue

    s = s.replace(oh, nh, 1)
    if OLD_SEND in s: s = s.replace(OLD_SEND, NEW_SEND, 1)
    if OLD_REPLY in s: s = s.replace(OLD_REPLY, NEW_REPLY, 1)

    # Close out the IIFE with the restore logic (replace only the chat block's ending)
    marker = "    return false;\n  };\n})();\n</script>"
    if marker in s:
        s = s.replace(marker, "    return false;\n  };\n" + RESTORE_BLOCK, 1)
    else:
        print(f"NO MATCH (tail): {page}"); continue

    with open(page, 'w', encoding='utf-8') as f:
        f.write(s)
    print(f"UPDATED: {page}")
    count += 1

print(f"\nTotal pages updated: {count}")
