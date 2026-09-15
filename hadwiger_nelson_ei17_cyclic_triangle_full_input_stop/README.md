# EI17 cyclic-triangle full-input stop

Three congruent copies of one exact 17-point, 31-edge, triangle-free,
four-chromatic EI17 realization are placed cyclically on the three sides of a
unit equilateral triangle.  For every choice of a source edge, its endpoint
order, and orientation, the resulting physical graph is four-colourable and
**every complete four-colouring of the first EI17 copy extends**.  Thus this
nonseparable whole-support operation does not couple the source's certified
four-chromatic forcing.

This is an exact, finite negative construction result.  It retires this one
cyclic three-copy architecture; it is not a five-chromatic graph, a record
candidate, a theorem about other EI17 realizations, or permission to sweep
other polygons, copy counts, source pairs, or phases.

## Construction and result

Let `P` be the exact EI17 realization certified in the sibling package
[`hadwiger_nelson_ei17_common_pair`](../hadwiger_nelson_ei17_common_pair).
For each of its 31 unit edges, each endpoint order, and each of the two plane
isometries taking that ordered edge to `A=(0,0), B=(1,0)`, take the normalized
copy `P_0`.  With

```text
C = (1/2,sqrt(3)/2),  zeta = (-1+i sqrt(3))/2,  T(z)=1+zeta*z,
```

put `P_1=T(P_0)` and `P_2=T^2(P_0)`.  Their marked edges are respectively
`AB`, `BC`, and `CA`.  This gives `31*2*2=124` labelled frames.

Exact rational interval arithmetic proves that each frame collision-merges to
48 distinct physical points: the 51 labels have exactly the three prescribed
pairwise anchor identifications.  All 93 inherited source edges are present.
For every other physical pair, the checker either excludes squared distance
one or adds the pair to a conservative upper graph.  The census is:

| Conservative complete-contact upper graph | Frames |
|---|---:|
| 48 points, 93 inherited edges, no possible extra edge | 116 |
| 48 points, 93 inherited plus 3 possible cross edges | 8 |

Every actual strict unit graph is a subgraph of its conservative upper graph.
After flooring in units of `10^-12`, the smallest coordinate-separation margin
has lower bound `447152094` and the smallest exclusion margin from squared
distance one has lower bound `157811208`.  The inherited-edge union has no
articulation vertex and no bridge in all 124 frames.

The source has exactly 85,088 complete proper four-colourings modulo global
colour permutation.  In each of the 116 contact-free frames, every such word
extends by an elementary cyclic permutation of colours on copies 1 and 2.  In
each of the eight contactful frames, an exact finite-domain search supplies and
directly checks a witness for every source word: 680,704 source/frame checks.
Only 27 or 39 distinct initial domain states occur, and `controls.py` re-solves
all of them with a separate algorithm.  Since every union contains the exact
four-chromatic source, each actual complete physical graph has chromatic number
exactly four.

## Reproduce

From the repository root, using Python 3.11 or later and no third-party
packages:

```sh
python3 -B hadwiger_nelson_ei17_cyclic_triangle_full_input_stop/verify.py --check-expected
python3 -O -B hadwiger_nelson_ei17_cyclic_triangle_full_input_stop/verify.py --check-expected
python3 -B hadwiger_nelson_ei17_cyclic_triangle_full_input_stop/controls.py
python3 -O -B hadwiger_nelson_ei17_cyclic_triangle_full_input_stop/controls.py
(cd hadwiger_nelson_ei17_cyclic_triangle_full_input_stop && sha256sum -c SHA256SUMS)
```

`verify.py` hash-pins the four exact source files, reruns the source root and
faithfulness certificate, constructs all 124 frames, collision-merges the
three prescribed anchor pairs, encloses every physical pair, enumerates the
85,088 normalized complete source colourings, and validates every extension
witness.  `EXPECTED.json` freezes the full result and witness-stream hashes.

`controls.py` independently obtains the source-colouring count in fixed vertex
order (225,141 search nodes), rebuilds all geometry, re-solves all distinct
contactful domain states with a separate backtracker, checks the equilateral
cycle map, and rejects a corrupted structural witness.  No floating-point
operation, SAT verdict, unprovided coordinate, or guessed equality enters the
proof.

## Scope, sources, and record context

The exact EI17 package is pinned at commit
[`9724508c76581b2283bbe65e02be77433a0146a4`](https://github.com/helgithorskarp/math_results/tree/9724508c76581b2283bbe65e02be77433a0146a4/hadwiger_nelson_ei17_common_pair).
Its numerical seed was transcribed from Section 1 and Appendix A of
[Silva Filho, arXiv:2607.19995](https://arxiv.org/html/2607.19995), while its
existence, local uniqueness, distinctness, faithful complete unit graph, and
four-chromaticity are certified in the repository rather than imported from
that manuscript.  The abstract small graphs originated with Exoo and
Ismailescu, *Small Order Triangle-Free 4-Chromatic Unit Distance Graphs*,
Geombinatorics 26(2), 49--64 (2016).

[Parts's 509-point graph](https://arxiv.org/abs/2010.12665) remains the supported
unrestricted vertex record and is still described as current by
[Haugland v4](https://arxiv.org/html/2608.04542v4).  This 48-point result is
four-chromatic, so it does not improve that record.  See [PROOF.md](PROOF.md)
for the proof obligations and [PROVENANCE.md](PROVENANCE.md) for the evidence
boundary.
