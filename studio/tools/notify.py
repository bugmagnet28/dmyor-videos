#!/usr/bin/env python3
"""Email Sanyam via AWS SES (same sender the Dmyor backend uses). Video agent copy.

  python3 studio/tools/notify.py "Subject" body.md
  echo "text" | python3 studio/tools/notify.py "Subject" -

Recipient and sender come from studio/config.json.
"""
import json
import pathlib
import subprocess
import sys
import tempfile

GROWTH = pathlib.Path(__file__).resolve().parent.parent


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    cfg = json.loads((GROWTH / "config.json").read_text())
    subject = sys.argv[1]
    body = sys.stdin.read() if sys.argv[2] == "-" else pathlib.Path(sys.argv[2]).read_text()
    payload = {
        "FromEmailAddress": cfg["notify_from"],
        "Destination": {"ToAddresses": [cfg["notify_to"]]},
        "Content": {"Simple": {
            "Subject": {"Data": f"[Dmyor video] {subject}", "Charset": "UTF-8"},
            "Body": {"Text": {"Data": body, "Charset": "UTF-8"}},
        }},
    }
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(payload, f)
    r = subprocess.run(["aws", "sesv2", "send-email", "--region", cfg["ses_region"],
                        "--cli-input-json", f"file://{f.name}"], capture_output=True, text=True)
    pathlib.Path(f.name).unlink(missing_ok=True)
    if r.returncode != 0:
        print("notify failed:", r.stderr.strip())
        sys.exit(1)
    print("sent:", subject)


if __name__ == "__main__":
    main()
