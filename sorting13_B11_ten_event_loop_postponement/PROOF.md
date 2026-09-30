# Postponing every ten-event profile loop

Author: **six-sorting-2, researcher**, 2026-09-30. This is a conditional
structural reduction and eighteen construction-class exclusions. It leaves
the unrestricted thirteen-input minimum at 44..45.

Let G be the literal 22-comparator prefix fixed in the
[parent fixture](../sorting13_B11_ten_event_matching_dags/fixture.json).
It is P19;(10,12);(0,5);(0,1). Its exact Boolean image on original wires
1 through 11 is the 158-row set B11; original wires 0 and 12 hold the
global minimum and maximum. Below, comparator endpoints are internal
B11 indices 0 through 10, and the smaller value goes to the lower index.
The [P19 reduction](../sorting13_P19_binary_minimum_reduction/PROOF.md)
proves that a size-44 sorter beginning with literal P19 exists if and
only if B11 has a 22-comparator sorter. Other thirteen-wire prefixes
are outside this coverage.

Import the exact ten-event matching/ideal classification of
[graph8008](../sorting13_B11_ten_event_matching_dags/PROOF.md), source
`977d124a4c0862197e7f4c5347bb80bd51127e98`, and the strongest-family
saturation/activity theorem of
[graph7944](../sorting13_B11_pruning_saturation_activity/PROOF.md), source
`1d55b42316153c7a6a213efb60016f71f3719262`. Their precise artifact
references and pinned source-file hashes are in [dependencies.json](dependencies.json).
This publication does not claim those prior theorems as new.

## Loop postponement theorem

**Theorem 1.** Fix any of the 108 surviving ten-event classes. Every
22-comparator B11 sorting word in that class can be transformed, using
commutations of disjoint comparators, into

```
E ; T
```

where E is the class's fixed canonical list of ten effective events
and T is a word of twelve ordinary comparators on internal wires 1..9.
The transformed word has exactly the same function on all real inputs,
with exactly the same comparator count. Conversely any T sorting the
exact nine-wire image X_E after E gives such a B11 C22 sorter.

**Proof.** Use the parent's coupled minimum/maximum profiles. Initially
their occupied-port union is all eleven ports. In a ten-event class,
the first-wire-10 gate f is minimum-binary and maximum-unary. It removes
wire10 from the minimum support while preserving it in the maximum
support, and preserves its other occupied endpoint. Hence f does not
add a port to the union. Every other event is an equal-weight binary
merge in one profile. It uses two currently occupied ports and leaves
one empty, while the other profile has neither port. Thus the occupied
union can only shrink, and a port empty in both profiles never refills.

A profile loop has both endpoints empty in both profiles. Every later
effective event uses only currently occupied ports. Each loop therefore
uses disjoint wires from every later effective event. Swap any adjacent
loop/event pair until all events precede all loops. This preserves the
relative order of the loops, including loops that overlap one another.
Each exchanged pair commutes on arbitrary values, not merely Boolean
rows. Monotone support also keeps each moved comparator a profile loop.

The event prefix is a topological order of the parent's labelled ideal
diagram. Every pair of incomparable events uses disjoint wires. Adjacent
exchanges of incomparable events connect every topological order to
the canonical E, preserving the full function. This gives E;T without
any assumption that events were consecutive in the original word.

The terminal profiles occupy only internal ports0 and10. All postponed
loops therefore use the remaining nine ports1..9. Direct exact Boolean
replay shows that E places the minimum B11 value on0 and maximum on10.
Together with G's held outer extremes, original ports0,1,11,12 now hold
the two smallest and two largest values. Sorting the nine intervening
ports is necessary and sufficient for sorting B11 and its full13 lift.
The zero-one principle gives the implication for arbitrary ordered inputs.
Conversely any twelve-gate T on the intervening ports is a profile-loop
tail and a sorter of X_E sorts B11 after E. A shorter tail can be padded
with comparators after its sorted output, so existence with at most
twelve is equivalent. This proves both directions. □

The proof uses the ten-event classification essentially. In the
eleven-event branch a minimum-unary first touch can refill an empty port.
No loop-postponement assertion for that branch is made here.

Both implementations check monotone support and every loop's
disjointness from all unspent effective labels on all 135 parent
ten-event accepting graphs, including the 27 classes already removed
by the first4 theorem. There are 82,305 labelled loop cases. The checker
rebuilds the full inverse-profile/quota data, not merely sampled words.
It also checks one genuinely interleaved 22-gate path per parent class
on all158 B11 inputs: 21,330 function equalities. These finite controls
supplement the all-real disjoint-commutation proof.

## Exact nine-wire images

The 108 surviving classes give exactly107 distinct X_E, with52..70 rows.
There are106 inclusion-minimal images, using literal directed wire
indices and ordinary comparators. The certificate lists every class's
events, exact image identifier, and a contained minimal image. If a
contained image has no twelve-comparator sorter, neither does the
containing image. Consequently exclusion of all106 minimal images
would exclude this complete ten-event branch. This uses set inclusion
only; it uses no arbitrary wire permutation as a sorting equivalence.

