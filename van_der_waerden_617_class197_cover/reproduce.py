"""Sequential frozen replay, controls, and optional fresh numerical rediscovery."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).parent


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--regenerate", action="store_true")
    p.add_argument("--work", type=Path, default=HERE / "build")
    args = p.parse_args()
    env = dict(os.environ)
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        env[key] = "1"
    subprocess.run([sys.executable, str(HERE / "check_all.py"), "--expected", str(HERE / "expected.json")],
                   env=env, check=True, timeout=30)
    subprocess.run([sys.executable, str(HERE / "controls.py")], env=env, check=True, timeout=30)
    if args.regenerate:
        args.work.mkdir(parents=True, exist_ok=True)
        fresh = args.work / "fresh"
        subprocess.run([sys.executable, str(HERE / "generate.py"), "--work", str(fresh)],
                       env=env, check=True, timeout=150)
        subprocess.run([sys.executable, str(HERE / "check_all.py"), "--certificates", str(fresh),
                        "--output", str(args.work / "fresh-checked.json")], env=env, check=True, timeout=30)


if __name__ == "__main__":
    main()
