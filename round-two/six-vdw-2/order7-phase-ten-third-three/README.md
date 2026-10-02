# Exact-ten third-selection bound THREE

Author: six-vdw-2, researcher. See [PROOF.md](PROOF.md) for precise H7/F617 scope and complete24-case reduction. No numerical W improvement or interval3704 witness.

Use Python3.11.2 with python-sat1.8.dev24/six1.17.0/CaDiCaL195, and drat-trim at the pinned upstream commit. From this directory, with generated outputs outsideGit:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /path/to/solver-venv/bin/python reproduce.py --work /path/to/fresh-work --converter /path/to/drat-trim
/path/to/solver-venv/bin/python guards.py --work /path/to/fresh-work --output /path/to/fresh-damage-work
```

Expected EXACT_H7_PHASE10_ADJACENT_THIRD_INDEX_AT_MOST3;24 checked cases,214464 additions/1475800 deletions/3675825 hints per strict mode for canonical proofs. To independently replay already available untrusted traces add `--certificate-cache /path/to/cache` with head/<stem>.cnf and head/<stem>.lrat. Full fresh model generation and both definition audits precede proof replay. Source reproduces large artifacts; none are uploaded. UNKNOWN/timeout proves no exclusion; do not repeat an identical bounded failure or increase shared scope caps.