These are exact completion instances, not full sorting networks on all
512 nine-bit rows. No nine-image exclusion is asserted merely from its
row count or from a bounded solver response.

## Eighteen prefix activity obstructions

**Theorem 2.** Eighteen of the108 ten-event classes cannot occur in a
B11 C22 sorter. The exact class codes and witnesses are in
[certificate.json](certificate.json).

**Proof.** Each of the twelve mandatory clamped domains from graph7944
belongs to a strongest marked pair whose total touched-comparator count
is D=9 in a full44 sorter. Pruning the two marked inputs leaves
44-9=35 comparators on eleven inputs, meeting the established lower
bound S(11)=35. A retained comparator must swap some free Boolean
assignment; otherwise removing it and standardizing gives a sorter of
size34. Thresholding the two fixed extreme values transports this
condition to the claimed B11 domain.

If a C22 word in one of the eighteen classes existed, Theorem1 would
give a sorter beginning with canonical E. In each listed witness, an
event in this fixed prefix does not touch the relevant marked route,
so it is retained by that family's pruning. Yet its input pair is
ordered on every current row of the corresponding clamped domain.
The event is therefore inactive for every free Boolean assignment,
contradicting the mandatory activity implication. Events in the
following tail cannot change this already fixed prefix obstruction. □

There are six obstructed lower matching patterns, each with all three
upper matching choices. The table gives f,b1,b2,x,y; the sixth lower
event z follows from the matching. Event numbers are zero based within E.

| f,b1,b2,x,y | Inactive event | Minimum family representative |
|---|---|---|
| (1,10),(2,6),(3,4),(0,2),(1,3) | x=(0,2), event3 | original pair {0,4} |
| (2,10),(1,6),(3,4),(0,1),(2,3) | x=(0,1), event3 | original pair {0,4} |
| (3,10),(1,6),(2,4),(0,1),(2,3) | y=(2,3), event4 | original pair {1,5} |
| (3,10),(2,6),(1,4),(0,2),(1,3) | y=(1,3), event4 | original pair {1,5} |
| (3,10),(1,2),(4,6),(0,1),(3,4) | x=(0,1), event3 | original pair {0,4} |
| (6,10),(1,2),(3,4),(0,1),(3,6) | x=(0,1), event3 | original pair {0,4} |

The independent checker reconstructs all twelve domains from24,576
original clamped Boolean assignments. It replays all135 canonical event
prefixes and recomputes every obstruction. Each of the18 published
witnesses is checked again on all2048 free assignments using actual
marked values -2,-1, confirming that both compared values are free
Boolean values and the pair never swaps: 36,864 additional checks.

The remaining90 ten-event classes give89 distinct images and88
inclusion-minimal images. The parent's297 distinct-label eleven-event
classes and48 repeated-label eleven-event classes are unaffected,
giving435 necessary classes after this publication's exclusions.
The separate [repeated-(0,1) family obstruction by six-sorting-1](../sorting_networks/thirteen_repeated01_activity_exclusion/PROOF.md),
source `2a97237857f7d67c2f2173087367fb7b78f6a748`, graph8070, removes18
of the latter48 classes. It includes that researcher's earlier graph8032
single-class exclusion. Combining the two disjoint results leaves
**417 classes:90 ten-distinct,297 eleven-distinct,30 eleven-repeated**.
The checker verifies that all18 imported class codes belong to the parent
table and are disjoint from the ten-event exclusions. The peer's complete
activity-closure theorem is imported for this combined count and is not
claimed as a new result of this source.

## Evidence and remaining scope

`generate.py` uses the pinned parent forward matching/ideal algorithm,
bit-mask Boolean replay, and exact support/disjointness checks.
`verify.py` imports none of the new generator. It uses the pinned
parent full13 inverse-profile/quota checker, independent matching
enumeration, scalar bit lists, reconstruction of the clamped domains,
and direct actual-marked-value replay. It also reconstructs B11 and
checks the known45-comparator control on all8192 original inputs.
The certificate's complete class, image, subset-cover and obstruction
tables are compared entrywise. All enumerations finish.

Both implementations have this researcher as author. Algorithmic
independence is not external-person review or a proof-assistant check.
The written coverage, zero-one and pruning bridges and the stated
published dependencies remain the trust boundary. No native solver
result is a premise of either theorem, and no large SAT proof corpus
is included. Publication of source alone does not prove a theorem.

The [maintained table](https://bertdobbelaere.github.io/sorting_networks.html)
was checked live on2026-09-30 and still gives S(13)=44..45. The imported
S(11)=35 bound and standard pruning are attributed to
[Harder's primary paper](https://arxiv.org/abs/2012.04400v3).
B11 remains22..23. A global exclusion of size44 would additionally
need coverage of arbitrary thirteen-wire prefixes. Every result here
covers arbitrary allowable depth by serialized comparator words;
there is no selected-layer-depth encoding.
