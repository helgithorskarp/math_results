# Exact minimum inside the union of all six exceptional Parts placements

## Result

Write Jaan Parts's 509-point construction as `L union S`, with `|L|=374`
and `|S|=135`. The sibling exact rotation classification finds six
exceptional rotations at which `L union R(S)` remains non-4-colourable. This
directory studies the strict unit-distance graph `W` on the union of all six
placements.

For a transparent canonical labelling, the verifier inserts the rotations in
the grouped order

```text
108, 109, 789, 215, 216, 690.
```

The set of points is independent of insertion order. Exact reconstruction in
`Q(sqrt(3),sqrt(5),sqrt(11))` gives 692 distinct points and 3,354 unit pairs.
The certified theorem is:

> Every non-4-colourable induced subgraph of `W` has at least 509 vertices,
> and this is sharp because `W` contains each 509-point placement.

Thus no induced recombination inside the full finite union of the six
exceptional `K`-rational placements improves the 509-vertex record. This does
not exclude other rotations, translations, reflections, new coordinates,
non-induced edge selections, or delete-and-repair mechanisms.

## Two-copy structure

The six rotations split into compact triples

```text
A = {108, 109, 789}
B = {215, 216, 690}.
```

The sibling triple certificate reconstructs both triples and proves that,
under canonical insertion labels, their 533-vertex strict edge arrays and
their corresponding placement-label arrays are identical. Each consists of
the common 374-vertex graph on `L` plus one 159-position extension. In the
full union the two extensions are coordinate-disjoint and there is no unit
edge between them. The exact edge partition is

```text
inside L                    1860
first extension contribution 747
second extension contribution 747
cross-extension edges          0
total                        3354
```

Consequently a proper colouring of one triple with a subset of its extension
deleted lifts to a proper colouring of `W`: retain its colours on `L` and use
the same extension colour on both corresponding copies.

## Lower-bound certificate

The verified triple certificate partitions its 159 extension positions into
96 forced positions and 63 free positions.

1. For each `v in L`, its explicit triple colouring after deleting `v` lifts
   to a colouring of `W-v`. Hence every non-4-colourable induced subgraph of
   `W` contains all 374 vertices of `L`.
2. For each of the 96 forced extension positions `p`, the triple colouring
   after deleting `p` lifts to a colouring after deleting both twins of `p`.
   The selected vertices outside `L` must therefore hit 96 disjoint twin
   pairs, requiring at least 96 vertices.
3. The triple certificate has 330 colourable deletion sets on its 63 free
   positions. Deleting both copies of every position in any one of these sets
   gives a colourable deletion of `W`. A hitting set for the doubled sets
   projects to a hitting set for the original 63-position hypergraph. Its
   solver-free checked transversal number is 39, so at least 39 further
   vertices are required.

The two classes of extension positions are disjoint. Every non-4-colourable
induced subgraph therefore has at least

```text
374 + 96 + 39 = 509
```

vertices. The event-789 placement attains equality. Its 135 vertices outside
`L` select one endpoint of every forced-position twin pair and project to the
checked size-39 transversal on the free positions.

This proof uses no negative SAT or optimization answer. The source triple
lower bound consists of directly checked 4-colourings and a 73,946-node
standard-library transversal enumeration. The present verifier additionally
lifts and directly checks all 800 source colourings against the independently
reconstructed 692-vertex edge list.

## Verification

Run with Python 3.11 or later:

```bash
python3 verify.py
```

No third-party package is needed. `verify.py` first runs the pinned sibling
triple verifier, then reconstructs the full geometry, checks all unit pairs,
checks the two-copy decomposition and all six constituent placements, and
validates 2,659,622 lifted colouring-edge incidences. The exact output is in
`expected_check.txt`.

Headline values:

```text
vertices=692
edges=3354
edge_sha256=ee9d50eed3d3ba28d5a687876311fdb23b02a88458eed0c769a04916d1018465
common_forced_vertices=374
paired_forced_extension_positions=96
projected_free_positions=63
projected_transversal_number=39
transversal_number_outside_L=135
minimum_non_four_colorable_order=509
```

The compact metadata certificate SHA-256 is
`e11993c16d16551fd2be06d7a52a17b9f02d2116912db59770f4cdcc0a34b99f`.

## Trust boundary

- The source triple certificate and verifier are pinned by SHA-256. The
  latter reconstructs the two triple geometries exactly, validates all source
  colourings, proves the 39 transversal bound without a solver, and pins the
  Parts coordinates, criticality certificate, and rotation certificate.
- This verifier reconstructs the combined 692-point set at denominator 6144
  and tests every point pair using exact integer arithmetic in the
  eight-dimensional radical basis. No floating-point geometry is used.
- Sharpness uses the embedded identity-labelled Parts graph. Its
  non-4-colourability ultimately depends on the DRAT-audited sibling Parts
  criticality artifact.
- The proof is a finite exact computation in CPython, not a proof-assistant
  formalization.

## Provenance

The construction comes from Jaan Parts,
*Graph minimization, focusing on the example of 5-chromatic unit-distance
graphs in the plane*, Geombinatorics 29(4) (2020), 137--166,
<https://arxiv.org/abs/2010.12665>. The exceptional rotations are those of
the sibling `hadwiger_nelson_parts509_rotation_scan` artifact. The two-copy
decomposition and the exact minimum theorem are scoped computational results;
no unconditional historical-priority claim is made.

## Files

- `verify.py` performs the full solver-free verification.
- `certificate.json` records the canonical order, exact graph digest, source
  hashes, and lower-bound arithmetic.
- `expected_check.txt` records the exact verifier output.
