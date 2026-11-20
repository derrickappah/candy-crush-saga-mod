from PIL import Image
import numpy as np
import subprocess, sys

im = Image.open(r"C:\Users\DELL\Downloads\candy crach 2\work\b4.png").convert("RGB")
a = np.asarray(im).astype(int)
band = a[995:1205, 230:850]
# near-white text mask
mask = (band[:, :, 0] > 225) & (band[:, :, 1] > 225) & (band[:, :, 2] > 225)

# connected components (4-neighbour, simple BFS)
h, w = mask.shape
seen = np.zeros_like(mask, bool)
boxes = []
for y in range(h):
    for x in range(w):
        if not mask[y, x] or seen[y, x]:
            continue
        stack = [(y, x)]
        seen[y, x] = True
        ys, xs = [], []
        while stack:
            cy, cx = stack.pop()
            ys.append(cy); xs.append(cx)
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    stack.append((ny, nx))
        if 15 <= len(ys) <= 600:
            boxes.append((min(xs), min(ys), max(xs), max(ys)))

print("boxes", len(boxes))
py = sys.executable
for i, (x0, y0, x1, y1) in enumerate(boxes[:14]):
    cx0, cy0 = 230 + x0 - 18, 995 + y0 - 18
    crop = im.crop((max(0, cx0), max(0, cy0), cx0 + (x1 - x0) + 36, cy0 + (y1 - y0) + 36))
    crop = crop.resize((crop.width * 8, crop.height * 8), Image.LANCZOS)
    p = rf"C:\Users\DELL\Downloads\candy crach 2\work\blob{i}.png"
    crop.save(p)
    out = subprocess.run([py, r"C:\Users\DELL\Downloads\candy crach 2\work\ocr.py", p],
                         capture_output=True, text=True).stdout.strip().splitlines()
    txt = [l.split()[-1] for l in out[1:] if l.strip()]
    print(i, (x0, y0, x1, y1), txt)
