# Minimum cover and the remaining binary maximum obstruction

Author and executing agent: **six-sorting-2, researcher**. Gates(a,b),a<b, put
the minimum on a and maximum on b. State bit i denotes wire i. A kernel is
the subsequence touching at least one of its specified individual one-hot
or one-zero routes. A binary kernel gate joins two occupied route groups;
a unary gate touches one group, including a stationary passage. Nonkernel
gates may interleave arbitrarily.

Let A be the fourteen-gate generalized eleven-wire prefix, followed by its
output permutation, in `fixture.json`. Write C=(3,10), B=(6,9),(9,10), and
K=proj0..9(A;C;B). Its127 Boolean states and20-gate construction are checked
on all2048 original inputs. The prefix has17 gates and its last wire contains
the global maximum. Established S(11)=35 gives s(K)>=18. Its connection to
the136-state X target and the original thirteen-wire prefix is in the
[earlier reduction](https://github.com/helgithorskarp/math_results/tree/main/sorting13_pruned10_mixed_kernels)
and [maximum-kernel dependency](https://github.com/helgithorskarp/math_results/tree/main/sorting13_prefix21_maximum_kernel).
Those are conditional reductions, not coverage of every thirteen-wire prefix.

**Theorem.** Every standard18-comparator sorter of K has its minimum kernel
among the43 words in the fixture. If that kernel is binary-only, its maximum
kernel has at least two unary gates and at least six gates in total.
Equivalently, every K18 sorter has either a unary minimum-kernel gate or at
least two unary maximum-kernel gates. Every K18 sorter already has at least
one unary maximum by the [previous exclusion](https://github.com/helgithorskarp/math_results/tree/main/sorting13_pure_maximum_exclusions).

More specifically, the pure minimum word M=(0,5),(0,1) gives the109-state
nine-wire target L=proj1..9(M(K)), whose checked interval is16..18. Every
L16 sorter has a unary maximum-kernel gate for the five one-hot rows on
3,4,5,7,8. The three binary-only maximum trees give the following targets:

| Case | Binary maximum tree G on L | Eight-wire image F | Lower bound |
|---|---|---:|---:|
|0|(4,7),(3,7),(5,7),(7,8)|68 states|13|
|1|(3,7),(4,7),(5,7),(7,8)|67 states|13|
|2|(3,4),(4,7),(5,7),(7,8)|68 states|13|

No13-gate upper bound for these F is claimed. The certificate rules out
their required12-gate completions at arbitrary depth and order. L16 with
unary maximum gates, the other42 minimum words, K18, X21 and global S(13)=44
remain open. General pruning, normalization, Kraft, binary commutation and
the terminal-threshold principle are prior methods, not new general theorems.

## Pruning convention

Fix original inputs of A to low, middle or high, with k middle values. A gate
touching any marker is deleted; propagating the middle ports gives a
generalized circuit on those k inputs. If a full eleven-input sorter has35
gates and the prefix deletes D, its suffix can delete at most35-S(k)-D.
Otherwise standardization would give a middle sorter smaller than S(k).

The high threshold x has1 at high ports. The nonlow threshold y has0 at low
ports. Execute these as separate Boolean rows. A suffix gate is deleted
exactly when either endpoint has x=1 or y=0. Write H(x,y) for this union
count. It includes stationary comparisons and counts a shared event once.
It is not the OR of independently evolved one-hot rows. The selected
witnesses and middle-port executions are checked independently.

## Why the minimum has only43 possible words

Use the [committed minimum/refill proposition](https://github.com/helgithorskarp/math_results/tree/main/sorting13_minimum_passage_reduction),
source aedd5f48b84a375cbd671d1daf331ede87815959, graph7402. In every K18 sorter,
the one-zero-1 route has exactly one passage(0,1); no gate uses1 earlier or0
later. The sole9 gate is(8,9), preceded by(6,8). The actual high row576 has
exactly three passages, all with endpoints at least6, ending in the unique
post-root refill(6,8) or(7,8).

The additional checked witness fixes original highs6/7/8 and low0. Seven
inputs remain middle; the17-gate prefix deletes14. It gives thresholds
(576,1022) and H<=35-16-14=5. The one-zero0 stays at0, so each0 gate is a
passage disjoint from those three high passages. Hence there are at most
two0 gates.

The one-zero5 must enter0 before the unique(0,1): its zero moves only left,
1 is unused earlier and0 is unused later. Its separate merge is(0,p),
2<=p<=5. Thus exactly two0 gates occur, first(0,p), then(0,1). The witness
with original high8 and low9 has nine middle inputs and six prefix
deletions; it gives the one-zero5 route cap4. Its two final merge passages
leave room for at most two earlier unary passages. Those use only2..8:
0 would be the merge,1 is forbidden, and the sole9 gate cannot touch a
zero initially on5 and moving only left. At each unary there are six
partners, and its zero moves to the smaller endpoint. Therefore the
candidate counts by word length2/3/4 are1/6/36. Repeated stationary passages
are included. The independent checker explores every support-touching
comparator under route caps(2,1,4), yielding the same43 words via175 states.
Arbitrary nonkernel events leave those three routes unchanged.

The sole binary-only word is M. Its two gates commute to the front across
disjoint preceding nonkernel gates. This is only a binary commutation;
none of the42 unary-containing words is front-loaded. Every proper K row
has a zero on0,1 or5, so M places its minimum on0. After its final(0,1),
no later gate uses0. Removing0 gives exactly L. The full prefix has19 gates,
so s(L)>=16; removing the two minimum gates from the checked K20 control
after disjoint commutation gives the checked L18 control.

## Why three binary maximum trees remain

The earlier marked-input caps on K give q6<=2 and q9<=1. M does not touch
these two trajectories, so their renumbered L caps are q5<=2 and q8<=1.
The one-hot7 row forces the sole8 gate to be(7,8); the one-hot5 then must
pass through(5,7) followed by(7,8), with no other passage. In a binary-only
maximum kernel, the groups from3,4,7 must coalesce on7 before(5,7). They
cannot join5,8 or the merged group afterward without exceeding these caps.
The two possible merge steps on3,4,7 are precisely the three first pairs
in the table. The checker independently enumerates all binary merges.

Every binary kernel gate commutes across earlier nonkernel gates: both of
its endpoints are live group ports throughout the intervening interval,
so each intervening gate avoids them. Thus G may be placed at the front
of the L suffix. It puts the global maximum on8, which is unused later.
An L16 sorter would leave a12-gate sorter of F=proj0..7(G(L)). The full
eleven-wire prefix A;C;B;M;G (with G labels increased by1) has23 gates. The
checker verifies its global minimum on0, global two maxima on9/10 and all
three F images on6144 original Boolean inputs.

## Two mixed budgets exclude every F12

Each F has one-hot5/6, one-zero1, and a two-one row whose final wire7 is0:
mask40 for cases0/2 and48 for case1. Each F12 sorter would extend the23-gate
prefix to a35-gate full generalized eleven-input sorter. The following
witnesses hold in all three cases:

| Thresholds(x,y) | Middle count k | Prefix deletions D | Bound35-S(k)-D |
|---|---:|---:|---:|
|128,254|6|21|2|
|160,254|5|23|3|

Their exact original marker sets are in the fixture. The first high row
is a stationary one on7; the low row is a stationary zero on0. Thus its
union counts precisely every gate using0 or7. Sorting one-zero1 requires
a gate(0,1), and sorting one-hot6 requires(6,7). These are distinct events,
exhausting the first budget. Therefore these are the only gates on0/7.
No nonredundancy or depth assumption is used in this step.

For high row160 (ones5/7), the unique0 gate(0,1) never touches a high1:
its initial leading zeroes stay zero. The second union bound therefore
gives H(160)<=2.

But the terminal-threshold lemma from the [previous proof](https://github.com/helgithorskarp/math_results/blob/main/sorting13_pure_maximum_exclusions/PROOF.md)
gives H(160)>=3. Here is the complete argument. The one-hot5 row is
dominated coordinatewise by row160, a relation preserved by AND/OR
comparators. It needs at least two passages to reach7 through the sole
(6,7). If H(160)<=2, those two passages exhaust H and must be(5,6),(6,7).
After(5,6), the actual high row is the sorted two-one row192 on6/7. No
other later gate can touch6/7 without spending another H passage. On
the test row40/48, wire7 stays0 until its sole gate; at(6,7), wire6 becomes0.
No later gate can refill6, contradicting the required sorted two-one output.
This proves s(F)>=13 and excludes all three binary L16 maximum kernels.

A maximum kernel for five groups has four binary merges. A unary gate adds
another event, hence L16 requires at least five maximum-kernel gates. In
the front-commuted K word, M's(0,5) is itself unary for the maximum route
starting on5; its(0,1) touches no maximum route. Thus the original K18 word
has at least two unary maximum gates and at least six maximum-kernel gates.
Disjoint commutations preserve these passage counts.

## Certificate, independent checks and positioning

The188-state certificate starts from both test rows and tracks five actual
Boolean executions (one-hot5, one-hot6, one-zero1, high160, the two-one test)
and the two union counts. It allows all28 comparator types. A transition is
discarded only if a union would exceed2 or3. The checker verifies membership
of the two initials, all5264 transitions (3131 allowed), and absence of
any state where all five rows are sorted. Induction proves the exclusion
for every word length, including arbitrary zero-cost cycles. There is no
selected parallel depth, slot count or unreported symmetry filter.

The checker imports neither the generator nor a solver. It uses scalar
compare/swap on five separate rows; the generator uses bit masks. Two
corrupted certificates are rejected. Two five-gate auxiliary words reach
the relaxed row targets at union counts2/4, demonstrating sharpness of
the second bound; they are not F sorting constructions. The independent
port checks cover1802 K witness assignments and300 F witness assignments,
including22 distinct-rank controls. The K20 and L18 constructions are
checked on2048 original inputs; simple bubble controls sort each F on
6144 original inputs. The certificate regenerates byte-for-byte. No
independent-person review, formalization or SAT exclusion is claimed.

The primary bounds are S11=35 from
[Harder2012.04400v3](https://arxiv.org/abs/2012.04400v3), S9=25 from
[Codish et al.1405.5754v3](https://arxiv.org/abs/1405.5754v3), and established
S5=9,S6=12,S7=16 (also reported in the
[live primary table](https://bertdobbelaere.github.io/sorting_networks.html)).
Their original proof corpora were not rerun. Pruning/standardization,
binary commutation and the imported7402 proposition remain analytic
dependencies in addition to the checked finite data.

The minimum-interleaving route is informed by the complementary
[Y1/Y2 result](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_minimum_interleaving),
source82e7d1028b9bbc7ce380f76e948752429bfe6325, graph7408. That result concerns
different146/145-state eleven-wire targets and a second-minimum Kraft
obstruction. No Y conclusion is silently transferred to K. The terminal
principle credited in the earlier7356 proof was motivated by independent
review7338 of a different Y2 theorem; neither that review nor7408 reviews
this result. The remaining constructive Y lane is owned by six-sorting-1.

The global table was refreshed2026-09-30 and still gives44..45 for13.
A private complete L16 probe with53 checked pruning bounds returned UNKNOWN
at30000-conflict/40-second limits; that is not an exclusion and is not used
here. The actual exclusions are the written threshold argument and the
independently checked arbitrary-length closed certificate. Remaining
directions are the L16 unary maximum interleavings and the other42 minimum
kernel words; unrestricted X and thirteen-wire coverage remain unresolved.
