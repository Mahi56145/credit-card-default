# tools/patch_index_for_static2.py
import os
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]      # project root
dist = root / "ui" / "dist"
assets = dist / "assets"
index = dist / "index.html"

if not dist.exists() or not assets.exists() or not index.exists():
    raise SystemExit("ERROR: expected ui/dist and ui/dist/assets and ui/dist/index.html to exist. cwd: %s" % root)

# list actual asset filenames
js_files = [p.name for p in assets.glob("*.js")]
css_files = [p.name for p in assets.glob("*.css")]

if not js_files:
    raise SystemExit("No .js files found in ui/dist/assets")
# pick the first matching main js/css
js_name = js_files[0]
css_name = css_files[0] if css_files else None

text = index.read_text(encoding="utf-8")

# Replace any existing /static/assets/... occurrences to the canonical ones.
# Remove duplicated "/static/assets/" occurrences and normalize to "/static/assets/<file>"
# Replace first <script ... src="..."> and <link ... href="..."> patterns.

# General approach: replace any src="/...index-*.js" or src="...index-*.js" with /static/assets/<js_name>
text = re.sub(r'src="[^"]*index-[^"]*\.js"', f'src="/static/assets/{js_name}"', text)
if css_name:
    text = re.sub(r'href="[^"]*index-[^"]*\.css"', f'href="/static/assets/{css_name}"', text)

# Also ensure we don't have doubled parts like /static/assets//static/assets/...
text = text.replace("//static/assets/", "/static/assets/")

# backup original just in case
bak = dist / "index.html.bak"
bak.write_text(index.read_text(encoding="utf-8"), encoding="utf-8")
index.write_text(text, encoding="utf-8")

print("Patched", index)
print("JS ->", js_name)
print("CSS ->", css_name)
print("Backup saved to", bak)
