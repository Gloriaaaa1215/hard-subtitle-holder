---
name: hard-subtitle-holder
description: Detect and track hardcoded subtitle regions in video, refine their frame-accurate appearance and disappearance boundaries, and generate an ASS text-holder timeline using styles already present in a supplied ASS file. Use for burned-in subtitles where OCR or translation is unnecessary, including videos with multiple independently timed text regions, white/orange color variants, upper/lower subtitle zones, an existing rough timeline, or no timeline at all.
---

# Hard Subtitle Holder

Create an ASS placeholder timeline from visible hardcoded text. Treat text content as irrelevant unless the user explicitly asks for OCR.

## Inputs

Require:

- hard-subtitled video
- ASS containing the styles to reuse

Accept either:

- an ASS with a rough timeline to refine
- a styles-only ASS from which to build a new timeline

Never overwrite source files.

## Workflow

1. Run `scripts/inspect_inputs.py` to inspect video metadata, ASS styles, and existing events.
2. Identify subtitle search zones. Start broad when layout is unknown, then exclude logos, clocks, signs, and persistent graphics.
3. Build a text-region mask from edge, outline, brightness, color, and connected-component evidence. Do not use whole-frame warm-pixel counts.
4. Detect coarse change intervals, then inspect individual frames only around changes.
5. Track every text region independently across frames. Assign a track ID and record its bounding box, first frame, last frame, color class, zone, and confidence.
6. Describe scene motion only to separate camera/background changes from text changes. Do not depend on semantic scene descriptions.
7. Write track data using `references/tracks-schema.md`.
8. Review all low-confidence boundaries and every multi-region interval visually.
9. Run `scripts/build_holders.py` to create a new ASS from reviewed tracks.
10. Run `scripts/validate_holders.py` and render representative frames before delivery.

Read [workflow.md](references/workflow.md) for detection, tracking, color, and review rules. Read [tracks-schema.md](references/tracks-schema.md) before creating track JSON.

## Holder Rules

- Create one holder per independently timed visible text region.
- Use `【待翻译】` unless the user supplies another placeholder.
- Treat line wrapping inside one coherent block as one holder.
- Create two holders only when the picture contains two independent upper/lower blocks.
- Do not split by punctuation, brackets, sentence meaning, or existing translation structure.
- Do not match Korean content to Chinese content.
- Reuse only styles present in the source ASS.
- Mark uncertain style/color/zone decisions for review instead of guessing.

## Existing Rough Timeline

Use existing event times as search hints, not truth. Search around each boundary and allow tracks to split, merge, appear, or disappear independently when the picture proves the rough timeline wrong.

## No Existing Timeline

Scan coarsely for text-region changes, create candidate tracks, then refine each candidate boundary frame by frame. Persistent graphics must be ignored or placed on a denylist.

## Delivery Standard

Do not label an output `reviewed` until:

- every low-confidence boundary was checked
- both white-to-orange and orange-to-white classifications were reviewed
- every simultaneous multi-region interval was checked
- no zero/negative duration or duplicate holder remains
- representative ASS renders passed
