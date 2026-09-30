"""Sequential frozen replay/controls and optional fresh weight generation."""
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
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                 "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        env[name] = "1"
    checker = [sys.executable, str(HERE / "verify.py")]
    base_flags = ["--base", str(HERE / "base/phase-269.json"), "--base-checker", str(HERE / "base/verify.py")]
    subprocess.run(checker+[str(HERE / "certificate.json"), *base_flags,
                           "--expected", str(HERE / "expected.json")], check=True, env=env, timeout=30)
    subprocess.run([sys.executable, str(HERE / "controls.py")], check=True, env=env, timeout=30)
    if args.regenerate:
        args.work.mkdir(parents=True, exist_ok=True)
        certificate = args.work / "fresh.json"
        subprocess.run([sys.executable, str(HERE / "generate.py"), "--output", str(certificate),
                        "--summary", str(args.work / "guidance.json")], check=True, env=env, timeout=30)
        subprocess.run(checker+[str(certificate), *base_flags, "--output", str(args.work / "checked.json")],
                       check=True, env=env, timeout=30)


if __name__ == "__main__":
    main()
