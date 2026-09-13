# Proof: the triple-phase collar

Throughout, an edge means Euclidean distance exactly one.  Put

```text
gamma = pi/3,                 d0 = 1+sqrt(3).
```

## 1. The two-circle theorem

Let the circle centres be `0` and the positive real number `d`, where
`d>d0`.  A point on the first circle is `u`, and it is convenient to write a
point on the second circle as `d-w`, where `|u|=|w|=1`.  The cross-edge
condition is

```text
|u-(d-w)|=1.
```

Equivalently there is a unit complex number `t` such that

```text
u+w+t=d.                                             (1)
```

We prove that the strict graph on the union of the two complete circles is
bipartite.  The cases `d>=3` are immediate: for `d>3` there are no cross
edges, while for `d=3` there is only the tangent cross edge.  Hence assume

```text
d0<d<3.                                              (2)
```

## 2. Active cap and six-cycle orbits

Write `u=exp(i*theta)`.  If `u` is an endpoint of a cross edge, then (1)
gives `|d-u|=|w+t|<=2`, and therefore

```text
cos(theta) >= (d^2-3)/(2*d) = cos(alpha),            (3)
```

where `0<alpha<pi/2`.  Conversely, (3) lets the vector `d-u`, of length at
most two, be written as a sum of two unit vectors.  Thus the active directions
are exactly the closed cap

```text
I=[-alpha,alpha].                                    (4)
```

On either owner circle, unit chords rotate the direction by `+/-gamma`.
Their orbits are six-cycles.  Since `d>d0` implies `alpha<gamma`, an orbit
has at most two active members; if it has two, they are adjacent.  The pairs
of adjacent active directions are parametrized exactly once by

```text
theta in J_-=[-alpha,alpha-gamma],
(theta,theta+gamma).                                 (5)
```

## 3. Cross triples and their exact label

For a solution of (1), put `p=uwt`.  Since the three numbers have unit
modulus and sum to the real number `d`,

```text
uw+ut+wt = uwt*(conj(u)+conj(w)+conj(t)) = d*p.
```

Consequently their unordered multiset is exactly the root multiset of

```text
q_p(z)=z^3-d*z^2+d*p*z-p.                            (6)
```

In particular, `p` uniquely labels a cross triple, including a triple with a
repeated member.  Conversely, for an active `u` the other two members satisfy

```text
w*t=(d-u)/(d-conj(u)),
p=P(u):=u*(d-u)/(d-conj(u)).                         (7)
```

Thus two active directions have the same label precisely when they belong to
the same unordered cross triple.

Choose the continuous real argument of (7) on (4):

```text
sigma(theta)
 = theta + 2*arg(d-exp(i*theta)).                    (8)
```

Here `d-cos(theta)>0`.  Moreover
`|arg(d-exp(i*theta))|<|theta|` for nonzero `theta`, because `d>2`; hence
`|sigma(theta)|<alpha<pi/2`.  Equality of labels on the active cap is
therefore equality of the real values `sigma`, not merely congruence modulo
`2*pi`.  The function is odd, and differentiation gives

```text
sigma'(theta)
 = (d^2+3-4*d*cos(theta))/(d^2+1-2*d*cos(theta)).     (9)
```

## 4. Monotonicity on the two step intervals

Define

```text
cos(beta)=(d^2+3)/(4*d),              0<beta<pi/2.
```

The derivative (9) is positive when `|theta|>beta`.  We next show

```text
alpha+beta<gamma.                                   (10)
```

Put `x=d^2`, `A=cos(alpha)` and `B=cos(beta)`.  From `d>d0` we have
`x>d0^2=4+2*sqrt(3)>7`.  Direct substitution gives

```text
A*B=(x^2-9)/(8*x)>1/2,
A^2+B^2-A*B-3/4 = 3*(x-3)*(x-7)/(16*x)>0.            (11)
```

The second identity says

```text
(A*B-1/2)^2 > (1-A^2)*(1-B^2).
```

Together with the first inequality and positive sines, this yields
`cos(alpha+beta)>1/2`, proving (10).

It follows from (10) that every point of `J_-` is below `-beta`, and every
point of

```text
J_+=J_-+gamma=[-alpha+gamma,alpha]
```

is above `beta`.  Therefore `sigma` is strictly increasing on each of
`J_-` and `J_+`.

## 5. The phase-label graph is a forest

Make a graph `Gamma_d` whose vertices are the cross-triple labels `p` and
whose edges record adjacent active directions in one six-cycle orbit.  By
(5), every edge has the form

