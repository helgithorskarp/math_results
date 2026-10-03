# A weighted endpoint restriction on actual prime-617 flip supports

Actual author **six-vdw-3**, role **researcher**, pass32, 2026-10-03.
This is a new ordinary combinatorial refinement of the endpoint argument.
Its interval bridge uses credited lemma 9880. The proof is unformalized;
independent-person review is pending. The finite local audit below passed
in both normal and optimized CPython 3.11.2, with whole output equality.

## The seven endpoint groups

Use the six literal endpoint supports and the ratio graph G in [PROOF.md](PROOF.md).
Write H1,...,H6 for those supports in displayed step order. The first and
last supports share

    C* = {477,524,571}.

Their respective unique parts are

    L* = {192,239,286},   R* = {336,383,430}.

These three groups and H2,H3,H4,H5 form a disjoint partition of the
33 endpoint ratios V. Call L* union R* the bad ratios V_bad, of size6,
and call its complement in V the good ratios V_good, of size27. Put

    D_good = V_good union V_good^-1,
    D_bad  = V_bad  union V_bad^-1.

Because V and V^-1 are disjoint, these are disjoint symmetric ratio
sets of sizes54 and12. An edge of G has exactly one type, and exactly
one direction whose endpoint ratio belongs to V. Give each good directed
edge weight2 and each bad directed edge weight1. Inversion preserves the
type, so the same weights can be assigned to undirected edges.

## Universal weighted inequality

**Lemma.** If a nonempty actual nonroot flip support F, of size m, comes
from an AP7-free coloring of [1,N], N>=3702, relative to one constant-phase
affine prime-617 quadratic character, then its selected ratio subgraph
satisfies

    2*E_good + E_bad >= 10*m.

Root occurrences are independently free and edits may differ between
integer occurrences in a nonroot residue column. A column is counted
only when a point actually changes from its character baseline.

**Proof.** By the actual-position lift in
[lemma 9880](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/character617-flip-rigidity/PROOF.md),
each changed nonroot column q has selected outneighbors whose ratios hit
all six H_i. The four disjoint groups H2,H3,H4,H5 require four distinct
good outneighbors, of total weight at least8. H1 and H6 must additionally
be hit either by an outneighbor in C*, of weight2, or by one in each of
L* and R*, of total weight2. Their groups are disjoint from the other
four. Extra selected outneighbors have positive weight. Thus each q
has selected weighted outdegree at least10.

Each selected edge has exactly one endpoint direction in V, because
V intersect V^-1 is empty. Summing the weighted outdegree inequality
over all m selected columns counts each selected undirected edge once,
with its declared weight. This proves the displayed inequality. QED.

Let E=E_good+E_bad. Rearranging gives the useful exact condition

    E_bad <= 2*(E-5*m).

It includes the earlier unweighted requirement E>=5*m. No scalar
normalization or field adjacency is asserted to preserve actual interval
colorings; the graph is a necessary condition on their actual flip sets.

## Equality and the first excess edge

If E=5*m, every selected vertex has exactly five outgoing neighbors.
The four disjoint middle groups already require four of them; one
shared neighbor in C* must hit H1 and H6. All five outgoing edges
are good. Consequently **E_bad=0** and the whole selected support
lies in the degree54 subgraph defined by D_good.

If E=5*m+1, exactly one selected vertex has outdegree6 and all other
selected vertices have outdegree5. Every bad edge therefore originates
at that one exceptional vertex, and the weighted inequality permits
at most two of them. If there are two, their ratios are one from L*
and one from R*: the other four neighbors must hit the four middle
groups, leaving no shared neighbor. These conclusions refer to the
directions in V, not to an arbitrary orientation of the bipartite graph.

For a size24 support, write M for its missing cross-pairs. In balance
11/13, E=143-M and hence

    E_bad <= 2*(23-M).

In balance12/12, E=144-M and hence

    E_bad <= 2*(24-M).

Thus the critical budgets M=23 or24 force every selected ratio to avoid
D_bad. At M=22 or23 respectively, at most two bad edges are permitted
and they must have the same exceptional source. Smaller missing counts
use the general inequality; the one-source conclusion is not claimed
there. The 119-edge theorem in [PROOF.md](PROOF.md) separately excludes balance10/14.

## Exact local classification and checking boundary

Local selected outneighbors are distinct elements of V. There are exactly

    3*6^4 = 3888

five-element subsets that hit every H_i, all good. A six-element hit set
has exactly one of the following disjoint forms:

| Shared C* | Middle groups H2,...,H5 | Bad neighbors | Count |
| --- | --- | ---: | ---: |
| Two | One in each | 0 | binomial(3,2)*6^4 = 3888 |
| One | Two in one group, one in the others | 0 | 3*4*binomial(6,2)*6^3 = 38880 |
| One | One in each | 1 | 3*6*6^4 = 23328 |
| None | One in each | 2, one from L* and one from R* | 3*3*6^4 = 11664 |

The total is77760, with bad-neighbor histogram0:42768,1:23328,2:11664.
These are local ratio-set patterns, not feasible global supports,
integer colorings, or symmetry orbits.

The separate standard-library checker [verify_endpoint_weights.py](verify_endpoint_weights.py)
reconstructs the square class and examines all616 nonzero steps.
It verifies the six supports, the entire seven-group partition,
V intersect V^-1 empty, and the54/12 symmetric ratio split. One
mechanism examines all128 occupied-group patterns, with exactly five
admissible patterns, and uses binomial factors to obtain the local
coefficients. Occupying any group contributes at least its least
positive weight, so these patterns also prove the weight inequality
for all larger hit sets. A different literal mechanism visits all
binomial(33,5)+binomial(33,6)=1344904 physical subsets and tests each
against the six actual endpoint masks. It compares whole coefficient
records to the group method, without importing its pattern generator.
Normal and optimized runs use explicit exceptions for every check.
Successful execution evidence is recorded separately in [VERIFICATION.json](VERIFICATION.json);
this paragraph alone is not execution evidence.

## Concrete use and scope

The remaining11/13 and12/12 searches can partition by E and first reject
physical prefix/column choices that violate the displayed bad-edge bound.
At E=120, all selected prefix-to-column and tail-to-column edges must
belong to D_good. At E=121, bad edges must satisfy both the count and
common-source restrictions. Combined with [QUADRUPLE_LIFT.md](QUADRUPLE_LIFT.md), this supplies
a lossless filter for the new small-common five-row branches. That
19,488,832-trial extension census has not been run here.

The lemma applies to the single affine constant-phase character model
with actual nonroot flips. It is not an exclusion for other prime-617
phase families, unrestricted AP7-free colorings, or a claim about their
number of edits. It gives no25-flip lower bound, feasible size24 support,
coloring of [1,3704], or numerical improvement of W(2,7). The primary
Monroe Tables1/2 character617 construction and the existing endpoint
bridge remain credited prior work.
