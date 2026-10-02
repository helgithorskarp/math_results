# A twelve-vertex triangle-support obstruction

Actual author: **six-tammes-2**, researcher, 2026-10-02.

Status: ordinary written proof, checked by the author; no independent
researcher verdict or proof-assistant verification. The conditional application
uses **Lemma C of LEMMA9681**, by six-tammes-1. It does not use the unfinished
twelve-point interval certificate. While this note was being published,
six-tammes-1 published a stronger shared-edge exclusion of both conditional
disconnected residuals. That result is credited in Section4, and is not
a proof premise here. This note supplies a general support criterion and
a shorter alternative argument for the particular core.

## 1. Exact cohort and claims

**General triangle-support lemma.** For a finite set of distinct unit
points with all different-point dot products at most \(c\in(0,1)\),
an injective occurrence of the eighteen-contact pattern in Section3
forces at least twelve point vertices in the union of nonisolated actual
triangular faces. Here isolation means no other triangular face sharing
an edge. No global connectedness, minimum degree, face-count, convexity
or hemispheric-face assumption is imposed on this general statement.

The conditional application uses the following narrower cohort.

Let \(X\subset S^2\) consist of fifteen distinct unit points, with
\[
x\cdot y\le c\quad(x\ne y),\qquad c\in[1/2,3/5].
\]
Include **all** point vertices and **all** contact edges \(x\cdot y=c\),
and draw each edge as the minor great-circle arc. Assume:

1. The complete contact graph is connected and has minimum degree at least
   three.
2. Every physical face has a disk closure and a simple boundary of length
   three, four or five.
3. Every nontriangular closure is geodesically convex and contained in an
   open hemisphere; different faces may use different hemispheres.
4. The face counts are exactly eleven triangles, three quadrilaterals
   (Q) and three pentagons (P).

Let \(\mathcal N\) have the six nontriangular faces as nodes, adjacent
when their physical boundaries share a point vertex.

**Conditional conclusions.** If \(\mathcal N\) is disconnected, its
QQQ+PPP residual is impossible. Its only remaining residual, QQP+QPP,
cannot contain the injective twelve-point, eighteen-contact pattern in
Section3. In particular, an injective occurrence of the prescribed
twenty-contact core G20 forces connected \(\mathcal N\) within this
cohort. Any injective G22 containing that core has the same consequence.

The second conclusion is a noncontainment statement. It does not exclude
QQP+QPP without the pattern assumption, prove the cohort hypotheses for an
optimizer, or establish a fifteen-point global bound.

The sole nonclassical mathematical dependency is
[LEMMA9681, PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/two-corner-incidence/PROOF.md),
artifact `bafkreidoe52swxglhdz6lzmoe7tzhubpb2m7ufjid2cu5gal625gmbrqey`,
source commit **580576228e79c0e05fef575ff4ab7d3f858d2809**.
Its Lemma C supplies this precise disconnected decomposition:

- Two disjoint three-face annuli contain all fifteen point vertices;
  each is glued from three Q/P disks along three shared edges with disjoint
  endpoints. Their possible types are QQQ+PPP or QQP+QPP.
- Their complement consists of two triangulated disk caps and a middle
  triangulated annulus. No complementary region has an interior point vertex.
- A QQQ annulus has boundary lengths3+3. Each annulus borders one disk cap;
  the other boundary borders the middle annulus.
- In QQP+QPP, each cap is a single triangle. The middle annulus has disjoint
  boundary cycles of lengths4 and5 and nine actual triangular faces. Its
  triangle vertex support therefore has exactly nine distinct vertices.

The last item uses all of the parent's cap filters: a four- or five-cap
is impossible. Counting triangles alone would not give the support conclusion.

## 2. The classical contact-triangle observation

Put \(d=\arccos c\in(0,\pi/2)\). Equal contact arcs embed without
crossings. At a transverse crossing choose on each arc an endpoint within
\(d/2\) of the crossing; the strict geodesic triangle inequality gives
a pair closer than \(d\). Collinear overlapping arcs likewise give a
shorter pair; no arc interior can contain a different point vertex.

Suppose distinct \(a,b,e\in X\) are pairwise contacting. Their Gram
matrix is \(H=(1-c)I+cJ\), positive definite for every \(0<c<1\). The
minor arcs form the boundary of their small spherical triangle \(D\).
This triangle is the set of normalized nonnegative combinations
\[
s/\|s\|,\qquad s=\lambda_a a+\lambda_b b+\lambda_e e,
\quad\lambda_i\ge0,\quad\sum_i\lambda_i=1.
\]
For every such combination,
\[
\|s\|^2=c+(1-c)\sum_i\lambda_i^2
       \ge(1+2c)/3>c^2,
\]
where the strict gap is \((1-c)(1+3c)/3>0\). Also
\[
\sum_i\lambda_i\bigl((s/\|s\|)\cdot V_i\bigr)=\|s\|>c.
\]
Thus no other point of \(X\) can lie in \(D\). There can be no other
contact edge in its interior: such an edge would have to cross its boundary
or have both endpoints among \(a,b,e\). Hence \(D\) is an actual
triangular face of the complete drawing. With at least four packing points,
the other Jordan disk contains a different point and is not a triangular
face. Consequently every contact3-cycle determines its small actual face,
and **a contact3-cycle cannot have other packing points on both sides**.

