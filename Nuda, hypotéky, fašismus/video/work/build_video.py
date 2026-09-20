# -*- coding: utf-8 -*-
import subprocess

WORK = r"c:\Repozitáře\nudaHypotekyFasismus\video\work"
AUDIO = r"c:\Repozitáře\nudaHypotekyFasismus\video\Classicals.de - Chopin - Nocturne Op. 9 no. 1 in B-flat minor.mp3"
OUT = r"c:\Repozitáře\nudaHypotekyFasismus\video\Promo_Nuda_hypoteky_fasismus.mp4"

CORONET = "C\\:/Program Files/Scribus 1.6.5/share/fonts/URWFonts-1.41/Coronet.ttf"

# trailing non-breaking spaces work around an ffmpeg drawtext clipping bug where
# the last glyph's right-side overhang (common in italic/script fonts) gets cut
# off by the auto-sized text_w render surface
PAD = "\u00a0\u00a0\u00a0"

clips = [
    "postel_prep_clip.mp4",
    "21e0f25e-d92f-494d-b60a-54b0e60d95ca_prep_clip.mp4",
    "314de715-4684-46e7-83c1-16896670eec5_prep_clip.mp4",
    "Nuda_obrazek_prep_clip.mp4",
]

CLIP_DUR = 3.5
XFADE = 0.4
TOTAL_DUR = len(clips) * CLIP_DUR - (len(clips) - 1) * XFADE  # 12.8
AUDIO_START = 100  # 1:40

inputs = []
for c in clips:
    inputs += ["-i", f"{WORK}\\{c}"]
inputs += ["-ss", str(AUDIO_START), "-i", AUDIO]

# xfade chain
filters = []
offset = CLIP_DUR - XFADE
filters.append(f"[0:v][1:v]xfade=transition=fade:duration={XFADE}:offset={offset}[v01]")
offset2 = offset + CLIP_DUR - XFADE
filters.append(f"[v01][2:v]xfade=transition=fade:duration={XFADE}:offset={offset2}[v012]")
offset3 = offset2 + CLIP_DUR - XFADE
filters.append(f"[v012][3:v]xfade=transition=fade:duration={XFADE}:offset={offset3}[vcat]")

# title text timing
t_in, t_hold_end, t_out = 2.0, 6.9, 7.5
title_alpha = (
    f"if(lt(t,{t_in}),0,"
    f"if(lt(t,{t_in+0.6}),(t-{t_in})/0.6,"
    f"if(lt(t,{t_hold_end}),1,"
    f"if(lt(t,{t_out}),({t_out}-t)/0.6,0))))"
)

# date/place text timing
d_in = 9.2
date_alpha = (
    f"if(lt(t,{d_in}),0,"
    f"if(lt(t,{d_in+0.6}),(t-{d_in})/0.6,1))"
)

drawtext_common = f"fontfile='{CORONET}':fontcolor=white:shadowcolor=black@0.7:shadowx=2:shadowy=2"

filters.append(
    f"[vcat]drawtext={drawtext_common}:text='Křest sbírky Mirka Mrkvičky{PAD}':"
    f"fontsize=56:x=(w-text_w)/2:y=650:alpha='{title_alpha}'[t1]"
)
filters.append(
    f"[t1]drawtext={drawtext_common}:text='Nuda, hypotéky, fašismus{PAD}':"
    f"fontsize=78:x=(w-text_w)/2:y=750:alpha='{title_alpha}'[t2]"
)
filters.append(
    f"[t2]drawtext={drawtext_common}:text='Cross Club{PAD}':"
    f"fontsize=68:x=(w-text_w)/2:y=1550:alpha='{date_alpha}'[t3]"
)
filters.append(
    f"[t3]drawtext={drawtext_common}:text='29. 9. 2026  ·  19\\:00{PAD}':"
    f"fontsize=56:x=(w-text_w)/2:y=1660:alpha='{date_alpha}'[vout]"
)

# audio: trim to total duration, fade out at the end
fade_out_start = TOTAL_DUR - 1.2
filters.append(
    f"[4:a]atrim=0:{TOTAL_DUR},afade=t=in:st=0:d=1,afade=t=out:st={fade_out_start}:d=1.2[aout]"
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

print(" ".join(f'"{c}"' if " " in c else c for c in cmd))
result = subprocess.run(cmd, cwd=WORK, capture_output=True, text=True)
print("returncode:", result.returncode)
if result.returncode != 0:
    print(result.stderr[-4000:])
else:
    print("OK ->", OUT)
