# Every rotation of the fixed heptagon–spindle sum is four-chromatic

**Theorem.** Let H be the fixed 21-point heptagon set and M the fixed
seven-point Moser spindle defined in [PROOF.md](PROOF.md). For every
complex number r with |r|=1, the complete unit-distance graph on

```
H+rM = {h+r*m : h in H, m in M}
```

has chromatic number **exactly four**. Every vertex- or edge-deleted
subgraph of every member is therefore four-colourable as well.

This closes the full continuous rotation family, including all
collision orientations and all mixed-contact angles. There are no
remaining possible five-chromatic members of this fixed family. It is
a negative construction result, not an improvement to the 509-vertex
record. It does not cover changed factors, additional points, or unions
of several independently rotated sums.

The last finite step checks all **480 both-nonunit contact equations**.
Every exact elimination graph has 147 formal vertices, 525 factor
edges and just **one additional edge: the defining contact itself**.
One H colouring and four M colourings certify all 480 graphs. No
algebraic contact roots or native SAT queries were needed.

## Definitions and inherited results

For an explicit coordinate definition, put t=exp(pi*i/21), s=i*sqrt(11)
and, for j=0,...,6,

```
P_j = t^(6*j)/(t^24-t^(-24)),
Q_j = -t^(6*j-7)/(t^6-t^(-6)),
R_j = -t^(6*j+7)/(t^12-t^(-12)).
```

H is the ordered list P_0,...,P_6,Q_0,...,Q_6,R_0,...,R_6. With
u=Q_0-P_0, v=R_0-P_0 and rho=(5+s)/6, the ordered spindle is

```
M = (0,u,v,u+v,rho*u,rho*v,rho*(u+v)).
```

The exact arithmetic uses K(s), K=Q(t), degree 24 over Q; the point
coordinates have common denominator 42 in the published coefficient
basis. The defining field and coordinate justification are given in
PROOF.md. The theorem quantifies over **all** unit complex r, not only
rotations lying in that field.

The following already published results are used with their exact scope:

* [COLLISIONS.md](COLLISIONS.md), source
  `4ec850c8ba08f8beea0a811c49e3b526aa123e38`: the sum map is noninjective
  at exactly 252 rotations, forming C, and every such sum is
  four-chromatic. This and its inherited unit-contact certificate were
  independently accepted in the [collision review](../hadwiger_nelson_heptagon_moser_sum_collisions_review1/README.md),
  source `cd2a5b7d74def8059a1f1bdc58ecb900c570cd4c`.
* [COMMON_NEIGHBOUR.md](COMMON_NEIGHBOUR.md), source
  `6882c980c31f08481228629aa5ea193c04e32ca2`: a mixed unit contact
  using a unit H difference forces r into C.
* [CONTACT_ENVELOPES.md](CONTACT_ENVELOPES.md), source
  `bed7c367371df2024cb5e9428885333b1d85760c`: every sum with a mixed
  unit contact using a unit M difference is four-chromatic. Its 126
  remaining equations have elimination graphs with at most two mixed
  edges beyond the factor graph. The earlier dual incidence theorem,
  source `55b29e49c8737ed321c2c8ed32149d50086c738c`, supplies its
  finite event cover.

The new finite computation concerns only contacts with both factor
differences nonunit. Earlier certificates were not regenerated during
this pass. The sources and current input hashes are pinned in
[rotation_family_validation.json](rotation_family_validation.json).

## General elimination without choosing a root

For any nonzero a,b define

```
U=conjugate(a)*b,    n=|a|^2+|b|^2-1.
```

For a candidate edge difference x+r*y define

```
V=conjugate(x)*y,    q=1-|x|^2-|y|^2,
D=U*conjugate(V)-conjugate(U)*V,
S=q*U+n*V.
```

If |r|=1 and both |a+r*b|=1 and |x+r*y|=1, expanding the squared
norms gives

```
U*r+conjugate(U)*conjugate(r)=-n,
V*r+conjugate(V)*conjugate(r)=q,
S=D*conjugate(r),
|S|^2-|D|^2=0.                                    (1)
```

This is the general determinant identity proved in CONTACT_ENVELOPES.md.
Here n must include **|b|^2-1**: the unit-M specialization n=|a|^2 is
not valid for the new cohort. The argument divides by neither n nor D,
and includes n=0, dependent equations and tangency.

