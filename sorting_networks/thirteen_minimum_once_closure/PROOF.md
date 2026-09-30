# The minimum-one-passage branch is impossible

Author and executing agent: **six-sorting-1, researcher**.

The literal24-gate prefixes P;T1 and P;T2 in `fixture.json` have the
eleven-wire Boolean images Y1 and Y2, of sizes146 and145. Their other two
wires hold the largest two values. We prove that no standard20-comparator
completion of either image has exactly one passage on the single-zero
input on wire1. There is no depth or preparation-count restriction.

Combining the existing mixed bound with this exclusion, every possible
20-gate completion must have exactly two such minimum passages and must
use wire10 exactly once, at(9,10). Both Y completion questions remain
20 versus21; the global thirteen-input44–45 gap remains open.

## Imported premises and kernel classification

We use established S(11)=35 and S(12)=39 from
[Harder](https://arxiv.org/abs/2012.04400v3). The final mixed-route
corollary also uses S(9)=25 from
[Codish et al.](https://arxiv.org/abs/1405.5754v3), and the established
S(13)>=44 recorded in [the current table](https://bertdobbelaere.github.io/sorting_networks.html).
Pruning and standardization are established methods; their literature
proofs are imported, not rerun or claimed as new.

Adding a Y20 completion to its literal prefix produces a44-gate full
sorter by the zero-one principle. Fixing a global minimum on original
inputs12,10,11 gives the single-zero Y rows on0,1,5, respectively, and
deletes2,3,2 prefix gates. Removing that minimum from a full44 sorter leaves
a12-input sorting circuit. S(12)=39 therefore bounds their suffix passages
by3,2,3. In the conditional branch at issue the middle bound is1.
The independent checker reconstructs these witnesses with distinct ranks.

Track the occupied positions of these three single-zero routes. A kernel
event touches an occupied position; a binary event merges two occupied
supports, while a unary event touches only one. A nonkernel event avoids
all occupied positions. It leaves these three trajectories unchanged.
Their passage caps are(3,1,3). The only passage of the zero initially on1
must be(0,1), and every later event on0 is forbidden. Hence(0,1) is the
terminal kernel gate, after the routes from0 and5 have merged at0.

Put E={2,3,4,6,7,8,9,10}. The complete kernel classification is:

* One binary-only word:(0,5),(0,1).
* Eight words:(0,p),(0,5),(0,1), p in E.
* Eight words:sort(5,p),(0,min(5,p)),(0,1), p in E.
* Nine words:(0,5),(0,p),(0,1), p=2..10.
* Sixty-four words:(0,p),sort(5,q),(0,min(5,q)),(0,1), p,q in E.
* Sixty-four words:sort(5,q),(0,p),(0,min(5,q)),(0,1), q in E,
  p=2..10 excluding min(5,q).

There are two binary merges. The routes from0 and5 each have only one
passage beyond those merges. Consequently a unary either occurs on one
route before their merge, occurs jointly after their merge, or occurs
once on each route before their merge. No other case fits the caps.
The support-history generator and the closed-form independent checker
agree on all154 words. Exactly153 have a unary event.

## Weighted two-minimum deletion invariant

For every one of the78 original pairs of input positions, fix the two
smallest values there and let the other eleven values be arbitrary above
them. At a prefix let z be their unordered pair of output positions and
D the number of gates touching at least one of them. A gate between both
marked values is counted once. Marker positions and deletion counts
depend only on the two-marker threshold, regardless of middle values.

For each distinct z retain the largest witnessed D, denoted d(z). This
loses no future constraint: equal marker positions have equal later marker
trajectories and deletion increments. Define

    W = sum_z 2^d(z).

A comparator has at most two input marker pairs mapping to any output
pair. In a two-element fiber, both input pairs touch a marker at the
comparator, so both deletion counts increase by one. Its new weight is

    2^(1+max(d1,d2)) >= 2^d1 + 2^d2.

In a singleton fiber the deletion count increases by zero or one.
Thus W never decreases under a comparator. The independent checker builds
all comparator fibers by scalar distinct-rank execution on all55 two-marker
rows for each of the55 allowable eleven-wire comparators.

At the end of a44-gate full sorter, all78 marked input families have the
same output pair{0,1}. Pruning both marked minima leaves an11-input sorter
with44-D gates, so S(11)=35 forces D<=9. The final W is therefore at most
512. Any prefix with W>512 is impossible, whatever the remaining depth,
gate order or number of preparations.

After either literal24-gate prefix, the strongest profile is identical:

| Marked output pair | d |
|---|---:|
| {0,1} | 5 |
| {0,4} | 4 |
| {0,5} | 4 |
| {0,8} | 4 |
| {1,2} | 5 |
| {1,5} | 5 |
| {1,3} | 5 |
| {1,7} | 5 |

Its weight is208. All78 input pairs are evaluated in each case; this
profile is an exact threshold compression, not an assumed witness subset.

## Finite closure with arbitrary preparation count

For each of the153 unary words K of length m, use states(t,F), where
0<=t<=m is the number of selected kernel events already performed and F
is the strongest marked profile. The three occupied single-zero positions
are determined by the first t events of K.

At t<m include the next kernel comparator, advancing t, and every
nonkernel comparator avoiding the currently occupied positions, leaving
t unchanged. Update F exactly, retaining the maximum deletion count at
each resulting marker pair. Reject a transition only when its W exceeds
512. No cutoff on preparation count, depth or number of prefix gates is
part of this mathematical state graph. Repeated and inactive nonkernel
events are included; equal states and self-loops are merged.

The graph is finite: there are55 marker pairs, each retained integer d
lies between0 and9, and t has finitely many values. Every actual candidate
prefix ending its minimum kernel follows a path in this graph, even if
its number of gates is not recorded. Both initial profiles are identical,
so one closure per word covers both Y cases.

Every computed reachable closure has no surviving state at t=m. The
generator uses packed forward marker states and breadth-first search.
The independent checker uses scalar comparator fibers, inverse grouping,
distinct marker labels and depth-first search. It regenerates every
reachable state and every allowed transition, checks every rejection,
and checks the exact state-set hashes and counts in `certificate.json`.
The hashes and counts alone are not a proof; the regeneration and the
transition/coverage argument establish the finite exclusions.

Operational state/time caps cause a loud incomplete-run failure and are
not mathematical pruning. No timeout, UNKNOWN, unverified solver result,
or incomplete enumeration is used. Neither algorithm uses a SAT solver.

## Binary-only branch and the forced maximum gate

The remaining binary-only word is(0,5),(0,1). A nonkernel event preceding
a binary merge avoids both its endpoints. Commuting disjoint adjacent
events moves this binary-only kernel to the front, leaving an18-gate
completion of its ten-wire image. The already established exact bound19
for both front-minimum images excludes it; see
[the independently checked nullary exclusion](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_nullary_minimum_exclusion),
source commit5ad75ecb80164da04c921f1898cf62334668a027, graph
`bafkreiehh3wz7zl4dniucqeujnylhfwvuwey6kegf5znv3mtdger65ecby`.
That computational result is a cited dependency. Its nine SAT certificates
are not republished or rerun here. No unary event is commuted to the front.

All154 possible kernels are now excluded when the minimum from1 has one
passage. Its witnessed cap is2, so every Y20 completion would instead have
exactly two passages on that route.

For completeness, the
[existing mixed bound](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_prefix_frontier/MIXED.md)
fixes inputs{2,3,5} to the three largest values and input10 to the minimum.
Exactly16 prefix gates touch a mark, leaving nine arbitrary middle inputs.
The remaining high mark is on10, the low mark on1, and the other maxima
are fixed on11/12. S(9)=25 gives a suffix union cap44-16-25=3.
The scalar checker independently verifies this particular witness.

Initially bit1<=bit10 on every Y row. Before the first(0,1), wire1 never
increases and10 never decreases, so(1,10) is redundant. After that pivot,
wire0 is at most the prior wire1 and subsequently never increases, making
(0,10) redundant. The established global lower bound44 forbids these
redundant gates in a44 sorter. Thus the tracked high and low passage sets
are disjoint. Their union cap gives qH+qL<=3. Since qL=2 and qH>=1, qH=1.
The one-hot input on9 must enter10 via(9,10), so that is the unique gate
involving wire10.

The new output is this fixed-prefix branch elimination and resulting
construction restriction. Extreme pruning, Huffman/Kraft bounds and
finite-state closure are established techniques. The written bridges and
imported literature bounds are not formalized; independence here means
different algorithms by this researcher, not external-person review.
