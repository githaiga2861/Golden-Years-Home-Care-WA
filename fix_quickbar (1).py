#!/usr/bin/env python3
"""Compacts the sticky quickbar: single-line on mobile (icon + hidden
sentence + minimized buttons), slightly shorter on desktop.
Run from inside the repo root, targeting css/styles.css."""

f = 'css/styles.css'
s = open(f, encoding='utf-8').read()

# 1) Slightly reduce desktop bar height
old1 = '.quickbar__inner{max-width:var(--maxw);margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:13px 24px;flex-wrap:wrap}'
new1 = '.quickbar__inner{max-width:var(--maxw);margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:10px 24px;flex-wrap:wrap}'
if old1 in s:
    s = s.replace(old1, new1, 1)
    print("Desktop height reduced")
else:
    print("WARNING: desktop rule not found, skipped")

# 2) Replace the old mobile rule with a real compact single-line layout
# Handle both known formats of the old mobile rule (single-line and multi-line)
old2_variants = [
    '@media(max-width:600px){.quickbar__inner{justify-content:center;text-align:center}}',
    '.quickbar__inner{justify-content:center;text-align:center}'
]
new2_rule = '''.quickbar__inner{flex-wrap:nowrap;justify-content:space-between;align-items:center;padding:8px 12px;gap:8px;overflow-x:auto}
  .quickbar__txt{font-size:0;gap:0;flex-shrink:0}
  .quickbar__txt svg{width:20px;height:20px}
  .quickbar__cta{gap:6px;flex-wrap:nowrap;flex-shrink:0}
  .quickbar .btn{padding:7px 12px;font-size:.72rem;white-space:nowrap}
  .chat-trigger{width:34px;height:34px;flex-shrink:0}
  .chat-trigger svg{width:17px;height:17px}
  .chat-badge{width:15px;height:15px;font-size:.6rem;top:-3px;right:-3px}'''
found = False
for variant in old2_variants:
    if variant in s:
        s = s.replace(variant, new2_rule, 1)
        found = True
        break
if found:
    print("Mobile layout compacted to one line")
else:
    print("WARNING: mobile rule not found, skipped")

open(f, 'w', encoding='utf-8').write(s)
