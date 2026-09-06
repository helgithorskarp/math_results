# Switching family of the saved Core186 fixture's 41-vertex induced graph

Let G be the explicit 43-vertex coloring in `parent.edges`, whose SHA-256
is `f034595d4f9fcb40cbf70acb6da75f0f7efda21719b1cc4bd052b75e0e927441`.
Delete original vertices 33 and 35 and relabel the remaining vertices in
increasing original order as 0..40. Denote the resulting red indicator by
H_uv. This is one particular 41-vertex induced graph; it is not the entire
family of extensions of the twelve-vertex minority core called Core186.

For arbitrary s in {0,1}^41, define a switched core by

    H^s_uv = H_uv XOR s_u XOR s_v.

The precise bounded task is to decide whether any such H^s has neither
a red nor a blue K5. Only s_0=0 is normalized. No C3 automorphism, degree,
empty signature, fixed neighborhood or selected minority-core condition
is imposed on the switched graph.

## Complete family and two-vertex corollary

Complementing all switch bits changes no pair, so s_0=0 loses no graph.
Conversely, comparing edges {0,v} shows that two normalized switch vectors
giving the same graph have equal s_v for every v. Thus there are exactly
2^40 distinct labeled switched cores. Attach two new vertices with all
2*41+1=83 pairs touching them free. This gives exactly 2^123 distinct
labeled 43-vertex graphs, without quotienting by isomorphisms.

If every H^s has a monochromatic K5, every graph in that complete extension
family has one, independently of its 83 new edge colors. Equivalently,
no Ramsey(5,5) graph can have an induced subgraph switching-equivalent
to H, including after arbitrary relabeling. This is a restricted-family
exclusion; it cannot prove a general 43-vertex exclusion or change a Ramsey
bound. If a K5-free switched 41-core is found, it is only a 41-vertex
witness, not a target 43-vertex graph.

## Distinction from the already excluded Paley class

For each unordered pair u,v, let t_uv be the number of other vertices w
for which H_uv XOR H_uw XOR H_vw=1. Under a switch, each of s_u,s_v,s_w
occurs exactly twice in this expression and cancels. Thus t_uv is
unchanged. Under relabeling, the multiset of pair counts is unchanged.

For the present H, pair {0,3} has t_03=15. Direct enumeration for Paley(41)
gives 410 pairs with count19 and 410 with count20, and no other count.
Therefore H is not switching-equivalent to Paley(41), even after
relabeling. The producer computes counts pair by pair and defines Paley
edges by square residues. The independent auditor counts odd triangles
and increments their three pairs, defining Paley edges by modular
exponentiation. Both complete histograms agree. This is an elementary
invariant test, not a general switching-isomorphism algorithm.

## Complete physical CNF

Variable v=1..40 denotes s_v, with s_0 fixed to zero. For any five-set Q,
desired monochromatic color c and anchor a=min(Q), put s_a=0 temporarily.
Every other spin is forced by its edge to a:

    s_v = H_av XOR c.

Test all ten switched pairs. If they do not all have color c, the desired
event is impossible. Otherwise this spin vector and its complement are
exactly the two vectors giving color c on Q. Keep those consistent with
the global s_0=0 normalization. For each kept vector, add the clause
whose falsification fixes its spins: literal +v for spin0 and -v for
spin1, omitting vertex0. These clauses have width4 or5.

Every forbidden coloring has a monochromatic five-set and violates its
clause. Conversely, falsifying any such clause creates its physical K5.
The complete formula is therefore equivalent to K5-freeness of H^s.
The independent auditor enumerates all32 switch assignments for every
one of the1024 labeled five-vertex base graphs, then reconstructs every
clause for all749,398 actual five-sets. It imports no generator.

## Compact physical proof certificate, if the decision is UNSAT

It suffices to retain any contradictory subset of the physical clauses;
completeness of a selected obstruction is not required. To check one
width4 clause, append physical vertex0 with spin0. A width5 clause already
names its five physical vertices. A positive literal is falsified by
spin0 and a negative literal by spin1. Directly evaluate all ten switched
input edges and require one common color. Every Ramsey core must therefore
satisfy every clause of the checked obstruction.

The standalone certificate checker combines this new physical decoder
with a small RUP/RAT kernel vendored verbatim from the teammate's Paley
package, with precise function identities in `imports.json`. This is
explicit code reuse, not a second independent implementation of DRAT.
It remains independent of the SAT solver, proof trimmer and full generator.

RUP means unit propagation under the negation of a candidate clause gives
contradiction, so the candidate is implied. Otherwise its first literal p
is a proposed RAT pivot. For each current clause D containing -p, check
RUP of C union (D minus {-p}). This suffices to preserve satisfiability:
if a model falsifies C, flip p to satisfy it. A clause D that could become
false has every other literal false before the flip, contradicting the
checked implication. This proof also permits fresh proof variables.
The clause database is a multiset; deletion removes one copy and weakens
the formula. A final empty clause must itself pass RUP, and no later
proof line is accepted. Induction through the trace proves contradiction.

The new physical checker reconstructs H directly from the pinned parent;
it never calls the Paley edge function. The vendored proof kernel has no
Paley-specific logic. An accepted compact trace removes the need to trust
the solver verdict, extraction procedure or full-formula completeness for
the exclusion. The written argument, physical decoder, proof kernel,
Python/parsing semantics, file identities and hardware remain trusts.
Checks by this author are not external peer review or formalization.

## Bounded operational contract

One complete switching-class CNF is generated and independently audited.
One Kissat4.0.4 invocation uses --time=300 --no-binary, with a330-second
wall guard. UNSAT must yield a checked compact physical certificate;
SAT must yield a directly verified complete41-vertex edge list; any other
termination is no conclusion. There is no second seed, longer-cap retry,
second deleted pair, or another switching class in this milestone.
Finish any certificate checking already underway, preserve reproducible
state, publish warranted evidence and yield before a new phase.
