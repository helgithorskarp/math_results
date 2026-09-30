# A 215-cell polyiamond realization of the known hexapillar-five example

Agent: **six-heesch-2**. Role: **researcher**. This is a reproduction and precise
scope correction, not a new marked-Heesch-five theorem or a priority claim.

The explicit unmarked polyiamond in tile.json has five complete hole-free coronas.
An independent mesh checker verifies every copy, every prefix and complete vertex
stars. A written angle-count proof includes arbitrary translations, rotations and
reflections, and gives the conservative bound **5 <= Hc <= Hh <= 112**. Thus the
tile is rigorously finite. The exact Heesch number is not established by this
package, and no independent reviewer verdict or formalization is claimed.

![The 215-cell polyiamond](tile.svg)

## Construction and certificate

Take four regular hexagons of side three in a straight strip, subdivide them into
216 unit equilateral triangles, remove nine centered boundary triangles and add
eight complementary external triangles. These are geometric cells, with no
remaining labels or imposed matching rules. The tile is edge-connected and has
one simple boundary cycle. Its boundary angles are 60:8, 120:30, 180:2, 240:22,
300:9.

The five-corona placement data come from six-heesch-3's exact reproduction of
[Mann's known marked fixture](../heesch_weighted_matching_obstruction/signed_hex4_depth5.witness.json).
Its unchanged input bytes have SHA256
d857774a28daa5e8f28e45a4ce711cc45ebc11cb759904fa98309122892aed0a.
The generator flips bump/nick signs globally, preserving matching, and places
single unit triangles on the centered unit segment of each side-three edge.

The fine triangular-grid vertex coordinates are integers. The physical basis
is (1,0),(1/2,sqrt(3)/2). Coarse hex centers (x,y) map to
3(x-y,x+2y). A coarse 60-degree rotation induces the same fine rotation, while
the coarse reflection (x,y)->(x+y,-y) induces fine (x,y)->(y,x). The generator
exports primitive integer isometry matrices and translations in coronas.json.
The independent checker reads only the geometric tile and these matrices; it
does not import the generator or trust symbolic edge labels.

| Corona | New copies | Cumulative copies | Unit triangles | Euler characteristic |
| --- | ---: | ---: | ---: | ---: |
| 0 | 1 | 1 | 215 | 1 |
| 1 | 5 | 6 | 1290 | 1 |
| 2 | 11 | 17 | 3655 | 1 |
| 3 | 23 | 40 | 8600 | 1 |
| 4 | 39 | 79 | 16985 | 1 |
| 5 | 52 | 131 | 28165 | 1 |

For each prefix, the checker cancels interior cell edges and verifies a single
simple oriented boundary cycle, edge connectivity and Euler characteristic one.
Different copies have disjoint unit cells and hence disjoint interiors. Every
unit-grid vertex of a preceding prefix has its complete six-triangle star filled
in the next, proving that the whole preceding prefix lies in the next prefix's
interior. Every added copy touches the immediately preceding corona. Thus the
certificate meets the closed-disc convention, not just a halo picture.

![Five checked coronas](five_coronas.svg)

## Finiteness and reproduction

[The full angle proof](angle_capacity.md) needs no grid-locking theorem: every
300-degree corner of an interior copy must be filled by a 60-degree vertex of
another copy. Distinct reentrant corners inject into convex tips, forcing
9*N_i<=8*N_(i+1). Exponential copy growth contradicts a quadratic area capacity;
the tile diameter is at most24 and the contradiction occurs at corona113.

From the repository root, using CPython3.11.2 or a compatible Python3 with only
the standard library:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      python3 heesch_polyiamond_hexapillar/check.py

The checker must match expected.json exactly. Optional deterministic regeneration:

    python3 heesch_polyiamond_hexapillar/generate.py
    python3 heesch_polyiamond_hexapillar/render.py
    python3 heesch_polyiamond_hexapillar/check.py

The certificate does not rely on the drawings. SVG coordinates use decimal
approximations solely for display. The proof arithmetic and cell coordinates
are exact integers. Trusted components are the written geometric injection and
diameter argument, Python and the definition-level checker. There is no SAT
solver, imported non-tiling verdict or unchecked numerical upper answer.

## Prior art and the research frontier

[Mann2004, Theorem1 and Figures5–6](https://faculty.washington.edu/cemann/Heesch.pdf)
already give the hexapillar-five family. Figure5's commensurate triangular outline
is relevant prior art for this realization. This package must not be called a
new five-corona discovery merely because it gives triangle-cell coordinates.
It independently makes the geometric lower witness and an all-motion finite
upper obstruction explicit.

[Kaplan2022](https://arxiv.org/abs/2105.09438) enumerates through24-iamonds,
17-hexes and19-ominoes. His record-four low-order tables do not imply a universal
upper bound of four for all unmarked polyforms. Accordingly the standing target
of any finite unmarked polyform with at least five coronas, without a size bound,
requires this prior-art qualification.

[Bašić2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7812982/) gives a general
six-corona figure built using regular hexagons, equilateral triangles and a half
triangle. That shape is not automatically an unmarked polyiamond; no such
conversion is claimed here. The next scoped frontier is a smaller finite-five
polyiamond, initially in a finite neighborhood of this215-cell shape, or a
finite-six polyiamond after a separate exact geometry proof. These remain
research questions, not consequences of the reproduction.

The preceding polyhex articulation-growth classification remains separate:
[source](../heesch_polyhex_bridge_growth/README.md). Neither its bounded exclusions
nor this reproduction classify arbitrary polyiamonds.
