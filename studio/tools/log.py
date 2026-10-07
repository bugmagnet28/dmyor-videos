#!/usr/bin/env python3
"""Append one action to studio/ledger.jsonl (the audit trail). Log EVERY action.

  python3 studio/tools/log.py --channel instagram --action render --exp V-EXP-01 \
      --summary "Published post on X" --ref ready-to-post/2026-10-09-slug --status done

--status: planned | done | failed | skipped | waiting_on_human
"""
import argparse
import datetime as dt
import json
import pathlib

GROWTH = pathlib.Path(__file__).resolve().parent.parent

ap = argparse.ArgumentParser()
ap.add_argument("--channel", required=True)
ap.add_argument("--action", required=True)
ap.add_argument("--summary", required=True)
ap.add_argument("--exp", default="")
ap.add_argument("--ref", default="", help="URL, file path, commit or post id")
ap.add_argument("--status", default="done",
                choices=["planned", "done", "failed", "skipped", "waiting_on_human"])
ap.add_argument("--cost", type=float, default=0.0)
a = ap.parse_args()

row = {"ts": dt.datetime.now().isoformat(timespec="seconds"), "channel": a.channel, "action": a.action,
       "exp": a.exp, "summary": a.summary, "ref": a.ref, "status": a.status, "cost_usd": a.cost}
with (GROWTH / "ledger.jsonl").open("a") as f:
    f.write(json.dumps(row) + "\n")
print("logged:", a.channel, a.action, a.status)
