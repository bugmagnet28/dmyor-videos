"""Narration with Gemini TTS (directed delivery). Key read from GEMINI_API_KEY or ~/Documents/x-automation/.env.

    python3 tts/gemini_say.py "script" out.mp3 --voice Puck --style "warm, conversational founder" [--model gemini-3.8-flash-tts]

"||" in the script = a breath/new thought (sent as a line break). "Dmyor" is spoken "Deem-yor".
Writes 44.1 kHz mp3 normalised to -16 LUFS. Logs each call (chars, model) to tts/gemini_usage.jsonl for cost tracking.
"""
import argparse, base64, json, os, re, subprocess, tempfile, time, urllib.request, wave

ap = argparse.ArgumentParser()
ap.add_argument("text"); ap.add_argument("out")
ap.add_argument("--voice", default="Puck"); ap.add_argument("--model", default="gemini-3.8-flash-tts")
ap.add_argument("--style", default="Read this like a friendly young founder talking to one person: warm, conversational, natural pauses, a little smile on the last line. Not an announcer.")
a = ap.parse_args()
key = os.environ.get("GEMINI_API_KEY") or [l.split("=", 1)[1].strip().strip('"') for l in open(os.path.expanduser("~/Documents/x-automation/.env")) if l.startswith("GEMINI_API_KEY=")][0]
text = open(a.text[1:]).read() if a.text.startswith("@") else a.text
text = re.sub(r"\bDmyor\b", "Deem-yor", text)
text = "\n".join(t.strip() for t in text.split("||") if t.strip())
body = {"contents": [{"parts": [{"text": f"{a.style}\n\n{text}"}]}],
        "generationConfig": {"responseModalities": ["AUDIO"],
                             "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": a.voice}}}}}
req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{a.model}:generateContent?key={key}",
                             data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
for attempt in range(3):
    try:
        r = json.load(urllib.request.urlopen(req, timeout=180)); break
    except urllib.error.HTTPError as e:
        msg = e.read().decode()[:300]
        if attempt == 2 or e.code not in (429, 500, 503):
            raise SystemExit(f"Gemini TTS error {e.code}: {msg}")
        time.sleep(5 * (attempt + 1))
part = r["candidates"][0]["content"]["parts"][0]["inlineData"]
pcm = base64.b64decode(part["data"])
rate = int(re.search(r"rate=(\d+)", part.get("mimeType", "rate=24000")).group(1))
tmp = tempfile.mktemp(suffix=".wav")
with wave.open(tmp, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-af", "loudnorm=I=-16:TP=-1.5", "-ar", "44100", "-b:a", "192k", a.out], check=True)
os.remove(tmp)
dur = len(pcm) / 2 / rate
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gemini_usage.jsonl"), "a") as f:
    f.write(json.dumps({"ts": time.strftime("%Y-%m-%d %H:%M"), "model": a.model, "voice": a.voice, "chars": len(text), "seconds": round(dur, 2),
                        "usage": r.get("usageMetadata", {})}) + "\n")
print(f"{a.out}  {dur:.2f}s  voice={a.voice} model={a.model}")
