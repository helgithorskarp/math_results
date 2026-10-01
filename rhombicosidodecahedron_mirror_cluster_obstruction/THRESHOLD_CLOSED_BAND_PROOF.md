# Closed RID passages on the 83/200 height band: a continuous exceptional plane

**six-rupert-3, researcher; 2026-10-01.** Complete written intermediate
proof with exact author-checked finite hypotheses. Unformalized and
independently unreviewed. Historical priority and sharpness are unasserted.
The global Rupert property of the rhombicosidodecahedron remains **OPEN**.

Let \(\phi=(1+\sqrt5)/2\). Use the ORIGINAL sixty distinct vertices obtained
by even coordinate permutations and independent signs from
\[
 (1,1,\phi^3),\qquad (\phi^2,\phi,2\phi),\qquad (2+\phi,0,\phi^2).
\]
They give the standard edge-two rhombicosidodecahedron
\(K=\operatorname{conv}V=-K\). All have squared radius
\(R^2=7+8\phi\). For a unit receiving normal \(n\), set
\[
 P_n=I-nn^t,\quad f(n)=\min_{v\in V}|v\cdot n|,\quad
 q=83/200,\quad \beta=(19-8\phi)/29,\quad J_n=2nn^t-I.
\]
For a nonzero raw normal \(u\), \(P_u=I-uu^t/(u\cdot u)\) denotes the
same projection. Let \(G\subset SO(3)\) be the actual sixty-element proper
body group, \(gK=K\). Define
\[
 a=(2\phi-1)/5,\qquad
 D=\begin{pmatrix}-1&0&0\\0&a&-2a\\0&-2a&-a\end{pmatrix}.
 \tag{1}
\]
This is the actual proper cross-class alignment, with \(D^t=D\),
\(D^2=I\), and \(D\notin G\).

The directed signed region of a unit reference \(m\) consists of unit
\(n\) satisfying \((v\cdot n)(v\cdot m)>0\) for every ORIGINAL \(v\).
The winning reference has raw ray \(B=(0,2-\phi,1)\). The two proper
threshold reference classes have the actual raw representatives
\[
 r_L=(0,(2-\phi)/3,-1),\qquad r_H=(0,1,(3\phi-1)/11),
 \qquad m_t=r_t/\|r_t\|.                                    \tag{2}
\]
In particular the LOW raw normalization in (2) is retained in every
box formula; a differently scaled representative cannot be substituted
while keeping those formulas fixed.

**Theorem.** Let \(n_{\rm phys}\) be ANY unit original receiving normal
with \(f(n_{\rm phys})\ge q\), \(Q\in SO(3)\) ANY original proper source
rotation, \(t\in n_{\rm phys}^{\perp}\), and \(\lambda\ge1\). Then
\[
 \lambda P_{n_{\rm phys}}(QK)+t\subseteq P_{n_{\rm phys}}K       \tag{3}
\]
holds exactly for \(\lambda=1,t=0\) and the following rotations.
Every such receiver is winning or threshold. In the threshold case
choose an actual receiving body fold \(U\in G\) so that
\(n=U^tn_{\rm phys}\) is in the LOW or HIGH region in (2), and put
\[
 u=\frac{\|r_t\|}{m_t\cdot n}n.                              \tag{4}
\]
The denominator is positive on this band, as proved below.

| receiving normal | complete actual proper source orientations | count |
| --- | --- | --- |
| winning | \(G\cup J_{n_{\rm phys}}G\) | 120 equality orientations |
| LOW threshold | \(G\cup J_{n_{\rm phys}}G\) | 120 equality orientations |
| HIGH threshold, \(u_x\ne0\) | \(G\cup J_{n_{\rm phys}}G\) | 120 equality orientations |
| HIGH threshold, \(u_x=0\) | \(G\cup J_{n_{\rm phys}}G\cup UDG\cup J_{n_{\rm phys}}UDG\) | 240 orientations: 120 equality, 120 unequal touching |

The cosets are disjoint in the stated cases. All factors involving the
moving receiving half-turn are on the **LEFT**; independent original
source body factors are on the **RIGHT**. The extra cosets can equivalently
use \(D_{\rm phys}=UDU^t\), since \(UDG=D_{\rm phys}G\).

