#!/usr/bin/env python3
"""Synthesise a quiet ambient bed for the film: slow major-key pads, a few soft bell notes, room reverb.

  python3 demo/video/music.py [seconds] [swell,swell,...] [out.wav]  -> demo/video/out/music.wav
"""
import sys
import wave
from pathlib import Path

import numpy as np

SR = 44100
OUT = Path(__file__).resolve().parent / "out" / "music.wav"
if len(sys.argv) > 3:
    OUT = Path(sys.argv[3])


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def pad_voice(f, n, rng):
    t = np.arange(n) / SR
    out = np.zeros((2, n))
    for ch, det in enumerate((-0.0011, 0.0011)):
        ph = rng.uniform(0, 2 * np.pi, 3)
        ff = f * (1 + det)
        wob = 1 + 0.0015 * np.sin(2 * np.pi * 0.11 * t + ph[0])
        out[ch] = (np.sin(2 * np.pi * ff * wob * t + ph[1]) + 0.22 * np.sin(4 * np.pi * ff * t + ph[2])
                   + 0.06 * np.sin(6 * np.pi * ff * t))
    return out


def main():
    dur = float(sys.argv[1]) if len(sys.argv) > 1 else 95.0
    n = int(dur * SR)
    rng = np.random.default_rng(7)
    mix = np.zeros((2, n))

    # D major colour: Dmaj9, Bm9, Gmaj9, A6/9 -- one chord every 9.5 s, long crossfades
    chords = [[50, 57, 61, 64, 66], [47, 54, 57, 61, 62], [43, 50, 54, 57, 62], [45, 52, 57, 59, 66]]
    step, fade = 9.5, 3.5
    for k in range(int(np.ceil(dur / step)) + 1):
        a, b = k * step - fade, (k + 1) * step + fade
        i0, i1 = max(0, int(a * SR)), min(n, int(b * SR))
        if i1 <= i0:
            continue
        seg = i1 - i0
        tt = np.arange(seg) / SR + max(a, 0) - a
        env = np.clip(tt / fade, 0, 1) * np.clip((b - a - tt) / fade, 0, 1)
        env = 0.5 - 0.5 * np.cos(np.pi * env)
        for m in chords[k % len(chords)]:
            mix[:, i0:i1] += pad_voice(hz(m), seg, rng) * env * (0.9 if m < 52 else 0.55)

    # sparse bell notes from D major pentatonic, softly, every ~4.75 s
    bells = [74, 78, 81, 76, 83, 78, 74, 81, 86, 78]
    for j, start in enumerate(np.arange(2.4, dur - 6, 4.75)):
        i0, seg = int(start * SR), int(3.5 * SR)
        t = np.arange(min(seg, n - i0)) / SR
        f = hz(bells[j % len(bells)])
        tone = (np.sin(2 * np.pi * f * t) + 0.18 * np.sin(2 * np.pi * 3.01 * f * t)) * np.exp(-t / 1.1)
        tone *= np.clip(t / 0.012, 0, 1)
        pan = 0.5 + 0.3 * np.sin(j)
        mix[0, i0:i0 + len(t)] += 0.32 * tone * (1 - pan)
        mix[1, i0:i0 + len(t)] += 0.32 * tone * pan

    # gentle low swell under the title card (16 s) and the end card (88.4 s)
    swells = [float(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [16.0, 88.4]
    for at in swells:
        i0 = max(0, int((at - 0.5) * SR))
        t = np.arange(min(int(7 * SR), n - i0)) / SR
        sw = np.sin(2 * np.pi * hz(38) * t) * np.sin(np.pi * np.clip(t / 7, 0, 1)) ** 2
        mix[:, i0:i0 + len(t)] += 0.8 * sw

    # one-pole low-pass for warmth
    alpha = 1 - np.exp(-2 * np.pi * 2200 / SR)
    for ch in range(2):
        y, acc = mix[ch], 0.0
        out = np.empty_like(y)
        for i in range(0, n, 4096):  # vectorised blocks are close enough at this cutoff
            blk = y[i:i + 4096]
            res = np.empty_like(blk)
            for j2, v in enumerate(blk):
                acc += alpha * (v - acc)
                res[j2] = acc
            out[i:i + 4096] = res
        mix[ch] = out

    # room reverb: decaying noise impulse, decorrelated per channel
    ir_len = int(3.2 * SR)
    t = np.arange(ir_len) / SR
    wet = np.zeros_like(mix)
    size = 1 << int(np.ceil(np.log2(n + ir_len)))
    for ch in range(2):
        ir = rng.standard_normal(ir_len) * np.exp(-t / 0.9)
        ir /= np.sqrt(np.sum(ir ** 2))
        wet[ch] = np.fft.irfft(np.fft.rfft(mix[ch], size) * np.fft.rfft(ir, size), size)[:n]
    mix = 0.7 * mix + 0.45 * wet

    # master: fades and level
    tt = np.arange(n) / SR
    mix *= np.clip(tt / 2.5, 0, 1) * np.clip((dur - tt) / 5.0, 0, 1)
    mix *= 0.5 / np.max(np.abs(mix))  # peak at -6 dBFS
    pcm = (mix.T * 32767).astype("<i2")
    OUT.parent.mkdir(exist_ok=True)
    with wave.open(str(OUT), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("wrote", OUT, f"{dur:.1f}s")


if __name__ == "__main__":
    main()
