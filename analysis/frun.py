import sys, time, frida

dev = frida.get_device_manager().add_remote_device("127.0.0.1:27042")
session = dev.attach("Gadget")
src = open(sys.argv[1], encoding="utf-8").read()
script = session.create_script(src)
script.on("message", lambda m, d: print("MSG", m, flush=True))
script.load()
print("loaded; observing", sys.argv[2] if len(sys.argv) > 2 else "10", "s", flush=True)
time.sleep(float(sys.argv[2]) if len(sys.argv) > 2 else 10)
