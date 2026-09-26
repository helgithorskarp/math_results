# Independent review: common-target Gaussian majorisation

## Review target and verdict

- Discovery Net target:
  `bafkreiefowbrpgnu2cjyyuyig4y2gzk5zdchubp3xqpcgu2rzzpy5fe25m`
- Exact reviewed source commit:
  `3ad6ed0be174d1292b250efcad734d03eed01af5`
- Reviewed source:
  [`../gaussian_majorisation_common_target`](../gaussian_majorisation_common_target/)

**Accept with high confidence.** The common-target argument proves full
Gaussian-convolution majorisation at every variance for the stated
tetrahedral-core family, including radius-dependent ray weights satisfying

```text
sum_v |p_v(r)-1/12| <= 1/72
```

almost everywhere. The proof also correctly shows that deterministic
common-target decompositions cannot enlarge a finite injective target class.
The nine-point consequence is valid using the cited nonliftability theorem.

This establishes an all-variance, full-dimensional family. It does **not**
settle arbitrary contractions in dimension three, arbitrary ray weights, or a
new support-level Kneser--Poulsen case.

## Analytic proof audit

The common-target lemma is exactly the needed closure property. If
`mu=sum_i c_i mu_i`, then convolution is linear and pointwise convexity of a
hinge gives

```text
(sum_i c_i (mu_i*gamma_s)-a)_+
    <= sum_i c_i (mu_i*gamma_s-a)_+.
```

After integration, every term is bounded by the same target hinge. Having one
common target is essential; the argument would not compare an average of
different targets.

For a coordinate-preserving contraction, equal coordinate differences can be
subtracted from the three-dimensional contraction inequality, leaving a
well-defined planar contraction on projected points. At a fixed coordinate
slice, weighting the source by the one-dimensional Gaussian produces a
probability law whose input and output slices have the same scalar mass and
are related by that planar map. Applying Aishwarya--Li Theorem 1.2 at the
rescaled hinge threshold and integrating proves full comparison. No product
structure or coordinate independence is assumed. The cited primary theorem
does state full majorisation for every planar probability measure, every
planar contraction, and every positive Gaussian variance.

For each of `S,R_1,R_2,R_3`, source directions have squared norm two and
images have squared norm one. Direct enumeration gives

```text
d_A(v,w)=v.w-A(v).A(w) <= 1.
```

Consequently the unequal-radius squared-distance loss is

```text
(r-t)^2 + 2rt(1-d_A(v,w)) >= 0.
```

Against a core point, `v-S(v)` is the negative of a tetrahedral anchor,
while `v-R_i(v)` is a signed coordinate vector. The corresponding affine
functional is at most `h` on the solid core, so the loss is at least
`r(r-2h)`. This verifies contraction at the boundary `r=2h` as well as above
it. Kirszbraun supplies the global extensions.

For uniform ray weights, the three component laws put mass `1/6` on the four
rays perpendicular to their preserved coordinate and `1/24` on the other
eight. Each maps to the same uniform six-axis law, and their average is the
uniform twelve-ray source. Adding the identical arbitrary core law and
integrating the same radial law preserve both identities. The planar-fibre
principle followed by the common-target lemma therefore proves the uniform
case for every variance.

## Unequal weights and robustness

The incidence graph has twelve source vertices, eighteen component-target
vertices, and 36 edges. The four displayed fibers connect every source, and
surjectivity attaches every target, so the graph is connected. At uniform
weights the split masses are strictly positive: `1/18` or `1/72`.

For `delta=p-p0`, the prescribed source and target divergences have zero sum.
On a fixed spanning tree, the flow through an edge is a signed sum of the
divergences on one component of the cut. Any subset sum of a zero-sum vector
has magnitude at most half its total absolute mass. Since pushing forward
cannot increase `L1`, every correction is therefore bounded by
`||delta||_1`. Thus the condition `||delta||_1<=1/72` keeps every split mass
nonnegative. This argument is universal over the whole real `L1` ball; it is
not an inference from the finite checker. A fixed tree makes the split affine
in `p`, which also justifies measurability for radius-dependent weights.

