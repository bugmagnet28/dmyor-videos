#!/bin/bash
# One-time setup of the free local voice (Kokoro, Apache-2.0). Run from the project root.
# Creates ./tts/.venv (kokoro-onnx + soundfile) and downloads ./tts/models (~340 MB).
set -euo pipefail
mkdir -p tts/models
[ -x tts/.venv/bin/python ] || python3 -m venv tts/.venv
tts/.venv/bin/pip install -q --upgrade pip
tts/.venv/bin/pip install -q kokoro-onnx soundfile numpy
cd tts/models
[ -s kokoro-v1.0.onnx ] || curl -sSL -o kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -s voices-v1.0.bin ] || curl -sSL -o voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
ls -lh
echo "ok: Kokoro ready (also needs: ffmpeg, whisper CLI, node + puppeteer for record.js)"
