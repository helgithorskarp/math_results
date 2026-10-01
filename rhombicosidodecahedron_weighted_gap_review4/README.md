# Weighted RID receiving-gap audit

**six-reviewer-4, independent mathematical reviewer.**

[REVIEW.md](REVIEW.md) confirms graph claim 8058: every strict RID passage
requires \(f(n)^2<\beta-1/100\), with exactly 120 equality orientations
on the stated winning receiving band. Global non-Rupertness remains open.
The review explicitly separates independent checks, native reproduction
and inherited geometric prerequisites.

From the repository root, run sequentially with Python 3.11+:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B rhombicosidodecahedron_weighted_gap_review4/audit.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B -O rhombicosidodecahedron_weighted_gap_review4/audit.py
~~~

No packages, solver or author code imports are required. The ten proposed
probe inputs in [PROBES.json](PROBES.json) are independently checked
against the regenerated original body. The result must match
[EXPECTED.json](EXPECTED.json), 8,128 bytes, SHA256
992e4cc9ea7f588d6e440d6e3862937ee9c3d949b1a9c26a44de21b407fa1aed.

[VALIDATION.json](VALIDATION.json) records successful ordinary/optimized
independent runs and the separate fixed-source author replay.
[PROVENANCE.json](PROVENANCE.json) records the reviewed source commit,
input hashes, graph prerequisites and primary literature.
