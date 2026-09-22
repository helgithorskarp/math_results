# Gaussian contraction entropy: equality and quantitative rigidity

This package supplies an author proof of the equality cases in Gaussian
Rényi entropy contraction, together with explicit stability estimates.
It is independently unreviewed and not proof-assistant formalized.

Let $T:\mathbb R^n\to\mathbb R^n$ be 1-Lipschitz, let $Z$ be an
independent standard Gaussian, and let $s>0$. For every positive Rényi
order, including Shannon and infinity, equality in

$$
h_\alpha(X+\sqrt{s}Z)\ge h_\alpha(T(X)+\sqrt{s}Z)
$$

with finite input entropy holds exactly when $T$ agrees on the support of
$X$ with an ambient rigid motion. No moment assumption is needed.

If $X$ lies in a radius-$R$ ball and
$\operatorname{Cov}(X)\succeq\kappa I_n$, its entropy loss $G_\alpha$
controls the optimal rigid-motion error:

$$
\inf_{Q\in O(n),b}\mathbb E|T(X)-QX-b|^2
\le \frac{2R^2}{\kappa c_\alpha}G_\alpha .
$$

[PROOF.md](PROOF.md) gives an explicit positive $c_\alpha$ for every
order, proves that the corresponding root mean square exponent $1/2$ is
optimal, and proves the sharp posterior-weighted bound
$G_\infty\ge \mathbb E_{\nu_z\otimes\nu_z}\Delta/(4s)$.
Here $\nu_z$ is the input posterior at a mode of the input Gaussian
mixture and $\Delta$ is the pairwise squared-distance decrease.
The general compact-support constants are not claimed optimal.

The qualitative entropy comparison, including removal of the moment
condition, is already known from Aishwarya--Li. Their September 2026
preprint was checked before publication of this package. The proposed
new content is the equality/stability analysis, not a new proof of an
open qualitative comparison. Targeted primary-source searches found no
matching quantitative theorem; priority is not established by that search.
See [SOURCES.md](SOURCES.md).

## Reproduce the finite checks

Tested with CPython 3.11.2; standard library only. From this directory:

~~~sh
python3 verify.py > actual.json
cmp actual.json EXPECTED.json
python3 -O verify.py > actual-optimized.json
cmp actual-optimized.json EXPECTED.json
sha256sum -c SHA256SUMS
~~~

Successful runs exit zero and print status FINITE_RATIONAL_CHECKS_PASS.
Failures raise exceptions that remain enabled under Python optimization.

The verifier checks 215 rational path-pair identities; centered Gram and
alignment bounds on four fixtures; 12 Gaussian entropy comparisons at
orders 2, 3, 4; four sharpness-family parameters; three exact
maximum-density sharpness examples; and rejection of four invalid
fixtures plus two invalid logarithm arguments. See
[NUMERICS.md](NUMERICS.md) for the enclosure contract.

The analytic proof covers arbitrary laws and all real positive orders.
Finite checks corroborate formulas and constants; they do not establish
that universal theorem or constitute independent peer review. No external
data, solver, floating-point inference, downloaded paper, or large
certificate is needed.

The original geometric Kneser--Poulsen conjecture and general Gaussian
majorization in dimensions above two are outside this result.
