# Proof of the 5,114-class three-wheel frontier

## 1. Imported exact frontier

Write `mu6` for the sixth roots of unity and

```text
phi(x) = (1+i sqrt(3)x)/(1-i sqrt(3)x).
```

The source h4065 theorem supplies 988 pairwise coprime nonconstant event
factors in `Q[x,y]`, thirteen explicit colour words, and 71,134 selected
pairs of factors.  On an injective parameter pair outside the alignment
lines, simultaneous failure of all thirteen words implies the vanishing of
one selected pair.  A separate list of 972 normalized equations covers all
three-coordinate label collisions.  Whole lines with `u`, `v`, or `u/v` in
`mu6` are already four-colourable by h4005/h4031.

The present verifier checks the source certificate hash, reconstructs the
selected-pair cover, and replays all 487,578 modular coprimality witnesses.
Thus this proof does not silently replace the source exceptional set.

## 2. Physical symmetry group

The following transformations preserve the strict physical unit graph up to
Euclidean congruence:

```text
R(u,v) = (omega u, v),
S(u,v) = (v,u),
T(u,v) = (u^-1, v/u),
C(u,v) = (conjugate(u), conjugate(v)).
```

For `R`, use `omega W=W`; for `S`, commute the two free summands.  Multiplying
all of `S(u,v)` by `u^-1` and reordering summands gives `T`.  Reflection gives
`C`.  The first generator together with its `S`-conjugate supplies the two
independent `mu6` rotations, while `S,T` generate all summand permutations.
Reflection commutes with the quotient action.  Hence the abstract order is
at most `6^2 * 6 * 2 = 432`.

In Cayley coordinates the maps are

```text
R: ((3x+1)/(3-3x), y),
S: (y,x),
T: (-x, (y-x)/(1+3xy)),
C: (-x,-y).
```

Their inverses have denominators only on alignment lines.  Consequently they
are bijections on the nonalignment domain `U`.

There are exactly sixteen finite alignment divisors: five values each for
`x` and `y` in `{0, +/-1/3, +/-1}`, five equations

```text
(y-x) - a(1+3xy) = 0,  a in {0, +/-1/3, +/-1},
```

and `1+3xy=0`.  Removing them and the two positive Cayley denominators leaves
972 event factors.

## 3. Certified action on factors and words

The certificate contains an identity for every generator and every one of
the 972 factors.  For example, the verifier clears the inverse `R` chart by

```text
f((3x-1)/(3x+3),y) (3x+3)^deg_x(f),
```

and the inverse `T` chart by

```text
f(-x,(y-x)/(1+3xy)) (1+3xy)^deg_y(f).
```

It expands these expressions with integer polynomial arithmetic and checks
that each equals, up to a nonzero scalar, one target factor times only listed
alignment or positive-denominator factors.  Those extra factors never vanish
on `U`.  The four target lists are permutations of all 972 factors, of orders
2, 2, 6, and 2 respectively.

Exact closure gives 432 distinct factor permutations, so the abstract upper
bound in Section 2 is attained and the action is faithful on this factor set.
The 972 factors form eleven orbits, with size histogram

```text
18:2, 36:2, 108:6, 216:1.
```

For each generator the checker also maps every bad-factor set of each colour
word and verifies equality with one of the thirteen original bad-factor
sets.  Thus simultaneous failure of all thirteen words is invariant; no new
colouring assumption enters the quotient.

## 4. The 800 pair representatives

Discarding selected pairs containing an alignment divisor leaves 66,515
pairs.  They still cover every possible nonalignment common-failure point,
because no discarded factor can vanish there.  Their full group closure has
280,197 distinct pairs, partitioned into exactly 800 orbits.  The orbit-size
histogram is

```text
9:1, 18:5, 36:4, 54:1, 72:1, 108:55, 216:198, 432:535.
```

Let a possible injective non-four-colourable parameter `p` lie on a selected
pair `{f,g}`.  Move that pair to the stored representative of its group
orbit.  Applying the same physical symmetry to `p` gives an isomorphic
candidate lying on the representative pair.  Therefore every candidate
orbit occurs in the union of the 800 representative intersections.

If two factors have bidegrees `(a,b)` and `(c,d)`, their bihomogeneous
closures in `P1 x P1` have intersection number

```text
a d + b c.
```

The imported pairwise coprimality rules out a common component; exact
bihomogenization introduces no boundary divisor.  Hence the number of
distinct complex affine intersections, and therefore of real intersections,
is at most `ad+bc`.  In each pair orbit the certificate chooses a member with
minimum such cost, then minimum ordinary total-degree product, then
lexicographic order.  The 800 costs sum to **5,110**.  The ordinary planar
Bezout backup sum is 6,715.  Multiple representatives may meet at the same
point, and many complex roots may be nonreal, so 5,110 is conservative.

## 5. Collision quotient

Every nonzero difference of two wheel points has squared norm 1, 3, or 4,
and each fixed norm class is one `mu6` orbit.  Independent wheel rotations
remove the coefficient directions, summand permutations forget their order,
and reflection identifies the two orientations of a nondegenerate triangle.
Thus the 972 source collision rows reduce to the ten multisets of size three
from `{1,3,4}`.

For squared norms `(a,b,c)`, the circle-intersection discriminant is

```text
Delta = 4ab - (c-a-b)^2.
```

It is positive for nine types and zero for `(1,1,4)`.  Exact Cayley solutions
show that all roots of six types are on alignment lines:

| squared norms | Cayley solutions `(x,y)` |
|---|---|
| `(1,1,1)` | `(1,-1)`, `(-1,1)` |
| `(1,1,3)` | `(1/3,infinity)`, `(-1/3,1)` |
| `(1,1,4)` | `(0,infinity)` |
| `(1,3,4)` | `(1/3,-1)`, `(-1,1)` |
| `(3,3,3)` | `(1,-1)`, `(-1,1)` |
| `(4,4,4)` | `(1,-1)`, `(-1,1)` |

The remaining four types have one orbit apiece.  Representatives are

| squared norms | `x` | `y` |
|---|---:|---:|
| `(1,3,3)` | `(-3+sqrt(33))/6` | `(-3-sqrt(33))/6` |
| `(1,4,4)` | `sqrt(5)/3` | `-sqrt(5)/3` |
| `(3,3,4)` | `sqrt(6)/3` | `1-2sqrt(6)/3` |
| `(3,4,4)` | `(2+sqrt(13))/3` | `(2-sqrt(13))/3` |

The standard-library checker evaluates every displayed collision equation in
the relevant quadratic field and verifies that the four latter points avoid
all sixteen alignment equations.  Reflection interchanges the two triangle
orientations, after the already-generated wheel and summand symmetries.

## 6. Conclusion and scope

The injective branch has at most 5,110 physical parameter orbits and the
collision branch contributes at most four more.  Each group orbit consists
of congruent physical strict unit graphs.  Therefore at most **5,114 physical
graph isomorphism classes** in this complete architecture can remain
non-four-colourable.

No exceptional root is isolated here, and no one of the 5,114 possible
classes is asserted to be non-four-colourable.  HN2 retains strict graph
reconstruction and chromatic candidate ownership.  This theorem is not a
five-chromatic unit-distance construction and not a record improvement.
