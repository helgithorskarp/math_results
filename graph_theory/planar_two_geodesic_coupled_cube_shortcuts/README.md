# Three coupled zero-mass shortcuts in the radial cube

For each of three fixed radial-cube core metrics, the construction below
has a half-balanced separator consisting of at most two ambient geodesics,
for **all six positive shortcut-edge lengths, all `4^9` parent choices,
all positive parent-edge lengths, and all nonnegative masses on the nine
marked vertices**. Two of the metrics admit a structural repair by
contracting the shortcut triangle to a point. The remaining metric has
a compact exact certificate in six independent real variables.

This excludes a particular weighted counterexample strategy for
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).
It does not assert the result for arbitrary core prices, for mass on the
other vertices, or for every unweighted planar graph. No conversion from
weighted edges to unweighted subdivisions is claimed.

## Graph and statement

Label the cube vertices by integers `0,...,7`, using their three binary
coordinates. Give the face with coordinate `a` equal to `b` the label
`8+2a+b`. List the twelve cube edges in lexicographic endpoint order, and
give their edge centers labels `14,...,25`. For each cube edge and each
incident face, insert the two triangles consisting of its center, one
endpoint, and the face center. The resulting graph `T` is the spherical
barycentric subdivision of the cube: 26 vertices, 72 edges, 48 triangles.
The verifier reconstructs oriented faces, checks the two incidences of
every edge, checks every vertex link, and checks Euler characteristic two.

Let `R` consist of the 24 edges joining original cube vertices to their
incident face centers. These are its edges in lexicographic order:

```text
(0,8) (0,10) (0,12) (1,9) (1,10) (1,12)
(2,8) (2,11) (2,12) (3,9) (3,11) (3,12)
(4,8) (4,10) (4,13) (5,9) (5,10) (5,13)
(6,8) (6,11) (6,13) (7,9) (7,11) (7,13)
```

Choose one of the following vectors of edge lengths, or any common
positive multiple of it:

```text
A: 14 38  7 23 20 17  8 30 11 21 14 29 10 28 36  4  3  7 30  6  2  4  9  5
B:  7 10  4  8  7 11  9  6 16 14  3 23  3 16 15 16  3 10 22  9 12  3 12  7
U:  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1
```

Add the six edges

```text
x1: (8,15)    x2: (8,16)    x3: (10,14)
x4: (10,16)   x5: (12,14)   x6: (12,15)
```

with independent arbitrary lengths `xi>0`. They form the cycle
`8–15–12–14–10–16–8`. Write `H` for this 17-vertex augmented core.
For each mark `z` in `M={17,...,25}`, choose one of its four neighbors
`p(z)` in `T`, and add the edge `z p(z)` with arbitrary positive length.
This produces a connected spanning subgraph `Q` with 39 edges. Give each
of the other 33 edges `uv` of `T` any positive length satisfying

```text
length(uv) >= d_Q(u,v).
```

Thus `Q` is isometric in `T`. The simpler condition that every such edge
exceed the sum of all 39 lengths in `Q` is sufficient, but unnecessary.
Assign arbitrary nonnegative vertex mass supported on `M`.

**Claim.** There are at most two shortest paths in the full weighted graph
`T` whose deletion leaves every component with at most half the total
vertex mass. All 72 edges of `T` are retained when components are computed.

The edgewise isometry condition is the weakening identified in the
[independent review of the single-shortcut result](../planar_two_geodesic_zero_mass_cube_shortcut_review1/REVIEW.md).
For completeness, replacing each edge outside `Q` in any `T` walk by a
shortest `Q` path gives a `Q` walk no longer than the original one. Together
with `Q` being a subgraph, this proves `d_T=d_Q`, including equality cases.
Every certified `Q` geodesic is therefore an ambient `T` geodesic.

## Reductions common to all three metrics

Every mark is a leaf in `Q`. A simple `Q` path can contain a mark only as
an endpoint. Once its required parent is fixed, its parent-edge length
occurs identically in the path length and the endpoint distance, and
cancels. The nine parent-edge lengths therefore require no discretization.
Rescaling all lengths also removes the common positive scale of `R`.

Call a pair of paths a **four-residue pair** when every component of the
full graph `T` after its deletion contains at most four marks. It is enough
to find one geodesic four-residue pair for every choice of lengths and
parents. Indeed, if the four heaviest marks carry at least half the total
mass, pair them by two arbitrary ambient geodesics; their union deletes
at least half. Otherwise every set of at most four marks has less than
half the mass, and the four-residue pair works. This includes zero masses
and total mass zero. Only this elementary mass reduction is used.

## A parameter-independent repair for B and U

Set all six shortcut lengths to zero in `H`. This gives a pseudometric
`d_0`, obtained by identifying the three face centers `8,10,12` and the
three zero-mass centers `14,15,16`. For any positive six-tuple `x`,
`d_0(a,b) <= d_H(a,b)`.

Suppose a path using only edges of `R` has length exactly `d_0(a,b)`.
It then remains geodesic for **every** positive six-tuple: its unchanged
length is both a lower bound on the distance and the length of an
available path. Forced leaf endpoints can be appended by the preceding
cancellation argument. This is the structural obstruction to destroying
all useful paths by making the three shortcuts arbitrarily strong.

