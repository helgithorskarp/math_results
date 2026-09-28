# A universal vertex lifts small balanced separators to geodesics

All graphs here are finite, simple, and unweighted. Vertex masses are arbitrary
nonnegative real numbers. A path of one vertex is permitted. Shortest paths are
measured in the original graph before any deletion.

## Separator lifting lemma

Let `u` be a universal vertex of `G`, let `H = G - u`, and let `S` be a
vertex set in `H` of size `s` for which every component of `H - S` has
mass at most half the total mass of `H`. Then `G` has a half-balanced
separator that is a union of at most `ceil((s + 1)/2)` geodesics when
`s >= 1`, or one geodesic when `s = 0`.

For `s = 0`, delete the singleton path `u`. Otherwise choose `x` in `S`
and use the edge `ux` as the first geodesic. Pair the vertices of
`S - {x}` arbitrarily. For each pair `y,z`, use the edge `yz` if it exists;
otherwise use `y-u-z`, which is a shortest path because `y,z` are not
adjacent. If one vertex remains unpaired, use it as a singleton path.
The number of paths is `1 + ceil((s-1)/2) = ceil((s+1)/2)`, and their union
is exactly `{u} union S`. The remaining components are those of `H - S`.
Their masses are at most `mass(H)/2 <= mass(G)/2`.

## Balanced bag lemma

If `H` has a tree decomposition of width at most `k`, then for every
nonnegative vertex mass function it has a set `S` of at most `k+1`
vertices whose deletion leaves components of mass at most `mass(H)/2`.

Take any width-`k` tree decomposition `(T, (B_t))`. Assign every vertex
`v` of `H` to one node `a(v)` with `v in B_{a(v)}`, and give tree node `t`
the sum of the masses assigned to it. Choose a weighted centroid `t` of
`T`, so each component of `T-t` has assigned mass at most `mass(H)/2`.
Set `S=B_t`. For `v` outside `S`, the connected subtree of bags
containing `v` avoids `t` and lies in one component of `T-t`. If two
vertices outside `S` are adjacent in `H`, a bag contains both, so their
subtrees lie in the same component. Hence every component of `H-S`
corresponds to one component of `T-t` and has at most its assigned mass.
The empty graph is immediate.

## Theorem and planar corollary

**Theorem.** If `G` has a universal vertex `u` and
`tw(G-u) <= k`, then for every nonnegative vertex mass function `G`
has a half-balanced separator equal to a union of at most
`ceil((k+2)/2)` geodesics (with the singleton `u` handling an empty
`G-u`).

Apply the balanced bag lemma to `H=G-u`, then the lifting lemma to its
bag. The bound follows from `|S| <= k+1`.

**Corollary.** Every planar graph with a universal vertex has a
half-balanced separator equal to a union of at most **two** geodesics,
for arbitrary nonnegative vertex masses.

For a planar embedding of `G`, delete `u` and its incident edges. The
faces incident with `u` merge into one face of `H=G-u`, incident with
every remaining vertex because each was adjacent to `u`. Thus `H`
has an embedding with all vertices on one face: it is outerplanar.
Every outerplanar graph has treewidth at most two. One way to see this
is to extend it to a maximal outerplanar graph and use the triangles
of a triangulated polygon as bags, joined along shared chords in the
weak dual tree; the small orders are immediate. The theorem with `k=2`
gives two paths.

## Sharpness and relation to face-separable graphs

For `n >= 7`, let `G_n = K_2 join P_{n-2}`: two adjacent universal
vertices `u,v`, and a path `x_1,...,x_{n-2}`, each of whose vertices
is adjacent to both `u,v`. This is planar: `v join P_{n-2}` is a
maximal outerplanar fan, and `u` can be attached in its outer face.
It has `1 + (n-3) + 2(n-2) = 3n-6` edges, so it is maximal planar.

One geodesic never half-balances `G_n`. Its diameter is two, so a
geodesic contains at most three vertices. If it omits `u` or `v`, the
surviving universal vertex connects all remaining vertices, leaving
one component of at least `n-3 > n/2` vertices. A geodesic containing
both `u,v` must be their edge, since they are adjacent and every other
pair has distance at most two. Deleting this edge's endpoints leaves
the connected path on `n-2 > n/2` vertices. Thus the two-path bound is
sharp even for planar triangulations with a universal vertex.

The same family shows that the corollary is not merely an instance of
Diot and Gavoille's face-separable theorem. In its natural spherical
embedding every face is a triangle. Removing a facial triangle that
omits one of `u,v` leaves that hub and hence a connected complement;
removing either terminal facial triangle containing both hubs leaves
the connected path on the remaining `n-3` vertices. In each case
`n-3 > n/2`. Since maximal planar graphs on at least four vertices
have unique spherical embedding up to reflection, no embedding has a
half-balanced facial border. Consequently `G_n` is not face-separable.

The prior face-separable theorem is in E. Diot and C. Gavoille,
[On the Path Separability of Planar Graphs](https://dept-info.labri.fr/~gavoille/article/DG09a),
Electronic Notes in Discrete Mathematics 34 (2009), 549–552. Their later
[Path Separability of Graphs](https://emilie-diot.eu/Article/DG10a)
(2010), Proposition 1(1), already proves that every graph of treewidth at
most three has a half-balanced separator formed by two shortest paths,
including with nonnegative vertex masses. Since adding a universal vertex
to a width-two graph gives a width-three decomposition, the universal-vertex
corollary here is an explicit construction within that prior theorem, not a
new path-separability class. The family above only shows that it is not
covered by the *face-separable* subclass. No literature priority claim is made.
