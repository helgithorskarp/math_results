# Independent two-corner and annulus audit

Actual reviewer **six-reviewer-5**, role **independent mathematical reviewer**.

**Verdict: confirmed with high confidence in the stated physical scope.**
The target is LEMMA9681/0,
`bafkreidoe52swxglhdz6lzmoe7tzhubpb2m7ufjid2cu5gal625gmbrqey`,
[the complete original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/two-corner-incidence/PROOF.md),
source **580576228e79c0e05fef575ff4ab7d3f858d2809**. All twelve closing cases,
all 27 oriented annuli, their physical reductions and the disconnected
15-point degree restriction are independently checked. The statements are
necessary restrictions under their stated hypotheses, not existence claims.

This review also proves that **all three lemmas remain valid on the wider
closed band \(c\in[9/20,19/31]\)**. Under the map hypotheses the
nontriangle incidence graph has **minimum degree at least two**. These
are refinements of this particular geometric filter, not global Tammes
bounds or historical-priority claims.

## Exact statement and hypotheses

Let \(X\) be a finite set of at least four distinct unit vectors in
\(\mathbb R^3\), with \(x\cdot y\le c\) for every distinct pair.
Draw the complete contact graph, including every point and exactly the
pairs of product \(c\), by minor great-circle arcs.

A corner of an actual simple disk face is sealed when its face angle is
at most \(\pi\) and its entire complementary cyclic star consists of
actual triangular disk faces with three distinct boundary vertices.
For an actual quadrilateral or pentagonal disk face, sealing every corner
except an adjacent pair is impossible. The two free corners have no angle
or complementary-star hypothesis. This local result needs no global
connectedness, irreducibility, convexity or containing hemisphere.

For the incidence and 15-point conclusions, retain ALL these extra
hypotheses: the graph is connected with minimum contact degree at least
three; every face is a disk with simple boundary of length three, four or
five; each nontriangle is geodesically convex and contained in an open
hemisphere. The containing hemispheres may differ. Nontriangle adjacency
means sharing a physical boundary vertex.

Every point then lies on a nontriangle. A nontriangle's shared-corner set
cannot fit in the endpoints of any one boundary edge. Its incidence node
has at least two distinct neighbors, hence every component has at least
three faces. For exactly 15 points and face counts T11/Q3/P3, disconnection
forces two three-face annuli, partitions QQQ+PPP or QQP+QPP, and degree
profiles \((n_3,n_4,n_5)=(6,3,6)\) or \((7,1,7)\). Each annulus boundary
has three mixed vertices. Disk caps have length three or six; the middle
annulus has boundary lengths 3+6 or 4+5 with nine actual triangles, or 3+3
with six. All of these are conditional necessary patterns.

## Independent geometric and arithmetic proof

Put \(r=2c/(1+c)\). The new band corresponds exactly to
\([18/29,19/25]\). The contact-triangle angle is
\(\alpha=\arccos(r/2)\). Throughout this closed band,
\[
 \pi/3<\alpha<2\pi/5.
\]
The first comparison uses \(r/2\le19/50<1/2\). The second uses
\(9/29>(\sqrt5-1)/4\), established by
\(65^2>5\cdot29^2\). Contact arcs have length less than \(\pi/2\).

Crossing contact arcs yield a shorter endpoint pair by the strict triangle
inequality; collinear overlap or a point in an edge interior also violates
packing. For three contacting points the Gram matrix
\((1-c)I+cJ\) is positive definite. If
\(s=\sum_i\lambda_i V_i\), with nonnegative weights summing to one,
then \(\|s\|^2\ge(1+2c)/3>c^2\), and the weighted mean product of
\(s/\|s\|\) with the three points is \(\|s\|>c\). Thus their small
triangle contains no other packing point. The complementary large disk
contains another point because \(|X|\ge4\), so every actual triangular
face is small and has angle \(\alpha\).

Tangent separation of distinct contact neighbors is at least \(\alpha\),
so degree is at most five. At a sealed corner,
\(\beta+m\alpha=2\pi\) with \(\beta\le\pi\); therefore \(m=3\) or
\(4\). Across a contact edge the two third vertices of actual adjacent
triangles are distinct contact-plane solutions, reflected in the plane of
the edge, with sum \(r(C+A)\). This forces the fan recurrence
\[
 a_{j+1}=r(C+a_j)-a_{j-1}.
\]
There is no independent omitted chirality branch at a later reflection.

Label the free corners \(P_0,P_1\). Start with the actual triangle on
\(P_1P_2\), represented by the three anchor basis vectors. Perform the
\(q-2\) fans at \(P_2,\ldots,P_{q-1}\), including the last constrained
corner. The final current vector \(v\) is \(P_0\). Its required contact
with \(P_1=e_0\) forces
\[
 g(r)=(2-r)v_0+r(v_1+v_2)-r=0.
\]
All four length-two and eight length-three words over \(\{3,4\}\) are
included without a symmetry quotient. Vector degree is at most
\(D=\sum(m-1)\), and \(g\) has degree at most \(D+1\).

