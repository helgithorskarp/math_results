# Independent asymmetric angular audit

Actual reviewer: **six-reviewer-1**, independent mathematical reviewer.
Target: committed lemma8800, source167af56c25651784f7c8106a3ec1d85e52b51c82.
Read [REVIEW.md](REVIEW.md) for the theorem, prerequisites, independent
methods, complete case coverage, stationary classification and stability.

Python3.11+ and the pinned [requirements.txt](requirements.txt) suffice.
Install dependencies in a local virtual environment or local target directory.
Do not copy the researcher's checker into this package. For a target install:

```sh
python3 -m pip install --target ./vendor -r requirements.txt
export PYTHONPATH=./vendor
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -B check.py
python3 -B -O check.py
```

Both runs compare all43 records with [expected.json](expected.json), including
the complete numerator, all four root/lift/value/Hessian enclosures, and a
hash of the complete resultant coefficient sequence. Four internal damages
must reject. Exact rational root endpoints are reconstructed/checked inputs,
not numerical approximations. The146 literal point determinants and proved
degree bound independently verify the universal resultant identity.
`python3 -B check.py --emit` explicitly regenerates the compact fixture;
the default never overwrites it. `--expected PATH` selects a fixture and
rejects any discrepancy with the full independently computed output.

Validation used CPython3.12.14 and SymPy1.14.0, sequential processes and native
threads1. Independent normal/optimized runs took21.041/24.683seconds; maximum
recorded cumulative child RSS71,492KiB. Separate author replays took1.314/1.459
seconds and retain their author-replay label. All math commands had fixed45s
parent guards; no timeout or incomplete computation supported a conclusion.
Additional optimized altered-fixture checks are recorded in
[provenance.json](provenance.json). No solver, numerical root or formal kernel
is used. The full-sphere/global first-power endpoint remains unresolved.
