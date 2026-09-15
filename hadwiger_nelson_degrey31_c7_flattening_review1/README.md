# Independent review of the de Grey D31 C7 planar-flattening gate

## Verdict

**ACCEPT, at the exact equivariant-map scope.**  At source commit
`7579d460086596290d3fcf061869d3a4f44aa001`, the submitted theorem is correct:
the fixed abstract/spatial 31-vertex de Grey graph has no plane unit-edge map
equivariant for its displayed order-seven automorphism and an action of
`C7` by Euclidean isometries.

This is not a plane realization, not a theorem about arbitrary plane maps of
D31, not a classification of non-equivariant deformations, and not a
five-chromatic plane unit-distance construction.  It gives no improvement on
the 509-vertex record.

Reviewed package:
<https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_degrey31_c7_flattening_obstruction>

Independent evidence:
<https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_degrey31_c7_flattening_review1>

## Independent mathematical check

Let `sigma` advance each of the four seven-vertex orbits `A,B,D,E` by one
index and fix vertices `C,F,G` (source labels 15, 30, 31).  The literal source
edge list independently confirms that `sigma` is an automorphism.  Suppose a
plane edge map `p` satisfies `p(sigma(v))=T(p(v))` for an isometry with
`T^7=1`.

If `T` is the identity, the adjacent vertices in the `A` cycle collapse.  A
nonidentity finite-order plane isometry of odd order is a rotation.  Write its
angle as `alpha=2*pi*m/7`, its centre as `O`, and

```text
p(A_j)=r exp(i(theta+j alpha)),
p(B_j)=  exp(i(phi  +j alpha)).
```

The fixed vertex `C` maps to `O`, so the edges `B_j C` give the displayed
unit radius.  The two offset edges from `A_j` to `B_(j-1),B_(j+1)` imply

```text
cos(theta-phi+alpha)=cos(theta-phi-alpha)=r/2.
```

Here `sin(alpha)` and `r` are nonzero, hence `sin(theta-phi)=0` and
`r^2=4 cos^2(alpha)`.  The unit chords `A_j A_(j+1)` instead give
`r^2=1/(4 sin^2(alpha/2))`.  For `x=2 cos(alpha)`, both conditions force

```text
f(x)=x^3-2x^2+1=0.
```

Dividing `1+z+...+z^6=0` by `z^3`, with `x=z+z^-1`, gives

```text
g(x)=x^3+x^2-2x-1=0.
```

The independent checker avoids a polynomial-GCD implementation by verifying
the explicit Bezout certificate

```text
(1-3x-2x^2) f(x) + (-3x+2x^2) g(x) = 1.
```

Thus the equations have no common root.  Only the 15 vertices `A union B
union {C}` and their 28 source edges are needed.  This sharpens the carrier
description, but it does not broaden the equivariance hypothesis.

## Source and chromatic audits

The 35,685,277-byte MathWorld notebook was downloaded afresh and matched
SHA-256
`3fc1c341c7a35f26e083929f54c9997fa88773a6de32d6700abbae2389c9d553`.
The submitted source audit parses a labelled `SparseArray`; the independent
audit instead scans separate literal `Graph` pair-list renderings.  It finds
90 literal 31-vertex, 98-edge blocks, of which 89 reproduce the D31 edge hash
`9691aadee6776f4e65e3dc2f3a5ff586b6d86b94c25bfc67e4dfaf819602b671`.
It also checks the notebook construction markers for two D31 copies sharing
vertex 31, with the copies of vertex 30 joined.

A full domain-propagation enumeration, rather than three separate inequality
tests, finds:

```text
canonical 3-colourings                         0
canonical 4-colourings                 1,668,352
labelled 4-colourings                  40,040,448
axis pattern (15,30,31) in every case         000
```

The canonical search introduces colour names in restricted-growth order and
visits 2,866,085 nodes.  Consequently D31 is exactly four-chromatic and all
three ports are equal in every four-colouring.  The independently rebuilt
61-vertex graph has 197 edges, is triangle-free, is non-four-colourable by the
shared-port/bridge argument, and has a checked five-colouring.  Deleting the
single bridge restores a four-colouring, providing a positive boundary
control.

These are abstract chromatic facts about a graph that has a published spatial
unit-distance embedding.  This review does not independently certify the
notebook's very large algebraic `Root` coordinate expressions; neither the
accepted planar obstruction nor the chromatic certificate depends on those
coordinates.

## Reproduction

Python 3.11 or later and the standard library suffice.

```bash
python3 -B independent_check.py > result.new.json
cmp result.new.json EXPECTED.json

python3 -B controls.py > controls.new.json
cmp controls.new.json CONTROLS_EXPECTED.json

curl -fL -o deGreyGraphs.nb \
  https://mathworld.wolfram.com/notebooks/GraphTheory/deGreyGraphs.nb
python3 -B source_audit.py deGreyGraphs.nb > source.new.json
cmp source.new.json SOURCE_AUDIT_EXPECTED.json

sha256sum -c SHA256SUMS
```

Normal and optimized (`python3 -O`) runs agree.  The respective expected
output hashes are
`b65a1a5ccb2b07b42416a664f634181b324ad4d03e17797364a63803396e672a`,
`8ae9d197908a6d51019446208fa2ba08c20a3eafa152f4eba72a98d9cf0999df`,
and `8d9685d3863d27b2052fd5fe0d36666f4fc82b21d1dc7d203c7b6f993edc1e24`.

## Campaign scope

The current published minimum remains Parts's 509-vertex plane unit-distance
graph.  D31 and its 61-vertex spindle live in three-dimensional space; their
small orders do not compete with that plane record.  The reusable conclusion
here is only that the most direct symmetry-preserving flattening fails.  A
future planar attempt must break this `C7` action or use a different carrier.