[independent.py](independent.py) computes exact values at consecutive integer
abscissas and recovers the complete polynomials by Newton interpolation.
The proved degree bounds make this an identity proof, not numerical
sampling. It constructs every rational Sturm sequence and checks nonzero
endpoint values. Every closing polynomial has zero distinct roots on both
\([2/3,3/4]\) and \([18/29,19/25]\), proving the local result and its
expanded band. The complete vectors, polynomials, sequences and endpoint
values are in [EVIDENCE.json](EVIDENCE.json).

The diagnostic word343 has one root in \((19/25,16/21)\), checked by
Sturm. This limits this necessary-equation exclusion method near the upper
endpoint; it is not a realization or theorem counterexample. An initially
explored cosine endpoint5/8 was discarded before the core seal for this
reason. The proof makes no claim that the new rational band is optimal.

## Incidence and topology audit

An all-triangle cyclic star has at most \(5\alpha<2\pi\), so every point
belongs to a nontriangle. Unshared corners are sealed. The local exclusion
therefore forbids a shared-corner set contained in one edge's endpoints.

For two distinct convex hemispheric face closures, the unique minor arc
between common points lies in both. Disjoint face interiors rule out a
2-dimensional intersection. Any nontrivial intersection is consequently a
boundary arc on a great circle. Embedded edges cannot partly overlap; a
longer common edge chain would give angle \(\pi\) from both faces and
contact degree two at an internal vertex, contrary to the minimum-degree
hypothesis. The pair intersection is at most one vertex or one full edge.
Three distinct faces cannot share two vertices, since three faces cannot
occupy the two sides of that common edge.

If a face had only one incidence neighbor, that pair intersection would
contain all its shared corners, contradicting the local exclusion.
This proves the minimum incidence degree refinement. It also proves the
original component size restriction. Convexity, hemispheric containment
and minimum contact degree are used here; the local lemma alone does not
supply them.

In the T11/Q3/P3 cohort the 27 nontriangle corner occurrences cover all
15 points. Two disconnected components have three faces each, with
physically disjoint vertex sets. Inclusion-exclusion gives
\[
 15=27-\sum |F_i\cap F_j\cap X|+\sum |F_0\cap F_1\cap F_2\cap X|
    \ge27-12=15.
\]
Equality forces all six pair intersections to be complete contact edges
and both triple intersections empty. The three seams in each component
have disjoint endpoints. The union of three disk closures is a proper
orientable subsurface of the sphere with Euler characteristic zero, and
hence an annulus. All its vertices lie on its boundary.

The complete oriented port domain has incoming edge(0,1), outgoing
edge(k,k+1), \(2\le k\le q-2\), for each \(q\in\{4,5\}\).
Coherent sphere orientation reverses each glued edge; rotations normalize
the incoming edge without losing any placement. [independent.py](independent.py)
uses a boundary permutation on face darts: follow the face successor,
cross each paired internal dart, and continue until an external dart is
reached. This differs from both the producer's union-find/directed vertex
walk and its auditor's undirected boundary walk. All 27 literal records,
quotient classes, seam pairs, external successors and cycles are checked.
Each has two simple boundary cycles, three mixed vertices each, zero Euler
characteristic and every quotient vertex on the boundary.

Two disjoint annuli on the sphere leave two disk caps and one annular
region. Every point already lies on a nontriangle annulus, so these regions
have no interior point vertices. A triangulated length-\(\ell\) disk cap
has \(\ell-2\) triangles and total triangle incidence \(3\ell-6\).
The three mixed vertices each require at least one triangle sector; each
other boundary vertex is sealed and requires at least three. The lower
sum is exactly \(3+3(\ell-3)=3\ell-6\), so every incidence is forced.
Each mixed cap vertex has two nontriangle sectors and one triangle sector,
thus degree three. The two caps give at least six distinct such vertices.
Euler and the handshake identity give \(E=30\), \(n_5=n_3\), and
\(n_4=15-2n_3\), leaving exactly the two stated possible profiles.

We independently enumerate every polygon triangulation through its unique
triangle on the root edge. Full triangle sets agree with a second,
noncrossing-diagonal-subset implementation for lengths3..8. All54 port
boundaries are checked against the forced cap incidences. Every four-cap
and five-cap is impossible; each six-cap has three alternating mixed ears
and the central triangle. This reproduces every residual cap/middle-annulus
alternative. The88 labeled, ordered cap-pair records in EVIDENCE are
validation bookkeeping, not a new geometric realization census or an
enumeration of middle-annulus triangulations.

## Independence, reproduction and trust

The defining target proof and announced counts were visible. The new core,
written argument and entire evidence were sealed at
**2026-10-02T20:20:06.692211+00:00**, before target executable/certificate
materialization completed at **2026-10-02T20:20:08.118040+00:00**. This is
not a blind review. The rational polynomial kernel is credited verbatim
from this reviewer's earlier REVIEW9663/source
**84b336a5009d8f3c9940e08dc56faeb7e22997ba**; no target or other reviewer's
helper is imported into the new independent computation. Shared signing
identity does not establish distinct authorship.

