# A facial attachment can defeat a prescribed first geodesic

This is an obstruction to extending the prescribed-first-path conclusion
of the [interval/facial sweep theorem](../planar_two_geodesic_interval_sweep/README.md).
It is **not a counterexample** to
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).
All edges below have length one, all paths are shortest in the full original
graph, and deleting paths means deleting their vertices.

There is a **43-vertex simple planar graph** G, a vertex r whose nonneighbors
induce a chordless four-cycle, and a prescribed two-edge r-to-that-cycle
geodesic P, such that

    min over all ambient geodesics Q of max component size of G-(P union Q)
        = 22 > 43/2.

The second path Q is completely unrestricted: it need not start at r or
end on the cycle. Nevertheless the two edges `ra` and `bc` are a half
separator of this same graph; their largest residual component has order
17. The failure concerns fixing P in advance, not the two-path target.

## Construction

First construct an outerplanar graph H_m, for m>=2. Start with the triangle
`abc`. For each of its three sides keep the side edge and add a parallel
alternative path with m new internal vertices:

    a - x_1 - ... - x_m - b,
    b - y_1 - ... - y_m - c,
    c - z_1 - ... - z_m - a.

All three alternative paths lie outside the central triangle, with their
internal vertices on the outer face. Add a vertex r adjacent to EVERY
vertex of H_m. The resulting planar cone K_m has `3m+4` vertices. Its
triangle `r x_1 x_2` is facial. No diagonals are added within the three
long faces of H_m.

For k>=4, take the unit annulus A_k with vertices

    r, u_0,...,u_(k-1), v_0,...,v_(k-1)

and, with subscripts modulo k, edges

    r u_i, u_i u_(i+1), v_i v_(i+1), u_i v_i, u_i v_(i+1).

It has a facial inner cycle `v_0 ... v_(k-1)` and facial triangles
`r u_i u_(i+1)`. Glue A_k to K_m along the facial triangles
`r u_0 u_1` and `r x_1 x_2`, identifying `u_0=x_1` and `u_1=x_2`.
Use opposite boundary orientations and retain one copy of every shared
edge. This gives a simple planar graph G_(k,m) with

    n = 3m + 2k + 2.

Every vertex except the v_i is adjacent to r. Consequently

    G_(k,m) - N[r] = C_k.

Prescribe the path `P=(r,u_2,v_2)`. It is an ambient geodesic of length two:
its edges are present and r is not adjacent to v_2. Its only vertex in
K_m is r. In particular it avoids every vertex of H_m.

## The local obstruction

Let Q be ANY ambient geodesic of G_(k,m), and put

    S = V(Q) intersect V(H_m).

All vertices of H_m are neighbors of r, so their ambient pairwise
distances are at most two. The portion of Q between its first and last
H_m vertices therefore has at most two edges. Hence either `|S|<=2`, or
S consists of three consecutive vertices of Q and induces a three-vertex
path in H_m. Gluing adds no edge between H_m vertices, so H_m remains
induced. In particular Q cannot contain all of the clique `abc`.

**Local lemma.** For m>=2 and any such S, the component of H_m-S containing
the undeleted vertices of `abc` contains at least `2m-1` alternative-path
internal vertices, and at least `2m` vertices in total.

The undeleted central vertices are nonempty and connected, because they
form a clique. Call their component R. There are three cases.

* If no central vertex is deleted and `|S|<=2`, deleting vertices in two
  different alternative paths leaves all surviving vertices attached to
  the central clique. If both deletions lie in one alternative path, the
  other two paths contribute 2m vertices to R. If `|S|=3`, its induced
  three-vertex path lies entirely in one alternative path, and again the
  other two paths contribute 2m.
* If exactly one central vertex, say a, is deleted and `|S|<=2`, the two
  alternative paths untouched by the possible extra deletion still join
  b or c and contribute 2m. If `|S|=3`, the two other deleted vertices are
  either the first two vertices next to a in one alternative path, or
  the two tips next to a in its two incident alternative paths. All
  remaining internal vertices stay joined to b or c, so R contains
  `3m-2>=2m` of them.
* If two central vertices, say a,b, are deleted, the alternative a-b
  path may detach, while the other two paths join c. With at most two
  deletions they contribute 2m. A third deleted vertex must extend the
  edge ab to an induced three-vertex path. It is a tip adjacent to a or
  b. If it lies on the detached a-b path it does not reduce R; otherwise
  it deletes only the first vertex next to the already deleted endpoint
  of one surviving path. Thus R still contains at least `2m-1` internal
  vertices and the vertex c.

These cases prove the lemma. Additional vertices of G outside H_m can
only join residual components. Since P avoids H_m, the lemma applies
unchanged to G-(P union Q).

## Exact bounds and two unrestricted paths

Give mass one to the `3m` alternative-path internal vertices and mass zero
to all other vertices. The local lemma gives a residual mass of at least
`2m-1` for every Q. This is attained by

    Q_* = (a,b,y_1).

It is an ambient geodesic: `ab` and `b y_1` are edges but `a y_1` is not.
After deleting P and Q_*, the component containing c has mass `2m-1` and
the detached x-path has mass m. All remaining vertices have mass zero.
Thus the exact weighted optimum is `2m-1`. It exceeds half of `3m` for
every m>=3. The case `(k,m)=(4,3)` is a 19-vertex example with nine
unit-mass vertices and optimum 5 rather than at most 4.

