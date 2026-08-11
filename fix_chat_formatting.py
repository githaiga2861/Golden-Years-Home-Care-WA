#!/usr/bin/env python3
"""Fixes two chatbot bugs on every page:
1. Horizontal scrolling on long messages
2. Literal ** markdown showing instead of bold, and non-clickable
   phone/email/links.
Run from inside the repo root (works for BOTH the main site and
Home Care WA repos — same fix applies to both)."""
import glob

OLD = '''  function appendBotMsg(text){
    var body = document.getElementById('chatBody');
    var div = document.createElement('div');
    div.className = 'chat-msg';
    var safe = escChat(text).replace(/\\n/g,'<br>');
    safe = safe.replace(/\\(206\\) 717-1234/g, '<a href="tel:+12067171234" style="color:inherit;text-decoration:underline">(206) 717-1234</a>');
    div.innerHTML = '<img src="/images/logo.png" alt=""><div class="chat-msg__bubble">'+safe+'</div>';
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
  }'''

NEW = '''  function formatBotMessage(text){
    var safe = escChat(text);
    safe = safe.replace(/\\*\\*(.+?)\\*\\*/g, '<strong class="chat-bold">$1</strong>');
    safe = safe.replace(/([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,})/g, function(m){
      return '<a href="mailto:'+m+'" class="chat-link">'+m+'</a>';
    });
    safe = safe.replace(/\\(?\\d{3}\\)?[\\s.-]?\\d{3}[\\s.-]?\\d{4}/g, function(m){
      var digits = m.replace(/\\D/g,'');
      if(digits.length !== 10) return m;
      return '<a href="tel:+1'+digits+'" class="chat-link">'+m+'</a>';
    });
    safe = safe.replace(/(https?:\\/\\/[^\\s<]+)/g, function(m){
      return '<a href="#" class="chat-link chat-ext-link" data-href="'+m+'">'+m+'</a>';
    });
    safe = safe.replace(/\\n/g,'<br>');
    return safe;
  }
  function appendBotMsg(text){
    var body = document.getElementById('chatBody');
    var div = document.createElement('div');
    div.className = 'chat-msg';
    var safe = formatBotMessage(text);
    div.innerHTML = '<img src="/images/logo.png" alt=""><div class="chat-msg__bubble">'+safe+'</div>';
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
  }
  document.addEventListener('click', function(e){
    var link = e.target.closest('.chat-ext-link');
    if(link){
      e.preventDefault();
      var url = link.getAttribute('data-href');
      if(confirm('This link will take you to another page:\\n'+url+'\\n\\nContinue?')){
        window.open(url, '_blank', 'noopener');
      }
    }
  });'''

count = 0
for page in glob.glob('*.html'):
    with open(page, encoding='utf-8') as f:
        s = f.read()
    if 'formatBotMessage' in s:
        print(f"SKIP (already fixed): {page}"); continue
    if OLD not in s:
        continue  # page has no chatbot, skip silently
    s = s.replace(OLD, NEW, 1)
    with open(page, 'w', encoding='utf-8') as f:
        f.write(s)
    print(f"FIXED: {page}")
    count += 1

print(f"\\nTotal pages fixed: {count}")
print("Now append the CSS: cat chat_fix_css.css >> css/styles.css")
