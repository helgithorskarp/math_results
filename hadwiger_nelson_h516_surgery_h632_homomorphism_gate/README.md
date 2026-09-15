# A 508-label H516 surgery has no homomorphism into H632

## Exact result

Let `S` be the lexicographically first labelled member of the published
four-disjoint-star H516 surgery family, selected exactly as described below.
Let `H632` be the complete strict unit-distance graph on the 632 exact points
from the existing Heule completion host. Then

```text
there is no graph homomorphism S -> H632.
```

The source has **508 vertices and 2,520 edges**. Its inherited surgery argument
proves that it is not four-colourable. A homomorphism into `H632` would therefore
have supplied an exact non-four-colourable physical image on at most 508 points,
with collision merging already built into the map. The complete finite gate is
negative: all **7,596** possible oriented images of one source triangle are
excluded by sound arc consistency.

This is a bounded source/host exclusion, not a record improvement. It does not
exclude a map of `S` into another unit-distance host or an arbitrary plane
realization, and it classifies only one of the 53,276 labelled surgeries. No
physical five-chromatic graph is produced. The source-host pair is retired at
this completed boundary; the result is not a reason to sweep neighbouring
surgery choices, relax anchors, or enlarge the host.

## Frozen source and physical target

The source file is the exact 516-vertex, 2,538-edge graph in
[`hadwiger_nelson_h516_degree4_surgeries`](../hadwiger_nelson_h516_degree4_surgeries/README.md).
Its ten degree-four vertices have 87 four-tuples with pairwise disjoint closed
stars, giving 53,276 labelled pair choices. Order centres, compatible tuples,
and allowed nonadjacent neighbour pairs increasingly by original H632 label.
The frozen choice is the first tuple and first pair at each centre:

```text
centres:    102, 109, 293, 299
operations: delete 102 and identify 75=105
            delete 109 and identify 76=106
            delete 293 and identify 144=272
            delete 299 and identify 147=273
```

Each identified vertex keeps the union of the two old incident edge sets;
duplicate edges are removed. Pairwise disjoint closed stars make these four
operations unambiguous and preserve the elementary chromatic pullback argument
from the parent: a four-colouring after deleting a degree-four centre and
identifying two nonadjacent neighbours would extend back over that centre.
Iterating gives `chi(S) >= 5`. The new theorem itself only needs the explicit
finite graph, not this chromatic premise.

The target is the complete graph of all unit pairs among the exact 632 points
reconstructed in
[`hadwiger_nelson_heule632_pair_pilot`](../hadwiger_nelson_heule632_pair_pilot/README.md).
Coordinates lie in the displayed eight-radical basis used there. Both routes
recheck all 199,396 point pairs exactly and obtain 3,112 edges. Thus a map into
the target gives genuine plane coordinates, although this gate finds none.

The source contains 1,030 triangles. The selector fixed before the complete run
chooses a triangle maximizing the sum of final source degrees, with a
lexicographic tie-break. It is

```text
(0,144,147), with degrees (37,23,23).
```

The target has 1,266 unordered triangles. A homomorphism to a simple graph maps
the three mutually adjacent source vertices to three distinct mutually adjacent
target vertices. Hence its restriction to the anchor is one of exactly
`1,266 * 6 = 7,596` oriented target triangles. This proves that the anchor
census covers every homomorphism; it is not a geometric-normalization
assumption.

## Arc-consistency certificate

For an anchored case, start each unpinned source domain at all 632 target
vertices and each anchor domain at its specified singleton. Repeatedly apply

```text
D(v) <- D(v) intersect
        {x : for every source neighbour w of v,
             some target neighbour of x belongs to D(w)}.
```

This deletion is sound. If `f` is a homomorphism surviving the pins and all its
values belong to the old domains, then for every source edge `vw`, the value
`f(w)` is a target neighbour of `f(v)` and remains a support. Induction shows
that no value used by an actual homomorphism is ever deleted. Consequently an
empty domain proves that anchored family empty.

The producer uses an asynchronous directed-arc queue with bit-vector domains.
Every one of the 7,596 cases empties; under its deterministic schedule the first
empty source domain is vertex 257 in every case. The independent checker imports
no producer code. It reconstructs the source quotient through a union-find,
reconstructs H632 with the sibling sparse-radical implementation, enumerates
triangles through neighbour-pair tests, and updates every source domain
simultaneously from the preceding round. All 7,596 cases empty after its second
synchronous round.

Arc consistency is not generally complete when its fixed point is nonempty.
No converse is used here: the conclusion follows because every anchored case
has an empty domain. [`certificate.json`](certificate.json) records the exact
graphs, selector, complete counts, canonical hashes, and producer schedule
statistics. The checker independently recomputes the mathematical counts rather
than trusting the recorded zero-domain verdicts.

## Reproduction

Python 3.11 or later and the standard library suffice. From the repository root,
use fresh output paths outside the checkout:

```sh
python3 -B hadwiger_nelson_h516_surgery_h632_homomorphism_gate/produce.py \
  --output /tmp/h516-surgery-h632-certificate.json
cmp /tmp/h516-surgery-h632-certificate.json \
  hadwiger_nelson_h516_surgery_h632_homomorphism_gate/certificate.json

python3 -B hadwiger_nelson_h516_surgery_h632_homomorphism_gate/verify.py \
  --controls --output /tmp/h516-surgery-h632-verified.json
diff -u hadwiger_nelson_h516_surgery_h632_homomorphism_gate/expected.json \
  /tmp/h516-surgery-h632-verified.json

(cd hadwiger_nelson_h516_surgery_h632_homomorphism_gate && \
  sha256sum -c SHA256SUMS)
```

Expected headline values are 508/2,520 for the source, 632/3,112 for the
target, 1,266 target triangles, 7,596 empty oriented cases, and zero nonempty
fixed points. The optional controls exhaust 4,096 combinations of labelled
three-vertex source graph, target graph, pinned source set, and pin images.
They explicitly enumerate 4,368 valid map instances, verify that every such map
survives propagation, and verify that an empty domain never excludes a valid
map.

## Scope and campaign decision

This theorem distinguishes three levels that must not be conflated:

- `S` is an abstract 508-vertex non-four-colourable graph;
- a homomorphic image in `H632` would be a genuine physical plane support;
- the complete negative gate proves that no such image in this fixed host
  exists.

It says nothing about other physical hosts, arbitrary exact coordinates,
non-homomorphic edge repairs, or the other labelled surgeries. It also does not
upgrade the earlier injective K2,3 obstruction to a global nonrealizability
theorem. There is no proper five-colouring or non-four certificate for a new
physical graph because there is no physical graph at this gate.

The result uses exact graph data, integer/rational radical arithmetic, SHA-256,
finite enumeration, and the elementary arc-consistency induction. The
independent implementation is author-side algorithmic validation, not an
independent-author review or proof-assistant formalization. No SAT solver,
floating-point geometry, omitted proof trace, or solver `UNKNOWN` occurs.

Discovery Net was refreshed before the run at committed index 4,363 while the
authorized RPC remained at block 4,364, both stale since 2026-09-11. The result
therefore relies on the current authorized Git repository and durable teammate
briefs for post-index evidence. It is a scoped negative checkpoint, not record
progress.
