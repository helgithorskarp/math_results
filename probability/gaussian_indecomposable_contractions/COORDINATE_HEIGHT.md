# Explicit coordinate sizes for the indecomposable reduction

Complete author proof, 27 September 2026; independent review pending.
The unrestricted Gaussian-majorisation sign remains open.

This fills the coordinate-height gap left by [EFFECTIVE_BOUND.md](EFFECTIVE_BOUND.md).
It does not change the accepted geometric construction. The new ingredient
is arithmetic control of its supporting planes and of every placement in
the resulting finite distance interval. In particular, multiplying cleared
affine matrices avoids an artificial exponential-in-the-number-of-cells
height recurrence.

## 1. Height convention and statement

A rational scalar has height at most B if, in lowest terms, its numerator
has absolute value at most `2^B` and its positive denominator is at most
`2^B`. Zero is allowed. This is a bound on binary encoding length, not on
Euclidean magnitude. All budgets below are positive integers.

Let N distinct rational source points `p_i` and rational images `q_i` obey
all pairwise contraction inequalities. Choose a rational R>0 with both
supports in B(0,R). Assume every prescribed coordinate and R has height at
most an integer B>=1. Use the earlier mesh bounds

    h = 512*2^N*(N+6) + 3N + binom(N,3) + 6,
    M = 12h [1+h+binom(h,2)+binom(h,3)].                    (1)

Define

    H0 = B+4,          Hrep = 2^(10N) H0,
    A = 64 Hrep,       Vtx = 64 A,
    J = binom(h,3),    K = J(Vtx+2),
    H = 2^15 M K.                                         (2)

**Theorem 1.** The construction in EFFECTIVE_BOUND.md has a choice of
supporting-plane representations such that every final mesh vertex has
coordinate height at most K. Every root-aligned placement preserving its
tetrahedron edge lengths has coordinate height at most H, including every
intermediate configuration in the full contraction interval. One may
translate a fixed root vertex to zero without changing the bound H.

For interval placements after this translation, all sites lie in B(0,4R).
There are at most M tetrahedra and M+3 labelled vertices, using the
[linear-height theorem](LINEAR_HEIGHT.md). The height bound satisfies

    H = O(N^7 2^(17N)(B+4)).                               (3)

The theorem bounds the numerator and denominator sizes of *all* relevant
representatives. It does not assert a practical construction algorithm,
polynomial runtime, or a favorable Gaussian sign. The integer `2^H` need
never be expanded to record the bound.

## 2. Elementary rational arithmetic

If a,b have heights at most u,v, respectively, then

    height(a*b), height(a/b) <= u+v,       b!=0,
    height(a+b), height(a-b) <= u+v+1.                     (4)

These follow by using the product denominator before reduction. Multiplying
by two adds at most one. Negation does not change height. The arithmetic
below always retains rational plane coefficients; normalizing a plane to a
unit vector would introduce unnecessary square roots and is not performed.

## 3. One repair increases the height budget by at most 1024

Represent a convex piece by affine inequalities F_l(x)>=0, and its
isometry by `S(x)=Ux+t`. Suppose all plane coefficients, U,t and all
prescribed data have height at most Z>=1. Write `a=p_i`, `b=q_i` and

    a'=U^T(b-t),       n=a'-a,
    c=|a'|^2-|a|^2,   q=|n|^2,
    H_Q(x)=2n.x-c.

Orthogonality makes the transpose the inverse linear map. If n=0 no repair
on this piece is needed. Otherwise q>0 and the bisector reflection is

    rho(x)=(I-2nn^T/q)x+(c/q)n.                            (5)

Successive applications of (4) give these deliberately coarse bounds:

| Quantity | Coordinate or coefficient height bound |
| --- | --- |
| `b-t` | `3Z` |
| `a'` | `14Z` |
| `n` | `16Z` |
| `c` | `95Z` |
| `q` | `98Z` |
| Bisector plane `H_Q` | `128Z` |
| Affine reflection (5) | `256Z` |
| Repaired isometry `S composed with rho` | `1024Z` |

For example, a sum of three products of height 4Z has height at most
12Z+2<=14Z. The squared norms in c have heights at most 86Z and 8Z,
respectively, giving 95Z after subtraction. The largest translation
coefficient in (5) has height at most 95Z+16Z+98Z=209Z. Composing its
affine map with S keeps every coefficient below 1024Z.

The side planes of a repair cone need no vertex enumeration or division.
For an old facet plane F, the plane through a and the line F=H_Q=0 is
represented by

    L_F(x)=F(a)H_Q(x)-H_Q(a)F(x).                          (6)

Every actual side facet of `conv(a,Q intersect {H_Q=0})` has this form:
its base edge lies in an old facet plane. The plane H_Q does not contain
a. Zero or redundant L_F can be discarded, and either sign may be chosen
to orient its inequality. Retained pieces use old facets and H_Q.

The values F(a) and H_Q(a) have heights at most 10Z and 640Z. Each
coefficient of (6) therefore has height at most

    (10+128)Z+(640+1)Z+1 <=780Z<1024Z.

