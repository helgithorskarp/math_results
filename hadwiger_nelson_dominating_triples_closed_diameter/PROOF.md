# Proof: the closed diameter-three boundary is four-colourable

For a point `c`, write `C(c)={x:|x-c|=1}`.  Let `a0,a1,b` be distinct and put

```text
Y={a0,a1,b} union C(a0) union C(a1) union C(b),
```

where `|a0-a1|>=3`.  All graph edges below mean Euclidean distance exactly
one.

## 1. The leaf support is bipartite

Put `omega=exp(i*pi/3)`.  On one unit circle, unit edges join precisely the
directions differing by `omega` or `omega^-1`.  The strict graph on a unit
circle is therefore a disjoint union of six-cycles.  Choose one direction
representative from each orbit in the half-open angular sector `[0,pi/3)`;
each orbit then has two explicit binary phases.

Call `C(a0),C(a1)` the leaf circles.  If `|a0-a1|>3`, no point of one leaf
circle is unit-separated from a point of the other, by the triangle
inequality.  If `|a0-a1|=3`, equality in

```text
|a0-a1| <= |a0-x|+|x-y|+|y-a1| = 3
```

forces the three unit segments to be collinear and codirected.  Thus there is
exactly one cross-leaf unit edge, between the two points dividing the segment
`a0 a1` into thirds.  Joining two bipartite circle components by one bridge
preserves bipartiteness.  Hence the full strict graph

```text
A = U(C(a0) union C(a1))
```

is bipartite for every `|a0-a1|>=3`.  The leaf circles are disjoint because
their centres are more than two apart.

The central circle graph `B=U(C(b))` is also bipartite.  We will use colours
`{0,1}` on selected vertices of `A` and colours `{2,3}` on selected vertices
of `B`.

## 2. The only monochromatic intersection exception

Let

```text
Mi=C(ai) intersection C(b),  i=0,1.
```

Each set has at most two points, and `M0,M1` are disjoint because the leaf
circles are disjoint.  If the two unit circles with centre separation `d`
meet in two points `p,q`, then

```text
|p-q|^2=4-d^2.                                      (1)
```

The squared chord lengths at rotation steps `0,...,5` on a unit circle are

```text
0,1,3,4,3,1.
```

Two prescribed points can receive the same binary colour unless they lie in
one orbit at an odd step.  Combining this table with (1), and excluding
coincident centres, shows that the only positive centre separation at which
the two points of `Mi` cannot be prescribed alike is

```text
|ai-b|=sqrt(3).                                     (2)
```

Call index `i` exceptional when (2) holds.  Then `Mi` consists of the
endpoints of a unit edge in both owner circles.

Fix `colour(b)=0`.  Every point of an `Mi` assigned to palette `{0,1}` will
be prescribed colour 1, so its edge to `b` is proper.  Points assigned to
palette `{2,3}` will be coloured by a bipartition of `B`.  We now make the
assignment.

## 3. No exceptional indices

At most one of `|a0-b|,|a1-b|` equals one, since otherwise
`|a0-a1|<=2`.  If such a unit index exists, call it `r`; otherwise put `r=0`.
Assign every point of `Mr` to palette `{0,1}` and every point of the other
intersection set `Ms` to `{2,3}`.

If `|ar-b|=1`, the point `b` itself lies on `C(ar)`, and the two points of
`Mr` are its two neighbours in the corresponding six-cycle.  A bipartition
with `b` coloured 0 automatically colours them both 1.  If there is no unit
index, Section 2 says that all points of `Mr` can be prescribed colour 1.
There is no other leaf-palette prescription, so this extends to a
bipartition of all of `A`; at distance three the phase on the other leaf's
bridge orbit is simply chosen to make the bridge proper.

Similarly, Section 2 lets all points of `Ms` receive one common colour in a
bipartition of `B`.  If `as` is not itself on `C(b)`, give it the other colour
of `{2,3}`.  If it is on `C(b)`, retain its bipartition colour; its two common
neighbours already have the opposite colour.  The centre `ar` is treated the
same way when it lies on `C(b)` and otherwise may receive either central
colour, since no point of `Mr` was assigned centrally.

