# A rigorous boundary for signed-radial counterexample searches

If a bounded radius A is independent of a unit direction U and h is an odd
scalar contraction, then the difference of two independent copies of h(A)U
is dominated in multivariate convex order by the corresponding difference
of AU. A four-point doubly stochastic certificate proves this directly.

Consequently **every spherical log-MGF tail test is nonnegative**, even when
h reverses radial signs and the angular law is asymmetric. An exact seven-site
paired-rank-six instance has a strictly positive all-temperature margin.

This excludes the spherical-tail counterexample route for the stated whole
class. **It does not prove full Gaussian majorisation for that class**, give
a Kneser--Poulsen theorem, or cover radius--direction dependence.

- [Proof, quantitative margin and scope](PROOF.md)
- [Exact checker](verify.py) and [expected record](EXPECTED.json)
- [Sources and relation to existing team work](SOURCES.md)

From this directory with standard-library Python 3.11 or later:

```sh
python3 -B verify.py --check
python3 -B -O verify.py --check
sha256sum -c SHA256SUMS
```

Expected status: `SIGNED_RADIAL_TAIL_EXCLUSION_EXACT_PASS`.
Complete author argument; independent mathematical review is pending.
