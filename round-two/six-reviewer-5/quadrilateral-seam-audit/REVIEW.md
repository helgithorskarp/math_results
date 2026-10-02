# Independent quadrilateral seam audit and a stronger one-vertex filter

Actual reviewer **six-reviewer-5**, role **independent mathematical reviewer**.

**Verdict: LEMMA9741 A–C is confirmed with high confidence in its stated
physical scope.** Target
`bafkreibaj24wtmx7r52pdvwbgjgfq7qszk7vi3wiupnukvgb6ebn6tmhse`,
by six-tammes-1, researcher, source **acab131cba3ea2893d647ff717c7706b6cb8ce81**.
The [complete original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/annulus-rhombus-obstruction/PROOF.md)
and its seven outgoing directions were inspected; no incoming assessment
was present at the initial signed committed cursor9757.

This review also proves a simpler, stronger local result: **an actual full
TQQ star forces \(c<1/\sqrt5\)**. Thus the local prohibition holds for
\(1/\sqrt5\le c<1\), including its lower endpoint, and removes every
second-endpoint assumption. This is a campaign refinement and an immediate
consequence of classical rhombus angle bounds; historical priority and a
physically sharp threshold are not claimed.

## Exact scope and dependencies

Let \(X\subset S^2\) have at least four distinct unit points and
\(x\cdot y\le c\) for every distinct pair, \(0<c<1\). Include ALL
points and ALL pairs of product exactly \(c\) in the contact drawing,
using minor great-circle arcs. A TQQ star means the entire cyclic star at
one vertex consists of exactly one actual triangular disk face and two
distinct actual quadrilateral disk faces, each with four distinct boundary
vertices and a geodesically convex closure in an open hemisphere.

The new local result requires those conditions only. It needs no hypothesis
at any second vertex, global connectedness, minimum contact degree, prescribed
total face counts, irreducibility or optimizer status. The complete contact
drawing and actual quadrilateral faces are essential to the strict endpoint.

The connectedness verdict retains ALL target map hypotheses: \(|X|=15\),
connected complete contact graph, minimum contact degree3, every face a
simple disk of length3–5, every nontriangle convex and hemispheric, and face
counts T11/Q3/P3. It holds on the original closed \([1/2,3/5]\) band and
the expanded closed \([9/20,19/31]\) band. Point coverage, the disconnected
two-annulus decomposition and cap stars are imported explicitly from
LEMMA9681 and this reviewer's earlier REVIEW9717. They are already sufficiently
reviewed; their large parent proof is not presented as a new independent audit.
The new local threshold does **not** extend the connectedness band below9/20.

No G20/G22 occurrence, optimizer coverage, three-addition capacity argument,
full contact-map enumeration, new global upper bound or Tammes15 optimality
follows. LEMMA9727's separate twelve-point triangle-support argument is
context only and is not reviewed or assumed. LEMMA9562's connected-case
facial interface remains a separate scoped result.

## Ordinary proof of the stronger local filter

Put \(d=\arccos c\) and \(\alpha=\arccos(c/(1+c))\).
The contact arcs embed: a crossing, overlapping arc, or interior point vertex
would force a shorter pair. The contact-triple Gram matrix \((1-c)I+cJ\)
shows that a normalized nonnegative combination of the three vertices has
some product greater than \(c\): the weighted mean is at least
\(\sqrt{(1+2c)/3}>c\). Therefore the small triangle has no other point.
With at least four points its complementary disk is not a face. Each actual
triangular face has angle \(\alpha\in(\pi/3,\pi/2)\).

A convex hemispheric equilateral quadrilateral has no zero or flat corner.
A zero corner identifies its two neighbors. If a corner at \(A\) were flat,
its neighbors \(D,E\) would satisfy \(D+E=2cA\); their other common
contact vertex \(C\) would have \(C\cdot A=1\), contradicting distinctness.
Its minor diagonals consequently lie in its interior. A diagonal cannot be
a contact, since the complete contact graph would then split the face.

For any quadrilateral angle \(b\), the neighboring boundary vertices have
product \(c^2+(1-c^2)\cos b<c\). Hence **\(b>\alpha\)**, strictly.
The classical spherical-rhombus identity is
\[
\cot(a/2)\cot(b/2)=c
\]
for adjacent angles. Reflection across the plane of a diagonal pairs the
two remaining contact-plane solutions; the convex diagonal splits the
rhombus into congruent isosceles triangles. The angle cosine law gives the
identity with all divided quantities positive. These steps justify its use
here without importing irreducibility or optimizer coverage.

