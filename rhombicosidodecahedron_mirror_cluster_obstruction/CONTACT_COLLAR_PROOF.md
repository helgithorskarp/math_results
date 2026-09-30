# Persistent original contacts give positive global axial slack for the RID

**six-rupert-3 — researcher — 2026-09-30.**

This is a complete written, unformalized intermediate proof with exact finite
certificates. The global Rupert property of the standard
rhombicosidodecahedron remains **OPEN**. The positive global slack below is
existential: **no numerical value of epsilon or all-source receiver-cap
radius is certified**. The explicit caps in Section 4 exclude sources near
specified closed branches; they are not themselves all-source caps.
Independent review of this new theorem and historical priority are not asserted.

## 1. Statement and closed-limit dependencies

Let phi=(1+sqrt(5))/2, and let V be the sixty distinct even coordinate
permutations and independent signs of
(1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2).
Put K=conv(V)=-K, R^2=7+8phi, and G equal to its order-sixty proper body
rotation group. This is the standard edge-length-two RID. For unit n put

\[
 f(n)=\min_{v\in V}|v\cdot n|,\qquad
 \beta=(19-8\phi)/29,\qquad q=57/125.
\]

**Theorem.** There exists a constant

\[
                         0<\epsilon<\beta-q^2                 \tag{1}
\]

such that every strict projection passage, with arbitrary proper spatial
rotation Q, planar translation t, full roll and scale lambda>=1, satisfies

\[
 \lambda P_nQK+t\subset\operatorname{int}(P_nK)
 \quad\Longrightarrow\quad f(n)^2<\beta-\epsilon.              \tag{2}
\]

Equivalently its squared receiving diameter is strictly greater than

\[
                       (736+960\phi)/29+4\epsilon.             \tag{3}
\]

The [threshold receiver theorem](THRESHOLD_RECEIVER_PROOF.md), source commit
c56d11f8c11bf1eb186b7d648eaf25a4d6586e29, supplies the complete classification
of closed containments for all receivers with f(n)^2>=beta. Its graph claim
bafkreianaonbifx6fbg6hdozuqiyv7553u6w7qitjixxzmrswi4hymjroq was confirmed
committed at height 7520, transaction 22, including its original body and
all eleven directed relations. We use the mathematical classification,
not broadcast acceptance, as a premise.

The [global axial theorem](GLOBAL_CAP_PROOF.md), source
9e9374854d153addb1d7697d05fd4b5d0180849f, gives 436 projective strict signed
regions: ten winning regions of maximum 1/3, all others of maximum <=beta,
exactly sixty nonwinning regions of maximum beta. It also proves
diam(P_nK)^2=4(R^2-f(n)^2). The sixty nonwinning beta axes form two proper
projective G-orbits of thirty, represented by

\[
 \ell=(0,1,-3-3\phi),\qquad h=(0,1,(3\phi-1)/11).               \tag{4}
\]

For all winning receivers at or above beta, closed containment has Q in
G union J_nG, where J_n=2nn^t-I is the proper half-turn about n. At unit
ell the same two left cosets are exhaustive. At unit h they are

\[
                G\ \cup\ J_nG\ \cup\ CG\ \cup\ J_nCG.          \tag{5}
\]

Here C is the proper 36-degree turn about u=(0,phi,-1):

\[
 C={\phi\over2}I+
   (1-{\phi\over2}){uu^t\over\phi+2}
   +{\phi-1\over2}[u]_\times.                                \tag{6}
\]

Its eight shared outer-circle points prevent strict passage, although
P_h(CK) is an unequal closed subset of P_hK. For a receiver g*unit(h),
replace C by gC in (5). All closed cases have unit scale and zero translation.
This classification alone does not imply (2): contacts at every closed
limit must first be shown to persist and obstruct nearby source rotations.

## 2. Complete original contacts on the two nonwinning references

Use the raw rays

\[
 r_L=(0,(2-\phi)/3,-1),\qquad r_H=h,\qquad n_*=r/\|r\|.        \tag{7}
\]

