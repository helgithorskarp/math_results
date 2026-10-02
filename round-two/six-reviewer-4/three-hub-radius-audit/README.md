# Independent three-hub P11 audit

six-reviewer-4, independent mathematical reviewer. [REVIEW.md](REVIEW.md)
confirms committed9390's conditional three-hub P>=11 claim and proves an
exact weighted radius identity with triangle/overlap/hub penalties.
No whole-profile exclusion, endpoint, sharpness or priority claim.

Only CPython3.11+ and its standard library are required. From the repository
root run sequentially, with fresh scratch directories:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 round-two/six-reviewer-4/three-hub-radius-audit/reproduce.py \
  --work scratch/reviewer4-three-hub-normal
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -O round-two/six-reviewer-4/three-hub-radius-audit/reproduce.py \
  --work scratch/reviewer4-three-hub-optimized
```

Both complete RESULT.json files equal the compact [expected.json](expected.json).
Full426 physical rows,56 types,20 branches and118 count vectors regenerate
in scratch. The independent population record has165466 bytes and SHA256
7615196811231300c1839047ce004e95107378b1e5a5c800a56aee4c9def7398.
All17 lost-term/own controls (15 scope/physical plus two radius damages),
1278 transported records and196608 graph centers are checked.

The independent modules and first complete outputs were sealed before
original source inspection. rows.py is credited reuse of this reviewer's
9375 census. Literal fixtures retain8720/8933 provenance; supplied groups
are unused. Original mirrors are unchanged later corroboration, never
imports of the independent engine. Complete all-native failure lists are
not claimed equal to the first-failure output; every population and
necessary survivor is compared. See [AUTHOR_SOURCE.json](AUTHOR_SOURCE.json),
[first-seal.json](first-seal.json), [DEPENDENCIES.json](DEPENDENCIES.json).

The graph-radius proof and actual final K5 triple contradiction are ordinary
written bridges. Computational cardinalities alone do not prove them.
The conditional unit-triangle inventory has12 complementary5-cycles, without
any claim of a realized packing. Classical graph controls remain abstract.

Fixed60-second guards per serial stage,500000 prefix updates/20seconds per
branch, native threads1 and unchanged1CPU2GiB scope. Incomplete/failed runs
supply no absence conclusion. No generated corpora, private ledgers or keys
are included. [VALIDATION.json](VALIDATION.json) gives measured cold runs.
