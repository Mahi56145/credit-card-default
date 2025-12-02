# tools/patch_index_for_static.py
from pathlib import Path
import re
p_dist = Path("ui/dist")
p_index = p_dist / "index.html"

if not p_index.exists():
    raise SystemExit("ERROR: ui/dist/index.html not found. Build the UI and ensure ui/dist exists.")

assets = list((p_dist / "assets").glob("*"))
js_files = [a.name for a in assets if a.suffix == ".js"]
css_files = [a.name for a in assets if a.suffix == ".css"]

if not js_files and not css_files:
    raise SystemExit("ERROR: no js/css found in ui/dist/assets. Did the build succeed?")

print("Found JS:", js_files)
print("Found CSS:", css_files)

backup = p_index.with_suffix(".html.bak2")
p_index.write_text(p_index.read_text(encoding="utf8"), encoding="utf8")  # ensure utf8
# create a safe backup only if not exists
if not backup.exists():
    backup.write_text(p_index.read_text(encoding="utf8"), encoding="utf8")
    print("Backup created at", backup)

html = p_index.read_text(encoding="utf8")

# Ensure asset references include the /static prefix. Replace occurrences of src="/assets/... or src="assets/...
html = re.sub(r'(src|href)\s*=\s*"(?:/)?assets/', r'\1="/static/assets/', html)

# Replace wildcard placeholders or <some js> like tokens by the actual filename(s).
# If index.html contains a token like <some js> or index-*.js the following will attempt to replace:
# Find the first JS tag and replace its filename to the actual first JS, same for CSS.
# Replace any index-*.js entry with actual js name
if js_files:
    html = re.sub(r'index-([a-zA-Z0-9_\-\.]+)\.js', js_files[0], html)
    # also replace tokens like <some js> or <some_js>
    html = re.sub(r'<[^>]*some[^>]*js[^>]*>', js_files[0], html)

if css_files:
    html = re.sub(r'index-([a-zA-Z0-9_\-\.]+)\.css', css_files[0], html)
    html = re.sub(r'<[^>]*some[^>]*css[^>]*>', css_files[0], html)

# As a final safety, ensure /static/assets/ prefix is present for the actual filenames we are referencing
for f in js_files + css_files:
    html = html.replace(f, f"/static/assets/{f}")

p_index.write_text(html, encoding="utf8")
print("Patched ui/dist/index.html -> now references /static/assets/<actual filenames>")
