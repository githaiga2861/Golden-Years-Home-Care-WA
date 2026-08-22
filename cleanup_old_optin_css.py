#!/usr/bin/env python3
"""Removes the old, no-longer-used opt-in card CSS from a previous pass.
Run from inside either site repo root, after fix_optin_markup.py."""
import re
f = 'css/styles.css'
s = open(f, encoding='utf-8').read()
before = len(s)
s = re.sub(
  r'\n/\* --- Clearer marketing opt-in checkbox --- \*/\n'
  r'\.optin-field\{[^}]*\}\n\.optin-label\{[^}]*\}\n\.optin-label:hover\{[^}]*\}\n'
  r'\.optin-label input\[type="checkbox"\]\{[^}]*\}\n\.optin-label span\{[^}]*\}\n\.optin-label strong\{[^}]*\}\n',
  '\n', s)
open(f, 'w', encoding='utf-8').write(s)
print(f"Removed {before-len(s)} bytes of unused CSS" if before != len(s) else "Nothing to remove — already clean")
