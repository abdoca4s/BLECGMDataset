# connect_churn.py

import os
import time
from whad_utils import connect_fast, _safe_disconnect

TARGET_MAC = os.environ.get("TARGET_MAC", "02:80:e1:78:42:d0")
RUN_DURATION_S = float(os.environ.get("RUN_DURATION_S", "300"))
VERBOSE = True


def main():
    t_end = time.time() + RUN_DURATION_S
    rounds = 0
    while time.time() < t_end:
        c = dev = None
        try:
            c, dev = connect_fast(TARGET_MAC, do_discover=False)
            rounds += 1
        except Exception as e:
            if VERBOSE:
                print(f"[warn] churn connect failed: {e}")
        finally:
            _safe_disconnect(c, dev)
    print("churn_rounds=", rounds, "duration_s=", RUN_DURATION_S)


if __name__ == "__main__":
    main()
