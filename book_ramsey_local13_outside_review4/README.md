# Independent local13 Book Ramsey review

Actual agent **six-reviewer-4**, role **independent mathematical reviewer**.

[REVIEW.md](REVIEW.md) confirms theorem8170: a thirteen-edge neighborhood in
an admissible ten-regular22-vertex host forces outside red degrees5,5,4^9.
The conditional lemma assumes local degrees2^4,3^6. The thirteen-edge and
110-edge corollaries reuse the explicitly credited prerequisite reviews.

The reviewer replaces the three/four-low selected-row branches by universal
real-slack forms -32/-112. Only the39all-cubic configurations need a finite
census: all40111matrices have checked strict negative forms from184primitive
zero-sum vectors. The original vectors and the four-low pattern are credited
to six-books-3. The reviewer imports no author code or expected-domain list.
The later8218two-five-row theorem remains outside this verdict.

From repository root, CPython3.11+ standard library, sequential commands:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B book_ramsey_local13_outside_review4/audit.py \
  --vectors book_ramsey_local13_outside_review4/vectors.json \
  --check book_ramsey_local13_outside_review4/expected.json
python3 -B book_ramsey_local13_outside_review4/bridge.py \
  --check book_ramsey_local13_outside_review4/bridge_expected.json
~~~

Add Python -O for optimized replay. Optional passive state/entry comparison:

~~~sh
--compare-author book_ramsey_b4_b7_regular110_local13_outside_degrees/expected.json
~~~

To reconstruct pruning, use the original author negative_vectors.json as the
vector input and add --export-used /tmp/local13-zero-sum-vectors.generated.json;
compare exported bytes to vectors.json. This option never selects the domain.

PROVENANCE.json records scope, exact input hashes and credit. VALIDATION.json
records complete runs and rejection of a forged positive pool. SHA256SUMS
covers all other compact text files. expected.json is complete compact stdout;
no generated matrix or core corpus is required or published.
