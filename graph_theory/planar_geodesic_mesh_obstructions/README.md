# Two capped-mesh construction families are excluded

For [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf),
two infinite families always have a **half-balanced** separator that is the
union of at most two shortest paths in the original graph:

1. A cylindrical grid capped by two poles, with either diagonal or no
   diagonal independently chosen in each quadrilateral.
2. The corresponding rectangular grid with top and bottom cap poles and
   an added edge joining the poles through the outer face.

The conclusions hold for arbitrary nonnegative vertex weights and after
attaching any number of leaves at each vertex. They are negative results
for these proposed counterexample families, not a solution of Problem 31.
No priority claim is made.

[PROOF.md](PROOF.md) gives complete elementary proofs. In the cylindrical
case two appropriately chosen meridians suffice. In the rectangular case
the added shortcut destroys the full meridians as shortest paths, but a
median meridian is covered by two geodesic halves. A map to a cycle proves
shortestness in the ambient graph, even with the cell diagonals present.

The construction lane is responsible for these family exclusions. The
general weighted-obstruction lifting reduction is separate work of the
structural lane and is not claimed here.

Run from this directory, using Python 3.11.2 or compatible Python 3 with
only the standard library:

```sh
python3 verify.py --check
```

Expected: `PASS`, 3,750 cylindrical witnesses, 750 shortcut witnesses, 225
pendant-inflated witnesses, and six deliberately rejected invalid inputs or
witnesses. The largest checked graph has 201 vertices. The complete compact
output is [expected.json](expected.json). The deterministic weighted-witness
stream SHA256 is
`7dc4ad02f91c843393b27228c6a1ca52c1d50854539c38f812239a06c472d336`.

The verifier uses BFS to establish endpoint distance and an explicit
component traversal after vertex deletion; it does not use the proof's
level maps or component-weight bounds. All arithmetic is exact Python
integer arithmetic. It checks the displayed witnesses, not every pair of
paths or every planar graph. The infinite statements depend on the written
proofs, not extrapolation from the stress suite. No solver, external graph
dataset, formal proof assistant, or omitted certificate is required.
