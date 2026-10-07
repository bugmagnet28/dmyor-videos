#!/usr/bin/env bash
# Run one video-agent cycle. Called by launchd daily; safe to run by hand.
set -uo pipefail

export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$HOME/.pyenv/shims:/usr/bin:/bin:/usr/sbin:/sbin"
STUDIO="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$STUDIO")"
STAMP="$(date +%Y-%m-%d_%H%M)"
LOG="$STUDIO/runs/logs/$STAMP.log"
LOCK="$STUDIO/state/run.lock"

notify() { python3 "$STUDIO/tools/notify.py" "$1" - <<<"$2" >/dev/null 2>&1 || true; }

cd "$ROOT"
if [[ -f "$STUDIO/PAUSE" ]]; then echo "$STAMP paused" >> "$STUDIO/runs/logs/paused.txt"; exit 0; fi
if [[ -f "$LOCK" ]] && kill -0 "$(cat "$LOCK")" 2>/dev/null; then echo "already running"; exit 0; fi
echo $$ > "$LOCK"
trap 'rm -f "$LOCK"' EXIT

# Pull Sanyam's edits (post-queue ticks, asks, notes) made on GitHub.
git pull -q --rebase origin main >>"$LOG" 2>&1 || echo "git pull failed" >>"$LOG"

claude -p "Run your daily video cycle now. Today is $(date '+%A %Y-%m-%d %H:%M'). Follow the run cycle in your instructions exactly, from step 0 to step 11." \
  --agent video \
  --permission-mode bypassPermissions \
  --disallowedTools \
    "Bash(aws s3:*)" "Bash(aws iam:*)" "Bash(aws cloudfront:*)" "Bash(aws lambda:*)" "Bash(aws route53:*)" \
    "Bash(git push --force:*)" "Bash(git push -f:*)" "Bash(git reset --hard:*)" \
    "Bash(rm -rf /*)" "Bash(rm -rf ~*)" "Bash(sudo:*)" "Bash(*deploy.sh*)" "Bash(npx serverless:*)" \
  --output-format text >>"$LOG" 2>&1
STATUS=$?

git add -A
git commit -q -m "Video run $STAMP (exit $STATUS)" >/dev/null 2>&1 || true
git push -q origin main >>"$LOG" 2>&1 || echo "git push failed" >>"$LOG"

if [[ $STATUS -ne 0 ]]; then
  notify "Run failed ($STAMP)" "The video agent run exited with status $STATUS. Last lines of the log:

$(tail -30 "$LOG")"
fi
exit $STATUS
