# Independent review of the unrestricted Book Ramsey global cuts

**six-reviewer-3, independent mathematical reviewer.** The
[review](REVIEW.md) confirms degrees8..11, at most112 red edges and the
degree-eleven neighborhood/endpoint restrictions for every ordinary
red-B4/blue-B7 avoiding22-vertex coloring. It independently audits the
uniform-incidence dependency and proves a further high-neighbor load cut.
The Ramsey interval remains22..23; no surviving histogram is asserted
realizable.

CPython3.11+ standard library only, from the repository root:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B book_ramsey_global_cut_review3/audit.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B -O book_ramsey_global_cut_review3/audit.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B book_ramsey_global_cut_review3/controls.py
~~~

The audit compares its deterministic output with [expected.json](expected.json).
Its independent static-edge reduction enumerates147456 template completions;
all188 root/neighborhood survivors have literal forbidden books.
It checks6006 weight-six incidence candidates by exact rational projection,
144 literal full22 identity controls, the weighted joint-root cases and
both endpoint histograms. [INPUT.json](INPUT.json) contains attributed
compact fixtures/certificates, with original source commits and hashes.
No researcher executable is imported.

The six corruption controls produce [controls_expected.json](controls_expected.json).
Some graph controls violate the book caps; they test identities only.
The written proof, prior capacity/local-degree results, historical
Bussemaker–Cvetković–Seidel spectral classification and complete finite
checker remain explicit trust boundaries. This is independent review,
not proof-assistant formalization.

Resources and interpreter are recorded in [VALIDATION.json](VALIDATION.json).
All jobs are sequential with numerical thread settings one, using
about1.5seconds and21MiB; no generated corpus or third-party package is needed.
