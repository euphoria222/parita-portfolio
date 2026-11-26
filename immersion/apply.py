"""Re-apply the site's patches to a fresh export of the portfolio page.

Usage: python3 immersion/apply.py <exported index.html> <output index.html>

The page is a compiled bundle, so each rebuild from the artifact loses these.
Every step is idempotent, so running it on an already-patched page is safe.
"""
import os
import re
import sys

src, out = sys.argv[1], sys.argv[2]
page = open(src, encoding="utf-8").read()
here = os.path.dirname(os.path.abspath(__file__))
layer = open(os.path.join(here, "immersion.html"), encoding="utf-8").read()

# 1. Remove the "skip the dive" button from the intro.
page, n_skip = re.subn(
    r',\(0,\w+\.jsx\)\("button",\{className:"tiny",type:"button",'
    r'onClick:\(\)=>\w+\.current\?\.skip\(\),children:\w+\.skip\}\)',
    "", page)

# 2. Video tiles fetch nothing until they scroll into view (lighter on phones).
page, n_pre = re.subn(r'playsInline:!0,preload:"(?:metadata|auto)",onClick:',
                      'playsInline:!0,preload:"none",onClick:', page)

# 3. Immersion layer (replace an older copy if one is already there).
page = re.sub(r'<!-- Immersion layer:.*?<script id="amb-script">.*?</script>\n*', "", page, flags=re.S)
cut = page.rfind("</body>")
layer = layer.rstrip("\n") + "\n"
page = page[:cut] + layer + page[cut:] if cut != -1 else page + layer

open(out, "w", encoding="utf-8").write(page)
print(f"skip button removed: {n_skip}  video preload set: {n_pre}  immersion: {'amb-script' in page}")
