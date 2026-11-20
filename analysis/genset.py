import subprocess, re, sys, json

out = subprocess.run([sys.executable, "setters.py"], cwd=r"C:\Users\DELL\Downloads\candy crach 2\work",
                     capture_output=True, text=True).stdout
line = [l for l in out.splitlines() if l.startswith("[")][0]
addrs = json.loads(line)
addrs = sorted(set(addrs))
print(len(addrs))

js = """const m = Process.findModuleByName("libcandycrushsaga.so");
const A = %s;
const seen = {};
let n = 0;
A.forEach((a) => {
  try {
    Interceptor.attach(m.base.add(a), {
      onEnter() {
        const v = this.context.x1.toUInt32();
        if (v === 0 || v === 1) return;
        if (n++ > 400) return;
        send("set " + a.toString(16) + " v=" + v +
             " lr=" + this.returnAddress.sub(m.base));
      },
    });
  } catch (e) {}
});
send("ready " + A.length);
""" % json.dumps(addrs)
open(r"C:\Users\DELL\Downloads\candy crach 2\work\agent_set232.js", "w").write(js)
print("written")
