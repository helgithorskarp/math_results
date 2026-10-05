# Reverse tree states and a failed balanced-join growth mechanism

Quinn / literature-researcher-3, 2026-10-05. New author partial arguments and
exact certificate awaiting Theo's independent check. They are separate from
the accepted tree quotient467 and the first public kernel/site packet477.
The full target410 remains unsolved. A specific sufficient uniform bound is
refuted here if the exact count below is reproduced; no weaker replacement
bound is silently treated as the target.

## 1. Incoming states have a boundary-spine grammar

Let a child maximum-tree shape be T=(L,R), and let g=|L| be its root's gap
before that maximum was inserted. A possible parent has prefix shape L and
suffix shape R. Standard Cartesian merging chooses its roots, in decreasing
priority order, from L's right spine and R's left spine. Record choices by a
word of letters L,R. All merges correspond bijectively to shuffles of those
two spines, preserving the order of each spine. The recursive merge choices
are (L.left, merge(L.right,R)) for a leading L, and
(merge(L,R.left), R.right) for a leading R. Nodes not on those boundary spines
are kept in their original subtrees. Conversely a prefix/suffix merge's root
must be one of these two maxima, and induction recovers its unique word.
Inorder positions distinguish words and parent shapes; no two different words
produce the same shape. Empty sides are included.

The new-root gap g is legal exactly when the descending-priority merge word
has no consecutive LL after any R has already occurred. For proof, a blocker
across g must have its minimum node j on L's right spine: any other L node has
a right greater ancestor still in L, whose blocker interval ends before g.
The first spine node has no greater predecessor within L. For any later
node j, its nearest greater predecessor is the preceding L-spine node l.
Its nearest greater successor, if any, is the deepest R-left-spine node
having value greater than j. Such a successor has value greater than l
exactly when no R priority lies between l and j and at least one R priority
precedes l. In the merged descending-priority word, that is precisely an LL
adjacency after an earlier R. If an R lies between the two L priorities, the
closest greater successor is below l and the kernel's comparison fails. If
no R has yet occurred, there is no greater successor. These cases prove both
directions. A node to the right of g cannot block insertion there.

Thus the checked weighted state recurrence has the equivalent incoming form

    w(())=1,
    w((L,R)) = sum w(U) over admissible boundary-spine merges U of L,R.

Every U has exactly one distinguished cut g and is a legal parent state;
the already checked unique maximum-deletion history supplies the weights.
Standard Cartesian merging is prior structure; no novelty claim is made.

Author controls compare all66197 merge candidates and every full weighted
state through size10 with the accepted forward rule. The proposed grammar
agrees; merge stream SHA256
f21ce999947f2c14955442e1e26a139ec53ba4648cf1a9132a23ee65d2d148b5.
The balanced size15 fiber is790086, later separately recovered by6,345,768
literal-definition joins. These finite checks are not the arbitrary-size
proof or independent team review.

## 2. A specific sufficient bound that would solve the full target

Let T_h be the perfect ordered binary tree of height h, with
m_h=2^h-1 nodes, and let F_h be the full boxed2143-avoiding fiber of T_h.
For alpha,beta in F_h and an m_h-subset S of[2m_h], form

    J_S(alpha,beta)=lift_S(alpha), (2m_h+1), lift_(S^c)(beta),

where lift replaces ranks1,...,m_h by the sorted selected values. Let
N(alpha,beta) count the subsets S for which this word avoids boxed2143.
Every avoiding permutation with shape T_(h+1) decomposes uniquely this way:
its maximum is the middle root, and its two contiguous position halves avoid
the boxed pattern, because points outside their horizontal intervals cannot
block an occurrence. Standardizing those halves preserves emptiness, and S
is recovered as the left half's value set. Consequently

    |F_(h+1)| = sum_(alpha,beta in F_h) N(alpha,beta).

The proposed uniform hypothesis H was

    for every h>=1 and alpha,beta in F_h,
    N(alpha,beta) >= 2^((m_h-1)/2).

It would suffice for the full negative growth answer, not just a narrower
fiber theorem. Write b_h=log2|F_h|. H would imply
b_(h+1)>=2b_h+2^(h-1)-1. Starting b_1=0, induction gives
b_h>=2^(h-2)(h-3)+1, whose ratio to m_h tends to infinity. Since
a_(m_h)>=|F_h|, the agreed limsup would be infinite. This is a conditional
bridge only; H is the statement tested and rejected below, not an assumption
used elsewhere.

Full literal tests on both size3 fiber words give minimum N=8. Tests on all43
size7 fiber words and all1849 ordered pairs/all3432 subsets per pair give
minimum N=37, exceeding H's threshold8. The sum is790086, agreeing with the
reverse state calculation at size15. These favorable finite values were not
promoted to a uniform conclusion.

## 3. Exact fixed-pair counting without enumerating all rank subsets

For arbitrary equal-length alpha,beta, define G_alpha(i) as the insertion gap
of rank i+1 in the restriction of alpha to ranks<=i+1 after deleting i+1.
This gap is the number of smaller source ranks before i+1 in alpha. Define
G_beta(j) analogously.

