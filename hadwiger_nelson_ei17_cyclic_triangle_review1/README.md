# Independent review of the cyclic EI17 full-input stop

Verdict: **accept, with strict fixed-source, cyclic-frame, and conservative-
contact limitations**.

An independent exact implementation confirms the target theorem for all 124
declared three-copy frames.  Each frame consists of 48 physical points and
contains the certified 17-point, 31-edge, four-chromatic EI17 source.  Every
complete source four-colouring extends through every frame's conservative
complete-contact upper graph.  Consequently every actual strict physical unit
graph in this family has chromatic number exactly four.

This is a valid stopping result for one architecture.  It is not a
five-chromatic construction or record candidate.

## Independent method

The review imports neither target code nor the EI17 source checker.  It parses
the pinned rational midpoint and edge list, recomputes the exact midpoint
Jacobian inverse, and proves the source root unique in its radius-`10^-18` box
using an entrywise `Fraction` interval enclosure of `I-AJ(X)`.  Direct interval
distance checks establish source distinctness and faithfulness.  A fixed-order
three-colour search independently proves the source non-three-colourable.

All 124 transformed frames are rebuilt with a new rational interval type and
a 70-decimal exact bracket for `sqrt(3)`.  The construction scans every label
and physical pair.  Its group-and-edge stream is byte-for-byte identical to
the target stream:

```text
6bb50a2375d31f15ab407fa24e5cb87ed003999eb0ee486d05c1b1e757abe913
```

The same census results:

| Conservative upper graph | Frames |
|---|---:|
| 48 vertices, 93 inherited edges | 116 |
| 48 vertices, 93 inherited plus 3 possible edges | 8 |

The word “possible” is essential.  For the latter eight frames, the proof does
not decide whether any of the three extra pairs is exactly unit.  It colours
the larger 96-edge upper graph, which is sufficient because every actual unit
graph is a subgraph of it.

## Independent full-input check

Instead of the target's 85,088 restricted-growth DSATUR representatives, the
review enumerates all 170,176 labelled source colourings with the fixed source
edge `(10,16)` assigned colours `(0,1)`.  Because the source is exactly
four-chromatic, each global-colour orbit occurs exactly twice in that census;
division by two independently recovers 85,088 orbits.

For the 116 plain upper graphs, the cyclic colour-permutation argument is
checked symbolically for all 12 ordered distinct anchor-colour pairs in every
frame, giving 1,392 checks.  For the eight conservative contactful frames, a
separate backtracker proves extension for every one of the
`8*170176 = 1,361,408` fixed-edge source/frame cases.  These collapse to 9 or
27 literal domain states per frame, each with a directly checked witness.

An additional independent-set partition algorithm finds 1,181 independent
sets and 85,088 partitions into four nonempty independent sets.  This confirms
the orbit count without sequential colour assignment.  The domain solver is
compared with brute force on 43,923 small instances.

## Structural refinement

The target correctly reports no articulation vertex or bridge.  The review
sharpens this: every inherited union has minimum degree three and exactly
three two-vertex cuts, namely the three pairs among the equilateral anchors.
Thus every union has vertex connectivity exactly two.  The construction is
cyclic and 2-connected, but it remains a cycle of edge-based 2-sums; it should
not be treated as a 3-connected forcing source.

## Reproduction

CPython 3.11 or later and a complete repository checkout are sufficient.  No
third-party package or solver is used.  From this review directory:

```sh
python3 -B verify.py --check-expected
python3 -O -B verify.py --check-expected
python3 -B controls.py
python3 -O -B controls.py
sha256sum -c SHA256SUMS
```

See [PROOF.md](PROOF.md), [REVIEW.md](REVIEW.md),
[PROVENANCE.md](PROVENANCE.md), and [VALIDATION.json](VALIDATION.json).

The reviewed target revision is
`abadf3d5f33005152f588fe0a2e2a52cf0d204eb`.  Large witness streams are
regenerated and hashed rather than stored.

## Exact scope and record status

The theorem covers one certified EI17 realization and the 124 frames obtained
by choosing one of its 31 source edges, an endpoint order, and an orientation,
then cycling that same normalized copy onto all three triangle sides.  It does
not cover independent edge choices on the three copies, other EI17
realizations, polygons, copy counts, phases, or later completion operations.
The 124 entries are labelled frames, not 124 claimed incongruent graphs.

The result remains four-chromatic.  Parts's published 509-point, 2,442-edge
construction remains the supported unrestricted record in the bounded source
check; Haugland's 2026 paper describes it as current while studying the
different Moser-spindle-free frontier.

## Sources

- Reviewed target:
  <https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_ei17_cyclic_triangle_full_input_stop>.
- Exact EI17 source package:
  <https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_ei17_common_pair>.
- Silva Filho, [Exact certification of the coordinate fields of the
  triangle-free Exoo--Ismailescu unit-distance graphs](https://arxiv.org/html/2607.19995).
- Parts, [Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane](https://arxiv.org/abs/2010.12665).
- Haugland, [A Moser-spindle-free 5-chromatic unit distance graph on 2131
  vertices in the plane](https://arxiv.org/abs/2608.04542).

The requested `math-review` skill was unavailable.  Its independence,
exact-scope, geometric-realization, chromatic-certificate, hidden-assumption,
and source-integrity criteria were applied directly with the available exact
computer-assisted, geometric, Discovery, and GitHub research skills.
