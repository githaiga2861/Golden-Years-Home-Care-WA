#!/usr/bin/env python3
"""Fixes the 'Moving to a Facility' card on the homepage: its downside
items were using the same affirmative blue checkmark as the 'Staying
Home' card. This gives it a distinct X icon in a muted amber tone.
Run from inside ~/Golden-Years-Home-Care-WA."""

# 1) HTML fix
f = 'index.html'
s = open(f, encoding='utf-8').read()
old = '<h3><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>Moving to a Facility</h3><ul class="checks">'
new = '<h3><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>Moving to a Facility</h3><ul class="checks checks--con">'
if old in s:
    s = s.replace(old, new, 1)
    open(f, 'w', encoding='utf-8').write(s)
    print("HTML fixed: index.html")
else:
    print("WARNING: pattern not found in index.html — no changes made")

# 2) CSS addition
css_addition = '''
/* Comparison list: downside items get an X in a muted amber tone, NOT a checkmark */
.checks--con li::before{
  background:#faf1e0;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23a7842f' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='18' y1='6' x2='6' y2='18'/%3E%3Cline x1='6' y1='6' x2='18' y2='18'/%3E%3C/svg%3E");
}
'''
css_file = 'css/styles.css'
css = open(css_file, encoding='utf-8').read()
if '.checks--con li::before' not in css:
    with open(css_file, 'a', encoding='utf-8') as f2:
        f2.write(css_addition)
    print("CSS added to css/styles.css")
else:
    print("SKIP: CSS already present")