The first is a positive rescaling of ell. Both have norm <11/10. Each
actual full receiving shadow has sixty distinct projected original
vertices, sixteen hull corners and eight maximum-radius circle points.
Every corner has a unique original preimage.

For each of the sixteen receiving edges with original endpoints a,b,
form e=b-a and its oriented support normal m(r)=e cross r. Select every
original maximum-circle endpoint w on that edge. This complete selection
gives **sixteen distinct endpoint/edge contacts on ten distinct receiving
facets**, with eight distinct torques. It does not give sixteen distinct
facets. All selected edges have length two and an actual second original
endpoint. Every selected (w,e) has the partner (-w,-e).

For each contact the checker compares all sixty original vertices:

\[
                  (e\times r)\cdot(w-v)\ge0.                 \tag{8}
\]

There are exactly two original ties. Both satisfy
(w-v) cross e=0. Therefore their support gaps are identically zero for
every normal, not merely zero at the reference. Among all other original
vertices the minimum positive raw gap is

\[
             g_L=(4-2\phi)/3,\qquad
             g_H=(-28+18\phi)/11.                            \tag{9}
\]

There are 960 complete original comparisons per reference. All sixteen
records, including original receiving vertex, edge, source preimage,
entire tie set and positive gap, are in the compact output.

For the lower body branch use D=I. For the higher branch use D=C.
At the latter V intersects CV in twenty original vertices, and all eight
selected circle preimages belong to that intersection. The checker
verifies C^t w in V and C(C^t w)=w for every contact. The same receiving
contacts also apply to the higher body branch D=I. Thus w is an actual
source point of DK in each stated case; it is not an invented shadow
point or the image of an improper alignment.

## 3. Supports persist on whole closed normal caps

Fix delta=1/300 and let ||n-n_*||<=delta with n unit. Since R<9/2 and
||e||=2, every positive original support gap changes by less than

\[
                       2(2R)\delta<18\delta.                 \tag{10}
\]

The reference unit gap is at least g/||r||>g/(11/10). Both exact values
in (9) exceed 18*delta*(11/10). The zero gaps remain zero by their
cross-product identities. Consequently

\[
                  (e\times n)\cdot(w-v)\ge0                  \tag{11}
\]

for all original vertices throughout the **entire closed cap**, including
both sides of any reflection wall through the reference. Adjacent
normal cones need not be inferred from a weak contact at their common wall.
The torque-ball bounds below also ensure some nonzero supporting normal
in every rotation direction.

## 4. Complete torque hulls and full proper rotation rigidity

For each original contact define T(r)=w cross (e cross r). The eight
distinct torques have full affine rank three. The checker enumerates all
56 triples and all 448 point/plane side comparisons. Exactly twelve
distinct supporting facets occur, all with positive oriented height.
Every actual facet of a full-dimensional three-dimensional finite hull
contains an affinely independent triple, so this enumeration is complete.
All its facet normals, heights, squared origin-plane distances and a full
affine rank witness are published.

The minimum squared distances of the origin from these complete hull
facets are exactly

\[
 d_L^2={1328+304\phi\over14589}>(7/20)^2,\qquad
 d_H^2={9692+15056\phi\over164681}>(9/20)^2.                   \tag{12}
\]

Hence their centered raw torque balls have radii greater than
rho_L=7/20 and rho_H=9/20. Normalize every contact by the common constant
B=9/2 and put S(n)=T(n)/B. Under normal movement each S changes by less
than 2*delta because ||w||||e||/B<2. The convex hull support function
therefore retains a centered ball of radius greater than

\[
 {\rho\over(11/10)B}-2\delta
   =\begin{cases}
       317/4950>1/16,&L,\\
       139/1650>1/12,&H.
     \end{cases}                                             \tag{13}
\]

The strict margins over those full angle bounds are respectively
61/39600 and 1/1100. No floating estimate enters (9)--(13).

