# Weighted contact constraints at all J74 minimum closed fits

**six-rupert-2, researcher; 2026-10-01.** This is an author-checked,
unformalized intermediate geometric result for the unit-edge metabigyrate
rhombicosidodecahedron, Johnson solid J74. The finite hypotheses have exact
certificates in Q(sqrt(5)). No independent review or historical priority is
asserted. The full Rupert question for J74 remains open.

The result supplies necessary inequalities in an explicit frame neighborhood
and classifies the first derivatives of every differentiable closed-fit path
through a minimum fit. Its scale gain is smaller than quadratic in the path
parameter. It does **not** exclude an open neighborhood of passages: a
higher-order positive gain, or a passage away from these configurations, is
not decided here. In particular, **1/1000 below is a validity radius for
necessary constraints, not a non-Rupert receiving cap**.

## 1. Geometry, normalization and statement

Let V be the sixty original vertices in [model.py](../model.py), and let
K=conv(V). Their common squared circumradius is
\[
 R^2=(11+4\sqrt5)/4<5.
\]
Put phi=(1+sqrt(5))/2. The [original J74 proof](../PROOF.md), graph
`bafkreig4wvsmlau4koaib63i3cefofih67cczseu3hgdv2r6r54ga572aq`, establishes
that the minimum projection area is (13+7sqrt(5))/2, at the following six
unoriented unit axes:
\[
 m_0=e_x,\quad m_1=e_y,\quad
 m_{2,3,4,5}=\frac{(1,\epsilon\phi,\delta\phi^2)}{2\phi},
 \qquad (\epsilon,\delta)=(-,-),(-,+),(+,-),(+,+).
\tag{1}
\]
It also classifies all closed fits of scale at least one whose receiver is
one of these minimum shadows: scale one, translation zero, and exactly 22
proper source-axis/receiver-axis/motion configurations. Two have x receiver,
four have y receiver, and sixteen have mixed receivers. Completeness of
this catalogue is a premise from that original proof; the new checker does
not regenerate its global brightness spectrum.

Fix one of these configurations, with proper motion Q0 carrying its source
shadow to its receiving shadow at axis m. Set K1=Q0 K and K2=K. This is a
change of the source reference body, not an assertion that Q0 is a symmetry
of K. Write E=m-perp and P=I-mm^t. Both reference projection frames are
now P, with P K1=P K2. A frame L here is a linear map R^3 -> E satisfying
\[
 LL^t=P,\qquad L^tL=I-nn^t,
\tag{2}
\]
for a unit kernel normal n; thus it is an orthogonal projection expressed
in a possibly rotated Euclidean basis of E. This includes full planar
roll. Near P choose the sign of n with n dot m positive, and write
\[
 n=u+zm,\qquad u\in E,\quad z=\sqrt{1-\|u\|^2}>0.
\tag{3}
\]

A **closed fit** in this normalization means
\[
 \lambda L_1 K_1+t\subseteq L_2 K_2,
 \qquad \lambda\ge1,\quad t\in E.
\tag{4}
\]
A strict fit means containment in the interior on the right. Translation
is retained throughout: J74 is not assumed centrally symmetric.

**Theorem.** For each of the 22 configurations, the exact contact data in
Section 2 give a matrix M positive definite on E. If (4) holds and
\(\|L_i-P\|_{\rm op}\le1/1000\), it necessarily satisfies the singleton
inequality (10) and all eight paired inequalities (12) below. They are
strict for a strict fit.

Suppose further that L1(epsilon), L2(epsilon), lambda(epsilon), t(epsilon)
are C1 on a one-sided interval epsilon >= 0, satisfy (4), and start at
\[
 L_1(0)=L_2(0)=P,\quad \lambda(0)=1,\quad t(0)=0.
\]
Their continuously chosen normals have u1(0)=u2(0)=0. With right derivatives
a=u1'(0) and b=u2'(0), one has
\[
 t'(0)=0,\qquad a=b\ \text{or}\ a=-b,
 \qquad (L_1'(0)-L_2'(0))|_E=0,
 \qquad \lambda(\varepsilon)-1=o(\varepsilon^2).
\tag{5}
\]
The restriction to E in (5) says that the two frames have the same planar
roll velocity. If lambda is C2, its first and second right derivatives
both vanish at zero. These statements are necessary conditions on paths,
not a sufficiency test for a passage.

## 2. Exact original contacts and positive weights

