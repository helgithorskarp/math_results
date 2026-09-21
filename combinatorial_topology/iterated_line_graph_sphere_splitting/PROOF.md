# Sphere splitting under iterated line graphs

All graphs are finite, simple and undirected. Write `L(G)` for the line
graph, `Cl(G)` for the clique complex (all cliques, not only maximal ones),
and `X^(2)` for the two-dimensional skeleton of a simplicial complex.
Homotopy statements concern geometric realizations. For a connected graph
with at least two edges set

\[
 s(G)=\sum_{v\in V(G)}\binom{\deg_G(v)-1}{3},
\]

where a summand is zero when the degree is at most three.

**Theorem 1 (splitting).** For every such graph,

\[
 \mathrm{Cl}(L^2G)\simeq
 \mathrm{Cl}(LG)\vee\bigvee^{s(G)}S^2.                 \tag{1}
\]

The equivalence is not asserted to be canonical or equivariant.
It identifies a homotopy retract, not a literal inclusion of one line
graph in another.

**Theorem 2 (sharp asphericity threshold).** Let `G` be a finite connected
simple graph. Every nonempty complex `Cl(L^r G)`, `r>=1`, is aspherical
if and only if `G` is a path, a cycle, or the claw `K_(1,3)`.
For every other `G`, `Cl(L^r G)` has `S^2` as a homotopy retract for every
`r>=5`. The constant five is best possible: the claw with one edge
subdivided once has contractible iterates for `1<=r<=4` and fifth
iterate homotopy equivalent to `S^2`.

Here aspherical means all homotopy groups in dimensions at least two
vanish. Paths include the one-vertex graph. We make no assertion that an
empty realization is an aspherical connected space.

## Prior input and scope

Adamaszek's Theorem 5.2 in *Clique complexes and graph powers* establishes

\[
 \mathrm{Cl}(LH)\simeq\mathrm{Cl}(H)^{(2)}             \tag{2}
\]

for connected nondiscrete `H`. We use it with `H=LG`. It also appears as
Lemma 3.2 in the arXiv v2 manuscript of Goyal--Shukla--Singh. This
one-step theorem is prior work. The degree-growth fact used below is a
special case of Caro--Lauri--Zarb, Theorem C; an elementary proof is included
to make the precise three-step bound transparent. See [SOURCES.md](SOURCES.md).

The additional argument is a relative star collapse showing exactly how
the two-skeleton in (2) splits when its input is already a line graph.
The asphericity statement is a corollary of this splitting and the known
degree-growth mechanism. No priority claim is made. This gives an
obstruction to maintaining asphericity under a specific graph operation;
it does not prove or refute Whitehead's asphericity conjecture.

## 1. The relative star collapse

Put `X=Cl(LG)`. Its vertices are the edges of `G`. For each vertex `v`
let `E_v` be the incident edges and let `Delta_v` be the full simplex on
`E_v`. Choose a distinguished edge `q_v` in `E_v`.

A pairwise intersecting family of edges of a simple graph either has a
common endpoint or consists of the three edges of a triangle. Indeed,
given `ab,ac`, an edge intersecting both and not containing `a` must be
`bc`; any further edge intersecting all three is one of these three.
Consequently every face of dimension at least three lies in one star
simplex. Every triangle is either a star triangle or a triangle coming
from a three-cycle of `G`. A star triangle belongs to a unique star.
Two different stars meet in at most a vertex. A three-cycle triangle
meets a star in an edge or a smaller face.

Inside `Delta_v`, define `Q_v` to consist of the entire one-skeleton,
together with the star triangles containing `q_v`. This is the cone with
apex `q_v` over the complete graph on the other star vertices. It is
contractible, has dimension at most two, and contains the entire
one-skeleton of `Delta_v`. For degree one this is a point; for degrees
two and three it is the whole simplex.

Collapse `Delta_v` to `Q_v` as follows. For every subset
`tau` of `E_v \ {q_v}` of cardinality at least three, pair

\[
                 (\tau,\tau\cup\{q_v\}).             \tag{3}
\]

Process these pairs in decreasing cardinality of `tau`. At the step for
`tau`, all its larger cofaces other than `tau union {q_v}` have already
been removed: those not containing `q_v` were lower faces of earlier
pairs, and those containing it were upper faces. No coface outside
`Delta_v` can contain `tau`, since a triple of edges sharing `v` neither
forms a three-cycle nor shares another common endpoint. Thus (3) is a
legal elementary collapse in the full current complex, with a unique
proper coface of codimension one. It removes no edge or vertex.

Do this for every star, in any order. The distinct stars do not interfere
with these pairs. The result is a two-dimensional subcomplex `K` formed
by all the `Q_v` and all the three-cycle triangles. In particular,

\[
                       X\searrow K.                  \tag{4}
\]

This argument is a collapse of the full complex. Merely discarding its
higher-dimensional faces would not give (4).

## 2. Recovering the two-skeleton by null attachments

