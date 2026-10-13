# Foxy Jumpscare

A tiny Linux prank: runs in the background and, at a random moment, plays a
transparent fullscreen jumpscare animation with sound on your screen.

## Requirements

- Linux, ideally an X11 session with a compositor (transparency is unreliable on Wayland)
- `mpv`: `sudo apt install mpv`
- Python 3 and Pillow (only for the one-time conversion): `sudo apt install python3-pil`

## Setup

Put your own media files next to `foxy.py` (they are not included in this repo):

- `foxy-jumpscare.webp` (animated, with transparency) and `foxy-sound.mp3`

Convert the WebP to a transparent APNG that mpv can play:

```
sh foxy.sh --convert
```

## Usage

```
sh foxy.sh --test    # trigger a jumpscare right now
sh foxy.sh           # run in the background, random trigger (about once per 3 hours on average)
```

If it shows on the wrong monitor, pick the screen manually:

```
FOXY_SCREEN=1 sh foxy.sh --test
```

## Notes

Five Nights at Freddy's and Foxy belong to their respective owners. This is an
unofficial fan project; bring your own media.