Let A be a proper rotation of principal angle theta>0 and unit rotation
axis z. The full axis-angle exponential remainder satisfies

\[
 Aw-w=\theta(z\times w)+E,\qquad
                         \|E\|\le\|w\|\theta^2/2.             \tag{14}
\]

By the torque ball choose a contact with z.S(n) at least its ball radius
b. Since ||e cross n||<=2 and R<B, its scalar support displacement obeys

\[
 {e\times n\over B}\cdot(Aw-w)
       \ge\theta b-{\|w\|\|e\times n\|\over2B}\theta^2
       >\theta(b-\theta)>0.                                 \tag{15}
\]

By (11) this violates even closed centered unit containment of ADK
in K's receiving shadow. It holds for every nonzero full principal angle
theta<=1/16 in the lower cap, and theta<=1/12 in the higher cap, for
both D=I and D=C in the higher case. These are **full spatial relative
rotation angles**, not roll angles or independently assumed source tilts.
At theta=0 an actual shared w projects onto a receiving support line,
so strict containment is still impossible.

Right factors g in G permute actual source vertices and do not change
DK. A fixed proper body image transports both receiver and source to
these references. Branches containing J_n are handled with the **actual
moving receiver half-turn**:

\[
                      P_nJ_nQK=-P_nQK=P_nQK,                 \tag{16}
\]

using K=-K. In a sequence n_j->n_*, if Q_j->J_(n_*)Dg,
then J_(n_j)Q_j->Dg. Formula (15) is applied to
A_j=J_(n_j)Q_j g^{-1}D^{-1}->I. A fixed J_(n_*) is not substituted for
J_(n_j). Every transformation remains proper. The determinant-minus-one
Gram alignment from the threshold calculation is never treated as a
permitted source rotation.

## 5. The winning closed limits are locally rigid too

The [winning receiver proof](WINNING_RECEIVER_PROOF.md), source
a666fd496161000af9dcb9dd408f3ed3d2a00fcc, supplies ten actual original
edge-endpoint supports on the entire closed outer triangle U=conv(B0,L*,C*),
with ||e||=2 and ||u||<27/25. Its complete 840-case facet certificate gives
the raw torque ball >=1/2 everywhere on U. Here

\[
 B_0=(0,\phi^{-2},1),\quad
 A_0=(0,0,1),\quad
 D_0=(1/[\phi(\phi+2)],1/(\phi+2),1),
\]

and L*,C* are the two q=57/125 cut intercepts of its proof.
The ten supports persist on the larger closed triangle A0 B0 D0.
For the physical unit normal n=u/||u|| the normalized torque ball is at least

\[
 {1/2\over(27/25)(9/2)}=25/243>1/16,                         \tag{17}
\]

with margin 157/3888. The same full proper rotation proof (14)--(15)
excludes every nonzero near-body angle <=1/16 for these receivers.
A zero angle gives an equal shadow and prevents strictness. Formula
(16) handles the other left coset.

We must justify using U for receivers approaching a winning closed limit
from below beta. The full six-positive-original-vertex tangent hexagon
in the winning proof has centered disk radius rho_6=sqrt(8/3+4phi)>3.
Within that same strict signed region write k=z*n0+w. Its exact inequality

\[
                         f(k)\le z/\sqrt3-\rho_6\|w\|        \tag{18}
\]

works whenever f(k)>=q, without requiring f(k)^2>=beta. The bounds
1/sqrt3<289/500 and (289/500-q)/3<1/20 give z>199/200.
The identical chord argument then gives

\[
 \|k-n_0\|\le(101/300)(1/\sqrt3-q)<1/24.                    \tag{19}
\]

The regenerated closed-chamber wall margins in the parent proof rule out
every threefold center except B0/||B0|| after folding. Its chart calculation
places u in closed A0 B0 D0. The actual original cut vertex
v*=(-1,phi^3,-1) has positive height and

\[
                         v_*\cdot u\ge f(n)\|u\|>q           \tag{20}
\]

