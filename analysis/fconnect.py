import sys, time, frida

dev = frida.get_device_manager().add_remote_device("127.0.0.1:27042")
print("device:", dev)
procs = dev.enumerate_processes()
print("processes:", len(procs))
for p in procs:
    print(" ", p.pid, p.name)

if len(sys.argv) > 1 and sys.argv[1] == "attach":
    session = dev.attach("Gadget")
    print("session:", session)
    script = session.create_script("send('hello from agent');")
    script.on("message", lambda m, d: print("MSG", m))
    script.load()
    time.sleep(2)
    session.detach()
