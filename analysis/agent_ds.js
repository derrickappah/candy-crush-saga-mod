const m = Process.findModuleByName("libcandycrushsaga.so");
let n = 0;

function key(ctx) {
  try {
    const p = ctx.x1;
    const len = ctx.x2.toInt32() & 0xffff;
    if (len > 0 && len < 40) return p.readCString(len);
  } catch (e) {}
  return "?";
}

for (const off of [0x200451c, 0x20047f8]) {
  try {
    Interceptor.attach(m.base.add(off), {
      onEnter() {
        if (n++ > 300) return;
        let d = 0;
        try { d = this.context.sp.add(0x30).readDouble(); } catch (e) {}
        send("f" + off.toString(16) + " key=" + key(this.context) +
             " sp30=" + d + " x3=" + (() => { try { return this.context.x3.readCString(12); } catch (e) { return "?"; } })());
      },
    });
  } catch (e) { send("hook err " + e); }
}
send("ready");
