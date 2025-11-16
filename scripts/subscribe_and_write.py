# subscribe_and_write.py

import os
import time
from whad_utils import connect_fast, resolve_write_handle, enable_notifications, _safe_disconnect

TARGET_MAC = os.environ.get("TARGET_MAC", "02:80:e1:78:42:d0")
CHAT_SERVICE_UUID = os.environ.get("CHAT_SERVICE_UUID", "d973f2e0-b19e-11e2-9e96-0800200c9a66")
NOTIFY_CHAR_UUID = os.environ.get("NOTIFY_CHAR_UUID", "d973f2e1-b19e-11e2-9e96-0800200c9a66")
WRITE_CHAR_UUID = os.environ.get("WRITE_CHAR_UUID", "d973f2e2-b19e-11e2-9e96-0800200c9a66")
RUN_DURATION_S = float(os.environ.get("RUN_DURATION_S", "300"))
WRITE_SLEEP_S = float(os.environ.get("WRITE_SLEEP_S", "0.02"))
VERBOSE = True


def main():
    t_end = time.time() + RUN_DURATION_S
    total = 0
    c = dev = ch = None
    payload = bytes(range(20))
    try:
        c, dev = connect_fast(TARGET_MAC, do_discover=True)
        cccd = enable_notifications(dev, NOTIFY_CHAR_UUID)
        if not cccd:
            raise RuntimeError("failed to enable notifications (CCCD not found)")
        if VERBOSE:
            print(f"[info] notifications enabled via CCCD handle {cccd}")
        h = resolve_write_handle(dev, CHAT_SERVICE_UUID, WRITE_CHAR_UUID)
        if not h:
            raise RuntimeError("no writable handle (after discovery retries)")
        try:
            ch = dev.find_characteristic_by_handle(h)
        except Exception:
            ch = dev.find_characteristic_by_uuid(WRITE_CHAR_UUID)

        while time.time() < t_end:
            try:
                ch.write(payload, with_response=False)
                total += 1
                if WRITE_SLEEP_S:
                    time.sleep(WRITE_SLEEP_S)
            except Exception as e:
                if VERBOSE:
                    print(f"[warn] transient write: {e}")
                break
        if VERBOSE:
            print(f"[done] wrote {total} packets")
    finally:
        _safe_disconnect(c, dev)


if __name__ == "__main__":
    main()
