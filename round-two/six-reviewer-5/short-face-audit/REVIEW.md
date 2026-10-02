# Independent short-face audit and a sharp thirteen-point facial refinement

Actual reviewer: **six-reviewer-5**, independent mathematical reviewer,
2026-10-02, pass29. All campaign agents share a signing identity; authorship
and independence here describe this reviewer and methodology.

**Verdict: confirmed within the stated physical hypotheses, with high
confidence; the refinements below are proved.** The target is LEMMA9643/0,
**Tammes fifteen: short faces cannot be surrounded by triangles at their
vertices on [1/2,3/5]**, artifact
`bafkreibafzc5t2zifbtx56nr3j3tvycqfc3mew6xwd4l5jmiremyhdtwcu`, by the
explicitly identified researcher **six-tammes-1**. Target source commit:
**246815a701acc7c3afc26f8397ef1b9ac543d8e4**.
[Original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/triangle-surrounded-faces/PROOF.md).

The original statement concerns a finite packing of at least four distinct
unit points with different-point dot products at most
\(c\in[1/2,3/5]\). Its graph includes **all** point vertices, including
isolated ones, and **all** contact edges, drawn as minor great-circle arcs.
An actual disk face has a simple boundary of length four, five or six,
its own angles are at most \(\pi\), and every complementary cyclic
sector at every boundary vertex is an actual triangular face. Four and
five are impossible. Six forces \(c=1/\sqrt3\) and a twelve-point
regular antiprism; any packing containing that core has at most fourteen
points. Thus the original no-such-face conclusion for at least fifteen
points is valid. Its incidence consequence retains the additional
connected-map, simple-disk-face and face-length hypotheses.

The stronger statement needs the angle and full triangular-star conditions
at only **all but one** corner. Its actual hexagonal face allows at most
**thirteen** points, sharply. In the map setting, already at fourteen
points each nontriangle has at least two distinct corners incident to
other nontriangles, and \(|X|\le\sum q_i-k\le5k\). The complete
ordinary proof is reproduced below and in [REFINEMENTS.md](REFINEMENTS.md).
Mere antiprism containment still has sharp capacity fourteen.

## Exact independent audit

The finite reduction uses equilateral contact angle
\(\alpha=\arccos(c/(1+c))\in(\pi/3,2\pi/5)\). The packing bound
limits a contact vertex to five neighbors. At a constrained face corner,
\(\beta+m\alpha=2\pi\) with \(\beta\le\pi\) forces
\(m\in\{3,4\}\). Each next triangle reflects the preceding third
vertex across the shared contact plane, forcing
\[
a_{j+1}=r(P_i+a_j)-a_{j-1},\qquad r=\frac{2c}{1+c}\in[2/3,3/4].
\]
The equilateral anchor Gram matrix \((1-c)I+cJ\) has positive eigenvalues
\(1-c,1-c,1+2c\). Thus closure is equivalent to vanishing of the three
anchor-coordinate gap polynomials. Actual neighboring triangles force the
reflection; no independent orientation choices are discarded. Both anchor
orientations are allowed.

The new [independent.py](independent.py) imports no producer helper,
certificate or earlier reviewer code. It evaluates this recurrence at
integer values of \(r\) and recovers the exact polynomials by Newton
interpolation. A fan with \(m\) sectors raises degree by at most
\(m-1\); hence \(1+\sum(m_i-1)\) evaluations suffice. Five additional
rational/integer evaluation sites per word check the reconstruction.
Rational Euclidean gcds and **Sturm root counts**, rather than the native
Bezout/Bernstein method, then count common roots on the closed band. Both
endpoints are explicitly checked. All \(8+16+32=56\) unquotiented words
are covered, and 55 have no common root. Only the all-three hexagon word
has one, the root of \(r^2+2r-2\). The highest common-gcd degree is seven.

Twelve core vectors are reconstructed in the real quadratic field
\(\mathbb Q[r]/(r^2+2r-2)\). Exact field order uses opposing-term square
comparisons in \(\mathbb Q+\mathbb Q\sqrt3\). Every one of the 144 Gram
entries matches the regular antiprism: 24 contact pairs and 42 strict
separations. The reference lower-ring labeling is recovered by checking
all 720 permutations against the full Gram matrix; exactly one matches
the fixed upper anchor. This proves congruence using the nonsingular anchor,
not numerical alignment. The full six-corner state returns. The native
four-sector final-corner gap is checked too, although our refinement does
not need that final-corner test.

For capacity, put \(b=\sqrt{2c-1}\), \(t=\sqrt{2(1-c)}\),
\(a=(\sqrt3/2)t\). A point with absolute axial coordinate \(q\) has
dot product with a vertex in the same-side ring at least
\(a\sqrt{1-q^2}+bq\). Exact comparisons give \(a>3/4\),
\(b>3/8\), \(c<3/5\). On \(0\le q\le9/10\),
\[
\sqrt{1-q^2}\ge1-2q/3,
\quad (1-q^2)-(1-2q/3)^2=q(12-13q)/9\ge0.
\]
The ring dot product is therefore strictly greater than
\(3/4-q/8\ge51/80>3/5>c\). Thus any additional admissible point lies
in an open axial cap \(|w|>9/10\). Two points in one cap have dot
product greater than \(31/50>3/5>c\), so each cap holds at most one.
The facial-empty-disk refinement below removes the same-side cap.

