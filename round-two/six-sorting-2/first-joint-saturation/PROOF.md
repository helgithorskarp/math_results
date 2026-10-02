# Native H21 cannot saturate both pruning masses at its first increase

Actual author and executing agent: **six-sorting-2, researcher**, 2026-10-02.
This is a restricted author proof with exact finite certificates and separate
same-author algorithms. The universal bridges are unformalized. No external
review verdict or unrestricted thirteen-input exclusion is claimed.

Ports are `0..12`; a standard gate `(a,b)`, `a<b`, writes the minimum to `a`.
The literal native nineteen-gate prefix is

```
N19 = (0,11),(1,7),(2,4),(3,5),(8,9),(10,12),
      (0,2),(3,6),(4,12),(5,7),(8,10),
      (0,8),(1,3),(2,5),(4,9),(6,11),(7,12),(0,1),(2,10).
H21 = N19;(9,11);(11,12).
```

For every original pair of LOW inputs, clamp those inputs to distinct ranks
below the eleven free middle inputs. Follow its two marked ports and count
each gate touching a mark once, obtaining `D`. Group the original histories
by their current unordered marked pair and keep the maximum `D` in each
class. The ordinary LOW mass is the sum of `2^D` over these classes. HIGH is
the dual construction with two ranks above the free inputs. Each original
free-input cube is retained; sharing current marked ports never identifies
the conditional functions of two different original domains.

At H21 the minimum is held at port0 and the maximum at port12. The complete
ordinary secondary classes are

| Family | `(secondary port, D)` |
|---|---|
| LOW | `(1,7),(2,7),(3,5),(4,6),(6,5),(8,6)` |
| HIGH | `(3,5),(5,6),(6,5),(7,6),(9,6),(10,6),(11,7)` |

Both masses are448. There is no HIGH secondary at port8.

**Theorem.** In any standard sorting completion of this literal H21 with
total size at most44, the first gate increasing either ordinary mass cannot
raise their ordered pair to `(512,512)`. That first increase must have pair
`(448,512)`, `(480,480)`, or `(512,448)`.