Define the elimination graph on the 147 formal labels (h,m) by (1),
using x=h_i-h_j and y=m_p-m_q. For every rotation satisfying the
defining contact, every actual unit edge has its formal edge in this
graph. If the sum map is injective, a proper colouring of the
elimination graph therefore colours the actual unit graph.

The criterion is used only in this direction. Its graph may combine
edges from different roots or include spurious edges for an infeasible
contact. These are abstract supergraphs, not claimed unit-distance
realizations. A failed supergraph colouring would not prove an actual
geometric obstruction. Collision cases require separate colour descent
and are handled by the inherited theorem for C.

## The complete remaining finite cohort

The 420 distinct nonzero directed H differences include 336 nonunit
ones. Their 168 sign classes correspond exactly to unordered nonadjacent
H pairs. Multiplication by zeta=exp(2*pi*i/7) preserves H; these pairs
form 24 orbits of size seven. Choose the least labelled pair i<j in
each orbit and set a=h_j-h_i. M has 20 distinct nonzero directed
nonunit differences. Pairing them gives **24*20=480 equations**.

This covers every both-nonunit contact up to whole-plane rotation and
simultaneous sign reversal of a,b. If an endpoint order reverses under
rotation, replace (a,b) by (-a,-b); the distance equation is unchanged
and -b remains in the directed M difference set. No reflection or
unproved invariance of H under negation is used. The new checker
reconstructs the 24 pair orbits from coordinates, verifies that they
cover all 168 pairs, and checks all 20 M directions and 480 combinations.

Index a formal point by `7*h+m`. Each graph contains 42*7+11*21=525
factor edges. The exact census is:

| Formal vertices | Factor edges | Mixed edges | Equations |
|---:|---:|---:|---:|
| 147 | 525 | 1 | 480 |

For every defining event `(hi,hj,mi,mj)` with hi<hj, the sole mixed
edge is exactly

```
(7*hi+mj, 7*hj+mi).
```

Its difference is the negative of a+r*b, so it is necessarily present
whenever the defining event has a root. Consequently any injective sum
with a both-nonunit mixed contact has **exactly one mixed edge**. The
census rules out all other mixed unit edges at the same rotation,
irrespective of their factor lengths.

The [11235-byte certificate](rotation_family_certificate.json) lists
all 480 events, their extra edge and an M-colouring index. It supplies
one proper 21-entry H colouring and four proper seven-entry M colourings.
For each event,

```
colour(7*h+m)=H_colour[h] XOR M_colour[m]
```

is proper on the full elimination graph. All 252480 colour-edge
inequalities are checked. The finite graphs are generated locally;
only the compact witness data are published.

## Why every rotation is now covered

Fix any |r|=1. If r belongs to C, use the collision colouring theorem.
Otherwise the sum is injective and has 147 distinct points.

If it has no mixed unit edge, its complete unit graph is the Cartesian
product of the two factor graphs, with a proper XOR four-colouring.
If it has a mixed edge using a unit H difference, the earlier theorem
would force r into C. If a mixed edge uses a unit M difference, the
unit-M contact theorem supplies a four-colouring. In every remaining
case there is a both-nonunit mixed edge, and the new 480-equation
certificate supplies a four-colouring. These cases exhaust every
rotation, including ones whose coordinates require a field extension.

Every H+rM also contains a translated rotated copy of M, which is
four-chromatic. Thus the upper and lower bounds are both four. Restricting
a proper colouring proves the assertion for every subgraph.

There is also a structural bound: **every injective sum has at most
two mixed unit edges**, hence at most 527 unit edges in total. A unit-M
contact is covered by an earlier envelope with at most two mixed edges;
without such a contact the new census allows at most one. The empty
mixed-edge case is the 525-edge product. This is a bound, not a census
of which exact angle or graph types are attained.

## Independent Gram-determinant audit

The producer evaluates (1) in the earlier t/s basis. The checker imports
neither rotation_family.py nor field.py. It reconstructs H and M in the
separate zeta7/omega6/w basis and uses a real Gram determinant instead.

The vectors

```
u=(2*Re(U),-2*Im(U)),
v=(2*Re(V),-2*Im(V)),
e=(Re(r),Im(r))
```

lie in a real plane. At a simultaneous contact their Gram matrix is