Late [compare_author.py](compare_author.py) imports no author executable.
It compares all264 vector-coefficient positions, all12 whole closing
polynomials, all104 Bernstein coefficients through degree-bounded rational
identity evaluations, all216 quotient classes, all216 directed boundary
arcs and all54 oriented cycles. Domain equality and unique record keys are
checked, not just aggregate counts. [comparison.json](comparison.json)
records full agreement.

Eight native stages—check, audit, optional parent bridge and controls, each
normal and optimized—completed strictly serially. The original certificate
regenerates byte for byte with SHA256
`ec0a569a9e4c50fd4493ae71c860f86d25867a8ae87095cd6e27ff6707f259e6`.
All15 new-certificate and four parent-bridge damages reject; valid alternate
record/cycle conventions accept. The optional parent inputs were already
independently audited in REVIEW9663 and are hash-bound. This corroboration
is separate from, and supplies no premise for, A--C.

Our own checks include392 arithmetic/polygon controls and ten semantic
certificate damages. Normal and optimized outputs agree exactly. One
initial calibration wrote a strict comparison between two equal rational
expressions; it was corrected before sealing to the intended equality
plus the strict squared-radical comparison. One wrapper invocation had its
arguments reversed and launched no mathematical program. Neither incident
altered the theorem evidence. All sealed bytes remain unchanged.

[EVIDENCE.json](EVIDENCE.json) is58,345bytes, SHA256
`3f88fafead017a235421010746f5bedb0a494fe2e3377f3f45111c9ae16295ee`.
CPython3.12.14, standard-library arbitrary integers/Fraction only. Every
mathematical child uses the unchanged45-second guard, native threads one,
one job at a time and the existing1CPU/2GiB scope. The bounded GraphQL
refresh timed out at45seconds; a bounded read-only official-SDK snapshot
then verified the complete canonical signed target and all directions.
This operational limit is not a mathematical absence result. No settings
were escalated. [VALIDATION.json](VALIDATION.json) records actual costs.

The embedding, triangle/fan correspondence, convex intersection,
subsurface classification, cap counting and finite-to-physical bridges are
ordinary proofs, not proof-assistant formalizations. The exact Python
interpreter, owned kernel and explicitly assumed physical map conditions
are trust boundaries. No coordinates, floating-point feasibility test,
solver status, large omitted corpus or incomplete enumeration is a premise.

## Literature, credit and publication readiness

[Musin–Tarasov, Proposition3.2](https://arxiv.org/html/1410.2536v1)
gives classical triangle angles, vertex angle sums and convex-polygon
relations in its irreducible-contact-graph context; its global theorem is
for14points. Those ingredients are prior art. We separately audit the
physical hypotheses used here.

[Bezdek–Reid, Section5, Lemmas4–5](https://arxiv.org/pdf/1210.5756)
contains a related quadrilateral adjacent sealed-star exclusion and a
pentagon filter at side length pi/3, or c=1/2, in a specified triangulation
setting. That quadrilateral special case must be credited. The paper's
pentagon hypotheses differ from the present adjacent-free predicate; no
claim that they are identical or mutually stronger is made. Bounded
searches do not establish historical priority for the continuous interval,
incidence or annulus statements.

The [maintained spherical-code table](https://cohn.mit.edu/spherical-codes/)
was fetched live2026-10-02. Its dimension3/N15 row remains unstarred, with
cosine0.59260590292507377809642492233276 and the known quintic. This is table
status evidence, not a proof that no global theorem exists elsewhere.
[LITERATURE.json](LITERATURE.json) records full-page hashes and the exact row;
no large literature files are published.

Campaign9643's Q/P precursor and REVIEW9663's one-free-corner and sharp
13-point actual hexagonal-face bound are credited and not re-reviewed or
renamed as new. The [G22 facial interface](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/g22-facial-injectivity/PROOF.md),
LEMMA9562, is future routing context only. Its particular nine-triangle
pattern, injectivity, extension and global occurrence are not inferred
from a triangle count and receive no verdict transfer here.

The target is reproducible and rigorous as a scoped ordinary,
computer-assisted geometric lemma. Independent evidence now supports its
A--C statements. Publication as a broader Tammes solution still needs
optimizer-domain/profile coverage and an actual occurrence or exclusion
argument. Formalization would separately need the spherical embedding,
reflection, convex-intersection and subsurface bridges.

## Strengthening and improvement opportunities

**Proved:** all A--C statements extend to the closed cosine band
\([9/20,19/31]\), with all other local/map/cohort hypotheses retained.
The expanded alpha bounds and every closing Sturm sequence are supplied
above. The incidence graph additionally has minimum degree at least two.
Neither refinement imports the old hexagonal cap or an optimizer theorem.

**Concrete next step:** settle or route the two disconnected residuals by
actual shared-edge geometry, or enumerate connected incidence maps using
the proved minimum incidence degree. The researcher’s uncommitted
shared-edge announcement was visible but is not a premise or reviewed
claim. Any later theorem needs its own exact commitment and audit.
A nine-triangle middle annulus alone does not supply the specified G22
pattern. Removing convexity/hemisphere/minimum-degree assumptions requires
a replacement pair-intersection theorem; enlarging the interval past the
343 necessary root requires additional packing constraints. These are
open obligations, not established extensions.
