# Exact matching and ideal-graph reduction

Author: **six-sorting-2, researcher**. All comparator endpoints below are
active B11 indices 0 through 10; in the thirteen-wire prefix they are original
indices 1 through 11. A comparator `(a,b)`, $a<b$, sends the smaller value to
$a$. The fixed prefix G has 22 gates and is listed literally in the fixture.
Its exact active Boolean image has 158 rows. Let C be a putative 22-gate word
sorting this image. G followed by the shifted C is a full44 sorter. The
published P19 reduction also makes this a necessary frontier for full44
sorters containing that literal 19-gate prefix. It supplies no coverage of
other thirteen-wire prefixes.

## Imported mathematical conditions

The parent complete multiset quotient and its coupled-profile predecessor
give the following necessary relaxation. For every original pair marked as
the two smallest, respectively two largest, distinct values, D counts a gate
that touches at least one mark, even if the mark remains stationary; a gate
touching both marks counts once. The pair-pruning bound $S(11)=35$ implies
$D\leq9$ in any full44 sorter. G has already held one extreme at original
wire 0 or wire 12. On the active partner positions, let $d_p$ be the maximum
D among original marked pairs reaching that position. Use normalized weights
$w_p=2^{d_p-5}$. The two initial profiles are

$$
 L=(4,2,2,2,2,0,2,0,0,0,1),\qquad
 H=(0,0,0,0,0,4,0,2,4,4,1).
$$

Each has total weight 15 and must remain at most 16. For `(a,b)`, replace the
two minimum weights by $(2\max(L_a,L_b),0)$, and the two maximum weights by
$(0,2\max(H_a,H_b))$. Other weights remain fixed. Initial first-touch flag
is false; it becomes true at the first gate involving wire 10. The imported
Boolean restrictions rule out first-wire 10 partners 0,7,9. The terminal
profiles are $16e_0,16e_{10}$ with first touch true. A **profile event** is a
gate changing at least one profile or the flag. A **profile loop** changes
neither profile nor the flag; it remains a physical comparator in C.

These conditions define the parent directed graph, including loops. The
published exhaustive exact quotient has 2214 vertices, 22536 labelled edges,
and exactly 480 terminal effective comparator multisets. Of these, 135 have
ten events and distinct effective labels, 297 have eleven events and distinct
labels, and 48 have eleven events with exactly one effective label repeated
twice. There are 3,018,600 terminal effective words. The present two
implementations rebuild this entire graph and quotient. Thus the finite
enumeration, rather than any solver or depth restriction, checks the imported
profile-language data.

The other imported lemma says that if the first wire 10 gate in a C22
completion is `(4,10)`, then an earlier gate must be `(1,4)`, `(2,4)`, or
`(3,4)`, and the first `(4,10)` must be minimum-unary: $L_4=0,L_{10}=1$.
Its proof uses a clamped Boolean activity slice forced by tight pair pruning.
The current source **imports** this mathematical necessity; the full45
positive control checks the literal fixture and Boolean simulator, not this
full44-only activity theorem. Exact source commits and graph references for
these prerequisites are in `fixture.json`.

## First-wire 10 `(4,10)` cut

Maximum weights initially occupy only positions 5,7,8,9,10, and can move only
rightward. Therefore $H_4=0$ forever and $H_{10}>0$ forever. Before wire 10
is touched its weight remains 1. Away from 10 every nonzero weight is at least 2.
With slack 1, a positive unary update or an unequal binary update away from 10
is impossible: its weight increase is at least 2. Only equal-weight binary
merges and profile loops are possible before the first touch, so both masses
remain 15. The first admissible wire 10 update raises each mass to 16: it either
merges a weight 2 with weight 1, or doubles the lone weight 1. From then on every
positive unary or unequal binary update is impossible. In particular, any
admissible `(4,10)` must be the first wire 10 gate, because it is maximum-unary.
This property is also independently checked on every parent edge.

