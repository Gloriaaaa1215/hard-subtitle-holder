# Detection And Review Rules

## Scene Context

Use a rough scene description only to estimate:

- hard cut versus continuous shot
- camera or subject movement
- stable versus moving background
- persistent on-screen graphics

Do not infer subtitle changes from semantics. Compare localized text regions after accounting for scene motion.

## Multi-Region Tracking

Represent text as independent tracks:

```text
track-001  lower-center  white   frame 302 -> 366
track-002  upper-center  orange  frame 319 -> 401
track-003  lower-left    white   frame 340 -> 357
```

Tracks may overlap in time. Match regions across frames using:

- bounding-box overlap
- center displacement
- size and aspect ratio
- outline/edge-mask similarity
- color class
- expected motion after camera compensation

Do not use one global “subtitle present” flag.

## Boundary Search

1. Scan at a coarse interval to locate change windows.
2. Compare localized masks before and after each change.
3. Search the candidate window frame by frame.
4. Start at the first frame where the region is visibly established.
5. End at the first frame where that region is no longer visible.
6. Keep other simultaneous tracks active if they remain visible.

For fades, record the first/last frame where text is meaningfully readable and flag the result as a fade boundary.

## Color

Classify color from pixels belonging to the text strokes, not the surrounding rectangle.

Review in both directions:

- every orange candidate for false orange
- every white candidate for missed orange

Skin, wood, hair, clothing, food, and warm lighting are common false-orange sources. Set `color` to `unknown` when stroke isolation is insufficient.

## One Block Versus Two

One holder:

- wrapped lines share alignment, style, timing, and spacing
- lines form one coherent subtitle block

Two holders:

- upper and lower blocks are spatially separated
- they have independent appearance/disappearance timing
- they use different colors/styles
- one block remains while the other changes

Content and punctuation must not influence this decision.

## Review Artifacts

Generate:

- boundary contact sheets showing frames before and after each uncertain change
- color sheets containing the complete subtitle area
- a multi-region sheet for every interval with two or more tracks
- a CSV or JSON review list with track ID and reason

Review reasons include:

- low boundary confidence
- camera cut near boundary
- moving text
- partial occlusion
- color unknown
- possible persistent graphic
- possible one-block/two-block ambiguity
