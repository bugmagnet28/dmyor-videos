#!/usr/bin/env python3
"""Word-level alignment of a reel's narration.

  align.py reels/<slug>                 transcribe -> cues.json
  align.py reels/<slug> --find "phrase" locate a phrase in an existing cues.json
  align.py reels/<slug> --beats         print sentence-level cue sheet

Never estimate narration timings. A previous cut was 3-5s out on every beat
because the timings were guessed instead of measured.
"""
import argparse, json, os, re, subprocess, sys

def norm(w):
    return re.sub(r'[^a-z0-9]', '', w.lower())

def transcribe(d, model):
    audio = None
    for ext in ('mp3', 'wav', 'm4a', 'aac'):
        p = os.path.join(d, f'audio.{ext}')
        if os.path.exists(p):
            audio = p
            break
    if not audio:
        sys.exit(f"no audio.* in {d} - add the recorded VO first")
    out = os.path.join(d, '_asr')
    os.makedirs(out, exist_ok=True)
    print(f"transcribing {os.path.basename(audio)} with whisper ({model})...")
    subprocess.run(['whisper', audio, '--model', model, '--language', 'en',
                    '--word_timestamps', 'True', '--output_format', 'json',
                    '--output_dir', out, '--verbose', 'False'],
                   check=True, stdout=subprocess.DEVNULL)
    base = os.path.splitext(os.path.basename(audio))[0]
    raw = json.load(open(os.path.join(out, base + '.json')))

    words, sents = [], []
    for seg in raw['segments']:
        for w in seg.get('words', []):
            words.append({'w': norm(w['word']), 'raw': w['word'].strip(),
                          's': round(w['start'], 2), 'e': round(w['end'], 2)})
        sents.append({'s': round(seg['start'], 2), 'e': round(seg['end'], 2),
                      'text': seg['text'].strip()})
    dur = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                          'format=duration', '-of', 'csv=p=0', audio],
                         capture_output=True, text=True).stdout.strip()
    cues = {'audio': os.path.basename(audio), 'duration': round(float(dur), 2),
            'text': raw['text'].strip(), 'words': words, 'sentences': sents,
            'wps': round(len(words) / float(dur), 2)}
    json.dump(cues, open(os.path.join(d, 'cues.json'), 'w'), indent=1)
    print(f"{len(words)} words, {cues['duration']}s, {cues['wps']} words/sec")
    print(f"-> {os.path.join(d,'cues.json')}")
    return cues

def find(cues, phrase, after=0.0):
    toks = [t for t in re.sub(r'[^a-z0-9 ]', '', phrase.lower()).split() if t]
    W = cues['words']
    for i in range(len(W)):
        if W[i]['s'] < after - 1e-3:
            continue
        j = k = 0
        k = i
        while k < len(W) and j < len(toks):
            if W[k]['w'] == toks[j]:
                j += 1
            elif W[k]['w'] == '':
                pass
            else:
                break
            k += 1
        if j == len(toks):
            return W[i]['s'], W[k - 1]['e']
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dir')
    ap.add_argument('--model', default='small.en')
    ap.add_argument('--find')
    ap.add_argument('--beats', action='store_true')
    a = ap.parse_args()

    cp = os.path.join(a.dir, 'cues.json')
    if a.find or a.beats:
        if not os.path.exists(cp):
            sys.exit("no cues.json - run align.py without --find first")
        cues = json.load(open(cp))
        if a.find:
            r = find(cues, a.find)
            print(f"{a.find!r}: {r[0]} -> {r[1]}" if r else f"{a.find!r}: NOT FOUND")
        else:
            for s in cues['sentences']:
                print(f"{s['s']:6.2f} -> {s['e']:6.2f}  {s['text']}")
        return
    transcribe(a.dir, a.model)

if __name__ == '__main__':
    main()
