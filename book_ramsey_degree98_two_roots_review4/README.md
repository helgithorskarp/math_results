# Independent 98-edge two-root Book audit

Reviewer: **six-reviewer-4**, independent mathematical reviewer.
Read [REVIEW.md](REVIEW.md) for the theorem, complete host-to-finite-domain
reduction, six-dimensional decomposition and integral lattice proof.
The conditional degree pattern \(8^2,9^{20}\) is excluded; this does not
settle \(R(B_4,B_7)\) or all 98-edge graphs.

CPython 3.11+; standard library only. From the repository root:

~~~bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -B book_ramsey_degree98_two_roots_review4/audit.py \
  --expected book_ramsey_degree98_two_roots_review4/expected.json
python3 -B -O book_ramsey_degree98_two_roots_review4/audit.py \
  --expected book_ramsey_degree98_two_roots_review4/expected.json
python3 -B -O book_ramsey_degree98_two_roots_review4/controls.py \
  > book_ramsey_degree98_two_roots_review4/controls.generated.json
cmp book_ramsey_degree98_two_roots_review4/controls.generated.json \
  book_ramsey_degree98_two_roots_review4/controls_expected.json
python3 -B book_ramsey_degree98_two_roots_review4/bridge.py \
  > book_ramsey_degree98_two_roots_review4/bridge.generated.json
cmp book_ramsey_degree98_two_roots_review4/bridge.generated.json \
  book_ramsey_degree98_two_roots_review4/bridge_expected.json
(cd book_ramsey_degree98_two_roots_review4 && sha256sum -c SHA256SUMS)
~~~

The main audit visits all 19683 ternary interiors, producing 282
margin-two matrices. It verifies 136488 literal invariant-basis entries,
264 nonsquare determinants and 18 integral-trace contradictions.
The full 21-kernel is six-dimensional in 250 cases and seven-dimensional
in 32; all square cases belong to the former.
Complete expected outputs, hashes and validation are included.
Main runtime is approximately one second and memory approximately 21 MiB.

An optional comparison with the original compact certificate happens
only after independently generating the reviewer domain:

~~~bash
python3 -B book_ramsey_degree98_two_roots_review4/audit.py \
  --expected book_ramsey_degree98_two_roots_review4/expected.json \
  --compare-author book_ramsey_4_7_degree_reductions/degree98_two_roots_expected.json
~~~

This is not needed to reproduce the reviewer proof. To reproduce the
credited native author checks and all internal matching placements:

~~~bash
python3 -B -O book_ramsey_4_7_degree_reductions/degree98_two_roots_check.py \
  --matrices /tmp/book-degree98-two-roots-review4.json
python3 -B -O book_ramsey_4_7_degree_reductions/degree98_two_roots_independent.py \
  --matrices /tmp/book-degree98-two-roots-review4.json
~~~

The optional full matrices are generated scratch data and are not published.
All commands run sequentially with one native thread. No solver or
external classification is required for the conditional theorem.
Written mathematics and exact Python computations are unformalized.
The budget-30 premise is explicitly imported for the combined corollary.

The small [baseline21.rows](baseline21.rows) fixture is credited to
Lidicky--McKinley--Pfender--Van Overberghe's companion repository; its
matrix is complemented off-diagonal into red orientation. Its source URL
and exact hashes are in [PROVENANCE.json](PROVENANCE.json).
It validates the known 21-vertex example and is not a new construction.
