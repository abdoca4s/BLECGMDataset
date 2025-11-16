# subscribe_notify.py

import os
import time
from whad_utils import connect_fast, enable_notifications, _safe_disconnect

TARGET_MAC = os.environ.get("TARGET_MAC", "02:80:e1:78:42:d0")
NOTIFY_CHAR_UUID = os.environ.get("NOTIFY_CHAR_UUID", "d973f2e1-b19e-11e2-9e96-0800200c9a66")
RUN_DURATION_S = float(os.environ.get("RUN_DURATION_S", "300"))
VERBOSE = True


def main():
    t_end = time.time() + RUN_DURATION_S
    c = dev = None
    try:
        c, dev = connect_fast(TARGET_MAC, do_discover=True)
        h = enable_notifications(dev, NOTIFY_CHAR_UUID)
        if not h:
            raise RuntimeError("failed to enable notifications (CCCD not found)")
        if VERBOSE:
            print(f"[info] notifications enabled via CCCD handle {h}")
        while time.time() < t_end:
            time.sleep(0.25)
    finally:
        _safe_disconnect(c, dev)


if __name__ == "__main__":
    main()
