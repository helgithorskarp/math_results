# Parallel branches and a cyclic mass median

All graphs are finite and simple. Edge lengths are positive real numbers;
vertex masses are nonnegative real numbers. A geodesic is a simple shortest
path in the original graph. A singleton is an allowed geodesic.

Let a and b be distinct vertices. Let P_0,...,P_(r-1) be distinct a-b paths
with pairwise disjoint interiors, and let H be their union. For a vertex x
of P_i write t_i(x) for its length-coordinate from a and L_i for the whole
length of P_i. In particular, t_i(a)=0 and t_i(b)=L_i.

## 1. Any two branches have a two-geodesic cover

For each branch define its a-half to contain the vertices with
t_i(x) <= L_i/2 and its b-half to contain those with t_i(x) >= L_i/2.
More precisely, use the prefix ending at the last vertex at or before
L_i/2, and the suffix starting at the first vertex at or after L_i/2.
These two subpaths cover every vertex of P_i: if the midpoint is in an
edge interior, the two endpoints of that edge belong to opposite halves;
if it is a vertex, that vertex belongs to both. No new subdivision vertex
is introduced at the midpoint.

Take distinct i,j. Reverse the a-half of P_i and concatenate it with the
a-half of P_j, identifying their common endpoint a. This is a simple path
Q_a; positive lengths imply that neither prefix reaches b. Construct Q_b
analogously from the two b-halves through b. Their vertex union is exactly
V(P_i) union V(P_j).

To prove Q_a shortest in H, let its endpoints be x in P_i and y in P_j,
with coordinates s <= L_i/2 and t <= L_j/2. Any x-y path must leave the
interior of P_i through a or b and enter the interior of P_j through a or
b. The first required segment has length at least

    min(s, L_i-s) = s,

and the last required segment has length at least

    min(t, L_j-t) = t.

The intervening segment has nonnegative length. These segments are
disjoint along a simple path, so every x-y path has length at least s+t.
Q_a has exactly that length. The same proof applies if an endpoint is a
(its required segment has length zero). Reversing the roles of a and b
proves Q_b shortest. If both endpoints of Q_a coincide at a, Q_a is simply
the singleton a, and similarly for b.

Consequently **any two full branches are covered by two H-geodesics**,
even when neither full branch is an H-geodesic. If H preserves distances
in a larger graph G, both constructed paths are also G-geodesics.

## 2. Planarity supplies the cyclic separation property

Now suppose G is planar and every positive-mass vertex lies in H. Fix a
plane embedding of G. For r>=3, the interiors of the branches occur in a cyclic order around
the two poles; consecutive branches bound the faces of H. Relabel them
P_0,...,P_(r-1) in that order. Two selected branches form a simple closed
curve. By the Jordan curve theorem, the remaining branches in one open
cyclic interval lie on one side of this curve, and those in the other
interval lie on the other side. A G-path avoiding the selected branch
vertices cannot cross the curve: its edges cannot cross H-edges, and any
intersection at an H-vertex on the curve would be a deleted vertex.

Deleting two entire branches therefore leaves each remaining component's
H-vertices within one of the two open cyclic intervals of surviving
branches. Vertices outside H have zero mass and do not change these mass
bounds. In the spanning case, this support condition holds for every mass
assignment. The branches need not have equal numbers of vertices or
comparable metric lengths.

For r=2, Part 1 covers every positive-mass vertex outright. For r=1, H is
a path; distance preservation makes that entire path a G-geodesic. These
cases already give the claimed conclusion.

## 3. Select two branches by their masses

Assume r>=3. Let A_i be the total mass of the internal vertices of P_i,
and let M=sum_i A_i. The masses of a and b will both be deleted.

If M=0, choose any two distinct branches. If A_0>=M/2, choose P_0 and any
other branch: after their deletion the total remaining mass is at most
M/2. Otherwise let j>=1 be the first index such that

    A_0 + ... + A_j >= M/2.

It exists since A_0<M/2 and the full sum is M. The mass on branches
P_1,...,P_(j-1) is less than M/2, while the mass on
P_(j+1),...,P_(r-1) is at most M/2. By Part 2, deleting P_0 and P_j leaves
every component with mass at most M/2. Since M is at most the original
total mass, this is exact half balance relative to the original graph.

Part 1 supplies two G-geodesics whose vertex union is precisely those
two branches. Hence their union is the required separator. This proves
the theorem for all nonnegative real masses, including zero masses and
all equality cases, and for arbitrary positive real edge lengths
satisfying the distance-preservation hypothesis.

## 4. What this excludes, and what it does not

When H is spanning, if every edge e=uv outside H has length at least
d_H(u,v), H preserves the entire G-metric by edge replacement. Conversely, if H preserves that
metric, d_H(u,v)=d_G(u,v)<=length(e). Thus this edgewise condition is exact.
It can be used either as a family definition or as a finite certificate
for an explicitly constructed metric. Added edges continue to count for
separator connectivity; none are deleted from G during the argument.

The midpoint cover alone uses no planarity. For at most four branches it
also gives half balance without planarity: deleting the two heaviest
branch interiors removes at least half of their total mass, and the pole
masses are deleted as well. For arbitrarily many branches we use the
planar cyclic separation property above.

Putting positive mass on metric leaves inside the faces changes the problem.
Their vertices are not on any of the core branches, and their incident edges
in G can connect them to several branches even if only one attachment is
cheap. They cannot simply be assigned to a branch for the median proof:
deleting that branch need not delete or isolate those vertices. The
20-vertex finite control in verify.py has nine such vertices, three in
each face of a three-branch core. Deleting any two full core branches
leaves six marked vertices in one component. Each component is measured
in the full graph, including its expensive edges. An explicit ambient
geodesic pair still half-balances this graph, so the control refutes only
that naive extension of the branch-deletion construction.

No assertion is made here for a theta core with general attached trees,
for every planar graph of a given geodesic-support cycle rank, or for
all edge-length assignments on a capped cylinder.
