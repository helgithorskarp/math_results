# The sharp determinant threshold for simple Ehrhart period collapse

For a bounded full-dimensional rational polytope `P` in `R^d`, write
`D(P)` for the least positive integer making `D(P)P` a lattice polytope,
and `per(P)` for the minimum quasiperiod of
`L_P(n)=|nP intersect Z^d|`. A fixed integral facet description is
`P={x:Ax<=b}`, with one inequality per actual facet and `A,b` integral.
Define

    Delta(A)=max_J |det A_J|,       |J|=d.

Only full-size minors are bounded. Rows need not be primitive in the
obstruction theorem; they are primitive in our example. The description
and ambient lattice are part of the hypotheses. A simple polytope has
exactly `d` facets through each vertex.

## 1. Results and dependencies

**Theorem 1 (sharp boundary).**

1. Every simple polytope with an integral description and `Delta(A)<=2`
   satisfies `per(P)=D(P)`. This is the previously proved and reviewed
   simple-bimodular theorem, credited in [SOURCES.md](SOURCES.md).
2. Every polytope of dimension one or two with an integral description
   and `Delta(A)<=3` satisfies `per(P)=D(P)`.
3. The twelve inequalities in Section 2 define a simple three-polytope
   with `Delta(A)=3`, `D(P)=3`, and

       L_P(n)=71 n^3+35 n^2+7 n+1       for all integers n>=0.

Thus three is the first determinant bound allowing period collapse for
simple polytopes, and dimension three is the first dimension allowing it
at that bound. This makes no claim about the minimum number of vertices
or facets.

The construction is part of a structural family.

**Theorem 2 (opposite-cone realization).** For every odd integer `q>=3`
there is a simple rational three-polytope `P_q` with twelve facets and
twenty vertices, exactly two of which are nonintegral, such that
`D(P_q)=q` and `per(P_q)=1`. Every edge has an integral endpoint. The two
nonintegral active images have cyclic index `q`; in common character
coordinates their two profiles are `+(1,1,-2)` and `-(1,1,-2)`, and they
cancel in every nontrivial character.

For prime `q` these are the normalized profiles of the previously reviewed
prime-index theorem. The argument below also covers composite odd `q`.
The global bound `Delta(A)<=q` is **not** asserted for this family. Only
the specialization `q=3` supplies Theorem 1(3).

Existence of period-one rational polytopes of arbitrary denominator was
already proved by McAllister--Woods. The contribution here is the sharp
simple determinant threshold and the specified pair of geometrically
compatible local cones. The analytic machinery, the prime-index formula,
and arbitrary-denominator existence are prior work. These proofs are
unformalized and this contribution has not received independent review.

## 2. The determinant-three witness and its finite certificate

Take `P={x:Ax<=b}` with rows of `[A|b]` as follows:

```text
 -1   0   0 | -1
  1   0   0 |  7
  0  -1   0 |  0
  0   1   0 |  6
 -2  -2  -3 |  0
  2   2   3 |  6
  1   1   2 |  3
 -1   0  -1 |  3
  1   2   2 |  7
  0  -1  -1 |  4
  2   1   2 |  8
  0   0  -1 |  8
```

The first six inequalities bound three independent coordinates, so `P`
is bounded. Exhausting the `binom(12,3)=220` active triples with Cramer's
rule gives twenty vertices, each in exactly three facets, and twelve
actual facets. Eighteen vertices are integral; the other two are

    (1,0,-2/3),          (7,6,-20/3).

They share no facet and have active determinants of absolute value three.
The histogram of absolute determinants over **all** triples, including
infeasible ones, is

| Absolute determinant | 0 | 1 | 2 | 3 |
| --- | ---: | ---: | ---: | ---: |
| Number of triples | 49 | 99 | 63 | 9 |

This verifies `Delta(A)=3` and `D(P)=3`. Full dimensionality, the thirty
edges, primitiveness of every normal, and nonredundancy of each facet are
also checked exactly by [verify.py](verify.py). Section 3 independently
proves the geometry through a cube truncation.

