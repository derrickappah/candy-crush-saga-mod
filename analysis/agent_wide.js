const m = Process.findModuleByName("libcandycrushsaga.so");
const LISTS = {
  pre: [0x21cef50,0x21cf074,0x21d20b0,0x21d20b4,0x21d02e4,0x21d09b0,0x21cf0e8,0x21cf654,
        0x21d09e0,0x21d2224,0x21d200c,0x21d20b8,0x21d29a0,0x21d22f8,0x21d2664,0x21d2818,
        0x21d2860,0x21d2878,0x21d2018,0x21d1dd8,0x21cf064,0x21cf098,0x21d283c,0x21d286c,
        0x21d2998,0x21d0414,0x21d09c4,0x21cf64c,0x21d02dc,0x21d09f4,0x21d2288,0x21d2010,
        0x21d2168,0x21d2d88,0x21d2430,0x21d273c,0x21d2004],
  btn: [0x1eb5d24,0x1eb5e20,0x1eb5f18,0x1e92bb0,0x1e92bb4,0x1eb5f28,0x1eb5f38,0x1eb5f48,
        0x1eb5f58,0x1eb5f68,0x1eb5fac,0x1eb6020,0x1eb5fbc,0x1eb601c,0x1eb5fcc,0x1eb5fdc,
        0x1eb5fec,0x1e92be4,0x1eb5ffc],
  amt: [0x22fafd0, 0x22fb0f8, 0x22faeec],
};

const seen = {};
let n = 0;

function install(list, tag) {
  list.forEach((a, i) => {
    try {
      Interceptor.attach(m.base.add(a), {
        onEnter() {
          const k = tag + i;
          if (seen[k] || n++ > 150) return;
          seen[k] = 1;
          send("HIT " + tag + "[" + i + "] " + a.toString(16) +
               " self=" + this.context.x0 + " arg1=" + this.context.x1);
        },
      });
    } catch (e) {}
  });
}

for (const k of Object.keys(LISTS)) install(LISTS[k], k);
send("ready hooked=" + (LISTS.pre.length + LISTS.btn.length + LISTS.amt.length));
