# Daily Why video tools

Backup of the workspace that makes the Daily Why Shorts and long videos (see the playbook in the DailyWhy project).

## Rebuild the workspace in a new session
1. Copy this folder to `/home/claude/shorts` (photos go to `/home/claude/shorts/photos`, `long2`/`long3` stay as subfolders).
2. Fonts: `tools/fonts/Inter-*.otf` must be at `/usr/share/fonts/opentype/inter/` (path `F` at the top of `engine.py`).
3. Voice: `pip install kokoro-onnx soundfile --break-system-packages`, then put `kokoro-v1.0.onnx` and `voices-v1.0.bin` in `/home/claude/tts/` (model files from the kokoro-onnx releases on GitHub; they are too large for this repo).
4. Other packages: pillow, numpy, scipy; ffmpeg must be installed.

## Make a Short
- Add the script to `scripts.json`, run `python3 tts2.py <key>`.
- Add a spec to `SPECS` in `mk.py`, then `python3 mk.py <key> preview` and `python3 mk.py <key>`.

## Make a long video
- `long3/script.json` (chapters) → `tts_long.py` → `render3.py` (4 frame ranges in parallel) → concat + audio mix.
