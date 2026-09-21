# A denominator-five PIP from local character cancellation

All polygons use the standard lattice `Z^2`.  Facet normals are ordered
counterclockwise and inequalities point outward.

## 1. Statement

For an integer `t>=1`, define

```text
a_1=( 1, 1),  a_2=(-1, 4),  a_3=(-1, 1),  a_4=(-4,-1),
a_5=(-1,-1),  a_6=( 1,-4),  a_7=( 1,-1),  a_8=( 4, 1)
```

and

```text
b(t)=(11t, 29t+1, 11t+1, 29t+1,
      11t+1, 29t+3, 11t+3, 29t).
```

Indices below are cyclic modulo eight, and

```text
P_t={x in R^2:a_i x<=b_i(t) for 1<=i<=8}.
```

**Theorem 1.**  For every integer `t>=1`, `P_t` is a convex rational
octagon of denominator five.  Every edge line meets `Z^2`; its four
integral vertices alternate with four nonintegral vertices.  At the latter,
the active images have index five and their normalized character profiles
are

```text
(1,1), (3,3), (4,4), (2,2).                            (1)
```

The Ehrhart quasipolynomial collapses completely:

```text
L_(P_t)(n)
 = ((364t^2+50t-5)n^2+(20t-1)n+2)/2                  (2)
```

for every nonnegative integer `n`.

This is a geometric realization of the full diagonal-profile cancellation
at `p=5`.  It is not a new assertion that period-one rational polygons of
denominator five exist; substantially more general existence constructions
are classical.

## 2. The normal fan and vertices

The consecutive determinants are

```text
det(a_i,a_(i+1)) = 5,3,5,3,5,3,5,3.                  (3)
```

They are positive, so the normals are cyclic.  The intersection `v_i` of
facets `i` and `i+1` is

```text
v_1=( 3t-1/5,   8t+1/5),
v_2=(-5t-1,     6t),
v_3=(-8t-2/5,   3t+3/5),
v_4=(-6t,      -5t-1),
v_5=(-3t-1/5,  -8t-4/5),
v_6=( 5t+3,    -6t),
v_7=( 8t+3/5,  -3t-12/5),
v_8=( 6t,       5t).                                  (4)
```

The normalized length of facet `i`, measured in its primitive direction
lattice, is respectively

```text
(15t+1)/5,  (10t+1)/5,  (15t-3)/5,  (10t+2)/5,
(15t-1)/5,  (10t+4)/5,  (15t-12)/5, (10t+3)/5.        (5)
```

These are all positive for `t>=1`.  Direct substitution of (4) shows every
nonincident inequality has strictly positive slack for `t>=1`; each slack
is affine in `t`.  For `v_1,...,v_8`, respectively, a simultaneous lower
bound for all six nonincident slacks is

```text
6(t-1)+33/5, 10(t-1)+11, 6(t-1)+36/5, 10(t-1)+12,
6(t-1)+42/5, 10(t-1)+3,  6(t-1)+9/5,  10(t-1)+13.
```

Equivalently, (5) makes the consecutive intersections traverse all eight
cyclic supporting lines in their positive primitive directions.  Thus the
eight inequalities are actual facets of the stated convex octagon.

All normals are primitive and all right sides are integral.  Hence every
edge line contains a lattice point.  Vertices `v_2,v_4,v_6,v_8` are
integral, while each remaining vertex has exact denominator five.  This
also proves that the denominator of `P_t` is exactly five.

## 3. The four local profiles

At the nonintegral vertices, (3) gives active image index five.  Moreover,

```text
a_1+a_2=( 0, 5),    a_3+a_4=(-5, 0),
a_5+a_6=( 0,-5),    a_7+a_8=( 5, 0).                  (6)
```

Thus the active image at each such vertex is annihilated modulo five by
the full-support character `epsilon=(1,1)`.  The four sums of active right
sides are

```text
b_1+b_2=40t+1,  b_3+b_4=40t+2,
b_5+b_6=40t+4,  b_7+b_8=40t+3.                        (7)
```

Normalizing `epsilon` by the inverse of (7) modulo five gives, in order,

```text
(1,1), (3,3), (4,4), (2,2),
```

which proves (1).  Since all edge affine spans meet the lattice, these four
points are precisely the minimum-codimension bad faces.  Point volume is
one, so the four weights are equal.

## 4. Exact cyclotomic cancellation

Let `p` be prime, let `zeta` be a primitive `p`th root, and put

```text
f(x)=(x^p-1)/(x-1)=product_(a=1)^(p-1)(x-zeta^a).
```

Twice logarithmically differentiating at `x=1` gives

```text
sum_(a=1)^(p-1) (1-zeta^a)^(-2)
 = (f'(1)/f(1))^2-f''(1)/f(1)
 = (p-1)(5-p)/12.                                     (8)
```

For `p=5`, this is zero.  Multiplication by any nonzero Fourier mode `h`
permutes `F_5^*`, so (8) also vanishes after every exponent `a` is replaced
by `ha`.

Apply the accepted prime-index local Fourier criterion to `P_t`.  The
degree-zero coefficient has, for each `h=1,2,3,4`, Fourier mode

```text
(1/5) sum_(a=1)^4 (1-zeta^(ha))^(-2)=0.                (9)
```

Therefore it is constant.  The degree-one coefficient is already constant
because every edge affine span meets the lattice, and the area coefficient
is always constant.  Hence the entire Ehrhart quasipolynomial has period
one.  This realizes the review's algebraic cancellation inside an actual
normal fan rather than merely among abstract profiles.

## 5. The Ehrhart polynomial

The shoelace formula applied to (4) gives

```text
area(P_t)=(364t^2+50t-5)/2.                            (10)
```

Summing (5) gives normalized lattice perimeter

```text
per_Z(P_t)=20t-1.                                      (11)
```

For an integral-affine facet line, the local transverse half-line has
Berline--Vergne value `1/2`; thus the constant linear Ehrhart coefficient
is half of (11).  The now-constant degree-zero coefficient equals one by
evaluation at `n=0`.  Combining these facts with (10) proves (2).

The numerator in (2) is always even: both coefficients displayed before
`n^2` and `n` are odd, while `n^2+n` is even.  Thus the formula is visibly
integer-valued.

## 6. Why a four-facet realization fails

There is no convex quadrilateral in which all four consecutive active
images have index five and all four active characters are diagonal.  This
does not prove that the octagon has the minimum number of facets; it only
rules out the naive all-bad quadrilateral.

Indeed, let its cyclic integral normals be `r_1,...,r_4`.  Diagonal
characters force

```text
r_(i+1)=-r_i mod 5,
```

and cyclic orientation plus index five gives
`det(r_i,r_(i+1))=5`.  The normals must be primitive: otherwise their
contents would force a determinant divisible by 25.  A unimodular change
of coordinates and a shear fixing the first normal reduce

```text
r_1=(1,0),        r_2=(-1,5).
```

Write

```text
r_3=(1+5u, -10-25u),     r_4=(-1+5w,-5),
```

as forced by the congruences and the determinants adjacent to `r_2` and
`r_1`.  The remaining determinant condition would require

```text
det(r_3,r_4)/5=-3-10u+10w+25uw=1.
```

The left side is `2 mod 5`, a contradiction.  The integral vertices
between the bad ones in `P_t` are therefore genuine geometric separators,
not decorative subdivisions of an all-bad four-facet fan.