At a full TQQ star, let \(a_1,a_2\) be the quadrilateral angles and
choose an adjacent angle \(b_i\) in each face. Set
\[
A=\cot(\alpha/2)=\sqrt{1+2c},\qquad
x=\cot(a_1/2)>c/A,\quad y=\cot(a_2/2)>c/A.
\]
The strict bounds use \(b_i>\alpha\) and the rhombus identity. The full
star gives \(a_1+a_2=2\pi-\alpha\), so cotangent addition yields
\[
1=xy+A(x+y)>\frac{c^2}{1+2c}+2c.
\]
Clearing the positive denominator proves \(5c^2<1\). Since
\((9/20)^2-1/5=1/400\), this proves target Lemma A throughout its entire
band after dropping its second-endpoint requirement.

Equivalently, the classical strict actual-face bound
\(\alpha<b<2\alpha\) gives a TQQ star sum less than \(5\alpha\).
For \(c\ge1/\sqrt5\), \(\alpha\le2\pi/5\), which is incompatible
with a full star of sum \(2\pi\). The cotangent proof above accounts for
the boundary using only rational algebra and the strict diagonal bridge.

## Annulus seams and connectedness

Import the parent facts precisely: disconnection consists of two disjoint
three-face annuli containing all point vertices; each pair of faces in
one annulus shares a full edge, with pairwise disjoint seam endpoint sets and no
triple intersection. The complementary regions are two disk caps and a
middle annulus, with no interior point vertices. Each annulus borders one
cap. Its boundary has three mixed vertices; at every mixed cap vertex the
full star has exactly its two nontriangles and one actual triangle.

Orient all three faces coherently. Normalize the incoming edge to \((0,1)\)
and the outgoing one to \((k,k+1)\), where
\(q\in\{4,5\}\), \(2\le k\le q-2\). Orientation reverses on gluing.
The unglued paths \(1\to\cdots\to k\) and
\(k+1\to\cdots\to q-1\to0\) connect within their respective tracks
around the three faces. They form the two boundary cycles, and each seam
has one endpoint on each cycle. No further vertex identifications are
permitted by the imported parent equality. This proves the bridge for
every case; a count alone would not suffice.

The full literal domain has three typed-port choices per face and thus
\(3^3=27\) cases without a symmetry quotient. Our credited owned dart
successor algorithm checks every quotient class, external successor, both
complete cycles and all81 endpoint-to-boundary assignments.

If one annulus contained two Qs, their seam's cap endpoint would have full
TQQ star, now impossible. Each annulus therefore contains at most one Q;
two annuli cannot contain Q3. This excludes both QQQ+PPP and QQP+QPP for
every degree profile in the explicit cohort. The argument and all parent
premises hold on both closed bands. Every point belongs to a nontriangle
by the credited parent, establishing the target's coverage conclusion.

## Independent computation and late native comparison

[PROOF.md](PROOF.md), [audit.py](audit.py), the whole [EVIDENCE.json](EVIDENCE.json)
and the two owned helpers were sealed at **2026-10-02T21:38:39.614647+00:00**.
Target executable/certificate materialization completed later at
**2026-10-02T21:39:04.746897+00:00**. The defining proof and counts were
visible, so this is not blind discovery. Shared signing identity does not
establish distinct authorship.

The polynomial kernel and annulus implementation are copied unchanged from
OWNED REVIEW9717, source **6d18f12a3c56925073e71bf1ad6855f334f35e16**.
The kernel's earlier provenance is OWNED REVIEW9663, source
**84b336a5009d8f3c9940e08dc56faeb7e22997ba**. These methods and input bytes
are credited. The new scaled cotangent elimination, one-vertex proof and
81 seam membership bindings are new review work. No other reviewer's or
target helper enters the primary computation.

The three original \(t=1,2,3\) cases are independently reconstructed with
\(U=(x+y)/A\) and rational \(B_t/A\), avoiding square-root arithmetic.
Exact degree-bounded interpolation after clearing denominators produces all
degree2/3/4 discriminant polynomials. Complete rational Bernstein coefficient
lists are strictly negative on the closed algebraic interval \([9/20,1]\).
Physical \(c=1\) remains excluded. [compare_author.py](compare_author.py)
compares all15 complete rational fields by degree-bounded cross-product
identities, all46 relevant coefficient positions, all216 quotient classes,
all216 directed boundary arcs, both cycles in every case, every seam,
all54 mixed-corner counts, all36 prism Gram entries, every named prism
contact and the full alternative adjacent-angle factorization. No target
executable is imported in that comparison.

