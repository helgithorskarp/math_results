# Four-deletion capped affine-table boundary

six-downset-3, researcher. For the specified triangle-majority downsets
with four bcx deletions, real affine-table/four-edge capped feasibility
holds exactly for q>=13. A two-valued integer PSD dual excludes q4..12;
five new 23-orbit certificates cover q13..17 at kappa=1/4096,t=4. The
q>=18 tail and undeleted spectral floors are explicitly credited premises.
See [PROOF.md](PROOF.md) for hypotheses and the ordinary bridges.
This result concerns an ansatz; general spectral H/I remain open.

Python3.12.14, standard library only. Keep the published directory layout:
[inputs.py](inputs.py) verifies the adjacent literal table and exact
arithmetic helper before import. All required inputs are compact source.

From this directory run:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py
sha256sum -c SHA256SUMS
```

Both modes must print PASS and the same record SHA256, exclude q4..12,
confirm the five positive classes, check235751 whole ordered entries,
and reject11 mathematical damages. [EXPECTED.json](EXPECTED.json) freezes
the full deterministic records; [RESULTS.json](RESULTS.json) records the
actual run costs and hashes. `--make-expected` refuses to overwrite the
frozen record and is not part of ordinary verification. Optional
`--record /absolute/scratch/path.json` keeps runtime records outside
this contribution directory.

Only order 23 PSD elimination and characteristic-polynomial checks are
used. No CAS, numerical library, solver, large data, credential or private
ledger is needed. Exactness is checked computationally; complete orbit,
real dual, lifting, infinite-tail and equality arguments remain written
unformalized mathematics. Independent review is pending.
