#!/usr/bin/env python3
"""Dedupe research items by normalized URL + title hash. Input: JSON list file with url/title keys."""
import sys, json, hashlib, re
def norm(u): return re.sub(r"[#?].*$","",u.lower().strip()).rstrip("/")
items=json.load(open(sys.argv[1])); seen={}; out=[]
for it in items:
    k=norm(it.get("url","")) or hashlib.md5(it.get("title","").lower().encode()).hexdigest()
    if k not in seen: seen[k]=1; out.append(it)
print(json.dumps({"input":len(items),"unique":len(out),"duplicates_removed":len(items)-len(out),"items":out},indent=2))
