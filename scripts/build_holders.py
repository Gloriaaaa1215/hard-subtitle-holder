#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def frame_to_ass(frame, fps):
    seconds = frame / fps
    centiseconds = round(seconds * 100)
    hours, centiseconds = divmod(centiseconds, 360000)
    minutes, centiseconds = divmod(centiseconds, 6000)
    seconds, cs = divmod(centiseconds, 100)
    return f"{hours}:{minutes:02d}:{seconds:02d}.{cs:02d}"


def ass_styles(lines):
    result = set()
    for line in lines:
        if line.startswith("Style:"):
            result.add(line.split(":", 1)[1].lstrip().split(",", 1)[0])
    return result


def main():
    if len(sys.argv) != 4:
        raise SystemExit(
            "usage: build_holders.py source-styles.ass tracks.json output.ass"
        )
    source, tracks_path, output = map(Path, sys.argv[1:])
    lines = source.read_text(encoding="utf-8-sig").splitlines()
    data = json.loads(tracks_path.read_text(encoding="utf-8"))
    fps = float(data["fps"])
    placeholder = data.get("placeholder", "【待翻译】")
    tracks = data.get("tracks", [])
    styles = ass_styles(lines)

    errors = []
    for track in tracks:
        if track["style"] not in styles:
            errors.append(f"{track['id']}: unknown style {track['style']}")
        if int(track["end_frame"]) <= int(track["start_frame"]):
            errors.append(f"{track['id']}: invalid frame range")
    if errors:
        raise SystemExit("\n".join(errors))

    event_index = next(
        (index for index, line in enumerate(lines) if line.strip() == "[Events]"), None
    )
    if event_index is None:
        raise SystemExit("source ASS has no [Events] section")

    header = lines[: event_index + 1]
    format_line = next(
        (
            line
            for line in lines[event_index + 1 :]
            if line.startswith("Format:")
        ),
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    )
    result = header + [format_line]
    for track in sorted(tracks, key=lambda item: (item["start_frame"], item["id"])):
        text = placeholder
        if not track.get("reviewed", False):
            text += f" [{track['id']}:待复核]"
        result.append(
            "Dialogue: 0,"
            + frame_to_ass(int(track["start_frame"]), fps)
            + ","
            + frame_to_ass(int(track["end_frame"]), fps)
            + ","
            + track["style"]
            + ","
            + track["id"]
            + ",0,0,0,,"
            + text
        )
    output.write_text("\n".join(result) + "\n", encoding="utf-8-sig")
    print(f"wrote {len(tracks)} holders to {output}")


if __name__ == "__main__":
    main()