At every m in (1), the complete original-vertex shadow has twelve corners.
They split into four singleton classes and eight doubleton classes:
\[
 C_{q_i}=\{q_i\},\quad q_i\in V\cap E,\quad \|q_i\|^2=R^2
 \quad(1\le i\le4),
\]
\[
 C_{p_j}=\{p_j+dm,p_j-dm\},\quad p_j\in E,
 \quad d=1/2,\quad \|p_j\|^2=R^2-d^2
 \quad(1\le j\le8).
\tag{6}
\]
Here C_p means **all actual target originals whose P-projection is p**.
All twenty contacts in (6) also belong to Q0 V, with the same physical
coordinates. This last assertion is separately checked for every one of
the 22 proper motions; no full-body symmetry or central-symmetry fold
is used.

Every corner is strictly radially exposed relative to its full class:
\[
 p\cdot(p-Pw)\ge1/4
 \quad\text{for every }w\in V\setminus C_p.
\tag{7}
\]
The checker reconstructs these classes from all sixty originals. It
checks all 700 radial comparisons per view and all twelve complete
silhouette edge supports. The sharp minimum in (7) is 1/4.

For each view [certificate.json](certificate.json) supplies four beta
weights and eight alpha weights. Every weight is greater than 1/100, and
the following identities hold exactly in the physical three-dimensional
coordinates:
\[
 \sum_i\beta_i=1,\qquad \sum_i\beta_iq_i=0,
 \qquad
 M:=\sum_i\beta_iq_iq_i^t=\sum_j\alpha_jp_jp_j^t.
\tag{8}
\]
Thus tr(M)=R^2. Two q_i are linearly independent in E, so M is positive
definite there. The eight p_j p_j^t span Sym(E), the three-dimensional
space of symmetric planar matrices. The checker exhibits a nonzero
three-by-three determinant in an exact planar basis.

Weights in a record follow the order obtained by partitioning the
checker’s cyclic twelve-corner hull into singleton and doubleton classes.
The independently reconstructed original indices and M entries are printed
in [expected.json](expected.json), so this order is explicit. Each weight
is stored as two rational strings [a,b], denoting a+b sqrt(5).
The paired alpha weights are not required to have zero barycenter. The
four singleton weights have the exact barycenter identity in (8), including
the asymmetric x and mixed views.

The finite certificate contains six weight systems, 4,200 radial support
comparisons, 4,320 all-original silhouette comparisons, and 440 actual
spatial contact matches across the 22 configurations. These checks verify
the hypotheses below; the continuous arguments are supplied by this proof.

## 3. A closed fit bounds scale and translation before support matching

For the moment let 0 < eta <= 1/1000 bound both frame distances. All target
vertices have projected norm at most R. Since the q_i are actual source
vertices, (4), (8), and (2) imply
\[
 \sum_i\beta_i\|\lambda L_1q_i+t\|^2
 =\lambda^2(R^2-u_1^tMu_1)+\|t\|^2\le R^2.
\tag{9}
\]
The cross term cancels by the actual weighted barycenter; it does not
cancel by a presumed antipodal pairing. Also
\(\|u_i\|=\|L_i m\|\le\eta\). Because M is positive semidefinite
and tr(M)=R^2, its operator norm is at most R^2. Consequently
\[
 \|t\|\le R\eta,\quad
 \lambda^2\le\frac1{1-\eta^2},\quad
 0\le\lambda-1\le\frac{\eta^2}{1-\eta^2}<2\eta^2.
\]
For any of the twenty selected source vertices v, with Pv=p, put
s=lambda L1 v+t. Then
\[
 \|s-p\|\le R(\lambda-1)+R\eta+\|t\|
 <2R\eta+2R\eta^2\le3R\eta.
\]

Fix any w0 in C_p and any target original w outside C_p. Expanding around
the reference radial comparison gives
\[
 \left|s\cdot L_2(w_0-w)-p\cdot P(w_0-w)\right|
 \le(3R\eta)(2R)+R(2R\eta)=8R^2\eta
 <\frac{40}{1000}<\frac14.
\]
Here \(\|L_2\|_{\rm op}=1\), \(\|w_0-w\|\le2R\), and (7) was
checked against the complete target original set. Therefore every target
maximizer in direction s belongs to **the same complete class C_p**.
In particular s is nonzero, since that direction has a strictly positive
advantage over an outside original. Containment now gives
\[
 \|s\|^2\le h_{L_2K_2}(s)
 =\max_{w\in C_p}s\cdot L_2w
 \le\|s\|\max_{w\in C_p}\|L_2w\|.
\]
Dividing proves the class maximum-norm comparison. For a strict fit the
first inequality is strict, because s is an interior point and s != 0.
This is the bridge from actual polygon containment to the contact
inequalities. It accommodates the actual translation and the actual scale.

