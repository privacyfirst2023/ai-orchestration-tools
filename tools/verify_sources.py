#!/usr/bin/env python3
"""Verify a list of URLs are live and report title/status. Input: one URL per line file."""
import sys, json
sys.path.insert(0, __file__.rsplit("/",1)[0])
from fetch_and_extract import fetch
out=[]
for u in [l.strip() for l in open(sys.argv[1]) if l.strip()]:
    try: f=fetch(u); out.append({"url":u,"live":f["status"]==200,"status":f["status"],"title":f["title"]})
    except Exception as e: out.append({"url":u,"live":False,"error":str(e)[:120]})
print(json.dumps(out,indent=2))
