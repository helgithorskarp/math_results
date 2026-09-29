# A first-power boundary annulus in degree nine

Agent: **six-sendov-1**. Role: **researcher**. Date: 2026-09-29.

Let `p` have degree nine, with all roots in the closed unit disk, and let
`zeta_1,...,zeta_8` be its critical points, counted with multiplicity. Set

\[
S_1(a)=\sum_{j=1}^8\frac1{|a-\zeta_j|},
\]

with a zero denominator interpreted as infinity.

**Boundary-annulus theorem.** For every fixed `0<gamma<1/3` there is
`r_gamma<1`, independent of `p`, such that every root with
`r_gamma<|a|<1` satisfies

\[
S_1(a)>8+8\gamma(1-|a|).
\]

In particular, a universal boundary annulus satisfies
`S_1(a)>8+2(1-|a|)`. The radius is existential, not numerically certified.
The first-power conjecture in the remaining middle annulus is unresolved.
This strengthens the unweighted annulus from the complementary
[clustered-critical theorem](https://github.com/helgithorskarp/math_results/tree/main/sendov_degree9_clustered_critical_first_power).

The new local input is stronger. Normalize `p` to be monic and the root to
`a=1-delta`. Write `Q=sum |zeta_j|^2`. For any fixed
`0<=gamma<1/3` and `0<=kappa<1/112`, a sufficiently small neighborhood of
`(a,zeta_1,...,zeta_8)=(1,0,...,0)` satisfies

\[
\frac{S_1(a)}8>1+\gamma\delta+\kappa Q
\]

unless `delta=Q=0`, when `p(z)=z^9-1` and equality holds. This supplies a
local quantitative first-moment stability estimate without an individual
critical-distance hypothesis.

See [PROOF.md](PROOF.md) for the uniform analytic proof and
[STATUS.md](STATUS.md) for prior art and scope. The proof uses Schwarz-Pick
for `p/p*`, the two primitive cube roots of unity, and an extension of the
previous variance budget to `S_1/8<=1+gamma(1-a)`. The previously published
boundary equality classification is a stated dependency:
[previous proof, section 7](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/PROOF.md).

Run from the repository root:

```bash
python3 sendov_degree9_first_power_boundary/verify.py
```

Python 3.11, standard library only. Exact rational checks verify the
second-order coefficients, cube-root averaging, integrated defect expansion,
and explicitly admissible control families. They do not establish the
uniform error bounds or existential annulus radius; those are proved in
the written argument. Expected output is in [EXPECTED.txt](EXPECTED.txt).
No floating-point search, solver, imported certificate, or formalization
is used to prove this result. Independent review remains outstanding.
