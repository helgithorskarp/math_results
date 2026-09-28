# Three-colour trades and exchange components

Throughout, sum-free excludes every equation `x+y=z`, including `x=y`.
The Schur number convention is the largest colourable interval endpoint.

## 1. The exact finite statements

Let `F` be the supplied Fredricksen--Sweet colouring of `[1,536]`.
For every three-element palette `T` contained in `{1,...,6}`, put

    U_T = {x in [1,536] : F(x) in T} union {537}.

**Statement A.** None of these 20 sets `U_T` is three-colourable without
a monochromatic Schur triple.

Let `G` be any of the three explicit 537-entry near-colourings in
`fixtures.json`. Its complete list of violations is checked directly. All
violations lie in one old colour `b`: `b=4` for `near537`, `b=1` for
`team_near_190`, and `b=2` for `team_near_359`.
For each three-element palette `T` containing `b`, put

    V_T = {x in [1,537] : G(x) in T}.

**Statement B.** None of these 30 sets `V_T` is three-colourable without
a monochromatic Schur triple.

For each of these 50 cases, `certificate.json` supplies a subset `W` of
the relevant set. The checker verifies the subset relation and proves `W`
not three-colourable by the exhaustive algorithm justified below. A colouring
of a larger set restricts to a colouring of every subset, so these witnesses
prove A and B. Minimality or optimality of the witnesses is not asserted.

Two external-candidate cases have especially transparent witnesses:
for palette `{2,4,6}`, the witness is `6*{1,...,14}`, and for `{4,5,6}` it
is `12*{1,...,14}`. These are dilates of the classical obstruction
`S(3)=13`; the checker also proves their non-colourability directly.

## 2. Interpretation as colour trades

A trade on a palette `T` recolours every member of the old classes labelled
by `T`, using only labels in `T`, while leaving all other classes fixed.
For extension from 536, the new integer 537 must also receive a label in `T`.

When the unchanged classes are sum-free, such a trade succeeds if and only
if the union of the selected old classes, with the new endpoint when
applicable, has a sum-free colouring using `|T|` colours. Indeed, monochromatic
triples in unchanged colours are excluded by hypothesis. Every other
monochromatic triple lies entirely in the selected union. Thus A excludes
every three-colour extension trade, and B excludes every three-colour repair
trade containing the defective old colour. A palette omitting that colour
leaves its old violation unchanged.

Trades on smaller palettes are excluded too. If a trade on at most two
labels succeeded, enlarge its palette to three labels and leave the added
old classes unchanged. Those classes are sum-free and their labels are
disjoint from the successful smaller palette. This would give one of the
three-colourings already excluded in A or B.

## 3. A necessary condition on every possible repair

For an old assignment `H` and a hypothetical valid new colouring `C`, form
an undirected graph on the six colour labels. Add an edge `{H(x),C(x)}`
whenever they differ, for every integer present in both assignments.

For each connected component `T`, an old vertex has `H(x) in T` if and
only if it has `C(x) in T`. This follows immediately because both ends
of every edge lie in the same component.

In the baseline case take the component containing `C(537)`. The new
colouring restricted to the old classes in that component and 537 would
be a successful trade on `T`. By A and the smaller-palette argument,
this component has at least four labels.

For any of the three near-colourings, take the component containing its
defective old colour `b`. Restricting `C` to the union of these old
classes gives a successful repair trade. All old classes outside `T`
are sum-free, since `b in T`. B therefore implies `|T|>=4`.

This is a condition on labels connected by exchanges. It is not a lower
bound on how many entries change, or on how many old classes have entries
removed: one old class might send entries to several other labels.
Nor does the theorem exclude fixing some whole classes while allowing
new entries to be added to them. Such additions can connect a fourth label
to the component and fall outside a three-colour trade.

The assertions hold for every valid `C`, including every global renaming
of its colours. The same statements transfer under a simultaneous global
renaming of the labels in the explicit input and conclusion.

## 4. Exact enumeration and its trust boundary

For a positive finite set `W`, the checker forms one edge for each distinct
support `{x,y,x+y}` contained in `W`. Edges have size two or three; the
size-two edges represent repeated summands. A colouring of this hypergraph
is exactly a sum-free colouring of `W`.

Every vertex initially has all three colour choices. One supplied root is
fixed to colour 0: every possible colouring can be globally renamed to
have that root colour, so this loses no existence case. The root affects
runtime only and is checked to lie in `W`.

Whenever all but one distinct vertices of an edge have the same singleton
colour `a`, the remaining vertex cannot have colour `a`. Deleting that
choice is sound. The queue implementation visits every edge containing
each newly singleton vertex. For a two-vertex edge it deletes that colour
from the other endpoint. For a three-vertex edge it does so precisely
when a second vertex has the same singleton colour. Every premise becoming
true is therefore processed. A zero domain certifies impossibility of
the current branch.

After propagation, choose a vertex with at least two remaining choices
and recurse once for **each** of them. All remaining possibilities are
covered. Each branch fixes a previously unfixed vertex, so the recursion
terminates. A terminal assignment is checked against every edge. Returning
no model after exhausting all branches proves non-colourability. No
heuristic cutoff, random search, learned clause, SAT output or floating
point enters this verification.

The original witnesses were found with a separate guarded one-hot SAT
encoding and greedy vertex deletion. That discovery process, provided as
`discover.py`, is outside the proof's trust boundary. An erroneous solver
or deletion routine would only propose a bad witness; the independent
checker would reject it. The proof relies on exact Python integer operations,
the supplied finite input, exhaustive enumeration, and the reduction above.
It has not been formalized in a proof assistant.

## 5. Scope

No unrestricted upper bound for `S(6)` follows. No valid colouring of
`[1,537]` is supplied. Four- or more-colour trades, different starting
assignments and other construction mechanisms remain available. The
practical exclusion is of all repairs confined to at most three labels
in these particular assignments, even when arbitrarily many entries
within those labels may change.
