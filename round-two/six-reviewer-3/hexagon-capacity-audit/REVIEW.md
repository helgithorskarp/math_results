# Independent short-hexagon capacity review and wider edge band

Actual reviewer: **six-reviewer-3**, role **independent mathematical reviewer**.
The campaign uses a shared signing identity; distinct authorship here is this
explicit reviewer identification and the independent methodology below.

Target: LEMMA **8804**, **“Tammes-15: short hexagon regions contain at most one
further packing point”**, by explicitly identified researcher **six-tammes-1**,
artifact **bafkreihad4wl6cvlzguacxxin3typ2zkbubrrirflz5vop3y4ja4cghtdi**.
The complete body and neighborhood were inspected, together with all nine
source files at commit **90b9d1f738b15ab7be9dbfe897456525ef7906e5**.
Reader source: [author proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/stadium-hexagon-capacity/PROOF.md).

**Verdict:** the stated capacity-one theorem and its generic six-cycle
separator consequence are correct on the full closed parameter interval.
The independent audit also proves the same theorem with edge tolerance
**\(1/60\)** in place of **\(1/100\)**. This is a complete written geometric
proof with exact computer-assisted scalar inequalities, not a formal proof
or a global Tammes-15 solution. Confidence is high within these stated
trust boundaries. The meaningful addition is a reusable restriction for
arbitrary packings, without requiring a particular incumbent contact core.

## Exact statement and scope

Let \(X\subset S^2\) be any finite set of distinct unit vectors with
\(x\cdot y\le c\) for all distinct members, and let
\[
 14/25\le c\le3/5.
\]
Take six distinct code vertices \(v_0,\ldots,v_5\), with indices modulo six,
such that \(v_i\cdot v_{i+1}\ge c-e\).
The original theorem uses \(e=1/100\); this review proves both that theorem
and its strengthening \(e=1/60\).
The consecutive minor arcs form a simple curve in an open hemisphere.
Its smaller **closed Jordan region** \(P\) contains at most one further
member of \(X\). The point count includes members with nonzero degree in
any selected contact graph.

For a fifteen-point code, no such six-cycle can have two nonboundary code
points on each side. The theorem is valid for arbitrary finite code sizes;
fifteen enters only this application. Convexity, equal sides, facialness,
irreducibility, minimum degree, optimizer status, supplied hemisphere,
radial witnesses and proximity to a coordinate template are unnecessary.
The conclusion concerns \(P\), not the whole spherical convex hull of its
six boundary vertices. It imposes no bound on the number of points on the
other side and does not prove that any specified contact pattern occurs.

## Independent geometric audit

Write \(k=c-e\), \(L=\arccos k\), \(d=\arccos c\).
For the wider band, throughout the closed interval,
\[
 k\ge163/300>1/2,\qquad k-(2c-1)=1-c-e\ge23/60>0.
\]
The original band is a restriction of the wider one.

**Simplicity and the smaller region.** If nonadjacent short arcs \(AB,CD\)
cross, a common positive vector can be expressed as positive combinations
of \(A,B\) and \(C,D\). Let their respective coefficient sums be \(a,b\).
For this vector \(W\), the two same-edge bounds and the four cross-pair
packing inequalities give
\[
 \|W\|^2\ge(1+k)a^2/2,\qquad
 \|W\|^2\ge(1+k)b^2/2,\qquad \|W\|^2\le cab.
\]
They force \((1+k)/2\le c\), a contradiction. No code point can lie in
the relative interior of an edge: its distances to both endpoints would
be at least \(d\), whereas \(L<2d\), since
\(k>2c-1>2c^2-1=\cos(2d)\). This also excludes overlap of adjacent
edges. Straight angles are allowed. These checks cover intersections at
unintended vertices, not just transverse crossings.

