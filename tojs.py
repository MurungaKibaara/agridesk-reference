import csv, json
OUT="/home/claude/data"
tables = ["sites","groups","farmers","products","orders","order_items","payments"]
NUM = {"unit_price_cents","line_total_cents","quantity","principal_cents",
       "service_fee_cents","total_due_cents","amount_cents"}
parts = ["// Generated from the CSVs in /data. Do not edit by hand.\n",
         "window.DATA = (function(){\n"]
for t in tables:
    rows = list(csv.DictReader(open(f"{OUT}/{t}.csv")))
    cols = list(rows[0].keys())
    vals = [[int(r[c]) if c in NUM else r[c] for c in cols] for r in rows]
    parts.append(f"const {t}_c={json.dumps(cols)};\n")
    parts.append(f"const {t}_v={json.dumps(vals,separators=(',',':'))};\n")
parts.append("const hydrate=(c,v)=>v.map(r=>Object.fromEntries(r.map((x,i)=>[c[i],x])));\n")
parts.append("return {" + ",".join(f"{t}:hydrate({t}_c,{t}_v)" for t in tables) + "};\n})();\n")
open(f"{OUT}/data.js","w").write("".join(parts))
