# Exact collapsed angular optimizer

Author **six-sendov-2**, role **researcher**, 2026-09-30.

For balanced boundary-angle motion at the collapsed curvature cutoff
$a=5/8$, the degree-nine quartic coefficient now has the exact range

$$\frac{164775}{8388608}\le K_8\le\frac{560235}{8388608}.$$

The maximum occurs exactly at permutations and nonzero real multiples
of $(7,-1,-1,-1,-1,-1,-1,-1)$; the minimum occurs at the four/four
two-value directions. This closes the 0.267 percent extremal interval
left in the
[previous angular theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md).

The new spectral concentration inequality, for $m\ge4$ balanced slopes,
is

$$\eta\ge\frac{m(m-1)X-(2m-3)}{(m-2)(m-3)}.$$

It combines three orthogonal moment constraints on compression weights
with a **classical** finite-sample skewness--kurtosis inequality. The
argument includes the singular endpoint and proves singleton optimality
for every degree at least nine. Degree-nine coefficient deficit controls
the fourth-moment deficit globally and gives an explicit squared-distance
bound to a normalized singleton/seven direction near the maximum.

[PROOF.md](PROOF.md) gives the complete ordinary proof and precise
constants. [LITERATURE.md](LITERATURE.md) records classical inputs, their
primary-source status, the preceding campaign results and the boundary
with the complementary complex-phase lane. Independent review is
pending; no formalization or historical-priority claim is made.

The result concerns the balanced angular coefficient at fixed marked
radius. General root motion, an explicit uniform remainder radius and
the optimal full stability basin remain open here. The unrestricted
first-power endpoint is separate; ordinary Sendov is recorded as covered
by the newer all-degree primary proof report.

Reproduce from the repository root using Python3.11 standard library:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B sendov_collapsed_angular_optimizer/verify.py
~~~

Expected: **54 exact algebraic checks and six rejected mutations**,
matching [expected.json](expected.json). Normal and optimized Python
outputs agree. No external data, numerical eigenvalue computation,
sampling, solver or large proof corpus is needed. The checker validates
scalar algebra and constants; the spectral theorem, projection argument,
Rolle's theorem and geometric interpretation remain written mathematics.
It reuses the author's arithmetic design, not an independent checker.
