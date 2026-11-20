try {
  send(hexdump(ptr("0x7c3c6098c0").readByteArray(96), { ansi: false }));
} catch (e) {
  send("err " + e);
}
