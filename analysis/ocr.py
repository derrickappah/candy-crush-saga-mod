import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()
for path in sys.argv[1:]:
    print("=====", path)
    res, _ = engine(path)
    if not res:
        print("(no text detected)")
        continue
    for box, text, score in res:
        xs = [p[0] for p in box]
        ys = [p[1] for p in box]
        print(f"{score:.2f}  x={int(min(xs))}-{int(max(xs))} y={int(min(ys))}-{int(max(ys))}  {text}")