There is a finite exact proof of the displayed Ehrhart polynomial which
does not import the local Fourier theorem. By the standard rational
Ehrhart theorem, each of the three residue constituents modulo three has
degree at most three. Direct lattice counts give:

```text
n= 0,...,11:
1, 114, 723, 2254, 5133, 9786, 16639, 26118,
38649, 54658, 74571, 98814.
```

These agree with `71n^3+35n^2+7n+1`. There are four distinct arguments
in each residue class, so equality of cubics proves the identity for
every `n>=0`. Values at `12,13,14` are unused checks. The direct counter
loops over the first two integral coordinates, obtains exact lower and
upper bounds for the third from every halfspace, and sums the lengths of
the resulting integral intervals. A second counter uses a congruence
filter on a cube and removes six disjoint open corner caps. Literal
three-coordinate enumeration also checks `n=0,1,2,3`.

The computer-assisted proof has an explicit small trust boundary: the
listed halfspaces, exact integer/rational arithmetic, exhaustive active
triples, completeness of the interval count, and the standard Ehrhart
degree and denominator theorem. It is not inference from an unbounded
sequence of numerical examples.

## 3. The uniform geometric construction

Fix odd `q>=3`, and set

    c=(1,1,-2),       a=(1,0,0),       L=2q,
    Lambda={u in Z^3:c.u=0 mod q}.

We first use `Lambda` as the lattice in `u`-space. A basis identifying it
with standard `Z^3` is

              [1  0  0]
    D_q =     [0  1  0],       r=(q+1)/2,       u=D_q x.
              [r  r  q]

Indeed `det D_q=q` and `c D_q=-q(1,1,2)`. The image is contained in
`Lambda`, and both have index `q` in `Z^3`, so the image equals `Lambda`.

Start with the cube `C=a+[0,L]^3`. Retain its all-lower and all-upper
vertices. For each other corner

    v=a+L epsilon,       epsilon in {0,1}^3\{000,111},
    sigma_i=1-2 epsilon_i,

let `t_i` be the unique integer in `{1,...,q-1}` satisfying

    sigma_i c_i t_i=-1 mod q.                              (1)

Every `c_i` is a unit modulo odd `q`. Since `c.v=1 mod q`, the first
point of `Lambda` along the `i`th inward edge is exactly
`v+sigma_i t_i e_i`. Retain the halfspace

    sum_i sigma_i (u_i-v_i)/t_i >= 1.                     (2)

Its new facet is the triangle through those three lattice points. Define
`Q_q` to be the cube intersected with these six halfspaces and put
`P_q=D_q^{-1}Q_q`.

**All cuts and faces are accounted for.** A removed cap, including its
closure, is within `q-1` of its corner in each coordinate: in inward
coordinates its defining conditions are `d_i>=0` and `sum_i d_i/t_i<=1`.
Closures associated with distinct corners are disjoint, because in a
coordinate where their bits differ the corners are `2q` apart. Thus each
cut removes exactly its own corner and makes three new vertices on its
incident edges. It meets no other cut. Every old edge keeps positive
length, since the two possible truncation distances sum to at most
`2q-2`; all six old facets retain a two-dimensional relative interior.

Truncating six vertices of a simple cube in this manner gives exactly
`8-6+6*3=20` vertices, `12` facets, and `30` edges. Each new vertex lies
on two old facets and its unique new facet, with independent normals;
the two retained corners each lie on three old facets. Hence the polytope
is simple. These observations also prove that there are no hidden
intersections, extra vertices, or redundant listed facets.

The eighteen new vertices belong to `Lambda`. The retained vertices are
`a` and `a+2q(1,1,1)`, which in standard coordinates are

    (1,0,-r/q),          (1+2q,2q,-2q-r/q).                (3)

