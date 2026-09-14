# Independent review: point606 partial translations are global

Verdict: **ACCEPT at high confidence, with exact restricted scope.** For the
frozen 530-point, 2,648-unit-edge point606 core, let `t` be any real plane
vector, choose `epsilon_v` independently from `{0,1}`, and put

```text
f(v) = p_v + epsilon_v t.
```

If `f` preserves the length of every source unit edge, then the choices are
global when `t` is nonzero. When `t=0`, the image is the original point set
regardless of the Boolean labels. Consequently every image in this declared
class has exactly 530 distinct points, so none has at most 508 points.

The reviewed source is
[`hadwiger_nelson_point606_partial_translation`](../hadwiger_nelson_point606_partial_translation/README.md)
at verified source commit `8b4a5d149d4d908530d9a3b0f8613446f627e36c`.
I found no mathematical gap, missed physical edge, direction-partition error,
connectivity failure, or hidden chromatic premise in the stated theorem.

## Proof audit

For an oriented source unit edge with displacement `d=p_b-p_a`, unequal
endpoint choices change its displacement to `d+t` or `d-t`. Since `|d|=1`,
preservation of unit length gives respectively

```text
2 d dot t = -|t|^2   or   2 d dot t = |t|^2.
```

For fixed nonzero `t`, each equation cuts the unit circle by a line
perpendicular to `t`. Across both signs there are at most four oriented unit
vectors, paired antipodally, hence at most two unoriented displacement
directions whose edges may have unequal endpoint choices. Tangencies and empty
intersections only reduce this number.

The exact finite check proves that deleting any two of the core's 36
unoriented unit-direction classes leaves the graph connected. If there are
zero or one exceptional classes, pad them to two distinct classes; the graph
after deleting only the exceptional classes contains a checked connected
spanning subgraph. Every remaining edge forces equal Boolean choices, and
connectivity propagates equality to all 530 vertices. Thus the map is the
identity or one global translation. Translation preserves distinctness, and
the source points are checked distinct. The `t=0` case is separately the
identity image.

This is a complete argument for the stated continuum of vectors and all
`2^530` Boolean assignments; it does not rely on sampling either space.

## Independent exact reconstruction

[`independent_check.py`](independent_check.py) imports no module from the
reviewed package. It hash-pins all nine source-package files, the point606
deletion certificate, and both original coordinate sources. It parses the
coordinates in the ordered basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165)
```

at common denominator 288. Instead of the target's bit-mask multiplication or
its audit's generic square-free-radical products, the checker multiplies first
in `Q(sqrt(3),sqrt(5))` and then treats every element as `a+b sqrt(11)`.
All 64 basis products are independently controlled.

Every one of the 140,185 unordered point pairs is decided by exact integer
arithmetic. The reconstruction gives 530 distinct physical points, 2,648
complete unit edges, and the target edge-stream SHA-256
`7116ca71d9b53598b931614a5c7f5406909f124555f0ecf231a4fc234b665faa`.
Direct coefficient comparison groups those edges into 36 unoriented
directions.

Connectivity is reimplemented using Python integer adjacency bitsets, rather
than the target's breadth-first parent array or its same-author audit's
disjoint-set unions. The checker directly tests deletion of zero directions,
each one direction, and all 630 unordered direction pairs: 667 connected
graphs in total. Every reachable set has all 530 vertices. Pair-deleted graphs
have 2,330 through 2,646 retained edges. The independently ordered direction
partition hashes to
`1e5abe71c36df14445609bb60780e4e5f3a784509614c13994a4f10c991a0fc9`;
the complete connectivity trace hashes to
`9fa211fd11c8dfdaf7e61adc935c7686285700587afee2aff81536542cd11c72`.

As a necessary-scope control, the checker tests all 16 Boolean assignments on
a four-point unit diamond. Four assignments preserve its five source edges,
and two contract it to three points by translating one apex onto the other.
Thus partial translations can genuinely contract unit-distance graphs when
the direction-connectivity hypothesis fails. A disconnected-graph test and a
zero-displacement rejection test exercise the bitset and direction layers.

The source package's normal verifier, optimized verifier, separate exact
audit, controls, and SHA-256 manifest also replayed successfully. Exact outputs
and timings are recorded in [`REPRODUCTION_RESULT.json`](REPRODUCTION_RESULT.json).

## Scope and limitations

This is a **restricted-family exclusion**, not a smaller five-chromatic graph,
not a new lower bound on the order of arbitrary five-chromatic plane
unit-distance graphs, and not a global Hadwiger--Nelson advance. It rules out
only maps of this fixed 530-point source that:

1. assign each vertex either displacement `0` or the same displacement `t`;
2. keep every source unit edge at unit length; and
3. do not delete source vertices first.

It does not cover a transformation that loses source edges and gains
replacement edges, three or more displacement values, rotations, reflections,
general deformations, a different parent, or a pre-deleted source. The earlier
508-point half-plane fold is outside the theorem precisely because it loses
497 source edges.

The geometric theorem itself uses no chromatic certificate. Chromaticity is
only the construction motivation: an edge-preserving image of a non-four-
colourable source would remain non-four-colourable because any image
four-colouring pulls back. The source core's separate high-confidence review
established a strict physical 530-point graph with chromatic number five, but
that result is not re-proved here and is not a premise of this exclusion.

The unrestricted published size record remains Parts's 509-vertex,
2,442-edge construction ([arXiv:2010.12665](https://arxiv.org/abs/2010.12665)).
Haugland's 2026 paper also identifies 509 as the current unrestricted record;
its 2,131-point construction concerns the additional Moser-spindle-free
restriction ([arXiv:2608.04542v4](https://arxiv.org/html/2608.04542v4)).

The trust boundary is the hash-pinned exact coordinate data and deletion
labels, the elementary geometric proof above, CPython's integer and rational
arithmetic, SHA-256, ordinary hardware, and inspection of two independently
structured exact implementations. No proof-assistant formalization is
claimed. The reviewed target's Discovery contribution is only pending in the
stale local network view, so this review cannot honestly claim a committed
`verifies` relation to it.

## Reproduce

From the repository root with CPython 3.11 or later and only the standard
library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_point606_partial_translation_review1/independent_check.py \
  | diff -u \
      hadwiger_nelson_point606_partial_translation_review1/EXPECTED_OUTPUT.txt -

PYTHONDONTWRITEBYTECODE=1 python3 -O \
  hadwiger_nelson_point606_partial_translation_review1/independent_check.py \
  | diff -u \
      hadwiger_nelson_point606_partial_translation_review1/EXPECTED_OUTPUT.txt -

(cd hadwiger_nelson_point606_partial_translation_review1 && \
  sha256sum -c SHA256SUMS)
```
