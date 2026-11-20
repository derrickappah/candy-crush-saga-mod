const m = Process.findModuleByName("libcandycrushsaga.so");
const A = [0x21cef50,0x21cf074,0x21d20b0,0x21d20b4,0x21d02e4,0x21d09b0,0x21cf0e8,0x21cf654,0x21d09e0,0x21d2224,0x21d200c,0x21d20b8,0x21d29a0,0x21d22f8,0x21d2664,0x21d2818,0x21d2860,0x21d2878,0x21d2018,0x21d1dd8,
           0x21cf064,0x21cf098,0x21d283c,0x21d286c,0x21d2998,0x21d0414,0x21d09c4,0x21cf64c,0x21d02dc,0x21d09f4,0x21d2288,0x21d2010,0x21d2168,0x21d2d88,0x21d2430,0x21d273c,0x21d2004];
const seen = {};
let n = 0;

for (const a of A) {
  try {
    Interceptor.attach(m.base.add(a), {
      onEnter() {
        const k = a.toString(16);
        if (seen[k] || n++ > 120) return;
        seen[k] = 1;
        send("hit " + k + " self=" + this.context.x0 + " a1=" + this.context.x1);
      },
    });
  } catch (e) {}
}
send("hooked " + A.length);