This extends the [critical-axis closed classification](THRESHOLD_RECEIVER_PROOF.md),
graph7520, to the full original \(q\) receiving band. The new extra
motions exist along a continuous HIGH plane segment, including ordinary
noncritical normals. The [published q83 proof](GLOBAL_BAND_83_PROOF.md),
graph8330/source6fbe50d0b130848b62786212c29dbfd307383a3a, had established
the winning row and excluded every strict threshold passage, without
classifying closed threshold passages. Its global strict cutoff
\(f(n)<83/200\), squared-height gap \(1/28\), and unresolved receiving
complement are unchanged by this theorem.

## 1. The original placement and the all-Q zero-motion reduction

For an original placement (3), the source and receiving shadows are
centrally symmetric. Reflection and convex midpoints remove the
physical \(t\) without changing \(n_{\rm phys},Q\). Contraction toward
the origin removes \(\lambda\ge1\). Hence
\[
 P_{n_{\rm phys}}(QK)\subseteq P_{n_{\rm phys}}K.               \tag{5}
\]
This reduction gives a necessary orientation condition; scale and
physical translation will be recovered from ORIGINAL supports below.
For this antipodal equal-radius body,
\[
 \operatorname{diam}(P_nK)^2=4(R^2-f(n)^2),
 \qquad f(Q^tn_{\rm phys})\ge f(n_{\rm phys})\ge q.           \tag{6}
\]
Indeed the largest projected original norm is
\(\sqrt{R^2-f(n)^2}\), and an original and its antipode attain twice it.

The inherited complete [signed-region spectrum](GLOBAL_CAP_PROOF.md),
graph7256, has 436 projective strict regions: ten winning maxima \(1/3\),
sixty threshold maxima \(\beta\), and 366 other maxima at most \(1/7\).
Since \(q^2>1/7\), both actual normals in (6) are winning or threshold;
neither can lie on an original zero-height wall. This complete spectrum
is a byte-pinned inherited dependency and is not reenumerated here.

For winning receivers, the complete original closed classification in
[GLOBAL_BAND_83_PROOF.md](GLOBAL_BAND_83_PROOF.md), Sections1,2,5, gives
the first row of the theorem. The original mixed
[threshold-to-winning exclusion](MIXED_PAIR_ROLL_PROOF.md), graph8270,
is part of that classification. For a threshold receiver,
the [winning-to-threshold exclusion](GAMMA_BRANCH_PROOF.md), graph8138,
rules out closed containment of every original winning source at \(q\),
including all rolls. Thus both normals are threshold.

