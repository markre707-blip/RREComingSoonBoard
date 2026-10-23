# Builds site/index.html from data.csv (the RRE Board Data sheet) + template.html
import csv, json, sys
rows = list(csv.DictReader(open("data.csv", encoding="utf-8-sig")))
if not rows or "address" not in rows[0]:
    sys.exit("data.csv doesn't look like the board data; keeping yesterday's page")
NUM = {"price", "beds", "baths", "sqft"}
DATES = {"go_live", "on_market", "pending", "closed", "as_of"}
import re
def iso(v):
    m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", v)
    return f"{m[3]}-{int(m[1]):02d}-{int(m[2]):02d}" if m else v[:10]
out = []
for r in rows:
    p = {}
    for k, val in r.items():
        val = (val or "").strip()
        if k in DATES and val: val = iso(val)
        if k == "as_of": r["as_of"] = val; continue
        if k in NUM: p[k] = float(val.replace(",", "").replace("$", "")) if val else None
        else: p[k] = val or None
    out.append(p)
as_of = max(r.get("as_of") or "" for r in rows)
data = json.dumps({"as_of": as_of, "rows": out}, separators=(",", ":")).replace("</", "<\\/")
import os; os.makedirs("site", exist_ok=True)
open("site/index.html", "w").write(open("template.html").read().replace("__DATA__", data))
print(f"Built board for {as_of}: {len(out)} rows")
