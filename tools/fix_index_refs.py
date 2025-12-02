# tools/fix_index_refs.py
# Usage: python tools/fix_index_refs.py
# Finds the built JS/CSS in ui/dist/assets and patches ui/dist/index.html placeholders.

import re
import sys
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]  # repo root
DIST = ROOT / "ui" / "dist"
ASSETS = DIST / "assets"
INDEX = DIST / "index.html"

if not DIST.exists():
    print("ERROR: expected ui/dist to exist. Run `npm run build` in ui/ first.")
    sys.exit(1)

if not INDEX.exists():
    print("ERROR: expected ui/dist/index.html to exist.")
    sys.exit(1)

# backup index.html if not done already
bak = DIST / "index.html.bak"
if not bak.exists():
    shutil.copy2(INDEX, bak)
    print(f"Created backup: {bak}")

# list real asset filenames
js_files = sorted([p.name for p in ASSETS.glob("*.js")])
css_files = sorted([p.name for p in ASSETS.glob("*.css")])

if not js_files:
    print("No JS files found in ui/dist/assets — build may have failed.")
    sys.exit(1)

print("JS:", js_files)
print("CSS:", css_files)

html = INDEX.read_text(encoding="utf-8")

# common placeholders that sometimes appear in templates (example: <some js>)
# We'll replace occurrences of patterns like <some js> or <some css> or %JS% with real filenames.
# If you used Vite/React template the file may include a placeholder like <some js>.
# We'll try a few heuristics / patterns and if nothing matches, we do minimal injection.

def safe_replace_placeholder(html_text, placeholder_regex, new_filename):
    new_html = re.sub(placeholder_regex, new_filename, html_text)
    return new_html

# Replace any token that looks like <some js> or &lt;some js&gt; with actual js filename
html2 = html
primary_js = js_files[-1]  # the last one is usually the main bundle with hash
primary_css = css_files[-1] if css_files else None

# Patterns to try (some builds put weird placeholders)
patterns_js = [
    r"&lt;some js&gt;",         # escaped HTML placeholder
    r"<some js>",              # literal placeholder
    r"%3Csome%20js%3E",        # URL-encoded
    r"<\s*some-js\s*>",        # variant
    r"\<\s*some_js\s*\>",      # variant
]
patterns_css = [
    r"&lt;some css&gt;",
    r"<some css>",
    r"%3Csome%20css%3E",
    r"<\s*some-css\s*>",
]

replaced_any = False
for p in patterns_js:
    if re.search(p, html2):
        html2 = safe_replace_placeholder(html2, p, f"assets/{primary_js}")
        print(f"Replaced JS placeholder pattern {p} -> assets/{primary_js}")
        replaced_any = True

for p in patterns_css:
    if primary_css and re.search(p, html2):
        html2 = safe_replace_placeholder(html2, p, f"assets/{primary_css}")
        print(f"Replaced CSS placeholder pattern {p} -> assets/{primary_css}")
        replaced_any = True

# If no placeholder matched, try to find the script tag with something missing and inject filenames:
if not replaced_any:
    # replace any src that contains <some or placeholder-like name inside quotes
    html2, n_js = re.subn(r'src=["\'].*<.*js.*["\']', f'src="assets/{primary_js}"', html2)
    if n_js:
        print(f"Rewrote {n_js} broken script src(s) to assets/{primary_js}")
        replaced_any = True

    if primary_css:
        html2, n_css = re.subn(r'href=["\'].*<.*css.*["\']', f'href="assets/{primary_css}"', html2)
        if n_css:
            print(f"Rewrote {n_css} broken link href(s) to assets/{primary_css}")
            replaced_any = True

if not replaced_any:
    print("Warning: no placeholders matched and no changes made. Please open ui/dist/index.html.bak and inspect placeholders.")
else:
    # write patched index
    INDEX.write_text(html2, encoding="utf-8")
    print(f"Patched {INDEX}. If UI still fails, open ui/dist/index.html.bak and compare.")
