# Proof of the unique-three-colour sum interface

All graphs below are finite and simple. A *uniquely three-colourable* graph
has chromatic number three and only one partition into three independent
sets, up to permutation of the colour names. Fix named colourings
`c_G:V(G)->F_3` and `c_H:V(H)->F_3`.

## 1. The two-pattern theorem

**Theorem.** If `G` and `H` are connected and uniquely three-colourable, every
proper three-colouring of their Cartesian product is, up to a global palette
permutation,

```
(x,y) |-> c_G(x)+c_H(y)  or  c_G(x)-c_H(y)  in F_3.
```

Let `F` be a proper three-colouring of `G square H`. For each `y`, restriction
to the `G`-layer is a proper three-colouring of `G`, so
`F(x,y)=pi_y(c_G(x))` for a permutation `pi_y` of `F_3`. Every permutation of
`F_3` has a unique affine form

```
pi_y(t)=a_y t+b_y,  a_y in {+1,-1}, b_y in F_3.
```

If `yy'` is an edge of `H`, the three matching pairs `(x,y),(x,y')` are
product edges. Since `c_G` is surjective, `pi_y(t)` differs from `pi_y'(t)`
for all three `t`. If `a_y` and `a_y'` differed, the two affine maps would
agree at exactly one `t`; therefore `a_y=a_y'`. Also `b_y` differs from
`b_y'`. Connectivity makes `a_y=a` constant, while `y|->b_y` is a proper
three-colouring of `H`. Unique three-colourability of `H` gives
`b_y=d c_H(y)+e` with `d` in `{+1,-1}`. Thus

```
F(x,y)=a c_G(x)+d c_H(y)+e.
```

The global palette change `t|->a(t-e)` leaves exactly the two displayed
signs. Notice that the proof does not require either factor to contain a
triangle. The executable checker asks for a triangle only as a compact way
to normalize and verify a supplied unique colouring.

## 2. Quotient-supergraph viability criterion

Let `K` be a graph and let `q:V(G)xV(H)->V(K)` be onto. Assume every Cartesian
product edge has distinct images and maps to an edge of `K`. Extra edges and
identifications of nonadjacent product labels are allowed.

Any proper three-colouring of `K` pulls back along `q` to a proper
three-colouring of `G square H`, hence to one of the two patterns above. A
pattern descends to `K` exactly when it is constant on every fibre of `q`,
and the descended word is proper exactly when it separates every edge of
`K`. Consequently:

**Interface criterion.** `K` is three-colourable if and only if at least one
of the two patterns is fibre-constant and edge-proper. If neither passes,
then `chi(K)>=4`. Because a colouring of `K` would pull back to a colouring
of either factor, `chi(K)>=3`; hence a passing pattern gives `chi(K)=3`.

A failed sign has a constant-size exact witness: either two labels in one
fibre with different pattern colours, or one `K`-edge whose endpoints have
the same pattern colour. No chromatic solver is needed for this gate.

## 3. Rotational Minkowski sums

Let `A,B` be finite sets of distinct points in the Euclidean plane, and let
their strict unit-distance graphs be connected and uniquely three-colourable.
For a complex unit `u`, put

```
S(u)={a+u b:a in A,b in B}.
```

The label map `q_u:(a,b)|->a+ub` maps every edge of the Cartesian product to
a strict unit edge. It never collapses a product edge, because such an edge
changes exactly one coordinate by a nonzero unit vector. The physical strict
unit-distance graph on `S(u)` therefore satisfies the interface criterion,
including when different nonadjacent labels coincide.

There are only finitely many rotations at which this physical graph is not
exactly the Cartesian product. Indeed, put `d=a-a'` and `e=b-b'`. A collision
of two different labels with both coordinates changed requires

```
d+u e=0,
```

which has at most one unit solution. An additional cross-layer unit edge
requires

```
|d+u e|^2=|d|^2+|e|^2+2 Re(d conjugate(e) conjugate(u))=1.
```

For nonzero `d,e` this is the intersection of the unit circle with a genuine
real line and has at most two solutions. If only one coordinate changes, the
pair is a unit edge exactly when it was already an edge of the corresponding
strict factor. Thus the union of all collision and cross-edge solutions is a
finite event set, and outside it the label map is bijective with no extra
edges. With `n=|A|` and `m=|B|`, the direct ordered-difference enumeration has
`n(n-1)m(m-1)` rows, so the number of event rotations is at most
`3n(n-1)m(m-1)`: at most two unit-edge roots and one collision root per row.
This deliberately loose bound needs no generic-position assumption.

**Rotational viability corollary.** Every non-event rotation is exactly
three-chromatic. At an event rotation, the physical sum is three-chromatic
exactly when at least one explicit sign passes the fibre-and-edge test. Any
four- or five-chromatic graph in this architecture must therefore occur at a
finite event rotation and must destroy both signs. Destroying both signs is
necessary, not sufficient, for the five-chromatic target.

This strictly generalizes the two-pattern step used for the radius-two
triangular hexagon `H+uH`: the factors may differ, no lattice is assumed, and
collisions are incorporated in the same exact interface.