when f(n)>q, because ||u||>=1. The parent's two linear cut intercepts
therefore put u in U. All normal reversals and chamber folds use the
finite group of actual body symmetries; a subsequence fixes the fold.

If n_j approaches a winning n_* with f(n_*)^2>=beta, then f(n_*)>q
and no original vertex has zero axial height. Eventually n_j stays
in that same winning signed region and f(n_j)>q. Thus (18)--(20)
apply to the whole tail. The checker regenerates every entry of the
positive active hexagon, the chart and chamber bounds, both cut intercepts
and 1800 original cut-corner support comparisons. It explicitly imports
the published complete 840-case whole-triangle torque theorem; it does
not claim to replay that parent computation in this new run.

## 6. Compactness gives a uniform positive global slack

First remove unrestricted translation and scale from a proposed strict
passage. With S=P_nQK=-S and T=P_nK=-T, lambda*S+t inside int(T)
implies lambda*S-t inside int(T) by symmetry. Midpoints in the convex
open interior give lambda*S inside int(T). Since 0 is interior to T,
convexity and lambda>=1 give S inside int(T). Therefore every original
strict passage supplies a centered unit strict passage with the same
(n,Q). No boundedness of the original t or lambda is needed.

Suppose no positive global slack exists. Then there are centered unit
strict passages (n_j,Q_j) with f(n_j)^2>=beta-1/j. Compactness of
S^2 times SO(3) gives a subsequence tending to (n_*,Q_*).
Projections of the finitely many original vertices, and hence their
convex hulls, vary continuously in Hausdorff distance. Taking the limit
gives

\[
               P_(n_*)Q_*K\subseteq P_(n_*)K,\qquad
                              f(n_*)^2\ge\beta.               \tag{21}
\]

The complete threshold classification in Section 1 has only two cases.

If n_* is a nonwinning beta axis, a fixed proper body image and, if
necessary, normal reversal bring it to (7). Eventually every n_j lies
in the closed 1/300 cap. The complete coset classification brings Q_j
to A_jD, with A_j->I and D=I in the lower case, or D=I,C in the higher
case; use the moving J_(n_j) when required. Eventually the full angle
is at most the corresponding positive bound in (13). A nonzero angle
contradicts even closed containment by (15), and angle zero contradicts
strict containment by its actual shared boundary contact.

If n_* lies in a winning region, Section 5 puts the receiving tail
in U after a fixed finite fold. Its classified closed source limit
is in G union J_(n_*)G. Right source gauges and the moving half-turn
give A_j->I. Nonzero full angle <=1/16 contradicts (17) and (15);
zero angle gives equal shadows and again contradicts strictness.

Both cases contradict the chosen strict passages. Some uniform
epsilon>0 must therefore exist. Decrease it if necessary to satisfy
(1). Formula (3) follows from the exact diameter identity.

In particular each of the sixty nonwinning beta axes has an open
all-source excluded receiving neighborhood. Its radius has not been
computed. The numerical chord 1/300 only verifies supports and the
source-near-branch angle obstructions used in the compactness proof.
Receivers farther below beta, and the global Rupert conjecture, remain
unresolved. This proof is not a finite numerical cover of their complement.

## 7. Reproduction and trust boundary

Use Python 3.11+ standard library, with numerical threads one:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/contact_collar_certificate.py --self-test
~~~

Every output byte must match contact_collar_expected.json. The exact
output SHA256 and completed normal/optimized replay timings are recorded
in the README. The checker regenerates both full original contact lists,
all original gaps and persistent ties, the complete torque hulls, the
proper C matrix and every new rational inequality. Ten malformed controls
must reject, also under python3 -O -B. They cover a missing original
vertex, reversed support, non-original edge, incomplete contact/torque
lists, unsupported torque radius, excessive cap or angle, unsupported
ray norm and nonpositive cap.

