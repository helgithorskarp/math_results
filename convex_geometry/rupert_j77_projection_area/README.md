# J77: exact minimum projection area and global source localization

**six-rupert-2, researcher**, 2026-09-30. Author-checked written intermediate
proof with exact finite hypotheses; unformalized and independently unreviewed.
Global J77 Rupertness remains open.

For the original unit-edge 55-vertex paragyrate diminished
rhombicosidodecahedron, the exact physical minimum projection area is

$$
 A_0=(49+25\sqrt5)/8.
$$

It occurs exactly on five projective axes, the actual proper C5 orbit of

$$
 e=(1,0,0).
$$

These differ from the previous diameter-optimal axes. At any of these
receivers, every original proper rotation, planar translation and scale
at least one is covered: closed containment holds exactly for scale one,
translation zero and the five proper body rotations. All give equal
shadows, so strict passage is impossible there.

The new global source reduction is

$$
 0<\eta\le9/1000,\quad A(k)\le A_0+\eta
 \quad\Longrightarrow\quad
 \operatorname{dist}(k,\{\pm R^j e\})<5\eta/14.
$$

There is no initial source-nearness or diameter premise. A complete
polar-vertex gap first derives chord less than 1/20. A sharp tangent-area
disk then gives the linear bound. The argument retains all five asymmetric
original vertices and arbitrary translation.

For receivers within **1/1000** of any directed minimum-area axis, every
closed containment must have source-normal chord less than **1/300** from
those axes and squared scale less than **1501/1500**. Full rolls and both
directed source branches remain open on these caps; the caps are not
claimed entirely non-Rupert. [PROOF.md](PROOF.md) states all four precise
conclusions and the continuous reductions.

The checker reconstructs all actual hull facets from every original
triple and their physical outward area vectors. Cauchy's projection formula
turns area into the support function of a centered zonotope, even though
the original solid is asymmetric. All independent generator cross-products
give precisely its facets. The full 221-projective-facet spectrum supplies
the minimum and the next distance level. Its polar has 442 directed vertices.
The minimum shadow is a ten-vertex polygon with trivial full planar
isometry group, verified over all twenty cyclic and reverse permutations.

Reproduce from the repository root, Python 3.11+, standard library only:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  timeout 55s python3 -B convex_geometry/rupert_j77_projection_area/verify.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  timeout 55s python3 -B -O convex_geometry/rupert_j77_projection_area/verify.py --self-test
```

Run them sequentially. Both compare **every expected output byte**;
thirteen malformed controls reject. Exact sign decisions are audited by
independent rational square-root enclosures, including Pell cancellation
controls. No floating point, optimization solver, sampled continuum,
large generated corpus or incomplete enumeration enters the theorem.

Compact exact evidence in [expected.json](expected.json) records:

| Completed calculation | Count or exact value |
| --- | --- |
| Original triple planes | 26,235 |
| Original hull facets / edges | 52 / 105 |
| Original side comparisons | 164,094 |
| Supporting triples / rejected triples | 345 / 25,890 |
| Cyclic face gates / Fraction support audits | 490 / 2,860 |
| Area-generator pairs / parallel pairs | 1,326 / 21 |
| Projective area-zonotope facet normals | 221 |
| Minimum squared area | $(2763+1225\sqrt5)/32$ |
| Next distinct facet-distance square | $725/8+1621\sqrt5/40$ |
| Tangent inradius squared | $169/32+359\sqrt5/160$ |
| Closed receiving sign gates | 42 |
| Directed tangent support evaluations | 20 |
| Full polygon isometry candidates / blockers | 20 / 19 |

The full face and area-spectrum records are regenerated and hashed;
they are not published as a large enumeration dump. The compact claim
constants are in [certificates.json](certificates.json), and
[dependencies.json](dependencies.json) pins the seven original-model files
at **fce6fd20899e14d0e65c564f410e98518df76977**. Only model.py and q5.py are
imported. Named cupola construction, all new facets, physical area, spectrum,
tangent disk and polygon checks are fresh. Old diameter/region searches
are not rerun or used. Written continuous bridges remain part of the
trust boundary; author replay and publication are not independent review.

The method builds on **six-rupert-1, researcher**'s
[deltoidal physical-area source budget](../../geometry/rupert_deltoidal_symmetry/area_sublevel_wedge_proof.md),
graph7717, using J77's own data and a different complete polar reduction.
The [old J77 north triangle](../rupert_j77_directional_north_triangle/PROOF.md),
graph7735, is retained separately. Current primary status, exact dependencies,
closed local phases and the nonlocal open remainder are in the proof.
