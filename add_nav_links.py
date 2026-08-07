#!/usr/bin/env python3
"""Adds a 'Reviews' nav link to every Home Care WA public page.
Run from inside ~/Golden-Years-Home-Care-WA after placing reviews.html and index.html."""
PAGES = ['index.html','services.html','why-us.html','locations.html','contact.html','reviews.html']
for page in PAGES:
    try:
        with open(page, encoding='utf-8') as f: s = f.read()
    except FileNotFoundError:
        print(f"SKIP (not found): {page}"); continue
    if '"/reviews"' in s:
        print(f"SKIP (already has Reviews link): {page}"); continue
    changed = False
    if '<li data-nav="contact"><a href="/contact">Contact</a></li>' in s:
        s = s.replace('<li data-nav="contact"><a href="/contact">Contact</a></li>',
                       '<li data-nav="reviews"><a href="/reviews">Reviews</a></li>\n      <li data-nav="contact"><a href="/contact">Contact</a></li>', 1)
        changed = True
    if '<a class="mm-item" href="/contact">Contact Us</a>' in s:
        s = s.replace('<a class="mm-item" href="/contact">Contact Us</a>',
                       '<a class="mm-item" href="/reviews">Reviews</a><a class="mm-item" href="/contact">Contact Us</a>', 1)
        changed = True
    if changed:
        with open(page, 'w', encoding='utf-8') as f: f.write(s)
        print(f"UPDATED: {page}")
    else:
        print(f"NO MATCH FOUND (check manually): {page}")
