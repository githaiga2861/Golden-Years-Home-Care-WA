#!/usr/bin/env python3
"""Adds saved-chat history to the chat widget:
 - a small history button in the panel header (panel size unchanged)
 - a history view that swaps into the existing body
 - visitor/session IDs sent with each message so the backend can log them
Run from inside either site repo root."""
import glob, os

SB = {
    'main': ('https://uldywugntkykeftuzxys.supabase.co', 'sb_publishable_kCCHxG8VAO_APnGWxCgLDg_Wj6Vxjj7'),
    'hcwa': ('https://styzbftuzuqcnkwvwpgm.supabase.co', 'sb_publishable_vgZaJznqe7aI_TJ8gV8ynw_UPgSsifR'),
}

HIST_BTN = ('<button class="chat-hist-btn" onclick="showChatHistory()" aria-label="View past chats" title="Past chats">'
            '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'
            '</svg></button>')

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history_js_block.txt'), encoding='utf-8') as f:
    HIST_JS_TEMPLATE = f.read()

count = 0
for page in glob.glob('*.html'):
    with open(page, encoding='utf-8') as f:
        s = f.read()

    if 'showChatHistory' in s:
        print(f"SKIP (already done): {page}"); continue
    if 'var CHAT_ENDPOINT' not in s:
        continue

    site = 'main' if "CHAT_SITE = 'main'" in s else 'hcwa'
    sb_url, sb_key = SB[site]

    # 1) Header button, immediately before the close button
    close_btn = '<button class="chat-panel__close" onclick="closeChatPanel()" aria-label="Close chat">'
    if close_btn not in s:
        print(f"NO MATCH (header): {page}"); continue
    s = s.replace(close_btn, HIST_BTN + close_btn, 1)

    # 2) Send visitor/session IDs with each request
    old_body = "body: JSON.stringify({site: CHAT_SITE, messages: chatHistory})"
    new_body = "body: JSON.stringify({site: CHAT_SITE, messages: chatHistory, visitorId: getVisitorId(), sessionId: getSessionId()})"
    if old_body not in s:
        print(f"NO MATCH (request body): {page}"); continue
    s = s.replace(old_body, new_body, 1)

    # 3) Inject the history logic just before the chat IIFE closes
    hist_js = HIST_JS_TEMPLATE.replace('__SB_URL__', sb_url).replace('__SB_KEY__', sb_key)
    anchor = "  /* Opening the chat marks everything as read */"
    if anchor not in s:
        print(f"NO MATCH (anchor): {page}"); continue
    s = s.replace(anchor, hist_js + "\n" + anchor, 1)

    with open(page, 'w', encoding='utf-8') as f:
        f.write(s)
    print(f"UPDATED: {page}")
    count += 1

print(f"\nTotal pages updated: {count}")
print("Now append the CSS:  cat chat_history_css.css >> css/styles.css")
