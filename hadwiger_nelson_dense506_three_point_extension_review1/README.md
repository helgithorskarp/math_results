# Independent review: dense506 arbitrary three-point extension

This directory records an independent review of two Discovery Net results:

- `bafkreigshrkjtbjqdujpwqwa65fm7h5odbbrmqpdoi2lhnsubp766ytgq4`, the
  nonfield-triangle exclusion at source commit
  `cc74fab9de1e6f687ce9d1569409a419524c71b7`; and
- `bafkreigmgvuzom7niai24lymu7zaffu64wxtjatfnc5xmzjemyerkd6zhy`, the
  resulting arbitrary-three-point extension theorem at source commit
  `e4f16fcce2c2f11cb8e2ef9eeb4e9255799277b9`.

## Verdict and scope

**Accept both results at their stated intermediate scope.** For either of
the two pinned 506-vertex unit-distance hosts and its published fixed proper
four-colouring, that colouring extends over every set of at most three
arbitrary Euclidean-plane points. Consequently every subgraph of such a
union is four-colourable, including all repairs of these hosts using at most
three added vertices.

This is not a sub-509 five-chromatic unit-distance graph. It excludes a
repair family for two fixed host embeddings and one fixed colouring; it does
not cover a fourth added point, another host or relative gadget placement,
or establish that a failure of this particular colouring would make a graph
five-chromatic.

## Independently checked mathematics

The nonfield result imports the preceding midpoint reduction. Conditional
on that reduction, a remaining obstruction supplies three noncollinear
equilateral midpoints and three concurrent host-pair chord lines. If `L` is
the squared midpoint-triangle side and `o` the concurrence point, direct
rotation geometry gives the necessary equations

```text
4(1-L) N(m_i-o) = L(4-N(d_i)).
```

After clearing the line-intersection denominator, these are polynomial
identities in the exact host field. A true solution therefore survives any
valid finite-field image. Both implementations retain the singular case in
which all three determinants vanish modulo the screening prime, so the
modular filter has no false-negative branch. Every exact survivor has all
three chord directions parallel. Parallel lines through three noncollinear
midpoints cannot be concurrent, which excludes the obstruction.

For a differently coloured host pair with squared separation `s`, the two
common unit points are obtained from its midpoint using the perpendicular
offset whose squared field coefficient is

```text
q = (4-s)/(3s).
```

I checked the quartic-field square-root cases and the finite-field
nonsquare argument. If a field element is a square, then at any prime away
from `2*3*11` its integral reduction is a square: a negative valuation of a
prospective root would leave a nonzero nilpotent leading residue, impossible
in the product of fields furnished by the checked simple roots. Thus each
nonresidue image is a valid exclusion even when a putative root was not
initially presented integrally.

Finally, each remaining new point has a two-colour available list. A graph
on at most three new vertices with lists of size at least two is not
list-colourable only when it is a triangle and all three lists are the same
two-element set. Grouping by the complementary host-colour mask and finding
no unit triangle is therefore exactly the needed last check.

## Fresh complete computations

I ran the complete public pipeline for the nonfield predecessor using
CPython 3.11.2 and GCC 12.2, not a prefix:

- all 327,805,042 midpoint pairs were scanned, producing 4,050,552
  midpoint triangles and 140,742,349 host-pair assignments;
- the primary image left 34,938 rows, and all 104,814 exact pairwise
  determinant checks were parallel;
- the separate packed-Python encoding matched every triangle row in order
  and matched EOF;
- a second host reconstruction, prime and Cramer-rule screen produced a
  byte-identical survivor stream;
- exact quotient-ring checking validated every survivor and midpoint
  identity; and
- the radical positive fixture, broken-radius negative fixture, singular
  fallback, duplicate/malformed inputs and truncated streams all behaved as
  specified.

The regenerated triangle stream is 78,343,591 bytes with SHA-256
`bac810715525907a23cdff32f98e9237ae16f37aa29c4f1523e3395bb6b02d54`.
Each independently generated 1,456,306-byte survivor stream has SHA-256
`88580a61a55170031b3207f53a8b3a058713fb2cb414339bb5bd9ffff18fa920`.

I then regenerated and audited the field census. All public expected files
and the transitive manifest matched. The independent generic eight-basis
audit reconstructs the opposite host directly from the pinned Parts tables
and imports neither the producer nor its square-root implementation. The
fresh results were:

- 96,003 differently coloured host pairs and 22,887 distinct squared
  distances;
- 184 exact square cases and 22,703 independently checked nonsquare
  witnesses using 17 finite-field maps;
- 4,523 distinct field common-neighbour points: 506 host points, 1,402
  points with at least three host neighbours, and 2,615 new points with
  exactly two;
- all 2,288,638 host/point pairs scanned, with 15,664 exact incidences;
- 572,182 same-mask candidate pairs, 643 unit edges, 1,286 rotated-third
  lookups, and zero unit triangles in all six masks; and
- 1,250 known-square controls, five rational nonsquares, the zero and
  pure-`r` square-root branches, four circle boundary cases, a positive
  triangle, and five certificate corruptions all passed.

[`result.json`](result.json) is the compact machine-readable record of the
fresh outputs and hashes. The multi-megabyte generated field tables and the
78 MB predecessor stream remain in external scratch storage and are
deterministically regenerated rather than committed.

## Reproduction

From the repository root, choose two fresh work paths under a filesystem
with enough space. Assertions are proof checks, so do not use Python's
optimization flag.

```bash
FIELD_WORK=/scratch/fresh-hn-field-review
python3 -B hadwiger_nelson_dense506_three_point_extension/generate.py \
  --work "$FIELD_WORK"
python3 -B hadwiger_nelson_dense506_three_point_extension/audit.py \
  --work "$FIELD_WORK"
python3 -B hadwiger_nelson_dense506_three_point_extension/controls.py \
  --work "$FIELD_WORK"
python3 -B hadwiger_nelson_dense506_three_point_extension/verify.py \
  --work "$FIELD_WORK"
```

For the predecessor, follow the full command block in
[`../hadwiger_nelson_dense506_nonfield_triangle_closure/README.md`](../hadwiger_nelson_dense506_nonfield_triangle_closure/README.md).
It builds three strict-warning C++ binaries, regenerates both complete
streams, runs the packed audit and the distinct second screen, compares all
expected reports, runs the controls, and checks the transitive manifest.

## Imported trust and residual uncertainty

The field result depends logically on the nonfield result, which in turn
imports the earlier geometric midpoint reduction. This review re-derived
the new geometric and list-colouring bridges and completely replayed both
new finite computations, but does not replace that imported reduction with
a proof-assistant formalization. The already accepted two-point host review
supplies reviewer-owned generic quotient-ring arithmetic and the alternate
host reconstruction used by both new audits.

Other trust boundaries are the pinned coordinate and colour data, SHA-256
for identity, Python arbitrary-precision integer/rational semantics, the C++
compiler/runtime, hardware, and ordinary human/code-review error. No
floating-point mathematical decision, solver heuristic, incomplete proof
trace, random choice, or background computation is involved.

Reviewer: `reviewer-1`, 2026-09-05.
