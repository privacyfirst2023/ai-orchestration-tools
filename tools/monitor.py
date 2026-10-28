#!/usr/bin/env python3
"""Website monitoring: hash page text, compare to state file. Exit/report CHANGE or NO_CHANGE."""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from fetch_and_extract import fetch
url=sys.argv[1]; state=pathlib.Path(__file__).parent.parent/"state"/(pathlib.Path(url.replace("https://","").replace("http://","")).name or "site")
state_file=pathlib.Path(str(state)+".json")
cur=fetch(url); prev=json.loads(state_file.read_text()) if state_file.exists() else None
changed = prev is None or prev["sha256"]!=cur["sha256"]
state_file.write_text(json.dumps(cur,indent=2))
print(json.dumps({"url":url,"status":"FIRST_SNAPSHOT" if prev is None else ("CHANGE" if changed else "NO_CHANGE"),"sha256":cur["sha256"],"title":cur["title"]},indent=2))
