#!/usr/bin/env python3
"""Intelligent task router - $0 cost guard. Routes by task type, not by hype.
Priorities: 1 deterministic code, 2 local VM, 3 external free cloud (only if advantage + authorized),
4 included AI agent tools (browser.search, subagents), 5 Muse reasoning for planning/QC.
Usage: python3 router.py "analyze this csv"  |  python3 router.py --json "monitor https://..."
"""
import re, sys, json

ROUTES = [
    ("deterministic_code", r"\b(csv|spreadsheet|excel|count|sum|average|sort|filter|dedupe|duplicate|parse|convert|hash|extract (emails|links|numbers))\b",
     "tools/csv_analysis.py or tools/dedupe.py", "local_vm", "Code is exact, free, reproducible. No AI tokens wasted."),
    ("web_monitoring", r"\b(monitor|watch|changed|alert.*when|check.*daily|track.*price|restock)\b",
     "tools/monitor.py + cron (scheduled agent)", "local_vm + cron", "Hash snapshot locally; cron re-checks. External service unnecessary."),
    ("public_web_research", r"\b(research|find|search|what is|compare|sources|evidence|verify)\b",
     "browser.search -> browser.open -> tools/dedupe.py + tools/verify_sources.py", "muse_tools + local_vm", "Search is included; dedupe/verify locally for free."),
    ("data_analysis", r"\b(analy[sz]e|chart|trend|statistics|dataset|pandas)\b",
     "tools/csv_analysis.py (pandas/numpy on local VM)", "local_vm", "2 vCPU / 7.7GB handles most CSVs. Colab GPU only if >1GB or ML training - requires your manual Google login."),
    ("ml_or_gpu", r"\b(train (a )?model|gpu|cuda|llm fine.?tun|stable diffusion|whisper large)\b",
     "EXTERNAL: Kaggle Notebooks (30 GPU hrs/wk free) or Colab free - MANUAL handoff", "external_provider_manual", "Real advantage over local VM (no GPU here), but no official headless API. I prepare notebook, you run it, I analyze output."),
    ("ci_or_long_compute", r"\b(ci|github actions|build.*repo|test.*repo|scheduled.*script.*github)\b",
     "EXTERNAL: GitHub Actions - only if you authorize GitHub connection/push", "external_provider_authorized", "2000 min/mo free for private repos, unlimited for public (standard runners). Triggerable via API/git - the ONLY truly programmable external compute in this audit."),
    ("browser_action", r"\b(book|buy|reserve|log ?in|fill.*form|checkout)\b",
     "browser.browse (live browser agent)", "muse_browser", "Needs real browser/session. Never delegate credentials to external agents."),
    ("parallel_fanout", r"\b(parallel|multiple.*(topics|sources|options)|compare.*\d|batch)\b",
     "subagent.spawn x N (parallel, independent)", "muse_subagents", "Verified: subagents run concurrently in this environment."),
]
DEFAULT = ("ai_reasoning", "Muse planning / interpretation / QC only", "muse_reasoning", "No code shortcut exists; reasoning is the work.")

def route(task: str):
    t = task.lower()
    hits = []
    for name, pat, tool, where, why in ROUTES:
        if re.search(pat, t):
            hits.append({"route": name, "tool": tool, "executes_on": where, "why": why, "cost_usd": 0})
    if not hits:
        name, tool, where, why = DEFAULT
        hits = [{"route": name, "tool": tool, "executes_on": where, "why": why, "cost_usd": 0}]
    return {"task": task, "primary": hits[0], "also_consider": hits[1:], "cost_guard": "$0 - refuse any route requiring payment/trial/card"}

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--json"]
    task = " ".join(args) or "analyze this csv and research trends in parallel"
    r = route(task)
    print(json.dumps(r, indent=2) if "--json" in sys.argv else f"PRIMARY: {r['primary']['route']} -> {r['primary']['tool']} [{r['primary']['executes_on']}]\nWhy: {r['primary']['why']}\nCost: $0")
