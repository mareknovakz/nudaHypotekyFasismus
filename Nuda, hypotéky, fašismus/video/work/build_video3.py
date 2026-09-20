# -*- coding: utf-8 -*-
import subprocess
import sys

WORK = r"c:\Repozitáře\nudaHypotekyFasismus\video\work"
AUDIO = r"c:\Repozitáře\nudaHypotekyFasismus\video\Classicals.de - Chopin - Nocturne Op. 9 no. 1 in B-flat minor.mp3"
OUT = r"c:\Repozitáře\nudaHypotekyFasismus\video\Promo_Nuda_hypoteky_fasismus.mp4"

CORONET = "C\\:/Program Files/Scribus 1.6.5/share/fonts/URWFonts-1.41/Coronet.ttf"
PAD = "\u00a0\u00a0\u00a0"

AUDIO_START = float(sys.argv[1]) if len(sys.argv) > 1 else 100.0

clips = [
    ("postel_c2.mp4", 4.0),
    ("horses_c2.mp4", 4.0),
    ("field_c2.mp4", 4.0),
    ("path_c2.mp4", 4.0),
]
XFADE = 0.4

inputs = []
for name, _ in clips:
    inputs += ["-i", f"{WORK}\\{name}"]
inputs += ["-ss", str(AUDIO_START), "-i", AUDIO]

filters = []
cum = clips[0][1]
prev_label = "0:v"
offsets = []
for i in range(1, len(clips)):
    off = cum - XFADE
    offsets.append(off)
    out_label = f"v{i}" if i < len(clips) - 1 else "vcat"
    filters.append(f"[{prev_label}][{i}:v]xfade=transition=fade:duration={XFADE}:offset={off}[{out_label}]")
    cum = off + clips[i][1]
    prev_label = out_label
TOTAL_DUR = cum

# title text timing: extended hold by +2s vs previous version
t_in, t_hold_end, t_out = 1.3, 7.5, 8.1
title_alpha = (
    f"if(lt(t,{t_in}),0,"
    f"if(lt(t,{t_in+0.5}),(t-{t_in})/0.5,"
    f"if(lt(t,{t_hold_end}),1,"
    f"if(lt(t,{t_out}),({t_out}-t)/0.5,0))))"
)

# date/place text: appears earlier, during the photos (not waiting for a separate end card)
d_in = 10.5
date_alpha = (
    f"if(lt(t,{d_in}),0,"
    f"if(lt(t,{d_in+0.6}),(t-{d_in})/0.6,1))"
)

drawtext_common = f"fontfile='{CORONET}':fontcolor=white:shadowcolor=black@0.7:shadowx=2:shadowy=2"

filters.append(
    f"[vcat]drawtext={drawtext_common}:text='Křest sbírky Mirka Mrkvičky{PAD}':"
    f"fontsize=90:x=(w-text_w)/2:y=580:alpha='{title_alpha}'[t1]"
)
filters.append(
    f"[t1]drawtext={drawtext_common}:text='Nuda, hypotéky, fašismus{PAD}':"
    f"fontsize=125:x=(w-text_w)/2:y=830:alpha='{title_alpha}'[t2]"
)
filters.append(
    f"[t2]drawtext={drawtext_common}:text='Cross Club{PAD}':"
    f"fontsize=90:x=(w-text_w)/2:y=580:alpha='{date_alpha}'[t3]"
)
filters.append(
    f"[t3]drawtext={drawtext_common}:text='29. 9. 2026  ·  19\\:00{PAD}':"
    f"fontsize=125:x=(w-text_w)/2:y=830:alpha='{date_alpha}'[vout]"
)

fade_out_start = TOTAL_DUR - 1.2
filters.append(
    f"[{len(clips)}:a]atrim=0:{TOTAL_DUR},volume=9dB,afade=t=in:st=0:d=1,afade=t=out:st={fade_out_start}:d=1.2[aout]"
)

filter_complex = ";".join(filters)

cmd = [
    "ffmpeg", "-y",
    *inputs,
    "-filter_complex", filter_complex,
    "-map", "[vout]", "-map", "[aout]",
    "-r", "30",
    "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k",
    "-movflags", "+faststart",
    OUT,
    "-loglevel", "error",
]

result = subprocess.run(cmd, cwd=WORK, capture_output=True, text=True)
print("TOTAL_DUR:", TOTAL_DUR)
print("returncode:", result.returncode)
if result.returncode != 0:
    print(result.stderr[-4000:])
else:
    print("OK ->", OUT)