The suffix has arbitrary order, repetition, interleaving, preparation length
and depth. The theorem is not a selected-depth SAT exclusion. It does not
decide whether H21's244-state eleven-wire target has a23-gate sorter.
The [maintained table](https://bertdobbelaere.github.io/sorting_networks.html)
still records unrestricted `44..45`.

## Pruning ceiling and zero events

The ordinary pruning theorem, with imported `S(11)>=35`, gives at every
prefix of a total-size-`m<=44` sorter

```
W_LOW, W_HIGH <= 2^(m-S(11)) <= 512.
```

We use the established pruning and standardization setting of
[Harder's primary paper](https://arxiv.org/abs/2012.04400), together with
the precise transport statement of
[lemma8539](../semantic-pruning/PROOF.md).
The original lower-bound corpus is not rerun. A touch of held port0 doubles
the LOW mass, and a touch of held port12 doubles the HIGH mass; either
already exceeds512. Thus every suffix gate uses physical ports1..11.

For one family, a singleton touch replaces `2^d` by `2^(d+1)`. A binary
touch of secondary costs `d,e` replaces their two weights by
`2^(1+max(d,e))`. A preparation touches no secondary candidate. Mass cannot
decrease; a binary event preserves it exactly when `d=e`. LOW retains the
smaller endpoint; HIGH retains the larger.

Before the first strict increase, a gate must therefore either avoid a
family's live support or merge two equal-cost live classes. A nonpreparation
zero event shrinks those supports, never resurrecting a released port.
Initially the support intersection is exactly `{3,6}`. The only joint zero
event is `J=(3,6)`, merging the cost5 leaves in both families. After J,
LOW retains3 and HIGH retains6, and the supports are disjoint.

If J has not occurred, the only cost5 leaves remain exactly3/6 in each
family. A gate meeting exactly one of them raises both masses by32 or exceeds
the available slack in a family; the permitted result is `(480,480)`.
Meeting both is J and gives no increase. Every other positive increment is a
multiple of64. The ceiling thus permits precisely the four first-increase
pairs `(448,512)`, `(480,480)`, `(512,448)`, `(512,512)` before the theorem's
exclusion. This reasoning applies to arbitrary preparations.

A first increase exists in a sorter: the final secondary configuration is
unique, so its ordinary mass is a power of two, whereas the initial448 is
not. The standalone numeric checker independently constructs all828 joint
zero profiles and all45540 next-gate controls. It obtains the complete
zero-word polynomial

```
1 + 9t + 62t^2 + 414t^3 + 2436t^4 + 11200t^5 + 31680t^6.
```

These45802 words describe events, not arbitrary preparation functions.
The enumeration is a control for the analytic normal form below; no shortest
profile representative is used as complete Boolean-function coverage.

## Simultaneous saturation forces a fifteen-cross normal form

Assume the first increase raises both masses to512. It cannot meet either
unmerged cost5 leaf: that would give32 rather than64, or exceed the ceiling.
Away from the cost5 leaves the two families have disjoint supports. A gate
increasing both must touch exactly one cost6 secondary in each family.
It is a cross gate, singleton on each side, with both endpoints live.
In particular it has no operand prepared on a dead union port.

J must eventually occur. The only cost5 leaves are3/6; before the first
increase they can only merge with each other. After simultaneous saturation
no positive mass increase is permitted, so they still can only merge with
each other. Both families must end in a unique secondary class. Every gate
preceding J avoids3/6, including the cross gate if it precedes J and all
preparations. Therefore commute J to the front after H21, preserving the
entire ordered-input network function and gate count.

After J the profiles are

```
LOW : (1,7),(2,7),(3,6),(4,6),(8,6)
HIGH: (5,6),(6,6),(7,6),(9,6),(10,6),(11,7).
```

The first increasing cross gate must join one of `{3,4,8}` to one of
`{5,6,7,9,10}`. A cost6 live root cannot have participated in an earlier
equal-cost merge, which would raise its cost. Thus every preceding zero event
and preparation avoids both cross endpoints. Commute the cross immediately
after J. This gives exactly15 choices, using the standard orientation:

```
(3,5),(3,6),(3,7),(3,9),(3,10),
(4,5),(4,6),(4,7),(4,9),(4,10),
(5,8),(6,8),(7,8),(8,9),(8,10).
```

If the HIGH endpoint is smaller, the singleton transitions exchange the
two families' endpoint labels. Their supports remain disjoint. Each family
now has mass512. LOW's cost inventory is three7s and two6s; HIGH's is two7s
and four6s. Every later nonpreparation event must be an equal-cost binary
merge within one family. Its support only decreases. A preparation before a
future event avoids that event's endpoints, since they are still live then.
Move every preparation, keeping their mutual order, after all future binary
events. LOW and HIGH events use disjoint leaf supports and commute across
families. No preparation is assumed to commute with another preparation.

The LOW genealogy first pairs its two cost6 leaves, then pairs its four
cost7 roots, and finally merges the resulting cost8 roots: exactly3 trees
and4 gates. HIGH first pairs its four cost6 leaves (3 pairings), then pairs
its four cost7 roots (3 pairings), and finally merges its cost8 roots:
exactly9 trees and5 gates. Independent child-subtree gates commute; child
events precede their parent. These canonical words therefore represent the
full ordered-input functions of all legal binary event orders. Equality of
their complete Boolean functions lifts by thresholding.

There are consequently exactly `15*3*9=405` canonical fronts

```
H21;J;cross;LOW_tree;HIGH_tree.
```

Each front has length32 and holds the two smallest ranks at0/1 and the two
largest at11/12. Those ports are frozen by the saturated ordinary envelopes.
The active nine wires are physical2..10, with at most12 suffix gates at total
size44. Core bitj is physical `j+2`. Their exact Boolean images have61..96
states and are405 distinct images. Preparations remain in the arbitrary
suffix after the front; no finite preparation-function closure is imported.

## Original-domain nested certificates exclude every front

Use the generic original-domain nested theorem of
[lemma9007](../native24-kernel-cover/NESTED.md) and the semantic anchor
operator of [lemma8604](../semantic-pruning/ANCHORS.md).
For each selected original3-LOW/3-HIGH domain f, retain all seven free inputs.
Let `D_f` count marked touches and `R_f` count free gates that are identities
on this entire original cube. Put `C_f=D_f+R_f`. Deleting these disjoint sets
and following free carriers gives an oriented seven-input prefix `Q_f`.
Let

```
B7(Q) = max(16, semantic LOW anchor(Q), semantic HIGH anchor(Q))
lambda_f = C_f+B7(Q_f)
lambda_z = max_(f with current LOW/HIGH tag pair z) lambda_f
M = sum_z 2^lambda_z.
```

Every sorting extension of total size m satisfies `M<=2^m`. Marked or
conditionally redundant gates raise C and preserve Q up to global carrier
renaming. Active free gates append an oriented gate to Q, whose anchor bound
cannot decrease. The tag transition has at most two preimages; a double
fibre charges both histories, so the new label is at least `1+max` and its
weight dominates their sum. At a complete sorter only one current tag pair
remains, and its pruned Q sorts its entire seven-input cube in `m-C` gates.
This proves the mass bound, retaining each original conditional domain.
The imported size bounds are `S(5)>=9,S(6)>=12,S(7)>=16`.

The certificate uses3003 selected original-domain occurrences across405
fronts, always in distinct current classes within a front. Of these2772 use
the valid constant inner bound16;231 use fully replayed nested anchors,
with184 distinct selected retained inner words. Constant witnesses only
underestimate the operator above and suffice when their selected mass
already exceeds the ceiling. The81-domain proposal pool is not an
exhaustive domain enumeration or a proof premise.

Every independently recomputed selected mass exceeds

```
2^44 = 17592186044416.
```

The smallest is

```
17729624997888 = 129*2^37 = (129/128)*2^44.
```

Thus none of the405 fronts has a size-at-most44 sorting extension. The
commutations and complete binary covers prove the theorem at arbitrary depth.

## Reproduction, comparisons and limits

[README.md](README.md) gives standard-library commands; [checks.json](checks.json)
records counters, hashes and damaged controls. [SOURCE-CREDITS.md](SOURCE-CREDITS.md)
identifies copied primitives, source pins and graph dependencies.
The producer uses pair partitions, packed full cubes and dyadic aggregation.
The standalone checker imports no producer or profiler: it enumerates
bottom-up forests, reconstructs numeric distinct-rank routes on full original
cubes, checks complete carrier functions, and compares heap Huffman bounds
with dyadic aggregation. It independently reconstructs all828 zero profiles,
all405 fronts, the full246-state H21 image from8192 inputs, all405 projected
images, every selected domain and every selected inner bound. Positive
controls use the primary7/11 sorters, all prefixes of the size16 seven-input
sorter and two whole pruning controls on the guaranteed native46 sorter.

The [weighted-shadow N19 reduction, lemma9396](../weighted-max-native19/PROOF.md),
already identifies native N19 size44 feasibility with the244-state H21/23-gate
question. This theorem removes only its first simultaneous-saturation case.
The [native20 exclusion, lemma9341](../native20-finite-cover/PROOF.md), covers
the different direct `H21;(3,8)` branch. The peer
[simultaneous-first-slack theorem, lemma9285](../../six-sorting-1/joint_saturated_core_branches/PROOF.md)
is the direct prior comparison. Its changed B23 function equals
`H21;(4,8);(3,6)`, and both appended gates preserve both448 masses. At B23
all costs are at least6, so simultaneous first increases necessarily give
`(512,512)`. The present H21 theorem therefore implies that earlier
conditional B23 theorem, while H21's additional `(480,480)` case remains
open. This is the scope of the GENERALIZES relation to9285; the earlier135
fronts and their exclusion retain their original credit.
The peer
[changed-B23 first-binary exclusion](../../six-sorting-1/both_first_binary_barrier/PROOF.md)
concerns `H21;(4,8);(3,6)` and the binary/singleton type of each side's first
increase; sharing masses does not identify the two prefixes' functions.
Its first-event-type hypothesis differs. Neither peer negative conclusion
is used as a premise of the405 certificates.

First increases `(448,512)`, `(480,480)` and `(512,448)` remain unresolved
here. In particular a singleton with a dead operand may depend on arbitrary
preparation functions. The native zero-event frontier can release five union
ports; no five-port function closure is asserted, and no previous four-port
cover is transferred. Native N19 feasibility at23 remaining gates, changed
prefix singleton cases and the unrestricted44–45 gap remain open.
