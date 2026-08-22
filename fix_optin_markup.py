#!/usr/bin/env python3
"""Restyles the marketing opt-in checkbox to match the existing consent
checkbox's plain layout exactly (same width, same row style), keeping
only the bold lead-in text and the blue hover border.
Run from inside either site repo root, AFTER fix_all.py has already run."""
import glob, re

OLD_BLOCK_RE = re.compile(
    r'<div class="field optin-field">\s*'
    r'<label class="optin-label">\s*'
    r'<input type="checkbox" id="([^"]+)">\s*'
    r'<span><strong>Keep me updated\.</strong> ([^<]+)</span>\s*'
    r'</label>\s*'
    r'</div>\s*'
)

NEW_TEMPLATE = ('<div class="optin"><input id="{id}" type="checkbox">'
                 '<label for="{id}"><strong>Keep me updated.</strong> {rest}</label></div>\n')

count = 0
for page in glob.glob('*.html'):
    s = open(page, encoding='utf-8').read()
    if 'optin-field' not in s:
        continue
    def repl(m):
        return NEW_TEMPLATE.format(id=m.group(1), rest=m.group(2))
    new_s, n = OLD_BLOCK_RE.subn(repl, s)
    if n:
        open(page, 'w', encoding='utf-8').write(new_s)
        print(f"RESTYLED ({n}): {page}")
        count += n

print(f"\nTotal checkboxes restyled: {count}")