Build a rank partition by choosing a word of m letters A and m letters B in
ascending value order. At the state (i,j,T), i A ranks and j B ranks have been
inserted, in the fixed positional layout alpha_(<=i) followed by beta_(<=j).
The next A rank inserts the new maximum at G_alpha(i); the next B rank at
i+G_beta(j). Each gap and updated i,j depends only on the state, not on a
forgotten priority assignment. The accepted tree quotient gives its exact
legality and child shape. Start (0,0,()) with weight1. Propagate each weight
at each permitted A/B step, retaining all multiplicities. At (m,m,T), retain
the weight only if gap m is legal for the final new maximum2m+1.

This counts N exactly. Every rank subset corresponds to one ascending A/B
word and one fixed source-layout permutation, and both are recoverable from
the result's left values. Conversely every valid final word has every
maximum-deletion ancestor avoiding, so no counted valid subset is pruned.
Legality/state updates are shape functions, so histories with identical
(i,j,T) have identical future choices and may be merged by summing weights.
This statement includes arbitrary nonavoiding inputs, which correctly give
zero; using zero as a counterexample to H additionally requires both inputs
actually lie in F_h.

`fixed_pair_join_dp.py` implements this exact recurrence with arbitrary Python
integers, deterministic state-stream hashes, one process/thread, and a
50,000-state-per-level cap. Reaching the cap raises an explicit incomplete
failure, never a count. The present run completed without reaching it.
Its10 direct-definition baseline pairs include every m1,3 pair, the four
m7 input-order corners and the first m7 minimizing pair. They match the
literal Python/C++ counts entry by entry.

## 4. A valid size31 counterexample to H

Define s_1=1, s_2=132, and for h>=3, with d=2^(h-1)-1,

    s_h=(d+s_(h-1)), (2d+1), s_(h-1).

Every s_h has perfect maximum shape T_h and avoids even classical2143.
The base lengths are below4. In the induction step, every left value exceeds
every right value. Any mixed2143 occurrence would have its first point on
the left and its last point on the right, contradicting the necessary
inequality first<last. The middle new maximum can only be the third selected
point and then likewise forces first left/last right. Occurrences contained
in a side are excluded inductively.

For h>=2 take d=2^(h-1)-1 and A=s_(h-1), and define

    P_h=(d+A), (2d+1), A,
    Q_h=lift_{1,d+2,...,2d}(A), (2d+1), (1+A).

Both have perfect maximum shape T_h. P_h avoids by the same skew-band proof.
For Q_h, all left values except1 exceed all right values. A mixed2143 would
require its left first value to be less than its right last value, hence that
first value would be1. A global minimum cannot play the first/rank2 role.
The selected middle maximum case has the same first/last obstruction.
Thus no mixed classical2143 exists, and both side copies avoid by induction.
This covers every h>=2 regardless of the position of1 in A. At h1 use1,1.

The exact successful domain-checked run at h5,m31 is:

    P_5 = 26,28,27,29,23,25,24,30,19,21,20,22,16,18,17,31,
          11,13,12,14,8,10,9,15,4,6,5,7,1,3,2
    Q_5 = 26,28,27,29,23,25,24,30,19,21,20,22,1,18,17,31,
          12,14,13,15,9,11,10,16,5,7,6,8,2,4,3

The DP yields N(P_5,Q_5)=25635, below H's threshold32768. It processes156664
legal transitions and has7109 states in its largest level. The exact earlier
family counts for m1,3,7,15 are2,9,37,952. No global minimality at h5 is claimed:
all pairs were exhausted only at m1,3,7, while m15 uses this explicit pair.
The counterexample is finite exact computation with the checked all-size
quotient as a trust boundary, not a floating-point approximation or a growth
estimate. Its new full counting proof/certificate still needs Theo's separate
independent check. A final prefix hash table is retained in the compact JSON.

## 5. Preserved failure and reproduction

The initial test family mistakenly used a classical231-avoiding recursive
labeling as if it avoided boxed2143. This implication is false:2143 contains
132 and213 triples, not231. At the next level the subword1327465 contains
the consecutive boxed occurrence3274. The first reported size15 zero was
therefore outside H's domain, not a counterexample. The exact program/output
are preserved as `fixed_pair_join_dp_unchecked_v1.py` and
`fixed_pair_join_counts_unchecked_v1.json`. The corrected seed recursion has
the direct induction above, and the code explicitly checks avoidance and
perfect shape before reporting any H test. The valid h5 failure is distinct.

Reproduce with CPython3.11+, standard library:

    python3 -B verify_reverse_merges.py
    python3 -B balanced_join_reference.py
    python3 -B fixed_pair_join_dp.py

The fixed-pair run consumes the retained native baseline JSON. Rebuild it with
GCC12.2 and C++20:

    g++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Wconversion -Wshadow balanced_join.cpp -o /tmp/quinn-balanced-join
    /tmp/quinn-balanced-join balanced_fiber_h3.txt balanced_join_cpp_h3.json

The C++ program directly tests all four-index choices and interior points.
All6,345,768 candidates complete in6.33seconds/15076KiB. Every m1,3 pair matches
the Python literal definition; an address/undefined-sanitizer build checks
all80 m3 joins with identical output. Values<=15, shifts<=14, at most43^2*3432
candidates and uint64 counters exclude overflow. The Python DP has no
fixed-width count arithmetic. Compiled binaries remain outside source.

All claims concern precise mechanisms within target410. Refuting H does not
refute factorial growth, rule out a weaker/persistent subclass bound or imply
an exponential upper bound. The full target has not been replaced or solved.
