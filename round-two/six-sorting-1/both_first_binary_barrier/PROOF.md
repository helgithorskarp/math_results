# Changed B23 requires a singleton first increase on at least one side

Author and executing agent: **six-sorting-1, researcher**, 2026-10-02.
Status: scoped author-proved lemma with exact finite certificates and separate
same-author algorithms. The written bridges are unformalized; no external
review verdict is claimed. The unrestricted thirteen-input interval remains
[44..45 in the maintained table](https://bertdobbelaere.github.io/sorting_networks.html),
refreshed 2026-10-02.

A standard comparator `(a,b)`, `a<b`, writes the minimum to `a`. Ports are
`0..12`. A prefix is a literal sequential word; a completion may have any
comparator order, repetition, interleaving, preparation length or depth.

## Statement and exact prefix

Let B23 be

```
(0,11),(1,7),(2,4),(3,5),(8,9),(10,12),
(0,2),(3,6),(4,12),(5,7),(8,10),
(0,8),(1,3),(2,5),(4,9),(6,11),(7,12),
(0,1),(2,10),(4,8),(3,6),(9,11),(11,12).
```

For each original choice of two LOW inputs, fix those inputs to two distinct
small ranks below all eleven free middle inputs. Follow its unordered marked
ports and count every comparator touching a mark once. For each current port
configuration take the maximum original touch count `d`, and sum `2^d` over
current configurations. This is the ordinary LOW pair mass. HIGH is the dual
family of two large ranks. The complete original free cubes are preserved.

At B23 the first output is the minimum and the last is the maximum. Every LOW
configuration is `{0,p}` and every HIGH configuration is `{p,12}`. The exact
secondary classes are

| Side | Secondary port and ordinary exponent |
|---|---|
| LOW | `(1,7),(2,7),(3,6),(4,7)` |
| HIGH | `(5,6),(6,6),(7,6),(9,6),(10,6),(11,7)` |

Both masses are 448. At a gate, a **binary** event touches two current
secondary candidates of the side under consideration. A **singleton** event
touches just one; a preparation touches none. The side's first **strict
increase** is its first gate whose ordinary pair mass exceeds 448.

**Conditional lemma.** Define the three LOW words

```
L1 = (1,3),(2,4),(1,2)
L2 = (2,3),(1,4),(1,2)
L4 = (3,4),(1,2),(1,3).
```

After either literal prefix `B23;L1` or `B23;L4`, a sorting completion of total
size at most 44 cannot have its first strict HIGH pair-mass increase binary.

**B23 corollary.** In any standard sorting completion of B23 with at most
44 comparators, the first strict LOW and HIGH increases cannot both be binary.
Each side must eventually have a strict increase. Therefore at least one
side's first strict increase must be singleton. This is a necessary structural
restriction; the singleton cases and the existence of such a completion
remain open.

## Ordinary ceiling and decreasing supports

The generic weighted pruning theorem gives

```
W_LOW(P), W_HIGH(P) <= 2^(m-S(11)) <= 512
```

at every prefix of a total-size-`m<=44` sorter. We import `S(11)>=35` and the
pruning/standardization setting from
[Harder's primary paper](https://arxiv.org/abs/2012.04400).
The general ordinary/semantic transport interface is credited to
[lemma8539's proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-2/semantic-pruning/PROOF.md).
The original lower-bound proof corpus is not replayed.

A touch of held port 0 doubles every LOW class; a touch of held port 12
doubles every HIGH class. Either gives at least 896 and is impossible.
Thus neither held port can be touched. At a remaining gate a singleton
doubles one weight, and a binary event with child costs `u,v` replaces their
weights by `2^(1+max(u,v))`. A preparation changes no ordinary cost.
Mass is nondecreasing; a binary event preserves it exactly when `u=v`.

If the first strict increase is binary, all preceding events on that side
are equal-cost binary merges. No singleton can precede it. Initially every
cost is at least 6. Of the unequal merges, only costs 6 and 7 can fit the
remaining slack 64: they replace weights 64 and 128 by 256, saturating 512.
Costs 6/8 or 7/8 already overshoot, and larger costs do also. Once saturated,
every subsequent event must again be an equal-cost binary merge. In
particular, a singleton cannot appear later either.

Under this hypothesis, the live secondary support only decreases. A binary
LOW event retains the smaller endpoint, and a binary HIGH event retains the
larger. A released port never returns. Every original candidate must
eventually join the single terminal secondary class at port 1 or 11. Hence
there are exactly three LOW binary events and exactly five HIGH binary
events, respectively.

The first strict increase exists on each side: the initial mass is 448,
whereas a sorter has one final secondary class and its ordinary mass is a
power of two. Nondecrease and the ceiling force that final mass to be 512.

## Commutation covers arbitrary preparations

Suppose first that the LOW side has one of the literal words L1/L4 at the
front. LOW then has sole class `{0,1}` of cost 9, so ports 0/1 are frozen;
port 12 is frozen by the HIGH ceiling. HIGH still has its original six
secondary classes, since L1/L4 use only ports 1..4. Assume its first strict
increase is binary. Its five binary events use only the six original HIGH
candidate ports. A preparation preceding a future binary event avoids that
event's endpoints: those endpoints are still live at the preparation, since
they have never been released and will not return after release. The
preparation therefore commutes with every later binary event.

Move preparations, keeping their mutual order, after all five HIGH events
by repeated disjoint-gate commutations. The full ordered-input network
function, gate count and event order are preserved. This proves reduction to
a five-event HIGH word without enumerating preparation functions or placing
a depth bound on the completion. An initial HIGH singleton cannot use this
argument: its free operand may have been prepared, and is retained in the
unresolved frontier.

For the B23 corollary assume both first strict increases binary. All LOW
events then stay within `1,2,3,4`; all HIGH events stay within
`5,6,7,9,10,11`. These sets are disjoint throughout, not just at B23. The same
decreasing-support argument moves all three LOW events to the front after
B23, and then all five HIGH events after them. HIGH marked routes and
ordinary deletion costs are unchanged by the LOW events, which never touch
a HIGH mark. Thus the HIGH first-increase type survives the LOW front
normalization. Preparations are not assumed to commute with each other,
and no singleton is moved past a preparation on its free operand.

## Complete binary covers

For LOW, the costs 7,7,6,7 imply three complete binary genealogies under
the 512 ceiling. Their full four-variable Boolean functions equal exactly
those of L1, L2 and L4. The standalone checker independently constructs
all bottom-up forests, with 13 states, 715 local pair controls and three
terminal trees. Equality of complete min/max Boolean functions lifts to
all totally ordered inputs by thresholding. Gates in disjoint child
subtrees commute; child events precede their parent. Thus these canonical
words cover every valid order of the LOW binary events.

The whole L2 branch is already excluded by
[published lemma9325](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-1/one_sided_low_binary_barrier/PROOF.md).
For a self-contained finite control this packet replays original LOW
inputs `{3,5}`: at `B23;L2` they have `D=9,R=1`, current LOW `{0,1}`,
with unmarked identity gate 25 `(1,4)`. Deletion produces an oriented
eleven-input prefix of length 16. Pruning any full sorter gives
`35 <= m-10`, so `m>=45`. All 2048 free assignments and the full carrier
function are checked. Original LOW `{0,2}` reaches the same current LOW
ports at cut 25 but activates gate 25 on some assignment. Sharing current
marker ports is consequently not a license to delete a free gate.

For HIGH use weight units 64. Initial weights are `1,1,1,1,1,2`, total 7.
Exactly one unequal merge is `1+2 -> 4`, raising the total to 8; every
other merge has equal weights. The final weight-8 root has two weight-4
children. Exactly one child is the unequal node. There are two cases:

1. Its weight-2 child is original port 11. Choose the unit sibling in
   five ways, and a pairing of the four remaining unit leaves in three
   ways: 15 trees.
2. Its weight-2 child consists of two unit leaves. Choose its unit sibling
   in five ways and the paired child in six ways. The other two unit leaves
   pair and then merge with original port 11 on the other root branch:
   30 trees.

This gives exactly 45 canonical five-gate words. Internal roots use the
maximum physical label in their leaf subset. The producer independently
enumerates every legal ordered binary route: 300 complete orders, 2145
local controls, 45 distinct complete six-variable functions. The
partitioned words give the same function set.

The standalone checker uses bottom-up forests and subset genealogies,
independently reconstructing 45 terminal trees from 281 states and 15455
local controls. It numerically reconstructs each full six-variable function
and compares the entire set with all 45 words for each LOW partner. Literal
prefix hashes link the immutable original-domain selectors to these words.
Thus all 90 conditional roots, not a heuristic representative subset, are
covered. Full scalar replay of all 8192 original thirteen-input vectors per
root checks four held ranks and the complete nine-input image. The images
have sizes 82..99 for L1 and 78..99 for L4. Each front has length 31, with
13 remaining gates on physical ports `2..10` at total size 44.

## Original-domain nested certificates close all 90 roots

For an original (3 LOW,3 HIGH) clamping `f`, retain all seven free Boolean
inputs. Count marked deletions `D_f`, and count free gates that are identities
on that entire original cube as `R_f`. Put `C_f=D_f+R_f`. Follow the free
carriers through marked exchanges and remove those two disjoint sets of
gates to obtain an oriented seven-input prefix `Q_f`.

Use the generic nested theorem of
[lemma9007](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-2/native24-kernel-cover/NESTED.md):
for any fixed selected original domains, define

```
lambda_f = C_f + B_7(Q_f)
lambda_z = max_(f with current LOW/HIGH mask pair z) lambda_f
M = sum_z 2^lambda_z.
```

Every sorting extension of total size `m` satisfies `M<=2^m`. Here
`B_7=max(16,LOW semantic anchor,HIGH semantic anchor)`; the anchor theorem
is [lemma8604](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-2/semantic-pruning/ANCHORS.md).
The bounds import `S(5)>=9,S(6)>=12,S(7)>=16`. The method is invariant
under global carrier permutations and nondecreasing under appended oriented
gates. No native-prefix negative theorem is imported.

Briefly, a marked gate or conditional free identity raises `C_f` by one
and leaves `Q_f` unchanged up to a global relabelling. An active free gate
appends an oriented comparator to `Q_f`, so its lower bound cannot decrease.
Different original domains remain distinct throughout. The current tag-pair
transition has at most two preimages; a double fibre charges both histories,
so its new label is at least `1+max` of their old labels. Its dyadic weight
is at least their sum. Thus `M` cannot decrease. At a full sorter one class
remains, every final pruned `Q_f` sorts its full seven-input cube in
`m-C_f` gates, and validity of `B_7` gives `lambda_f<=m`.

The certificate selects 582 original-domain occurrences across the 90
roots, always in distinct current classes within a root. It has 449 distinct
oriented retained inner words. For every root the independently recomputed
selected mass is strictly greater than

```
2^44 = 17592186044416.
```

The smallest is

```
18691697672192 = 17*2^40 = (17/16)*2^44.
```

Therefore none of these 90 literal fronts admits a total-size-at-most-44
sorting extension, at any depth. Commutation proves the conditional HIGH
lemma. The complete three-LOW cover, L2 obstruction and preservation of
HIGH first-event type prove the stated B23 corollary.

## Reproduction, credits and trust boundary

See [README.md](README.md) for exact standard-library Python commands and
[SOURCE-CREDITS.md](SOURCE-CREDITS.md) for copied source pins and prior
artifact references. The compact certificate is 40232 bytes, SHA256
`cce7383fbe1e0401ef9c7dbbe9fc176a7603c34ca2148de1ea12a099ee4d6f5d`.
Producer normal/optimized runs give identical bytes. Standalone numeric
normal/optimized runs give identical finite fields and reject all 15
damages; [expected.json](expected.json) records the exact counters and hashes.

The producer uses weighted partitions, route DFS, packed original-cube
functions and dyadic anchor aggregation. The checker imports no generator,
sibling source, solver, graph package or external data: it uses numeric
distinct ranks on full original cubes, bottom-up forests, explicit complete
carrier functions and heap `1+max` Huffman aggregation. Its generic numeric
primitives have precise published code credit. Shared mathematics is stated,
and this is same-author algorithmic independence, not independent-person
review or a proof-assistant result.

Proof replay covers 737280 original thirteen-input vectors/22855680 gates,
319488 initial ordinary pair assignments/7348224 gates, 74496 selected outer
assignments/2309376 gates, 76544 complete pruned-function assignments
(including the L2 control), and 1609216 inner assignments/11432960 gates.
Additional positive controls check the primary seven-input size-16 and
eleven-input size-35 sorters, every prefix of the seven-input sorter,
24 oriented wire relabellings, and two whole original clamping/pruning
controls on a guaranteed full sorter. Damages alter coverage, word support,
image size, original marker configuration, D/R/identity mask, inner bound,
strict mass, original-domain count, duplicate class accounting and the L2
redundancy record. The duplicate-class damage repairs the selector too,
so its rejection uses actual class disjointness rather than a file checksum.

The 99-element selected proposal pool credits published native9341 data and
prior own9285 data. It is only proposal data: any domain can be proposed,
and every used domain is independently reconstructed here. The full private
90-image and all-99-domain exploratory arrays are omitted and unnecessary.
No timeout, partial enumeration, UNKNOWN or heuristic failure is a proof
premise. All proof jobs use one process/native thread and unchanged limits.

The remaining construction frontier includes the complete 156/157-state
ten-core images of L1/L4 with 18 gates available. The new result removes
their first-HIGH-binary option; their first-HIGH-singleton preparations remain.
Up to three equal HIGH merges can release three additional ports before such
a singleton, so preparation support can have seven ports. The native9341
four-port closure is not transferred. First LOW singleton cases, earlier
prefixes and unrestricted thirteen-input networks remain outside the result.
