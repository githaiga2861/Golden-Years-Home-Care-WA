#!/usr/bin/env python3
"""Adds the 'coming soon' chat widget to every Home Care WA page's
sticky quickbar. Run from inside ~/Golden-Years-Home-Care-WA."""
PAGES = ['index.html','services.html','why-us.html','locations.html','contact.html','reviews.html']

TRIGGER = '<button class="chat-trigger" onclick="toggleChatPanel()" aria-label="Open chat"><span class="chat-badge">1</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 8.7 8.7 0 0 1-3.8-.9L3 20l1-4.9a8.4 8.4 0 1 1 17-3.6Z"/></svg></button>'

PANEL = '''<div class="chat-panel" id="chatPanel">
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
</div>
'''

JS = '''<script>
window.toggleChatPanel = function(){
  var p = document.getElementById('chatPanel');
  if(p) p.classList.toggle('open');
};
window.closeChatPanel = function(){
  var p = document.getElementById('chatPanel');
  if(p) p.classList.remove('open');
};
document.addEventListener('click', function(e){
  var panel = document.getElementById('chatPanel');
  var trigger = e.target.closest('.chat-trigger');
  if(panel && panel.classList.contains('open') && !panel.contains(e.target) && !trigger){
    panel.classList.remove('open');
  }
});
</script>
'''

OLD_INNER = '<div class="quickbar" id="quickbar"><div class="quickbar__inner">\n  <span class="quickbar__txt">'
NEW_INNER = '<div class="quickbar" id="quickbar"><div class="quickbar__inner">\n  ' + TRIGGER + '\n  <span class="quickbar__txt">'

for page in PAGES:
    try:
        with open(page, encoding='utf-8') as f: s = f.read()
    except FileNotFoundError:
        print(f"SKIP (not found): {page}"); continue
    if 'chat-trigger' in s:
        print(f"SKIP (already has it): {page}"); continue
    if OLD_INNER not in s:
        print(f"NO MATCH — check manually: {page}"); continue
    s = s.replace(OLD_INNER, NEW_INNER, 1)
    marker = '<a class="btn btn--white-outline" href="tel:+12067171234">Call (206) 717-1234</a></span>\n</div></div>'
    if marker in s:
        s = s.replace(marker, marker + '\n' + PANEL, 1)
    s = s.replace('</body>', JS + '\n</body>', 1)
    with open(page, 'w', encoding='utf-8') as f: f.write(s)
    print(f"UPDATED: {page}")

print("\nDone. Now append css_chatwidget.css to css/styles.css:")
print("  cat css_chatwidget.css >> css/styles.css")
