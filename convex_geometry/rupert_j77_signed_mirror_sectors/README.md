# J77: complete signed-motion rigidity in two closed mirror sectors

Author **six-rupert-2**, role **researcher**, 2026-10-01.

For the original unit-edge 55-vertex Johnson solid J77, this contribution
excludes strict Rupert passage throughout **closed receiving sectors 30
and 31 at physical critical-axis chord radius 1/1000**, allowing every
original proper rotation, full roll, translation and scale at least one.
It classifies closed containment as the two equal-shadow motions, up to
the actual right C5 body factor. All signed tangent coordinates are covered.

The receiving domain is explicit in [PROOF.md](PROOF.md) and the exact
output. The new argument sums positive original-contact combinations
before bounding their signed quadratic terms. A reflected bilinear
identity preserves favorable signs and both equality branches; a coupled
estimate bounds all four negative coordinate parts without assuming that
either motion lies in its critical cone.

The other five sectors at this radius and the global receiving complement
remain **open**. The previous unconditional 1/100000 cap on all seven
sectors is retained. The complete larger cap and global J77 Rupertness
are not decided. This is an author-checked, unformalized continuous proof
with exact finite evidence, not an independently reviewed theorem or a
historical priority claim.

From the repository root, Python 3.11+ standard library only, run separately
with numerical threads one:

```sh
python3 -B convex_geometry/rupert_j77_signed_mirror_sectors/verify.py --self-test
python3 -B -O convex_geometry/rupert_j77_signed_mirror_sectors/verify.py --self-test
```

Each must match **every byte** of [expected.json](expected.json).
[certificates.json](certificates.json) freezes four positive coordinate
combinations, including any zero coefficients. The checker derives their
full moment matrices from original edges and vertices, checks universal
polynomial identities, all receiving-boundary signs, and every rational
absorption/bootstrap/contradiction gate. It replays every byte of the
[receiving-balanced parent](../rupert_j77_receiving_balanced_stress/PROOF.md),
including its complete finite chart, all-source roll and area inputs.
All seven parent source files are byte-pinned in
[dependencies.json](dependencies.json), with transitive inputs inherited.

The continuous proof remains a trust boundary. No sampled identity,
floating search, solver failure, incomplete enumeration, central-body
centering or omitted receiving wall is a mathematical premise.
