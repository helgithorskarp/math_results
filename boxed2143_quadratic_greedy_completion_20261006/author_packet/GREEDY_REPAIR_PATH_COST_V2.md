# Exact greedy repair cost and original-gap blocker mass

Quinn / literature-researcher-3,2026-10-06. Version2 AUTHOR uniform lemmas and complete
finite controls (version1 prose/source/results preserved), pending a different researcher's ENTIRE check. Full target410
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

## Exact blocker-count corollary

For an eligible minimum node j, accepted444/467 assign the unique nearest-
greater blocker interval [j+1,r(j)] in zero-based gap coordinates. Accepted534
identifies the external leaves in that interval with the secondR of one RR
pair after an earlierL. Distinct counted pairs have distinct minimum nodes.
Thus the correspondence is a BIJECTION, not merely an existence equivalence:

    D(path(g)) = #{eligible j : j+1 <= g <= r(j)}.

The accepted kernel's exact new-maximum occurrence bijection further identifies
this count with the number of literal boxed2143 occurrences that an unrepaired
new maximum at g would create in the avoiding parent. These hypothetical
occurrences are not inserted by the greedy algorithm. The cost theorem says
its actual number of legal auxiliary insertions equals this INITIAL count.

## Definition-level controls, not the all-size proof

The preserved repair_path_cost_probe_v1.py/.json enumerates ALL626 binary
shapes of sizes0..7 and all4707 external gaps in increasing size, canonical tree
word and gap order. It computes D and executes the actual greedy shape/kernel
repair on an explicit classical2143-avoiding representative. Its occurrence
function is the accepted OPTIMIZED complete oracle, NOT a new literal quadruple
scan. The earlier version1 prose and chat641 erroneously described this scope
as literal; both are preserved, and this correction is explicit. No executed
version1 source/result has changed. Its canonical shape|gap|path|D|cost stream
is SHA25607841e7f30461c63aa40349d4ef55c03b4e6acd6a6099c32606c891c8bc82982.

The separate repair_path_cost_literal_controls_v2.py now compares FULL literal
quadruple occurrence sets for ALL4707 hypothetical maximum children and every
one of1380 actually executed auxiliary children, as well as the626 initial
representatives. Every hypothetical occurrence count equals D, and every actual
auxiliary child avoids. Blocker interval coverage also equals D in every case.
All old cost/shape stream fields match exactly; the new full-evidence stream is
SHA2563fb17c7423b137fb55799285cf40ca0522c6b688bdc6329f631168c22b54a25b.
Its complete result is repair_path_cost_literal_controls_v2.json, with exact
source hashes. Runtime0.742seconds/Linux peak18896KiB, one CPython3.11.2 process,
standard library/native threads1. It imports same-author path/repair helpers
and the existing definition-level direct_occurrences function; this is not an
independent team check. It does not enumerate every heap labeling. The label-
free proof and accepted quotient supply that domain, subject to the new whole
proof check. Original historical dependencies retain their exact hashes.

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
full negative answer. The source-conditioning claim608 is now separately ENTIRE-checked by Lyra632
and acknowledged638, distinct from the earlier limited discussion614. That
acceptance supplies its exact conditioning scope, not acceptance of these new
path/cost lemmas.
No all-parent conditional cost bound is assumed: the rare descending-parent
family gives linearly manyRR violations and does not reject an unconditional
bound or an amortized potential.

Equivalently, for the deterministic tagged completion C(sigma) of a source
sigma in S_n, define its ORIGINAL-gap blocker mass

    B(C(sigma)) = sum_(eligible current nodes j)
                     #{g in ORIGINAL gaps : j+1 <= g <= r(j)}.

Each original gap is before an ORIGINAL point or is the final gap; no weight
is assigned merely because a gap precedes an auxiliary point. Original and
auxiliary minimum nodes are both included if eligible. The original-gap law
and the new bijection give the EXACT finite equality

    E[total auxiliaries on uniform S_m]
       = sum_(n=0)^(m-1) (1/(n+1)) * E_(sigma uniform S_n)[B(C(sigma))].

The completion history on n ranks depends only on sigma, so this equality
retains all n! source histories with their multiplicities. It does not replace
that law by a uniform tree-shape law or condition away expensive parents.
Proving that displayed sum is o(m log m) is the concrete FULL-target claim in
this lane. A sufficient stronger bound E[B(C(sigma))]=O(n) would give O(m)
expected auxiliaries, but neither bound is currently proved or asserted.

The expectation is currently UNPROVED. A concrete next analytic route is a
potential/drift inequality for the distribution of these countedRRedges under
uniform ORIGINAL insertion positions, retaining their tagged gap weights. A
uniform all-parent constant bound is already obstructed; favorable small input
means or a tree-state census cannot replace this distributional argument. This
new exact cost formula is a tool toward the same full target, not its solution.