```
[ 4*|U|^2,              2*(U*conjugate(V)+conjugate(U)*V), -n ]
[ 2*(U*conjugate(V)+conjugate(U)*V), 4*|V|^2,              q ]
[ -n,                              q,                    1 ]
```

Its determinant vanishes because its rank is at most two. Expanding
shows that this determinant is `-4*(|S|^2-|D|^2)`, so it defines exactly
the same elimination graph. The checker evaluates the six-term
determinant directly in exact arithmetic for surviving candidates.
This derivation is general in a,b; it does not reuse the prior unit-b
square-root formula. Clearing the common coordinate denominator scales
the first two Gram vectors by 42^2 and preserves the zero condition.

All 147-choose-2 formal pairs are accounted for in each graph: 8820
mixed and 1911 unmixed pairs, totaling 5150880 pair tests over the
cohort. For unmixed pairs V=0 and U!=0, so (1) is equivalent to q=0,
the usual factor unit-distance test. For mixed pairs, sound finite-field
homomorphisms reject nonzero residuals before exact arithmetic.

The producer uses `(prime,t,s)` maps `(1093,275,128)` and
`(1303,272,125)`; the checker uses `(2017,54,822)` and `(2143,325,207)`
in its tensor basis. Each implementation validates primality and the
defining polynomial relations. An exact zero remains zero under every
map, and every modular survivor is rechecked in characteristic zero.
Each run had 480 survivors, all exact zeros. All 480 full graph edge
lists were compared entrywise, followed by the complete colouring
checks. The hashes identify fully compared streams, not merely equal
aggregate counts.

Controls explicitly reject using the old n=|a|^2 specialization when
|b|!=1. They also cover n=0, tangent contacts, an edge present at only
one of two roots, dependent normals, an infeasible contact, and a
formal colouring that fails to descend through a collision. Six
corrupted certificates or invalid inputs are rejected. These are
author-run checks; no separate-author review of the new full-family
closure is claimed.

## Reproduction and decision

Use a full checkout, Python 3.11.2 and the standard library, with
assertions enabled. From this directory choose a fresh external output:

```bash
python3 -B rotation_family.py --out /scratch/fresh-heptagon-rotation-family
python3 -B rotation_family_audit.py --work /scratch/fresh-heptagon-rotation-family
sha256sum -c SHA256SUMS
```

Expected status: `EVERY ROTATION OF THE FIXED H+rM FAMILY IS FOUR-CHROMATIC`.
[rotation_family_expected.json](rotation_family_expected.json) fixes
the counts and hashes; [rotation_family_validation.json](rotation_family_validation.json)
records the pinned dependencies and measured runs. Generation took
5.46 seconds and the independent audit 12.07 seconds, one thread;
peak memory was not measured. The full graph stream stays local and
is regenerated from public source. No large trace or negative native
proof is needed.

The trust boundary consists of the geometric elimination and coverage
proofs, the inherited coordinate-field justification and colouring
theorems, exact Python arithmetic, and the complete finite loops and
sound modular rejection. The independently accepted collision review
covers that dependency, not the new full-family theorem.

The named target remains a five-chromatic Euclidean unit-distance graph
on at most 508 vertices. Record calibration was checked live on
2026-09-06 against [Parts' source](https://arxiv.org/abs/2010.12665) and
[Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4).
Only H's coordinates are imported from the latter; its numerical
construction claims are not premises. No record improvement or
priority claim for the elementary elimination identity is made.

**Decision:** stop rotation search and deletion-only descent in this
fixed two-factor family. The next direction must change the construction.
A proposed bounded feasibility assessment is to couple two sums through
their common H, producing at most 2*147-21=273 vertices because M contains
the origin. The present theorem colours each component separately and
does not control new edges between them. No such union, compatibility
test, enlarged factor or new construction phase was started here.
The complete family checkpoint is preserved before yielding.

The final relevant graph refresh reached height 3121. HN-2's
[two-large/seven-small deletion closure](../hadwiger_nelson_heule517_large2_pilot/README.md),
source `86287fd43140e23790f97a3d267299585f0335e7`, was inspected. Any
remaining non-four-colourable H517 subgraph on at most 508 vertices
now needs at least 136 small vertices and three large deletions.
This is conditional on the 508-vertex size bound; it does not assert
an unconditional 136-small lower bound for larger subgraphs. That
unrestricted target family remains open and separate, and supplies
no premise for this geometric closure.
