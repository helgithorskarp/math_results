# Complete independent mixed-mean audit

six-reviewer-1 / independent mathematical reviewer. Read REVIEW.md for the
complete verdict and boundaries, PROOF.md for the reconstruction and proved
negative-mean extension, and DEPENDENCIES.json for exact written/operation pins.

Requires CPython3.12 standard library only; observed version3.12.14. From this
source directory, choose an output directory outside the source and run:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py all /tmp/mixed-mean-record
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B validate.py /tmp/mixed-mean-validation
```

The first command reconstructs eighteen entire original-root records, two full
physical-scalar records and all complete controls, using serial bounded children.
It saves their entire combined269286-byte mathematical record as `whole.json`.
The second performs normal/optimized and cold source-only replays and intended
mathematical/source rejections. Native solver/BLAS/OpenMP threads are one; each
mathematical child is fixed at45 seconds. A timeout or incomplete run is failure
to complete the check, not a theorem or nonexistence proof. No ancestor working
tree, producer program, fixture, certificate corpus or external package is used.

PRIMARY_SEAL.json guards all eight mathematical sources before their imports.
EXPECTED.json fingerprints the entire regenerated record only after every
mathematical gate passes. The generated corpus stays outside publication;
VALIDATION.json is the compact observed evidence. The manual analytic bridges
are stated in PROOF.md and remain unformalized.
