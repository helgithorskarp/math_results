# Exact half separators after subdividing the whole necklace core

The two-geodesic half-separator theorem for a necklace extends to positive
mass at **all subdivision vertices**, including wheel and cross edges.
Those vertices could not receive mass in the preceding metric theorem.
A switch between two geodesics ending inside one cross edge repairs the
specific overlap that prevents a direct transfer of the old proof.

This gives a family of simple planar **unit-edge graphs**, of unbounded
order and number of branches, satisfying the exact-half target for every
nonnegative vertex mass, including uniform vertex counts. It is a partial
result for [Barbados Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf),
not a result for every planar graph. Independent review is pending.

## Precise statement

Let t>=4 and let lambda,ell_0,...,ell_(t-1) be positive integers.
Start with vertices r, a_j,b_j,c_j for j=0,...,t-1. The edges are:

* the cycle a_0,b_0,a_1,b_1,...,a_(t-1),b_(t-1),a_0;
* every root edge from r to an outer vertex a_j or b_j;
* the two cross edges a_j c_j and b_j c_j for each j;
* the cycle edges c_j c_(j+1), with cyclic indices.

Replace every outer, root and cross edge by a path of **lambda unit
edges**, and c_j c_(j+1) by a path T_j of **ell_j unit edges**. All new
interiors are disjoint. Call the resulting graph U. The original vertices
retain their names; paths replacing original edges will be called chains.
Its planar embedding is the usual two-ring annulus capped by r, followed
by edge subdivision. It is simple for t>=3.

**Theorem.** For every nonnegative real mass on every vertex of U, of
total W, there are at most two shortest paths in the original U whose
union leaves every component with mass at most W/2.

The ell_j may vary independently. The common lambda condition on all
wheel and cross chains remains essential to this proof. The theorem does
not allow arbitrary independent lengths on those chains or additional
attachments. No new mass is ignored or moved to a chain endpoint.

The proof depends on the distance and path catalogs in the preceding
[arbitrary-inner-metric lemma](../planar_two_geodesic_arbitrary_inner_metrics/README.md)
and [all-long-inner theorem](../planar_two_geodesic_metric_necklaces/README.md).
We give the new mass partition, all changes to their component bounds,
and the new cross-edge switch below. Thus this is a written structural
proof using those predecessors, with finite exact checks as controls.

## Edge pieces, the heavy case, and the metric quotient

An **edge piece** is the interior vertex set of one outer, root or cross
chain. Write B for the largest mass of any edge piece, with default zero.
Each such whole chain is an ambient geodesic: in the weighted quotient,
its length is lambda, and another route cannot beat it. The wheel is
isometric, because every inner excursion uses two cross edges. A route
from a branch to an outer parent must use at least one cross edge of
length lambda. Suppressing degree-two interiors preserves these distances.

If an edge piece has mass greater than W/2, its whole geodesic chain
alone removes more than half the mass. This proves that case. We may
henceforth assume B<=W/2. Equality also causes no difficulty.

Whenever both original ends of a chain have been deleted, any surviving
part of its interior is a component contained in that one edge piece,
and is bounded by B. Partial deletions can only split such a piece.
This replaces the old proof's treatment of detached outside components.
Inner-arc interiors are not edge pieces in this argument; their entire
mass remains in the sweep.

Suppress only the outer, root and cross interiors, retaining every
vertex of each T_j. Give each suppressed chain length lambda. Call this
weighted graph H. Its metric on retained vertices agrees exactly with U.
Lifts of H-geodesics are U-geodesics. Geodesics ending inside a suppressed
chain are justified separately by the endpoint comparison below.

If some ell_j<=lambda, rotate the labels so ell_(t-1)<=lambda and use
the arbitrary-inner-metric proof. If no such j exists, all ell_j>lambda
and use the all-long proof. This explains both the metric dichotomy and
the requirement t>=4. All paths retain their ambient shortestness.

## A mass partition which keeps cross interiors

Set o_(2j)=a_j and o_(2j+1)=b_j, and fix S0={r,a_0,c_0}.
Every path pair below collectively contains S0. Discard the interiors
of the r--a_0 and a_0--c_0 chains from the represented mass: after S0
is removed, they are detached pieces of mass at most B. Let D be their
total mass and put

```
M=W-w(S0)-D,                 h=max{M/2,B}<=W/2.
```

Partition the represented vertices into disjoint groups:

```
alpha_i: o_i and the interior of r--o_i, for i!=0;
beta_i:  the interior of o_i--c_floor(i/2), for i!=0;
kappa_i: the interior of o_i--o_(i+1);
gamma_j: {c_j}, for j!=0;
tau_j:   the interior of T_j.
```

The groups alpha_0,beta_0,gamma_0 are empty. At the incident state (i,j),
where i=2j or 2j+1 before the final wrap, define

```
L(i,j)= union_(s<i)(alpha_s union beta_s union kappa_s)
        union union_(q<j)(gamma_q union tau_q);
R(i,j)= represented minus L(i,j),alpha_i,beta_i,gamma_j.
```

