# Exact consumer contract for the R2/R3/R8 spine

The favorable gap is `H(u)=integral(g-C_s u)_+-integral(f-C_s u)_+`.
Keep the variance normalization: `d=E distance_loss/s` and
`Q=E distance_loss^2/s^2`. Do not confuse Q with d squared.

For each exact finite input, or uniformly over a certified parameter cell:

1. Verify a common nonnegative prior and the labelled contraction.
2. Prove `|X-E X|^2<=s/4` for every positive-mass site, and
   `Cov(X)/s-2^-15 I` positive semidefinite. All seven principal minors
   give an exact three-dimensional PSD test, including boundary cases.
3. Compute d and Q exactly. If d=0, declare the hinge curve zero by rigidity.
   Otherwise test the polynomial inequality `Q<=2^-48 d`, without dividing
   by an approximate d.
4. If it passes, `H(u)>=2^-40 d` simultaneously on `[1/64,1/2]`, and
   `H(u)>=0` on `[1/64,infinity)`. No threshold samples or grid are needed.
   If it fails, return **UNRESOLVED**. The interval below 1/64 needs an
   actual signed endpoint or another proof with checked overlap.

For a rational finite input, all these guard operations are rational.
Pairwise evaluation costs O(n^2); after the contraction has been established,
d and Q can instead be obtained from a constant-size moment table in O(n)
arithmetic operations. Formula (11) in PROOF.md computes Q using centered
marginal fourth moments, nine cross second moments, and one cross quartic.
It can have cancellation: use exact arithmetic or justified outward bounds.
This is an arithmetic-operation statement, not a bound on rational bit sizes.

For a parameterized input, the guard is polynomial after positive denominators
are cleared. A Bernstein, interval, or exact algebraic certificate must cover
the whole parameter region; checking rational sample points is insufficient.
The eight-site family in PROOF.md supplies such a uniform proof directly:
`0<t<=2^-40`, `alpha<=2^-65 t`, arbitrary priors (14). Its middle margin
vanishes with d, but its proof and parameter budget do not deteriorate.

To preserve this guard when using paired cubature, add exactly
`(X_i-E X_i)(Y_j-E Y_j)/s` for all nine i,j and
`|X-E X|^2 |Y-E Y|^2/s^2` to the existing separate marginal moment list.
For q>=2 the atom budget becomes

```
2 binom(2q+3,3)-1+10.
```

The degree budget, beta error, and R8 full-curve loss modulus are unchanged.
At q=2, 79 original pairs retain the guard exactly; the new sign theorem
applies both to the original law and to its sparse law. For general inputs
outside the guard, approximation alone supplies no sign. We do not append
ordinary rational rounding, which can destroy the loss-relative inequality.

The ten features use that input's means. If the feature list must be fixed
before specifying the prior, use the nine raw cross seconds, the raw cross
quartic, and six raw mixed cubics `X_i|Y|^2,Y_i|X|^2`. The corresponding
prior-independent list costs only `M_q+16` pairs (85 at q=2). Formula (11a)
includes the nonzero-mean correction. A single cubature rule valid for every
point of a parameter cell is not claimed.

This consumes accepted analytic estimates and gives a new exact exclusion
test. It neither duplicates R2's deep-flap replay nor delegates work to R2
or R8. The unrestricted conjecture and global defect bound remain unchanged.
