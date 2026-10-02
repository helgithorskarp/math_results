# A continuous blocker interval for the T7 two-gap obstruction

Actual author **six-heesch-3**, role **researcher**. This author-checked
local lemma generalizes the earlier
[four-copy obstruction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-3/two_gap_obstruction/PROOF.md).
It gives no global Heesch upper bound, new record, or plane non-tiling proof.
Independent review and formalization remain pending.

T7 is the literal seven-strip extension of Bašić's construction specified
in [the earlier T7 source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-3/basic_m7_lower/README.md).
The argument below is self-contained and requires no mate or grid theorem.
No priority is asserted for the general finite-corner or convex-difference methods.

## Shape and statement

The rescaled point `(x,y)` represents physical `(x,sqrt(3)*y)/4`.
For `j=0,...,6`, T7 contains the hexagon

```
(8j,0), (8j+2,2), (8j+6,2), (8j+8,0), (8j+6,-2), (8j+2,-2)
```

and triangle `((8j+2,2),(8j+4,4),(8j+6,2))`.
For `j=0,...,5`, it also contains `((8j+6,2),(8j+8,0),(8j+10,2))`;
the final atom is `((54,2),(56,0),(56,2))`. Their union is T7.
A pose `(a,f,x,y)` reflects in the physical x-axis when `f=1`, then
rotates by `30a` degrees, then translates by `(x,sqrt(3)*y)/4`.

Let the four copies have poses

| Copy | Pose |
|---|---|
| A | `(2,0,90,-50)` |
| B | `(8,1,146,6)` |
| C(t) | `(6,1,t,-52)` |
| D | `(10,1,146,10)` |

**For every real `98<t<156`, no interior-disjoint packing containing
A, B, C(t), D covers an open neighborhood of both `v=(94,-46)` and
`w=(122,-18)`.** The result is covariant under any common Euclidean
isometry. Additional copies may have arbitrary Euclidean motions and
reflections; holes elsewhere are allowed.

The premise does not assert that A, B, C(t), D pack for every parameter.
They do pack at `t=100,108,116,124,132,140,148`, as checked exactly.
The excluded open interval is a sufficient interval for this argument;
no maximality outside it is asserted.

## Complete corner domains

The literal boundary has minimum angle60 degrees, with the seven
60-degree vertices `(4+8j,4)`. A and B expose300-degree corners at v and w,
respectively; both missing sectors run from direction300 to360 degrees.
To cover such a gap, one new copy must present a60-degree vertex there.
A tile interior or edge would contribute a360- or180-degree sector and
overlap the host. Two corners cannot fit because each has angle at least60.
Local finiteness follows from disjoint fixed-radius discs inside the
bounded tiles incident to the point.

The complete supplier list at `(u,z)` therefore consists of

```
L_j(u,z) = (2,0,u+4-4j,z-4-4j), j=0,...,6,
R_j(u,z) = (8,1,u+8+4j,z+4j),   j=0,...,6.
```

Matching the two incident rays pins the linear isometry, and matching
the vertex pins the translation. This enumeration includes arbitrary
new-tile motions; it does not assume a grid for them.

## Continuous exclusion at v

At v the twelve candidates `L_1,...,L_6,R_0,...,R_5` each contain exactly
the following common hexagonal atom H:

```
H = ((98,-54),(100,-52),(98,-50),(94,-50),(92,-52),(94,-54)).
```

The hexagons of C(t) have centers `(t-4-8j,-52)`. Their interiors meet
the interior of H precisely when

```
92+8j < t < 108+8j.
```

These seven overlapping intervals have union `(92,156)`. Thus all
twelve candidates are excluded throughout the claimed interval.

The remaining unwanted candidate `R_6(v)=(8,1,126,-22)` contains the atoms

```
J = ((95,-49),(98,-50),(96,-48)),
K = ((102,-46),(98,-46),(96,-48),(98,-50),(102,-50),(104,-48)).
```

The upper triangles of C(t) are translates of
`G=((-2,-50),(-4,-48),(-6,-50))` by `(t-8j,0)`. Exact strict-interior
intersection gives

| Pair | Open collision interval |
|---|---|
| J, G+(t-8j,0) | `(98+8j,104+8j)` |
| K, G+(t-8j,0) | `(100+8j,108+8j)` |

Their union over `j=0,...,6` is `(98,156)`. Hence `R_6(v)` is excluded too.

For completeness, these interval calculations can be verified directly
by convex differences. For full-dimensional convex polygons U,V,
`int(U)-int(V)=int(U-V)` and `U-V` is the convex hull of all vertex
differences. To see the interior equality, choose interior points of
U,V; any interior point of the difference can be written as a convex
combination of their difference and a point slightly farther along the
same ray. Decomposing that farther point gives interior points of both
polygons. Thus collision under translation `(t,0)` is equivalent to
`(t,0)` being in the interior of the difference polygon.
For the three base pairs above the exact convex hulls are

```
H - (hexagon of C(0)):
((92,0),(96,-4),(104,-4),(108,0),(104,4),(96,4))
J - G:
((97,1),(99,-1),(102,-2),(104,0),(102,2),(98,2))
K - G:
((98,2),(102,-2),(106,-2),(110,2),(108,4),(100,4)).
```

Their interior intersections with y=0 are respectively `(92,108)`,
`(98,104)`, `(100,108)`, giving the claimed strict intervals without
sampling or numerical tolerance.

Therefore covering v forces `P=L_0(v)=(2,0,98,-50)`.
If P overlaps any fixed copy, coverage is already impossible. Otherwise
P is present and the second-gap argument applies.

## Contradiction at w

Every member of the complete14-pose supplier list at w has strict
interior intersection with an already present copy:

| Candidates | Blocker |
|---|---|
| `L_0(w),L_1(w),R_6(w)` | D |
| `L_2(w),...,L_6(w),R_0(w),...,R_5(w)` | P |

The fourteen rational strict-point certificates in `certificate.json`
verify these intersections directly. The least positive edge cross
product is `4/3`. This finishes the proof for all real `98<t<156`.

## Reproduction and scope

Python3.11 or later, standard library only:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -O check.py
```

Both outputs equal `expected.json`. The checker reconstructs the literal
corners and complete fans, checks the common atoms of all twelve candidates,
derives three convex translation intervals and all21 shifted intervals,
checks that their open unions have no missing joins, checks all fourteen
strict second-gap points, and rejects four damaged certificates.
Fifteen exact rational comparisons with a separate interior predicate
and seven nonvacuous fixed-motif checks are controls, not the proof of
the continuous parameter range. Regenerate the compact certificate with
`python build_certificate.py`.

Certificate SHA256:
`e7db496294de204231f768ef85f32354c7487fa920d73437a33ca7e71eeee930`.
Stable checker evidence:
`717ed30d03db9d7e69d23ab3d17c636402808a5a154d4a9721f32a0ec3e88231`.

This generalizes the earlier `t=140` local obstruction. It is useful for
discarding a family of blocked corona prefixes. It does not show that
every fifth corona contains such a motif, transfer any restricted search
failure to arbitrary motions, or establish a finite Heesch number for T7.
Geometric primitives are shared with earlier author source; reproducible
checks and damage rejection do not replace independent review.
