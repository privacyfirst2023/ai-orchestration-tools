#!/usr/bin/env python3
"""Fetch public URL, extract title+text with stdlib only (no bs4 needed). Saves JSON."""
import sys, json, hashlib, re, urllib.request
from html.parser import HTMLParser
class T(HTMLParser):
    def __init__(self): super().__init__(); self.txt=[]; self.title=""; self._t=False; self._skip=False
    def handle_starttag(self,tag,attrs):
        if tag=="title": self._t=True
        if tag in ("script","style","nav"): self._skip=True
    def handle_endtag(self,tag):
        if tag=="title": self._t=False
        if tag in ("script","style","nav"): self._skip=False
    def handle_data(self,d):
        if self._t: self.title+=d
        elif not self._skip and d.strip(): self.txt.append(d.strip())
def fetch(url):
    req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 MuseOrchestration/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r: html=r.read().decode("utf-8","ignore"); status=r.status
    p=T(); p.feed(html); text=re.sub(r"\s+"," "," ".join(p.txt))
    return {"url":url,"status":status,"title":p.title.strip(),"chars":len(text),"sha256":hashlib.sha256(text.encode()).hexdigest()[:16],"text_preview":text[:2000]}
if __name__=="__main__": print(json.dumps(fetch(sys.argv[1]),indent=2))
