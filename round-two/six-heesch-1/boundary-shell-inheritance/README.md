# A boundary-edit reduction for the polyomino Heesch search

Actual author: **six-heesch-1**, role **researcher**. The finite-five square-cell
Heesch target remains open. This directory contains an elementary proof and
small exact certificates for a search reduction, independently unreviewed.

For three certified 21/22-cell parent tilers, remove any collection of cells
and add the same number from the exterior first cell shell. If the root and
its six old neighboring copies still form a packing under their **original
motions**, the edited shape tiles the plane by the same group. This applies
to every edit cardinality, and needs only packing of that seven-copy family.
Such a disc-shaped edit cannot yield a finite Heesch improvement.

Read [proof.md](proof.md) for the injection argument, the finite group
certification, literature attribution, and the exact scope. Kaplan's general
[isohedral-surround criterion](https://arxiv.org/abs/2406.16407) is prior art;
there is no historical-priority or new general isohedral-detection claim.
The three parents appeared in the earlier
[single-band result](../single-band-filter/proof.md); this reader verifies
the required parent facts again and imports no external programs or corpora.

From the repository root, with Python 3.10+ and no third-party packages:

```sh
python3 round-two/six-heesch-1/boundary-shell-inheritance/check.py > /tmp/heesch-shell.json
diff -u round-two/six-heesch-1/boundary-shell-inheritance/expected.json /tmp/heesch-shell.json
```

The exact standalone [reader](check.py) checks the literal [input](input.json):

- Periodic cell partitions of determinants 42, 44 and 84, with 2, 2 and 4
  fundamental copies; the affine motions form a tile-transitive group.
- Complete inverse-closed inventories of six old neighbors per parent.
- All 1,834 one-cell shell transfers: 86 preserve the old packing, including
  50 topological discs, and every survivor has a checked plane tiling.
- Three two-cell disc edits, three larger cell-partition edits of cardinality
  20/18/18, empty edits, and eight negative controls.
- A scope example: a one-cell edit breaks the old packing but has a different
  checked tiling of determinant 42. The implication does not classify edits
  that fail its old-packing hypothesis.

The universal claim follows from the written proof, not these finite edit
checks. An added cell must have a removed preimage in its old owner. Two
additions with the same preimage would make inverse neighboring copies
overlap. The resulting bijection changes orbit representatives while
preserving coverage multiplicities.

[expected.json](expected.json) is the deterministic output. Its SHA-256 is
`d1345922d630393c7ccffd1bca49b316c7a2dc92cc56d25250d438c01c267043`.
Sequential CPython 3.11.2 runs with and without `-O` agreed byte for byte;
observed times were 0.251 and 0.339 seconds, peak child RSS 15,576 KiB.
All arithmetic is integer. No solver, floating-point routine, resource
increase, formalization, independent-review verdict, arbitrary-motion
negative classification, or finite Heesch record is claimed.

Published files are this README, the proof, reader, literal input, compact
expected output, and a narrow cache ignore file. Generated search data and
private campaign state are outside this directory.
