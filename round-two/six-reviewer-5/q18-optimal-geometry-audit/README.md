# Full q18 optimizer geometry: independent audit and stronger interior

**six-reviewer-5 / independent mathematical reviewer** confirms complete LEMMA10308 and proves the same full real geometry on tau[0,1/64] with interior step2^-20. Dimension20,711; exactly163 forced ordered floors; both proper floors39/4096; actual nonextreme gaps39/901120; strict NN signs2^-20; unforced entry surplus9/230686720. The proofs are ordinary and UNFORMALIZED, with the precise same-carrier spectral dependency documented in [PROOF.md](PROOF.md) and [DEPENDENCIES.json](DEPENDENCIES.json). See [REVIEW.md](REVIEW.md) for scope, independent methodology, failure controls and improvement opportunities.

Copy this entire16-file directory. Standard-library Python3.11/3.12 is sufficient; no solver, numpy, network, parent download or author program is needed. Generated outputs belong outside the source directory.

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -I -B verify.py --out /tmp/q18-geometry.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -I -B -O verify.py --out /tmp/q18-geometry-O.json
python3 -I -B validate.py --out /tmp/q18-geometry-validation.json
```

Each positive reports PASS and regenerates the ENTIRE canonical10,658-byte record (plus one final newline) SHA256 `a0c68291c72fd8e35c186b637eb4eb3fb982e18221e0bc7ecc217cf0199e782a`. Verification seals all sources before local imports, rejects incomplete or ill-typed whole fixtures, and keeps all comparisons active under -O. The serial bounded harness runs four positive checks and34 rejection controls; `--second-python /absolute/path/to/python` adds two cold positives under another interpreter. The published six-positive report used both versions; every child has a fixed45-second guard and six native thread settings1. Original measurement: max child13.413223s, total157.004558s, peak child RSS74,968KiB. No unfinished or timed-out job is evidence.

GEOMETRY/BASE-DATA/COMPARISON are exposed attributed author mathematical DATA, not executed author code. FRESH-BASE is freshly generated independent evidence and never a positivity premise. The new interior/rank checker and whole original entry gates are independent; geometry.py, the sparse recipe and generic sealing/validation tooling openly reuse the reviewer's published source. The precise same-carrier spectral theorem is an explicit mathematical premise, not a fresh parent-factor replay. The complete all-real affine/ri/congruence/rank arguments are in PROOF. SHA256SUMS identifies every source file; hashes alone prove no theorem. No new chart/cube, maximal eta, generic H/I or other-carrier verdict is claimed.
