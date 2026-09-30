# Necessary activity and first-touch preparation for B11 size 22

Author: **six-sorting-2, researcher**. This is a scoped structural lemma,
not a B11 nonexistence proof or a determination of the thirteen-input
minimum. All wire numbers and comparators below are zero based and
ordinary: `(a,b)`, with `a<b`, sends the smaller value to `a`.

Let `P19` be the first nineteen comparators of the incumbent fixed in
`fixture.json`, and let

```
G = P19 ; (10,12) ; (0,5) ; (0,1).
```

After this 22-comparator prefix, original wires 0 and 12 hold the global
minimum and maximum. The projection of its Boolean image to original
wires 1 through 11 is the 158-row set `B11_states`. Internal B11 indices
0 through 10 denote these eleven wires in order. A 22-comparator sorter
of B11, lifted by adding one to each endpoint and appended to G, sorts
all 8192 original Boolean inputs, hence all inputs by the zero-one
principle. The [P19 reduction](https://github.com/helgithorskarp/math_results/blob/main/sorting13_P19_binary_minimum_reduction/PROOF.md)
also proves the converse existence implication from P19 full size 44.
No coverage of arbitrary thirteen-input prefixes follows.

## The marked-family conclusion

For either polarity and any original pair of positions, place the two
smallest, or the two largest, distinct values in those positions.
A comparator is **touched** when either endpoint currently holds either
marked value, including a touch without a swap and a comparator touching
both marks. Let D be the number of touched comparators. This trajectory
and D depend only on the marked pair and the comparator sequence.

For a given polarity and output pair, the prefix profile stores the
largest D over its original witnesses. A witness attaining this largest
D is called strongest. In G every marked pair contains a held endpoint
(original 0 for minima, original 12 for maxima) and one internal partner.
Exact prefix replay gives:

| Polarity | Internal partner | Prefix D | Strongest original witnesses |
|---|---|---|---|
| minimum | 0 | 7 | 40 |
| minimum | 1 | 6 | 16 |
| minimum | 2 | 6 | 8 |
| minimum | 3 | 6 | 2 |
| minimum | 4 | 6 | 7 |
| minimum | 6 | 6 | 4 |
| minimum | 10 | 5 | 1 |
| maximum | 5 | 7 | 4 |
| maximum | 7 | 6 | 8 |
| maximum | 8 | 7 | 16 |
| maximum | 9 | 7 | 16 |
| maximum | 10 | 5 | 4 |

**Lemma 1.** In every ordinary B11 completion with 22 comparators, all
48 strongest maximum families and 77 strongest minimum families finish
at total D=9. The remaining strongest minimum family, original pair
`{0,12}`, finishes at D=8 if the first internal-wire-10 event is a
minimum binary merge, and at D=9 if it is minimum unary. Thus 125 of the
126 strongest typed families always saturate the pruning bound; the
last saturates conditionally. This statement does not assert that a
sorting completion exists in either branch.

**Proof.** Import the complete necessary coupled-profile language of
[six-sorting-1's joint-extrema lemma](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_joint_extrema_normal_form/PROOF.md).
Its first-wire-10 partner exclusions 0, 7 and 9 are part of that import;
only the weight ceiling would not imply all three exclusions. The
ceiling is 512 for each profile, from full size 44 and S(11)=35. In units
of 32 the initial vectors are

```
minimum: (4,2,2,2,2,0,2,0,0,0,1)
maximum: (0,0,0,0,0,4,0,2,4,4,1).
```

Before the first gate at internal 10, effective events are equal-weight
binary merges. At that gate the maximum part is unary, 32 to 64, and
the minimum part is either unary, 32 to 64, or binary, (64,32) to 128.
Afterward both sums are 512, their supports are disjoint, and effective
events are equal-weight binary merges. A profile-preserving comparator
touches neither support. These properties include arbitrary interleaved
profile-preserving gates and are not a fixed-depth restriction.

Track actual witness depths rather than just the maximum stored in an
output pair. At an equal-weight binary merge both maximal incoming
depths agree and both increment by one. Unary doubling also increments
the actual depth by one. The only possible gap between this incremented
incoming maximum and the new output maximum is the smaller minimum
entry at internal 10 in the first minimum binary merge. Its actual
incremented depth is 6 while the new profile depth is 7. This one-unit
deficit persists at later equal merges. No other strongest family
acquires a deficit. At the terminal profile both surviving depths are 9.
The unique strongest minimum family initially at internal 10 is `{0,12}`,
proving the conclusion.

The computation supplies an exact audit of this local induction. The
forward generator tracks tagged actual witnesses through all non-loop
edges of the complete 2214-state, 22536-edge language. The independent
checker uses full thirteen-wire pair profiles and inverse fibers, rather
than importing that generator or its tagged algorithm. It checks 161017
positive-entry depth transitions; all 380 possible deficit edges have
exactly the form above. It includes self loops and confirms every
reachable state can reach the terminal profile. An induction over every
actual comparator therefore covers arbitrary comparator order and depth.
Both algorithms reconstruct the full state and edge sets and compare
these sets entry by entry when the private catalogue is supplied. □

## Saturation forces activity on clamped slices

For a minimum family, set its two original inputs to -2 and -1, and vary
the other eleven inputs independently over 0/1. For a maximum family
use 2 and 3. Thresholding at 1 commutes with every comparator, so the
projected thresholded image after G is exactly the B11 slice obtained
by fixing the original pair's Boolean bits to 0 or to 1, respectively.
The certificate lists these exact images as integer bit masks.

**Lemma 2.** For each family with final D=9, every suffix comparator
that is retained by its marked-pair pruning must swap at least one
Boolean row of its corresponding slice, at that comparator's actual
position in the suffix sequence.

**Proof.** Marked pruning of the full 44-comparator sorter deletes nine
touched comparators and gives an eleven-input generalized sorter with
35 comparators. By S(11)=35 this is minimal. If any retained comparator
were inactive on every free Boolean assignment, deleting it would give
a generalized sorter with 34 comparators, which standardization turns
into an ordinary sorter without adding a comparator. This contradicts
S(11)=35. At a retained comparator both endpoint values are free 0/1
values. Its scalar swap is therefore exactly the swap seen after
thresholding in the clamped Boolean slice. Pruning's wire relabeling
does not change this correspondence between trajectories. The lifted
suffix never touches either held outside endpoint. □

This uses known marked pruning and standardization, as in
[Harder's primary paper](https://arxiv.org/abs/2012.04400v3), and does
not claim these methods as new. The new statement applies the exact
strongest-family saturation and slice data to B11.

Families with the same polarity and internal partner have identical
suffix marked trajectories and deletion masks. Requiring activity on an
inclusion-smaller initial slice then guarantees activity on any containing
slice at the same gate, because a comparator sequence maps subsets to
subsets. The 126 strongest families give 14 class-labelled distinct
slice images. Their inclusion-minimal domains are:

| Polarity | Partner | Original pair representative | Rows | Requirement |
|---|---|---|---|---|
| minimum | 0 | {1,5} | 101 | mandatory |
| minimum | 0 | {1,4} | 120 | mandatory |
| minimum | 1 | {1,2} | 104 | mandatory |
| minimum | 2 | {1,6} | 100 | mandatory |
| minimum | 3 | {0,4} | 87 | mandatory |
| minimum | 4 | {0,5} | 87 | mandatory |
| minimum | 6 | {1,10} | 104 | mandatory |
| minimum | 10 | {0,12} | 77 | conditional on D=9 |
| maximum | 5 | {1,10} | 126 | mandatory |
| maximum | 7 | {1,6} | 116 | mandatory |
| maximum | 8 | {1,2} | 126 | mandatory |
| maximum | 9 | {1,5} | 133 | mandatory |
| maximum | 10 | {0,5} | 81 | mandatory |

The first two minimum domains are incomparable. The remaining 130-row
minimum-partner-0 domain is redundant. The independent scalar checker
replays all 126 times 2048 = 258048 free assignments with actual marked
values, checking the threshold bridge and every domain entry. Thus
exactly twelve listed activity domains are unconditional and one is
conditional. This does not say these are all useful necessary constraints.

## A first-wire-10 preparation corollary

**Corollary.** If a B11 size-22 completion first uses internal wire 10
in `(4,10)`, some earlier comparator is `(1,4)`, `(2,4)`, or `(3,4)`.
In particular `(4,10)` cannot be the first suffix comparator. This is
not a restriction on every later occurrence of that pair.

**Proof.** In the 101-row minimum-partner-0 slice, bit 0 is always zero
and initially bit 4 is at most bit 10. Until the first wire-10 gate,
bit 10 is unchanged. Without the three listed earlier gates, bit 4
cannot increase: gates with lower endpoint 4 only decrease it; a gate
with upper endpoint 4 has lower endpoint 0 and hence zero input; and
all other gates preserve bit 4. Also bit 0 stays zero under every
ordinary comparator. Thus `(4,10)` at the first wire-10 use swaps no
slice row. The minimum partner remains at internal 0, so `(4,10)` is
retained by this saturated pruning. Lemma 2 gives a contradiction. The
checker audits the invariant on all 32256 Boolean state/gate transitions
on wires 0 through 9 excluding the three preparation gates. □

**Further corollary.** If the first wire-10 comparator is `(4,10)`,
its minimum part is unary. Hence its effective profile word has eleven
events, all 126 strongest families have D=9, and all thirteen listed
slice requirements are mandatory in this branch.

**Proof.** Each required earlier comparator has upper endpoint 4 and
therefore sends any positive minimum partner weight at 4 to its lower
endpoint, leaving port 4 empty. An empty minimum port cannot refill
before the first wire-10 comparison: every other positive weight is at
least 64, so doing this would be a unary event costing at least 64,
whereas the available slack is only 32. Equivalently, once port 4 has
become empty, every admitted pre-first-touch profile transition preserves
its emptiness. Thus the first `(4,10)` merges (0,32), a minimum unary
part. Apply the parent's event count and Lemma 1. □

Both algorithms check all 603 pre-first-touch edges with empty port 4
and all 184 preparation edges. Consequently 76 parent first-wire-10
edges with partner 4 and a minimum binary part are excluded as candidate
sorting trajectories. The 100 unary first-4 edges are only remaining
relaxation edges; no sorting completion is asserted for them. The parent
profile hashes retained in the certificate refer to the entire parent
language, before this additional necessary restriction.

Initially the imported profile language allows 18 comparator choices.
The mandatory slice activity test rules out `(4,10)` and leaves 17.
No existence assertion is made for any of the remaining choices.

## Controls and trust boundary

Both programs sort all 158 B11 rows with the published 23-comparator
control and all 8192 original rows with its full size-45 lift. This
control starts with `(7,10)`, demonstrating that the size-44 first-touch
language must not be imposed on a larger control. Duplicating its first
gate gives a size-46 full sorter with an inactive retained comparator
in the minimum-partner-0 slice; activity must be conditioned on actual
size-bound saturation.

A private native SAT probe with these new necessities used all 55 pairs
in 22 sequential slots and all 158 rows. Its 30000-conflict cap was
reached (30014 actual conflicts), returning UNKNOWN in 14.592 solver
seconds. The independently checked size-23 calibration satisfied all
1914346 generated clauses. These are operational evidence only and
are not premises of the lemmas. No solver exclusion, certificate of
B11 nonexistence, or numerical bound improvement is asserted.

The proof imports S(11)=35, the published P19 equivalence, the parent
coupled-profile coverage and its first-touch exclusions, and the written
marked-pruning/standardization argument. Large historical proof corpora
are not replayed here. The induction, slice bridge, and pruning argument
are written mathematics rather than proof-assistant formalizations.
The two computational implementations are by this researcher; they are
not external-person review. The global S(13)=44..45 and B11=22..23 gaps
remain open.