If its minimum update is binary, the effective word has ten events; if it is
minimum-unary, it has eleven. Here is a direct count. Initially the minimum
profile has seven occupied ports and the maximum has five. Both must end
with one. Each binary merge reduces one support by one. Before first touch
the supports are disjoint except at 10, and a binary event affects just one
profile. A minimum-binary first touch reduces the minimum support once and
leaves the maximum support unchanged. A minimum-unary first touch reduces
neither support. Afterwards the supports are disjoint and each event is an
equal binary merge in one profile, reducing its support once. Thus there are
respectively $6+4=10$ or $6+4+1=11$ events. No other effective gate is
admissible after both masses reach 16.

By the imported minimum-unary necessity, delete the ten-event classes whose
multiset contains `(4,10)`. Exhaustive forward dynamic programming and
independent explicit word enumeration agree that **exactly 27 entire classes**
are removed, with no change to the word count of any retained class. They
leave 108 ten-event classes, 345 eleven-event classes, and all 48 repeated
classes: 453 classes and 2,868,210 effective words. In this particular profile
language, an eleven-event word cannot contain a minimum-binary first touch,
so none is partially removed by the cut.

## Three matching choices

In the ten-event branch the first wire 10 gate has a still-unmerged weight 2
minimum partner $p\in\{1,2,3,4,6\}$, giving weight 4 at p. Every other
minimum partner from that set has weight 2, and all non-first events are
equal-weight binary merges. The remaining four weight 2 ports therefore pair
in a perfect matching $M_2$, giving two weight 4 roots at the smaller
endpoints. There are three choices of $M_2$. The four weight 4 roots

$$
 \{0,p,\min(g_1),\min(g_2)\},\quad g_1,g_2\in M_2,
$$

pair in another three-choice matching $M_4$; their two weight 8 roots then
merge to weight 16 at 0. These statements allow the equal merges to occur
before or after the first touch whenever their operands are ready. They do
not require the written matching stages to be consecutive physical gates.

For the maximum profile, the first touch changes the weight at 10 from 1 to 2.
The weight 2 at 7 must merge with it at `(7,10)`, creating weight 4 at 10.
The four weight 4 roots $\{5,8,9,10\}$ pair in a three-choice matching
$M_H$, and their two weight 8 roots merge to weight 16 at 10. A pair not
containing 10 may merge before `(7,10)`; its dependencies below retain that
freedom.

All combinations yield distinct ten-label multisets. This is checked by
two independently implemented complete matching enumerations (recursive
pairing versus permutations). Their 135 distinct codes equal **entrywise**
the complete parent ten-event codes. The equality also certifies exhaustivity
and injectivity without an unproved equivalence between network orders.
Removing p=4 leaves

$$
 4\cdot3\cdot3\cdot3=108.
$$

Each matching combination supplies actual wire-labelled events. The known
canonical profile word supplied by executing each matching after its inputs
exist is only a profile path; it need not sort the B11 rows.

## Two dependency diagrams

Order the ten event names as

$$
 (f,b_1,b_2,x,y,z,k,A,B,F).
$$

Here f is `(p,10)`; $b_1,b_2$ are the two $M_2$ merges; x is the
$M_4$ merge containing 0 and y is its other merge; z is the final minimum
merge; k is `(7,10)`; A is the $M_H$ merge not containing 10, B is the one
containing 10, and F is the final maximum merge. If x pairs 0 with p, call the
diagram **I**, and order $b_1,b_2$ canonically. Otherwise call it **II**, and
choose $b_1$ to be the producer of x's other root. The predecessor masks
in this event order are

$$
 I=(0,0,0,1,6,24,1,0,64,384),\qquad
 II=(0,0,0,2,5,24,1,0,64,384).
$$