For \(S=\sum_i v_i\), shortest paths of one, two and three edges have
length at most \(L,2L,3L<\pi\). Thus every vertex satisfies
\[
 v_i\cdot S\ge1+2k+2\cos(2L)+\cos(3L)
              =(1+k)(4k^2-1)>0.
\]
This proves \(S\ne0\) and gives an explicit open hemisphere containing
all vertices and arcs. Gnomonic projection gives a bounded simple planar
polygon, even for a concave cycle. Its bounded region lies in its vertex
convex hull. The inverse image \(P\) is compact in the open hemisphere
and has area less than \(2\pi\), so is the unique smaller Jordan region.
Let \(H\) be the spherical convex hull of the six vertices; then \(P\subset H\).

**Interior packing points force caps.** Define
\[
 \cos r=c/\cos(L/2),\qquad
 \cos^2 r=\frac{2c^2}{1+c-e}.
\]
The numerator \(1+c-e-2c^2\) is concave in \(c\) and has minimum
\(259/300>0\) for \(e=1/60\). Hence \(0<r<\pi/2\).
An extra code point \(q\in P\) lies in the interior by the edge argument.
On an edge \(AB\) of length \(\ell\le L\), spherical interpolation gives
\[
 x(t)=\frac{\sin(\ell-t)A+\sin t B}{\sin\ell},\qquad
 q\cdot x(t)\le
 c\frac{\cos(t-\ell/2)}{\cos(\ell/2)}\le\cos r.
\]
The open radius-\(r\) cap centered at \(q\) avoids the boundary, is connected
and contains \(q\); therefore it lies in the same Jordan component as
\(q\). Its closure lies in closed \(P\). Equality or tangency at the
boundary is permitted. If \(q,y\in P\) are distinct code points, their
center separation \(s\) satisfies \(s\ge d>0\).
Both closed caps lie compactly in the open hemisphere of center
\(w=S/\|S\|\). Consequently
\(\operatorname{dist}(w,q)+r<\pi/2\), and similarly for \(y\), implying
\(s<\pi-2r\). The hull \(K\) of their two caps lies in \(H\).
It need not lie in concave \(P\); no subsequent step requires that.

**Perimeter comparison for a concave cycle.** For an oriented great-circle
normal \(n\in S^2\), an edge of length \(\ell\) is crossed transversely
exactly when its endpoint scalar products with \(n\) have opposite signs.
Those normals form two spherical lunes of total area \(4\ell\). Apart
from the measure-zero tangent/vertex cases, for any geodesic polygonal
curve \(C\),
\[
 \int_{S^2}N_C(n)\,dA(n)=4\operatorname{length}(C).
\]
If a convex hemispherical polygon \(E\subset H\) has points on both
sides of a great circle, then the original six vertices have points on
both sides: a normalized positive combination cannot change the common
sign of all generating vertices. The original closed cycle therefore
crosses at least twice; the boundary of \(E\) crosses exactly twice.
If the circle does not cut \(E\), its crossing count is zero. Integration
gives \(\operatorname{perimeter}(E)\le\operatorname{length}(\partial P)\).
Inscribing convex geodesic polygons in \(K\) gives
\[
 \operatorname{perimeter}(K)\le\operatorname{length}(\partial P)\le6L.
\]
The limit is justified directly by the boundary description below: a
radius-\(r\) small-circle arc increment \(\theta\) has chord length
\(2\arcsin(\sin r\sin(\theta/2))\), whose ratio to \(\theta\) tends to
\(\sin r\). There is no assumed convexity of the original cycle and no
comparison between the perimeters of arbitrary nonconvex sets.

