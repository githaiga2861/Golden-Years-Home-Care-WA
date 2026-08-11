#!/usr/bin/env python3
VERCEL_DOMAIN = "golden-years-websites-admin.vercel.app"

PAGES = ['index.html','services.html','why-us.html','locations.html','contact.html','reviews.html']

OLD_PANEL = '''<div class="chat-panel" id="chatPanel">
  <div class="chat-panel__head">
    <img src="/images/logo.png" alt="Golden Years Home Care WA logo">
    <div><strong>Golden Years Home Care WA</strong><span>Typically replies within a day</span></div>
    <button class="chat-panel__close" onclick="closeChatPanel()" aria-label="Close chat"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18M6 6l12 12"/></svg></button>
  </div>
  <div class="chat-panel__body">
    <div class="chat-msg">
      <img src="/images/logo.png" alt="">
      <div class="chat-msg__bubble"><strong>Golden Years Home Care WA</strong><br>Hi there! \U0001F44B Our live chat is being built right now and is coming very soon. In the meantime, tap "Get Care Now" below or give us a call \u2014 a real person is always happy to help.</div>
    </div>
    <div class="chat-typing"><span></span><span></span><span></span></div>
  </div>
  <div class="chat-panel__foot">
    <input type="text" placeholder="Live chat coming soon\u2026" disabled>
  </div>
</div>'''

NEW_PANEL = '''<div class="chat-panel" id="chatPanel">
  <div class="chat-panel__head">
    <img src="/images/logo.png" alt="Golden Years Home Care WA logo">
    <div><strong>Golden Years Home Care WA</strong><span>Ask us anything</span></div>
    <button class="chat-panel__close" onclick="closeChatPanel()" aria-label="Close chat"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18M6 6l12 12"/></svg></button>
  </div>
  <div class="chat-panel__body" id="chatBody">
    <div class="chat-msg">
      <img src="/images/logo.png" alt="">
      <div class="chat-msg__bubble"><strong>Golden Years Home Care WA</strong><br>Hi there! \U0001F44B I'm here to answer questions about home care for your family. How can I help?</div>
    </div>
  </div>
  <div class="chat-panel__foot">
    <form id="chatForm" onsubmit="return sendChatMessage(event);" style="display:flex;gap:8px">
      <input type="text" id="chatInput" placeholder="Type your question\u2026" autocomplete="off">
      <button type="submit" class="chat-send" aria-label="Send message"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2 11 13M22 2l-7 20-4-9-9-4 20-7Z"/></svg></button>
    </form>
  </div>
</div>'''

CHAT_JS = '''<script>
(function(){
  var CHAT_ENDPOINT = 'https://''' + VERCEL_DOMAIN + '''/api/chat';
  var CHAT_SITE = 'hcwa';
  var chatHistory = [];
  var chatBusy = false;

  function escChat(s){return (s||'').replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}

  function appendUserMsg(text){
    var body = document.getElementById('chatBody');
    var div = document.createElement('div');
    div.className = 'chat-msg';
    div.style.flexDirection = 'row-reverse';
    div.innerHTML = '<div class="chat-msg__bubble" style="background:var(--teal);color:#fff;border-color:var(--teal);border-radius:14px 14px 4px 14px">'+escChat(text)+'</div>';
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
  }
  function appendBotMsg(text){
    var body = document.getElementById('chatBody');
    var div = document.createElement('div');
    div.className = 'chat-msg';
    div.innerHTML = '<img src="/images/logo.png" alt=""><div class="chat-msg__bubble">'+escChat(text).replace(/\\n/g,'<br>')+'</div>';
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
  }
  function showTyping(){
    var body = document.getElementById('chatBody');
    var div = document.createElement('div');
    div.className = 'chat-typing';
    div.id = 'chatTypingIndicator';
    div.innerHTML = '<span></span><span></span><span></span>';
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
  }
  function hideTyping(){
    var el = document.getElementById('chatTypingIndicator');
    if(el) el.remove();
  }

  window.sendChatMessage = function(e){
    e.preventDefault();
    if(chatBusy) return false;
    var input = document.getElementById('chatInput');
    var text = input.value.trim();
    if(!text) return false;
    input.value = '';
    appendUserMsg(text);
    chatHistory.push({role:'user', content:text});
    chatBusy = true;
    showTyping();

    fetch(CHAT_ENDPOINT, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({site: CHAT_SITE, messages: chatHistory})
    }).then(function(r){ return r.json().then(function(data){ return {ok:r.ok, data:data}; }); })
      .then(function(res){
        hideTyping();
        if(res.ok && res.data.reply){
          appendBotMsg(res.data.reply);
          chatHistory.push({role:'assistant', content:res.data.reply});
        } else {
          appendBotMsg(res.data.error || "Sorry, something went wrong. Please call (206) 717-1234.");
        }
        chatBusy = false;
      })
      .catch(function(){
        hideTyping();
        appendBotMsg("I'm having trouble connecting right now \u2014 please call (206) 717-1234.");
        chatBusy = false;
      });
    return false;
  };
})();
</script>
'''

for page in PAGES:
    try:
        with open(page, encoding='utf-8') as f: s = f.read()
    except FileNotFoundError:
        print(f"SKIP (not found): {page}"); continue
    if 'chatBody' in s:
        print(f"SKIP (already activated): {page}"); continue
    if OLD_PANEL not in s:
        print(f"NO MATCH — check manually: {page}"); continue
    s = s.replace(OLD_PANEL, NEW_PANEL, 1)
    s = s.replace('</body>', CHAT_JS + '\n</body>', 1)
    with open(page, 'w', encoding='utf-8') as f: f.write(s)
    print(f"ACTIVATED: {page}")