The faces in `X^(2)` missing from `K` are precisely the star triangles
`tau` which avoid the corresponding distinguished edge `q_v`. There
are `binom(deg(v)-1,3)` at each vertex. No two stars contribute the same
triangle. For each such `tau`, its boundary lies in `Q_v`, and its
boundary loop is nullhomotopic there. Explicitly, the three triangles
`{q_v} union e`, for the three edges `e` of the boundary of `tau`, form
the cone disk filling that loop in `K`.

Attaching a two-cell to a connected CW complex along a nullhomotopic
loop gives the wedge with `S^2`: replace the attaching map by a constant
map using homotopy invariance of cell attachment. All the loops here are
already nullhomotopic in `K`, so attach the finitely many triangles one
at a time. Connectedness lets all wedge points be moved to a common
basepoint. Hence

\[
 X^{(2)}\simeq K\vee\bigvee^{s(G)}S^2
          \simeq X\vee\bigvee^{s(G)}S^2.              \tag{5}
\]

Since `G` has at least two edges, `LG` is connected and has an edge.
Apply (2) to `LG` and then (5) to obtain (1).

For any `r>=2` for which all applications satisfy this edge condition,
induction gives

\[
 \mathrm{Cl}(L^rG)\simeq \mathrm{Cl}(LG)\vee
 \bigvee^{\sum_{j=0}^{r-2}s(L^jG)}S^2.               \tag{6}
\]

In particular, this holds for every `r>=2` if `G` is not a path.
A nonpath connected graph contains a cycle or has a vertex of degree
at least three. Its line graph therefore contains a cycle, which
persists as a subgraph in all later line graphs. Thus no edge condition
can fail. For paths the formula holds up through the last nonempty
iterate; their behavior is also immediate directly.

The connected graph with one edge must be excluded from (1): its first
line graph is a point and its second line graph is empty.

## 3. A degree-four vertex within three steps

For an edge `uv` of a simple graph `H`, the corresponding vertex of
`LH` has degree

\[
                 \deg_H(u)+\deg_H(v)-2.             \tag{7}
\]

Suppose `G` is neither a path, a cycle nor a claw. If its maximum degree
is at least four, no iteration is needed. Otherwise its maximum degree
is three. Choose a degree-three vertex `v`. At least one neighbor `u`
is not a leaf, since connectedness would otherwise make `G` a claw.

If `u` has degree three, (7) gives a degree-four vertex in `LG`.
If `u` has degree two, the vertex `a` of `LG` corresponding to `vu`
has degree three. The two other edges at `v` give vertices `b,c` of
`LG`, adjacent to `a` and to one another, each of degree at least two.
If `LG` already has maximum degree at least four, we are done. Otherwise
the degrees of `b,c` are two or three. If either is three, its edge to
`a` produces a degree-four vertex in `L^2G`. If both are two, the
edges `ab,ac` produce adjacent degree-three vertices in `L^2G`; their
joining edge produces a degree-four vertex in `L^3G`.

In every case some `L^jG`, `0<=j<=3`, has a vertex of degree at least
four, hence `s(L^jG)>=1`. Formula (6) puts an `S^2` wedge summand in
`Cl(L^(j+2)G)` and preserves it in all later iterates. Collapsing the
other wedge factors supplies a homotopy retraction onto that sphere.
Its nonzero second homotopy group rules out asphericity. This proves
the upper bound in Theorem 2.

The exceptional graphs behave directly: successive line graphs of a
path are shorter paths until empty, those of a cycle are the same
cycle, and the claw maps to a triangle which stays a triangle. The
clique complexes are respectively contractible, a circle (cycle length
at least four) or a filled triangle (cycle length three and the claw's
iterates). These are aspherical. The one-vertex path has no nonempty
positive iterate, so the stated condition holds vacuously.

## 4. Sharpness

Take the tree with edge set

\[
                  \{01,02,03,34\}.                 \tag{8}
\]

Its first line graph is the paw (a triangle with a pendant edge), its
second is the diamond `K_4` minus an edge, and its third is the wheel
on a four-cycle. The degree multisets of `G,LG,L^2G,L^3G` are

\[
 (3,2,1,1,1),\quad(3,2,2,1),\quad(3,3,2,2),
 \quad(4,3,3,3,3).
\]

Their `s` values are `0,0,0,1`. By (2), `Cl(LG)` is homotopy equivalent
to the tree `G` and is contractible. Formula (6) now makes the first
four positive iterates contractible and the fifth homotopy equivalent
to one `S^2`. This proves sharpness without inferring contractibility
from acyclicity.

## Verification boundary

The proof above is an ordinary, unformalized mathematical proof, using
the credited one-step theorem and standard CW attachment invariance.
[verify.py](verify.py) provides exact finite corroboration: it constructs
clique faces directly, replays every collapse against the whole face
poset, checks the explicit cone disks, and separately computes boundary
ranks over `F_2`, including tetrahedra. The finite enumeration is not
the justification for any universal quantifier or homotopy equivalence.
