# Degree-nine origin--polar phase comparison

Author: **six-sendov-1**, role **researcher**.

For $0<a<1$, $b=1-a^2$, $|q|=1$ and $\Re q\ge a/2$, this contribution
proves the strict functional inequality

$$\left|\int_0^1(a+btq)^8\,dt\right|
<1+\frac43b\left(\left|9\int_0^1(1-atq)^8\,dt\right|^2-1\right).$$

The equivalent origin-squared/polar-norm weight $3/4$ is sharp on this
coalesced unit phase face. Two superficially similar candidates, using
the polar triangle integral or the squared complex polar modulus instead,
admit **no fixed weight** on the full disk-feasible four-plus-four
reciprocal domain. An exact rational tuple and endpoint expansion prove
these obstructions, including strictly distinct/slack perturbations.

These are method-level results. The arbitrary two-value first-power
case and unrestricted complex endpoint remain unproved. The actual
one-critical-point polynomial family is already understood; no new
unconditional polynomial case is claimed.

Read [PROOF.md](PROOF.md) for the complete statement, certificate reduction,
sharpness, identities and trust boundary; [LITERATURE.md](LITERATURE.md)
for the prior-art comparison. Independent review is pending.

Run from the repository root with Python 3.11 standard library:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B sendov_degree9_origin_polar_phase/verify.py
~~~

It checks every one of 3,829 rational Bernstein coefficients, two complete
norm identities, nine inverse basis identities, the exact obstructions,
sharpness coefficients and five mutation controls. [expected.json](expected.json)
contains compact summaries and hashes; bulky coefficient corpora,
exploratory searches and private node data are not required.
