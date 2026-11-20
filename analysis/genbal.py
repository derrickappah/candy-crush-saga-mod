import zipfile, subprocess, json, re, sys

out = subprocess.run(
    [sys.executable, "balget3.py"], cwd=r"C:\Users\DELL\Downloads\candy crach 2\work",
    capture_output=True, text=True).stdout

addrs = re.findall(r"^\s+(0x[0-9a-f]+)", out, re.M)
addrs = sorted({int(a, 16) for a in addrs})
print(len(addrs))
js = """const m = Process.findModuleByName("libcandycrushsaga.so");
const A = %s;
const seen = {};
let n = 0;
A.forEach((a) => {
  try {
    Interceptor.attach(m.base.add(a), {
      onEnter() {
        const k = a.toString(16);
        if (seen[k] || n++ > 80) return;
        seen[k] = 1;
        send("hit " + k + " self=" + this.context.x0 + " lr=" + this.returnAddress.sub(m.base));
      },
    });
  } catch (e) {}
});
send("ready " + A.length);
""" % json.dumps(addrs)
open(r"C:\Users\DELL\Downloads\candy crach 2\work\agent_bal2.js", "w").write(js)
print("written")
