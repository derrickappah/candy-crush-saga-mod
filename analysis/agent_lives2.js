const m = Process.findModuleByName("libcandycrushsaga.so");
let n = 0;

function dump(tag, p) {
  try {
    const lives = p.readS32();
    const interval = p.add(0x10).readS32();
    const max = p.add(0x14).readS32();
    let ts = 0;
    try { ts = p.add(8).readS64().toNumber(); } catch (e) {}
    send(tag + " lives=" + lives + " interval=" + interval + " max=" + max + " ts=" + ts);
  } catch (e) {
    send(tag + " ERR " + e);
  }
}

Interceptor.attach(m.base.add(0x1ec9c4c), {
  onEnter() {
    if (n++ > 24) return;
    const p = this.context.x1;
    if (p && !p.isNull()) dump("tick", p);
  },
});

Interceptor.attach(m.base.add(0x1ec9bfc), {
  onEnter() {
    if (n > 40) return;
    n++;
    const p = this.context.x2;
    const val = this.context.w1;
    if (p && !p.isNull()) dump("set(new=" + val + ")", p);
  },
});
send("ready");
