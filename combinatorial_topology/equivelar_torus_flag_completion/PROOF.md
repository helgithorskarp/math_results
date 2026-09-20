# Flag completions of degree-six torus triangulations

## Statement

Let `T` be a finite simplicial complex triangulating the two-dimensional torus,
with every vertex incident to exactly six edges. Put `G = T^(1)`, let
`K = Cl(G)` be its flag (clique) completion, and assume **G contains no K4**.
Write `n = |V(G)|`, and call a graph triangle missing if it is not a face of T.
Exactly one of the following alternatives holds:

1. There are no missing triangles, and `K = T` is a torus.
2. The missing triangles partition the vertex set into `m = n/3` triples.
   Their boundary curves are disjoint parallel primitive essential geodesics
   in the equilateral metric, and
   `K ≃ S¹ ∨ (∨_{i=1}^m S²)`.
3. `n = 9`, `G ≅ K_{3,3,3}`, there are nine missing triangles, and
   `K ≃ ∨_{i=1}^8 S²`.

Here ≃ means homotopy equivalence. In particular, **K is aspherical if and
only if T was already flag**. These alternatives concern the full flag
completion, not merely the triangle-filled two-skeleton of a larger complex.

This is an all-size geometric proof. The finite computation in `verify.py`
is corroboration, not the proof. The classical lattice representation and
known nine-vertex example are credited in `REFERENCES.md`; no priority claim
is made for the combined statement.

## 1. Classical flat-lattice representation

Give each face of T the metric of a unit equilateral triangle and glue along
edges. Six faces surround each vertex, so the total angle is 2π. Thus T is a
complete flat oriented surface. Its universal cover, developed into the
Euclidean plane, is the regular triangular tiling. One may use the standard
fact that a complete simply connected flat surface is isometric to the plane;
the lifted equilateral triangles then determine the regular tiling.

Every deck transformation is an orientation-preserving Euclidean isometry
without fixed points. Such an isometry is a translation. The transformations
preserve the vertex lattice, so they form a rank-two sublattice Λ of
`L = Zu + Zv`, where u and v are unit vectors at angle π/3. Consequently
`T = Δ/Λ`, with Δ the triangular tiling and `n = [L:Λ]`.
This is the classical description of equivelar torus triangulations, not a
new classification here; see Altshuler and Mohar–Salas, Theorem 2.2.

The six directed unit edge steps are
`±u, ±v, ±(u−v)`. Simpliciality and degree six imply that their images at each
vertex are six different vertices, all different from the vertex itself.
In particular, neither s nor 2s belongs to Λ for a unit step s.

## 2. The straight-triangle obstruction

**Lemma.** Every missing triangle is a straight closed geodesic of length
three, in one of the three lattice-axis directions.

Let abc be a missing triangle. The simplicial link of a in **T** is a
six-cycle. (The graph induced on its six neighbors in **G** may have extra
edges; these two links must not be confused.) The distance between b and c
in that cycle is 1, 2, or 3. Distance 1 means abc is a face of T, contrary to
its being missing. At distance 2 there is a link vertex d adjacent in the
link to both b and c. Then a,b,c,d span all six edges of a K4 in G, contrary
to the hypothesis. Therefore their link distance is 3.

Thus the incoming and outgoing edge germs of the triangle are opposite at
a. The same argument works at b and c. On lifting the three-edge path to
Δ, all three directed steps are equal to one unit step s. Its endpoints
differ by 3s, which lies in Λ. This proves the lemma.

Conversely, if `3s ∈ Λ`, the vertices `p, p+s, p+2s` are distinct and form a
graph triangle for every lattice vertex p. It is missing: its two edge germs
at p are opposite, whereas a surface face uses consecutive germs. Hence the
missing triangles are **exactly** the length-three orbits in the directions

`D = {s ∈ {u,v,u−v} : 3s ∈ Λ}`.

The loops are essential, because their lifts have nonzero displacement 3s.
They are primitive: a shorter lattice period on the line Rs would have to be
s or a divisor of 3s in L, and s is excluded. Equivalently, Λ∩Rs = Z(3s).
Each such triangle is embedded because T is simplicial.

