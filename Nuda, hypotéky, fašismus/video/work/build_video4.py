# -*- coding: utf-8 -*-
import subprocess
import sys

WORK = r"c:\Repozitáře\nudaHypotekyFasismus\video\work"
AUDIO = r"c:\Repozitáře\nudaHypotekyFasismus\video\Classicals.de - Chopin - Nocturne Op. 9 no. 1 in B-flat minor.mp3"
OUT = r"c:\Repozitáře\nudaHypotekyFasismus\video\Promo_Nuda_hypoteky_fasismus.mp4"

CORONET = "C\\:/Program Files/Scribus 1.6.5/share/fonts/URWFonts-1.41/Coronet.ttf"
PAD = "\u00a0\u00a0\u00a0"
LOGO = f"{WORK}\\white_logo.png"

AUDIO_START = float(sys.argv[1]) if len(sys.argv) > 1 else 100.0

clips = [
    ("postel_c2.mp4", 4.0),
    ("horses_c2.mp4", 4.0),
    ("field_c2.mp4", 4.0),
    ("path_c2.mp4", 4.0),
    ("predmesti_c2.mp4", 4.0),
]
XFADE = 0.4

inputs = []
for name, _ in clips:
    inputs += ["-i", f"{WORK}\\{name}"]
TOTAL_DUR = sum(d for _, d in clips) - (len(clips) - 1) * XFADE

inputs += ["-loop", "1", "-t", str(TOTAL_DUR), "-i", LOGO]
inputs += ["-ss", str(AUDIO_START), "-i", AUDIO]
LOGO_IDX = len(clips)
AUDIO_IDX = len(clips) + 1

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
assert abs(cum - TOTAL_DUR) < 1e-6

# title text timing
t_in, t_hold_end, t_out = 1.3, 7.5, 8.1
title_alpha = (
    f"if(lt(t,{t_in}),0,"
    f"if(lt(t,{t_in+0.5}),(t-{t_in})/0.5,"
    f"if(lt(t,{t_hold_end}),1,"
    f"if(lt(t,{t_out}),({t_out}-t)/0.5,0))))"
)

# Cross Club / date: appears during slide 4, fades out before slide 5 takes over
d_in, d_out_start, d_out_end = 10.5, 13.6, 14.2
date_alpha = (
    f"if(lt(t,{d_in}),0,"
    f"if(lt(t,{d_in+0.6}),(t-{d_in})/0.6,"
    f"if(lt(t,{d_out_start}),1,"
    f"if(lt(t,{d_out_end}),({d_out_end}-t)/0.6,0))))"
)

# credit card text: fades in on slide 5, holds to the end
c_in = offsets[-1] + 0.9
credit_alpha = (
    f"if(lt(t,{c_in}),0,"
    f"if(lt(t,{c_in+0.6}),(t-{c_in})/0.6,1))"
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
    f"fontsize=125:x=(w-text_w)/2:y=830:alpha='{date_alpha}'[t4]"
)
filters.append(
    f"[t4]drawtext={drawtext_common}:text='Vydalo Poezie, vole!{PAD}':"
    f"fontsize=62:x=(w-text_w)/2:y=1500:alpha='{credit_alpha}'[t5]"
)
filters.append(
    f"[t5]drawtext={drawtext_common}:text='© Mirek Mrkvička, 2026{PAD}':"
    f"fontsize=50:x=(w-text_w)/2:y=1650:alpha='{credit_alpha}'[t6]"
)
filters.append(
    f"[t6]drawtext={drawtext_common}:text='poezievole.cz{PAD}':"
    f"fontsize=58:x=(w-text_w)/2:y=1750:alpha='{credit_alpha}'[vtext]"
)

# logo: fade its own alpha in at the same moment as the credit text, then overlay
filters.append(
    f"[{LOGO_IDX}:v]format=rgba,fade=t=in:st={c_in}:d=0.6:alpha=1[logo]"
)
filters.append(
    f"[vtext][logo]overlay=x=(W-w)/2:y=1120:format=auto[vout]"
)

fade_out_start = TOTAL_DUR - 1.2
filters.append(
    f"[{AUDIO_IDX}:a]atrim=0:{TOTAL_DUR},volume=9dB,afade=t=in:st=0:d=1,afade=t=out:st={fade_out_start}:d=1.2[aout]"
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
print("TOTAL_DUR:", TOTAL_DUR, "credit_in:", c_in)
print("returncode:", result.returncode)
if result.returncode != 0:
    print(result.stderr[-4000:])
else:
    print("OK ->", OUT)
