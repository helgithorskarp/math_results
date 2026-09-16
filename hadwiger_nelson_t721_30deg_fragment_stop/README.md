# A 30-degree interaction of two proper T721 fragments is four-chromatic

This directory gives an exact, complete decision of one bounded physical
Hadwiger--Nelson construction.  Two 254-point proper fragments of Heule's
native `T721.vtx` support are placed in frames rotated by 15 and 45 degrees
about the native origin.  Collision merging and a complete all-pairs unit
test give a strict plane graph with **391 vertices and 1,264 edges**.  It is
**exactly four-chromatic**, so this frozen architecture is not a sub-509
five-chromatic candidate.

The interaction itself is substantial: the two formal 254-point fragments
have 117 exact collisions and 134 private--private cross edges.  The complete
graph is connected, has no articulation or bridge, and its 253-vertex
four-core contains 94 private vertices from each frame and 65 shared vertices.
Thus the failure is not explained by separation or by one fragment dropping
out of the four-core.

## Frozen fragment and placement

The source input is the SHA-256-pinned 721-point coordinate file already used
by the independently accepted native-host theorem in
[`hadwiger_nelson_t721_weighted_cover`](../hadwiger_nelson_t721_weighted_cover/README.md).
The fragment is defined without a chromatic search:

1. take the 238 source labels occurring in that package's positive terminal
   deletion cover (the two terminals and 236 deleted labels);
2. add the first 16 outside labels under the exact order
   `(-number of neighbours in the 238-set, -native degree, label)`.

The resulting extra labels are stored in [`fragment.json`](fragment.json), and
the verifier recomputes their ranking from the complete native half graph.
Write `R_theta` for rotation about the origin.  The final physical support is

```
R_15(fragment) union R_45(fragment).
```

Both fragments are proper subsets of the 721-point source and both are moved.
The construction is not a subgraph of the closed native 1,441-point spindle.
It is also outside the pointwise-Galois scope: every automorphism of the native
field fixes the rational point `(-1,0)`, whereas both displayed rotations move
it.  No map-existence surrogate is used.

A finite contact-only preflight selected the 30-degree relative offset before
the chromatic query.  No alternate placement received a chromatic test.  The
preflight is discovery history, not part of the theorem; the verifier checks
the frozen support directly from its definition.

## Exact physical and chromatic certificates

Coordinates are represented over
`Q(sqrt(2),sqrt(3),sqrt(5))` in the ordered basis

```
(1, sqrt(2), sqrt(3), sqrt(6), sqrt(5), sqrt(10), sqrt(15), sqrt(30)).
```

After the two rotations every coefficient has common denominator 12.  The
verifier merges identical 16-tuples, tests all 76,245 unordered physical
pairs, and reconstructs every unit edge by exact radical arithmetic.  It then
checks the literal proper four-colour word in [`four_word.txt`](four_word.txt).

For the lower bound, [`fragment.json`](fragment.json) records a 26-vertex,
50-edge induced subgraph.  It uses eight private vertices from the first
frame, thirteen from the second, five shared vertices, and seven private cross
edges.  A short definition-level backtracker exhausts all three-colourings
after fixing one triangle's palette.  It finds none; deleting any one of the
26 vertices does admit a three-colouring.  This proves the complete physical
graph has chromatic number exactly four without trusting the SAT solver used
to discover the small witness.

## Reproduction

From the repository root, with CPython 3.11 or newer:

```sh
python3 -B hadwiger_nelson_t721_weighted_cover/fetch_input.py /tmp/T721.vtx
python3 -B hadwiger_nelson_t721_30deg_fragment_stop/verify.py \
  --input /tmp/T721.vtx --check-expected
python3 -O -B hadwiger_nelson_t721_30deg_fragment_stop/verify.py \
  --input /tmp/T721.vtx --check-expected
```

Only the Python standard library is required for verification.  Expected
coordinate, edge and four-word hashes are in [`expected.json`](expected.json).
The external input must have 40,529 bytes and SHA-256
`a63fa371d7cf42faa8a3b26d56df81b0c25c1f149d6791dd25c7c356abe1b7c6`.

## Scope

This is one exact four-colour stopping result.  It does not classify other
T721 fragments, other relative rotations, or arbitrary moved-fragment unions,
and it does not improve the 509-vertex record.  The native-subgraph theorem
and the pointwise-Galois orbit bound remain separate negative results.  No
nearby frame, enrichment, fragment size, or placement is licensed by this
computation.

The trust boundary is the pinned upstream coordinate file, the accepted
source package's compact radical parser/arithmetic, the readable new
rotation/collision/all-pairs code, the explicit positive four-word, the small
exhaustive three-colour checker, SHA-256 collision resistance, and ordinary
CPython execution integrity.  This is exact author-side computer-assisted
evidence, not a formal proof or an independent review.
