#!/usr/bin/env python3
import os
import random
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOUND = HERE / "foxy-sound.mp3"

# Prefer APNG (made by --convert), then WebP, WebM, GIF.
VISUAL_CANDIDATES = [
    HERE / "foxy-jumpscare.apng",
    HERE / "foxy-jumpscare.webp",
    HERE / "foxy-jumpscare.webm",
    HERE / "foxy-jumpscare.gif",
]


def find_visual():
    for p in VISUAL_CANDIDATES:
        if p.is_file():
            return p
    return None


def primary_screen_index():
    """Return the index of the primary monitor (X11 only), else '0'."""
    try:
        out = subprocess.check_output(["xrandr", "--listmonitors"], text=True)
        for line in out.splitlines()[1:]:
            if "*" in line:
                return line.split(":")[0].strip()
    except Exception:
        pass
    return "0"


# Override with: FOXY_SCREEN=1 sh foxy.sh --test
SCREEN = os.environ.get("FOXY_SCREEN") or primary_screen_index()


def jumpscare():
    visual = find_visual()
    if visual is None or not SOUND.is_file():
        names = [p.name for p in VISUAL_CANDIDATES]
        print(f"Missing media: need {SOUND.name} and one of {names}", file=sys.stderr)
        return

    if not shutil.which("mpv"):
        print("Install the media player first: sudo apt install mpv", file=sys.stderr)
        return

    sound = subprocess.Popen(
        ["mpv", "--no-video", "--really-quiet", str(SOUND)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    common = [
        "--alpha=yes",
        "--fullscreen", f"--screen={SCREEN}", f"--fs-screen={SCREEN}",
        "--ontop", "--no-border", "--no-osc",
        "--no-input-default-bindings", "--no-audio",
        "--loop-file=no", str(visual),
    ]
    # --background syntax differs between mpv versions, and the GPU backend
    # differs between X11 and Wayland, so try the combinations in order.
    backgrounds = [["--background=#00000000"], ["--background=none"], []]
    backends = [["--vo=gpu", "--gpu-context=x11egl"], ["--vo=gpu"], []]
    last_err = ""
    try:
        for bg in backgrounds:
            for be in backends:
                result = subprocess.run(["mpv"] + be + bg + common,
                                        capture_output=True, text=True)
                if result.returncode == 0:
                    return
                last_err = result.stderr[-400:]
        print("mpv could not show the video:\n" + last_err, file=sys.stderr)
    finally:
        if sound.poll() is None:
            try:
                sound.wait(timeout=10)
            except subprocess.TimeoutExpired:
                sound.terminate()


def convert():
    """One-time: turn foxy-jumpscare.webp into a transparent APNG that old mpv can play."""
    try:
        from PIL import Image
    except ImportError:
        print("Install Pillow first: sudo apt install python3-pil", file=sys.stderr)
        raise SystemExit(1)
    src = HERE / "foxy-jumpscare.webp"
    dst = HERE / "foxy-jumpscare.apng"
    if not src.is_file():
        print(f"{src.name} not found", file=sys.stderr)
        raise SystemExit(1)
    im = Image.open(src)
    frames, durations = [], []
    for i in range(getattr(im, "n_frames", 1)):
        im.seek(i)
        frames.append(im.convert("RGBA").copy())
        durations.append(im.info.get("duration", 40) or 40)
    frames[0].save(dst, format="PNG", save_all=True, append_images=frames[1:],
                   duration=durations, loop=1, disposal=1, blend=0)
    print(f"Wrote {dst.name} ({len(frames)} frames)")


def main():
    if sys.argv[1:] == ["--convert"]:
        convert()
        return
    if sys.argv[1:] == ["--test"]:
        jumpscare()
        return
    if sys.argv[1:]:
        print("Usage: sh foxy.sh [--test | --convert]", file=sys.stderr)
        raise SystemExit(2)

    print(f"Foxy is running on screen {SCREEN}. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
            if random.randrange(10_000) == 0:
                jumpscare()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
