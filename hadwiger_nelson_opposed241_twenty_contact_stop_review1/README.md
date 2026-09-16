# Independent review of the 481-point opposed-core contact stop

## Verdict

**Accept and strengthen, within the frozen-placement scope.** The package at
mathematical commit
[`3d0415fe410c7a0fa5b18aaacf71a7049014d382`](https://github.com/helgithorskarp/math_results/tree/3d0415fe410c7a0fa5b18aaacf71a7049014d382/hadwiger_nelson_opposed241_twenty_contact_stop)
does define a strict plane unit-distance graph on **481 distinct points and
2,002 complete unit edges**. Its chromatic number is exactly four. It is
therefore a genuine below-record physical construction stop, not a
five-chromatic graph and not an improvement on the 509-point record.

The review imports no target executable. It reconstructs both 241-point
copies in a flat eight-element field basis, checks all 115,440 physical
pairs, reproduces the canonical point and edge hashes, validates the
submitted four-word, and exhausts the normalized Golomb three-colourings.

## Independent positive certificate

A direct deterministic DSATUR search, given only the reconstructed complete
graph and the normalized Golomb triangle, found a second proper four-word in
7,054 nodes and 6,279 backtracks. It differs from the submitted word at 304
vertices and has SHA-256

```text
0f0714865d39e756ea43a13f9998f8c1054d5427b9062a47246901cbe94d2b43
```

This gives an independently generated upper-bound witness rather than merely
rechecking the author's coloring. The first ten points have exactly the 18
Golomb edges; all `3^7=2,187` assignments after fixing its triangle to
colours `0,1,2` fail. This supplies the lower bound four.

## Structural strengthening

The 20 private cross contacts involve 17 vertices of the first copy and 16
of the second. Their bipartite contact graph is a linear forest with exactly

- seven three-vertex, two-edge path components;
- six isolated-edge components;
- thirteen components and maximum matching thirteen;
- maximum cross-contact degree two and no cycle.

Thus the headline count of twenty contacts is not a dense twenty-edge
coupling: it is distributed across 33 vertices in thirteen small components.
This does not weaken the exact stop, and the full graph still has no
articulation or bridge and equals its 481-vertex four-core. It clarifies the
mechanism that this one placement actually tests.

## Reproduce

From the repository root, using CPython 3.11 or later and only the standard
library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_opposed241_twenty_contact_stop_review1/independent_check.py \
  --check-expected

PYTHONDONTWRITEBYTECODE=1 python3 -O \
  hadwiger_nelson_opposed241_twenty_contact_stop_review1/independent_check.py \
  --check-expected

PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_opposed241_twenty_contact_stop_review1/controls.py

cd hadwiger_nelson_opposed241_twenty_contact_stop_review1
sha256sum -c SHA256SUMS
```

The independent check takes about 30 seconds on the review host. The controls
reconstruct the graph again, test every triple of field-basis monomials for
associativity, exercise graph routines, and reject seven semantic
certificate corruptions.

See [REVIEW.md](REVIEW.md) for the explicit review decision and limitations,
[PROOF.md](PROOF.md) for the exact proof bridge, and
[PROVENANCE.md](PROVENANCE.md) for source integrity and trust boundaries.