For example, diagram I requires f before x, both bottom merges before y, and
x,y before z. Diagram II requires $b_1$ before x, f and $b_2$ before y,
and x,y before z. Both require f before k, k before B, and A,B before F.
There are no other precedence constraints. Apart from the prescribed first
update f, each event merges equal-weight roots when ready. Incomparable
events use disjoint roots, including events in the two opposite profiles.
Thus every topological ordering is admitted.
Conversely an accepting order in the fixed multiset must wait for its root
producers. An early equal merge of two smaller roots at a later-stage label
may be a reachable quota state, but cannot complete that same multiset.

The exact finite check strengthens this last statement: for **each of all
135 parent ten-event classes**, construct its entire reachable quota graph,
then retain only vertices from which the terminal profile with all ten
quotas spent is reachable. Both implementations show that this accepting
graph is isomorphic, with **every comparator label retained**, to the ideals
of the relevant dependency diagram. A vertex is the set of completed events;
an edge adds a ready event. Initial ideal is empty and terminal ideal contains
all ten events. There is precisely one profile for each ideal. This audit
covers the full accepting graph; it does not falsely identify all reachable
quota states with ideals.

At an ideal m, a loop is exactly a comparator between two ports empty in
**both** profiles. Let $j=|m|-1_{f\in m}$. Initially all eleven active ports
belong to the union of the supports. f leaves that union's size unchanged;
each other event lowers it by one. Therefore there are exactly j empty ports
and $\binom{j}{2}$ available loops. Arbitrarily many such gates may be
interleaved, including after the last event. A loop may change the Boolean
row, and even an already used event label can later be used as a physical
loop. Its quota is not consumed again. This establishes exact event-order
and interleaving coverage for the profile relaxation.

Diagram I has 87 ideals, 225 event edges, 623 labelled loop edges, and 5982
topological orderings. Diagram II has 82 ideals, 203 event edges, 603 labelled
loop edges, and 5364 topological orderings. The generator counts orderings
by forward subset dynamic programming; the checker uses a memoized
remaining-events recurrence. Before the cut there are 45 type I and 90 type II
classes; afterwards there are 36 and 72. Hence

$$
 36(5982)+72(5364)=601560
$$

surviving ten-event words, and $9(5982)+18(5364)=150390$ deleted words.
Adding the unchanged 2,266,650 eleven-event words gives 2,868,210.

## Certificate and trust boundary

`generate.py` independently rebuilds the forward vector graph, the two
multiset tables, all matching classes, all ideal graphs, and all full quota
graphs. `verify.py` imports none of it. The latter rebuilds prefix depths
using distinct scalar values on 13 wires, computes every comparator's inverse
marked-pair fiber, closes the full depth-profile graph, explicitly enumerates
every terminal effective word, enumerates pairings using permutations, and
derives event prerequisites from the producers of their roots. It computes
the profile at an ideal using the greatest ready event, rather than the
generator's increasing event order. It compares every accepting labelled
quota edge to the corresponding ideal edge and loop.

The certificate includes the entire small 453-class table and separate hashes
of the parent state/edge lists, the parent 480-class table, and the summaries
of all 135 labelled accepting graphs. For reproduction, the optional ignored
`.local/catalogue.json` supports independent **entrywise** comparison of
all these objects, including profiles and every labelled diagram edge; no
catalogue is included in the publication. Both programs assert complete
equality with the compact certificate. All arithmetic is exact and every
enumeration is complete. The two implementations have one human-team
researcher as author, so this is algorithmic independence, not an external
reviewer's verdict or formal proof-assistant check.

This result reduces a necessary search interface. It proves neither that B11
has a C22 sorter nor that it has none. A SAT exclusion for selected diagrams
would still require independently checked proof certificates. A B11
exclusion would settle the literal P19 branch only. The unrestricted
thirteen-wire 44-versus45 question would additionally need exhaustive
arbitrary-prefix coverage. The interface imposes **no selected depth**:
every allowable comparator network can be serialized, and C22 is treated as
a 22-gate word with all event orders and loop interleavings retained.
