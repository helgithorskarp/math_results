# Opposed B214 copies give a strict physical relation gain, but native A159 does not amplify it

This package freezes one exact, cap-feasible whole-composition experiment for
the Hadwiger--Nelson construction campaign.  It starts with the ten-point
Golomb graph and places two copies of Parts' 214-point distance-three forcing
gadget on opposite collinear extensions of a diameter.  Exact collision
merging gives a **343-point, 1,782-edge** strict plane unit-distance graph.

The support is not five-chromatic: its chromatic number is exactly **four**.
Nevertheless, the complete unrestricted four-colour relation on the ten
Golomb vertices drops from 95 canonical patterns to 66.  This is a genuine
whole-composition gain caused by the physical interaction of the two gadgets,
not merely the intersection of their isolated relations.  The canonical
pattern `0121212203` extends through each isolated B214 copy, but a checked
RUP refutation proves that it cannot extend through their complete physical
union.

The one declared cap-feasible finishing step places the full native A159
gadget in the same coordinate frame.  Of its 159 points, 143 already occur in
the opposed support, so it adds only 16 points.  The resulting complete graph
has **359 points and 1,893 unit edges**, including 32 new cross-contact edges.
Its exact Golomb relation is still the same 66 patterns, and it has a literal
proper four-colouring.  Thus the native A159 completion is relation-neutral
and the selected source/operation is retired at this boundary.  No rotations,
translations, nearby copy counts, or alternative frames are classified here.

This is a positive local interaction theorem followed by an exact construction
stop.  It is **not** a five-chromatic graph, a record candidate, or a restricted
family theorem about arbitrary A159/B214 placements.

## Exact construction

All coordinates are represented at common scale 36 in the real basis

```text
1, sqrt(3), sqrt(11), sqrt(33).
```

The Golomb vertices are the usual unit hexagon together with its three inner
points.  For the archived B214 coordinates, whose marked terminals are
`+3/2` and `-3/2`, use the two isometries

```text
L(x,y) = (x-1/2, y),
R(x,y) = (-x+1/2, y).
```

Thus the marked pairs become `(1,-2)` and `(-1,2)`.  Each transformed B214
contains all ten Golomb points.  The two transformed copies overlap in 85
physical points; adding the ten already-contained Golomb labels accounts for
95 label collisions in the 438-label construction.  Reconstructing all
unordered point pairs gives 1,674 distinct inherited component edges and 108
additional cross-copy unit contacts.

For the second support, adjoin A159 with its archived coordinates and no
further isometry.  Exact merging leaves 359 points.  Its complete edge graph
has 1,893 edges; the verifier records the inherited/contact split and checks
every pair directly.

## Complete relation certificate

The unit triangle on Golomb vertices `0,1,2` fixes colours `0,1,2`, removing
global palette symmetry.  Exhausting the remaining seven Golomb vertices
gives 95 canonical proper four-colour patterns.

The certificate contains a full proper colouring of the 343-point graph and
the 359-point graph for each of the 66 surviving patterns.  The verifier
checks all 132 words against the freshly reconstructed complete edge lists and
checks their ten-vertex projections.

The complement consists of 29 patterns.  One CNF asks whether the 343-point
graph has a proper four-colouring whose normalized Golomb projection is any
one of those 29 patterns.  It has 1,401 variables and 9,823 clauses.  The
deletion-free `excluded.rup` file contains 1,382 RUP additions ending in the
empty clause.  `verify.py` regenerates the CNF, checks its SHA-256, and replays
every lemma using its own watched-literal unit propagator.  No SAT library or
solver verdict is trusted during proof replay.  Because the 343-point graph is
a subgraph of the 359-point completion, the same exclusion applies to the
larger support; its 66 positive words prove that A159 leaves the relation
unchanged.

The RUP trace was produced by CaDiCaL 3.0.1 and trimmed to its addition-only
core with `drat-trim`.  As a cross-check, the published trace was independently
accepted by `drat-trim -U` against the regenerated CNF.

## Reproduce

From the repository root, using CPython 3.11 or later and only the standard
library:

```sh
python3 -B hadwiger_nelson_golomb_opposed_b214_stop/verify.py --check-expected
python3 -O -B hadwiger_nelson_golomb_opposed_b214_stop/verify.py --check-expected
sha256sum -c hadwiger_nelson_golomb_opposed_b214_stop/SHA256SUMS
```

On the producing host each verifier run took about five seconds.  To emit the
exact CNF for a separate proof checker:

```sh
python3 -B hadwiger_nelson_golomb_opposed_b214_stop/verify.py \
  --check-expected --write-cnf /tmp/golomb-opposed-b214.cnf
drat-trim /tmp/golomb-opposed-b214.cnf \
  hadwiger_nelson_golomb_opposed_b214_stop/excluded.rup -U
```

The second command is optional and requires an independently obtained
`drat-trim` binary.  The standard verifier already checks the RUP proof.

## Scope and campaign consequence

The 343-point support passes the forcing-feature admission gate: the displayed
cross-component pattern has separate lifts but no joint lift, and the full
relation is strictly smaller than the bare Golomb relation.  The native A159
addition is a concrete capped continuation, not a speculative budget: it is a
fully reconstructed 359-point physical graph.  Its unchanged relation and
proper four-colouring trigger the construction stop.

In particular, this package does not authorize an angle, phase, shell, copy,
or alternate-root sweep.  A future use of the 343-point relation would need an
independently motivated exact finishing operation that attacks the surviving
66 patterns; none is claimed here.  Parts' 509-point graph therefore remains
the supported unrestricted order record.

## Sources

- Jaan Parts, [Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane](https://arxiv.org/abs/2010.12665).
- The exact archived A159/B214 transcriptions and their provenance are pinned
  in [`../hadwiger_nelson_nonmono159_214_lowden2`](../hadwiger_nelson_nonmono159_214_lowden2/README.md).
- The exact Golomb coordinates agree with the source used in
  [`../hadwiger_nelson_golomb_direction_ball`](../hadwiger_nelson_golomb_direction_ball/README.md).

