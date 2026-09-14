# A sixteen-point unit-distance gadget with an essential eight-terminal relation

Two explicit nine-point cells share a unit edge. Their collision-merged strict
plane unit-distance union has **16 points and 25 edges**. Each cell alone
permits every four-colour pattern on its four independent input terminals.
The combined graph forbids **104 of the 2795** patterns on its eight
independent terminals. **32** of these obstructions require all eight pins:
every seven-pin restriction extends.

This is a small exact physical composition with a real joint relation. It is
**three-chromatic**, and does not improve the five-chromatic record. No
abstract colouring obstruction is presented as a new plane realization.

The relation has a short interpretation. Let the two opposite `X` pairs use
the same two-colour palette `P`, and the two opposite `Y` pairs use the same
two-colour palette `Q`. An extension exists exactly when `P` and `Q` are
disjoint. The complete theorem also covers all monochromatic-pair inputs;
the gadget itself does not force the repeated or bichromatic input premises.

[PROOF.md](PROOF.md) gives the coordinates, exact graph, path-elimination
relation, direct three-case palette proof, counts, and budget limitation.
[points.tsv](points.tsv) fixes all sixteen physical points. Each pair's
distance is `sqrt(3)`; the eight interior points are their unit-circle
intersections. With eight existing terminals an attachment costs at most
eight new vertices, so a suitable host of order at most 500 would fit the
508-point budget. Such a forcing host is still missing.

The first bounded attachment is closed: all unit-circle intersections at the
126 distance-`sqrt(3)` pairs of the existing 421-point Haugland difference
host are already present. Thus any matching comparator is already contained
in that host. No new point or strengthened graph is obtained. This attachment
is retired; no phase, copied-host, or allowance expansion follows it.

## Reproduce

Python **3.11.2**, standard library only; no SAT library or floating arithmetic
is needed. From this directory:

```sh
python3 -B verify.py --check-expected
python3 -O -B verify.py --check-expected
python3 -B controls.py
python3 -B host_gate.py
sha256sum -c SHA256SUMS
```

Regenerate the certificate to a fresh external path:

```sh
python3 -B produce.py --output /tmp/fresh-opposed-palette-certificate.json
cmp /tmp/fresh-opposed-palette-certificate.json certificate.json
```

The producer uses exact sparse-radical multiplication and general complete
colour-domain search. The verifier imports neither. It reconstructs the
coordinates from separate closed formulas, uses integer prime-mask
multiplication for all pair distances, checks every positive word directly,
and decides the complete relation by eliminating the three internal colours
of each cell. The colour-permutation quotient is complete because the checker
normalizes all `4^8` named terminal assignments independently of the producer's
restricted-growth generation. Colourings with fewer than four colours are
included throughout.

The compact certificate includes 2691 positive full words, all 104 forbidden
patterns, 15 single-cell extensions, a three-colouring, and eight witnesses
for relaxing the pins in `01020102`. Controls compare the two exact arithmetic
implementations on all 120 pairs and compare path elimination with general
search on all 3072 proper ordered-edge/input assignments. Ten corrupted
certificates are rejected, including a proper word with wrong terminal pins.
Normal and optimized verification agree, and regeneration is byte-identical.
Hashes, timings and trust boundaries are in [VALIDATION.json](VALIDATION.json).
This is author-run exact evidence, pending independent review, not a formal
proof-assistant development.

## Dependencies and scope

The sixteen-point result is self-contained. Only the auxiliary host gate
imports the existing
[Haugland difference geometry](../hadwiger_nelson_heptagon_difference_lifts/README.md),
mathematical commit `b42754c605b69877056555955ac7f72a56e824f3`. The imported
`geometry.py` bytes are pinned in `host_gate.py`. Its existing four-colourability
and the later
[84-pair joint monochromatic result](../hadwiger_nelson_heptagon_joint_pairs/README.md)
were read as construction context; neither is a premise of the sixteen-point
relation. No claim is made about the earlier 42 unresolved monochromatic-pair
queries, which were not rerun.

Live primary-source checks on 2026-09-14 still found
[Parts' 509-point construction](https://arxiv.org/abs/2010.12665), also used as
the unrestricted record comparison in
[Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4).
No priority or smallest-source claim is made for the standard odd-cycle and
diamond mechanisms or the present explicit gadget.

The next mathematical gate is a budgeted physical driver for the repeated
input palettes or another forbidden full terminal pattern. A larger sum of
cells without such a driver is not justified by this result. This package
does not reopen native allowances, A159, odd-valuation sweeps, L10 windows,
the F29 reflected-chord transfer, Parts inversion, triangular phase patches,
or H510/Heule deletion supports.