Since `gcd(r,q)=1`, both have exact denominator `q`. The active matrices
there are `-D_q` and `D_q`, up to row ordering, and have determinant
absolute value `q`. No edge joins these opposite corners. Therefore
every edge has a lattice endpoint, and every positive-dimensional face
contains a lattice point; in particular its affine span meets the lattice.

All facet equations have primitive integral normals and integral supports
in `x`-coordinates. For old facets this follows from the rows of `D_q`,
whose contents are one. A new facet contains three affinely independent
points of `Z^3`, so its primitive integral normal has integral value on
that facet. The construction program obtains the normals by clearing
the denominators in (2), multiplying by `D_q`, and dividing the normal
and support by the normal's content. At `q=3` this is precisely Section 2.

## 4. Why the two nonintegral cones cancel

We spell out the composite-modulus bridge rather than silently applying
a prime-only theorem. Fix one rational positive-definite scalar product
and the induced quotient lattices throughout the Berline--Vergne local
Euler--Maclaurin construction. Its cone identity, lattice-translation
invariance, and local Ehrhart formula are Theorems 19(d), 20(a,e), and
Corollary 30 of the cited 41-page version.

For a rational polytope the formula is

    L_P(n)=sum_F mu(t(nP,nF))(0) vol(F) n^dim(F),           (4)

with volume normalized by the direction lattice. A face whose affine span
contains a lattice point has a constant local coefficient as `n` varies.
Thus all positive-degree coefficients of `P_q` are constant, as are the
local terms of its eighteen integral vertices. Only the two vertices (3)
can cause period dependence.

Here is a direct calculation of their nonconstant modes, in `u`-space
with lattice `Lambda`. Put `zeta=exp(2 pi i/q)`. At the lower vertex the
cone of the dilated polytope is `na+R_{>=0}^3`. After removing its vertex
exponential, its lattice exponential sum is

    (1/q) sum_(h=0)^(q-1) zeta^(hn)
                    product_i (1-zeta^(h c_i) exp(xi_i))^(-1).       (5)

Indeed an integer point is `na+w`, where `w_i>=0` and `c.w=-n mod q`;
the finite character filter gives (5). At the upper vertex
`v=a+L(1,1,1)` the cone is `nv-R_{>=0}^3`. Since `c.v=1`, its normalized
sum, after changing the sign of the character index, is

    (1/q) sum_(h=0)^(q-1) zeta^(hn)
                    product_i (1-zeta^(-h c_i) exp(-xi_i))^(-1).    (6)

Every nonzero-character summand is analytic at `xi=0`. This includes
nonprimitive roots when `q` is composite: `c_i` is a unit modulo `q`, so
`zeta^(h c_i)!=1` for all `h=1,...,q-1`.

To pass from (5)--(6) to `mu`, consider any positive-dimensional face
of one of these orthants. It fixes a proper subset `I` of the coordinates.
Projection of `Lambda` onto those coordinates is surjective: choose
an omitted coordinate and solve the single congruence using its unit
coefficient. There is therefore `z in Lambda` agreeing with the relevant
vertex on `I`. The vertex minus `z` belongs to the direction of that
cone face. In the quotient by that direction, dilating the vertex is
an integer lattice translation, so the transverse `mu` function is
independent of `n`. After removing the vertex exponential, the face
integral is independent of `n` too.

Consequently all positive-dimensional terms in the local cone identity
have only the zero character. In a nonzero character, the normalized
lattice sum equals just the vertex `mu` term. Its coefficients, for the
phase `zeta^(hn)`, are respectively

    (1/q) product_i (1-zeta^(h c_i))^(-1),
    (1/q) product_i (1-zeta^(-h c_i))^(-1).                (7)

For any nontrivial `q`th root `z` the denominators below are nonzero, and

    product_(c_i=1,1,-2) (1-z^(-c_i))^(-1)
       =(-1)^3 z^(1+1-2) product_i (1-z^(c_i))^(-1)
       =-product_i (1-z^(c_i))^(-1).                     (8)

