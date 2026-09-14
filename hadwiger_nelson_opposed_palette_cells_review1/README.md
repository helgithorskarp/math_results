# Independent review: opposed palette cells

## Verdict

**ACCEPT with high confidence for the exact physical terminal-relation claim**
at target commit
`169a7bb32bd0cb28e992773199bea21d6c6f3c50`.

The complete strict unit-distance graph specified in the target has 16
distinct plane points and 25 edges.  Its eight terminals are independent and
the graph has chromatic number exactly three.  Of the 2,795 terminal colour
partitions using at most four colours, exactly 2,691 extend to a proper
four-colouring and 104 do not.  Exactly 32 of the forbidden partitions become
extendible whenever any one terminal pin is dropped.  Under the target's
explicit repeated-bichromatic-palette hypothesis, extension occurs exactly
when the two palettes are disjoint.

This is a real plane unit-distance gadget, not an abstract chromatic graph.
It is not itself five-chromatic, supplies no global lower bound, and does not
improve the 509-vertex record.  Its possible record value depends on a
separate, presently missing physical host that forces one of its forbidden
terminal patterns.

Reviewed package:
[`hadwiger_nelson_opposed_palette_cells`](../hadwiger_nelson_opposed_palette_cells/README.md).
The target Discovery contribution is
`bafkreigunu5bg7kw25ku6qwa7yrmpvcspqtup7tiniizyx2l45ojwkxhvm`,
“A sixteen-point physical palette coupler has 32 essential eight-terminal
obstructions.”  It was accepted for broadcast once but was still absent from
the stale committed ledger during this review.  The review contribution
`bafkreifp74uzfozsk5ns5qzxjiai2jci64raox35vad7fekkmumg3ih6c4` was likewise
accepted for broadcast once and remains pending.  Target-directed relations
are deferred until both endpoints commit; neither contribution should be
resubmitted merely because the ledger is stale.

## Mathematical audit

Let the nine-point cell be

```text
S = (A,B,D,C,E,X+,X-,Y+,Y-),
```

with the coordinates and equilateral-apex formulas displayed in the target.
The reviewer independently evaluated those formulas in
`Q(sqrt(3),sqrt(5),sqrt(7))`, merged exact coordinate equalities in
`S union (-S)`, and scanned all 120 physical pairs.  This recovered 16
distinct points and exactly the claimed 25 unit edges: two 13-edge cells
sharing only the edge `AB`.  No undeclared cross edge occurs.  The eight
designated terminals induce no edge, and their four designated pairs all
have squared distance three.  The reconstructed point and edge hashes match
the target:

```text
points  4e7a496cba7ad1d2eadadb844498af277740a6b79c3b5dcfbc31902ced45aa9e
edges   d73e2b514f1c5656d260a75a9418e29dbca79ab4ebd249bfd3c83f95656b1264
```

A generic domain-propagating graph-colouring search, independent of the
target's three-variable path elimination, then solved all `4^8 = 65,536`
named terminal assignments.  It found 63,328 feasible named assignments.
Quotienting by colour permutations gives exactly 2,691 feasible and 104
infeasible canonical patterns among the 2,795 partitions.  The review
independently reproduces the target's negative-pattern hash
`e4ee1d00f9a50d6bfe17dcfcdb09702deac5e1ec9b8c686a3c866d6b25099641`.
It checks all 2,691 saved positive words against all 25 physical edges and
their terminal pins, for 67,275 witness-edge inequalities.

The complete projection census also agrees.  No subset of at most five
terminals has a forbidden projected pattern; 2 of the 28 six-terminal
subsets, 4 of the 8 seven-terminal subsets, and the full terminal set do.
Exactly 32 canonical forbidden patterns evade every seven-terminal
restriction, with hash
`b04071bd7d031c26ac3573a2df4248a52d206af7f0e205a69aa65d6199f4e122`.
The example `01020102` and all eight of its single-pin relaxations were
independently solved.

The palette corollary was checked more broadly than in the target verifier.
For each of the 36 ordered pairs of two-element palettes, the review tests all
16 orientations of the four terminal pairs, 576 cases in total.  Every case
extends if and only if the palettes are disjoint.  This confirms that the
target's “orientations do not matter” sentence hides no ordering assumption.
The size-two and repetition hypotheses remain essential: this gadget alone
does not force them, and an all-monochromatic terminal word extends.

Finally, a general two-colour search returns UNSAT and a general three-colour
search returns the proper word `0101222111022200`.  Thus the ordinary graph
has chromatic number exactly three.  The terminal nonextension result must not
be promoted to ordinary non-four-colourability.

## Auxiliary H421 attachment gate

The review separately reconstructed the 21-point heptagonal motif in
`Q(exp(pi*i/21))` from the published formulas and formed its physical
difference set.  Without importing the target host checker or the sibling
geometry code, it recovered the 421-point, 1,848-edge strict graph and scanned
all 88,410 pairs.  There are exactly 126 pairs at distance `sqrt(3)`.  For
every such pair, both unit-circle intersection points are already in the
support; all 252 memberships and 504 unit-root equalities pass.  The root
index table has the same hash as the target:

```text
2b4e992265a51af8837568fc5380ff3b956938b83d11a88e511a9e7e010eee90
```

This validates the limited conclusion: embedding all eight comparator
terminals into this particular H421 support cannot add a new comparator
vertex or unit edge.  It does not exclude other hosts or larger circle
constructions.  The committed H421 source
`bafkreieymqno3tggkhnxvrwoprgctvvi4mtk3yjvfs7vt6ykfwyje4ywbm` already
has an independent review that accepts its geometry and also exhibits an
ordinary recolouring outside its potential class.  That recolouring does not
affect the present root-closure argument, which uses geometry only.

