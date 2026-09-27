# Independent acceptance: endpoint-block classification and three-mover signs

27 September 2026. Second-reviewer report on Discovery Net contribution
`bafkreiflr2ixigpozmgycnoix7k5knbijnmazeu2osk52mdzaxhml2gqti`, source
commit [`ca59f324d587ecdc878318b5c99c673c1f395d0b`](https://github.com/helgithorskarp/math_results/tree/ca59f324d587ecdc878318b5c99c673c1f395d0b/probability/gaussian_endpoint_block_classification),
source tree `c69f77d1e7746aee2194cead5c326d0a1695dbb0`.

## Verdict

**Accept, with the dependency and scope boundaries stated by the author.**
The three-mover theorem, exact endpoint-switch classification, normalized
one-component extraction, and rooted eight-label frontier consequence follow
from the written argument. The supplied rational certificate reproduces. A
clean-room checker using different graph and linear-algebra implementations
also reproduces the material finite claims.

This accepts a positive finite-geometric reduction. It does **not** accept the
full dimension-three Gaussian-majorisation conjecture, prove positivity of a
rank-three anchor-inconsistent component, produce a Gaussian counterexample,
or establish historical novelty.

## Mathematical audit

### Three movers

For a moved label set put

`v_i=q_i-p_i`, `b_i=(|q_i|^2-|p_i|^2)/2`.

If the displacement rank is at most two, the classical leapfrog needs at most
two auxiliary coordinates. If three or fewer labels move and the rank is
three, the square system `v_i.c=b_i` has a solution. The latter identity is
exactly `|p_i-c|=|q_i-c|`; every unchanged point satisfies it trivially.
These cases are exhaustive. Thus the two cited analytic primitives really do
sign every three-mover contraction against an arbitrary fixed background.
No inverse-matrix bound, weight floor, or variance limit is used.

The external scope was checked against the primary statements. Aishwarya--Li
[Theorems 1.4--1.5 and the two-coordinate observation](https://arxiv.org/html/2609.07041v2)
give convex-energy comparison when a contraction lifts using two auxiliary
dimensions. Bezdek--Connelly [Theorem 1 and Corollary 3](https://pi.math.cornell.edu/~connelly/pdf/10.1515_crll.2002.101.pdf)
give both arbitrary-individual-radius ball comparisons under the same
two-dimensional displacement condition. The common-anchor branch uses the
previously accepted norm-preserving theorem at exact source commit
`7ec05f2b89b4ab69de7a6696f236aa1f6ecc3ffc`; its pinned proof SHA256
`9b3702e2737b7784c298522054f0159535172b5edde7e3de2ee59aac9b56e7e3`
matches the packet manifest.

### Endpoint-switch classification

Suppose label `i` switches before `j`. Their squared distance visits

`U_ij=|p_i-p_j|^2`, `A_ij=|q_i-p_j|^2`, `L_ij=|q_i-q_j|^2`.

The switch is pairwise contractive exactly when `L_ij <= A_ij <= U_ij`.
Consequently a failed mixed-distance test forbids `t_i<t_j`, equivalently it
creates the stated edge `j->i` and constraint `t_j<=t_i`. The reverse order
uses the other mixed distance and is tested separately. Pairs involving a
fixed label make only their already-contractive endpoint transition.

These inequalities force equal times precisely within strongly connected
components. A topological order of the condensation graph supplies the
converse chain. Hence the least possible largest batch is exactly the largest
SCC; this is an iff statement, not merely a sufficient scheduling heuristic.

For a block, failure of both accepted primitives is exactly
`rank(D)=3`, `rank([D|b])=4`. Adding rows cannot reduce either rank, while
`D` has only three columns. Therefore a failed SCC cannot be repaired by
coarsening it with another component. This proves the stronger iff
classification for endpoint-switch chains made from the two named
primitives. It does not classify other intermediate positions or other
positivity mechanisms.

Target collisions are harmless: once two current labels coincide, a
contractive next step keeps them coincident, so the labelled transition
induces a single-valued map on the actual support.

### Extraction and rooted consequence

The hinge increments and ordered mean squared-distance losses telescope over
the component chain. Strictly positive weights and nonnegative pair losses
show that zero stage loss preserves every labelled distance; the two stages
are congruent and the hinge increment is zero. Good components have
nonnegative increments. Weighted averaging of the remaining ratios therefore
gives a failing component with

`H_a/D_a <= -delta/D(P,Q)`.

This proves the claimed loss-normalized extraction. It does not preserve a
covariance floor or strict loss on every pair, exactly as the packet warns.

In the accepted rooted class, four fixed affinely independent labels leave at
most three movers on seven labels, so the new theorem signs every such case.
If the endpoint graph of a nontrivial rooted indecomposable pair had more than
one SCC, switching a source component would give a proper contracting
intermediate. A complete distance matrix congruent to an endpoint cannot
avoid this contradiction: the congruence fixes the common tetrahedron
pointwise and is therefore the identity. Thus an adverse rooted witness needs
at least eight labels, one SCC on at least four movers, and ranks `(3,4)`.
The pinned rooted-reduction proof SHA256
`bc4eed76242de833971fa79bb28da984ed9e021262f852e2a3d24e320c0aa5ad`
matches exact source commit `4518e569424cbac04083e6cb9497cc97991cf301`.

## Independent computation

[`independent_audit.py`](independent_audit.py) imports no reviewed code. It
uses exact `fractions.Fraction`, definition-level mixed-distance tests,
Boolean transitive closure instead of Kosaraju, exhaustive minors instead of
row reduction, and brute ordered partitions instead of trusting graph
metadata.

Run with CPython 3.11 or later from the repository root:

```sh
python3 -B probability/gaussian_endpoint_block_classification_review2/independent_audit.py
```

The audit returns `INDEPENDENT_ENDPOINT_BLOCK_AUDIT_PASS` and establishes:

- the published fixture has 6 movers, 19 directed constraints, SCCs
  `{4,5,6}` and `{7,8,9}`, exactly 2 valid weak orders, and optimum batch 3;
- all 4,096 simple directed graphs on four labelled vertices agree between
  SCC size and brute weak-order optimum; the exact histogram is
  `(543,867,1080,1606)` for optimum sizes 1 through 4;
- the fixture's full displacement and augmented ranks are `(3,4)`, while
  both three-label stages have exact common anchors and ranks `(3,3)`;
- the ordered loss is `211968/4235`, split into nonnegative stage losses
  `927048/21175` and `12072/1925`;
- independently generated layered controls with one through five components
  have exactly the claimed triple SCCs; the whole map changes from ranks
  `(3,3)` at one layer to `(3,4)` for every tested multi-layer instance;
- the fixed tetrahedron plus one mover triple has paired affine rank six.

The author's commands were also replayed at the pinned bytes. The producer
matched `CERTIFICATE.json`; the separate stage checker returned
`ENDPOINT_BLOCK_CERTIFICATE_VERIFIED`; normal and optimized audits returned
`ENDPOINT_BLOCK_CLASSIFICATION_CONTROLS_PASS`; and every entry in
`SHA256SUMS` matched. The source directory is unchanged between the cited
commit and the review base.

## Trust boundary and remaining gaps

The exact programs guarantee their finite rational graph, distance, rank,
anchor, loss, and control claims. They do not formalize the analytic transfer
theorems, evaluate a Gaussian integral, prove the full conjecture, or certify
novelty. The displacement-plane and common-anchor conclusions remain written
mathematics relative to the cited accepted/primary inputs. The rooted result
also remains relative to the previously accepted indecomposable reduction.

The arbitrary strongly connected, rank-three, anchor-inconsistent case is
still unsigned and can have unbounded cardinality. `NOT_COVERED` remains only
a classifier failure, not evidence of an adverse hinge. Historical priority
of the endpoint-switch packaging and its ball consequences remains uncertain.
