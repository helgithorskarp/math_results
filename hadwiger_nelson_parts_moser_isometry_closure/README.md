# Parts-509 plus one pair-anchored Moser spindle: minimum order 509

**Exact computer-assisted result.** Let P be the published Parts-509 point
set. For every plane isometry T placing at least two distinct points of the
seven-point Moser spindle on P, every unit-distance subgraph of `P union T(M)`
on at most **508 vertices is four-colourable**. Reflections, all additional
unit contacts, and every partial selection of spindle points are included.

The complete geometric census has **25,590 placements**. Direct positive
colouring checks, ending in **42 explicit colourings of 508-point graphs**,
close the whole family. Since each full union contains P, the minimum order
of a non-four-colourable subgraph is exactly 509. The result does not improve
the record or give a global vertex lower bound.

This pass followed the direct record lane: add an entire rigid four-chromatic
motif in every placement determined by two coincidences, allowing new support
and simultaneous vertex replacement. The initial degree gate left 2,213
placements with five new vertices of degree at least four. Subsequent checks
closed them and then checked the entire family independently of the old
four-new-point exclusion theorem. This is not a repeated deletion scan of a
previously closed fixed host.

See [PROOF.md](PROOF.md) for the exact isometry reduction, deletion-budget
argument, partial-selection coverage, and trust boundary. No SAT/UNSAT answer
is trusted: the final verifier uses exact arithmetic and positive colourings.
A second implementation in a different complex number field representation
agrees entry by entry on the geometry. Both implementations were run by the
same author; an independent external review is still outstanding.

## Reproduce

From the repository root, Python 3.11+ and the standard library suffice:

```sh
python3 -B hadwiger_nelson_parts_moser_isometry_closure/verify.py --check-expected
```

The recorded run took about 53 seconds and 134 MiB maximum RSS. Expected output
includes `target_rows=42`, `target_edge_checks=101723`, and
`all_sub509_subgraphs_four_colourable=true`. The compact certificate SHA-256 is
`9315dda9981850529ecb7e816f2c055e3e376796327b878691d7b081b109bacc`.

[REPRODUCE.md](REPRODUCE.md) gives the additional arithmetic check, exhaustive
small controls, and optional witness regeneration. [DEPENDENCIES.json](DEPENDENCIES.json)
pins the three existing input files. Only the coordinate table and 6,398
explicit positive colouring rows are imported from them. The verifier checks
every row on its retained strict original edges. Expanded coordinate output,
search transcripts, Python environments and timing logs stay outside Git.

## Scope and next decision

Stop the pair-determined single-spindle family: every target-sized subgraph is
now covered. This theorem leaves placements with at most one coincidence,
multiple coupled motifs, and different support constructions open. A future
record attempt needs a different geometric mechanism; automatically increasing
an attachment count is not justified by this result.

The working record of 509 was rechecked on 13 September 2026 in
[Parts' primary paper](https://arxiv.org/abs/2010.12665) and the introduction of
[Haugland's August 2026 manuscript](https://arxiv.org/html/2608.04542v4).
Moser-spindle-free constructions address a separate restriction.
Targeted Discovery Net and repository searches found no earlier closure of
this exact pair-anchored Parts/Moser family. No historical priority claim is
made. Prior source context and the stale ledger boundary are recorded in
[CONTEXT.json](CONTEXT.json).
