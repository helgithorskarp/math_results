# Independent review: Parts509 source-pole inversions

## Verdict

**ACCEPT with high confidence, within the stated restricted family.**  At
immutable target commit
`9f2a8a6c603d6166124abcb1d062a3e0cbf41c6c`, every drawing obtained by
inverting the first 509 Parts points about one of those points, omitting the
pole, and applying an arbitrary positive scale has 508 distinct physical
points and a four-colourable strict unit-distance graph.  Every such graph has
at most 486 unit edges, and pole 0 at scale 2/3 attains 486.

This is a complete exclusion for a nonlinear but restricted construction
family.  It is not a global lower bound, a sub-509 five-chromatic construction,
or a classification of inversions about free poles.

Target package:
[`hadwiger_nelson_parts_pole_inversions`](../hadwiger_nelson_parts_pole_inversions/README.md).

## Why the reduction works

For source points `p_i`, inversion about `p_a` gives

```text
I_a(p_i) = (p_i-p_a)/|p_i-p_a|^2,
|I_a(p_i)-I_a(p_j)|^2 = |p_i-p_j|^2 /
                         (|p_i-p_a|^2 |p_j-p_a|^2).
```

At scale `s`, an edge therefore has one of the 128,778 ratio values for that
pole; scales producing no edge give empty graphs.  Equality of algebraic ratio
values implies equality after every valid finite-field projection.  Thus the
physical graph at an event scale is a subgraph of one residue bucket.  A
positive four-colouring of the bucket restricts to the physical graph, and its
edge count is an upper bound.  This direction is safe even when unequal exact
values collide modulo the prime.  No modular non-colourability inference is
made.

Inversion is injective away from its pole, so the 508 retained source points
remain distinct in the Euclidean plane.  The target's Möbius corollary also
checks: a nonconstant complex Möbius map with a source-point pole is, after a
translation, a nonzero complex multiple of `1/(z-a)`; this differs from the
displayed circle inversion only by reflection, rotation, and positive scale.

## Independent computation

`review.py` imports no target code.  It performs these checks:

1. Reads the original eight-radical Cartesian coordinate rows directly and
   verifies their pinned SHA-256.
2. Proves the modulus prime by trial division and constructs radical images
   independently.
3. For every pole, explicitly builds all 508 inverted finite-field points and
   recomputes all 128,778 pair distances.  Across all poles this checks
   65,548,002 labelled event representatives.
4. Groups the distances independently, uses a heap-based 3-degeneracy peel,
   and obtains fresh positive words for every nonempty 4-core with a
   deterministic DSATUR search.  Search failure is never used as an UNSAT
   certificate.
5. Repeats the complete scan for all four conjugate projections of the
   squared-distance field.  The differing bucket totals are evidence that the
   runs are not merely replaying one copied partition.
6. In characteristic zero, checks all 128,778 pairs at pole 0 and scale 2/3
   by the independent event equation
   `4*d(i,j) = 9*d(0,i)*d(0,j)`.  This avoids field inversion and recovers the
   target's exact 486-edge list hash.

| signs of `(sqrt(5),sqrt(11))` | buckets | buckets with >=10 edges | nonempty 4-cores | maximum edges |
|---|---:|---:|---:|---:|
| `(+,+)` | 56,554,414 | 118,103 | 17 | 486 |
| `(+,-)` | 56,554,412 | 118,103 | 17 | 486 |
| `(-,+)` | 56,554,404 | 118,103 | 17 | 486 |
| `(-,-)` | 56,554,428 | 118,103 | 17 | 486 |

The `(+,+)` stream SHA-256 is
`956fdb8478b527ac69c858e05a1a6430592684c9b6698c14fec9ab85645443a7`,
entry-for-entry equal to the target.  Its complete 509-row pole inventory hash
is `21b8f1b84ce9edf99c3f084979d2b9bbd204e5a0080aaba5bb623e5a2df5e2cf`.
The clean-room checker also validates all 17 published certificate words, but
its theorem check does not depend on them: it finds independent words first.

The exact pole-0 fixture has 508 points and 486 edges.  Its canonical edge-list
SHA-256 is
`ce567d8e826bf849985d121ae847350e028b6f95ab055dc5bdf0690e7dd708f9`,
again equal to the target.

The unmodified author replay with UBSan also passed in 48.268 seconds.  It
compared all 65,548,002 modular entries between the target's two implementations
and separately checked the exact fixture.

## Reproduce

From the repository root, using Python 3.11+:

```sh
python3 -m venv /tmp/parts-pole-review-venv
/tmp/parts-pole-review-venv/bin/pip install -r hadwiger_nelson_parts_pole_inversions_review1/requirements.txt
/tmp/parts-pole-review-venv/bin/python -B hadwiger_nelson_parts_pole_inversions_review1/review.py --check-expected
```

The full four-projection review takes about four minutes on the review host.
It emits no large certificate or comparison stream.  `expected.json` pins all
stable outputs, including per-pole, histogram, residual-key, and independently
generated word hashes.

## Scope and limitations

- The result covers exactly the first 509 source rows, poles at one of those
  points, omission of that pole, and every positive scale.  It does not cover
  free or midpoint poles, additional deletions, or arbitrary deformations.
- The residue buckets are abstract finite-field supergraphs and need not be
  realizable as plane unit-distance graphs.  The 508-point supports at exact
  event scales are genuine Euclidean drawings; only a downward colouring and
  edge-bound transfer is used.
- The result proves chromatic number at most four, not exactly four, for every
  drawing.  No five-chromatic graph is produced.
- The proof trusts the hash-pinned coordinate file, Python/NumPy execution, and
  this independently authored finite enumeration.  It is not proof-assistant
  formalization.
- As refreshed on 2026-09-14, [Parts's published 509-vertex, 2,442-edge
  graph](https://arxiv.org/abs/2010.12665) remains the unrestricted order
  record.  [Haugland's 2,131-vertex construction](https://arxiv.org/abs/2608.04542)
  is stronger only under the separate Moser-spindle-free restriction.

Discovery Net's committed index was still stale at height 4363 (node height
4364, last block 2026-09-11).  The target broadcast was therefore treated as
pending rather than committed.  The bounded committed HN review found no
relevant objection, but it predates this target.