## 4. Exactly one exceptional index

Let `e` be exceptional and `j=1-e`.  Split the edge `Me`: assign one endpoint
to each palette.  Assign all of the nonexceptional set `Mj` to palette
`{2,3}`.

If `b` lies on a leaf circle, first choose a bipartition of `A` with `b`
coloured 0; otherwise choose any bipartition.  The two endpoints of `Me` have
opposite binary colours, so select as the leaf endpoint the one coloured 1.
This satisfies every leaf-palette prescription.

On `B`, make `Mj` monochromatic, which Section 2 permits.  The remaining
endpoint of `Me` takes whatever central colour its orbit supplies.  Give
`ae` the opposite central colour.  If `aj` is not on `C(b)`, give it the
opposite colour to `Mj` (or either colour when `Mj` is empty); if it is on
`C(b)`, retain its bipartition colour.  In the latter case the points of
`Mj` are its two circle neighbours and already have the opposite colour.

## 5. Two exceptional indices

Choose any bipartition of `A`; here `b` is on neither leaf circle.  From each
unit edge `Mi`, assign its unique colour-1 endpoint to the leaf palette and
the other endpoint to the central palette.  Thus both leaf prescriptions are
satisfied even if the two relevant six-cycles are connected by the
distance-three bridge.

Choose any bipartition of `B`.  Each `Mi` has only one centrally assigned
point, so give `ai` the opposite central colour to that point.  The two leaf
centres are not adjacent because their separation is at least three, and
their colours need not agree.

These three cases exhaust every centre position.

## 6. Check all edges and pass to domination

Every vertex assigned palette `{0,1}` lies in `A` and uses one fixed proper
bipartition of `A`.  Every vertex assigned palette `{2,3}` lies in `C(b)` and
uses one fixed proper bipartition of `B`.  Thus all same-palette unit edges
are proper, while different palettes are colour-disjoint.

The centre `b` has colour 0.  Its leaf-palette neighbours are precisely the
assigned points of `M0 union M1`, all coloured 1, and its other neighbours
use the central palette.  A leaf centre `ai` has leaf-palette neighbours in
its own circle.  Its central-palette neighbours are precisely the centrally
assigned points of `Mi`, and its colour was either inherited from the proper
central-circle bipartition or explicitly chosen opposite their common or
singleton colour.  Centre-centre edges are also proper: `a0,a1` are not
adjacent, and when `ai,b` are adjacent their colours lie in disjoint palettes.
This covers every unit edge of `Y`, so `chi(Y)<=4`.

If a plane unit-distance graph is dominated by the three centres, every
noncentre vertex lies on one of these circles.  Its graph is a subgraph of
the strict graph on `Y`, so it too is four-colourable.  Applying the theorem
to any pair at distance at least three proves that every dominating triple
of a non-four-colourable plane unit-distance graph has diameter less than
three.

## 7. Sharpness and exact boundary

At equality take leaf centres `0,3` and central centre
`u+v`, where

```text
u=1,  v=(1+i*sqrt(3))/2.
```

The full support contains the classical Moser spindle

```text
0,u,v,u+v,rho*u,rho*v,rho*(u+v),
rho=(5+i*sqrt(11))/6,
```

because `0,u+v` dominate its seven vertices.  Its exact strict graph has
eleven edges and chromatic number four.  Hence the theorem's upper bound is
attained with leaf separation exactly three.

The certificate verifies that the two boundary six-cycles have exactly one
cross edge, exhausts their 4,096 binary assignments, and reconstructs the
sharpness graph exactly.  This proves a genuine realized boundary statement,
not an abstract phase candidate.

## 8. New stop boundary

The proof uses bipartiteness of the two-leaf support.  When the leaf-centre
distance is below three, cross-leaf unit edges form a continuum
correspondence rather than zero or one bridge, and this argument no longer
applies.  No non-four-colourable example is inferred.  The remaining global
frontier is the compact region in which all three centre separations are
strictly below three; after the unit-edge theorem, all three also differ from
one.