The threshold compact output is pinned to SHA256
5516794048036b35ce73b63b0fdf5eb1c01620b260b11f87dfc401e0e5ccfeac.
The winning compact output is pinned to SHA256
f2796de9c7123917dbd845c651179216ca595545c30e6a7cdb48ea7bf6312ba3.
All source dependencies remain byte-identical to the previously verified
published threshold source. The full old threshold, winning, global and
directional self-tests are **not** claimed rerun here.

The new run uses only exact Q(phi) arithmetic and Fraction inequalities;
no floating diagnostic, interval sample, solver result or private input
is a premise. The complete old regional spectrum, closed classification
and whole-winning-triangle torque theorem remain mathematical dependencies.
Their written geometric bridges, the exact arithmetic kernel, the
original body model, and Sections 3--6 remain the trust boundary.
Matching output is regression evidence, not an independent proof algorithm,
formalization or independent review of this new theorem.

## 8. Precise collaboration and current literature

The normalized-support method is informed by six-rupert-1, researcher,
whose [deltoidal normalized-cap proof](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/normalized_cap_proof.md)
is source 0b8097a272e4b134b88869e6bf1a395b898da6c3, graph
bafkreidbimtnphxte3m2xe2d7hev7c3lopnsvrxdzmbibfma232eyz2i74,
actually committed at 7520. All RID constants and original contacts above
are independently derived here; deltoidal constants are not transferred.
Six-rupert-2, researcher, supplies complementary proper-frame context in
[J77 adaptive roll domains](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_adaptive_roll_domains/PROOF.md),
source 94e3ef96d8cdaff6fd6e0c6f0f7397b14c2f0a6b, graph
bafkreigxs2bozl4ddvvryzxhvtbng3lf5daw3eh7uxzngo3t7b3q2hs4am at 7514.
Neither body's exclusion theorem is a RID premise.

Two independently selected reviews, actually committed at 7520, confirm
specific older inputs. Six-reviewer-1's
[axial-cap audit](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_axial_cap_review1/PROOF.md),
source 559baae441b925c7272e1c359492a4ecfcae8d0f, graph
bafkreibxnfiewtz3s7zzrusehteanyx6pp4fes75sikeez2eqoblk6p7f4,
checks the global spectrum and earlier cap using a different closest-hull
algorithm. Six-reviewer-2's
[winning receiver audit](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_winning_receiver_review2/REVIEW.md),
source 3ea4c34f1a8263845316d2944249513c99601ccf, graph
bafkreifzwcsd4ddv5evsmpb5f6q3iu57k3w2rs4eif35thfyflhaxx3rve,
checks the winning theorem, including all 840 facet strata, with an
independent integer-basis arithmetic implementation. We use the weaker
published raw radius 1/2, rather than its refinement 51/100.
These reviews do **not** certify the new threshold or contact-collar
theorems. No reviewer target or verdict was requested or influenced.

The final refresh also found six-reviewer-2's later
[threshold receiver review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_threshold_receiver_review2/REVIEW.md),
source 52d7829380a548c66fe716ca8155c2c22e6cd23f, graph
bafkreifggmzorznb46eyzayy6kovnoen76lcyt4e5iwzktimhewtw6zzgu at 7576.
It independently confirms the two-orbit threshold classification and
120/240 closed orientation counts, using a quadratic Bernstein continuum
roll certificate. Its stronger winning-source gap 3313/96000 and exact
threshold tangent-disk squared radius (39+37phi)/29 are useful for a
future numerical slack certificate. Neither refinement is needed for
Sections 2--6 here. That later review covers the threshold parent,
not this new positive-slack theorem.

Primary literature was live checked on 2026-09-30:
[2604.26531](https://arxiv.org/html/2604.26531) retains RID as a
non-Rupert conjecture; [2508.18475](https://arxiv.org/abs/2508.18475)
constructs a different non-Rupert body. The unresolved named-solid context
is also checked against [2509.08190](https://arxiv.org/html/2509.08190).
We use the standard strict projection equivalence from
[2112.13754](https://arxiv.org/html/2112.13754).
No published result is restated as a new global non-Rupert theorem, and
no absence of a floating passage is used as mathematical evidence.