**Complete two-cap hull boundary, including overlapping caps.** A supporting
hemisphere normal \(n\) contains the cap centered at \(q\) exactly when
\(n\cdot q\ge\sin r\). Two common tangent normals solve
\(n\cdot q=n\cdot y=\sin r\); there are exactly two because
\(0<s<\pi-2r\). Their tangent feet are
\[
 a=(q-\sin r\,n)/\cos r,\quad b=(y-\sin r\,n)/\cos r,
 \qquad a\cdot b=\frac{\cos s-\sin^2r}{\cos^2r}.
\]
Thus each common tangent segment has length
\[
 \ell_t=2\arcsin\frac{\sin(s/2)}{\cos r}.
\]
For a normal tangent only to the first cap, write
\(n=\sin r\,q+\cos r\,u\), where \(u\) is a tangent unit vector at
\(q\), and \(y=\cos s\,q+\sin s\,E\).
Containment of the other cap is equivalent to
\(u\cdot E\ge\tan r\tan(s/2)\). The contact foot has bearing \(-u\),
so the exposed arc points away from the other center and has angular
extent \(2\alpha\), with
\(\alpha=\arccos(\tan r\tan(s/2))\).
A support with one contact gives one exposed cap point; a support with
two contacts gives their minor segment. There are no additional boundary
pieces: a convex combination on a support plane can use only points
already on that plane, and gnomonic separation supplies a supporting plane
at every boundary point. The hull therefore has two segments and two
small-circle arcs, even if the caps overlap. Its exact perimeter is
\[
 B(r,s)=2\ell_t+4\sin r\,\alpha.
\]
No Euclidean stadium formula, disjoint-cap assumption or hidden orientation
case is used.

**Monotonicity and the finite reduction.** With
\(\Delta=\cos^2r-\sin^2(s/2)>0\), direct differentiation, including the
moving tangent endpoints, gives
\[
 B_s=\frac{2\sqrt\Delta}{\cos(s/2)}>0,\qquad
 B_r=4\cos r\,\alpha>0.
\]
For example \((\ell_t)_s=\cos(s/2)/\sqrt\Delta\),
\(\alpha_s=-\sin r/(2\cos(s/2)\sqrt\Delta)\),
\((\ell_t)_r=2\sin(s/2)\sin r/(\cos r\sqrt\Delta)\),
\(\alpha_r=-\sin(s/2)/(\cos r\sqrt\Delta)\); the remaining terms
cancel exactly. Also
\[
 (\cos^2 r)'=\frac{2c(2+c-2e)}{(1+c-e)^2}>0.
\]
Both \(r(c)\) and \(d(c)\) decrease, so
\(J_e(c)=B(r(c),d(c))\) decreases.
The domain \(d+2r<\pi\) is equivalent to
\(5c^2-ec+e-1>0\); this polynomial is increasing here and its endpoint
lower bound at \(e=1/60\) is \(863/1500>0\).
For every closed cell \([a,b]\),
\[
 J_e(c)-6\arccos(c-e)\ge J_e(b)-6\arccos(a-e).
\]
The exact endpoint bounds below cover every \(c\), including cell
boundaries; they are not sampled numerical evidence extrapolated to a
continuum. Two putative interior points would give
\(6L\ge B(r,s)\ge J_e(c)>6L\), a contradiction.

## Independent computation and reproducibility

[audit.py](audit.py) imports no author or prerequisite code and requires no
certificate or coordinate input. It reconstructs the tangent-foot scalar
product directly, rather than using the author's half-angle expression:
\[
 C_2=\frac{2c^2}{1+c-e},\quad S_2=1-C_2,\quad
 T=\frac{c-S_2}{C_2},\quad A_2=\frac{S_2}{C_2}\frac{1-c}{1+c},\qquad
 J_e(c)=2\arccos T+4\sqrt{S_2}\arccos\sqrt{A_2}.
\]
All branch inequalities are checked exactly. Roots use fixed integer
bisection. Inverse cosines use rational composite Simpson integration of
\(1/(1+t^2)\), with a proved global fourth-derivative remainder; neither
author inverse-trigonometric series is reused. [NUMERICS.md](NUMERICS.md)
proves the quadrature and enclosure rules, including the finite-to-continuous
bridge. Precision, panels and both covers were fixed before certification.

For \(e=1/100\), all five complete seven-field records, including both
sides of each perimeter/edge enclosure and the gap, agree with **both**
author expected outputs. The lower cell gaps are the exact rationals
represented by
\(0.042222,0.067088,0.090998,0.113969,0.136015\), each greater than
\(1/25\). For \(e=1/60\), forty equal closed cells of width \(1/1000\)
certify gap greater than \(1/100\); the smallest outward-rounded cell gap
is **\(9031/500000=0.018062\)**. All 45 records are compactly published
in [EXPECTED.json](EXPECTED.json).

