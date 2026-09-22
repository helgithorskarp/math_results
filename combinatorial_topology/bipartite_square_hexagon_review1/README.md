# Independent review: hexagonal spheres in bipartite graph squares

This directory records an independent review of the theorem in
[`../bipartite_square_hexagon`](../bipartite_square_hexagon).  For a finite
connected simple bipartite graph `B` with no four-cycle, the theorem detects
the octahedral sphere of every six-cycle in `Cl(B^2)`, identifies the
resulting integral six-cycle lattice in second homology, and proves that
`Cl(B^2)` is aspherical exactly when `B` has no six-cycle.

The verdict is **accept with high confidence in the stated scope**.  The
proof reconstruction, explicit human premises, completeness reductions,
caveats, and literature boundary are in [`REVIEW.md`](REVIEW.md).

[`independent_check.py`](independent_check.py) is a definition-level checker
whose implementation is separate from the target's checker.  It represents
faces by bit masks, checks collapse pairs globally at the moment of deletion,
constructs transition digraphs for both Dowker matchings, uses exact integer
chains for the detector, and computes rational homology by dense `Fraction`
elimination.  It exhausts the `3 x 5` and `4 x 4` labelled incidence
rectangles, all eight-vertex bipartitions capable of containing a six-cycle
up to exchanging the colors, and also checks hand-picked hypothesis and
dependency boundaries.

Reproduce with standard-library Python 3.11 or later:

```sh
./run_checks.sh
```

Expected runtime is about 30 seconds in the review environment.  This is
supplementary finite evidence.  The universal integral theorem still rests
on the written collapse, chain-map, Mayer--Vietoris, fundamental-group, and
asphericity arguments enumerated in the review.