All six original native stages—producer, auditor and controls, each normal
and optimized—passed strictly serially. The complete original16166-byte
certificate regenerated with SHA256
`308b6a783ffa4b0ec739db4b7598ff9d12605109daa8b3419739b77d5fa5a7b6`.
All23 native semantic damages reject and five valid representations accept.
Our own ten semantic damages reject in both modes and a noncanonical record
order accepts. [comparison.json](comparison.json) and [VALIDATION.json](VALIDATION.json)
record full agreement and costs. Controls, comparison and replay adapters
were written after the primary seal and are labelled accordingly.

The whole own evidence is25825bytes, SHA256
`f3704fd4904205d84b32a11814361dee7d12153df0ac65ce27a71756d7a549b5`.
CPython3.12.14, standard-library integer/Fraction arithmetic only; no solver,
floating-point claim, omitted large corpus or incomplete enumeration is a
proof premise. Native threads1, one mathematical child at a time, unchanged
45-second guards and the existing1CPU/2GiB process scope. Our primary normal
and optimized checks took0.101/0.232seconds; all native stages were below
0.395seconds, cumulative observed peak21384KiB. The parent corpus was not
rerun; its stated theorem and already sufficient prior review are explicit
logical imports. All spherical, strict-diagonal, subsurface/cap and
finite-to-physical bridges remain **ordinary unformalized mathematics**.

## Strengthening and improvement opportunities

**Proved:** the one-vertex \(c<1/\sqrt5\) necessary condition removes all
second-endpoint star assumptions and modestly widens the local prohibition's
lower range. It shortens the connectedness proof; the connectedness cohort
and its wider parent band stay the same. This is a direct use of classical
rhombus bounds, not a new global Tammes theorem or a priority assertion.

**Endpoint control:** at \(c=1/\sqrt5\), a center and five equally spaced
latitude points form a complete icosahedral wheel with ten contacts and five
actual triangles. Deleting two radial contacts merges triangle pairs into
fake convex hemispheric quadrilaterals and produces TQQ in an incomplete
drawing. Those deleted contacts are precisely the fake diagonals. The
ordinary exact coordinate proof is in PROOF.md; the six-point Gram and
whole contact set are recorded in EVIDENCE. This is a hypothesis control,
not a counterexample to the new lemma or a proof of sharpness. The classical
\(c=1/7\) triangular prism supplies a valid actual TQQ control below the
new range. Neither construction is claimed new.

**Next consequential frontier:** prove enough optimizer coverage to enter
the explicit cohort, or force the required contact pattern in its connected
case. Such a bridge must keep actual faces, completeness and injectivity;
connected incidence alone does not imply G20/G22 occurrence. A lower
connectedness band would need a new parent proof: near the local threshold,
the parent's strict five-triangle angle exclusion no longer follows merely
from the present interval argument. These opportunities remain unproved.

## Primary literature and publication readiness

[Musin–Tarasov, Proposition4.1](https://arxiv.org/pdf/1312.5450)
records the classical spherical-rhombus identity; its Section4.2 also uses
quadrilateral angle bounds. Their irreducible-graph setting is credited;
this review proves the particular bridges needed under its explicit face
hypotheses. The one-vertex consequence is not claimed historically new.
[Bezdek–Reid, Lemma4](https://arxiv.org/pdf/1210.5756) supplies related
quadrilateral sealed-star filters at \(c=1/2\). Those are relevant classical
prior art, not premises for this new review's computation.

The [maintained spherical-code table](https://cohn.mit.edu/spherical-codes/)
was fetched live2026-10-02; its dimension3/N15 candidate row remains unstarred
at cosine0.59260590292507377809642492233276. The
[primary coordinates](https://spherical-codes.org/data/3/15) were also fetched.
Neither source is an input or optimality certificate. Targeted exact-constant
and local-face searches do not establish historical priority or the absence
of a later global theorem. The known [N14 result](https://arxiv.org/abs/1410.2536) is credited separately.

The packet is reproducible and ready as a scoped independent audit and local
refinement, with ordinary proof trust boundaries stated. Publication of the
source and a confirming graph review does not resolve unrestricted Tammes15.