Thus the two quantities in (7) cancel for every nonzero character. Formula
(4) now has no periodic coefficient. All coefficients are constant and
`per(P_q)=1`. The usual Ehrhart constituent identity extends the polynomial
to `n=0`, where its value is one. This proves Theorem 2.

For comparison with the prime-index convention, the lower active matrix
is `-D_q` with support `-a`, and the upper matrix is `D_q` with support
`v`. The annihilator can be taken to be `c` in both cases, and its values
on the supports are `-1` and `1`. Normalization therefore gives `-c`
and `c`. At `q=3` these are `(2,2,2)` and `(1,1,1)`, precisely the
previously unrealized third-root pair. The determinant bound is supplied
by the full enumeration in Section 2, not by the two active determinants.

## 5. Explicit Ehrhart polynomial for the uniform family

This calculation gives a symbolic check on the construction. Put

    s=(q-1)/2,       epsilon=gcd(s+1,2),
    V=(95q^2-q)/12,
    B=(s^2+45s+22+epsilon)/2,
    N=8q^2+12q+6-2 floor(s/2),
    C=N-1-V-B.

Then

    L_(P_q)(n)=V n^3+B n^2+C n+1.                        (9)

To verify every coefficient, the six step triples from (1) are:

| Corner bits | Steps `(t_1,t_2,t_3)` | New facet's normalized area |
| --- | --- | ---: |
| 001 | `(2s,2s,s)` | `s^2` |
| 010 | `(2s,1,s+1)` | `epsilon/2` |
| 011 | `(2s,1,s)` | `s/2` |
| 100 | `(1,2s,s+1)` | `epsilon/2` |
| 101 | `(1,2s,s)` | `s/2` |
| 110 | `(1,1,s+1)` | `1/2` |

Normalized three-volume in `u`-space is ordinary volume divided by `q`.
The cube has volume `8q^2`. The sum of the six products `t_1 t_2 t_3`
is `q^2(q+1)/2`, so the removed volume is `q(q+1)/12`, giving `V`.

Every facet has an integral affine span. The coefficient of `n^2` is
therefore half the total normalized facet area. In an old coordinate
plane, its direction sublattice has index `q`, since either remaining
coefficient of `c` is a unit. The cube's total normalized facet area is
`24q`. The triangles removed from its old facets have combined area

    (1/(2q)) sum_cuts (t_1 t_2+t_1 t_3+t_2 t_3)
       =(1/(2q)) (2s+1)(8s+5)=4s+5/2.

For a triangle in `Z^3`, normalized area is half the gcd of the three
coordinates of the cross product of two edge vectors. In `x`-coordinates
these cross products, up to signs or interchange of the first two
coordinates, are

    001: (2s^2,2s^2,4s^2),       110: (0,0,1),
    010: (-(s+1),0,-2s),         011: (-s,-2s,-2s).

This proves the last column of the table. Its sum is
`s^2+s+epsilon+1/2`. The remaining total boundary area is consequently
`s^2+45s+22+epsilon`, giving `B`.

It remains to count `P_q` itself. Character filtering the cube gives
`((2q+1)^3-1)/q=8q^2+12q+6` lattice points. A removed point in a cap has
integer inward coordinates `d_i>=0`, with

    sum_i d_i/t_i<1,        1+sum_i c_i sigma_i d_i=0 mod q.

At 001, the congruence expression `d_1+d_2+2d_3` is strictly below
`2s=q-1`, so it cannot equal `-1 mod q`. The same argument, with the
coordinate having step one forced to zero, covers 011 and 101. At 110,
`d_1=d_2=0` and `d_3<=s`; the congruence would require `d_3=s+1`, so
there is no point. At 010, `d_2=0` and the bounds force
`d_1-2d_3=-1` as an integer equality. Substitution in the strict cap
inequality gives `1<=d_3<(s+1)/2`, exactly `floor(s/2)` points. The
100 cap has the same count. This gives `N`. Polynomiality from Section 4,
the value at zero, and the first two coefficients determine `C` as in (9).
At `q=3`, the coefficients are `V=71,B=35,C=7`.

