# discovery_loop.py

import os
import time
from whad_utils import connect_fast, _safe_disconnect

TARGET_MAC = os.environ.get("TARGET_MAC", "02:80:e1:78:42:d0")
RUN_DURATION_S = float(os.environ.get("RUN_DURATION_S", "300"))
DISCOVERY_SLEEP_S = float(os.environ.get("DISCOVERY_SLEEP_S", "0.01"))
VERBOSE = True


def main():
    t_end = time.time() + RUN_DURATION_S
    total = 0
    c = dev = None
    while time.time() < t_end:
        try:
            if not dev:
                c, dev = connect_fast(TARGET_MAC, do_discover=False)
            dev.discover(include_values=False)
            total += 1
            if DISCOVERY_SLEEP_S:
                time.sleep(DISCOVERY_SLEEP_S)
        except Exception as e:
            if VERBOSE:
                print(f"[warn] discovery transient: {e}")
            _safe_disconnect(c, dev)
            c = dev = None
            continue
    print("discoveries=", total, "duration_s=", RUN_DURATION_S)


if __name__ == "__main__":
    main()
