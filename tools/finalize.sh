#!/usr/bin/env bash
# Usage: finalize.sh <key>
# Makes <key>_final.mp4: loudness-normalized audio + the cover shown in the last 0.5 s,
# so the cover can be picked as the Short's thumbnail frame in the YouTube app.
set -e
k=$1; cd /home/claude/shorts
python3 cover.py "$k" >/dev/null
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$k.mp4")
s=$(python3 -c "print(max(0, $d - 0.5))")
ffmpeg -loglevel error -y -i "$k.mp4" -i "covers/${k}_cover.jpg" \
  -filter_complex "[1:v]scale=1080:1920[c];[0:v][c]overlay=0:0:enable='gte(t,$s)'[v]" \
  -map "[v]" -map 0:a -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p \
  -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 160k -movflags +faststart "${k}_final.mp4"
echo "$k finalized ($d s, cover from $s s)"
