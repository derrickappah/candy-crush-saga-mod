import sys, re

path, key = sys.argv[1], sys.argv[2].encode()
after = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
raw = open(path, "rb").read()
i = raw.find(key)
if i < 0:
    sys.exit("not found")
seg = raw[max(0, i - 200): i + after].decode("utf-8", "replace")
seg = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", " ", seg)
print(seg)
