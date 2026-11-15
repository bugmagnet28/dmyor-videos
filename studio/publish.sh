#!/usr/bin/env bash
# Run one publisher session (schedule due reels on IG/X/YT via Claude in Chrome + read metrics).
# Called by launchd twice a day (com.dmyor.publisher); safe to run by hand.
set -uo pipefail
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$HOME/.pyenv/shims:/usr/bin:/bin:/usr/sbin:/sbin"
STUDIO="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(dirname "$STUDIO")"
STAMP="$(date +%Y-%m-%d_%H%M)"; LOG="$STUDIO/runs/logs/publish-$STAMP.log"; LOCK="$STUDIO/state/publish.lock"
notify() { python3 "$STUDIO/tools/notify.py" "$1" - <<<"$2" >/dev/null 2>&1 || true; }
cd "$ROOT"
if [[ -f "$STUDIO/PAUSE" || -f "$STUDIO/PAUSE_PUBLISH" ]]; then echo "$STAMP paused" >> "$STUDIO/runs/logs/paused.txt"; exit 0; fi
if [[ -f "$LOCK" ]] && kill -0 "$(cat "$LOCK")" 2>/dev/null; then echo "already running"; exit 0; fi
echo $$ > "$LOCK"; trap 'rm -f "$LOCK"' EXIT
# Don't fight the video agent's run for the browser/CPU.
for i in $(seq 1 60); do [[ -f "$STUDIO/state/run.lock" ]] && kill -0 "$(cat "$STUDIO/state/run.lock")" 2>/dev/null && sleep 60 || break; done
git pull -q --rebase origin main >>"$LOG" 2>&1 || echo "git pull failed" >>"$LOG"
FREE_MB=$(( $(vm_stat | awk '/Pages free/ {gsub("\\.","",$3); print $3}') * 16384 / 1048576 ))
echo "free memory: ${FREE_MB} MB; $(sysctl -n vm.swapusage)" >>"$LOG"
claude -p "Run your publisher session now. Now is $(date '+%A %Y-%m-%d %H:%M %Z'). Follow your instructions: schedule what is due from studio/schedule.json on Instagram, X and YouTube, then read metrics." \
  --agent publisher --chrome \
  --permission-mode bypassPermissions \
  --disallowedTools "Bash(git push --force:*)" "Bash(git push -f:*)" "Bash(git reset --hard:*)" "Bash(rm -rf /*)" "Bash(rm -rf ~*)" "Bash(sudo:*)" "Bash(*deploy.sh*)" \
  --output-format text >>"$LOG" 2>&1
STATUS=$?
git add studio/schedule.json studio/post-queue.md analytics/inbox >/dev/null 2>&1
git commit -q -m "Publish run $STAMP (exit $STATUS)" >/dev/null 2>&1 || true
git push -q origin main >>"$LOG" 2>&1 || echo "git push failed" >>"$LOG"
if [[ $STATUS -ne 0 ]]; then notify "Publisher run failed ($STAMP)" "The publisher exited with status $STATUS. Last lines:

$(tail -30 "$LOG")"; fi
exit $STATUS
