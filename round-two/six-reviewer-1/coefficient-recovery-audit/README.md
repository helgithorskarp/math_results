# Independent critical-coefficient recovery audit

Actual six-reviewer-1, independent mathematical reviewer. Confirms LEMMA9743,
actual author six-sendov-2, and proves a four-chart complex recovery predicate
and sharper pointwise real derivative bound. Complete ordinary proof is in
[PROOF.md](PROOF.md); publication assessment is in [REVIEW.md](REVIEW.md).
Unformalized; imported actual-real-original feasibility remains explicit.

Python3.10+ standard library only (run here CPython3.12). From repository root:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-reviewer-1/coefficient-recovery-audit/verify.py
python3 -I -B -O round-two/six-reviewer-1/coefficient-recovery-audit/verify.py
python3 -I -B round-two/six-reviewer-1/coefficient-recovery-audit/validate.py
```

Canonical SHA256 `9b363c8893b7517cc56d3660e14ba6957d6234874c900f719ef7f2a01c233530`,
287697 canonical bytes,141 complete identities, two full direct polynomial
Sylvester determinants, prime263 full unit, four complex recovery charts,
five bridge controls and three whole chart controls. EXPECTED.json stores
every coefficient, not aggregate hashes. Optional `verify.py --export PATH`
regenerates the full record; no export is required at runtime.

No producer import, CAS, root solver, ledger, key, network or private corpus
is a mathematical input. Defining written formulas were visible; this is
independent reconstruction, not blind discovery. The full code/proof/record
seal precedes target executable/fixture inspection. PROVENANCE.json and
NATIVE_REPLAY.json distinguish that ordering and late native corroboration.
The finite generic controls assert no actual stationary-original feasibility.
The proofs of the original-root interpretation, legal clearing, evaluation
column, Gauss and real positivity remain ordinary mathematics outside a
formal kernel. No uniform derivative floor, coupled Jacobian theorem,
stationary classification or first-power endpoint is claimed.

`validate.py` runs one child at a time, native threads1, fixed45s child guard;
no process limit is raised. A timeout is an operational failure. Its small
VALIDATION.json includes normal/O/cold runs and7 source/6 optimized-fixture
semantic rejection checks. Native replay uses separately pinned producer
sources only after the seal and is not an independent method.
