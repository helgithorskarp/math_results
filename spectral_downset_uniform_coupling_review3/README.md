# Stable-uniform H: independent audit and coupling refinement

**six-reviewer-3**, independent mathematical reviewer, confirms committed
claim8064 for every integer \(r\ge2,\ n\ge2r\). The complete ordinary
unformalized [review](REVIEW.md) proves that the same matrix formula
works throughout
\[
0<t\le\min\{1/(2B),\alpha g/(4B^2)\},
\]
where \(B\) is the exact maximum absolute row sum of its perturbation,
\(g\) is an explicit rational lower bound for the positive baseline gap,
and \(\alpha=r/\binom{n-2}{r-1}\). The interval is at least \(4N\)
times the original \(1/(8N^6)\), with exact maximal lower-slack rank
\(N-n\) and precisely the star kernel. This formula still fails the
additional upper cap. General H/I remain open.

The review includes all-order harmonic completeness, every top odd
boundary kernel at \(n=2r\), the full Schur coupling argument, the
empty-row lift, universal rank bound and explicit full upper-cap witness.
Classical EKR and harmonic machinery are credited, without priority claims.

Run from repository root, CPython3.11+ standard library (tested3.11.2):

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B -O spectral_downset_uniform_coupling_review3/verify.py \
  --check spectral_downset_uniform_coupling_review3/RESULTS.json
~~~

The [independent checker](verify.py) uses signed difference products
instead of the author's lowering-nullspace harmonics. It checks27
parameter pairs and five complete literal matrices at four couplings:
32,219 Gram entries,1,164 complete basis actions,24 dense PSD/rank
forms, six literal gap forms and nine rejected controls. It imports
no author code or data. Exact counts, safe intervals and ranks are in
[RESULTS.json](RESULTS.json); trust boundaries and original replay
are distinguished in the review and [PROVENANCE.json](PROVENANCE.json).

Expected compact output:

~~~json
{"agent": "six-reviewer-3", "basis_sizes": [10, 15, 41, 63, 162], "compressed_cases": 27, "literal_cases": 5, "negative_controls": 9, "summary_sha256": "a721f440598601d00141254f15146e795b5adf96c0f52a507dc3595306fa64ba", "verified": true}
~~~

Normal and optimized runs agree; measured optimized replay9.364s
and peak child-RSS upper bound28,036KiB. These finite checks support
the written proof, rather than proving universal scope by sampling.
All proof/code/evidence files are hashed in [SHA256SUMS](SHA256SUMS).
