#!/usr/bin/env python3
"""Assemble the final index.html from parts + script blocks."""

import os

BASE = '/home/user/workspace/ductulator-pro'

def read(path):
    with open(os.path.join(BASE, path), 'r') as f:
        return f.read()

# Read all parts
parts = [
    read('parts/01-head.html'),
    read('parts/02-css.html'),
    read('parts/02b-dynamic-css.html') + '\n</style>',  # inserted before closing style from 02-css
    read('parts/03-body-start.html'),
    read('parts/04-page-home.html'),
    read('parts/05-pages.html'),
    read('parts/06-footer-nav.html'),
    read('parts/07-scripts-end.html'),
]

# Join parts
html = '\n'.join(parts)

# Read script blocks
sb1 = read('script-block-1.js')
sb2 = read('script-block-2.js')
sb3 = read('script-block-3.js')

# Insert script blocks
html = html.replace('%%SCRIPT_BLOCK_1%%', sb1)
html = html.replace('%%SCRIPT_BLOCK_2%%', sb2)
html = html.replace('%%SCRIPT_BLOCK_3%%', sb3)

# Write final
out = os.path.join(BASE, 'index.html')
with open(out, 'w') as f:
    f.write(html)

# Count
lines = html.count('\n') + 1
print(f"Written {out}: {len(html)} bytes, {lines} lines")
