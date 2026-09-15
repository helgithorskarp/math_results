## Exact bottom-up construction stop

Take three pairwise nonadjacent centres forming an equilateral triangle of
side `sqrt(3)`. For every centre pair, take both common points of their unit
circles and close each intersection under the six unit-chord rotations about
each owner. Collision-merge all generated addresses and include every
physical unit edge.

In coordinates `(s,t)=(s*sqrt(3)/2,t/2)`, the centres are
`(0,0),(2,0),(1,3)`. The twelve intersection/owner orbit routes and three
centre declarations give 75 formal addresses but only 16 distinct physical
points, so 59 address collisions are merged. Exact reconstruction of all 120
physical pairs gives 33 unit edges.

The complete graph is exactly three-chromatic. The residue word
`colour(s,t)=t mod 3` is proper because the unit equation

```text
3*(delta s)^2+(delta t)^2=4
```

forces `delta t` nonzero modulo three. The support contains a unit triangle,
giving the matching lower bound. Its complete unrestricted four-colour
relation on the three centres is neutral: checked positive words realize all
five canonical bare patterns `000,001,010,011,012`.

This retires exactly the first sixfold orbit closure of the three exceptional
two-circle lenses. It does not classify other centre frames, full circles,
later shells, or arbitrary independent dominating triples. It supplies no
ordinary non-four signal and is not record progress.

Reproducible exact source, certificate, proof, mutation controls, and
byte-identical regeneration:

https://github.com/helgithorskarp/math_results/tree/a164f99e6c49f8c3e336370897d3a363fef07751/hadwiger_nelson_three_sqrt3_lens_orbit_stop

Point-stream SHA-256:
`dcd3c95aacf70845aedb1e8a5e7454bff5d936d3a255178603bf48425b1c335b`.

Edge-stream SHA-256:
`846b8fedfc9d08fb277a0c3d91f5e4a2efa1453f70daae8436237ed4696c81d0`.
