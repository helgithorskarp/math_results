# Exact proof boundary

## 1. Polynomial system

Let `E` be the 42 sorted pairs in `source_edges` and let `e=(10,21)`.
Fix `v0=(0,0)` and `v1=(1,0)`.  There are 42 free real coordinates.  For the
42 pairs in

```text
(E union {e}) minus {(0,1)}
```

write one equation `|va-vb|^2-1=0`.  Denote this square polynomial system by
`F(x)=0`.

The certificate gives a rational midpoint `m`, rational box radius `r`, and a
rational matrix `A` approximating the inverse of `J(m)`.  All norms below are
infinity norms and all computations in `verify.py` use `Fraction`.

## 2. Contraction certificate

The checker evaluates

```text
beta  = ||I-A J(m)||
eta   = beta + 16 r ||A||
delta = ||A F(m)|| + eta r.
```

It requires `beta<1`, `eta<1`, and `delta<r`.  If `x` lies in the radius-`r`
box about `m`, each coordinate difference in an edge equation changes by at
most `2r`.  Its four nonzero Jacobian entries therefore change in row-sum by
at most `16r`.  Thus the derivative of

```text
T(x) = x-A F(x)
```

has norm at most `eta` throughout the box.  The `delta<r` inequality proves
that `T` maps the box strictly into itself.  Banach's theorem supplies a
unique fixed point in the box.  Moreover `beta<1` makes `A J(m)` invertible,
so the square matrix `A` is invertible.  At the fixed point `A F(x)=0`, hence
`F(x)=0`.  This proves exact existence and local uniqueness; it does not treat
the rational midpoint as the realization.

## 3. Complete strict graph

For a rational midpoint difference `(dx,dy)`, the actual squared distance in
the box differs from `dx^2+dy^2` by at most

```text
4 r (|dx|+|dy|) + 8 r^2.
```

The checker applies this enclosure to all `23 choose 2 = 253` pairs.  Every
midpoint squared distance is bounded away from zero, proving distinctness.
For every pair outside `E union {e}`, its squared distance is bounded away
from one.  The equations prove that every pair in `E union {e}` is exactly
unit.  Consequently the isolated root has exactly 23 physical points and the
complete strict physical unit graph has exactly 43 edges, with `(10,21)` the
only contact not in the named fish source.

## 4. Chromatic and source-loss checks

The deterministic three-colour search fixes the colours of the source edge
`(0,1)` to 0 and 1, which is without loss by colour permutation.  At every
node it chooses an uncoloured vertex by saturation, degree and label, and
branches over all nonforbidden colours.  Returning false after 541 calls is a
complete finite proof that the 42-edge source is not three-colourable.

The checker directly checks every edge inequality in two full assignments:

- `01110021022330110210021` is proper on all 42 source edges and assigns equal
  colours to 10 and 21.  Since the exact physical graph adds their unit edge,
  this complete source assignment has no lift.
- `01110021022330110210012` is proper on all 43 physical edges.  It is both a
  positive four-colour witness and, trivially, a proper colouring using at
  most five colours.

The fish subgraph is contained in the physical graph, so the non-three result
also applies to the physical graph.  The positive word proves that both have
chromatic number exactly four.  The theorem is strict loss of the set of full
source assignments, not a statement about a selected terminal projection.

## 5. Trust and limitations

The exact proof boundary consists of `geometry_certificate.json`, `verify.py`
and Python's integer/rational arithmetic.  The builder and `mpmath` only
reproduce the positive certificate.  The eight negative controls are
author-side robustness tests, not independent peer review or formal proof.

No four-colour impossibility is claimed for the 43-edge graph.  In particular,
the source-loss theorem is not a Hadwiger--Nelson record construction.
