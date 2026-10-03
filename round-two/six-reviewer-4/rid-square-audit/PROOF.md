# Independent RID collar classification with its exact first companion

Actual author: **six-reviewer-4, independent mathematical reviewer**, 2026-10-03.
This is ordinary, unformalized mathematics with freshly reconstructed exact
finite hypotheses. The definition of the standard solid and classical
convexity/Cayley facts are explicit trust boundaries.

Let \(\phi=(1+\sqrt5)/2\). Let \(K\) be the convex hull of all signed cyclic
permutations of \((1,1,\phi^3),(\phi^2,\phi,2\phi),(2+\phi,0,\phi^2)\).
These are the sixty original edge-two standard RID vertices. Labels below
sort the three rational coefficient pairs in the basis \((1,\phi)\), as in
the target; the actual arithmetic here uses \((1,\sqrt5)\).

Put
\[
 \ell=2\phi-3,\quad s=2-\phi,\quad U=(0,1,0),\quad
 r=(x,0,1),\quad \ell\le x\le s,
\]
\[
 c_*={1\over5}(4-3\phi,0,3-\phi),\quad R_*=R(c_*),\quad
 R(d)v={(1-d\cdot d)v+2d(d\cdot v)+2d\times v\over1+d\cdot d},
\]
and let \(P_r=I-rr^T/(r\cdot r)\). Define
\[
 \rho={2\phi-3\over4-\phi}={5\sqrt5-9\over22},
 \qquad {1\over11}<\rho<{1\over10}.
\]

**Centered-collar classification.** For every original physical
\(t\in r^\perp\), every real \(\lambda\ge1\), and every real physical LEFT
relative Cayley vector \(\|d\|\le\rho\),
\[
 \lambda P_rR(d)R_*K+t\subseteq P_rK
\]
holds exactly when \(\lambda=1,t=0\), and either
\[
 d=0,
 \qquad\hbox{or}\qquad x=s,\ d=-\rho U.                 \tag{A}
\]
Consequently the isolated-center result of LEMMA10074 holds on every closed
ball of radius strictly smaller than \(\rho\), including \(1/11\), and on
the whole open ball of radius \(\rho\). This open radius is sharp uniformly
over the closed receiver segment: the displayed second pose is a fit on its
boundary, and hence belongs to every larger open or closed ball. The
isolated-center conclusion fails on the closed ball of radius \(\rho\).

**Companion-set corollary.** Let \(G=\{g\in SO(3):gK=K\}\),
\(H_r=2rr^T/(r\cdot r)-I\), and
\(E(r)=R_*G\cup H_rR_*G\). For every proper original \(Q\), assume
\[
 \operatorname{tr}(Qe^T)\ge {25+12\phi\over15}
       \quad\hbox{for some }e\in E(r).                    \tag{B}
\]
Then a fit with arbitrary original planar \(t\) and \(\lambda\ge1\) holds
exactly when \(Q\in E(r),\lambda=1,t=0\). Equivalently, the source gate in
(B) is the closed relative Cayley radius \(\rho\), or squared Frobenius
distance at most \((40-24\phi)/15\). No optimality of this **set** gate is
claimed. This is conditional localization, with no arbitrary-source entry
theorem and no global RID decision.

## 1. Fresh geometry and the whole fixed-source converse

The programs generate the full sixty-point set directly from the three
displayed seeds. They use the matrix definition
\((I+[c]_{\times})(I-[c]_{\times})^{-1}\) and exact adjugate inversion for
\(R_*\); all nine orthogonality entries, determinant one, and all sixty
matrix/Rodrigues image identities are checked. No target executable,
primitive library, certificate, expected record or earlier theorem is imported.

The original receiving cyclic list is
\[
 48,36,54,56,38,53,46,18,19,11,23,5,3,21,6,13,41,40.         \tag{C}
\]
Use planar coordinates \(\pi_x(v)=(v_x-xv_z,v_y)\). This linear map has
kernel \(\mathbb Rr\) and restricts to an isomorphism on \(r^\perp\), so
it preserves the required projected containment. No orthonormality is assumed.

For every one of the 816 ordered triples from (C), its turn determinant is
affine in \(x\): each determinant term contains one first planar coordinate.
All 1,632 endpoint values are nonnegative. All 816 midpoint values agree
entry by entry with affine interpolation. There is a strictly positive
triple at both endpoints, so the polygon remains nondegenerate. All 153
pair differences remain nonzero throughout the interval: either their fixed
second coordinate differs, or their sole possible first-coordinate coincidence
lies outside the interval. These are continuum statements derived from affine
identities, rather than inference from a sampled plot.

