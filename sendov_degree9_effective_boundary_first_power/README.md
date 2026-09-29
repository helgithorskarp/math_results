# Effective first-power boundary stability in degree nine

Agent: **six-sendov-2**. Role: researcher. Date: 2026-09-29.

Let `p` have degree nine and all roots in the closed unit disk. For every
root `a` with

\[
1-10^{-18}\le |a|<1,
\]

its critical points, counted with multiplicity, satisfy the strict bound

\[
\sum_{j=1}^8|a-\zeta_j|^{-1}
   >8+\frac{1-|a|}{20}.
\]

A zero denominator means infinity. The numerical annulus is explicit;
its width and slope are conservative constants, not claimed optimal.

The new structural input is quantitative. Normalize `a` real and put
`eta=1-a`. If `0<eta<=10^-6` and the sum is at most `8+eta/20`, then

\[
\sum_j|\zeta_j|^2\le1.6\times10^9\eta.
\]

An approximate elementary-symmetric identity, Newton's inequality, and
a finite polar variance bound force concentration toward the binomial
equality family and exclude the collapsed equality family. This replaces
the previously qualitative compactness step with an explicit estimate.
The estimate feeds a slight strengthening of the published clustered
critical-point theorem to obtain the explicit annulus.

[PROOF.md](PROOF.md) gives the complete argument and every error constant.
[LITERATURE.md](LITERATURE.md) distinguishes the stronger first-power
endpoint from the known Sendov and quadratic assertions and cites the
complementary analytic results. The full degree-nine first-power conjecture
in the middle range remains unresolved here.

Run from the repository root:

```sh
python3 sendov_degree9_effective_boundary_first_power/verify.py
```

Python 3.11, standard library only. The checker verifies the exact Newton
sum-of-squares identity, shifted symmetric identities, all rational
constants, and controls. It rejects a corrupted symbolic identity.
It does not replace the written universal proof. No independent specialist
review or formalization of this new result is claimed.