For UNIFORM vertex masses, the local lemma gives a component of order at
least 2m. The same Q_* leaves the c-component with exactly 2m vertices;
the x-path together with any annular vertices has at most `m+2k-4`
vertices, because P already deletes r and two annular vertices not in
H_m. Therefore the uniform optimum is exactly 2m whenever `m>=2k-4`.
In particular, whenever

    m > 2k+2,

we have `2m > (3m+2k+2)/2`: no second geodesic completes P to a half
separator. Taking k=4,m=11 gives the claimed 43-vertex example. For fixed
k the optimal residual fraction tends to 2/3 as m grows. This is a limit
for this family, not a universal upper bound for prescribed paths.

By contrast, the unrestricted pair of edges `ra` and `bc` deletes exactly
the four central vertices. The remaining components have orders

    m, m, m+2k-2.

The last contains the x-path and the annulus without r. They half-balance
uniform masses whenever `m>=2k-6`, in particular throughout the stated
counterexample range. For the mass supported on the alternative paths,
all three component masses are m, so this pair always half-balances.

## What extension this rules out

In the unattached annulus, every vertex lies on a shortest path from r
to its facial inner cycle. The facial-support theorem therefore permits
P to be prescribed for every vertex-mass assignment. The attachment adds
only neighbors of r, through one facial triangle. These new vertices do
not lie on shortest r-to-inner-cycle paths: those paths have length two
and use an original u_i as their sole internal vertex.

Thus one cannot replace the support hypothesis by the condition that all
unsupported vertices are neighbors of r, even when the nonneighbors of
r form one chordless cycle. Nor can one retain the prescribed first path
through this simple facial triangle attachment. A proof for arbitrary
unicyclic nonneighbors would have to allow a different first path, or use
another invariant.

This does NOT disprove closure of the unrestricted two-path property
under clique sums: the displayed two-edge witness handles this family.
It also differs from a failure of two paths required to start at the same
root; here the second path is arbitrary. No novelty or general sharpness
claim is made for prescribed-path obstructions.

The [independent sweep review](../planar_two_geodesic_interval_sweep_review1/REVIEW.md)
identified control of mass outside the facial union as the missing bridge.
The example isolates a concrete failure of one proposed form of that
bridge. It leaves the original interval theorem and its review intact.

## A safe reduction for peripheral components

Here is a small structural reduction that does survive; it does not retain
the prescribed path. Let G be planar, let r be a vertex, and suppose the
induced graph on `C=V(G) minus N[r]` is nonempty and connected. Put
`B=N(r)`, let A be the vertices of B with a neighbor in C, and let K be a
component of `G[B minus A]`. Then K has at most two neighbors in A.

Indeed, contract C and K separately to vertices c and x. If K had three
distinct neighbors in A, those neighbors together with r,c,x would give
a K_(3,3) subgraph of the planar minor. Thus the boundary of K is contained
in `{r} union Y` for some Y subset A of size at most two.

The torso on `K union {r} union Y`, completing this boundary to a clique,
has treewidth at most three. For two vertices a,b in Y, an a-b path with
interior in C supplies the added edge ab by a planar minor operation.
The torso is consequently planar with universal vertex r. Deleting r
gives an outerplanar graph, of treewidth at most two; adding r to every
bag gives width at most three. This decomposition has a bag containing
the completed boundary clique.

Consequently, if K has more than half the total vertex mass, G has a
two-geodesic half separator, for ANY positive edge lengths. To see this,
join the local width-three decomposition at its boundary bag to one large
bag containing all vertices outside K. Assign the mass of K to local bags
and all other mass to the large bag. That large bag cannot be a weighted
centroid, because its one branch contains all of K and has more than half
the mass. A centroid is therefore a local bag with at most four vertices.
Cover those vertices by two ambient shortest paths; deleting additional
path vertices cannot spoil balance.

For the unit single-cycle target, C is facial and the facial interval
union is exactly `{r} union A union C`. This reduction settles the case
of a heavy component outside that union by allowing BOTH paths to change.
The remaining case has every peripheral component of mass at most half.
No theorem completing a fixed first path in that remaining case is claimed.

## Reproduction and trust boundary

Run with Python 3.11 or later, using only the standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_prescribed_attachment/verify.py --check
```

The checker validates a spherical rotation system for each fixture,
independently recomputes unit distances by BFS, enumerates all ambient
geodesics, checks their actual residual components, and verifies the
unrestricted two-edge witnesses. It also directly checks the local lemma
over every possible one- or two-vertex set and every induced three-vertex
path in its tested H_m graphs. The run checks 9,262 ambient geodesics
across seven original fixtures and one triangulated control, and 8,880
local deletion sets for m=2,...,16. Exact counts appear in `expected.json`.
The parameterized theorem rests on the written case analysis, not these
finite runs. No solver, census, or formal proof is a premise, and this
publication is not independent review.

The boundary fixtures include m=2 for the weighted threshold and k=4,m=10
for uniform equality. A control triangulates the three long faces of the
43-vertex example into fans; the obstruction then disappears, with a
completion leaving at most 13 vertices. This explains why the preceding
private probe of 48 triangle-stacked attachments, all positive, could not
justify a transfer theorem. Graph triangulation changes ambient shortest
paths and is not a valid preservation step for this prescribed-path claim.
