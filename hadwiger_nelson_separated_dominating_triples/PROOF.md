# Proof: separated dominating triples are four-colourable

Write `C(c)={x:|x-c|=1}` and let

```text
Y={a0,a1,b} union C(a0) union C(a1) union C(b),
```

where the three centres are distinct and `|a0-a1|>3`.  All edges below mean
distance exactly one.

## 1. Binary colourings of one unit circle

Let `omega=exp(i*pi/3)`.  On a circle `C(c)`, two points are adjacent exactly
when their directions from `c` differ by multiplication by `omega` or
`omega^-1`.  Thus every orbit under multiplication by `omega` induces a
six-cycle, independently of every other orbit.  Each orbit has precisely two
binary colourings, and two prescribed points of the orbit have the same
binary colour exactly when their rotation exponents have the same parity.

Suppose two distinct unit circles with centres at distance `d` meet in two
points `p,q`.  Elementary circle geometry gives

```text
|p-q|^2=4-d^2.                                      (1)
```

The squared chord lengths in a six-rotation orbit are `0,1,3,4` at steps
`0,1/5,2/4,3`.  Hence `p,q` cannot be prescribed the same binary colour only
when their step is odd.  Equations (1) and `d>0` show that the only positive
centre separation causing this obstruction is

```text
d^2=3.                                              (2)
```

At `d=1` the two intersections are two steps apart and are compatible.  At
`d=2` there is only one intersection; at `d>2` there is none.  Coincident
centres do not occur here.

## 2. Separate the two leaf circles

Call `C(a0),C(a1)` the leaf circles and `C(b)` the central circle.  If
`x in C(a0)` and `y in C(a1)` were adjacent, the polygonal chain
`a0-x-y-a1` would give

```text
|a0-a1| <= |a0-x|+|x-y|+|y-a1| = 3,
```

contrary to the hypothesis.  In particular the two leaf circles are
disjoint, and no point has all three circles as owners.

Put `Mi=C(ai) intersection C(b)`.  Each `Mi` has at most two points and the
two sets are disjoint.  We will assign every noncentre point either to the
leaf palette `{0,1}` or the central palette `{2,3}`.  Points with one owner
are assigned to that owner's palette.  Only the points of `M0 union M1`
require a choice.

Pin the centres by

```text
colour(b)=0, colour(a0)=2, colour(a1)=3.             (3)
```

These pins are proper: `a0,a1` are not adjacent, while either may be adjacent
to `b` but has a different colour.

If `|ai-b| != sqrt(3)`, assign every point of `Mi` to the leaf palette and
prescribe colour 1 there.  Section 1 shows that this extends on `C(ai)`.  If
`|ai-b|=1`, the centre `b` itself lies on `C(ai)` and has prescribed colour
0; the two points of `Mi` are one rotation step from it and therefore both
have colour 1, exactly as required.

If `|ai-b|=sqrt(3)`, the two points of `Mi` are adjacent.  Assign one of them
to each palette.  Prescribe colour 1 at the leaf-assigned point.  At the
central-assigned point prescribe the colour in `{2,3}` different from
`colour(ai)`: colour 3 for `i=0`, and colour 2 for `i=1`.  There is only one
leaf prescription on `C(ai)`, so its binary colouring extends.

## 3. The central-circle compatibility

It remains to choose the exceptional endpoints, if any, and binary-colour
`C(b)` consistently.  The central-palette prescriptions can arise in only
two ways for each index `i`:

- if `|ai-b|=1`, the point `ai` lies on `C(b)` and is fixed to colour `2+i`;
- if `|ai-b|=sqrt(3)`, one selectable endpoint of the unit edge `Mi` is fixed
  to colour `3-i`.

The first event cannot occur for both indices, because it would imply
`|a0-a1|<=2`.  Thus, if there are two prescriptions, at least one comes from
a selectable unit-edge endpoint.

If the two prescribed objects belong to different six-rotation orbits of
`C(b)`, their orbit phases are independent.  If they belong to the same
orbit, a selectable unit edge has one endpoint of each parity.  Choose its
endpoint so that the parity relation agrees with whether the two prescribed
colours in `{2,3}` are equal or different.  With two selectable edges, choose
an endpoint of the first arbitrarily and then the required-parity endpoint of
the second.  Their underlying point sets are disjoint by Section 2.  Hence
all central prescriptions extend to a binary colouring of `C(b)`.

The finite certificate exhausts the eleven normalized same-orbit cases:
four fixed-point/edge positions, four edge/fixed-point positions, and three
disjoint edge/edge positions.  This enumeration only audits the elementary
choice just proved; the continuum statement does not rest on sampling.

## 4. Check every unit edge

Use the chosen binary leaf colourings in palette `{0,1}` and the central
binary colouring in palette `{2,3}`.  At a multiple-owner point use the
palette to which it was assigned.

Two leaf-palette points with the same leaf owner are properly coloured by
that leaf's binary colouring.  Two with different leaf owners cannot be
adjacent by Section 2.  Every two central-palette points lie on `C(b)` and are
properly coloured by its binary colouring.  Points in different palettes
have different colours.

For centre edges, an `ai`-neighbour using the leaf palette has colour 0 or 1.
An `ai`-neighbour using the central palette is necessarily a selected point
of `Mi` and was explicitly given the colour opposite (3).  Similarly, a
`b`-neighbour using the central palette has colour 2 or 3, while one using the
leaf palette is in some `Mi` and was explicitly given colour 1.  The
centre-centre edges were checked after (3).  These cases exhaust the strict
unit graph on `Y`, proving `chi(Y)<=4`.

Every graph dominated by `{a0,a1,b}` embeds as a subgraph of `Y`, so the
domination corollary follows by restriction.

## 5. Sharpness

The certificate contains the classical seven-vertex Moser spindle

```text
0, u, v, u+v, rho*u, rho*v, rho*(u+v),
u=1, v=(1+i*sqrt(3))/2, rho=(5+i*sqrt(11))/6.
```

Its exact strict unit graph has eleven edges, is dominated by vertices
`0,u+v`, and has chromatic number four.  Add the third centre `4`.  The pair
`0,4` has distance four, while the full three-circle support contains the
entire spindle because every spindle vertex is a centre or is adjacent to
`0` or `u+v`.  Therefore the theorem's upper bound four is attained.

The checker reconstructs all 21 spindle distances exactly, checks a proper
four-colouring, and rejects all `3^7=2187` labelled three-colourings.

## 6. Scope

The strict inequality is essential to this proof mechanism.  At leaf-centre
distance exactly three there is one unit edge between the two leaf circles;
the disjoint-palette argument above no longer covers that edge.  No claim is
made here for that boundary or for triples with all three pairwise distances
below three.  This is an explicit stop boundary, not evidence that either
remaining family contains a five-chromatic graph.