The lifts of (r,a_0,c_0) and (r,o_i,c_j) are geodesic. Their deletion
leaves every component either inside L(i,j), inside R(i,j), or inside
one edge piece. To verify this, the two root paths cut the inner and
outer cycles into matching intervals; each cross chain stays on its
side. A cross chain with both original ends deleted is detached. A root
chain with its outer end still present stays with that endpoint; one
whose outer end is deleted is detached. The same statements apply to
outer chains. This accounts for every vertex of U.

The left mass increases and right mass decreases from (0,M) to (M,0),
with their sum at most M<=2h. If no spoke pair has both sides light,
take the first transition with new left mass >h. Its old right mass is
also >h. The old left and new right sets, written L,R below, are light.
It remains to repair the A- and D-transitions. The earlier proof's
geodesic paths are kept except for the cross-edge switch described next.

## Repair when both parents bypass the inner carrier

Assume ell_(t-1)<=lambda. Write delta_j for intrinsic inner-cycle
distance from c_0 to c_j. The preceding proof establishes

```
d(a_0,c_j)=lambda+min{delta_j,2lambda};
d(c_0,a_j)=lambda+min{delta_j,lambda+delta_(j-1),2lambda};
d(c_0,b_j)=lambda+min{delta_j,lambda+delta_(j+1),2lambda}.
```

Its ordinary A-step pairs remove both parents and their branch, so any
remaining cross interiors are detached edge pieces. They therefore still
give the light L,R bounds. Only the case where neither parent can be
appended to an inner carrier needs a change. Here

```
delta_j<2lambda,
delta_j>lambda+delta_(j-1),
delta_j>lambda+delta_(j+1).
```

Let an inner shortest I_j enter c_j through T_(j-1). Write I_(j-1)
for its prefix. Put a=a_j, b=b_j, c=c_j, i=2j, and let the cross chain
a--c be X=(x_0=a,...,x_lambda=c), with coordinate z_s=s. The detour

```
J=I_(j-1), b_(j-1), a
```

is shortest from c_0 to a, of length e=delta_(j-1)+2lambda.
The path I_j is shortest from c_0 to c, of length d=delta_j. Neither
uses the interior of X. Therefore extension of J through x_p is shortest
if 2z_p<=theta, while extension of I_j backwards through x_q is shortest
if 2z_q>=theta, where

```
theta=lambda+d-e=ell_(j-1)-lambda.                     (1)
```

These follow by comparing the only two entrances a,c to an interior
vertex: e+z versus d+lambda-z. Here 0<theta<lambda, using the strict
parent bypass and delta_j<2lambda. Choose p last with 2z_p<=theta
and q first with 2z_q>=theta. Thus q<=p+1. Compare the two pairs

```
J followed by x_1,...,x_p,          (a_0,r,b);
I_j followed by x_(lambda-1),...,x_q,   (a_0,r,b).       (2)
```

All quotient routes are lifted to U. The common wheel complement is
geodesic; the adjacent closing exception cannot occur in the bypass case.
Both pairs contain S0. Their potentially heavy core supports are

```
H1=R union gamma_j union tau_(j-1) union beta_(i+1)
       union {x_(p+1),...,x_(lambda-1)};
H2=(L minus tau_(j-1)) union alpha_i union kappa_i
       union {x_1,...,x_(q-1)}.                         (3)
```

The other components lie in L or R or a detached edge piece. For the
first pair, the surviving cross interiors attach on the branch side.
For the second, the remaining part of X attaches on the a side, while
the b--c interior has both ends deleted. Its mass is at most B.
The two displayed cross subsets are disjoint because q<=p+1. Every
other group in H1,H2 is disjoint as well, so H1,H2 cannot both exceed h.

If I_j instead enters backwards through T_j, use X from b_j to c_j,
J=I_(j+1),a_(j+1),b_j, and common complement (a_0,r,a_j). The supports
become

```
H1=L union gamma_j union tau_j union beta_i
       union the surviving suffix of X;
H2=(R minus tau_j) union alpha_(i+1) union kappa_i
       union the surviving prefix of X.
```

The same coordinate comparison and disjointness prove that orientation.
This is the new step: leaving the old carrier endpoints unchanged would
count the same cross-interior mass on both potentially heavy sides.

## All D-steps retain disjoint supports

At a D-step set i=2j+1, a=b_j, b=a_(j+1), and
T_j=(v_0=c_j,...,v_n=c_(j+1)). Whenever a pair deletes both outer sites
and a suffix v_q,...,v_n, its core components lie in

```
L union gamma_j union beta_i union {v_1,...,v_(q-1)}, R. (4)
```

With a prefix v_0,...,v_p they lie in

```
L, R union gamma_(j+1) union beta_(i+1)
       union {v_(p+1),...,v_(n-1)}.                    (5)
```

Other components are detached edge pieces. Thus the far-endpoint
prefix/suffix pairs of the arbitrary-inner-metric proof still work:
their ordered cuts q<=p+1 give disjoint supports (4),(5). The two newly
added beta groups are distinct and occur in opposite supports.

For its near-left carrier/split pair, the two potentially heavy supports
are now

```
R union gamma_(j+1) union tau_j union beta_(i+1);
L union alpha_i union kappa_i union beta_i.             (6)
```

