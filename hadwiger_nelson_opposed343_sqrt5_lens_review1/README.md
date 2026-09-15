# Independent review of the opposed-S343 sqrt(5) lens stop

## Verdict

**Accept, with exact frozen-finishing-class and imported-source-relation
limitations.** The package at mathematical commit
`8a98d34290f4ba578a28ae69aa1edb8fe7399d85` constructs an actual 451-point,
2,170-edge strict plane unit-distance graph. It adjoins both unit-circle
intersections for every one of the 54 S343 pairs at squared distance `16/9`.
All 108 new points are distinct and outside the old coordinate field, and all
66 reviewed source inputs extend. The projected Golomb relation is therefore
unchanged and the final graph is exactly four-chromatic.

This closes only the declared full two-lens layer on this fixed S343 source.
It is not a five-chromatic graph, a record candidate, or evidence against
other distances, one-sided selections, multiple completion rounds, or other
sources.

## Independent reconstruction

[`verify.py`](verify.py) imports no target code. It represents the coordinate
field as the quadratic tower

```text
Q(sqrt(3),sqrt(11)) + sqrt(5) Q(sqrt(3),sqrt(11)),
```

rather than the target's flat radicand lookup or its control's bit-mask
arithmetic. It independently rebuilds S343 from the B214 fixture, finds the
54 center pairs, applies the geometric lens formula, and decides all 101,475
physical pairs exactly. The complete point, edge, center-pair, and 66-witness
streams agree with the target.

The upper bound of 66 projected inputs imports the previously accepted
[independent S343 review](../hadwiger_nelson_golomb_opposed_b214_review1).
This review directly checks that its reconstructed first 343 vertices have
the same complete edge set, and checks all 66 parent and all 66 final positive
words. It does not claim a second independent replay of the parent's
29-pattern RUP exclusion.

## Structural sharpenings

The independent audit adds three exact facts:

1. The 54 center pairs form a matching on 108 distinct old vertices.
2. The new-vertex graph has twelve connected components and exactly two
   isomorphism types: eight bipartite components of order 6 with 7 edges, and
   four four-chromatic components of order 15 with 29 edges. Each large
   component contains exactly one induced seven-vertex, eleven-edge Moser
   spindle, giving four vertex-disjoint spindles entirely inside the new
   layer. The twelve components occur in six pairs with identical old
   attachment sets.
3. The full 451-point graph has vertex connectivity exactly four. Exhaustive
   low-link tests cover all 101,475 removed pairs and, through articulation
   tests in the pair-deleted graphs, all 15,187,425 possible triples. None
   separates. Removing the neighbours `[15,139,386,413]` of vertex 349
   isolates it and supplies a four-cut.

Thus the new layer is internally substantial—it already contains four
four-chromatic unit-distance subgraphs—but its coupling to S343 still leaves
every complete source input available. The full graph is robust even though
the induced new layer factors into small pieces.

## Reproduce

From the repository root with CPython 3.11 or later and no third-party
dependency:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_opposed343_sqrt5_lens_review1/verify.py \
  --check-expected

PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_opposed343_sqrt5_lens_review1/controls.py

cd hadwiger_nelson_opposed343_sqrt5_lens_review1
sha256sum -c SHA256SUMS
```

The full review takes roughly two to three minutes on the review host, almost
entirely because of the exhaustive separator census. The controls rescan all
101,475 pairs using square-class masks, compare all 64 basis products, compare
the graph-coloring routine with brute force on 2,048 small cases, exercise
isomorphism and cut detection, and reject two semantic corruptions.

See [PROOF.md](PROOF.md) for completeness and [PROVENANCE.md](PROVENANCE.md)
for the imported theorem and trust boundary. The reviewed target is available
at [its stable repository directory](../hadwiger_nelson_opposed343_sqrt5_lens_stop).
