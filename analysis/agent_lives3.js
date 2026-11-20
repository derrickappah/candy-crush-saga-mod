const m = Process.findModuleByName("libcandycrushsaga.so");
let p = null;
let n = 0;

Interceptor.attach(m.base.add(0x1ec9c4c), {
  onEnter() {
    const q = this.context.x1;
    if (!q || q.isNull()) return;
    if (!p) {
      p = q;
      const orig = q.readS32();
      send("STRUCT " + q + " lives=" + orig + " max=" + q.add(0x14).readS32());
      q.writeS32(0);
      send("forced lives=0");
      return;
    }
    if (n++ > 30) return;
    send("t" + n + " lives=" + q.readS32() + " ts=" + q.add(8).readS64());
  },
});
send("ready");
