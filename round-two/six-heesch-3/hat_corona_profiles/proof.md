# Complete surrounds force flat full-port hat profiles

Author: **six-heesch-3**, role **researcher**, 2026-10-01.

## 1. Reference geometry and precise scope

Use axial coordinates with Euclidean embedding

\[
 L(x,y)=(x+y/2,\sqrt3\,y/2).
\]

Let \(U=\{(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)\}\), and let
\(C=\{(x,y)\in\mathbb Z^2:y\equiv0\pmod2,\ x-y\equiv0\pmod6\}\).
A kite cell is indexed by \(p=c+v\), with \(c\in C\), \(v\in U\).
This representation is unique. Write \(v^+=(-v_y,v_x+v_y)\) and
\(v^-=(v_x+v_y,-v_x)\). Its counterclockwise vertices are

\[
 c,\quad p+v^-,\quad p+v,\quad p+v^+ .
\]

These are the kites of the usual \([3.4.6.4]\) Laves tiling.
Each cell has Euclidean area \(\sqrt3\). A hat consists of the eight cells
and has the 14 boundary ports specified in input.json. Cancelling internal
oriented kite edges yields precisely the listed port cycle. The only
artificial endpoint subdivides the length-two side into two unit ports.
There are eight unit ports, six length-\(\sqrt3\) ports, and area
\(8\sqrt3\).

An **aligned reference hat** is an image under one of the twelve linear
isometries preserving the axial lattice, followed by a translation in
\(C\). Reflections are included. After applying a common isometry, the
root may be taken to have the identity pose.

For a set \(S\) of occupied kite cells, let \(\mathcal H(S)\) be all
unoccupied cells sharing any edge or vertex with \(S\). Covering this halo
by nonoverlapping aligned hats is a complete surround. It is exactly the
condition that the union of \(S\) lie in the interior of the enlarged
union: an uncovered incident cell leaves uncovered points arbitrarily near
its shared vertex, whereas covering all incident cells covers each local
star. Iteration gives complete surrounds. Holes, pinches and temporarily
enclosed regions are permitted throughout the search. A **disk final
union** has the additional usual topological-disk requirement. Taking
extra filler hats is allowed in the theorem.

The reference ports specify a system of normal-profile matching equations.
For each original port \(i\), replace its chord by

\[
 v_i+t(v_{i+1}-v_i)+q_i(t)n_i,\qquad 0\le t\le1,
\]

where \(n_i\) is its inward unit normal and \(q_i(0)=q_i(1)=0\).
The same fourteen functions are used on every copy. The result concerns
deformations that retain every matched full port and its reference
endpoint order. Endpoint motion and new poses may also be considered
provided these labelled pairings remain; the conclusion then concerns the
normal functions only. No general endpoint classification is proved here.

## 2. The theorem

**Theorem.** For every aligned hat reference network admitting three
complete surrounds, its full-port equations imply \(q_i\equiv0\) for all
fourteen ports. The same conclusion holds with two complete surrounds
when the final reference union is a topological disk.

These depths are optimal for the reference equations: a disk first
surround and a hollow second surround have a nonzero common profile
solution. This optimality concerns the equations, not an assertion of an
exact finite Heesch number for a physical curved tile.

Thus a different deep aligned hat network cannot evade the profile
obstruction by choosing a different pattern of complete port incidences.
Partial-port matches, new incidences, and unaligned reference placements
require additional analysis. The general finite-seven construction remains
unresolved.

## 3. The matching and odd-walk argument

At any shared full port, the two inward normals are opposite. Projection
onto the common chord fixes the parameters to be either \(t,t\) or
\(t,1-t\), according to endpoint order. Hence

\[
 q_i(t)=-q_j(t)\quad\hbox{or}\quad q_i(t)=-q_j(1-t).
\]

This reasoning also holds for reflected copies: an isometry maps the
tile's inward normal to the image tile's inward normal.

Lift each port to states \(2i+r\), \(r\in\{0,1\}\), carrying
\(q_i(t)\) or \(q_i(1-t)\). For a relation with reversal bit \(e\),
join \(2i+r\) to \(2j+(r\mathbin\oplus e)\). Every graph edge
negates the function. An odd closed walk therefore implies \(F=-F\),
so \(F\equiv0\). All states in its connected component also vanish.
If every component has an odd walk, all fourteen functions are zero.
No finite sampling of \(t\), polynomial-degree assumption, or numerical
curvature argument enters this proof.

The generator uses graph colouring to produce literal odd closed walks.
A separate reader checks their odd length, every edge, component closure,
and connectivity to all 28 states, without relying on the colouring
routine. Bipartite-component counts below are diagnostics, not counts of
independent functions: parameter reversal couples the paired states.

## 4. Complete candidate generation

The twelve axial linear isometries are enumerated directly: each column
lies in \(U\), and the two columns have Euclidean scalar product \(1/2\).
They preserve \(C\). Every aligned hat meeting a target cell can be
enumerated by mapping one of its eight cells to that target, keeping only
translations in \(C\). Full eight-cell footprints must be disjoint from
the occupied patch, including cells outside the target halo.

This produces exactly 58 possible neighbours of the root. An independent
control enumerates all translations in a sufficient coordinate box: its
bounds are the extremal target coordinates minus the extremal rotated-hat
coordinates. It produces the same transformations and footprints.

Every halo-covering tile touches the old patch. Conversely every tile
touching the old patch occupies one of its halo cells. Thus once the halo
is covered, no further disjoint neighbour can be added. The search
enumerates complete neighbour sets, with optional non-neighbour fillers
irrelevant to this extraction.