## Prepublication refresh

Immediately before publication, repository main advanced with the author-side
package
[`hadwiger_nelson_palette_terminal_circle_gate`](../hadwiger_nelson_palette_terminal_circle_gate/README.md)
at commit `8f33696c8f67fedb73a40b18cd889ba47546070b`.  It adds every common unit
neighbour of every terminal pair, obtaining a 44-point, 85-edge physical
graph, and reports that every colouring of the original 16 vertices extends.
The new points are independent and each sees at most three old colours, so
this is compatible with—and sharpens the construction limitation in—the
present review.  It does not contradict the 16-point relation.

The target-circle package's normal and optimized checks, controls, and source
manifest were replayed successfully.  Its separate exact geometry was not
clean-room rederived in this review, so it remains author-side rather than an
additional accepted review target.  Its negative conclusion retires this
particular full common-neighbour driver, not every possible physical host.

## Reproduction

The substantive review source is commit
`9493a42f27660f4b92c4b86d18424d89d05d0a34`.  From the repository root,
using CPython 3.11 or later and only the standard library, run:

```sh
python3 -B hadwiger_nelson_opposed_palette_cells_review1/independent_check.py --check-expected
python3 -O -B hadwiger_nelson_opposed_palette_cells_review1/independent_check.py --check-expected
python3 -B hadwiger_nelson_opposed_palette_cells_review1/independent_host_check.py --check-expected
python3 -O -B hadwiger_nelson_opposed_palette_cells_review1/independent_host_check.py --check-expected
sha256sum -c hadwiger_nelson_opposed_palette_cells_review1/SHA256SUMS
```

The main check took about 31 seconds per run.  The deliberately independent
cyclotomic host reconstruction took 101–104 seconds per run.  Normal and
optimized outputs agree byte for byte.

`independent_check.py` imports no target code.  The target point fixture is
read only after the displayed coordinate formulas have been evaluated, and
the certificate is read only after the full relation has been generated; they
are used for entrywise comparison and positive-witness checking.
`independent_host_check.py` imports neither target nor sibling code; it
implements the displayed cyclotomic quotient and motif formulas directly.
The trust boundary is the unformalized coordinate transcription, exact Python
`Fraction` arithmetic, exhaustive deterministic search, SHA-256, ordinary
code-review error, and the Python runtime and hardware.  This is not a
proof-assistant formalization.

## Literature status, novelty, and publication readiness

The target makes no priority or smallest-gadget claim.  A candidate-specific
search found no matching published opposed-cell terminal relation, but the
ingredients—odd-cycle restrictions and equilateral diamonds—are standard.
The responsible novelty assessment is therefore only **apparently new in the
reviewed graph/repository**, not a literature-priority claim.

The package is publication-ready as a scoped exact computer-assisted finding:
its geometry, full relation, witnesses, limitations, source, and reproduction
commands are explicit.  It is not publication-ready as a record construction
because it has neither a forcing host nor an ordinary non-four-colourability
certificate.  Live primary-source checks still identify Parts's 509-vertex,
2,442-edge graph as the published unrestricted record:
[Parts](https://arxiv.org/abs/2010.12665).  Haugland's August 2026 paper calls
its own 2,131-vertex spindle-free graph non-record-small:
[Haugland](https://arxiv.org/abs/2608.04542v4).

## Strengthening and improvement opportunities

1. **Highest impact: construct a forcing host.**  To turn this relation into a
   sub-509 result, one must exhibit a strict physical host whose every proper
   four-colouring induces a forbidden pattern on an isometric terminal frame.
   For all eight terminals, a host of order at most 500 leaves room for the
   eight remaining gadget vertices.  The completed graph would still need
   exact collision/edge reconstruction, a checked non-four-colourability
   certificate, and a positive five-colouring.  The full common-unit-neighbour
   pool of the fixed terminals has now been closed as neutral at 44 points and
   85 edges, so a successor must use a genuinely different coupling mechanism.

2. **Exploit the six- and seven-terminal projections.**  The proved projection
   census supplies alternative interfaces that the target's eight-terminal
   budget discussion does not pursue.  Pinning `k` gadget terminals can add at
   most `16-k` vertices, so the corresponding host limits for total order 508
   are 498 for `k=6`, 499 for `k=7`, and 500 for `k=8`.  A six- or
   seven-terminal driver may be easier to force even though it costs one or
   two extra vertices.  The next rigorous step is to list those projected
   forbidden relations and test concrete physical hosts, not merely abstract
   terminal assignments.

3. **Replace the 104-row census by a structural classification.**  The
   single-cell endpoint relation makes this plausible.  A short theorem
   classifying all forbidden patterns by the four terminal colour sets and
   orientations would reduce reliance on enumeration and might reveal the
   easiest host premise.  It must cover singleton pairs and all colour-set
   intersection types; the present complementary-palette corollary covers
   only one important stratum.

4. **Determine minimality only if it aids composition.**  No vertex-, edge-,
   or terminal-minimality claim has been proved.  Deletion/contraction tests
   could identify a cheaper physical gadget or show which of the 25 edges are
   essential to a chosen forbidden relation.  This is secondary to finding a
   realizable driver, because abstract minimization alone does not advance the
   plane record.

These are research directions, except for the stated `492+k` host-budget
arithmetic and the independently verified projection counts.  No stronger
Hadwiger–Nelson bound follows from the current gadget.
