# Complete separator classification through order18

Red is adjacency and blue is nonadjacency. A graph is good if it contains
neither a red nor a blue K5. We prove that a good43 has no separator of
size at most17, and that every separator of size18 isolates exactly one
vertex, leaving a connected24-vertex component. The same applies in blue.

## 1. Inputs and complete component reduction

The standard bound R(4,5)<=25 implies minimum degree18 in each color:
a vertex has at most24 neighbors in the other color. We import this
classical theorem; the later [Gauthier--Brown HOL4 proof](https://arxiv.org/abs/2404.01761)
is primary provenance, not a formal development rerun for this artifact.

For completeness, R(3,3)<=6 follows from the three same-color edges at a
vertex. A triangle-free graph on9 vertices with independence number<=3
would have maximum degree3. Every nonneighbor set has independence<=2
and is triangle-free, hence has at most5 vertices. Minimum degree is3,
forcing an impossible odd degree sum27. Thus R(3,4)<=9. A triangle-free
order14 graph with independence<=4 has maximum degree4, while its
nonneighbor sets have order<=8 by R(3,4)<=9; minimum degree is5, impossible.
This proves R(3,5)<=14. We also use color reversals and R(2,5)=5.

Let S be a separator, k=|S|<=18. Distinct red components of G-S are
blue-complete to each other. Their independence numbers add and sum to
at most4. A component with independence number1,2,3 has order at most
4,13,24, respectively. These follow from R(5,2), R(5,3), R(5,4).
There are at least two components, so no component can have independence4.

If a nonsingleton component A is a clique, 2<=a=|A|<=4. Each of its
vertices has at least18-(a-1) red neighbors in S. The common red
neighborhood therefore has order at least

    L(a,k)=a(19-a)-(a-1)k.

At k=18, for a=2,3,4 this is16,12,6. Smaller k increases L. But this
common neighborhood has no red (5-a)-clique and no blue K5, so its order
is at most13,4,0, respectively. Every nonsingleton clique component is
impossible.

If a singleton occurs, there cannot be two nonsingleton components:
the independence budget would be at least1+2+2=5. If there are at least
two singletons and a nonsingleton, the latter has independence<=2 and
order<=13, so altogether there are at most16 remaining vertices. If
all components are singletons there are at most4. Both contradict
43-k>=25. Hence a singleton forces exactly two components, of orders
1 and at most24. Again 43-k>=25 forces k=18 and the orders1,24.
Minimum degree18 then gives S=N_G(v) for the singleton v and d_G(v)=18.
This is the sole retained boundary and is not asserted realizable in good43.

If no singleton occurs, every component has independence at least2.
There are exactly two, both of independence2, of orders at most13.
Their total is at least25. Consequently the only possibilities are

    k=17, orders13+13; or k=18, orders12+13.

The same independent arithmetic is exposed in CERTIFICATE.json. It
contains12 conservative necessary component profiles before the clique
contradictions:11 excluded profiles and the retained18/1+24 profile.
Two differently organized enumerators agree on every row. This does not
claim that the arithmetic profiles themselves are realized by good graphs.

## 2. The13+13 branch (previous accepted argument)

Choose z in S. Its red neighbors in either component have no red K4
and independence number<=2, so number at most8 by R(4,3)<=9. At least5
vertices of each13-side are blue to z. Each such set contains a blue
pair, since otherwise it contains a red K5. The two blue pairs, all
blue across the component cut, together with z form a blue K5.

This argument and the smaller-separator cases are already in accepted
h3381 ([source](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_global_connectivity18)),
reviewed at h3393 ([review](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_global_connectivity18_review1)).
The review explicitly left12+13 open. We reproduce this coverage for a
self-contained classification; it is not claimed as new.

## 3. Exact unique-attachment lemma

**Lemma.** Let F have12 vertices, no triangle and no independent5-set.
There is at most one independent4-set Q such that F-Q has no independent
4-set. Call such a Q special.

Here is a complete finite proof, independently executable by `check.py`.
If a special Q exists, H=F-Q has8 vertices, no triangle and independence
number<=3. Generate every labeled such H by appending vertices in order.
The new vertex's neighbor set M must be independent (to avoid triangles)
and intersect every independent triple in the previous graph (to avoid
an independent4 containing the new vertex). These conditions are necessary
and sufficient. Deleting the last vertex proves completeness and uniqueness
of the recursion by induction from the empty graph.

The labeled counts at orders1..8 are

    1, 2, 7, 40, 322, 2812, 13842, 17640.

All8! permutations are then applied explicitly to each successive smallest
remaining8-vertex code. The three complete disjoint orbits have sizes
5040,10080,2520 and least codes5388912,5404008,5683824. Codes use low bits
for lexicographically ordered unordered pairs. No canonical-labeling
library, automorphism verifier, or external completeness assertion enters.
Taking representatives is a finite proof-enumeration convenience; this is
not a new carrier quotient or a count of43-vertex target classes.

For each H, append four labeled vertices Q with no edges among them.
For a vertex q in Q let X_q be its neighbor set in H. Each X_q must be
independent. To forbid independent5-sets meeting Q, it is necessary and
sufficient that:

- each union X_q1 union X_q2 meets every independent triple of H;
- each union of three X_q meets every independent pair of H;
- the union of all four X_q is V(H).

Indeed an independent5 uses0,1,2,3 or4 vertices of Q. The first two cases
are already impossible because alpha(H)<=3. The last three are exactly
the three conditions. Triangles are impossible precisely when each X_q
is independent, since Q has no internal edges.

All ordered star tuples are covered; no permutation quotient of Q is
used. There are39,36,33 possible stars for the three core representatives.
The compatible ordered two-star prefixes number274,258,200; the three-star
prefixes number288,150,0. The complete four-star extension counts are
48,0,0. Every one of the48 physical12-vertex graphs is independently
checked by literal triples and five-sets. In each, all independent fours
are enumerated and precisely one intersects every independent four:
Q={8,9,10,11}. Intersecting every independent four is exactly the condition
that its deletion leaves none. Thus Q is the only special set.

If any F had two special sets, selecting the first and relabeling H to
one of the three representatives would produce an enumerated extension
with two special sets, a contradiction. This proves the lemma. All48
edge codes and all orbit sizes are in INDEPENDENT.json; the checker
regenerates the enumeration rather than trusting those expected counts.

For a different route to the same finite observation, `derive.py` scans
the12 author catalog records in [McKay's Ramsey(3,5;12) file](https://users.cecs.anu.edu.au/~bdm/data/r35_12.g6).
It finds exactly one special set: vertices0,1,2,3 in zero-based record2,
`K?_YPMQoPokc`. All other records have none. The independent checker instead
checks all4096 contact words per record, transports every admitted marked
graph by all necessary core/tail vertex permutations, and compares the
entire resulting set of48 physical graph codes with its exhaustive output.
This is entry-level agreement, not just matching totals. The author
[page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html) describes a complete
catalog, but that completeness is **not a premise** of our proof: the
self-contained marked enumeration above already covers every possible F
that could have a special set. The small raw file is retained for the
independent discovery crosscheck and attribution.

## 4. Decide every12+13 attachment, including all separator edges

Let the red components be A of order12 and B of order13. Both have
independence number2. For each z in S, its red neighborhood in either
component has no K4 and independence<=2, so has size at most8.
Consequently its blue neighborhood in B has at least5 vertices and
contains a blue pair.

The blue neighborhood of z in A cannot contain a blue pair: one pair
from A and one from B would join z to make a blue K5. Thus its blue
neighbors in A form a red clique, of size at most4. Its red neighborhood
in A has size at least8, and hence exactly8. Write Q_z for the other
four vertices. They form a red K4, and A-Q_z has no red K4.

The complement F of G[A] is triangle-free with independence number<=4.
Every Q_z is a special set in F. By the complete lemma all Q_z coincide.
Every z in S therefore has the **same** eight red neighbors D in A.
Since alpha(G[D])<=2 and |D|=8, D contains a red triangle by R(3,3)<=6.
Any red edge inside S would join that triangle to give a red K5.
Thus every pair in S is blue. But |S|=18, which contains a blue K5.
This contradiction decides the entire12+13 branch, not a single fixed
component, attachment signature, or local compatibility projection.

The reduction quantified over arbitrary component graphs, all18 separator
vertices, all their contacts to both components, and every edge in S.
The finite12-vertex calculation becomes a full43-vertex class decision
through this forced common-neighborhood and separator-clique mechanism.

## 5. Global cut and connectivity consequences

In either color every separator of size<=18 is consequently of the
18/1+24 form. A degree18 vertex always gives such a separator by deleting
its neighborhood; the other24 vertices must be connected by the theorem.
Therefore kappa(G)=18 iff delta(G)=18. If delta(G)>=19, then kappa(G)>=19.
No assertion of kappa=delta at other values is made.

Let A,B be disjoint, |A|,|B|>=2, |A|+|B|=25. A monochromatic A--B cut
would disconnect the other color after deleting the18 remaining vertices.
Its connected components lie inside A or B, so cannot include a24-vertex
component. This contradicts the classification. A larger pair of parts
contains such a25-vertex pair with both parts still of size>=2. Thus

    1 <= e_R(A,B) <= |A||B|-1

for every disjoint pair of parts of size>=2 and total>=25. The lower
bound is the clause OR(x_uv: u in A,v in B); the upper bound is the
clause OR(not x_uv: u in A,v in B). All other physical edges remain free.
These clauses are valid under every global good43 labeling, including
all h3873/h3887 tasks, without multiplying carriers or changing task IDs.
No complete packing task is claimed decided solely by this result.

## 6. Scope, provenance and evidence limits

This is a computer-assisted theorem with a short unformalized structural
proof and complete exact small enumeration. It imports the established
R(4,5)<=25 theorem but no graph-catalog completeness, SAT/UNSAT verdict,
numerical relaxation, or invalidated automorphism verifier. It is not an
external peer review or proof-assistant formalization. Finite fixture
checks validate translations; the proof supplies universal43-vertex scope.

Separator/independence-budget methods are classical; compare
[Beveridge--Pikhurko, On the connectivity of extremal Ramsey graphs](https://ajc.maths.uq.edu.au/pdf/41/ajc_v41_p057.pdf).
Their extremal-order hypotheses are not imposed here. We make no priority
claim for the method, the small attachment observation, or this numerical
classification. Relative to the durable campaign, the accepted h3393
review explicitly identified the12+13 obstruction as unresolved.

The principal's03:28Z boundary stopped the carrier/symmetry sequence at
h3887. That immutable result remains untouched. This pass instead closes
a complete global structural branch. It does not run a new physical
packing solver, reopen any fixed H92/H93 gluing or saved-parent repair,
or supply another denominator. All2,189,178 packing tasks remain undecided.
No good43, new Ramsey bound, or computational tractability claim results.