For its reflected near-right pair they are

```
L union gamma_j union tau_j union beta_i;
R union alpha_(i+1) union kappa_i union beta_(i+1).       (7)
```

They remain disjoint. In the carrier pair the untraversed cross chain
stays with its surviving branch. In the split pair the whole inner arc
is deleted, and the untraversed cross chain stays with its surviving
outer endpoint. Its beta group is on the opposite side of (6) or (7).
These formulas also include the first and closing steps, where beta_0
is empty and its physical chain is a discarded edge piece. No change to
the predecessor's clipped coordinate thresholds is needed.

## The all-long region

If every ell_j>=lambda, retain the path catalog and coordinate choices
of the [all-long-inner proof](../planar_two_geodesic_metric_necklaces/README.md).
Its A-step pairs remove both parents and their branch, so each untraversed
cross piece detaches, as above. Every noninitial D-step removes both
outer sites together with an inner prefix or suffix. Its potentially
heavy supports are exactly (4),(5), with the same ordered cuts proved
there. Adding beta_i on one side and beta_(i+1) on the other preserves
disjointness.

For clarity, the only special initial D-step uses coordinates z on T_0
and the paths

```
(a_0,c_0,v_1,...,v_p),               (r,b_0);
(r,a_0,c_0),               (b_0,a_1,c_1,v_(n-1),...,v_q),
```

where p is last with 2z_p<=ell_0+min{2lambda,ell_0}, and q is first
with 2z_q>=ell_0+lambda. These are the predecessor's ambient geodesics.
Because ell_0>=lambda, q<=p+1. The first pair's possibly heavy support
is old R with the deleted prefix removed; the second's is the initial
inner slice {v_1,...,v_(q-1)}. They are disjoint. The b_0--c_0 cross
piece has both ends deleted in both alternatives and is bounded by B;
the a_1--c_1 cross piece is traversed by the second alternative and is
included in old R for the first. The outer a_0--b_0 piece likewise
detaches. Hence no omitted cross mass defeats the initial-step argument.

This verifies every modified component bound in both metric regions.
The monotone sweep gives two geodesics with residual mass at most h.
Since h<=W/2 in the light-piece case and the heavy-piece case was already
handled, the theorem follows. For W=0 any singleton suffices.

## A literal control where the old transfer fails

Take t=4, lambda=3 and inner totals (1,4,4,1). The unit graph has
67 vertices and 82 edges. At the A-step for c_2, give mass 4 to the
first interior vertex of a_2--c_2 measured from a_2, mass 4 to the
first interior vertex of a_2--b_2, and mass 3 to c_3. All other masses
are zero. Thus W=11, B=4, h=11/2. The relevant old and new light sides
satisfy the sweep crossing conditions: old right mass is 7 and new
left mass is 8.

The unmodified carrier pair leaves mass 7; the unmodified complementary
inner pair leaves mass 8. Both are still geodesic, but neither balances
this mass. In (1), theta=1, so p=0 and q=1. The repaired second pair
extends the c_0-to-c_2 inner route backwards through both interior
vertices of a_2--c_2, and uses (a_0,r,b_2) as its other path. Its largest
residual component has mass 4. Reflect the construction to the other
cross edge for the second control in [audit.py](audit.py).

This is a failure of the old local transfer, with an explicit repair.
It is not a counterexample to the two-free-geodesic target or to the
previous theorem, whose hypotheses excluded these new masses.

## Reproduction and trust boundary

From the repository root, Python 3.11+, standard library, assertions on:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_subdivided_wheels/verify.py --check
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_subdivided_wheels/audit.py
```

The main checker constructs the full unit graphs, uses exact BFS distances
and actual components, checks all displayed path pairs and support
containments, and checks disjointness in both proof regions. Geometry
helpers and the mass-selection routine are imported from earlier work;
the core embedding is checked there, and subdivision preserves it.
Seed 2026092929 specifies 48 models and 420 anchor orientations, including
lambda=1 and both cross-switch orientations. It checks 12,216 component
cuts, 2,512 quantitative mass choices, 2,100 light-piece half bounds, and
412 heavy-edge repairs. Uniform mass is included for every orientation.
Full expected counts are in [expected.json](expected.json).

The separate audit imports no research code. It independently rebuilds
the named 67-vertex unit graph, computes BFS distances and components,
and checks both literal cross-switch controls. For each it prints old
residuals [7,8], repaired residuals [7,4], W=11, B=4 and theta=1, with
status PASS. Its scope is these new local controls; it does not independently
reproduce the main fixture stream or the universal theorem.

The all-order and all-real-mass conclusions use the written partition,
switch and predecessor path proofs, not sampling. No solver or proof
assistant is a premise. This is same-researcher checking; independent
review of the extension is pending. The theorem concerns the specified
uniform wheel/cross subdivisions, not arbitrary unit subdivisions of a
graph with a weighted separator certificate.

The [official workshop schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html)
announces a Codsi separator-conjecture disproof. The bounded primary-source
refresh on 2026-09-29 still did not identify its exact statement or witness.
No continued-open, general-resolution, or historical-priority claim is made.