These controls put every other listed point to the left of each directed
consecutive segment, including the wrapping segment. Thus each is a boundary
support segment of the nondegenerate convex hull. The complete cyclic triple
order and distinctness force traversal in one direction and once: a reversed
collinear segment would reverse the sign of its triple with an off-line point;
a repeated circuit would reverse some triple or repeat a point. Consequently
the corresponding inward halfplanes intersect in this hull, with consecutive
collinear boundary points allowed.

For an edge \(V_a\to V_b\) in (C), put
\(m(x)=(V_b-V_a)\times r\) and \(H(x)=m(x)\cdot V_a\).
For all sixty original receiving vertices and all sixty moving vertices,
the gaps \(H-m\cdot V_j\) and \(H-m\cdot R_*V_j\) are affine in \(x\).
All 4,320 endpoint values are nonnegative, all 2,160 midpoint comparisons
agree with exact affine interpolation, heights are positive, and all eighteen
normals are nonzero throughout the interval. The latter is checked using their
constant first component, or the exact zero criterion for their affine second
component when the first component is zero.

Therefore the listed hull is exactly \(\pi_x(K)\), and every
\(\pi_x(R_*V_j)\) lies in it for the entire closed interval. This proves
\(P_rR_*K\subseteq P_rK\) directly. Independently constructed monotone-chain
hulls of the complete sixty-point projections agree with the hulls of (C) at
both endpoints and the midpoint, and contain all sixty moving points there.
These extra checks corroborate the original-coordinate and orientation bridges;
the affine argument proves the continuum. No older fixed-source claim9896
is a mathematical premise.

## 2. Paired squares retain scale and original translation

Put \(h=\phi^3=1+2\phi\). Both full literal bodies \(K,R_*K\) lie between
the supports \(U\cdot v=\pm h\). The receiving positive square has original
labels 18,19,46,47, with negative labels 12,13,40,41. The moving positive
square has original labels 35,39,47,53, and negative labels 6,12,20,24.
Its four corners are \(hU\pm u\pm v\), where
\[
 u={1\over5}(4\phi-2,0,1-2\phi),\qquad
 v={1\over5}(1-2\phi,0,2-4\phi).
\]
All 240 signed whole-body height gaps, the literal corner sets and the
orthonormal identities for \(U,u,v\) are checked independently.

Write \(d=(d_x,b,d_z)\), \(p_\perp=\sqrt{d_x^2+d_z^2}\),
\(N=1+p_\perp^2+b^2\), and let \(\psi\) be the angle between \(U\) and
\(R(d)U\). Direct Rodrigues algebra gives
\[
 \cos\psi=1-{2p_\perp^2\over N}>0,
 \qquad \sin\psi={2p_\perp\sqrt{1+b^2}\over N}.           \tag{D}
\]
Positivity follows from \(\rho<1/10\). The rotated positive square's
maximum height is
\(M=h\cos\psi+|U\cdot R(d)u|+|U\cdot R(d)v|\).
Its actual negative is a moving face too. Their receiving support inequalities
give \(\lambda M\pm U\cdot t\le h\); addition cancels the unrestricted
original translation. Since \(M>0\) and \(\lambda\ge1\), \(M\le h\).
Orthonormality gives the lower bound \(M\ge h\cos\psi+\sin\psi\).

If \(p_\perp>0\), substitution of (D) and division by the positive
\(2p_\perp\) imply
\[
 \sqrt{1+b^2}\le h p_\perp\le h\rho<1,
\]
a contradiction. The exact checked margin is
\(1-h^2\rho^2=(215-7\sqrt5)/242>0\).
Thus \(d=zU\). The squares keep heights \(\pm h\), so the original
inequalities \(\lambda h\pm U\cdot t\le h\) give
\(\lambda=1,U\cdot t=0\). No initial centering or scale normalization has
been used, and the other translation coordinate remains unrestricted.

## 3. The exact axis classification

The genuine receiving normals from edges 48 to36 and36 to54 are denoted
\(m_0,m_1\), with heights \(H_0,H_1\). All their positive and negative
supports are already certified in section1, since the body is centrally
symmetric. Opposite moving points and receiving supports imply the necessary
inequalities \(m_i\cdot R(zU)R_*V_j\le H_i\) for every original source
point, after deriving \(\lambda=1\).

Put \(A=1+c_*\cdot c_*=(12-4\phi)/5>0\) and
\[
 P_{ij}=A(1+z^2)[m_i\cdot R(zU)R_*V_j-H_i].
\]
The fresh code derives all 120 such full polynomials directly from the
physical vertices and rotation numerator, and independently checks each on
an exact affine/quadratic unisolvent grid (720 full comparisons). All six
coefficients of each selected row match the written target's table.

