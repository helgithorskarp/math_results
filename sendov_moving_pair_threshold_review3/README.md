# Moving-pair angular threshold audit and two proved refinements

Actual reviewer **six-reviewer-3**, independent mathematical reviewer.

[REVIEW.md](REVIEW.md) confirms claim8160's all-balanced angular threshold,
complete equality set, uniform actual-family energy comparison and analytic
equal-value curve, with the stated reviewed local-minimum premises.
The unrestricted first-power endpoint and full fixed-energy global
transition remain outside the verdict.

The audit proves two additional conclusions:

1. For \(a_P=(6\sqrt{101}-29)/52\le a<a_G\), the moving pair
   \((1,-1,0,\ldots,0)\) is the unique angular optimizer, up to nonzero
   scaling and permutation. Here \(a_P\) lies between0.601908 and0.601909,
   and \(a_G=(20\sqrt{1614}-385)/692\). The lower endpoint is sufficient,
   with no optimality claim.
2. The uniform actual comparison coefficient improves from77/10000
   to3/100. More generally every positive coefficient below
   \(C_G=C_P(a_G)-C_Q(a_G)\) works with a common sufficiently small energy
   threshold; \(C_G\) is the supremum of such coefficients. Attainment at
   that supremum is not claimed.

From repository root, Python3.11+ standard library (tested3.11.2):

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -I -B -O sendov_moving_pair_threshold_review3/verify.py \
  --check sendov_moving_pair_threshold_review3/RESULTS.json
~~~

Expected final JSON:

~~~json
{"agent": "six-reviewer-3", "verified": true, "identities": 62, "strict_signs": 18, "result_sha256": "1b9d02f285f6ada0f0b7c3709f1802c0a22c62e96d0d4a7132e3ea45937fae88", "new_pair_interval": "[aP,aG)"}
~~~

The [checker](verify.py) uses a unified sparse four-index rational ring,
direct differentiation of all nine original factors, geometric/binomial
series, simultaneous Newton doubling and an arbitrary symbolic common
mean. It imports no author program. [RESULTS.json](RESULTS.json) records
complete symbolic coefficients, exact field signs, an8x8 operator control
and five rejected invalid arithmetic inputs.

Optional entry-level comparison is performed only after independent
construction and checks. From an existing repository clone:

~~~sh
git show 5741f9d5651644598d0d685599b9e95b79d5d069:sendov_degree9_moving_pair_comparison_boundary/expected.json \
  > /tmp/moving-pair-original-review3.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -I -B -O sendov_moving_pair_threshold_review3/verify.py \
  --check sendov_moving_pair_threshold_review3/RESULTS.json \
  --original /tmp/moving-pair-original-review3.json
~~~

This compares all57 mathematical records of the original59-record
fixture literally; the two original textual variable-binding labels are
excluded. The fixture neither selects the domain nor supplies proof input.

Independent normal0.327s/O0.521s and original normal0.897s/O1.016s
all completed. Peak child-RSS upper bounds were below25MiB. Numeric/native
threads are one and all mathematical jobs run sequentially under the
unchanged1CPU2GiB scope.

[PROVENANCE.json](PROVENANCE.json) pins source, prior reviewed inputs,
resources and trust boundaries. [SHA256SUMS](SHA256SUMS) hashes the six
other files in this seven-file package. Universal moment/Gram inputs,
real-rooted lifting, collision uniformity, analytic implicit functions
and compactness remain ordinary written mathematics, outside a formal
proof kernel. No solver, floating proof input, external corpus or
effective energy cutoff is required or claimed.
