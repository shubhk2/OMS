#!/usr/bin/env python3
"""
update_view_links.py

Scan Frontend/src/html and update relative links inside HTML files that were moved
into views/<role>/ so links like "./authentication-login.html" and "./index.html"
are fixed to the deeper paths (../../html/authentication-login.html and
../../html/views/<role>/index.html).

It writes a .bak backup for every file it modifies and prints changed files.
"""
import os
import re

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Frontend', 'src', 'html'))

def update_file(path, role):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    new_text = text
    # auth page
    new_text = re.sub(r"(\./authentication-login\.html|\.\./authentication-login\.html|/authentication-login\.html)",
                      r'../../html/authentication-login.html', new_text)
    # index: role-specific under views
    role_index = f"../../html/views/{role}/index.html"
    new_text = re.sub(r"(\./index\.html|\.\./index\.html|/index\.html)", role_index, new_text)

    # assets (css/js/img) -> from views/<role>/index.html to Frontend/src/assets is ../../../assets/
    # match common forms like "assets/...", "./assets/...", "../assets/...", and "/assets/..."
    # preserve surrounding quote if present
    new_text = re.sub(r'(["\'])(?:\./|\.\./|/)?assets/', r"\1../../../assets/", new_text)
    # also handle unquoted occurrences at line-start or after whitespace by capturing the prefix and reusing it
    new_text = re.sub(r'(^|\s)(?:\./|\.\./|/)?assets/', r"\1../../../assets/", new_text)

    if new_text != text:
        bak = path + '.bak'
        with open(bak, 'w', encoding='utf-8') as b:
            b.write(text)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print(f"Updated {path} (backup: {bak})")


def main():
    if not os.path.isdir(BASE):
        print(f"Base html directory not found: {BASE}")
        return

    for root, dirs, files in os.walk(BASE):
        # look for views/<role> in path
        parts = root.split(os.sep)
        role = None
        if 'views' in parts:
            try:
                vi = parts.index('views')
                role = parts[vi + 1]
            except Exception:
                role = 'employee'
        else:
            # skip non-views folders; leave top-level html alone
            continue

        for fn in files:
            if not fn.lower().endswith('.html'):
                continue
            path = os.path.join(root, fn)
            update_file(path, role)

if __name__ == '__main__':
    main()
