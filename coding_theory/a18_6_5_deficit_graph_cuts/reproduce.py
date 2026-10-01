"""Sequential exact production and separate certificate replay."""
import datetime
import json
import os
import resource
import subprocess
import sys
import time
from paths import BASE, WORK

def main():
    start = time.monotonic()
    env = dict(os.environ)
    env.update({x: "1" for x in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")})
    record = dict(agent="six-code-3", role="researcher", status="INCOMPLETE", started_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    path = WORK / "proof_run.json"
    path.write_text(json.dumps(record, indent=2) + "\n")
    for name in ("cut_certificate.py", "carrier.py", "verify.py"):
        subprocess.run([sys.executable, "-B", str(BASE / name)], env=env, check=True, timeout=55)
    record.update(status="COMPLETE; cut certificate, full six-point carrier and literal verification passed",
                  seconds=round(time.monotonic() - start, 6),
                  parent_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    path.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record))

if __name__ == "__main__":
    main()
