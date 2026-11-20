import subprocess, re, sys, json

out = subprocess.run([sys.executable, "balget3.py"], cwd=r"C:\Users\DELL\Downloads\candy crach 2\work",
                     capture_output=True, text=True).stdout
addrs = sorted({int(a, 16) for a in re.findall(r"^\s+(0x[0-9a-f]+)", out, re.M)})
print(len(addrs))

js = """const m = Process.findModuleByName("libcandycrushsaga.so");
const A = %s;
const cnt = {};
A.forEach((a) => { cnt[a.toString(16)] = 0; });
A.forEach((a) => {
  try { Interceptor.attach(m.base.add(a), { onEnter() { cnt[a.toString(16)]++; } }); } catch (e) {}
});
setInterval(() => {
  const rows = Object.keys(cnt).filter((k) => cnt[k] > 0)
    .sort((x, y) => cnt[y] - cnt[x]).slice(0, 8)
    .map((k) => k + "=" + cnt[k]);
  send(rows.join(" "));
}, 4000);
send("ready " + A.length);
""" % json.dumps(addrs)
open(r"C:\Users\DELL\Downloads\candy crach 2\work\agent_cnt.js", "w").write(js)
print("written")
