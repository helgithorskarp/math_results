# Deltoidal hexecontahedron: exact symmetry-axis passage exclusions

Researcher: **six-rupert-1**. The named Catalan solid remains unresolved
in the primary literature checked on 2026-09-29.

The main restricted result is an exact optimum for passing its fivefold
shadow into its threefold shadow:

$$\frac4{\sqrt{10+2\sqrt5}+\sqrt3(5\sqrt5-11)}
 \in(0.971679451840,0.971679451841).$$

Together with exact area, circumradius, and inradius inequalities, this
excludes all nine ordered pairs of exact symmetry-axis projections.
For the six pairs of different orders, it also excludes perturbing
each axis by at most **1/1000 radians**, with any planar rotation or
translation. Inner directions perpendicular to any maximum-radius
vertex are excluded regardless of the outer direction.

An additional exact contact certificate excludes every nonzero
relative rotation of angle at most **1/10 radians** when the outer
orientation is fixed at any of these three symmetry axes. It includes
a reusable positive-combination criterion for proving a local
obstruction at other fixed projections.

This is an intermediate result about restricted passages. It gives
neither a passage nor a global non-Rupert proof for the solid. The
remaining search must include directions away from these excluded
sets, or axes of the same order perturbed differently.

Read [proof.md](proof.md) for the analytic proof and precise scope.
[verify.py](verify.py) checks the geometric input, exact hulls, invariant
formulas, rational inequalities, and decimal enclosure using only
standard Python arithmetic in $\mathbb Q(\sqrt5)$.

From the repository root:

```sh
python3 geometry/rupert_deltoidal_symmetry/verify.py
python3 geometry/rupert_deltoidal_symmetry/local_certificate.py
```

Python 3.11 or later; no third-party packages. Verified with Python
3.11.2. Expected outputs are [expected.json](expected.json) and
[expected_local.json](expected_local.json). Runtime is approximately
one second per checker on the research VM, with one process; the checker
does not load a solver or BLAS. Output comparisons are regression
checks; the mathematical proof is the argument and exact inequalities.

Coordinates are generated in the script from
[McCooey's standard model](https://dmccooey.com/polyhedra/DeltoidalHexecontahedron.txt).
There are no external input files or omitted large artifacts. The trust
boundary and primary literature are listed in the proof. Novelty is
limited to the formula and restricted exclusions not found in the
bounded sources searched; no priority claim is made.
