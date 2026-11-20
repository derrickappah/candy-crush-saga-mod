from PIL import Image
import subprocess, sys

im = Image.open(r"C:\Users\DELL\Downloads\candy crach 2\work\n5.png").convert("RGB")
py = sys.executable
for i, x in enumerate(range(230, 860, 60)):
    for y in (1000, 1040, 1080):
        c = im.crop((x, y, x + 90, y + 70))
        c = c.resize((c.width * 6, c.height * 6), Image.LANCZOS)
        p = rf"C:\Users\DELL\Downloads\candy crach 2\work\g{i}_{y}.png"
        c.save(p)
        out = subprocess.run([py, r"C:\Users\DELL\Downloads\candy crach 2\work\ocr.py", p],
                             capture_output=True, text=True).stdout
        lines = [l for l in out.splitlines()[1:] if l.strip()]
        if lines:
            print(x, y, lines[0][:40])
