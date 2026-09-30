# Independent six-element spectral-downset audit

Author: **six-reviewer-4**, independent mathematical reviewer. See
[REVIEW.md](REVIEW.md) for the scoped verdict, completeness argument,
exceptional certificate and proved inertia refinement.

Run from the repository root with CPython 3.11.2 or a compatible Python 3,
standard library only. The target directory must contain the pinned files
from commit `145fedcf4a56269c398c1714c29567dce013ea23`. The exporter refuses
changed inputs. It imports the researcher source only to propose untrusted
partitions; the auditor independently generates every orbit and checks each
certificate. No catalog is required from another machine.

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B spectral_downset_six_review4/export_candidates.py --out /tmp/downset-six-review4.jsonl
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B spectral_downset_six_review4/census_audit.py --candidates /tmp/downset-six-review4.jsonl --expect spectral_downset_six_review4/expected.json
python3 -B spectral_downset_six_review4/controls.py
python3 -O -B spectral_downset_six_review4/controls.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O -B spectral_downset_six_review4/census_audit.py --candidates /tmp/downset-six-review4.jsonl --expect spectral_downset_six_review4/expected.json
```

Expected: 16,353 classes, 7,828,354 labeled downsets, 16,350 verified positive
partitions, two trivial classes and one exact exceptional certificate. The
full matrix has inertia (25,0,7), and the exception's fractional value is 35/3.
Normal and optimized output agree. `controls_expected.json` records nine
rejected mutations and all local inertia-bin spectra. Each command is a
single process; run sequentially. An interrupted or timed-out census is
incomplete, not a mathematical verdict. Approximate runtime is 59 seconds
for regeneration and 27 seconds per full independent audit, peak RSS 104 MiB.

`census_audit.py --n 5` independently enumerates smaller domains without
candidate files. `exception_audit.py` independently checks the exception
alone. The default full audit without `--candidates` performs the census
only; use the documented command to verify the mathematical certificates.

- [expected.json](expected.json): exact full-domain and exceptional results.
- [controls_expected.json](controls_expected.json): bounded negative controls.
- [provenance.json](provenance.json): pinned source and output hashes.
- [census_audit.py](census_audit.py): one-member growth, full permutation
  quotient, orbit matching and positive certificate validation.
- [exception_audit.py](exception_audit.py): direct rank/facet matrix formula,
  exact full congruence inertia and fractional primal/dual checks.
- [export_candidates.py](export_candidates.py): explicitly untrusted source
  bridge; source pins and stream-hash checks.
- [controls.py](controls.py): certificate rejection and inertia-template checks.

Keep the generated JSONL outside the publication directory. The algorithms
and mathematical argument are unformalized; Python exact arithmetic and the
reviewer code remain trust dependencies. General H and I remain unresolved;
this review also leaves the exceptional six-point I case unresolved.
