#!/usr/bin/env python3
"""Adds an 'Articles' nav link to every existing HCWA page (desktop + mobile).
Run from inside ~/Golden-Years-Home-Care-WA, AFTER placing article.html
and articles.html in the repo root."""
import glob

PAGES = ['index.html','services.html','why-us.html','locations.html','contact.html','reviews.html','articles.html','article.html']

count = 0
for page in PAGES:
    try:
        with open(page, encoding='utf-8') as f: s = f.read()
    except FileNotFoundError:
        print(f"SKIP (not found): {page}"); continue
    if '"/articles"' in s and 'data-nav="articles"' in s:
        print(f"SKIP (already has it): {page}"); continue
    changed = False
    old_nav = '<li data-nav="reviews"><a href="/reviews">Reviews</a></li>'
    new_nav = '<li data-nav="articles"><a href="/articles">Articles</a></li>\n      <li data-nav="reviews"><a href="/reviews">Reviews</a></li>'
    if old_nav in s:
        s = s.replace(old_nav, new_nav, 1)
        changed = True
    old_mm = '<a class="mm-item" href="/reviews">Reviews</a>'
    new_mm = '<a class="mm-item" href="/articles">Articles</a><a class="mm-item" href="/reviews">Reviews</a>'
    if old_mm in s:
        s = s.replace(old_mm, new_mm, 1)
        changed = True
    if changed:
        with open(page, 'w', encoding='utf-8') as f: f.write(s)
        print(f"UPDATED: {page}")
        count += 1
    else:
        print(f"NO MATCH — check manually: {page}")

print(f"\nTotal pages updated: {count}")
