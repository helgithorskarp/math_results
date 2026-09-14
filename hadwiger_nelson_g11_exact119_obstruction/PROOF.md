# Proof of the complete `G_11` 119-image obstruction

## 1. Source and exact fibres

Let `V=F_11^2`, let `N(x,y)=x^2+y^2`, and join `u,v` when
`N(u-v)=1`. This is the 121-vertex graph `G_11`. The pinned chromatic
certificate proves `chi(G_11)=5`.

Suppose an edge-preserving map `f:V -> R^2` has exactly 119 images. Vertices
in one fibre cannot be adjacent, because the image of a source edge must have
Euclidean length one. Let the fibre sizes be `s_1,...,s_119`. Then

```text
sum_i (s_i - 1) = 121 - 119 = 2.
```

Consequently the nonsingleton part of the partition has exactly one of the
two shapes

```text
3                         or                         2+2.       (1)
```

Collapsing each fibre gives a simple quotient graph `Q` on 119 vertices, with
an edge between classes whenever a source edge has endpoints in those
classes. The map `f` induces an injective unit-edge drawing of `Q`. Conversely,
every possible fibre partition of either shape in (1) is represented by such
a quotient.

The quotient map `G_11 -> Q` is a graph homomorphism. Hence every such quotient
has chromatic number at least five. If every fibre is monochromatic in a
proper five-colouring of the source, that colouring descends and proves
`chi(Q)=5`.

## 2. Nine complete first-pair normalizations

Choose a pair `u,v` in a nonsingleton fibre. Translation is an automorphism,
so put `u=0` and write `d=v-u`. The pair is a nonedge. Since `-1` is a
quadratic nonresidue modulo 11, `N(d)=0` implies `d=0`; and `N(d)=1` would make
the pair an edge. Thus

```text
N(d) in {2,3,...,10}.                                      (2)
```

For nonzero vectors `d,e` of the same norm, identify `F_11^2` with
`F_121=F_11[i]`, where `i^2=-1`. Multiplication by `e/d` is `F_11`-linear and
preserves the norm, since `N(e/d)=1`. It is therefore an orthogonal
transformation carrying `d` to `e`. Hence `O(2,11)` is transitive on each
shell in (2). The verifier independently enumerates all 24 orthogonal matrices
and checks each 12-vector orbit.

We may therefore identify `0` with one fixed representative `d_k` for each
`k=2,...,10`. In the resulting 120-vertex quotient:

- for shape `3`, the third class is any singleton nonadjacent to the merged
  class `{0,d_k}`; this is equivalent to being nonadjacent to both source
  vertices;
- for shape `2+2`, the second fibre is any nonedge between two singleton
  classes, neither of which is `{0,d_k}`.

These loops enumerate 864 and 56,871 normalized cases respectively. Given any
partition in (1), choose one pair from a nonsingleton fibre and apply the
translation and orthogonal normalization above. The remaining collision then
appears in exactly the applicable loop. Therefore the enumeration covers
every possible fibre partition, even though it deliberately does not quotient
out the remaining stabilizers or duplicate choices of first fibre.

## 3. Rhombus equations survive contraction

Let four distinct points `p_a,p_b,p_c,p_d` form a cyclic unit four-cycle.
The two distinct common intersections `p_b,p_d` of the equal-radius circles
centred at `p_a,p_c` are exchanged by the half-turn about the midpoint of the
centres. Therefore

```text
p_a + p_c = p_b + p_d.                                    (3)
```

This is valid whether or not either diagonal or any additional chord is an
edge. Apply (3) separately to the two Cartesian coordinate lists. Its integer
row is

```text
e_a - e_b + e_c - e_d.                                    (4)
```

Begin with the predecessor's checked 119-row basis in a 120-vertex
one-collision quotient. After the second identification, discard a row only
if two of its four cycle vertices become equal. Every other cycle remains a
simple unit four-cycle in the final quotient, so its projected row remains a
valid instance of (4). The verifier calculates the rank of these rows over
`F_2`. If their rank is below 118, it reconstructs the final quotient graph,
enumerates every simple four-cycle, and calculates the rank of the complete
row set instead.

## 4. Rank lift and contradiction

Every row (4) has coefficient sum zero. For a quotient with 119 vertices, its
real rank is therefore at most 118. Modulo two, (4) is the four-bit incidence
row on its cycle. A mod-two rank of 118 exhibits a `118 x 118` integer minor
whose determinant is odd and hence nonzero. Thus the same rows have real rank
at least 118. Their real kernel is exactly the constant vectors.

The exact enumeration gives final mod-two rank 118 in all 57,735 normalized
events. The two Cartesian coordinate vectors of any induced drawing would
both be constant, contradicting both injectivity and the presence of a unit
edge. No edge-preserving map of `G_11` has exactly 119 images.

The finite-abelian predecessor rules out 121 images, and the one-collision
predecessor rules out 120. Together with the new result, they imply that every
edge-preserving plane map of `G_11` has at most 118 distinct images. Existence
at 118 or below is not claimed.

## 5. Finite certificate and trust boundary

The published one-collision basis already gives rank 118 after projection in
56,958 cases. The other 777 final quotient graphs require complete cycle
censuses; together these contain 1,567,802 checked equations and every rank is
118. The alternate audit derives a new rank-119 basis by reverse-canonical
enumeration of all one-collision cycles. Its different basis needs 844 full
fallbacks, and again every final rank is 118.

The 12,627 normalized cases whose second contracted classes have the same
colour in the predecessor's explicit proper five-colouring inherit a proper
five-colouring; the homomorphism lower bound makes them abstractly exactly
five-chromatic. This is supplementary calibration and is not needed for the
geometric contradiction.

Trust remains in the written fibre, symmetry, rhombus and rank-lift arguments;
the pinned predecessor bytes; CPython's integer, set, JSON and SHA-256
operations; and the small checker implementations. The producer and verifier
use the published first basis, while the audit reconstructs a differently
ordered basis from the full one-collision cycle sets. This is not a
proof-assistant formalization or an independent-author review.