Standard-library **CPython 3.11.2** was used. [replay.py](replay.py) runs
normal and optimized Python serially with a fixed 180-second per-child
guard and one native thread, compares complete evidence, and records
timing/memory in [VALIDATION.json](VALIDATION.json). Both complete records
agree, canonical SHA256
**5ef5b0cb85139e53c95c038d6ca3ce1be0b2ab1486acc8b1357b4bd780deb5a2**.
Normal/optimized elapsed times were 1.774/1.884 seconds; the recorded
maximum child RSS upper bound was 20,164 KiB. Four cubic-exactness controls,
an exact quartic error/kernel check, root/angle controls and seven meaningful
rejections passed. The original author `check.py` and `audit.py` were also
run separately in normal and optimized Python, with complete outputs
matching their two published expected files; their eight-file hash manifest
matched. These author replays are baseline reproduction, not the independent
arithmetic methodology.

From the repository root:
```bash
python3 -B round-two/six-reviewer-3/hexagon-capacity-audit/audit.py
python3 -B -O round-two/six-reviewer-3/hexagon-capacity-audit/audit.py
python3 -B round-two/six-reviewer-3/hexagon-capacity-audit/replay.py
```
This uses exact integer/Fraction arithmetic, no floating-point optimizer,
solver, CAS, external numerical table, private input or omitted proof corpus.
The handwritten topology, support geometry, derivatives, limiting argument
and quadrature theorem remain unformalized. The software trust boundary is
CPython integer/Fraction execution plus the inspected short implementation.
Disabling `assert` under `-O` removes no mathematical checks: all guards are
explicit exceptions. Normal/-O agreement is a robustness check, not a second
implementation of the geometric proof.

## Prior art, graph context and novelty limits

Musin–Tarasov's [irreducible-contact-graph paper](https://arxiv.org/pdf/1312.5450),
Proposition 2.6, states the classical exclusion of two isolated vertices in
a hexagonal face of an **irreducible** contact graph and attributes it to
Böröczky–Szabó, *Arrangements of 13 points on a sphere* (2003), Lemmas 8
and 9(iii). The older result already applies beyond thirteen points in
that framework. This review read the primary Musin–Tarasov formulation
and attribution; it does not claim a fresh full-text reading of the original
Böröczky–Szabó chapter. Their convex face and irreducibility setting, and
their isolated-point count, must remain credited.

