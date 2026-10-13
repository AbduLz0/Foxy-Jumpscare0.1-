# Foxy Jumpscare

A tiny Linux prank if you hate yourself or want to feel something.Gives a Psychological warfare by running 1-in-10,000 chance every second., plays a
transparent fullscreen foxy jumpscare animation with sound on your screen.

Inspired by the Terraria mod. Built for Linux. Absolutely unnecessary.

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