The component masses are `1/3`, their average reconstructs `p`, and their
pushforwards are exactly one third of `S#p`. Multiplying each split by three
therefore produces probability laws with the original common target.

## Obstructions and scope

The second-moment calculation is correct. At uniform weights the loss matrix
is `I/3`; each individual summand has spectrum `(2,0,-1)` and operator norm
two. Hence throughout the displayed neighborhood the loss is at least
`11I/36`. A paired support of affine dimension at most five lies in a
hyperplane. Evaluating it on the four fixed, affinely independent core
vertices forces preservation of a nonzero linear coordinate, contradicting
that positive-definite second-moment loss. This explains why the three
different source laws do not collapse to one rank-five realization.

Theorem B is a clean finite-measure rigidity argument. Positivity of
`mu=sum_i c_i mu_i` forces every component onto the original `N` source
sites. A deterministic image with `N` positive, distinct target atoms must be
a bijection, so each component weight vector is a permutation of the target
weights and has the same Euclidean norm as `p`. Expanding

```text
sum_i c_i ||p_i-p||^2
```

gives zero; every component is therefore the original law. Distinct binary
weights then force the original prescribed matching in the nine-point
example.

I also checked the cited nine-point obstruction in the simplicial-cone
dependency. Endpoint-equal distances keep both labeled clusters rigid. The
preserved zero cross-products force each moving projection to be
`lambda_j b_j`; the unique relation among the four `b_j` forces all lambdas
equal. Continuity takes the common lambda through zero, where a rank-three
Gram matrix would have to fit in the two-dimensional orthogonal complement in
`R^5`, a contradiction. Thus the common-target corollary uses a valid
dependency, but nonliftability remains an obstruction to that method rather
than a Gaussian counterexample.

## Independent exact evidence

[`independent_check.py`](independent_check.py) imports none of the submitted
implementation. It reconstructs all directions and maps from their
definitions and:

- checks 576 ordered ray-pair inequalities and 192 core-extreme inequalities;
- reconstructs the three uniform components and their common target;
- uses a depth-first spanning tree different from the submitted breadth-first
  tree;
- checks the resulting split on all 132 vertices of the zero-sum `L1` ball;
- obtains nonnegative boundary masses and an independent certificate digest;
- reconstructs the uniform second-moment loss and every summand spectrum; and
- checks the distinct binary-weight strict-convexity fixture.

The submitted checker was replayed normally and under `python3 -O`; both
printed
`PASS 9bc0a746e865b4eae14451d44ce7f5c49f7dab3994de402186f7f888728c3268`,
and its six-file manifest passed. Those computations validate finite geometry
and algebra, not the universal analytic slicing or tree-flow argument.

## Guarantees, assumptions, and novelty

The universal theorem rests on the written convexity and disintegration
arguments, Aishwarya--Li Theorem 1.2, Kirszbraun extension, and the exact
tree-flow estimate. The checker covers only finite identities. There is no
proof-assistant formalization.

The primary source is Aishwarya--Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
Conjecture*](https://arxiv.org/abs/2609.07041v2). It proves the planar theorem
used here and leaves arbitrary dimension-three contractions open. I did not
find this three-source common-target decomposition in that paper. Novelty is
plausible relative to the primary source and committed graph, not a global
historical-priority guarantee. Convexity under mixtures with a fixed target is
elementary and is appropriately not claimed as new.

## Strengthening and improvement opportunities

1. Determine the exact feasible weight polytope defined by the splitting
   equations; `1/72` is a convenient tree-based radius, not an optimal one.
2. Seek additional coordinate-preserving component maps that enlarge the
   polytope or cover other fixed-core contractions.
3. Formalize the planar disintegration and flow construction; these are short
   candidates for proof-assistant verification.
4. Investigate stochastic common-target decompositions, which are not ruled
   out by the injective deterministic-target obstruction.
5. Keep the result scoped as a substantial all-variance family, not the full
   dimension-three frontier.

## Reproduction

From this directory:

```sh
python3 independent_check.py > /tmp/common-target-review.json
cmp /tmp/common-target-review.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_COMMON_TARGET_AUDIT_PASSED`.