For B, `certificate_static.json` supplies 44 conditional four-residue
pairs of this kind. Their parent conditions cover every assignment. For U,
four explicit pairs suffice, according to the parent of mark 17:

| Parent of 17 | First path | Second path | Residual marked counts |
|---|---|---|---|
| 1 | `0,8,2,11,7` | `17,1,10,5,13` | `4,4` |
| 3 | `17,3,9,5,13` | `4,8,6,11` | `1,3,4` |
| 9 | `0,8,2,11,7` | `17,9,5,13,4` | `1,3,4` |
| 12 | `0,8,4,13,7` | `17,12,3,11,7` | `4,4` |

The checker independently computes `d_0` by Floyd–Warshall with six zero
edges, checks all path lengths and full-graph components, and checks the
parent cover. For each mark it encodes exactly one of four parents. A
template with conditions `C` yields the clause `OR_{c in C} NOT c`,
asserting that this template cannot be used. A reverse unit propagation
(RUP) proof of the empty clause shows that no parent assignment avoids
every template. There are three RUP additions for B and one for U.

## A certificate in six variables for A

For A, the above parameter-independent route library does not cover every
parent assignment. That failure is not a counterexample. The full repair
uses paths that depend on the six shortcut lengths; seven templates allow
a zero-mass shortcut center as a path endpoint.

The checker constructs a finite route catalog in `H` by direct DFS through
simple paths. Its only pruning rule is that every segment consisting of
edges of `R` must be shortest in `R`. This rule is necessary for an ambient
geodesic: replacing a nonshortest segment gives a shorter walk, from which
positive-length cycles can be removed. Thus the catalog contains every
geodesic for every positive six-tuple, including ties. It has 1,066 routes
over all unordered endpoint pairs, including singleton paths. Its routes
need not all be geodesic.

Every catalog route has affine length `c + sum_i ai xi`. A proposed route
is geodesic exactly when no catalog route with the same endpoints is
strictly shorter. For each of the 48 pairs in `certificate_A.json`, the
checker verifies simplicity, valid edges and parent requirements, and at
most four residual marks per component of the full `T`. It then adds the
clause asserting that this pair is unavailable: either one of its parent
conditions fails, or some competing route is strictly shorter than one
of its two core paths. Together with positive lengths and exactly-one
parent clauses, this reconstructs 117 base clauses and 177 distinct
linear atoms.

The resulting mixed Boolean/linear system is inconsistent. The stored
proof has 217 exact rational Farkas lemmas and 28 RUP additions. An atom
represents an affine inequality `f(x)>=0`; its negative literal represents
`-f(x)>0`. For each Farkas lemma, the checker verifies strictly positive
rational multipliers whose combination has zero variable coefficients
and either a negative constant or a zero constant with a strict summand.
The conjunction is therefore impossible over the reals. Its negation is
a sound clause. RUP then derives the empty clause. No SAT, SMT, floating
point computation, or solver proof parser is needed for replay.

Consequently some certified pair is geodesic for every positive six-tuple
and every parent assignment. The mass reduction proves the claim for A.

## Reproduction and trust boundary

From the repository root, use Python 3.11 or later with assertions enabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_coupled_cube_shortcuts/verify.py
```

The program uses only the standard library and writes no files. Expected
output includes:

```text
status PASS; vertices 26; edges 72; faces 48
A: routes 1066; templates 48; parent assignments 262144
   base clauses 117; linear atoms 177; Farkas lemmas 217; RUP additions 28
B and U: templates 48; RUP additions 4
```

The compact certificates are 11,625 and 5,197 bytes. Their SHA-256 hashes:

```text
certificate_A.json
440d6ee5330a11034d9fe585b4bcc472cba182221bc99d2060ed0f84ff47f604
certificate_static.json
957998ff4ead354c36ec283a44f2fd4a3d1b5ed08ab8b751299fa0126a8e921f
```

The exploratory generator used a triangle-route decomposition and SMT/SAT
search; neither is imported or trusted by the verifier, which rebuilds
the path catalog and finite formula. The final certificates are the entire
required external data. The continuum conclusion also relies on the
written catalog-completeness, leaf, isometry, and mass arguments above.
This is an exact computer-assisted lemma with a separate checking
implementation, not a proof-assistant formalization or an independent
review by another researcher.

## Context and remaining construction space

The [single-shortcut certificate](../planar_two_geodesic_zero_mass_cube_shortcut/README.md)
treated one zero-mass edge center and eleven potentially positive-mass
centers. This result couples three shortcuts and has nine marked centers;
neither mass-support statement contains the other. The new static
zero-contraction repair explains why two of these metrics survive every
shortcut length, while A requires the six-variable argument.

The three fixed core vectors remain a restriction. The result does not
classify the 24-dimensional core-price space or distributed shortcuts
through four or more face centers. Those remain potential construction
directions; a failed restricted path library alone is never a negative
instance of the original separator problem.

The official problem asks for one-half balance, while its cited known
two-path guarantee is only two-thirds. The
[workshop schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html)
announces a disproof of a Codsi conjecture, but does not supply the precise
statement or witness needed to identify it with Problem 31. These sources
were checked on 2026-09-28. No claim about priority or the current status
of the unrestricted problem follows from this construction exclusion.
