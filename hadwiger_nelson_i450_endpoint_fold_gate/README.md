# The marked I450 inequality cannot be converted by one-axis folding

The published I450 source has **450 exact points, 2,290 strict unit edges**,
and two marked points O,V at distance `sqrt(11/3)` which differ in every proper
four-colouring. A proposed transfer was to preserve its unit edges while
identifying O and V geometrically. Any such image would be non-four-colourable
on at most **449 points**: a four-colouring of the image would pull back to
an impossible equal-pin colouring of I450. A proper five-colouring would still
have to be checked before calling the image five-chromatic.

The selected transfer allows each point to stay fixed or reflect across one
common line, with arbitrary choices, preserving every inherited unit edge.
**No such map identifies O and V.** An exact three-edge path already blocks
it. This is the complete preflight failure of that transfer, not a new physical
support, a stronger interface relation, or progress on the 509-vertex record.
No other endpoints, inputs, sequential folds, deletions or free deformations
were searched or excluded.

## Exact obstruction

Use the coordinate convention from the
[parent construction](../hadwiger_nelson_overlapping_forcing_seed/README.md):

```
[a,b,c,d] = ((a*sqrt3+b*sqrt11)/36, (c+d*sqrt33)/36).
```

I450 is the `unequal` component of the parent's `certificate.json`. The full
file SHA256 is
`3a487318d1d417e812791a1fd66d679151a7816fcf325a5bfd6a0351a0663237`.
The marked rows are `O=[0,0,0,0]` and `V=[0,0,0,12]`.
If opposite reflection choices identify two distinct points, the reflecting
line must be their perpendicular bisector. Thus the only possible line is
`L: y=sqrt33/6`; its reflection is exactly

```
R[a,b,c,d] = [a,b,-c,12-d].
```

For any line L, reflect exactly one endpoint of a unit edge. In coordinates
where L is horizontal, the squared edge length changes by `4*y_u*y_v`, where
the y values are signed distances from L. Therefore choices must agree on
every edge whose endpoints are off L. Equivalently, choices are constant on
each connected component after removing vertices on L. This standard
criterion was already used in the
[nine-move seed fold gate](../hadwiger_nelson_bisector_fold_gate/README.md);
no novelty is claimed for it.

Here the following path avoids L:

| Source label | Coordinate row | 1296 times (distance² to O − distance² to V) |
|---:|---|---|
| 0 | [0,0,0,0] | −4752 |
| 10 | [−3,−9,−9,3] | −2376 − 216 sqrt33 |
| 16 | [3,−9,−9,9] | 2376 − 216 sqrt33 |
| 1 | [0,0,0,12] | 4752 |

All three consecutive distances are exactly one. Every value in the last
column is nonzero. Thus all four vertices must make the same reflection
choice. O and V remain distinct whether both stay or both reflect.

For a difference row `[a,b,c,d]`, squared length is

```
(3a²+11b²+c²+33d² + 2(ab+cd)*sqrt33)/1296.
```

This identity verifies the path and every table entry with integers only.
A second finite check examines all 16 choices on the four path vertices:
exactly `0000` and `1111` preserve the three unit edges, and neither identifies
the endpoints. Any admissible map of the full source must restrict to one of
these path maps. The argument includes arbitrary real axes because the target
collision uniquely determines L; there is no angle-grid assumption.

## Evidence and reproduction

Keep this directory alongside the parent package. Python 3.11.2, standard
library only:

```sh
python3 -B verify.py --check-expected
python3 -O -B verify.py --check-expected
python3 -B controls.py
sha256sum -c SHA256SUMS
```

[verify.py](verify.py) reads the hash-bound parent coordinate fixture but
imports no parent code. It checks all **101,025** source pairs, obtains all
2,290 strict edges, verifies the saved positive four-colouring, checks path
membership and all 16 choices, and finds the exact seven on-axis labels
`[2,3,67,97,181,306,438]`. The path alone proves the negative fold result;
the full reconstruction provides the construction preflight and provenance.

[controls.py](controls.py) compares every norm vector with independent
prime-mask radical arithmetic and repeats the 16 path choices. Its positive
control is the unit path
`O -> [6,0,0,6] -> V`: the middle point lies on L, and reflecting O alone does
preserve the two edges and identify O with V. Four corrupted certificates are
rejected. Normal and optimized replay agree. Hashes and timings are in
[VALIDATION.json](VALIDATION.json).

The [compact certificate](certificate.json) contains just the path, its
coordinate rows, signed distance differences and parent hash. There is no SAT
search, floating comparison, external service or omitted large artifact in
verification. Trust is in Python exact arithmetic, radical independence, and
the elementary reflection/collision argument. This is author verification,
not independent review of I450. The parent's published inequality proof
motivates the attempted construction; it is not a premise of the fold
impossibility proved here.

## Campaign consequence

This changes R2's transfer method from attaching palette sources to seeking
an edge-preserving geometric quotient of an established relation. The exact
compatibility gate fails before any full colouring search. Retire this
specific quotient; no nearby fold variant is started. The opposed-palette
coupler, its F29/circle drivers, and R1's banked eleven-point source remain
dormant. R3's Snail--Moser work and R4's fresh source synthesis are separate.

The [Parts primary paper](https://arxiv.org/abs/2010.12665), refreshed on
2026-09-14, still supplies the 509-vertex / 2442-edge record comparison.
This small path certificate is construction-selection evidence only. It does
not claim that I450 has no other plane realization, that every quotient
transfer fails, or that a sub-509 construction is impossible.
