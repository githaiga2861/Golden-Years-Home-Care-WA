#!/usr/bin/env python3
"""Adds the 'ask us anything' chat hint tooltip to every page that has
the chat widget. Run from inside the repo root."""
import glob

hint_html = open('chat_hint_html.html', encoding='utf-8').read().strip()
hint_js = open('chat_hint_js.html', encoding='utf-8').read()

anchor = '<div class="chat-panel" id="chatPanel">'

count = 0
EXCLUDE = {'chat_hint_html.html','chat_hint_js.html'}
for page in glob.glob('*.html'):
    if page in EXCLUDE: continue
    with open(page, encoding='utf-8') as f:
        s = f.read()
    if 'chatHint' in s:
        print(f"SKIP (already has it): {page}"); continue
    if anchor not in s:
        continue  # page has no chat widget, skip silently
    s = s.replace(anchor, hint_html + '\n' + anchor, 1)
    s = s.replace('</body>', hint_js + '\n</body>', 1)
    with open(page, 'w', encoding='utf-8') as f:
        f.write(s)
    print(f"ADDED: {page}")
    count += 1

print(f"\nTotal pages updated: {count}")
print("Now append the CSS: cat chat_hint_css.css >> css/styles.css")
