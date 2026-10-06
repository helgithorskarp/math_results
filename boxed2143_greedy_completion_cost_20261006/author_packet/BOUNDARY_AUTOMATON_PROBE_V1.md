# Falsifiable boundary-statistic quotient

Quinn, workday3,2026-10-05. Author exploratory proof/test, not independently
checked or part of the accepted publication. The full target410 is fixed.

An external leaf of a maximum Cartesian tree denotes a gap. Write its
root-to-leaf directions L/R. The checked shape blocker rule implies that
the gap is legal iff its word has no RR after an earlier L. Indeed a blocker
minimum j is a right child with an ancestor on its right, so its root-to-node
word has an earlier L and ends in R. Its forbidden gaps j+1,...,R are exactly
the external leaves of j's right subtree, including the right boundary leaf.
Their paths append another R. Conversely any RR after L supplies exactly
such a node j and ancestor/boundary. External boundary gaps and empty trees
are included, not discarded.

Let A(T) count accepted external words starting before any L has appeared;
B(T) count accepted words after L has appeared and the previous letter is L;
C(T) count accepted words after L has appeared and the previous letter is R.
For the empty tree A=B=C=1. For a node T=(L,R), direct automaton branching gives

    A(T)=B(L)+A(R), B(T)=B(L)+C(R), C(T)=B(L).

Thus A(T) is the exact number of legal maximum gaps. These are uniform author
identities deduced from the accepted tree rule, not finite extrapolation.

Specific quotient hypothesis Q: for ANY two shapes T,U of the SAME size with
the same (A,B,C), the MULTISET of (A,B,C) of their legal insertion children
coincides, including transition multiplicities. Every shape is realized by
a classical2143 avoider: recursively assign all left ranks above all right
ranks, put their maximum between them, and induct on the first<last
inequality for any mixed occurrence. Hence a shape collision is a real
avoiding-history collision, not an out-of-domain test.

If Q holds, summing weights in each (A,B,C) fiber gives an exact polynomial-
state recurrence (each coordinate<=n+1). This does NOT itself prove a growth
bound: multiplicities would still need a uniform analysis. The potential
full-target route is to derive a closed succession rule and then prove an
exponential bound or a persistent family with unbounded roots. No such
asymptotic step is established here.

First decisive test: enumerate every binary shape by size, compare the
external-leaf rule with the accepted complete gap set, and stop at the first
same-size/statistic child-multiset collision. Retain both explicit avoiding
representatives and all child statistic multiplicities. Do not expand a
favorable census in place of an all-size proof.
