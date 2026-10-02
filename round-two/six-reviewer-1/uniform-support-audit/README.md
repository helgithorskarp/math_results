# Near-cube support audit

Reviewer **six-reviewer-1**, independent mathematical reviewer.
See [REVIEW.md](REVIEW.md) for the all-real theorem, infinite-coverage proof,
conditional n10 premise and exact eleven-point improvement.

From this directory, with CPython3.12.14 and no third-party packages:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B check.py --check expected.json
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B -O check.py --check expected.json
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B controls.py --check controls_expected.json
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B -O controls.py --check controls_expected.json
```

Run serially. The POSIX alarm is45s; the recorded outer guard is50s.
Every whole canonical fixture byte must match, including field types.
The7154-byte main SHA256 is
`12f68012099b4dc2d22e5fc139fdde71afcadcb3ae939dd04d685c40f88b9f20`;
the834-byte control SHA256 is
`71e73ef8c98c6406525ec1966b2d0c4b88a50f712d66cfc770b6296f18114b3f`.

Exact computation uses the small `algebra.py` kernel copied from this
reviewer's prior even-angular audit. New author executables/fixtures and
the peer's overlapping message were inspected only after the first
independent record was frozen. `VALIDATION.json` records provenance,
separate later comparison/replays, runtimes and negative controls.

The finite checks validate identities, not a matrix enumeration. The
unbounded induction and real PSD/kernel bridges are written ordinary
mathematics. Literal matrices/trades are affine controls, not capped
examples. The greatest feasible S2 order10 corollary imports8499's known
ten-point certificate. There is no general H/I claim or optimal mass claim.
