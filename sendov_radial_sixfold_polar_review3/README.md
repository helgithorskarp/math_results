# Radial-sixfold audit and stronger complex polar mean gap

**six-reviewer-3**, independent mathematical reviewer, confirms the
degree-nine first-power theorem for a critical point of multiplicity
at least six on the line through the marked root and origin, and the
separate full complex6+1+1 polar deficit lemma in claim8148.

The [complete audit and proof](REVIEW.md) also establishes
\[
|C_a|\ge1\quad\Longrightarrow\quad
\xi-a\ge\frac{1-a}{9a(1+a)J(a)}
          \ge\frac{1-a}{45a(1+a)},
\]
where J is an explicit integrated derivative polynomial. This improves
the original uniform1/128 coefficient by128/45. It does not remove
the radial hypothesis from the polynomial first-power theorem or prove
the unrestricted endpoint. Coincidences and infinite reciprocals are
handled explicitly; no real-coefficient assumption is imposed.

Run from repository root, CPython3.11+ standard library (tested3.11.2):

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B -O sendov_radial_sixfold_polar_review3/verify.py \
  --check sendov_radial_sixfold_polar_review3/RESULTS.json
~~~

The final output line is:

~~~json
{"agent": "six-reviewer-3", "complete_signs": 122115, "result_sha256": "c91e45b78855cc672f2ad91cc51e127ad1b4ed4eea67b6598c2ffcb4efa17e0a", "uniform_mean_gap_gamma": "1/45", "verified": true}
~~~

The [checker](verify.py) uses direct cleared cube moments, an alternate
discriminant, common-denominator integer polynomials and Pascal
addition/subtraction transforms, importing no author code. It regenerates
every sign and full inverse, all equality supports, the675-entry polar
quotient and208 coefficients for the uniform derivative bound.
[RESULTS.json](RESULTS.json) records exact certificates, minima and hashes.

Independent normal9.840s and optimized10.233s runs agreed, with child-RSS
upper bounds75,232/77,772KiB, including optional original comparison.
All122,115 original sign entries and both complete cleared power
polynomials were literally compared after independent construction.
The8.33MB comparison regeneration stays private and is unnecessary
for the command above.

For optional compact original comparison, export the original fixture
from an existing clone to scratch and supply its path:

~~~sh
git show 4c04ae6fa05920f3f749ffec6ecb1f8aa3ad219a:sendov_degree9_radial_sixfold_critical_first_power/expected.json \
  > /tmp/radial611-original-review3.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -B -O sendov_radial_sixfold_polar_review3/verify.py \
  --check sendov_radial_sixfold_polar_review3/RESULTS.json \
  --original /tmp/radial611-original-review3.json
~~~

Expected optional comparison: complete power/sign tensor digests and
zero inventories agree. That comparison follows all own construction,
sign, physical-path and example checks; the original fixture selects
no domain.

[PROVENANCE.json](PROVENANCE.json) separates independent checks,
researcher replays, literature and ordinary-proof trust boundaries.
[SHA256SUMS](SHA256SUMS) hashes the other six files in the seven-file
package. No generated tensors, external corpus, solver, floating-point
sign input or formalization is required.
