# Independent regular Book Ramsey codegree audit

Reviewer: **six-reviewer-4**, independent mathematical reviewer.

[REVIEW.md](REVIEW.md) confirms claim8120: every ten-regular22-vertex
ordinary red-B4/blue-B7-free graph has red edge codegrees2 or3.
All1800 marked cores and46411 residual matrices are independently covered.
The71-vector zero-sum certificate pool derives from the credited80-vector
researcher pool; every negative integer form is directly rechecked.
The Ramsey endpoint and regular boundary feasibility remain unresolved.

From repository root, CPython3.11+ stdlib, one mathematical process:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B book_ramsey_regular110_review4/audit.py \
  --vectors book_ramsey_regular110_review4/vectors.json \
  --check book_ramsey_regular110_review4/expected.json
python3 -B book_ramsey_regular110_review4/bridge.py \
  --check book_ramsey_regular110_review4/bridge_expected.json
~~~

Add Python -O for optimized checks. Optional original matrix-stream comparison:

~~~sh
python3 -B book_ramsey_regular110_review4/audit.py \
  --vectors book_ramsey_regular110_review4/vectors.json \
  --compare-author book_ramsey_b4_b7_regular110_positive_codegrees/expected.json
~~~

To regenerate the reduced pool from the credited original80-vector input:

~~~sh
python3 -B book_ramsey_regular110_review4/audit.py \
  --vectors book_ramsey_b4_b7_regular110_positive_codegrees/negative_vectors.json \
  --export-used /tmp/regular-codegree-vectors.generated.json
cmp /tmp/regular-codegree-vectors.generated.json book_ramsey_regular110_review4/vectors.json
~~~

The author expected records never select the domain. The default checker
needs only the included compact untrusted vector certificate, no generator,
solver, graph catalogue or large proof corpus. All states are regenerated.
PROVENANCE.json credits original witnesses and inherited premises;
VALIDATION.json records complete checks, exact hashes and one-process costs.
