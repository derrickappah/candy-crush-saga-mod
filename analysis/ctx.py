import sys, re

path = sys.argv[1]
raw = open(path, "rb").read()
key = sys.argv[2].encode()
start = 0
while True:
    i = raw.find(key, start)
    if i < 0:
        break
    seg = raw[max(0, i - 700): i + 500].decode("utf-8", "replace")
    seg = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", " ", seg)
    print(f"--- at {i:#x}\n{seg}\n")
    start = i + 1