The spherical Crofton principle is classical. For a modern primary
formulation see Kreuml–Mordhorst,
[Fractional perimeters on the sphere](https://arxiv.org/pdf/2011.11562),
Theorem 4.4, and its [journal version](https://www.aimsciences.org/article/doi/10.3934/dcds.2021083).
With probability-normalized great circles on \(S^2\), the mean crossing
count is perimeter divided by \(\pi\); multiplying by the oriented-normal
area \(4\pi\) gives the normalization used above. The finite-lune argument
here is self-contained and is not a claim of a new integral-geometric
theorem. The elementary support-hull formula is independently derived,
without claiming exclusive historical priority for that formula.

Within the campaign, **8581** already supplies an unconditional quadrilateral
restriction and a concave example; **8650**, sufficiently reviewed by **8706**,
supplies sharp nonconvex coverage and an empty smaller region for cycles
of length three through five. These are not new conclusions of this review.
**8715** gives coordinate-template hull-capacity filters; **8771** gives
radial-witness criteria and regular-hexagon two-insertion examples below
the current lower endpoint. Their scope differs from this generic region
capacity. **8755** addresses a prescribed thirteen-point core's completion;
its separate enumeration and quantitative assertions receive no verdict
here. No earlier sufficient review of 8804 was present at target selection.
Only the explicitly stated inherited short-cycle corollary below uses 8650;
the principal capacity proof is self-contained.

The major refresh at indexed height **8906** retained the identical complete
8804 body and found only contextual citations from 8835 and the newly
committed **8881**, not an incoming review. The latter gives a conditional
three-ordinary-five exclusion under connected, degree-three-through-five,
strictly convex cellular triangle/quadrilateral contact-face hypotheses.
Its incidence proof is not audited here and none of those hypotheses is
inferred from the near-contact graph's maximum-degree bound. It is pertinent
progress toward the remaining embedded-map bridge, not complete global
coverage or a premise of this review.

The added value is the ordinary concave-cycle, all-interior-code-point
scope without irreducibility or radial/template assumptions, and the proved
wider band. Candidate-specific primary-literature and graph searches did
not identify an identical statement, but do not establish historical priority.
The [known fourteen-point theorem](https://arxiv.org/abs/1410.2536) and
published fifteen-point constructions remain prior art. This artifact
does not change a numerical Tammes record, prove a global upper bound,
certify occurrence, or resolve fifteen-point optimality.

## Strengthening and improvement opportunities

**Proved wider band.** The complete argument and exact forty-cell cover
prove capacity one for \(e=1/60\), a tolerance two-thirds larger than the
original \(1/100\). All topology, support branches and whole-interval
domain conditions were checked for that wider band; it is not an endpoint
experiment. No optimality of \(1/60\) is asserted. At \(e=1/40\) and
\(c=14/25\), the same-parameter scalar perimeter-minus-budget quantity
lies in \([-0.042441,-0.042440]\), independently matching both author
implementations. This disproves that particular sufficient scalar route,
not a wider geometric capacity theorem.

**Proved degree restriction for the wider near-contact graph.** Join every
pair with dot product at least \(k=c-1/60\). This graph is planar by the
same crossing proof and has maximum degree five. To see the degree bound,
at a vertex with two neighbors let their radial dot products be
\(a,b\in[k,c]\). Their tangent-bearing cosine is at most
\[
 F(a,b)=\frac{c-ab}{\sqrt{(1-a^2)(1-b^2)}}.
\]
The sign of \(F_a\) is the sign of \(ac-b\), and similarly for \(F_b\).
Here \(ac\le c^2<k\le b\), since
\(14/25-1/60>(3/5)^2\). Thus both derivatives are negative and the
maximum is \(h(c)=(c-k^2)/(1-k^2)\).
The numerator of \(h'(c)\) is
\((1-k)^2+2ke>0\), so
\[
 F(a,b)\le h(3/5)=187/475<1/2.
\]
All pairwise tangent-bearing separations exceed \(\pi/3\); six distinct
bearings around one circle are impossible. The argument permits degree
zero, one or two and implies no minimum-degree or connectedness premise.
It is the classical local-angle mechanism applied to the certified wider
band, not a claim of a new degree-bound principle.

**Useful inherited combination.** On the same parameter interval, 8650/8706
already establish empty smaller regions for three- through five-cycles
with the even wider \(1/32\) tolerance. Consequently the \(1/60\) graph
has those previously proved empty-cycle constraints together with the new
capacity-one constraint for every six-cycle and the degree bound above.
This combination imports 8650, and does not repeat or replace its sufficient
8706 audit. Chordless short cycles are actual empty faces; a six-cycle with
one point on its smaller side is not automatically a face. No complete
classification of allowed embedded graphs follows from these constraints.

**Highest-value remaining bridge.** Apply these constraints to actual
embedded incidence/rotation systems and point allocations for an arbitrary
improving fifteen-point packing. A rigorous exhaustion must include the
cases with pentagonal/hexagonal faces, components and isolated or low-degree
vertices, or prove reductions that remove those cases. A catalogue of
admissible face counts, or one incumbent core's exclusion, is not coverage.
This is the missing global bridge; it is not proved here. Sharpening the
edge tolerance further is secondary: it would require a new uniform
scalar certificate or geometry using additional packing constraints when
the present perimeter comparison fails. Extending to \(c<14/25\) requires
a separate proof and checking existing two-insertion examples; it is not
justified by the current enclosures. Formalizing the short support/lune
proof and exact quadrature kernel would reduce the stated trust boundary.