## 3. Classifying the short directions

If D is empty, the lemma says there are no missing triangles. The K4-free
hypothesis also forbids all higher-dimensional simplices of K, so `K = T`.

Suppose D has exactly one member s. The order of s in L/Λ is exactly three.
Its cosets partition all n vertices into triples, giving exactly n/3 missing
triangles. Their embedded boundary curves are disjoint, since they use
disjoint vertices and T is embedded as a surface. Translations of the flat
torus carry one such curve to any other and are isotopic to the identity.
Thus these curves are parallel and freely homotopic, up to orientation.

If two different axis directions s and t belong to D, they form an integer
basis of L. Thus `3L ⊆ Λ`, and `[L:Λ]` divides 9. Since a simple graph with
degree six has at least seven vertices, n must equal 9. It follows that
`Λ = 3L`, and the third axis also lies in D. In particular, exactly two short
directions cannot occur.

For Λ=3L the vertex group is `(Z/3Z)²`. The six neighbors of any vertex differ
from it by the six unit steps. The two remaining nonzero differences are
`±(u+v)`. The three cosets of the subgroup generated by u+v are therefore
independent triples, and every pair in different triples is an edge. This is
`K_{3,3,3}`. Each of its three short directions supplies three missing
triangles, giving nine in total. There are 27 graph triangles and 18 surface
faces, in agreement with that count.

## 4. Homotopy after disk attachment

The following elementary observation is useful beyond the lattice setting.
If m≥1 disks are attached to a torus along embedded primitive essential
circles that are all freely homotopic up to orientation, the resulting space
has homotopy type `S¹ ∨ (∨^m S²)`.

To see this, choose torus generators x,y with the first attaching circle
representing x. Such a choice exists because that circle is primitive.
Use the torus CW structure with two one-cells x,y and a two-cell attached
along `[x,y]`. The first extra disk, together with its boundary circle x,
is a contractible CW subcomplex D. Collapsing D to a point is a homotopy
equivalence. After this collapse, y remains and the torus two-cell has
nullhomotopic attaching word `[1,y]`; thus the space is `S¹ ∨ S²` up to
homotopy. Every remaining attaching circle was freely homotopic to x or its
inverse, so it is now nullhomotopic. Attaching a two-cell by a nullhomotopic
map adds a wedge summand S². This proves the observation and alternative 2.

For alternative 3, the clique complex of `K_{3,3,3}` is the join of three
sets of three points. The join of the first two sets is the graph K3,3,
which is homotopy equivalent to four circles wedged at a point. Joining a
connected CW complex X to a set of three points gives three cones on X
with their bases identified. Collapsing one cone yields, up to homotopy,
two copies of the suspension of X wedged together. With
`X ≃ ∨^4 S¹`, this is `∨^8 S²`, as claimed.

The K4-free hypothesis ensures that **these are all the attachments**:
K is obtained from T precisely by adding its missing two-simplices, with
no tetrahedra or other higher cells that could kill the resulting spheres.
This completes the trichotomy.

## 5. Asphericity and the limited Whitehead consequence

The torus is aspherical. Both other alternatives contain S² as a homotopy
retract, so they have nonzero π2 and are not aspherical. This proves the
asphericity criterion.

If K in this family is aspherical, then K=T, and every subcomplex of K is
aspherical componentwise. Indeed, a proper subcomplex cannot contain all
surface faces. Every nonempty proper collection of faces has an edge incident
to exactly one face in the collection: otherwise the collection would be a
union of components of the connected dual graph of T. That edge is a free
face in the subcomplex. Remove it together with its unique triangle and
repeat. All two-faces eventually disappear, leaving a graph. The whole
complex T is already aspherical.

This closes this particular family as a source of Whitehead counterexamples.
It is not a result for arbitrary graphs of maximum degree six, arbitrary
flag two-complexes, or general two-dimensional aspherical complexes.
