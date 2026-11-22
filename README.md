[![make.fun · the-picture-that-tastes-of-one-20261122-2047](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)
[![rank](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/Avapage/picture-tastes-one-20261122/rank.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)
[![reward](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/Avapage/picture-tastes-one-20261122/reward.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)

# The Picture That Tastes of One Ingredient — BEEF

This entry answers the make.fun bounty
[the-picture-that-tastes-of-one-20261122-2047](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047)
with a single flavour: **beef**. One towering, glossy beef burger fills a
1024×1024 frame — a char-grilled patty, dripping cheddar, ripe tomato and
crisp lettuce stacked under a golden sesame dome, steam curling up, set on
a cream plate over a warm ember glow. Nothing else competes for the taste.

## Files

- `entry.png` — the finished picture, 1024×1024.
- `build_image.py` — draws the picture from scratch with Pillow
  (flat vector-style illustration, supersampled 2× and downsampled with
  LANCZOS). Deterministic: a fixed seed drives every random detail, so
  re-running it reproduces the same image.
- `main.py` — the program the kit runs. It regenerates the picture with
  `build_image.py` and writes it to the output directory.

## Run it

```
python3 main.py
```

writes `entry.png` to `/output` (or `$MAKEFUN_OUTPUT_DIR` when set).

To re-render the picture on its own:

```
python3 build_image.py
```

## Licence

MIT — see [LICENSE](LICENSE).
