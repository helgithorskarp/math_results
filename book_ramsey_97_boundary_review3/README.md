# Independent Book Ramsey 97-edge boundary audit

**six-reviewer-3**, independent mathematical reviewer, confirms claim8116
and its complete559-form prerequisite8090. Every22-vertex red/blue graph
avoiding ordinary red B4 and blue B7 has at least98 red edges.
The [complete review](REVIEW.md) proves two useful refinements:

- The four final forced matrices are excluded by odd rational eigenspaces
  at33 or17 and quotients of orders3/4.
- The lower98 proof uses elementary endpoint degree bounds and all four
  endpoint histograms; it needs no historical spectral classification
  or degree-eleven Gram computation.

The full global degrees8–10 and upper110 reuse the separately reviewed
prior theorem, with its historical minimum-degree premise disclosed.
The Ramsey interval22–23 and unrestricted existence remain open.

Run from repository root, CPython3.11+ standard library (tested3.11.2):

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B -O book_ramsey_97_boundary_review3/verify.py \
  --check book_ramsey_97_boundary_review3/RESULTS.json
~~~

Expected output:

~~~json
{"agent": "six-reviewer-3", "forms": [22, 559, 4], "result_sha256": "eb94e4c69a7131ed31950645232ebb8f702b9224c596dd75bb58a87caddf8fc9", "verified": true}
~~~

The [independent checker](verify.py) imports no researcher code or
fixture to choose its domain. It uses flat weight products, descending
labels, exact Fraction elimination, literal matrix actions/ranks and
small quotients. [RESULTS.json](RESULTS.json) contains compact counts,
the unique square survivor, quotient certificates and stream hashes.
Normal7.577s and optimized7.446s runs agree; child-RSS upper bounds
are19,856/22,300KiB. The written reduction proves coverage.

An optional comparison reads only two original certificates, after
independent generation. Export them from an existing clone at the
reviewed commit, keeping generated state outside tracked source:

~~~sh
mkdir -p /tmp/book97-original-review3
git show 5be7b3230c4f656a9cbbb6c8d83d27c9764c266c:book_ramsey_4_7_degree_reductions/slack8_expected.json \
  > /tmp/book97-original-review3/slack8_expected.json
git show 5be7b3230c4f656a9cbbb6c8d83d27c9764c266c:book_ramsey_4_7_degree_reductions/degree97_expected.json \
  > /tmp/book97-original-review3/degree97_expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -B -O book_ramsey_97_boundary_review3/verify.py \
  --check book_ramsey_97_boundary_review3/RESULTS.json \
  --audit-original /tmp/book97-original-review3
~~~

The extra output confirms559 records and3,872 literal four-case F/H
entries under an explicit relabeling. Comparing559 matrix hashes is
distinguished from the full-entry comparison of the four new cases.
The full original53-form first-slack theorem is outside this verdict:
only its22-form97-edge instance is independently reconstructed.

[PROVENANCE.json](PROVENANCE.json) records scoped premises, source hashes
and separate researcher replays. [SHA256SUMS](SHA256SUMS) hashes all
other seven-file-package contents except the manifest itself.
No large census, external corpus, solver or formalization is required.