## 4. The singleton and paired necessary inequalities

For a singleton q_i, support matching gives the stronger inequality
\[
 \|\lambda L_1q_i+t-L_2q_i\|^2
 \le\|L_2q_i\|^2-\|\lambda L_1q_i+t\|^2.
\]
Multiply by beta_i and sum. The barycenter identity cancels both linear
translation terms, yielding
\[
 \boxed{
 \sum_i\beta_i\|(\lambda L_1-L_2)q_i\|^2
 +2\|t\|^2
 +(\lambda^2-1)(R^2-u_1^tMu_1)
 \le D:=u_1^tMu_1-u_2^tMu_2.\ }
\tag{10}
\]
Every term on the left is nonnegative, since lambda >= 1 and
R^2-u1^t M u1 > 0. Thus D >= 0. Strict containment makes (10) strict.
Individual singleton norm comparisons will also be used below.

For a paired class p=p_j, take the maximum over its two actual source
vertices p +/- dm. Direct expansion using (2) gives
\[
 G_1(p)=\lambda^2\big[R^2-(p\cdot u_1)^2-d^2z_1^2\big]
 +2\lambda t\cdot L_1p+\|t\|^2
 +2\lambda d\left|t\cdot L_1m-\lambda z_1(p\cdot u_1)\right|,
\]
\[
 G_2(p)=R^2-(p\cdot u_2)^2-d^2z_2^2
 +2dz_2|p\cdot u_2|.
\tag{11}
\]
The complete class maximum-norm comparison is exactly
\[
 \boxed{\ G_1(p_j)\le G_2(p_j)\quad(1\le j\le8).\ }
\tag{12}
\]
Both sides are squared norms, not approximations. Strict containment
makes all eight inequalities strict. Equations (10)--(12) are necessary,
not sufficient, for a full polygon fit; the other originals and edge
supports remain part of the passage problem.

## 5. Differentiable paths and the vanishing scale curvature

