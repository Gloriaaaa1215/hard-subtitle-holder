# Track JSON Schema

Use this shape as input to `build_holders.py`:

```json
{
  "fps": 29.97002997,
  "placeholder": "【待翻译】",
  "tracks": [
    {
      "id": "track-001",
      "start_frame": 351,
      "end_frame": 423,
      "zone": "lower",
      "color": "white",
      "style": "Example - Lower - White",
      "bbox": [420, 710, 1510, 870],
      "confidence": 0.96,
      "reviewed": true,
      "notes": ""
    }
  ]
}
```

Rules:

- `end_frame` is exclusive.
- `style` must exactly match a style in the source ASS.
- `bbox` uses source-video pixel coordinates as `[x1, y1, x2, y2]`.
- `zone` may be `upper`, `lower`, `center`, or a project-specific label.
- `color` may be `white`, `orange`, another confirmed label, or `unknown`.
- Set `reviewed` to `false` for uncertain boundaries, style, color, or block grouping.
