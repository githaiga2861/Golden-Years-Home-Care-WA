#!/usr/bin/env python3
"""Fixes checkbox misalignment: .optin had 13px of horizontal padding that
.consent doesn't have, pushing it out of alignment. Removes the horizontal
padding so both checkboxes start at the exact same left edge.
Run from inside either site repo root."""
f = 'css/styles.css'
s = open(f, encoding='utf-8').read()

old = """.optin{display:flex;gap:11px;align-items:flex-start;font-size:.86rem;color:var(--slate);margin-bottom:22px;
  border:1px solid var(--line);border-radius:10px;padding:11px 13px;transition:border-color .2s;cursor:pointer}"""

new = """.optin{display:flex;gap:11px;align-items:flex-start;font-size:.86rem;color:var(--slate);margin-bottom:22px;
  border:1px solid var(--line);border-radius:10px;padding:9px 0;transition:border-color .2s;cursor:pointer}"""

if old not in s:
    print("Pattern not found — checking if already fixed or CSS differs.")
    raise SystemExit(1)

s = s.replace(old, new, 1)
open(f, 'w', encoding='utf-8').write(s)
print("Fixed: removed the 13px horizontal padding causing the misalignment")