This covers lower-dimensional or redundant sections: only actual facets
of the full-dimensional retained pieces and cones are needed. The proof
of the geometric repair, including coverage and continuity, remains the
accepted argument in EFFECTIVE_BOUND.md.

The 512-piece folded seed has coefficients among small integers and
integer multiples of R of magnitude at most 4R. Their heights are at most
B+4. After at most N repairs, every piece isometry and supporting plane
therefore has height at most Hrep in (2).

## 4. Arrangement vertices and shared barycentres

The conforming arrangement also includes the coordinate planes through
the prescribed points and the supporting planes of P. A plane through
three rational points of coordinate height Z can be represented using
their difference cross product and its dot product with one point, with
coefficient height at most 64Z. Thus A=64 Hrep bounds every arrangement
plane in (1), including the convex-hull or cube boundary.

Each arrangement vertex solves three independent plane equations. A
3-by-3 determinant with entry heights at most A has height at most
18A+5<=23A: expand its six signed triple products and apply (4).
Cramer's rule bounds each coordinate by 46A<=Vtx. Singular triples are
ignored. Every vertex of the bounded full-dimensional cells has such an
independent triple, even if many planes meet there. There are at most
J=binom(h,3) distinct arrangement vertices in total.

Each vertex used in the barycentric subdivision is the average of at most
J such vertices. Summing t rational coordinates and dividing by t costs
at most `t Vtx+(t-1)+ceil(log2 t)<=t(Vtx+2)`. Hence every subdivided
mesh vertex has height at most K. Shared faces use the same vertex average,
as in the existing construction; no separate irrational interior points
are chosen. Original prescribed vertices remain vertices.

## 5. All root-aligned interval states have bounded height

Each reference triangular face has rational vertices of height K. Its
plane has height at most 64K. For a plane n.x+c=0 of coefficient height P,
the reflection

    x -> (I-2nn^T/|n|^2)x-2cn/|n|^2

has affine coefficient heights at most 12P. Thus every source-face
reflection has affine coefficient height at most

    T=1024K.                                                (7)

Fix a root tetrahedron to its reference placement. Along a rooted facet
tree, the isometry on a child either continues the parent's isometry or
composes it with reflection in the corresponding *reference* face. This
is the finite-interval reconstruction from the earlier proof. A vertex
in any consistent placement is consequently a reference vertex acted on
by at most m-1 such reflections. Cycles can reject choices, but cannot add
new placements not represented by this construction.

A naive recurrence using (4) on every matrix product would grossly
overestimate heights. Instead represent each affine map as a 4-by-4
homogeneous matrix. Clearing its twelve variable entries with their
product denominator gives denominator at most `2^(12T)` and integer
entries of magnitude at most `2^(13T)`. The fixed last row causes no
additional denominator. For a word of r such matrices, product entries
have magnitude at most `4^(r-1) 2^(13rT)` when r>=1, and the product
denominator is at most `2^(12rT)`.

Clear the three coordinates of a reference point with a denominator at
most `2^(3K)`; the resulting homogeneous integer vector has entries at
most `2^(4K)`. Applying the matrix product shows that every image
coordinate has height at most

    13rT+4K+2r <= 2^14 M K,        0<=r<=m-1<=M-1.          (8)

The r=0 case satisfies the same bound directly. Subtracting a root vertex
of height K increases the height by at most K+1, leaving the final bound
H=2^15 M K. No word of length M is constructed in this argument.

For actual interval placements, all complete pairwise distances are at
most their reference source values. The reference domain P is either
inside B(0,R) or the cube [-R,R]^3, so its diameter is less than 4R.
After translating one fixed root vertex to zero, every interval site is
in B(0,4R). Arbitrary inconsistent or distance-expanding reflection words
are not asserted to satisfy this radius bound.

Finally h=O(N2^N), J=O(N^3 2^(3N)), Hrep=2^(10N)(B+4),
K=O(N^3 2^(13N)(B+4)) and M=O(N^4 2^(4N)), proving (3).

## 6. Meaning and limits of the new bound

The [finite-input handoff](COORDINATE_HANDOFF.md) first uses the existing
rational paired-cubature producer, then this height theorem and the linear
chain bound. The order matters: applying the construction directly to a
real cubature output gives no finite rational height parameter B.

The resulting indecomposable class has explicit coordinate numerator and
denominator bounds as well as label, weight, radius and adverse-gap bounds.
The preceding [exposed-edge theorem](../gaussian_exposed_edge_tail/PROOF.md)
therefore also gives *uniform* signed outer intervals for this complete
finite class. Only the middle sign is missing; none is supplied here.

The [exact controls](coordinate_height.py) verify the repair-plane formula,
reflection denominators, shared rational barycentres, cleared-matrix
products, and the parameter substitution on small data. They do not
construct the worst-case mesh, enumerate its states, calculate a Gaussian
integral, or establish the universal theorem independently of this proof.
The geometric construction is classical Brehm repair; the prior team mesh
theorem supplies its finite piece and tetrahedron counts. Standard rational
height inequalities and determinant bounds are not claimed as new.
