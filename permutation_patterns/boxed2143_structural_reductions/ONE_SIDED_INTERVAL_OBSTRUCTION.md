# A precise failure of one-sided interval testing

Author: Theo, literature-researcher-4. This is negative evidence for a proposed compression in the full-class interval lane, not a target pivot or a growth theorem. A different researcher's review is pending.

The known source criterion requires checking consecutive2143 factors after restricting to **every** interval of values [lo,hi]. A tempting weakening H would check only initial intervals [1,t] and terminal intervals [t,n]. State H precisely: whenever a permutation contains boxed2143, at least one of these one-sided restrictions has a consecutive factor in2143 order. The reverse implication is true by the source criterion; H's forward implication is false.

## Minimal exact counterexample

Take p=(3,1,2,5,6,4). The selected entries at one-based positions(1,3,4,6) are(3,2,5,4), in2143 order. The two unselected points horizontally between them have values1 and6, respectively below2 and above5. Its rectangle is therefore empty. The interval[2,5] restriction is exactly(3,2,5,4).

The initial-value restrictions at t=1,...,6 are

    (1), (1,2), (3,1,2), (3,1,2,4),
    (3,1,2,5,4), (3,1,2,5,6,4).

None has a consecutive2143 factor. The terminal-value restrictions at t=1,...,6 are

    (3,1,2,5,6,4), (3,2,5,6,4), (3,5,6,4),
    (5,6,4), (5,6), (6).

Again none has a consecutive2143 factor. Thus even combining all initial and all terminal tests misses this boxed occurrence. An increasing permutation of the same size has the identical all-false signature and avoids the pattern, so that boolean signature cannot decide boxed avoidance.

This failure is minimal in length. For n<4 there is no occurrence, and at n=4 the full interval sees any occurrence. At n=5, select a boxed occurrence. If the fifth point is horizontally outside its bounding rectangle, the selected four are consecutive in the original word, so the full interval detects it. If it is horizontally between the selected endpoints, rectangle emptiness forces it vertically below the selected minimum or above the selected maximum. A terminal restriction at that minimum, or an initial restriction at that maximum, respectively removes it while retaining all four selected entries. They are then consecutive and detected. These cases cover every possible fifth point, proving no failure before6.

## Uniform obstruction family

For any integers k,l>=1 set n=k+l+4 and

    p_(k,l)=(k+2, 1,2,...,k, k+1, k+4, k+5,...,k+l+4, k+3).

This is a permutation of[n]. The distinguished four entries A=k+2,B=k+1,C=k+4,D=k+3 form a boxed2143: entries between A and B are below B, and entries between C and D are above C. The interval[B,C] deletes both intervening blocks and returns(A,B,C,D).

For an initial restriction, either it lacks one of the two descents, or its only descents are the first transition A to the low block and its last transition from the retained high block to D. If both exist, at least five entries remain, so these descents are separated by at least three positions. For a terminal restriction the same argument applies: retaining B keeps A, C, every high-block entry and D, at least five entries; deleting B also removes the low block and leaves at most one descent. A consecutive2143 factor requires two descents whose starting positions differ by exactly2. It is therefore impossible in every one-sided restriction. This proves failure for the whole two-parameter family, without extrapolating from a census.

The obstruction excludes H and the corresponding one-sided occurrence-boolean state, only. It does not exclude a richer interval encoding, prove unbounded growth, or show that an upper-bound argument using a weaker superset is impossible. The uniform growth target410 remains open to the team. The original all-interval characterization is prior work, [Kitaev–Qiu–Xu, Theorem3.2](https://arxiv.org/html/2609.13764v1); no novelty claim is made for this elementary caution.

`one_sided_controls.py` preserves all restrictions of the minimal example, confirms finite minimality through n=6, and tests the exact family for1<=k,l<=6. Those controls supplement the written arbitrary-parameter argument and do not constitute its proof.
