# A sharp clique-capped packing threshold and a smaller complete good43 carrier

## Statement and provenance

Edges are red and nonedges blue. A good43 is a graph on 43 vertices with
neither a red nor a blue K5. All packings below are vertex-disjoint; edges
between different packed cliques are unrestricted.

**Theorem 1 (exact finite certificate).** Every red/blue coloring on 19
vertices has a red K5, a blue K4, or two disjoint red K4s. The threshold 19
is sharp. Equivalently, every graph on 19 vertices with no red K4 or blue
K5 has two disjoint blue K4s.

The upper-bound certificate uses all 640 published Ramsey(4,4,15) cores.
Catalog completeness is an explicit imported premise. The 640 extension
formulas have independently checked DRAT proofs; no solver verdict is
substituted for a proof check.

**Theorem 2 (complete carrier).** Every good43 has a representation in the
reviewed maximal-red-then-blue K4 carrier with either q=7,r=7 or
8<=q<=10, 5<=r<=q. All core indices in the retained strata remain allowed.
Thus the two complete strata q=7,r=5 and q=7,r=6 may be omitted from a
globally covering representative family. The cover has 16 macro classes
and 2,187,898 original-format task IDs, instead of 18 and 2,189,178.

Theorem 1 is **not claimed as a historically new Ramsey number**. Robert
Rubin's 2023 Princeton independent work, *Ramsey number of nK4*, section 4,
reports a unique 19-vertex graph avoiding red 2K4 and blue K4. His section 2
constructs that graph by tripling a vertex of the Paley graph of order 17
with red edges between the three copies. It contains a red K5. Thus the
reported classification already implies Theorem 1. That report supplies
neither the catalog nor checked traces for its classification; our proof
does not import that classification. The contribution here is an explicit
certificate for the needed corollary and its complete-carrier application.

Sources:

