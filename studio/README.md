# dmyor video agent

Makes one short motion-graphics video a day for Instagram @dmyor_global, learns from the numbers, and gets better. Rules: `.claude/agents/video.md`. Pipeline: `.claude/skills/dmyor-reel/`.

**Start here: [DASHBOARD.md](DASHBOARD.md)**

| You want to | Do this |
|---|---|
| Post today's video | `post-queue.md` -> top entry -> `ready-to-post/<date>-<slug>/video.mp4` + caption in `post.md`. Tick `[x] posted` |
| Give it numbers | Drop insight screenshots in `inbox/metrics/` (or type into `inbox/metrics/video-performance.md`) |
| Give it a voiceover | Drop the audio in `inbox/audio/` (name it after the video if you can) |
| Tell it something | `inbox/notes.md` |
| Pause it | `touch ~/Documents/dmyor-videos/studio/PAUSE` (delete to resume) |
| Run it now | `~/Documents/dmyor-videos/studio/run.sh` |

Runs daily at 11:00 via LaunchAgent `com.dmyor.video` (Mac must be on). History: `runs/`, `ledger.jsonl`, `learnings.md`, `experiments.md`, git log.
