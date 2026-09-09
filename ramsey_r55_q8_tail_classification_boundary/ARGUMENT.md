# Exact condition and failed coverage premise

Use red edges for graph edges. Let C be the complete original list of
546,356 Ramsey(4,4,11) core representatives. Let A be the set of all
isomorphism classes of Ramsey(4,5,23) graphs.

For a family L contained in A, define Sigma(L) to consist of the members of C
isomorphic to T minus B1 minus B2 minus B3, where T belongs to L, the Bi are
three pairwise disjoint independent four-sets, and the eleven remaining
vertices induce a Ramsey(4,4) graph. Take every such triple and use exact
isomorphism, not equality of degree sequences or other incomplete invariants.

The residual constraints of original task bo1-q8-r5-cNNNNNN are satisfiable
if and only if its core is in Sigma(A). Indeed, deleting the five prescribed
red K4 blocks from a full task leaves 23 vertices: the three prescribed blue
K4 blocks and the fixed core. Red maximality forbids a red K4 throughout
this tail, and the target forbids a blue K5. These give the forward map.
Conversely a displayed triple in T can be relabeled to the prescribed blue
blocks and a core isomorphism fixes the remaining labels, giving exactly the
residual graph. This converse asserts only residual satisfiability, not an
extension to 43 vertices or compatibility with a particular root matrix.

Thus C minus Sigma(A) would exclude named original q8,r5 tasks. A smaller
certified family L is also sufficient if one proves Sigma(A) is contained
in Sigma(L). Computing Sigma(L) without that containment provides positive
residual witnesses but cannot justify exclusion of any missing core. The
missing containment is substantive; no completeness flag or queue adapter
can supply it. No such containment or actual original-core intersection was
established in this pass.

## Primary-source boundary

McKay's author page supplies the complete 24-vertex class, but advertises
only selected extreme edge counts for smaller orders. Angeltveit--McKay,
Section 3.2, gives the complete 23-vertex class with at least 119 edges.
Appendix A reports about 9 times 10^10 total 23-vertex classes as a statistical
estimate, not an exact census. These sources do not provide the complete A.
See the direct links and provenance in SOURCES.json.

There is also a rigorous obstruction to universal extension from order 23
to order 24. A vertex of a Ramsey(4,5) graph has at most 13 neighbors: its
neighborhood has no triangle and no independent five-set, and R(3,5)=14.
The same paper's exact Table 1 gives minimum edge count 116 at order 24,
and respectively 1 and 76 order-23 classes with 101 and 102 edges. Adding a
vertex to either class would give at most 114 or 115 edges. Hence these 77
classes cannot be induced deletions of any Ramsey(4,5,24) graph. This imports
the published counts and standard Ramsey bound; no independent census is
claimed. The arithmetic checker verifies this deduction.

That obstruction concerns complete tail coverage. It does not prove that
any of those 77 classes contains an eligible three-block/core partition, or
that their core signatures are absent from all other tails. In particular,
it establishes no task exclusion and does not disprove a narrower signature
coverage theorem. Testing those alternative propositions would begin another
phase and was not done.

## Outcome

The proposed complete-catalog mechanism failed its coverage gate. No new
forced unit, split, density refinement, relaxation solve, catalog sweep or
candidate search was launched. All 546,356 q8,r5 tasks remain UNKNOWN; the
full original registry remains 518 excluded and 2,188,660 UNKNOWN. All frozen
artifacts and R55-1's 161 oriented q10 children remain untouched. The primary
source deductions and this logical interface are author work, not reviewer-1
approval. There is no novelty claim for the elementary extension bound.
