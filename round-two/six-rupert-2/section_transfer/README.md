# J74 half-difference sections and all-source receiving caps of radius 1/270

**six-rupert-2, researcher; 2026-10-01.** A scoped exact construction and
written geometric proof for the original unit-edge Johnson solid **J74**,
the metabigyrate rhombicosidodecahedron. Its full Rupert status remains
open. This extension is author-checked and unformalized; independent
review and historical priority are not asserted.

Let `S=(K-K)/2`, `A(n)=Area(P_nK)`, `A_D(n)=Area(P_nS)` and
`a0=(13+7sqrt(5))/2`. [PROOF.md](PROOF.md) establishes:

- At all six original minimum axes, the entire shadow `P_mS` equals
  the actual central section `S intersect m-perp`. Its 94 corners have
  compact witnesses: 50 direct half-differences and 44 opposite-height
  midpoints of original half-differences.
- Globally, `A_D` has minimum `a0` exactly at `+/-e_y`. For
  `0<eta<=1/25`, `A_D(n)<=a0+eta` puts `n` within chord `<eta/3` of
  those axes. The original-area version localizes to all six original
  minimum axes with the same budget and bound.
- Every original closed fit of scale at least one with receiver in
  the common-shadow cone and `A(n)<=a0+1/25` forces every source into
  that cone. Proper J74/RID placement existence is equivalent at fixed
  scale and physical translation. The same conclusion applies to the
  global receiving condition `A_D(n)<=a0+1/25`.
- The transfer includes closed y-normal caps of chord **8/875**.
  The committed RID input then excludes every strict J74 passage of
  scale at least one on the closed caps of chord **1/270**, for arbitrary
  source orientation, full roll and translation. Every strict J74 passage
  also satisfies **globally** `A_D(n)>a0+1/90`; the original-area version
  is proved only in the common-shadow cone.

Chords are between unit normals. `8/875` is a transfer radius and
`1/270` is an exclusion radius for **strict** containment; touching closed
fits are allowed. The exact central sections give the global lower
bound `A_D(k)>=A_D(m)|k dot m|`, which avoids a linear continuity loss.
The transfer band is sixteen times the previous band; the exclusion
radius grows by `1000/9` from `1/30000`.

From the repository root, run separately with Python 3.11+ standard
library and one process:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  timeout 55s python3 -B round-two/six-rupert-2/section_transfer/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  timeout 55s python3 -O -B round-two/six-rupert-2/section_transfer/check.py
```

The checker hash-pins its [parent source](..) before importing anything,
regenerates the complete earlier compact geometric record, and then
checks the supplied section certificate by original-vertex membership,
planarity, convex cyclic boundaries and complete separable support
bounds. It performs 5640 original support evaluations and 1304 strict
boundary gates, and rejects four malformed certificates even under `-O`.
`--emit` optionally finds the same lifts before checking them. Exact
arithmetic is in the ordered real field `Q(sqrt(5))` using `Fraction`.

The compact [expected.json](expected.json) has 12,341 bytes, SHA256
`a4e995b18b2dd3d7190417470703335ae30f53addba8ecbd5c5adb56a615b277`.
Both production modes compare every field. Continuous theorem statements
in that record refer to the written proof, not to verification of a
string as a quantified theorem.

Final author runs on Python 3.11.2 completed in **9.148598 seconds** at
**18,244 KiB** peak RSS normally and **16.188472 seconds** at
**20,928 KiB** under `-O`. Each used one child process under its separate
55-second deadline. Timing depends on the shared host.

The explicit mathematical inputs in [DEPENDENCIES.json](DEPENDENCIES.json)
are the pinned J74 original geometry and first transfer proof, the
classical planar Brunn-Minkowski inequality, and the published
[RID complete spectrum](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md)
and [larger RID cap theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_quadratic_twofold_caps/PROOF.md).
The edge-two RID input is rescaled explicitly to unit edge. Its larger
exact checker was separately replayed locally. That input replay is not
an independent review.

Trust boundaries are the exact Python implementation, original-solid
identification, complete finite checks and the unformalized written
geometric and cited RID arguments. No floating search, solver result,
private input, large omitted corpus or numerical package is required.
The remaining concrete frontier is an original J74 passage or a support
obstruction outside the receiving restrictions proved here.
