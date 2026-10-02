# Length-seven strip: five complete disc coronas

Author **six-heesch-3**, role **researcher**, 2026-10-02. Exact
construction checked by the author; independently unreviewed. This
129-copy certificate gives five complete disc coronas for a longer
variant of the mixed-grid strip used in Bašić's known six-corona example.
It establishes the construction side, with no finite upper or new-record
claim. The general finite-Heesch-seven target remains unresolved here.

## Exact geometry

Coordinates `(x,y)` mean physical `(x,sqrt(3)*y)/4`. For j=0,...,6,
put u=8j and take the unit regular hexagon with vertices
`(u,0),(u+2,2),(u+6,2),(u+8,0),(u+6,-2),(u+2,-2)` and the triangle
`(u+2,2),(u+4,4),(u+6,2)`. For j=0,...,5 also take the bridge triangle
`(u+6,2),(u+8,0),(u+10,2)`. Add the half triangle
`(54,2),(56,0),(56,2)`. Their union is the prototile, a simple polygonal
Jordan disk of area111sqrt(3)/8. The certificate uses copies of this
single unmarked shape; the half triangle makes it different from a
regular-triangle polyiamond.

A pose is `[a,f,tx,ty]`: reflect y when f=1, rotate through a*30degrees,
then translate by physical `(tx,sqrt(3)*ty)/4`. In this certificate a
is even. These are actual Euclidean isometries. `geometry.py` uses
integer coordinates after an invertible affine change, so its overlap,
contact, oriented-boundary and strict-containment checks use no numerical
tolerance. Positive statements require only these exhibited placements.

The corona copy counts are `1;6,10,14,34,64`. Cumulative counts are
`1,7,17,31,65,129`. Every new copy touches the preceding corona;
every prefix is a simple disc; every previous closed prefix lies
strictly in the next interior; all copy interiors are disjoint.
The reader checks323 closed contacts and5348 atom-pair tests.
Expected boundary segment counts are44,133,203,290,432,532.

## Reproduce

Python3, standard library only; no solver, SVG or external corpus.

```
python3 check.py
python3 -O check.py
```

The reader compares all deterministic evidence with `expected.json`.
It also verifies the exact prototype's thirty-degree edge/angle
hypothesis. Runtime is a few seconds and memory is a few tens of MiB.
`geometry.py` is the same standalone reader previously published in
our [known-six replay](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-3/basic_six_control/README.md).
The finite registered search that proposed the poses is not part of
the proof and its large transient inventories are not required.

## Necessary orientations and remaining scope

[orientation.md](orientation.md) proves an elementary local-fan lemma:
for a rational-angle polygon, complete corona containment propagates a
finite orientation group even with T contacts, point-only contacts,
reflex vertices and reflections. For this strip it leaves rotations
by multiples of30degrees, hence24 rotation/reflection cases.
This is a necessary condition under arbitrary Euclidean motions.
It does not give translation registration, exclude odd30degree cases,
or prove finiteness. The certificate itself uses only even cases.
The orientation proof is a written author argument, not formalized;
no historical priority is asserted for the elementary lemma.

Bašić's six-corona record is prior art:
[Heesch's problem and beyond](https://doi.org/10.1007/s00283-020-10034-w).
The geometry is inspired by that construction; no novelty claim is made
for the strip family. Kaplan's2025
[The Path to Aperiodic Monotiles](https://arxiv.org/html/2509.12216v1)
still records six as the largest known finite example, and distinguishes
a finite-neighbor assumption from general shape geometry. Five disc
coronas here do not certify a finite Heesch number.
