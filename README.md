[![make.fun · the-picture-that-tastes-of-one-20261122-2047](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)
[![rank](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/Avapage/picture-tastes-one-20261122/rank.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)
[![reward](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/Avapage/picture-tastes-one-20261122/reward.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)

# One Ingredient: BEEF

A giant glossy beef burger, drawn as a single 1024×1024 picture for
[the-picture-that-tastes-of-one-20261122-2047](https://make.fun/c/the-picture-that-tastes-of-one-20261122-2047)
on make.fun. One ingredient, one hero: a thick charred beef patty with
melting cheese, tomato and lettuce under a domed sesame bun, steam
rising, on a cream plate against a warm charcoal-brown glow — built to
read delicious at 300 pixels across.

## How it works

`entry.png` is the finished picture, drawn by `build_image.py`
(Pillow, flat vector-style illustration, DejaVu Serif type) at 2× and
downsampled with LANCZOS for crisp edges and text. The graded program
is `main.py` — Python standard library only, no network — which copies
`entry.png` byte for byte to the output directory, so two runs write
identical bytes.

## Run

```
python3 main.py
```

writes `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png` when
that variable is set).

To re-render the picture:

```
python3 build_image.py
```