For the second stage, candidate transformations are generated by composing
each selected first-patch pose with each of the 58 relative-neighbour
poses. An independent control aligns all eight prototype cells with every
cell of the second halo. These candidate dictionaries agree entry by
entry for all cases considered. In particular, completeness does not
depend on the primary atlas's excluded pair gaps or its intermediate
simple-connectivity pruning.

## 5. Exhaustive cover recursion and exact output

For the first implementation, encode complete footprints as Python integer
bit sets. Select an uncovered halo cell with the fewest compatible hats,
branch over all such hats, and reject full-footprint collisions. Stop
only when every halo cell is covered. If a halo cell has no compatible
hat, reject the branch. Nothing else is pruned.

For the independent implementation, use sets, a fixed reverse coordinate
order, and reversed candidate order. It uses no minimum-choice heuristic
or bit arithmetic. The only additional prune is the same elementary
dead-cell implication. The complete sorted solution lists agree, not just
their counts. Choosing the next uncovered cell deterministically means
each final cover has exactly one recursion path.

The first stage generates 414 surrounds. Their numbers of bipartite
lifted components have histogram

\[
 (0:302),\ (2:92),\ (4:14),\ (6:5),\ (8:1).
\]

The 302 already having no bipartite component need no second enumeration:
adding matched interfaces cannot undo an existing odd walk.
For the other 112, the complete second-surround enumeration produces 1305
patches. Of these, 1301 have odd walks forcing all 28 states. Exactly four
retain bipartite components. Their regenerated poses and isolated gaps
equal exceptions.json exactly.

The bit implementation visits 943 first-stage and 4326 second-stage
nodes; the fixed-order set implementation visits 1117 and 19687. Their
different search trees provide an arithmetic/recursion control. The written
coverage proof remains necessary; agreement alone is not a proof of
completeness.

## 6. The four exceptions cannot acquire a disk or third surround

Each exceptional network has 23 hats. In each, three unoccupied kite
cells have all four edge-adjacent cells occupied. The entire boundary of
each missing kite is therefore present in the union, sealing a missing
region of area \(\sqrt3\). An eight-kite hat cannot be placed in such
a one-kite cavity.

The checker independently enumerates every possible aligned hat covering
each gap, with its entire footprint disjoint from the 23 fixed hats. The
candidate list is empty. It also checks the four occupied neighbours
directly from actual kite faces. The proof uses neither a bounding-box
flood approximation nor an intermediate hole rejection.

Any additional aligned hats disjoint from the fixed patch cannot fill the
sealed cell. Every enlarged union containing it therefore still has a
bounded missing component, so cannot be a topological disk. A third
complete surround would have to cover the cell because it shares boundary
points with the occupied union, which is also impossible.

Given any larger reference two-surround network, extract the root's
neighbours and then the neighbours of that extracted first patch. These
appear in the two complete enumerations. Extra hats only add profile
equations. If the extracted network is one of the four exceptions, its
sealed gap prevents the larger network from being a disk or from admitting
a third collar. Otherwise its odd walks force all profiles. This proves
both assertions of the theorem, including networks with optional fillers.

## 7. Sharpness within the equations

The common first surround of all four exceptions is generated at index17
in the sorted first atlas, and has eight hats. Cancelling all internal
kite edges gives one positively oriented boundary cycle with 44 edges,
every boundary vertex having one incoming and one outgoing edge. Its area
is the sum of its 64 kite areas. In the conforming planar kite tiling this
is a Jordan disk. The checker verifies this boundary, as well as the
complete first and second halo covers.

Let \(f(t)=t^2(1-t)^2\) and choose

\[
 (q_0,\ldots,q_{13})
 =f(t)\,(1,0,0,0,0,-1,-1,0,0,-1,-1,0,0,1).
\]

The vector is nonzero, and \(f(1-t)=f(t)\), with zero endpoint values
and endpoint derivatives. Every full-port relation of the disk first
surround and of each exceptional hollow second surround pairs opposite
entries of this vector. The checker verifies the relation list and the
polynomial coefficient identity exactly. Thus one disk surround, and two
hollow surrounds, cannot force all profiles by these equations.

## 8. Provenance, reproduction and trust boundary

The hat and its tilability are established primary literature:
Smith--Myers--Kaplan--Goodman-Strauss,
[An aperiodic monotile](https://arxiv.org/html/2303.10798v3),
Combinatorial Theory4(1),2024. Their
[hatvalidate](https://github.com/isohedral/hatvalidate) source, commit
38f59ed540d4075f213e98abbadb6bc01d2a64a8, supplies the original eight-cell
coordinates. This checker imports none of its code or atlas. The current
theorem supplies a finite-depth obligation for arbitrary normal functions;
the primary plane-tiling alignment result is not imported as a
finite-corona alignment theorem.

The earlier [25-hat proof](../hat_patch_rigidity/proof.md) is methodological
prior work, with graph reference
bafkreidjfkyzgnxujcwruckzxwrtigukquhuy5de74ypsldb2fkjwmougm.
Its endpoint Jacobian theorem is separate from this profile theorem.

Run the README command. The checker uses only exact integers, sets and
graph walks, with no external solver. expected.json contains the compact
counts and hashes; the four exceptional fixtures are the only published
search patches. Five malformed controls reject. The proof depends on
the stated geometric interpretation, candidate-coverage argument and
auditable finite enumeration. It is an author proof with reproducible
exact computation; no formal proof-assistant or reviewer verdict is
asserted.
