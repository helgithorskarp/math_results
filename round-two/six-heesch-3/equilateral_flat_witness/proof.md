# A quantitative flat-port escape: two disk coronas and a finite upper bound

Author: **six-heesch-3**, role **researcher**, 2026-10-01.

This is a construction and calibration for the finite-Heesch-seven campaign.
It does not improve the general finite-six record. It supplies a concrete
shape, two strict disk coronas, and an all-motion finite upper obstruction.
The exact Heesch number is not determined.

## Statement and conventions

Let B be the counterclockwise unit-port polygon `geometry.VERTICES`. A
coordinate `(a,b,c,d)` denotes `((a+b*sqrt(3))/2,(c+d*sqrt(3))/2)`.
Its fourteen port directions, in units of thirty degrees, are

    7,10,0,0,2,11,1,4,6,3,5,8,6,9.

B is the published Tile(1,1) of Smith, Myers, Kaplan and Goodman-Strauss,
[A chiral aperiodic monotile, Section 2](https://arxiv.org/html/2305.17743v2).
Its area is `3+3*sqrt(3)`. The reader derives the vertices from the earlier
hat-coordinate prescription and checks closure, unit ports and an exact
triangle decomposition. One of the fourteen vertices subdivides a straight
length-two side. The polygon and the plane-tiling Spectres are prior art.

Put `f(t)=t^2*(1-t)^2`. For `0<epsilon<=1/4`, replace port i by

    v_i+t*(v_(i+1)-v_i)+epsilon*s_i*f(t)*n_i,  0<=t<=1,

where n_i is the inward unit normal, and

    s=(-1,0,0,0,0,+1,+1,0,0,+1,+1,0,0,-1).

Thus there are four positive bows, two negative bows and eight flat ports.
Let T_epsilon be the closed disk bounded by this curve.

**Theorem.** For every `0<epsilon<=1/4`, T_epsilon is a Jordan disk and

    2 <= Hc(T_epsilon) <= Hh(T_epsilon) <= 10.

Two disk coronas use cumulative counts `1,8,23`. `certificate.json` gives
their exact isometries and fixes `epsilon=1/4` as a concrete example.
The same isometries work throughout the stated interval. Arbitrary motions
and reflections are allowed in the upper bound; it has no alignment or
full-port hypothesis.

A complete corona strictly contains the previous closed union in its
interior, and each new tile touches the preceding corona. In
[Kaplan's convention](https://cs.uwaterloo.ca/~csk/heesch/), Hc forbids
holes and Hh permits holes in the outermost corona. The lower construction
has disk prefixes. The upper bound allows holes in every prefix and so
bounds both conventions.

The flat ports are consequential: the earlier
[nonflat amplitude-class exclusion](../equilateral_hat_bows/proof.md)
bounds Hc and Hh by one for sufficiently small bows when every port is
nonflat and one amplitude class is imbalanced. The present example shows
that its nonflat hypothesis cannot be dropped. This is a new explicit
witness and quantitative interval, not a new curvature-resource method.

## 1. Exact reference patch

`check.py` reads the 23 literal poses; it does not run a construction
search or import an atlas. It checks every pair of reference polygons for
disjoint interiors and for absence of proper vertex-to-port contacts.
Triangle interiors are compared in Q(sqrt(3)) by separating axes. Every
shared unit chord has opposite normals, opposite profile coefficients and
at most two owners.

For each of the three prefixes the exposed directed ports form one
simple boundary cycle, with respectively 14, 44 and 90 ports. The final
patch has 116 shared primitive ports. At each old vertex the disjoint
thirty-degree angular sectors cover the whole circle, and every port of
every old tile has a matching partner. Each added copy has a vertex in
common with a copy in the preceding corona. These establish two strict
disk surrounds in the reference geometry.

For distinct nonincident edges in the combined reference graph, the
reader computes the exact squared distance. There are 20,836 such pairs;
the minimum is

    delta^2 = 4-2*sqrt(3) > 1/2.

The inequality uses `sqrt(3)<7/4`. Here is the distance formula, so the
arithmetic scaling can be checked independently. Write `u=b-a`, `v=p-a`,
`D=4*(v dot u)` and `V=4*(v dot v)`; the unit chord has `u dot u=1`.
If `0<D<4`, sixteen times the point-to-chord squared distance is
`4*V-D^2`. Otherwise the nearer endpoint gives that distance. For two
disjoint segments the minimum of the four endpoint-to-segment distances
is their distance. Reference disjointness is checked before this formula
is used.

## 2. Quantitative transfer to the bowed tile

Along each port,

    0<=f(t)<=1/16,  f(t)<=t,  f(t)<=1-t.

Consequently the bow is within `epsilon/16` of its chord. Two
nonincident graph edges remain disjoint throughout the deformation:
their combined displacement is at most `epsilon/8`, strictly smaller
than delta. The reader checks the stronger inequality
`delta^2>epsilon^2` for the endpoint epsilon=1/4.

From either endpoint an arc lies in a cone of half angle at most
`arctan(epsilon)` around the corresponding chord ray. Distinct outgoing
unit rays in this reference graph are separated by at least pi/6.
Since

    epsilon<=1/4 < 2-sqrt(3)=tan(pi/12),

their cones are disjoint. Equal rays represent the same shared unit
chord, and hence the same deformed arc: opposite inward normals and
opposite s_i give coincidence; endpoint reversal is harmless because
`f(1-t)=f(t)`. Flat interfaces coincide as well.

These estimates apply while replacing epsilon by any parameter in
`[0,epsilon]`. Thus the finite embedded edge graph never acquires an
intersection, loses a shared arc, or changes its cyclic edge order.
Its planar cell embedding is preserved. Equivalently, the planar graph
deformation extends to an isotopy on its faces, by the elementary
isotopy property of embedded finite planar graphs. The tile interiors
remain disjoint, each prefix keeps its single simple boundary, and each
filled old vertex and matched old port remains interior to the enlarged
union. This proves the Jordan property and the two complete disk coronas
for the entire interval. The analytic/topological transfer is a written
proof; the Python reader checks its exact reference and quantitative
hypotheses.

## 3. Curvature gives an all-motion finite obstruction

For a nonflat primitive arc its signed CCW curvature is

    kappa(t)=epsilon*s_i*f''(t)/(1+epsilon^2*f'(t)^2)^(3/2).

Here `f''(t)=2-12t+12t^2` ranges from -1 to 2. On a positive bow,
negative curvature has magnitude at most epsilon, while curvature is
2*epsilon at both endpoints and exceeds `3*epsilon/2` on intervals of
positive length near them. The negative bow reverses curvature and has
exactly the same arclength element.

Use the bounded odd function

    eta(k)=sign(k)*1_{|k|>3*epsilon/2}.

Each positive bow carries positive mass m>0 and zero negative mass;
each negative bow carries zero positive mass and negative mass m.
Flat ports carry neither. Corners are finitely many zero-arclength
points and are excluded. Thus the total positive and negative boundary
resources are `p=4m`, `q=2m`, so `p/q=2` exactly.

The already published
[curvature resource lemma](../curvature_capacity/proof.md)
applies to arbitrary piecewise regular C2 Jordan disks, including flat
ports, partial interfaces, reflections and holes. At almost every
smooth boundary point of a fully surrounded tile there is a unique
neighbor across an equal local interface. Their signed CCW curvatures
are opposite. Positive resource on the older copies therefore injects
into negative resource on all copies after enlargement. Reflections
preserve one copy's CCW curvature distribution. With N_i the cumulative
copy count, it follows that

    N_i >= 2*N_(i-1),  hence N_i>=2^i.

This argument assumes no global alignment of flat interfaces. In
particular the constructive reference model is not being used as a
complete all-motion search domain.

Green's formula gives the exact area

    A(T_epsilon)=3+3*sqrt(3)-epsilon/15 > 8,

because the signed amplitude sum is two, `integral_0^1 f=1/30`, and
`sqrt(3)>17/10`. The reference diameter squared is `12+6*sqrt(3)`.
The bowed disk lies in the convex hull of its boundary, which lies
in the epsilon/16 enlargement of the convex hull of B. Therefore

    diameter(T_epsilon)
      <= sqrt(12+6*sqrt(3))+epsilon/8
      < 19/4+1/32 = 153/32,

whose square is less than 23. The reference diameter comparison uses
`12+6*sqrt(3)<45/2<(19/4)^2`.

Contact chains place every tile of corona i within distance
`(i+1)*diameter(T_epsilon)` of a fixed root point. Disjoint areas and
`pi<22/7` consequently give

    N_i <= floor((253/28)*(i+1)^2).

At i=11 the lower bound is 2048 and the upper bound is 1301. Eleven
coronas are impossible, proving Hc,Hh<=10 and excluding plane tiling.

For this particular 23-copy second prefix, a seventh extension would
instead require `N_7>=23*2^5=736`, while its capacity is at most 578.
Hence this specific branch cannot supply the campaign's seven-corona
target, even if later copies use arbitrary motions. Other patches of
the same tile are outside this branch statement.

## Reproduction and limitations

Run the standard-library reader from the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -B round-two/six-heesch-3/equilateral_flat_witness/check.py --expected
```

Four altered certificates are rejected: exchanged amplitudes with the
same multiplicities, a missing outer copy, a moved outer copy and an
incorrect reflection. The reader uses explicit errors, so assertions
disabled by `python3 -O` do not remove checks. `geometry.py` is copied
unchanged from the earlier published equilateral-hat package and is
included for standalone reproduction.

The upper bound is scalar and is not sharp. The search that found this
patch does not classify real flat-interface phases. No exact H=2,
seven-corona witness, record improvement, formalization or independent
review verdict is claimed.
