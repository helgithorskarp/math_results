"""Run one complete 537 branch; directly check SAT and proof-check UNSAT."""
import argparse
import hashlib
import subprocess
import tempfile
import time
from pathlib import Path

from audit import check as audit
from check import defects
from encode import write


def run(args):
    with tempfile.TemporaryDirectory(prefix="schur-six-branch-") as directory:
        root = Path(directory)
        cnf, proof, log = root / "case.cnf", root / "case.drat", root / "solver.log"
        info = write(cnf, args.branch)
        audit(cnf, args.branch)
        cmd = [str(args.kissat), "--sat", f"--time={args.seconds}",
               f"--seed={args.seed}", str(cnf)]
        if args.drat_trim:
            cmd.append(str(proof))
        start = time.monotonic()
        with log.open("w", encoding="ascii") as output:
            solved = subprocess.run(cmd, stdout=output, stderr=subprocess.STDOUT,
                                    check=False)
        elapsed = round(time.monotonic() - start, 2)
        content = log.read_text(encoding="ascii")
        if solved.returncode == 10 and "s SATISFIABLE" in content:
            true = {int(t) for line in content.splitlines()
                    if line.startswith("v ") for t in line.split()[1:]
                    if int(t) > 0}
            assert all(sum(6 * (v - 1) + c in true for c in range(1, 7)) == 1
                       for v in range(1, 538))
            word = "".join(str(next(c for c in range(1, 7)
                                    if 6 * (v - 1) + c in true))
                           for v in range(1, 538))
            assert word[0] == "1" and word[1] == "2" and word[-1] == str(args.branch)
            assert not defects(word)
            args.out.write_text(word + "\n", encoding="ascii")
            print("VERIFIED537", "branch", args.branch,
                  "word_sha256", hashlib.sha256((word + "\n").encode()).hexdigest(),
                  "out", args.out)
        elif solved.returncode == 20 and "s UNSATISFIABLE" in content:
            if not args.drat_trim:
                print("UNVERIFIED_UNSAT", "branch", args.branch,
                      "seconds", elapsed, "cnf_sha256", info["sha256"])
                return
            checked = subprocess.run([str(args.drat_trim), str(cnf), str(proof)],
                                     capture_output=True, text=True, check=False)
            if checked.returncode != 0 or "s VERIFIED" not in checked.stdout:
                raise RuntimeError(f"DRAT verification failed: {checked.stdout} {checked.stderr}")
            print("CERTIFIED_UNSAT", "branch", args.branch,
                  "proof_sha256", hashlib.sha256(proof.read_bytes()).hexdigest())
        elif solved.returncode == 0 and "s UNKNOWN" in content:
            print("UNKNOWN", "branch", args.branch, "seconds", elapsed,
                  "seed", args.seed, "cnf_sha256", info["sha256"])
        else:
            raise RuntimeError(f"unexpected solver result {solved.returncode}: {content[-1000:]}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch", type=int, choices=(1, 2, 3), required=True)
    parser.add_argument("--kissat", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path)
    parser.add_argument("--seconds", type=int, default=180)
    parser.add_argument("--seed", type=int, default=20261004)
    parser.add_argument("--out", type=Path, default=Path("/tmp/schur-six-537-word.txt"))
    args = parser.parse_args()
    if args.seconds <= 0 or args.seed < 0:
        parser.error("seconds must be positive and seed nonnegative")
    run(args)