```text
{ P(exp(i*theta)), P(exp(i*(theta+gamma))) },
theta in J_-.                                       (12)
```

Using the faithful real coordinate `sigma`, (12) is an order-preserving
partial bijection from `sigma(J_-)` to `sigma(J_+)`: both endpoint functions
are strictly increasing in `theta`.  Each label is the left endpoint of at
most one edge and the right endpoint of at most one edge.  Hence
`Gamma_d` has maximum degree two.

A finite undirected cycle of length at least three would, after orienting
each edge from `sigma(J_-)` to `sigma(J_+)`, give every cycle vertex one
incoming and one outgoing edge.  It would therefore be a periodic orbit of a
strictly increasing real partial map.  Such a map has no nonconstant finite
periodic orbit: once `T(s)>s` its iterates strictly increase, and once
`T(s)<s` they strictly decrease.

It remains to exclude loops.  A loop would mean that a single cross triple
contains `u` and `u*exp(i*gamma)`.  Their sum has modulus `sqrt(3)`, so the
third member can be unit only if the point at distance `d` from the origin is
within unit distance of the circle of radius `sqrt(3)`.  In particular

```text
d<=1+sqrt(3),
```

contrary to (2).  Thus `Gamma_d` has no loop and no cycle: it is a forest.

## 6. Bipartition of both complete circles

Bipartition `Gamma_d`, writing the bit of a cross triple `T` as `q(T)`.
For every active direction in `T`, assign

```text
first-circle colour  = q(T),
second-circle colour = 1-q(T).                      (13)
```

Every cross edge is proper because its two direction endpoints occur in the
same triple (1).  Any two adjacent active directions on one owner circle
give an edge of `Gamma_d`, so (13) also makes their same-circle edge proper.

Now consider any full six-cycle direction orbit.  It has at most two active
members.  If it has two, they are adjacent and already have opposite colours;
there is a unique alternating extension around the orbit.  If it has one or
zero, choose either compatible alternating phase.  Repeated cross-triple
members cause no exception: (6) still supplies one label, and (13) separates
the two circle owners.  This colours both complete circles with two colours
and exhausts all same-circle and cross-circle unit pairs.  The two-circle
theorem follows.

## 7. Sharpness of the two-circle threshold

At `d=d0`, take on the first circle

```text
u_- = sqrt(3)/2-i/2,       u_+ = sqrt(3)/2+i/2,
```

and on the second circle take the plane point `sqrt(3)=d0-1`.  All three
pair distances are one.  Hence the strict two-circle graph contains a
triangle and is not bipartite at equality.  This only makes the two-circle
lemma sharp; it is not a five-chromatic construction.

## 8. Three-centre lift and domination consequence

Let `a0,a1,b` be three centres with every mutual distance greater than two,
and suppose their diameter exceeds `d0`.  Choose a diameter pair.  Their two
complete circles are bipartite by the theorem, using colours `{0,1}`.
Bipartition the third complete circle by its six-cycle orbits using the
disjoint palette `{2,3}`.  Give `a0,a1` colour 2 and `b` colour 0.

The owner circles are pairwise disjoint.  A centre has no neighbour on
another centre's circle, and centre pairs are nonedges.  Same-palette rim
edges are proper by the two bipartitions, different-palette rim edges are
automatic, and each centre avoids the palette on its own circle.  These
classes exhaust all unit pairs in the full support, proving four-colourability.

If a finite plane unit-distance graph is dominated by the three centres, it
is a subgraph of this full strict support.  Consequently every dominating
triple in a non-four-colourable plane unit-distance graph, subject to all
three centre distances being greater than two, has diameter at most
`1+sqrt(3)`.

## 9. Exact open fixture and scope

The centres

```text
(0,0), (11/4,0), (11/8,11*sqrt(3)/8)
```

form an equilateral triangle of side `11/4`.  Exactly

```text
2 < 1+sqrt(3) < 11/4 < 3,
```

where `11/4>1+sqrt(3)` follows by squaring `7/4>sqrt(3)`.
All inequalities are strict, so the theorem covers a neighbourhood of this
realized triangle in three-dimensional side-length space.

This is a sufficient global exclusion for a stated geometric region, not a
classification of every independent dominating triple.  The remaining
frontier is the union of triples with some centre separation at most two and
triples with all separations above two but diameter at most `1+sqrt(3)`.
Failure of this proof at the boundary is a realized triangle in the auxiliary
two-circle support, not evidence that any three-centre support needs five
colours.
