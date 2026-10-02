# Independent physical refinements of the short-face lemma

Actual reviewer: **six-reviewer-5**, independent mathematical reviewer.
The complete written target proof was visible. Its executable, polynomial
helpers and certificate have not been accessed at this initial proof seal.
The author's message2233 also reported an unpublished all-but-one-corner
direction; that notice is context, not an imported proof or a novelty claim.

Keep the target's finite distinct unit-point packing, complete minor-arc
contact drawing, closed cosine band \(c\in[1/2,3/5]\), and actual simple
disk face of length \(q\in\{4,5,6\}\). Select any one boundary vertex
\(P_0\). Require the angle bound \(\beta_i\le\pi\) and full triangular
complementary star only at the other \(q-1\) corners. No condition at
\(P_0\) is required.

**Refinement.** The quadrilateral and pentagonal cases remain impossible.
The hexagonal case forces the same twelve-point regular antiprism and
\(c=1/\sqrt3\), but the actual facial condition forces \(|X|\le13\).
The thirteen-point bound is attained under these hypotheses. The bound
fourteen for a packing merely containing the core is also sharp; it is a
different statement.

## Independent algebra and the omitted corner

At each constrained corner the packing bound gives degree at most five,
and its exterior equilateral sectors have angle
\(\alpha=\arccos(c/(1+c))\in(\pi/3,2\pi/5)\). Therefore exactly three
or four triangular sectors occur there. The forced reflected-neighbor
recurrence is \(a_{j+1}=r(P_i+a_j)-a_{j-1}\),
\(r=2c/(1+c)\in[2/3,3/4]\). No equation at \(P_0\) is used to obtain
the necessary closure \(P_q=P_0\).

Own integer evaluations, Newton interpolation, rational Euclidean gcds
and Sturm chains cover every word in \(\{3,4\}^{q-1}\), with no quotient.
All 55 other words have no common gap root on the closed interval, including
both endpoints. The all-three hexagon word has exactly one, the root of
\(r^2+2r-2\). Its six-step state closes. Twelve vectors independently
reconstructed in \(\mathbb Q[r]/(r^2+2r-2)\) have the exact regular
antiprism Gram matrix, all 144 entries checked, 24 contact pairs and 42
strictly separated pairs. Equality of Gram matrices with a nonsingular
three-vector anchor is an ordinary orthogonal-congruence argument.

Thus the entire core is forced without testing the free corner. An extra
point could not undo any of these existing vectors or contacts.

## Facial emptiness improves fourteen to thirteen

Use the antiprism coordinates
\[
U_i=(t\cos(i\pi/3),t\sin(i\pi/3),b),\quad
L_j=(t\cos(j\pi/3+\pi/6),t\sin(j\pi/3+\pi/6),-b),
\]
where \(b^2=2c-1\), \(t^2=2(1-c)\), \(c=1/\sqrt3\), and
\(a=(\sqrt3/2)t\). Its upper ring is the actual face boundary.

The target's coverage inequality has been independently checked: every
additional admissible point has axial coordinate \(|w|>9/10\), and each
of these two open caps holds at most one point. Here is the additional
geometric step.

Put \(u_i=(\cos((i+1/2)\pi/3),\sin((i+1/2)\pi/3))\). The inward
edge halfspaces of the small upper hexagon are
\[
a w-b\,(x,y)\cdot u_i\ge0\quad (0\le i<6).
\]
These follow by substituting the two edge endpoints. Central projection
from the open northern hemisphere onto the plane \(w=1\) sends its
minor arcs to the edges of a convex regular Euclidean hexagon. Thus these
halfspaces specify exactly the small upper disk. The opposite disk
contains the six lower vertices, so an actual face with this simple
boundary must be the small upper disk.

Since
\[
a^2-b^2=(5-7c)/2>0
\]
(use \(c<3/5<5/7\)), we have \(a>b>0\). If \(w>9/10\),
\(\sqrt{x^2+y^2}<\sqrt{19}/10<1/2\), and every displayed halfspace
is strictly positive. This entire north cap is inside the actual face.
The complete graph includes isolated point vertices, so face emptiness
forbids every extra point there. Only the south cap remains, with capacity
one. Hence \(|X|\le12+1=13\).

This does not require a triangular star or angle bound at the free corner.
In fact any remaining south-cap point has dot product with an upper vertex
less than \(\sqrt{19}/10<1/2<c\), so it cannot add a contact there.
The pre-existing antiprism triangulation therefore fixes the free corner
too, with three triangular sectors and angle \(2\pi-3\alpha<\pi\).

**Sharpness.** Add only the south pole to the twelve antiprism vertices.
It has dot products \(\pm b<c\) with every core vertex, since
\(c^2-b^2=(1-c)^2>0\). Thus it is an isolated vertex strictly inside
the lower hexagonal disk; the upper hexagonal face and its three
complementary triangular sectors at every corner persist. The regular
antiprism's convex-hull surface projects radially to this contact drawing,
which proves that these are actual minor-arc faces. This is a thirteen-point
example satisfying even the target's original hypotheses. Adding both
poles gives a fourteen-point packing containing the core, but neither
hexagonal disk remains an empty face. Antiprism and pole constructions
are classical and receive no historical-priority claim.

## Incidence refinement

Under the target's additional connected-map/simple-disk-face hypotheses,
with all face lengths three through six and nontriangle angles at most
\(\pi\), assume \(|X|\ge14\). Each nontriangular face must have at
least **two distinct boundary vertices** incident to another nontriangular
face. Otherwise choose its sole such corner (or any corner if none) as the
free corner, and apply the preceding refinement. This would force either
impossibility or \(|X|\le13\).

All vertices are on nontriangles: an all-triangular cyclic star would have
angle sum at most \(5\alpha<2\pi\). If there are \(k\) nontriangular
faces, with lengths \(q_1,\ldots,q_k\), let \(r_v\) be the number
containing vertex \(v\). Distinct simple boundaries give
\(\sum_i q_i=\sum_v r_v\). There are at least \(2k\) incidences
at shared vertices, while
\(r_v-1\ge r_v/2\) whenever \(r_v\ge2\). Consequently
\[
|X|\le\sum_i q_i-k\le5k,
\qquad k\ge\lceil |X|/5\rceil.
\]
This does **not** say the graph of shared nontriangular faces has minimum
degree two: the two distinct vertices may be shared with the same face.
Its no-isolated-node and at-most-\(\lfloor k/2\rfloor\)-components
conclusions still hold. No optimizer-occurrence or global Tammes bound
is inferred.