Here is the precise CLOSED conclusion used from graph8330, whose
threshold derivation in Sections3--5 starts with (5), rather than
requiring strict containment. Independent actual receiving and right
source body factors give a proper gauged \(Q'\), with receiving normal
in one of the two regions (2) and actual source normal \(Q'^tn\) in
one of them. For all four ordered class pairings the actual alignment
is \(I\) for equal classes and the SAME matrix \(D\) in (1) for unequal
classes. The complete original candidate pools have 8 and 12 elements;
all 384 and 5760 signed antipodal injections are checked. The only
proper circle survivors are shifts0,4. Proper oriented circle order
excludes both metric reversals. Actual LEFT multiplication by \(J_n\)
absorbs shift4 without changing the projected source set.

In that gauge, put \(A=Q'D_t^t\), where \(D_t=I\) or \(D\).
The matched ORIGINAL radial inequalities and positive original moment
matrix force the full spatial angle of \(A\) below \(9/100\), and its
actual Cayley norm below \(1/22\). This is derived for arbitrary
original \(Q\); no small full-angle or initial roll premise is imposed.
All16 original contact preimages \(D_t^tv\in V\) are checked for
every ordered pairing. The complete signed closed-axis covers exclude
EVERY nonzero local Cayley vector, even for CLOSED inequalities.
Consequently \(A=I\), so \(Q'=D_t\).

The new checker fully replays all 97277 parent expected bytes: 198 closed
leaves, 9906 strict exact coefficients, 9480 original corner supports,
158 contact identities, all 6144 assignments, all four actual pairings,
and the parent's 36 malformed-evidence controls. The generic continuous
proper-gauge, matching, moment and Cayley bridges are in the complete
parent proof. The inherited spectrum and two mixed branches are pinned
dependencies; their production checkers are not recursively rerun.

Undoing the source body factor and the LEFT antipodal gauge proves that
for a canonical threshold receiver all possibilities in (5) are
\[
 Q\in G\cup J_nG\cup DG\cup J_nDG.                         \tag{7}
\]
Equation (7) is a necessary closed orientation reduction, not a claim
that all four cosets contain their other original vertices. The new
affine lemmas decide exactly which of these candidates do contain them.

## 2. The full raw enclosures and the affine method

The actual derived threshold chord bound in graph8330 is
\[
 d=\frac{42008277980669}{1846406179243000}.
\]
For each canonical threshold normal on the original \(q\) band,
\(\|n-m_t\|\le d\). Put
\[
 z_0=1-d^2/2>0,\qquad
 \alpha=\frac{17d}{16z_0},\quad \gamma=\frac d{z_0},\quad
 b_t=(0,-r_{t,z},r_{t,y}).                                   \tag{8}
\]
Let \(\mathcal U_t\) be the closed four-corner box
\[
 \{r_t+x(1,0,0)+yb_t:|x|\le\alpha,\ |y|\le\gamma\}.
 \tag{9}
\]
The raw representative (4) lies in (9). Indeed
\(m_t\cdot n\ge z_0\), \(\|r_t\|<17/16\), and the tangent
component of \(n\) has norm at most \(d\). These give respectively
the x bound \(\alpha\) and the coefficient bound \(\gamma\).
The checker regenerates (8)--(9) from the freshly replayed parent
records and verifies all four corners and both actual raw references.
Every raw point in (9) is nonzero since \(u\cdot r_t=\|r_t\|^2\).

For fixed vectors \(e,p,v\),
\[
 (e\mathbin\times u)\cdot(p-v)
\]
is affine in \(u\). Corner bounds extend to the entire closed box;
endpoint bounds extend to the entire closed segment. A positive or
negative bound verified with the same sign at both endpoints stays
strict. The functional \(e\times u\) is perpendicular to \(u\), so
its values on originals equal its values on their actual projections.

The next lemmas hold for the fixed matrix \(D\) on ENTIRE boxes (9),
including box points with \(f(u/\|u\|)<q\). The all-original-Q reduction
(7) and the theorem are asserted on the original height band, where
their parent hypotheses apply. Full-box fixed-D assertions are not
silently extended to all other rotations outside that band.

## 3. A uniform LOW separation

Use the constant vector and ORIGINAL source
\[
 e=(1,\phi,\phi-1),\qquad p=(2+\phi,0,-1-\phi),
 \quad Dp=(-2-\phi,(2+6\phi)/5,(1+3\phi)/5).                  \tag{10}
\]
At all four LOW corners the checker compares \(Dp\) to ALL60 original
receiving vertices and verifies
\[
 (e\times u)\cdot(Dp-v)>1/4\qquad(v\in V).                  \tag{11}
\]
The least of these 240 original gaps is
\[
 \frac{-83013884329165624355549912072818+
       55041381350077290892053083363362\phi}
      {20450000586223697184449280937317}>1/4.
\]
By affinity (11) holds throughout \(\mathcal U_L\); the receiving
maximizer may change. Thus \(P_uDp\) is outside \(P_uK\), and
\(P_uDK\not\subseteq P_uK\) everywhere on the LOW box.
Centrality and the midpoint/contraction reduction exclude every
scaled translated closed D placement with \(\lambda\ge1\) there.
The \(J_nD\) candidate has the same projected shadow because
\(P_nJ_n=-P_n\) and \(DK=-DK\). Hence only the first two cosets
of (7) can survive for a LOW receiver.

## 4. HIGH off-plane: two complete signed half-box witnesses

Set \(c=(12\phi-16)/5>0\). Divide \(\mathcal U_H\) at \(u_x=0\).
Each signed half-box has four corners: the two x=0 midpoints of the
original box corners and the two outer corners of the chosen sign.
Use the following fixed ORIGINAL receiving endpoints and sources:

| sign \(s\) | \(v\) | \(w\) | original source \(p_s\) |
| --- | --- | --- | --- |
| \(-1\) | \((-1-2\phi,-1,-1)\) | \((-1-2\phi,-1,1)\) | \((1+2\phi,-1,1)\) |
| \(+1\) | \((-1-2\phi,1,1)\) | \((-1-2\phi,-1,1)\) | \((1+2\phi,-1,-1)\) |

Write \(e_s=w-v\), \(\mu_s(u)=e_s\times u\). All endpoints and
sources are checked to belong to \(V\), and \(\|e_s\|^2=4\).
At every corner of its half-box the checker verifies
\[
 \mu_s(u)\cdot(v-z)\ge0\quad(z\in V),\qquad
 h_s(u)=\mu_s(u)\cdot v>0,\qquad
 \mu_s(u)\cdot(Dp_s-v)=c s u_x.                              \tag{12}
\]
These are 480 original receiving support comparisons, eight positive
support values and eight exact protrusion identities. Every expression
is affine, so (12) holds on each WHOLE closed half-box. If \(u_x\ne0\),
the corresponding ORIGINAL D-source protrudes strictly through an
actual receiving support. Centrality and contraction again exclude
every physical translation and scale at least1. Thus on the HIGH box
the cross candidates of (7) can survive only at \(u_x=0\).

## 5. HIGH on-plane: the whole closed segment contains the original DK

Let
\[
 u_-=r_H-\gamma b_H,\qquad u_+=r_H+\gamma b_H.                 \tag{13}
\]
The entire plane section of (9) is the closed segment \([u_-,u_+]\).
Take the fixed ORIGINAL receiving sequence
\[
\begin{array}{ll}
v_0=(-1-2\phi,-1,1),&v_1=(-2-\phi,0,1+\phi),\\
v_2=(-1-\phi,-\phi,2\phi),&v_3=(-1,-1,1+2\phi),\\
v_4=(1,-1,1+2\phi),&v_5=(1+\phi,-\phi,2\phi),\\
v_6=(2+\phi,0,1+\phi),&v_7=(1+2\phi,-1,1),\\
v_{i+8}=-v_i\quad(0\le i<8).&
\end{array}                                                  \tag{14}
\]
Use cyclic indices, \(e_i=v_{i+1}-v_i\),
\(\mu_i(u)=e_i\times u\). All16 originals and their distinctness
are checked. At BOTH endpoints (13), for EVERY facet and ALL60 original
receiving and source vertices, the checker verifies
\[
 \begin{split}
 &\mu_i(u)\cdot(v_i-z)\ge0,\qquad
   \mu_i(u)\cdot(v_i-Dz)\ge0\quad(z\in V),\\
 &h_i(u)=\mu_i(u)\cdot v_i>0,\qquad
   u\cdot(e_i\times e_{i+1})>0.                              \tag{15}
 \end{split}
\]
These are 1920 receiving and 1920 D-source comparisons, 32 positive
supports and 32 strictly positive consecutive turns. All are affine
in \(u\), and therefore hold on the ENTIRE closed segment.

The projected vertices remain pairwise distinct along the segment,
which is also verified directly. For each of all120 original pairs,
112 have unequal fixed x coordinates. For the remaining eight, let
\(\Delta=v_j-v_i\); the affine chart separation
\((u\times(1,0,0))\cdot\Delta\) has one strictly nonzero sign at
both endpoints. Since \(u_x=0\), the x axis lies in \(u^\perp\),
and these two chart coordinates distinguish the actual projections
throughout the segment. No projected vertex collision is possible.

The first inequalities of (15) make every projected segment
\([P_uv_i,P_uv_{i+1}]\) a receiving support segment. The strictly
positive consecutive turns make its adjacent support lines distinct
and meeting at an exposed corner. Thus every listed vertex is a
strict convex corner of \(P_uK\), and each listed segment joins
successive corners of its convex boundary. Following these successors
through the sixteen distinct vertices returns to the start and gives
the ENTIRE receiving polygon. Its sixteen supporting half-planes
therefore have intersection exactly \(P_uK\). The D-source inequalities
in (15) put every projected ORIGINAL D-source in that intersection.
Convexity gives
\[
 P_uDK\subseteq P_uK\qquad(u\in[u_-,u_+]).                   \tag{16}
\]
This is an endpoint-affine proof of continuous containment, rather
than a conclusion from finitely many successful passage tests.

## 6. The original scale and translation on the plane

Two fixed ORIGINAL sources supply exact shared support contacts
throughout this segment:
\[
 p_1=(1+\phi,-2-\phi,0),\qquad
 p_2=(1,-1-2\phi,-1),\qquad Dp_1=v_2,\ Dp_2=v_3.             \tag{17}
\]
They contact facets1,2 respectively. The checker verifies at BOTH
endpoints that
\[
 \mu_i(u)\cdot(v_i-Dp_i)=0\quad(i=1,2),
 \qquad u\cdot(e_1\times e_2)>0.                            \tag{18}
\]
The first identities and the strict determinant extend by affinity
to the entire segment. Here \(e_1\times e_2=(-2,0,2\phi)\).
The identity
\[
 u\cdot((e_1\times u)\times(e_2\times u))
   =(u\cdot u)\,u\cdot(e_1\times e_2)                       \tag{19}
\]
makes the actual projected support normals \(\mu_1,\mu_2\) independent
in \(u^\perp\). Their positive support values \(h_i\) are from (15).

A hypothetical ORIGINAL scaled translated D containment, applied to
BOTH signs of the original sources (17), gives
\[
 \lambda h_i+|\mu_i\cdot t|\le h_i\quad(i=1,2).              \tag{20}
\]
Since \(\lambda\ge1\) and \(h_i>0\), necessarily
\(\lambda=1\), \(\mu_1\cdot t=\mu_2\cdot t=0\).
Independence and the physical constraint \(t\in u^\perp\) give
\(t=0\). Conversely (16) supplies containment for precisely those
values. Combining Sections4--6 proves the full fixed-D lemma
\[
 \lambda P_uDK+t\subseteq P_uK
 \quad\Longleftrightarrow\quad
 u_x=0,\ \lambda=1,\ t=0\qquad(u\in\mathcal U_H).            \tag{21}
\]
The \(J_nD\) source has exactly the same shadow as \(D\), so (21)
also handles that branch with the original scale and translation.
All these placements touch receiving supports and are never strict.

## 7. HIGH cross shadows are unequal throughout the box

The LOW separation has a reverse counterpart. Use the fixed receiving
ORIGINAL \(p\) in (10) and constant vector \(\widetilde e=De\).
At ALL four HIGH corners and for every ORIGINAL source \(z\in V\),
the checker verifies
\[
 (\widetilde e\times u)\cdot(p-Dz)>1/4.                     \tag{22}
\]
All240 exact comparisons extend by affinity to \(\mathcal U_H\).
Thus the actual receiving original \(P_up\) lies outside \(P_uDK\),
and
\[
 P_uK\not\subseteq P_uDK\quad(u\in\mathcal U_H).              \tag{23}
\]
In particular the contained HIGH plane shadow in (16) is unequal to
the receiving shadow everywhere on the segment.

The actual normalization clarifies this transported witness. With
\(c_r=(-3+9\phi)/11>1\), exact calculation gives
\[
 Dr_H=c_r r_L,\qquad Db_H=-c_r b_L.                          \tag{24}
\]
Consequently \(Du/c_r\) maps the HIGH box into the LOW box: its x
coefficient is \(-u_x/c_r\) and its tangent coefficient reverses sign.
Proper orthogonal cross-product covariance transports (11) to the
reverse inequality. The production checker verifies (22) directly
against all60 originals, as well as (24); the witness does not depend
on recognizing an approximate or symmetry-equivalent reference ray.

## 8. Exact continuous disjointness of the LEFT cosets

The checker freshly generates and verifies every matrix in \(G\).
Among them are exactly fifteen trace-minus-one proper body half-turns.
For each it supplies a nonzero actual fixed axis and an ORIGINAL
vertex perpendicular to that axis. This complete list proves, for
ANY unit \(n\),
\[
 J_n\in G\quad\Longrightarrow\quad f(n)=0.                 \tag{25}
\]
Therefore \(G\) and \(J_nG\) are disjoint whenever \(f(n)>0\),
including every receiving normal in the theorem.

For the four-coset statement on HIGH, one also needs
\(f(Dn)>0\). At all four corners of EACH raw threshold box, the
checker verifies strict ORIGINAL signs for \(u\) and \(Du\) relative
to \(r_t\) and \(Dr_t\):
\[
 (v\cdot u)(v\cdot r_t)>0,\qquad
 (v\cdot Du)(v\cdot Dr_t)>0\quad(v\in V).                   \tag{26}
\]
All960 scalar comparisons are regenerated. Their affinity makes
both minimum original heights strictly positive on the whole boxes.

Fix a HIGH box normal \(n=u/\|u\|\), and consider
\(G,J_nG,DG,J_nDG\). Every left coset has sixty proper rotations.
Their six possible overlaps are excluded as follows.

1. \(G\cap J_nG\ne\varnothing\) would give \(J_n\in G\),
   contradicting (25)--(26).
2. \(DG\cap J_nDG\ne\varnothing\) would give
   \(D^{-1}J_nD=J_{D^tn}\in G\), contradicting
   \(f(D^tn)>0\) and (25).
3. Either \(G\cap DG\ne\varnothing\) or
   \(J_nG\cap J_nDG\ne\varnothing\) would give \(D\in G\),
   excluded by the exact actual body enumeration.
4. Either of the remaining overlaps,
   \(G\cap J_nDG\ne\varnothing\) or
   \(J_nG\cap DG\ne\varnothing\), would give \(J_nD\in G\).
   Then \(J_nDK=K\), so
   \(P_nDK=P_nJ_nK=-P_nK=P_nK\), contradicting (23).

This proves FOUR disjoint left cosets throughout the HIGH box,
and exactly 240 distinct candidate proper rotations wherever all
four survive. Three finite exact coset constructions in the expected
record supplement this universal group/shadow proof; they are not
used as a continuum counting premise.

## 9. Actual folds, body orientations and completion

For a canonical normal, \(Q\in G\cup J_nG\) always gives equal
shadows, because \(K=-K\) and \(P_nJ_n=-P_n\). In an original
scaled translated containment of an equal shadow, its positive
two-dimensional area gives \(\lambda^2\le1\), hence \(\lambda=1\).
Then \(C+t\subseteq C\) for a nonempty bounded shadow \(C\) forces
\(t=0\): iterating any nonzero translation would contradict boundedness.

Sections3 and4 exclude the remaining two cosets for LOW and off-plane
HIGH. On-plane HIGH admits them by (16) and forces the original
\(\lambda=1,t=0\) by (20). They have unequal touching shadows by
(18) and (23). The counts follow from Section8. Together with the
inherited winning branch, this proves all canonical rows of the theorem.

For a physical receiving fold \(U\in G\), transform the actual
placement by \(U^t\). This keeps \(\lambda\) and sends the physical
planar translation to \(U^tt\). Undoing the fold uses
\[
 UJ_n=J_{Un}U,\qquad UG=G,
\]
so the cross cosets become exactly \(UDG,J_{Un}UDG\), and the
two body cosets become \(G,J_{Un}G\). A zero canonical physical
translation is a zero original physical translation. All actual
independent right source body factors stay on the right. No improper
source rotation or body-symmetry premise for \(D\) enters this step.

Normal reversal is harmless explicitly. The actual proper body matrix
\(L=\operatorname{diag}(1,-1,-1)\) belongs to \(G\), commutes with
\(D\), and sends both \(r_t\) to \(-r_t\). Replacing the physical
normal by its negative can use \(UL\) as receiving fold and canonical
raw representative \(-Lu=(-u_x,u_y,u_z)\). The exceptional plane is
preserved and \(ULDG=UDG\). Thus the asserted physical orientations
are independent of the normal sign. The same necessary-and-sufficient
proof holds for any actual body chart satisfying the stated signed
region, so chart selection does not change the resulting physical set.

## 10. Reproduction, scope of reviews and current status

Run separately from the repository root with Python3.11+ standard
library and all numerical thread counts1:

```bash
python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/threshold_closed_band_certificate.py
python3 -B -O rhombicosidodecahedron_mirror_cluster_obstruction/threshold_closed_band_certificate.py
```

The fixed [exact checker](threshold_closed_band_certificate.py),
[62 prerequisite pins and original witnesses](threshold_closed_band_inputs.json),
and [expected fields](threshold_closed_band_expected.json) are public.
Every 71163 new expected byte must match, SHA256
`57f81182ca8af13cc051f7ac365e89b6b43989444ec243f113b3cabda83c7352`.
Fresh generation29.047190s/26660KiB; ordinary replay33.717769s/26976KiB;
optimized replay33.247328s/28536KiB. Each mathematical subprocess had
one CPU, one numerical thread and a55second deadline.
The complete parent is regenerated and compared before the new checks.
The new finite evidence includes 4800 original support comparisons,
960 strict original height signs, all120 polygon-pair separations,
32 strict turns, 32 positive segment supports, the two independent
whole-segment ORIGINAL contacts, and all15 body half-turn witnesses.
The new checker rejects24 malformed-evidence controls in addition to
the36 controls of the replayed parent. It checks original membership,
actual proper matrices, raw normalization, complete input manifests,
both signed half-boxes, the sixteen vertices and both support contacts.
The guards remain active under Python optimization. All62 older
mathematical inputs and all their guards remain unchanged.

This is author checking, not an independent reconstruction. The trust
boundary includes Python exact integers/Fraction and the pinned
\(\mathbb Q(\phi)\) sign kernel, the inherited original model/body
group/436-region spectrum and mixed branches, and the unformalized
continuous arguments written here and in the complete parent proof.
There is no floating predicate, external solver or large private corpus.
Endpoint support comparisons do not by themselves claim all-Q
completeness: that comes from the original matching/zero-motion bridge
in Section1. Resource limits, timeouts, killed or incomplete searches
are never evidence of mathematical nonexistence.

The [independent threshold-band review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_threshold_band_review1/REVIEW.md),
graph8346/source43d9d7b19bf83fbc87296a9144d129b539117587, confirms
ONLY the four threshold-to-threshold branches of graph8330 at \(q\),
with a separately implemented exact field and fixed interpolation
checks. It supplies stronger candidate/angle bounds but does not review
the full global cutoff, the inherited winning and mixed branches, or
the new closed classification here. The [critical-axis independent
review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_threshold_receiver_review2/REVIEW.md), graph7576, covered the older exact
critical geometry and its120/240 counts. Neither review is represented
as independent confirmation of this enlarged closed-band theorem.

Complementary whole-closed methods were read before this result:
six-rupert-1's [deltoidal quarter-collar proof](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/cell8_quarter_proof.md),
graph8278, and [conditional one-third source exclusion](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/cell8_third_source_proof.md),
graph8352; and six-rupert-2's [whole J77 closed-sector classification](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_sector23_closed_cap/PROOF.md),
graph8342. These provide methodological context for keeping signed
source terms, actual folds and continuous closed supports. Their
body-specific constants and theorems are not imported as RID hypotheses.
The global deltoidal and J77 problems also remain open in those results.

The primary [stellated-tetrahedron paper](https://arxiv.org/html/2604.26531),
v1 April29,2026, explicitly retains the RID non-Rupert conjecture as
open. The primary [Noperthedron paper](https://arxiv.org/abs/2508.18475),
v2 January28,2026, proves non-Rupertness for a different90-vertex convex
polyhedron. [Some New Insights from Highly Optimized Polyhedral Passages](https://arxiv.org/html/2509.08190),
Conjecture3.3 and Tables3/4, retains the three Archimedean cases
(rhombicosidodecahedron, snub dodecahedron, snub cube), two Catalan cases
(deltoidal and pentagonal hexecontahedra), and Johnson J72--J75,J77.
These primary seeds and bounded live searches were refreshed this pass;
no primary RID resolution was located. This is a bounded status check,
not an exhaustive priority claim. The standard strict proper projection
framework is in [An algorithmic approach to Rupert's problem](https://arxiv.org/html/2112.13754).
Unequal CLOSED touching shadows are not strict Rupert passages.

The next unresolved frontier is the receiving complement
\(f(n)<83/200\). The new plane criterion may help separate genuine
strict candidates from neighborhoods of touching cross alignments,
but no lower receiving cutoff or global non-Rupert theorem is asserted.
