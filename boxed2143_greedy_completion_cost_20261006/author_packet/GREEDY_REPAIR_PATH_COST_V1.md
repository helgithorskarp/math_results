# Exact greedy repair cost from one external tree path

Quinn / literature-researcher-3,2026-10-06. New AUTHOR uniform lemma and complete
finite controls, pending a different researcher's ENTIRE check. Full target410
remains fixed and UNSOLVED. No expectation, density or useful completion-size
theorem is claimed. This scope is excluded from every previous public/graph
packet and does not inherit534/592 acceptance.

## Statement and explicit dependencies

T is the maximum Cartesian shape of a boxed2143-avoiding current permutation.
An external leaf in inorder represents its gapg. Its root-to-leaf direction word
w usesL/R. Accepted534 says that g is legal exactly when w contains no consecutive
RR after an earlierL. Define

    D(w) = #{j : w_j=w_(j+1)=R and some i<j has w_i=L}.

If g is illegal, the accepted592 repair policy inserts a new auxiliary global
maximum at the RIGHTMOST legal gapk<g, updates the desired original gap to g+1,
and repeats until it is legal. Then the number of auxiliaries is EXACTLY D(w),
where w is the initial gap path. This is a shape/gap statement independent of
the labels or original/auxiliary tags; an original-gap interpretation merely
selects which leaf to use. The algorithm does not insert the next original
maximum until repair is over.

The proof uses only accepted534's exact leaf-language criterion, accepted467's
inorder split update for maximum insertion, and the separately checked592
repair definition. It supplies a new all-size bridge among them, not a finite
extrapolation. Each auxiliary is inserted legally, preserving current avoidance.

## One repair removes exactly one counted pair

Assume D(w)>0. Let the FIRST offending pair give the factorization

    w = q R R v,

where q contains at least oneL. The prefix qR has no offending pair. Let j be the
node reached by qR, and let B=j.left, C=j.right. The target gap is in C. Every
external leaf of C has prefix qRR and is therefore illegal. The leftmost leaf of
B has path qR followed only byL's (including the empty-child edge), so it is legal.
All leaves of B precede all leaves of C in inorder. Hence the globally RIGHTMOST
legal leaf before the desired gap is a leaf of B: later leaves before the target
are all inside C and illegal, while B contains at least one legal leaf. This
includes B empty, whose one leaf is the gap immediately before node j.

Insert the auxiliary maximum at that leaf k. The new maximum becomes the root,
and the desired gap is on its right, in the suffix part of the old tree's inorder
split. Along the old path from its root to j, everyR step has an ancestor whose
root lies BEFORE the cut and so is removed from the suffix path; everyL step has
an ancestor whose root lies AFTER the cut and so stays on the suffix path, with
the direction to j stillL. Node j itself lies after the cut in its left subtree,
so stays. Nodes along the cut path strictly inside B lie before the target path's
j-right branch and do not occur on the new path to the target. Its C-subtree and
the suffix v of that path are unchanged.

If ell is the number ofL's in q (ell>=1), the NEW desired-gap word is therefore

    w' = R L^ell R v.

The leadingR is the new auxiliary root's right edge. This word has no offending
pair in its displayed prefix. Offending pairs entirely in v, and a possible pair
between its precedingR and the first letter of v, are exactly the pairs AFTER
the first offending pair in w. Both prefixes have already seen anL before v.
Thus D(w')=D(w)-1, without any assumption about the off-path subtree shapes.

Inductively each repair drops D by one. The leaf-language criterion says repair
stops exactly at D=0. Thus it performs exactly the initial D(w) auxiliaries.
When D(w)=0 initially it performs none, as required. The chosen gap's monotone
position/distance bound592 remains valid but is not needed for this exact cost.

## Definition-level controls, not the all-size proof

repair_path_cost_probe_v1.py enumerates ALL626 binary shapes of sizes0..7 and all
4707 external leaves/gaps, in increasing size, canonical tree word, gap order.
It computes D directly from each external word. Separately it runs the greedy
repair via the previously checked complete legal-gap/split functions, with an
explicit classical2143-avoiding representative for each initial shape. Every
actual auxiliary child is also checked by the complete literal boxed definition
and its Cartesian shape. No mismatch occurs. Source dependencies kernel.py and
tree_dynamics.py retain their original exact hashes.

The canonical stream contains shape|gap|path|predictedD|actualcost for every case:
SHA25607841e7f30461c63aa40349d4ef55c03b4e6acd6a6099c32606c891c8bc82982.
Author runtime0.563seconds/Linux peak18880KiB, one CPython3.11.2 process, standard
library/native threads1. It does not test every heap labeling; the label-free
uniform lemma plus the previously accepted state quotient justify that domain.
Same-author controls and old dependencies are not a separate independent check
of the new proof or source. The complete result is repair_path_cost_probe_v1.json.

## The missing FULL-target obligation

For a uniform source permutation onm original ranks, its next-rank position is
uniform among the original gaps, conditional on the preceding source order and
deterministic history. Auxiliary CURRENT gaps do not receive a uniform law.
Let T_n and its tagged original gaps describe the current completion after n
original ranks. The exact remaining statistical obligation becomes

    E[sum over n<m of D(path of the chosen ORIGINAL gap in T_n)]
        = o(m log m).

This plus the m original points gives expected completion length o(m log m),
and Markov gives a fixed positive fraction of inputs with a useful length bound.
The separately checked relaxed entropy bridge592/580 would then establish the
full negative answer. The source-conditioning discussion608/614 is separate
from this path proof; its whole new check remains with Theo's existing Lyra pair.
No all-parent conditional cost bound is assumed: the rare descending-parent
family gives linearly manyRR violations and does not reject an unconditional
bound or an amortized potential.

The expectation is currently UNPROVED. A concrete next analytic route is a
potential/drift inequality for the distribution of these countedRRedges under
uniform ORIGINAL insertion positions, retaining their tagged gap weights. A
uniform all-parent constant bound is already obstructed; favorable small input
means or a tree-state census cannot replace this distributional argument. This
new exact cost formula is a tool toward the same full target, not its solution.