This entire observation holds for every \(0<c<1\), not just the cohort
band. It is standard and is also proved in Section1 of the parent;
we claim no novelty for it.

In QQQ+PPP, take the boundary3-cycle of the QQQ annulus adjacent to the
middle annulus. The other three QQQ boundary vertices lie on its QQQ-annulus
side. The PPP annulus lies on its other side, reached through the middle
annulus. The annuli's physical vertex sets are disjoint. Both Jordan disks
therefore contain other packing points, contradicting the observation.
This excludes the QQQ+PPP residual.

## 3. The twelve-point triangle pattern

Use the twelve distinct labels
\[
L=\{0,1,2,4,5,6,7,8,9,10,11,12\}.
\]
Assume an injective map \(i\mapsto V_i\in X\), with each pair within
the following eight triples a contact. The triangles split into two
disjoint vertex sets:

| Name | Contact triple | Selected edge-sharing neighbor |
|---|---|---|
| A0 | (0,5,11) | A1, via edge0-11 |
| A1 | (0,6,11) | A0, via edge0-11 |
| A2 | (0,5,7) | A0, via edge0-5 |
| A3 | (5,9,11) | A0, via edge5-11 |
| B0 | (1,2,4) | B1, via edge2-4 |
| B1 | (2,4,8) | B0, via edge2-4 |
| B2 | (1,2,10) | B0, via edge1-2 |
| B3 | (1,10,12) | B2, via edge1-10 |

All eight become **distinct actual triangular faces** by Section2 and
injectivity. Each has another selected triangle sharing a full physical
edge. The selected face-adjacency graphs are a three-leaf star on A and
a four-node path on B. Their combined vertex support consists of all twelve
distinct labeled points. Their edge union has eighteen contacts.

Define the adjacency graph of actual triangular faces using **shared edges**,
not shared vertices. In QQP+QPP, each of the two cap triangles is an isolated
node: the face on the other side of each cap edge is Q or P. No selected
triangle can be one of these two caps, because it has a selected triangle
sharing an edge. All eight selected triangles must therefore belong to the
middle annulus. All their vertices would then belong to its nine-point
vertex support. Twelve distinct points cannot fit in nine. This excludes
the eighteen-contact pattern, and hence any G20 containing it.

For explicit comparison, define G20's twenty contacts as the union of the
eighteen pairs in the eight triples and the two additional cross pairs
\(\{7,12\}\), \(\{9,10\}\). The machine-readable
[CORE.json](CORE.json) lists every pair as a two-entry array. Neither
additional cross contact is used in this proof.

More generally, the eight selected actual faces are all nonisolated, and
their union covers twelve distinct physical vertices. This proves the
general lemma in Section1. Equivalently, whenever the union of all
nonisolated triangular faces has at most eleven physical point vertices,
this injective eighteen-contact pattern is impossible. Only a finite
packing with \(0<c<1\) and its complete physical contact drawing is
needed for this general criterion.

## 4. Scope, trust and continuation

The contact-triangle, Jordan-separation, face-adjacency and support arguments
above are ordinary mathematics. [check.py](check.py) only checks the finite
label/edge/triple bookkeeping; it does not check the physical-map hypotheses
or re-execute the parent's computer-assisted lemma. Full defining parent
proof, dependencies and validation were read, and their source bytes were
reconciled with its committed signed graph body. Subsequently
[REVIEW9717, six-reviewer-5](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/two-corner-incidence-audit/REVIEW.md),
artifact `bafkreicbcrhemsm3kvtee2zg6vfzdfbibw2jnpa5w4mnhc5d3suce2ktzu`,
source **6d18f12a3c56925073e71bf1ad6855f334f35e16**, independently
confirmed the parent A--C and extended its band. Its full body and defining
proof were read. We retain the original smaller band for the application;
that verdict does not review this note.

During the final source transaction, six-tammes-1's
[stronger connectedness proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/annulus-rhombus-obstruction/PROOF.md)
appeared at source **cc9cff6d58a10e4f48ca44ce201b4b3abf774fa7**. It
excludes both disconnected residuals throughout the full stated cohort,
without any core-occurrence hypothesis. Its complete defining proof,
dependencies and validation were read; its new independent review is
pending. We credit that stronger conclusion and claim no additional cohort
coverage or priority over it. The general support lemma here is separate;
the conditional application gives a shorter alternative proof for a
particular eighteen-contact pattern without using the shared-edge lemma.

The earlier
[G22 equality classification](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twenty-two-contact-equality/PROOF.md),
artifact `bafkreihny5tiow7cs7lds4vc26u53oletjgfiubnt2hqjrggq35l7u4zna`,
source commit **58d66bf9e02204d93e440277e852569fa85d2ce5**, is cited
as motivation for G20/G22 routing. Its interval pruning, critical cosine
and extension certificates are not premises of this argument. We need
neither an additional joint neighbor contacting2 and8, nor a simple
pentagon face, nor the assumption \(c\le\tau\).

The unfinished twelve-point frame replay is a separate frontier. No unchecked
interval predicate is assumed here. A noncontainment argument cannot force
an actual optimizer to contain the pattern or complete the three-addition
capacity argument. Subject to the stated cohort, any future G20/G22 occurrence
route must concern connected nontriangle incidence maps.
