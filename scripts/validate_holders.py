#!/usr/bin/env python3
import re
import sys
from collections import Counter
from pathlib import Path


def ass_time(value):
    hours, minutes, seconds = value.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_holders.py output.ass")
    path = Path(sys.argv[1])
    errors = []
    styles = Counter()
    names = Counter()
    events = 0
    review = 0
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8-sig").splitlines(), 1
    ):
        if not line.startswith("Dialogue:"):
            continue
        fields = line.split(":", 1)[1].lstrip().split(",", 9)
        if len(fields) != 10:
            errors.append(f"line {line_number}: malformed Dialogue")
            continue
        events += 1
        start = ass_time(fields[1])
        end = ass_time(fields[2])
        if end <= start:
            errors.append(f"line {line_number}: non-positive duration")
        styles[fields[3]] += 1
        names[fields[4]] += 1
        if "待复核" in fields[9]:
            review += 1
        if not re.search(r"待翻译|待复核", fields[9]):
            errors.append(f"line {line_number}: missing holder text")
    duplicates = [name for name, count in names.items() if name and count > 1]
    if duplicates:
        errors.append("duplicate track IDs: " + ", ".join(duplicates))
    print(f"events: {events}")
    print(f"needs_review: {review}")
    print("styles:")
    for style, count in styles.most_common():
        print(f"  {style}: {count}")
    if errors:
        print("errors:")
        for error in errors:
            print(f"  {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
