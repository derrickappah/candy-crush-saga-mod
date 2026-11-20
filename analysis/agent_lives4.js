const m = Process.findModuleByName("libcandycrushsaga.so");
let p = null, done = false;

Interceptor.attach(m.base.add(0x1ec9c4c), {
  onEnter() {
    const q = this.context.x1;
    if (!q || q.isNull()) return;
    if (!p) p = q;
    if (done) return;
    done = true;
    const start = q.readS32();
    send("start=" + start + " max=" + q.add(0x14).readS32() + " struct=" + q);
    q.writeS32(0);
    let last = -1, i = 0;
    const iv = setInterval(() => {
      i++;
      try {
        const v = q.readS32();
        if (v !== last) { send("+" + (i * 100) + "ms lives=" + v + " ts=" + q.add(8).readS64()); last = v; }
      } catch (e) { send("gone"); }
      if (i > 40) clearInterval(iv);
    }, 100);
  },
});
send("ready");
