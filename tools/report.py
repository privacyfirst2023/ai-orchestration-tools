#!/usr/bin/env python3
"""Report generation: build a Markdown report from JSON result files in a directory.
Usage: report.py <results_dir> <title> > report.md  - summarizes each JSON file generically."""
import sys, json, pathlib
d=pathlib.Path(sys.argv[1]); title=sys.argv[2] if len(sys.argv)>2 else "Report"
print(f"# {title}\n")
for f in sorted(d.glob("*.json")):
    print(f"## {f.stem}\n")
    try: data=json.loads(f.read_text())
    except Exception as e: print(f"_unreadable: {e}_\n"); continue
    if isinstance(data, dict):
        for k,v in data.items():
            if isinstance(v,(dict,list)): print(f"- **{k}**: `{json.dumps(v)[:300]}`")
            else: print(f"- **{k}**: {v}")
    elif isinstance(data, list):
        print(f"- items: {len(data)}")
        for it in data[:10]: print(f"  - `{json.dumps(it)[:200]}`")
    print()
