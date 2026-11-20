const MOD = "libcandycrushsaga.so";
const mod = Process.findModuleByName(MOD);
if (!mod) { send("module missing"); }
const base = mod.base;
send("base " + base);

const GET = base.add(0x2a033e0);   // ldr w0,[x0,#0x9a8]
const SET = base.add(0x2a02f1c);   // str w1,[x0,#0x9a8]

let seen = null;

Interceptor.attach(GET, {
  onEnter() { this.self = this.context.x0; },
  onLeave(ret) {
    const self = this.self;
    if (!seen) { seen = self; send("state obj = " + self); }
    if (ret.toInt32() === 0 || (self.equals(seen) && ret.toInt32() < 200)) {
      send("GET moves=" + ret.toInt32() + " self=" + self);
    }
  },
});

Interceptor.attach(SET, {
  onEnter() {
    const self = this.context.x0;
    const v = this.context.x1.toInt32();
    if (!seen) { seen = self; send("state obj(set) = " + self); }
    send("SET moves -> " + v + " self=" + self);
  },
});

// sanity: check vtable slot wiring once
send("hook installed");
