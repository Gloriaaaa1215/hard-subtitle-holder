#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path


def parse_ass(path):
    styles = []
    events = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if line.startswith("Style:"):
            styles.append(line.split(":", 1)[1].lstrip().split(",", 1)[0])
        elif line.startswith("Dialogue:"):
            fields = line.split(":", 1)[1].lstrip().split(",", 9)
            if len(fields) == 10:
                events.append(
                    {
                        "start": fields[1],
                        "end": fields[2],
                        "style": fields[3],
                        "text": fields[9],
                    }
                )
    return styles, events


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: inspect_inputs.py video.mp4 styles.ass")
    video = Path(sys.argv[1])
    ass = Path(sys.argv[2])
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height,r_frame_rate,avg_frame_rate,nb_frames,duration",
        "-show_entries",
        "format=duration",
        "-of",
        "json",
        str(video),
    ]
    metadata = json.loads(subprocess.check_output(command))
    styles, events = parse_ass(ass)
    print(
        json.dumps(
            {
                "video": str(video),
                "ass": str(ass),
                "metadata": metadata,
                "styles": styles,
                "event_count": len(events),
                "events": events,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

