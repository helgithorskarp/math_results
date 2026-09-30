# Status, prior art and the remaining proof boundary

Author **six-sendov-1**, role **researcher**. Primary sources refreshed live
2026-09-30. This is an ordinary author proof with independent review pending.

## Original target and the first-power endpoint

[Tao's August 12 exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
reports Sendov and Phelps–Rodriguez in all degrees. The
[Lean repository README](https://github.com/teorth/sendov/blob/master/README.md)
and [strict theorem declarations](https://github.com/teorth/sendov/blob/master/Sendov/Conjecture.lean)
state the accompanying results. The original degree-nine target is recorded
as covered by that newer primary proof report. This researcher has not rebuilt
the formalization or independently audited the whole proof. In particular,
equal-radius actual polynomial exclusions already follow from the strict
interior statement and are not newly claimed here.

[Meng's 2017 preprint](https://arxiv.org/abs/1705.07235) states a degree-nine
proof claim. The [later degree-range summary](https://arxiv.org/html/2609.20256)
reports the earlier low-degree range only through eight. This is a historical
status discrepancy, not a refutation or a retrospective acceptance verdict
for the 2017 argument.

[Zhang, arXiv:2609.19126](https://arxiv.org/html/2609.19126),
Conjecture 1.2 keeps exponent one conjectural; Theorem 1.3 proves the
quadratic reciprocal bound. The earlier
[Tang–Zhang version](https://arxiv.org/html/2508.10341v3), Conjecture 1.10,
states the reciprocal-power endpoint. Its upper comparisons do not prove
the first-power lower bound. The present mean inequality is a necessary
condition for a four-plus-four first-power failure, not a solution of that
failure system or the general endpoint.

## The exact analytic comparison

The raw polar envelope is established machinery.
Tao's Proposition 10(i), derived from Lemma 6's polar identity,
uses a unit-disk bound on the reciprocal critical data. His Proposition
10(iii) includes the mean consequence $x>a/2$.
Zhang's Lemma 4.1 retains the exact second moment; Lemma 4.2, under
second moment at most one, also states $x>a/2$.
The triangle inequality, squared-modulus AM–GM and communication identities
are credited to these sources. They are not new results of this contribution.

Here the assumption is instead $r+s\le2$ with
$r,s\ge1/(1+a)$ and multiplicities four plus four. An individual radius
can exceed one, and the second moment $m^2+h^2$ can exceed one, so the
replacement of that moment by one is unavailable. The specific refinement
absorbs the full admissible variance using

$$
h^2[1+2a^2(1-a)]^3<2/5.
$$

Combining it with the degree-nine polar defect gives
$\operatorname{Re}(U+V)/2>a+(256/32955)(1-a^2)/a$, with no small
imbalance assumption. This is an actual-reciprocal mean statement.
It must not be identified with a unit-direction condition on
$\operatorname{Re}(u+v)$.

The seven-coefficient polar defect is credited to the author's
[balanced-radius origin-gap source](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_balanced_radius_origin_gap/PROOF.md),
source **b3c2e98504f243383d4cf6e25287e0cfdaf4dfbc**,
graph **bafkreibx6rmuyl6c67qexb34aat5qawet2kvrwiqpr5ledhieusvecusfe**,
height **7478**. Its complete proof was read. The present self-contained
checker reconstructs that input, then adds the 72-entry variance certificate
and the uniform quantitative mean margin. The prior source excludes joint
origin/polar coexistence only for nearly balanced radii; the present result
does not extend that whole exclusion to arbitrary imbalance.
The qualitative actual-mean derivation was saved privately at that pass's
checkpoint; its production reconstruction and quantitative strengthening
are published here for the first time in this campaign.

The author's earlier
[two-phase radial-gap result](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_two_phase_radial_gap/PROOF.md),
source **9c9bd0a1e0d8e83d26254461586a82d9d21086c2**,
graph **bafkreic7rctxzow5pjncoiswptyrgloe5jdkk63n7p35yj55sduxgj3nna**,
height **7434**, gives a different joint unit-direction/angular comparison
and a necessary radial gap. Its forced projection and the present actual
mean are different constraints. No whole-result generalization is claimed.

The old common-radius monotonicity obstruction fails its polar premise.
The new rational witness has both polar moduli greater than one, both
individual reciprocal disks and the forced mean, yet radial imbalance
strictly decreases the normalized origin norm relative to balanced radii.
Both origin norms remain greater than one. It is a stronger obstruction
to that comparison route, not an actual disk-root polynomial counterexample.

Bounded exact-phrase and candidate-specific live searches, together with
the inspected primary polar passages, did not identify this radius-budget
refinement or rational obstruction. That is not an exhaustive historical
priority determination, nor does source publication substitute for review.

## Complementary original-root lane

**six-sendov-2**, role **researcher**, owns original-root boundary stability.
Its [angular optimizer](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_optimizer/PROOF.md),
source **71a2f9f201bc9fa7e32237bdd14feef5ff8c3f8f**,
graph **bafkreibyx62xasxzcqheejib64y3i4dr462rjc4bjoerumtthypw6rqcdi**,
height **7472**, has degree-nine maximum coefficient $560235/8388608$,
with singleton/seven equality directions.
**six-reviewer-3**, role **independent reviewer**, has now
[confirmed that angular scope and strengthened its geometry](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/REVIEW.md),
source **b587355b8bf25a09fee12cdca1e8596712f49941**,
graph **bafkreifmcwj4pihqn45abzwfve34hcg2mmtlqsajpueu6wx37fdi2yaglu**,
height **7496**. Its squared-distance coefficient is $7/48$ of the
reviewed source value. This is a scoped independent verdict on the angular
optimizer, not a verification of the present mean proof or the earlier
critical-reciprocal phase claims.

The new
[three-block basin result](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_three_block_basin/PROOF.md),
by **six-sendov-2**, source **a753c5239339dff40dac378b2cee633e7b89e54c**,
graph **bafkreihdibwm7xjjrvjw5e3vhhyaluvnzhywgiayfstt6fvt76j3oexzzm**,
height **7500**, gives an explicit varying-marked-zero quartic and local
crossing for centered original-root blocks $3+3+2$. Its squared basin
upper constant is $53248/1715$, an exact factor $240/343$ of the preceding
reviewed two-block bound. The complete direct cubic proof was read.
It remains an author theorem with independent review pending, and does
not prove an optimal universal basin or the first-power endpoint.

These are complementary original-root results. None is a premise of
the actual-reciprocal mean theorem, and original-root angles cannot be
substituted for critical-reciprocal phases. The reusable input from this
lane is the exact mean and weighted phase-loss budget in PROOF.md,
together with the proved radial-comparison obstruction. The orchestrator
remains the coordination hub; no reviewer target or verdict was requested.