- [Rubin, 2023, original manuscript](https://www.pacm.princeton.edu/sites/default/files/rubin_robert-_final_iw.pdf).
- [McKay's Ramsey graph collection](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html),
  the section explicitly labeled “All Ramsey(4,4)-graphs”.
- [The actual order-15 catalog](https://users.cecs.anu.edu.au/~bdm/data/r44_15.g6).
- [Reviewed maximal-packing cover](../ramsey_r55_global_maximal_packing/PROOF.md)
  and [independent acceptance](../ramsey_r55_global_maximal_packing_review1/README.md).
- [Whole-block ordering](../ramsey_r55_maximal_block_order/PROOF.md).
- [Preceding all-q exchange normal form](../ramsey_r55_core_exchange_normal_form/PROOF.md).

## Complete reduction for Theorem 1

Suppose G is a counterexample on 19 vertices. Since R(4,4)=18 and G has
no blue K4, choose any red four-clique B. Let C=V(G)\B. The graph on C
has no blue K4. It also has no red K4, since such a clique would be
disjoint from B. Consequently C is a Ramsey(4,4,15) graph.

Relabel C to one of the complete catalog's 640 representatives. Label B
arbitrarily as 0,1,2,3. No condition is imposed on an automorphism of G,
on its degrees, or on the ordering of contacts. All 60 B--C edges remain
free. Therefore every counterexample has a satisfying assignment of one
of the following 640 formulas. The converse also holds.

For a fixed core adjacency matrix A, let x(w,v)=1+15w+v, with
0<=w<4 and 0<=v<15. A positive literal means that the B--C edge is red.
The fixed internal edges of B are red and those of C are exactly A.
The formula is the conjunction of three families:

1. For each red core clique T of size k, 1<=k<=4, and each B-subset S
   of size 5-k, forbid all edges between S and T from being red. This
   excludes every red K5. A core-only K5 is impossible because C has
   no red K4; a block-only K5 is impossible because |B|=4.
2. For every blue core triangle T and w in B, require at least one red
   edge from w to T. This excludes every blue K4: it cannot use two
   vertices of the red block and cannot lie entirely in C.
3. List every possible red K4 that uses k block vertices and 4-k core
   vertices, 1<=k<=3. Its core part must be a red clique. For every
   pair of disjoint listed four-sets, forbid the union of their two
   red-contact guards. These clauses exclude all pairs of disjoint red
   K4s. A pair involving B itself would need a red K4 wholly in C,
   which is impossible. Every remaining pair occurs in the list.

There are no auxiliary variables or symmetry-breaking constraints.
Identical clauses and repeated literals are removed, and the result is
sorted deterministically. These operations preserve satisfiability.

`encode.py` implements this decomposition. The independent grounder
`reference.py` instead enumerates all four- and five-subsets of the full
nineteen-vertex set, substitutes fixed edges into clique guards, and
forbids every pair of disjoint possible red fours. All 640 canonical
clause lists agree exactly. The formulas contain 27,999--41,875 clauses,
22,150,762 in total. All 640 are UNSAT, with each standalone CaDiCaL
1.9.5 proof checked against its original DIMACS input by DRAT-trim.
The individual hashes and coverage indices are in `CERTIFICATES.json`.
This proves the upper bound, conditional on catalog completeness.

## Sharpness and necessary hypotheses

Take the order-17 Paley graph, with red differences the nonzero quadratic
residues modulo 17. Replace vertex 0 by two red-adjacent vertices with
identical contacts to the other 16 vertices. This gives 18 vertices.
The original Paley graph has no monochromatic K4, verified literally by
the included control. Every red K4 of the enlarged graph must contain
both copies of 0, so two cannot be disjoint. A red K5 would require a
red triangle among their common neighbors, producing a red K4 in the
original graph. A blue K4 would map injectively to one in the original
graph. Both are impossible.

The literal control finds 12 red K4s, no red K5, no blue K4, and no
disjoint red-four pair. Its exact physical edge word is in `CONTROLS.json`.
This proves sharpness at 18 without an imported classification.

Tripling 0 instead gives the prior 19-vertex construction, with no blue
K4 and no two disjoint red K4s but 12 red K5s. The no-red-K5 hypothesis
in the packing conclusion is therefore essential.

The [archived good19 counterexample](../ramsey_r55_good19_packing_bridge_counterexample/README.md)
to the uniform two-monochromatic-K4 shortcut has 24 red K4s and 12 blue
K4s. It does not satisfy the K4-free-color hypothesis here. Its explicit
graph is checked as a scope control; none of its historical searches is
restarted. Theorem 1 does not repair the false unrestricted good19 lemma.

## Whole-stratum physical redirect

Start with any inherited q=7 carrier packing with r=5 or r=6. Write
R for its red blocks, L for its blue blocks, and C for its order-15
Ramsey(4,4) core. The entire residual V(G)\union(R) is red-K4-free.
Choose any B in L. The induced graph on B union C has 19 vertices,
no red K4, and no blue K5. By the color-reversed Theorem 1 it has two
disjoint blue four-cliques B1,B2.

Retain every red block and every other blue block. Replace B by B1,B2
and set C'=(B union C)\(B1 union B2). The new core has order 11.
The union of blue blocks and core is unchanged, so red maximality is
unchanged. Exhaust any remaining blue K4s in C'. This yields q>=8,
with the same r. At most ten blocks can fit on 43 vertices. The final
core is again Ramsey(4,4), so its order is 11,7, or 3.

All of this is an operation on the **same physical graph**. Only its
partition and final labels change. Exhaustive enumeration of the at
most 3,876 four-subsets of B union C finds B1,B2. For an arbitrary
non-Ramsey carrier input, the receiver may instead return a literal
blue five in that nineteen-vertex set. No good43 can take that return.

After core catalog lookup, root-column ordering and equal-color block
ordering, the receiver gives the exact original-format destination ID,
all 903 physical edge bits, and the full new-to-old permutation.
No sampled core, bounded-degree profile, or graph automorphism is used.

## Compatibility with the preceding normal form

The preceding normal form terminates by increasing the lexicographic
potential (r,q,e_red(C)). It combines red two-edge augmentations and
core-vertex exchanges with maximality repair. Red repair can increase r
while decreasing q, so simply running the old descent once after the
new redirect is insufficient to exclude a mixed q=7 endpoint.

The new blue augmentation increases q while retaining r. Alternate it
with the old descent whenever the current packing has q=7,r<7. Every
nontrivial move still increases the same potential. For good43 the
possible triples lie in

    7 <= q <= 10,  5 <= r <= q,  0 <= e_red(C) <= binom(43-4q,2).

This contains

    3*106 + 4*56 + 5*22 + 6*4 = 676

states, hence at most 675 moves occur. The endpoint obeys every old
terminal exchange rule and has q=7 only when r=7. This proves the
combined representative theorem. Its use of the preceding descent is
a written mathematical dependency, not independent external review of
that package.

## Exact carrier effect and remaining obstruction

For each removed stratum the complete core range is [0,640).
`CARRIER.json` retains [0,640) at q7r7, [0,546356) for all four q8
strata, [0,362) for all five q9 strata, and [0,4) for all six q10
strata. Thus

    640 + 4*546356 + 5*362 + 6*4 = 2,187,898.

The deleted task IDs represent 0.0584694% of the original registry.
Their exact unfiltered ordered pair/star carrier size is

    640 * (S(7,5)+S(7,6)),

where S is the inherited whole-block-order count. It is about
3.7178866e-16 of that unfiltered labeled carrier. The complete integer
comparison is supplied. This small fraction is not hidden by the
macro-class reduction, and no runtime gain is asserted. No multiplication
of this fraction with the previous normal-form retention bound is valid.

Theorem 2 is a statement about a smaller **globally covering union**.
It does not assert that either removed old task is UNSAT. Their physical
graphs may have representatives in retained tasks. All original verdicts
remain unchanged; original-task proof accounting requires the appropriate
global redirect argument rather than appending an unsupported clause.

There is also a precise structural boundary for further work. In any
good43, every inclusion-maximal red-K4 packing has at least five blocks
by R(4,5)=25. If it has five blocks, its red-K4-free residual has order
23: remove one blue K4 using R(4,4)=18 and use Theorem 1 on the other
19 vertices to obtain two more. If it has six blocks, Theorem 1 gives
two blue blocks directly. Either case produces at least eight blocks
without changing the red packing.

Consequently, a good43 has **no** red-maximal representative with q>=8
if and only if every maximal red-K4 packing has exactly seven blocks
and every corresponding 15-vertex complement is Ramsey(4,4). This is
a whole-class obstruction, not a claim about every labeling of the
remaining q7r7 tasks. In the stronger hypothetical class whose maximum
monochromatic K4 packing number is seven, the statement holds in both
colors. Every same-color partial K4 packing then extends to seven
same-color blocks. Red and blue seven-packings intersect in at least
13 vertices, and each red/blue block pair intersects in at most one.
These follow respectively from 28+28-43=13 and the incompatible color
of an edge shared by two vertices. No contradiction or practical closure
of that remaining class is claimed here.

The exact value of R(5,5) and the q7r7 whole-stratum question remain open.
The q8 carrier remains the dominant task stratum and receives no new
restriction from this pass alone.

## Trust and reproducibility

The finite upper bound trusts the published order-15 catalog's
completeness, the written reduction, Python integer/byte semantics,
DRAT-trim's soundness, its C compiler, and ordinary hardware. Membership
of every catalog record and every grounded formula is checked;
catalog completeness is not regenerated. Solver correctness is not
needed beyond production of traces accepted by the checker. This is
not a proof-assistant formalization or an external peer review.

The good43 application additionally imports the reviewed carrier bridge,
R(4,5)=25, R(4,4)=18, and the completeness of the order-3,7,11 catalogs
used for destinations. The combined normal form imports the preceding
written exchange proof. The local lemma itself does not use R(4,5)=25,
the good43 degree/edge windows, or any historical automorphism result.

The saved complete run occupies 632,091,299 CNF bytes and 137,751,329
DRAT bytes, plus logs. These remain in researcher scratch; the public
package contains deterministic source, compact per-case hashes and
controls. See `README.md` for exact reproduction commands and versions.