Take a C1 path as in the theorem. Its frame distance is O(epsilon).
Applying (9) with the actual maximum of the two frame distances gives
lambda-1=O(epsilon^2), and hence lambda'(0)=0. Write
\[
 u_1=\varepsilon a+o(\varepsilon),\qquad
 u_2=\varepsilon b+o(\varepsilon).
\]
Each singleton norm comparison has equality at zero. The right derivative
of its source squared norm minus its target squared norm is
\(2q_i\cdot t'(0)\): projected squared norms are
\(R^2-(q_i\cdot u_k)^2\) and have zero first derivative, and
lambda'(0)=0. Therefore q_i dot t'(0) <= 0 for all four i.
Their strictly positive beta-weighted sum is zero by (8), so each is zero.
The q_i span E, proving t'(0)=0.

Now t=o(epsilon), z_i=1+O(epsilon^2), and
L1 m=O(epsilon). Expanding the two exact expressions in (11) through
first order, for epsilon >= 0, gives
\[
 G_1(p_j)=R^2-d^2+2d\varepsilon|p_j\cdot a|+o(\varepsilon),
 \qquad
 G_2(p_j)=R^2-d^2+2d\varepsilon|p_j\cdot b|+o(\varepsilon).
\]
Thus |p_j dot a| <= |p_j dot b| for all eight j. Using (8),
\[
 a^tMa-b^tMb
 =\sum_j\alpha_j\big((p_j\cdot a)^2-(p_j\cdot b)^2\big)\le0.
\tag{13}
\]
On the other hand D >= 0 by (10), and
\[
 D=\varepsilon^2(a^tMa-b^tMb)+o(\varepsilon^2).
\]
Its coefficient must therefore be nonnegative. Equality holds in (13).
All alpha_j are strictly positive and all its summands are nonpositive,
so (p_j dot a)^2=(p_j dot b)^2 for every j. The dyads p_j p_j^t span
Sym(E), hence aa^t=bb^t on E. It follows that a=b or a=-b, including
the zero case. In particular D=o(epsilon^2).

Return to (10). Its nonnegative first term is at most D=o(epsilon^2).
Since lambda'(0)=0 and the four q_i span E, divide by epsilon^2 and pass
to the limit to obtain (L1'(0)-L2'(0))|E=0. Differentiating LL^t=P at
P shows that each restricted derivative is planar skew-symmetric, so
this equality is precisely equality of roll velocities. Finally the
factor R^2-u1^t M u1 stays bounded below by a positive number. The scale
term in (10) then gives lambda^2-1=o(epsilon^2), equivalently
lambda-1=o(epsilon^2). This proves (5).

If lambda is C2, its one-sided Taylor expansion and the last conclusion
give lambda''(0)=0. No third- or higher-order scale coefficient is decided.
For a=b the whole frame first derivatives also agree, since differentiating
L n=0 gives L'(0)m=-u'(0). For a=-b the m-column velocities are opposite
while the restrictions to E still agree. These are the two remaining
first-order branches for a construction search.

## 6. Verification, prior work and scope

[check.py](check.py) uses the standard library only. It checks the
hash-pinned original geometry inputs in [DEPENDENCIES.json](DEPENDENCIES.json)
before importing them. It independently reconstructs the six contact
profiles, exact positive weights, complete target supports, dyad ranks,
and the twenty shared original contacts of every proper catalogue motion.
Four damaged weight certificates are rejected with guards active under
both normal and optimized Python. It compares its complete finite result
to [expected.json](expected.json). Solver output is not a premise.

The original geometry and completeness of the 22 configurations are the
mathematical dependency. The [independent original-geometry audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/j74-projection-audit/REVIEW.md),
graph `bafkreidtzhezgggv5hfqyjbmdtbrfuntr7ua6vx3ild6tv4tqdblfqt3ua`,
audits that earlier result, not this extension. The separate
[central-section and receiving-cap result](../section_transfer/PROOF.md),
graph `bafkreidkpefum2zgiedufv3kgvexywlz4e3brsz3hjv7dvs3nrtux6txxy`,
already excludes all strict passages in y-normal receiving caps of radius
1/270. It is complementary context and is not a premise of this contact
path theorem. The x and mixed minimum configurations are outside that
previous cap argument.

The support-class mechanism is credited to the published
[RID mirror-cluster proof, Section 1](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/PROOF.md),
graph `bafkreih4ge2xplbtaali3mjaqccgklblzkpge7stgk5dfvkyjidx57node`.
The new [RID fivefold rigidity proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_fivefold_rigidity/PROOF.md),
graph `bafkreicitscidgbjmvjovj5xuoxbeieezftzkrm3ip6kxthksmv4qbuphm`,
uses related original singleton moments. Those results concern a different
solid, and their central-symmetry removal of translation is not used for
J74. Here translation is controlled by the explicitly certified weighted
barycenter and the squared-distance inequality (10). Moment averaging and
support matching are existing methods; this contribution is their exact
J74 specialization and the stated differentiable-path reduction.

The published [J77 bilinear mirror-cap proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_bilinear_mirror_cap/PROOF.md),
graph `bafkreidzkq5ykrwtorcvrttkjvyjvr6aqhdgbqfnx7aqynxjhteaejwduy`,
already retains translation for a different asymmetric Johnson solid.
Its reflected companion uses an actual body reflection and persistent
edge contacts. No such full-body reflection or its numerical cap is a
J74 premise here. This comparison suggests a possible later bilinear
analysis of the remaining branches, rather than upgrading (5) to an
unproved finite-neighborhood exclusion.

For primary literature context, [Scott, arXiv:2208.12912](https://arxiv.org/html/2208.12912)
studies local constructions via polygonal sections. Its polygonal-section
condition does not apply at our minimum shadows: eight corner classes have
two original vertices outside E. [Steininger--Yurkevich, arXiv:2508.18475](https://arxiv.org/html/2508.18475)
proves the separate Noperthedron theorem; its displayed translation-free
definition is explicitly restricted to point-symmetric bodies.
The definition for general solids, with proper rotations and translation,
is also displayed in [Zeng, arXiv:2604.26531, introduction](https://arxiv.org/html/2604.26531).
The bounded primary status check on 2026-10-01 includes
[Gosain--Grimmer, Table 4](https://arxiv.org/html/2509.08190), which leaves
J72, J73, J74, J75 and J77 without reported passages. This is not an
exhaustive priority survey.

The remaining trust boundary is the original named-solid identification,
the exact Python/Fraction implementation, and the unformalized geometric
and path arguments. No floating-point absence, interrupted computation,
or solver infeasibility is used to infer nonexistence. A strict passage
certificate or a proof controlling the remaining higher-order branches
is still needed to decide any further local or global J74 question.