For rows \((0,32),(0,40),(1,36)\), abbreviate \(P_{32},P_{40},P_{96}\).
Then
\[
 P_{32}={8(2\phi-1)\over5}z[2x-1-(x+2)z].               \tag{E}
\]
The bracket is increasing in \(x\) and decreasing in \(z\) throughout
\([\ell,s]\times[-\rho,\rho]\). Its maximum is zero, attained only at
\((s,-\rho)\), by the definition of \(\rho\). If \(z<0\), the necessary
\(P_{32}\le0\) therefore forces exactly this endpoint corner. If
\(\|d\|<\rho\), the bracket is strictly negative, so \(z<0\) is impossible.

For \(P_{40}=a_{40}(z)x+b_{40}(z)\),
\(P_{96}=a_{96}(z)x+b_{96}(z)\), the full reconstructed coefficients give
\[
 b_{40}a_{96}-b_{96}a_{40}={64\over5}(3-\phi)z^2(1+z^2). \tag{F}
\]
On \([0,\rho]\), \(a_{40}<0\) and \(a_{96}/z>0\), with the value of the
second expression at zero interpreted as its polynomial extension. Their
complete Bernstein controls, in the \((1,\sqrt5)\) basis, are
\[
 a_{40}:\quad {4-4\sqrt5\over5},\quad
 {58-42\sqrt5\over55},\quad {2516-1212\sqrt5\over605};
\]
\[
 a_{96}/z:\quad 8+{16\sqrt5\over5},\quad
 {68\over11}+{212\sqrt5\over55}.
\]
The first three are strictly negative and the last two strictly positive by
exact rational-square sign comparisons. If \(z>0\), \(P_{40}\le0\) forces
\(x\ge-b_{40}/a_{40}\), and hence
\[
 P_{96}\ge{b_{40}a_{96}-b_{96}a_{40}\over-a_{40}}>0,
\]
contradicting its actual receiving support. Thus only \(z=0\) or the single
negative endpoint corner can survive. This includes every closed gate and
receiver boundary; no limiting case is dropped.

## 4. Actual translation closure and boundary sufficiency

The actual normal is
\(m_0=(1,1-\phi(1+x),-x)\), so \(m_0\times U=r\ne0\).
At \(z=0\), the original source32 touches this support throughout the
segment, as does its antipodal point at the opposite support. At the critical
corner it still touches, because (E) is exactly zero. Thus in either surviving
case the original constraints give \(m_0\cdot t=0\). Together with
\(U\cdot t=0\) and \(t\in r^\perp\), this proves \(t=0\).

At \((x,z)=(s,-\rho)\), all 1,080 original moving-point support gaps against
the eighteen actual receiving edges are checked to be nonnegative. An
independent sixty-point monotone-chain hull check confirms containment.
Thus \(Q_c=R(-\rho U)R_*\) is a genuine proper unit-scale touching fit,
with original \(t=0\). This is an explicit exact witness, rather than a
failed exclusion or a first-order prediction. Section1 proves the other
surviving converse. The pair of cases proves (A) and its sharp open radius.

## 5. The endpoint companion and physical covariance

Let
\[
 g_s={1\over2}
 \begin{pmatrix}
 -\phi&1-\phi&1\\
 1-\phi&-1&-\phi\\
 1&-\phi&\phi-1
 \end{pmatrix}.
\]
The checker verifies \(g_s^Tg_s=I,\det g_s=1\), its entire sixty-point
permutation of the original vertices, and every entry of
\[
             Q_c=H_{(s,0,1)}R_*g_s.                       \tag{G}
\]
In particular the boundary pose is an actual member of the already defined
companion set. No enumeration or pose count for the whole group is needed.

For a proper relative rotation, the Cayley parameter is unique whenever its
trace is greater than \(-1\), and
\[
 \operatorname{tr}R(d)={3-\|d\|^2\over1+\|d\|^2},\qquad
 \|R(d)-I\|_F^2={8\|d\|^2\over1+\|d\|^2}.
\]
At \(\rho\), the trace is \((25+12\phi)/15\). Hence (B) is precisely the
physical relative Cayley gate, including its closed boundary.

If its center is \(e=R_*g\), right multiplication by \(g^{-1}\) preserves
the moving set and relative metric; apply (A). The exceptional endpoint case
is \(Q_cg\in H_rR_*G\) by (G). If the center is \(H_rR_*g\), first
multiply on the left by \(H_r\), then on the right by \(g^{-1}\). Since
\(P_rH_r=-P_r\) and the actual receiving shadow is centrally symmetric,
this maps the original fit to another with translation \(-t\), the same
scale and the same gate. Applying (A) and undoing these proper actions leaves
exactly a member of \(E(r)\). Conversely every member of \(E(r)\) has the
fixed-source shadow or its negative and therefore fits. This proves (B)'s
classification while retaining the original translation, scale and SET ties.

The square supports rule out every strict passage in these gates. The receiver
segment remains one dimensional. Unknown source entry, receivers off this
segment, and the global named-solid conjecture remain outside this proof.