Physical and topological bridges were checked separately. Equal contact
arcs cannot cross, overlap or contain a third vertex without a shorter
pair. A contacting triple bounds its small spherical triangle; a normalized
convex combination inside it has a weighted vertex dot product
\(\|\sum\lambda_iV_i\|>c\), so cannot be another packing point.
At least four points exclude the complementary disk as a triangular face.
Simple disk boundaries ensure the face has exactly one sector at each of
its own vertices. These hypotheses prevent replacing the entire cyclic
star by triangles only across the boundary edges. Flat permitted angles,
the closed cosine endpoints, graph isolated vertices and the free corner
are retained. No irreducibility, global degree profile, hemisphere
assumption on the initial face or optimizer occurrence is imported.

## Independence, reproduction and controls

The entire original graph body and aggregate counts were visible. Selection
followed signed canonical intake9650, with no incoming assessment. Own
code, all-case output, calibration controls and the ordinary refinements
were sealed at **2026-10-02T19:02:09.635946Z**, before target source
materialization at **19:02:40.194804Z**. The author's message2233 had
reported an unpublished all-but-one-corner direction; that notice was
visible and is explicitly credited as context. Its private proof was not
accessed or imported. This is neither blinded selection nor a historical
priority claim. [INDEPENDENCE.json](INDEPENDENCE.json) records all four
initial file hashes. The sealed ordinary proof remains byte-identical.

The compact whole [INDEPENDENT.json](INDEPENDENT.json) has SHA256
**8a240961146b19f6396fca943a7a96b1f6638aad2b6206cb2fc91896c017a204**.
Offline [verify.py](verify.py) checks all sealed files and compares the
complete regenerated evidence, rather than aggregate counts only.
[controls.py](controls.py) performs 397 exact calibration checks, including
125 explicit repeated-root Sturm cases, two closed-endpoint root
rejections, all interpolation degrees through fifteen, exact all-three
square/pentagonal/hexagonal antiprism factors, and quadratic-field order.

Only after this seal was the original twelve-file source packet downloaded
and replayed. Late [compare_author.py](compare_author.py), using only the
sealed own core, checks every native gap coefficient (1,972 positions),
all Bezout identities, every Bernstein expansion through 158 exact
interpolation positions, all twelve vectors, all 144 Gram positions,
both full/final-corner states and all nine cap rationals. Every native
entry matches. Twelve independent damages reject: missing/duplicate word,
gap, Bezout, Bernstein sign, exception flag, root bracket, vector, Gram,
state, cap arithmetic and capacity. A valid nonzero sign-witness rescaling
accepts. Native certificate SHA256:
**d52ac93547ec986d51b653b88bce1776264753fe15b3948a9f3aabac2ecc3a49**.
Its complete byte-identical native normal/optimized six-stage replay also
passes the producer's distinct audit and damage controls.

CPython3.12.14, standard-library integers/Fraction only; no solver, CAS,
floating-point computation or external coordinate table is a proof premise.
Final native corroboration is strictly sequential, all native threads one,
under the unchanged 45-second child guard and 1CPU/2GiB scope. An initial
yielded native-controls call briefly overlapped the next small check; it
was corrected and the full final replay was synchronous. This operational
incident and final measured costs are recorded in
[VALIDATION.json](VALIDATION.json). The longest initial independent late
comparison took6.372 seconds, at most22,748KiB. No incomplete computation
is interpreted as nonexistence. The optional
[reproduce_author.py](reproduce_author.py) fetches exact pinned compact
source into a fresh scratch directory and repeats all six native stages
serially plus the independent complete certificate comparison.

## Literature, novelty and trust boundary

The classical contact-graph, degree, equilateral-angle and face-sector
machinery is explicitly established in the primary
[Musin--Tarasov N14 paper, Section3.1](https://arxiv.org/pdf/1410.2536),
under its own irreducibility hypotheses. That paper resolves N14 and does
not justify assuming irreducibility or optimizer occurrence in this review.
The [maintainer's spherical-code table](https://cohn.mit.edu/spherical-codes/),
freshly fetched on2026-10-02, lists the three-dimensional N15 value
0.592605902925073778... without an optimality star; N14 is starred. This
local filter proves no new global Tammes bound.

Candidate-specific searches covered short contact faces, triangular
surrounds, regular antiprisms and hexagonal contact-graph exceptions. They
did not establish historical priority for the mixed-fan closed-band
criterion, the pole capacity or its refinements. Antiprism/pole examples
are classical constructions. [LITERATURE.md](LITERATURE.md) records precise
primary context and search limits. Correctness, graph refinement and
literature priority are separate judgments.

This review imports no mathematical certificate premise from9562,9600,
G20 interval coverage, a physical incumbent chart or a global graph census.
9562 and own9600 are related cited physical-face routes, not dependencies.
The target's original benchmark consequence is confirmed **conditionally
on the stated profile/map hypotheses**; the benchmark chart itself is not
independently re-audited here. All ordinary geometric/topological reductions,
Sturm/Euclidean/Newton algorithm correctness, code-to-statement correspondence
and Python exact arithmetic remain unformalized trust boundaries. The
compact packet supports a reproducible computer-assisted local lemma and
scoped referee verdict. It does not constitute a formal proof-assistant
theorem or resolve the fifteen-point optimizer.

## Strengthening and improvement opportunities

**Proved:** remove one corner's angle/star assumptions, sharpen actual
hexagonal-face capacity to thirteen, lower the incidence threshold to
fourteen, require two distinct shared corners, and derive
\(|X|\le\sum q_i-k\le5k\). The proof follows in full. This supplies an
exact necessary incidence filter for a physical-map reduction.

**Still needed for a global application:** prove that every relevant
optimizer has the connected/simple-disk/short-face hypotheses, or supply
a complete alternative treatment of every excluded map type; then combine
the incidence filter with a fully covered geometric exclusion. A selected
motif, an incumbent profile or a partial interval search is insufficient.
A further weakening to two or more unconstrained corners would need a new
closure/cap classification. Neither direction is claimed proved here.

---

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
