# Theo's separate full partial review of Quinn529

Author: literature-researcher-3. Checker: literature-researcher-4.
Verdict: accept the entire uniform ID/retention representation argument,
the conditional reciprocal-to-growth bridge, and the complete domain-safe
finite reciprocal counterexample. Both independent replays have finished.
This is internal team checking, not external peer review or novelty approval.
The full agreed target410 remains unsolved. No earlier acceptance is extended.

Frozen manifest138bcbd7676e82fd3c5eea0d16afa0394e617871f8951b0cea90b29017134825;
proof76dbd25634c83363c82d36e4486e76f59aa998ae14d56da262b897df1a0f0968;
optimized code d2b2b8f4a1289023151d4f16710c438e0625892585ac152bbe5034da98427170;
certificate8fe06193ed0e7db64b0249215ed70e23862a9ac55b77a74887a0ff8251f4c5a3.
All15 named files were frozen and byte-verified before the independent run.

## Uniform representation and counting argument

The author storage assigns a nonzero ID to each ordered pair of existing
child IDs, reserving0 for the empty shape. Child construction precedes parent
construction. Induction gives exactly one ID for each allocated shape, with
no cycles, and size1+left size+right size. Neither ID values nor allocation
order are mathematical state coordinates.

For each traversed node j, its flag says whether its last edge was right;
the carried right boundary is the nearest ancestor on its right. Going left
sets that boundary to the current root, and going right preserves it. Thus
the eligible flags give exactly the already checked blocker nodes. The mask
((1<<(R-j))-1)<<(j+1) excludes bits j+1 through R, including the right
boundary gap. The finite complement is restricted to the n+1 genuine gaps.
This computes the old legality predicate; it asserts no summary-statistic
lumpability and does not depend on the later boundary-automaton hypothesis.

The recursive split is the original inorder cut in the two child cases.
Replacing its child shapes by their canonical IDs is a representation change,
not a recurrence change. At a rank-history state(i,T) after total ranks have
been inserted, j=total-i ranks have come from beta. The next alpha and beta
ranks have unique required positions G_alpha(i) and i+G_beta(j), respectively.
Each legal insertion therefore gives exactly the old state edge. Two possible
origin sides remain distinct rank histories even if their child states
coincide; their integer weights are added. After all2m ranks, the final root
at cut m is allowed exactly when its corresponding legal bit is set. This
recovers the complete fixed-pair count, not a heuristic tree-state count.

Retention traverses the entire subtree closure of all current weighted roots.
Its postorder constructs the same shapes in a fresh canonical ID store,
with a bijection from retained old shapes. Translation preserves(i,T) and
its weight; equal translated states cannot arise from different shapes.
Cached legal masks are shape functions and survive translation unchanged.
An obsolete shape outside this closure has no current weighted history.
Any later split or insertion can reconstruct its needed shape canonically
from the retained current children. No state weight is lost by dropping the
obsolete cache. Cache sizes and collection schedules are implementation
details, independent of the mathematical recurrence.

The canonical level word reconstructs each tree as dot/ordered-parenthesis
text. Sorting by i and that text and hashing the exact weight is independent
of allocation IDs or collection order. The code's reindexing cardinality
check and exact integer arithmetic agree with these arguments. Python and
ordinary hardware, not a proof assistant or solver proof log, are the
remaining computational trust base.

## Input domain and conditional growth bridge

The family P_h,Q_h is the uniformly domain-proved family in accepted498.
My own implementation constructs P6 using its earlier seed function and
constructs Q6 by lifting the small seed's rank1 to1, its other ranks by+31,
and putting the shifted small seed on the right of63. The actual63-entry
arrays are checked against the author's arrays, my strict rectangle checker
and my nearest-greater parent reconstruction. They must both avoid and have
the perfect height6 maximum tree. A numerical pair outside this domain
would not refute the quantified reciprocal hypothesis.

If R held for every ordered pair in F_h, AM-GM would give
N(alpha,beta)+N(beta,alpha)>=2*2^((m_h-1)/2). Summing over every ordered
pair, including diagonal pairs, makes the two sums equal by reindexing.
The exact join identity then gives
|F_(h+1)|>=2^((m_h-1)/2)|F_h|^2. Taking base2 logarithms and using
m_h=2^h-1 yields b_(h+1)>=2b_h+2^(h-1)-1. The elementary induction
b_h>=2^(h-2)(h-3)+1 starts at h=1 and gives b_h/m_h tending to infinity.
Thus the proposed uniform reciprocal hypothesis really would prove the full
negative target. Neither a few favorable products nor its failure proves
anything about the full-population average required by that join identity.

## Independent implementation and required exact evidence

check_quinn_reciprocal_join.py imports no author executable. It uses canonical
shape strings directly as state keys, without IDs, interning or reindexing.
Legality comes from my separately reconstructed external-leaf automaton in
the distinct534 review. The state-language proof is uniform; using it here
does not assert the false ABC child-multiset quotient. Cuts use an iterative
zipper: locate the external gap, collect its sibling substrings up the path,
and rebuild prefix and suffix from the bottom upward. Thus the new-root
transition has a different representation and a different implementation
from the author's recursive interned split and ancestor bitmask.

The run first checks all626 shapes and4707 cuts through7 against actual
new-maximum words and direct greater-neighbor gap geometry. Every weighted
level, peak-state count, transition count and final count of the ten prior
forward/transposed family controls through31 must match. Five tiny pair
baselines are also checked directly from the boxed definition. Each new
m63 orientation then must match all126 canonical level records, without
truncation. The independent representation retains only current-level
geometry caches. State200000, time600seconds per orientation and conservative
memory1400000KiB caps certify incompleteness if reached; they do not alter
the fixed team resources. The exact replay JSON records the completed scope.

## Scope and preserved failures

The two earlier capped author runs remain preserved and certify no count.
No later all-pair minimality, population-average obstruction, full-target
solution, weakened-coefficient growth claim or external peer review is
accepted. The completed reproduction rejects the exact uniform R only.
It does not reject a compatible subpopulation or a total-population entropy
invariant. Existing public39045c3 and graph originals retain their old scope.

## Completed exact reproduction

The actual P6,Q6 inputs have length63, avoid by my literal rectangle checker,
and have the perfect height6 shape by nearest-greater reconstruction. The
independent counts are N(P6,Q6)=751802 and N(Q6,P6)=46579123. Every one of
126 canonical weighted levels in each orientation matches the author,
including each state count and full stream hash; both complete transition
totals and peak states also match. Their product35018277829646 is strictly
less than4611686018427387904=2^62, so this actual pair in the quantified
avoidance/perfect-tree domain refutes R.

The same independent string implementation reproduces all228 complete levels
of the ten old forward/transposed controls through31, plus five literal
small-pair baselines. Its own626 shape/4707 cut controls pass. The complete
run took370.347seconds and peaked at178608KiB Linux RSS, one process/thread;
individual orientations took217.374 and142.224seconds, below their600second
caps. No state, time or memory cap was reached. The independent representation
has no interned-node cap because it has no interned-node storage; its separate
state/memory caps retain the unchanged team resource restrictions.

Durable evidence: check_quinn_reciprocal_join.py,
quinn-reciprocal-join-reproduction.json and
QUINN_RECIPROCAL_JOIN_REVIEW_MANIFEST.json. The manifest pins the complete
reviewer implementation, all own imported dependencies and the frozen author
packet manifest. Existing498 scope, source and graph originals are unchanged.
No all-pair minimality is claimed. The result is an exact failure of the
specified sufficient mechanism, not an answer to the full growth decision.
