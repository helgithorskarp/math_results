# RID threshold-band independent review

Actual author **six-reviewer-1**, independent mathematical reviewer.

[REVIEW.md](REVIEW.md) gives the exact theorem, universal geometric
bridges, two proved improvements, literature and trust boundaries.
The threshold-to-threshold part of claim8330 is confirmed at receiving
height83/200. The full global bound has winning and mixed dependencies
outside this verdict.

CPython3.11.2, standard library only. From the repository root, run
separately, with one CPU-intensive job at a time:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -I -B rhombicosidodecahedron_threshold_band_review1/verify.py
```

Repeat with `python3 -I -B -O` to check optimized execution. Each
complete run takes about9s and20MiB. Expected compact output reports
PASS,6144complete signed injections,168threshold leaves and8736strict
coefficients, with complete record SHA256
`e61385cf28ac6e2527f36d3b64f7869311b3f79917db3b893973e96f129139df`.
`--emit` prints the full mandatory8758byte record.

[fixture.json](fixture.json) contains only untrusted original edges and
fixed selected covers. The checker independently reconstructs all
original vertices, tangent disks, candidate pools, signed injections,
moment matrices, proper alignments, supports and tensor coefficients.
The complete record is [expected.json](expected.json).
No campaign code, external solver, network or private data is needed.
The exact field kernel is visibly copied from this reviewer's earlier
axial census, as credited in the review. The certificate choices retain
the researcher's credit. This is independent verification of those
choices, with a different interpolation and coverage implementation.

Nine intentionally damaged supports/coverage controls reject in both
modes; nine full interpolation identities are checked. Written geometry
remains outside a formal kernel. No large proof corpus is published.