## 6. No collapse below dimension three at determinant bound three

We use the previously reviewed prime-index local Fourier theorem, whose
precise hypotheses and proof are linked in [SOURCES.md](SOURCES.md).
If `pR` is lattice for prime `p`, let `g` be the minimum codimension of
a face whose affine span misses the lattice. Suppose each such minimal
face `F` lies in exactly `g` facets and

    [Z^g:A_F Z^d]=p.

The normalized annihilator profile `eta_F` has all coordinates nonzero
in `F_p`. Writing `k=d-g`, the Fourier coefficient of the first possibly
nonconstant Ehrhart coefficient is

    qhat_k(h)=(1/p) sum_F vol_k(F)
                       product_(j=1)^g (1-zeta^(h eta_(F,j)))^(-1),  (10)

where `qhat(h)=(1/p)sum_(r mod p)q(r)zeta^(hr)`. A nonzero value proves
`per(R)=p`. Full support follows because a proper support would define
a bad face of smaller codimension. Formula (10) is a dependency, not
a theorem first claimed here.

Now let `P` have dimension `d<=2` and `Delta(A)<=3`. Remove redundant
inequalities if present. Such a polytope is simple. By Cramer's rule,
each vertex denominator is one, two, or three, so `D=D(P)` divides six.
Fix a prime `p|D`, and set `R=(D/p)P`. This has exact denominator `p`
and the integral facet description `Ax<=(D/p)b` with the same `A`.

For any `g` independent active rows `A_F`, extend them to a nonsingular
square row submatrix `T` of `A`. Projection on the active coordinates
induces a surjection

    Z^d/T Z^d --> Z^g/A_F Z^d.

Thus the active-image index divides `|det T|` and is one, two, or three.
At a bad face of `R`, its support class in this finite quotient is nonzero
but is killed by `p`: choose any vertex of that face and use `pR` lattice.
The class has order `p`, forcing the index to be exactly `p`. In particular
all minimum-codimension bad faces satisfy the hypotheses of (10).

Here `g<=2`. For `p=2`, the product in (10) is the positive real number
`2^(-g)`. For `p=3`, each factor has real part `1/2`, and

    Re[(1-zeta^a)^(-1)] = 1/2,
    Re[(1-zeta^a)^(-1)(1-zeta^b)^(-1)]
        = 1/6 if a=b, and 1/3 if a!=b,

for `a,b in {1,2}`. Multiplication by a nonzero `h` preserves this list.
Every face volume in (10) is positive, so the real part of its sum is
strictly positive. Hence `per(R)=p`.

Finally the minimum quasiperiod `r` of `P` divides `D`. If it omitted
the prime `p`, squarefreeness of `D` would give `r|D/p`. Then
`L_R(n)=L_P((D/p)n)` would be a polynomial, contrary to `per(R)=p`.
Every prime dividing `D` must therefore divide `r`, giving `r=D`.
This proves Theorem 1(2). Together with the prior bimodular theorem and
Section 2 it proves the claimed sharp boundary.

## 7. Evidence and limitations

The fixed determinant-three witness has both an exact finite all-dilation
certificate and the structural proof above. The universal construction
and the low-dimensional obstruction are proved by the mathematical
arguments; the finitely many additional moduli in `verify.py` are checks
on them, not a proof by extrapolation. All arithmetic in that program is
integral or rational; no floating-point solver is used. Its alternate
counting representation and small literal enumeration provide algorithmic
cross-checks, not independent peer review.

There is no claim that every odd-denominator collapse has two cancelling
cones, that these vertex/facet counts are optimal, or that arbitrary
integral descriptions have the same determinant bound. Even moduli are
outside this construction because the coefficient `-2` ceases to be a
unit. The global determinant bound for general `q` can be much larger
than `q`; the exact checker records this explicitly. Literature novelty
is bounded by the primary-source comparison in SOURCES.md.
