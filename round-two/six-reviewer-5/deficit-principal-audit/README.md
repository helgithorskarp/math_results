# Independent near-cube deficit audit

Actual six-reviewer-5, independent mathematical reviewer. See REVIEW.md for
scope, the local count erratum and the stronger full-principal relaxation;
DERIVATION.md gives the complete ordinary, unformalized derivation.
No actual capped H construction or general H/I resolution follows.

CPython3.12.14 and SymPy1.14.0 (including its mpmath1.3.0 dependency) were used.
Only algebra.py uses SymPy; all matrix and certificate checks use Python
integers/Fraction. Install SymPy1.14.0 in your own environment if needed.
From this directory run serially:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B reproduce.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O -B reproduce.py
python3 -B frozen.py
```

The two full replays regenerate and compare EVERY BYTE of PRIMARY.json:
32619B, SHA2566153e7ba393ef60ec20db3b22530c3213623aae1fad123db3b97c75db4888d79.
All12 frozen rational certificates pass; all12 semantic damages reject.
Each child has a fixed45s guard, with one child at a time. Temporary files
are outside the publication tree. PRIMARY-SEAL.json binds all original
primary source/proof/record bytes before target executable/fixture access.
Post-access bridge and controls are explicitly disclosed.

Optional network-dependent corroboration, separate from primary proof:

```sh
python3 -B corroborate.py
python3 -O -B corroborate.py
```

This fetches all16 files at the exact AUTHOR-SOURCE.json commit into temporary
storage, checks complete sizes/hashes, runs the unchanged native verifier
under a45s guard, then independently recomputes the ENTIRE scoped COMMON.json.
Expected native73825B SHA249b2778b1c92125ec9334a42846e86829c0df6074482b3a43a47d43f973304d;
COMMON70556B SHA3fc7fffdf5298122381194e2f1df4586c0e56a22ccc7f6e11512e800eee91b53.
No target runtime is imported by the bridge. Native corroboration and scoped
independent category correspondence are distinct from whole-cone verification.
No raw stream, solver, private ledger, credential or large proof corpus is an
input. For original literature and remaining coupling recovery see REVIEW.md.
