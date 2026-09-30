# Spectral moment Grams bound the complete five-level displacement class

Actual author **six-sendov-2**, role **researcher**, 2026-09-30.
Status: complete ordinary author proof and exact rational continuous
certificates; unformalized, independent review of this extension pending.

## 1. Statements and credited quantities

For a balanced real eight-vector with \(\max|\theta_j|=1\), put
\[
 \mu_k=\sum_j\theta_j^k,\quad e=\mathbf1/\sqrt8,\quad P=I-ee^*,
 \quad C=P\operatorname{diag}(\theta)P|_{e^\perp},
 \quad w=\operatorname{diag}(\theta)e,
\]
\[
 \Psi=\sum_{\lambda\ {\rm distinct}}\|\Pi_\lambda w\|^4,
 \qquad J=122\mu_2+\frac{224\mu_4-5760\Psi}{\mu_2}.          \tag{1}
\]
Here \(\Pi_\lambda\) is the full orthogonal eigenspace projection,
including at collisions; \(\mu_2>0\). The functional and its polynomial
interpretation are credited to the
[angular quartic](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and its
[independent audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/REVIEW.md).
Let \(M_m\) consist of these vectors admitting positive constant block
sizes \(m=(m_1,\ldots,m_5)\), allowing equal-valued labels and permutations.
Let \(\mathcal F_5\) be the full normalized class with at most five
actual coordinate values.

**Theorem 1.** Throughout the entire remaining labeled class,
\[
 \boxed{J\le786\quad\hbox{on }M_{3,2,1,1,1}.}              \tag{2}
\]
Consequently \(J\le786\) on all of \(\mathcal F_5\). The latter step
uses the credited
[five-level reduction](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_five_level_moment_reduction/PROOF.md),
which proves \(J\le750\) on \(M_{2,2,2,1,1}\) and \(J\le650\) on
\(M_{4,1,1,1,1}\). These three patterns are exactly the positive
five-part partitions of 8. A profile with fewer than five actual values
can be represented with five positive labels by splitting occupied
blocks without changing their levels. Thus the union covers the whole
class, including all collisions.

The credited
[four-level classification](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_four_level_displacement/PROOF.md)
has sharp value \(J_*=j(u_*)\), where
\[
 j(u)=\frac{2058+21912u-15876u^2+19224u^3+3402u^4}
                   {(3+u)(1+3u)^2},
\]
\[
 26634-231084u-907290u^2+376920u^3
                 +971190u^4+224532u^5+30618u^6=0,
 \qquad 2/25<u_*<9/100.                                  \tag{3}
\]
Its equality vector is
\((1,1,1,-1,-1,-1,\sqrt{u_*},-\sqrt{u_*})\), and
\(J_*=785.7538723\ldots\). It belongs to \(\mathcal F_5\) and to
\(M_{3,2,1,1,1}\) after splitting one triple label. Therefore
\[
 J_*\le\sup_{\mathcal F_5}J\le786.                         \tag{4}
\]
The exact five-level maximum, equality set and every six-to-eight-level
global reduction remain unproved here. The scalar value in (3) is an
input, not a new optimum claimed by this certificate.

## 2. Uniform active-space projection and the exact four-moment formula

Fix five positive block sizes \(m_i\) and balanced labels \(t_i\).
The block-constant space is invariant under \(P\operatorname{diag}(\theta)P\).
Its balanced part \(A\) has dimension 4, contains \(w\), and its orthogonal
complement in \(e^\perp\) consists of within-block difference spaces.
The latter have eigenvalue \(t_i\) with multiplicity \(m_i-1\) and zero
\(w\)-weight. Let \(C_A=C|_A\), and define
\[
 s_0=4,\qquad
 s_r=\operatorname{tr}C_A^r
 =\operatorname{tr}C^r-\sum_i(m_i-1)t_i^r\quad(r\ge1),
 \qquad b_i=w^*C_A^i w.                                  \tag{5}
\]
These formulas retain all four labeled modes even at collisions.
Direct multiplication gives
\[
 b_0=\mu_2/8,\quad b_1=\mu_3/8,\quad
 b_2=\mu_4/8-\mu_2^2/64,\quad
 b_3=\mu_5/8-\mu_2\mu_3/32.                              \tag{6}
\]
For \(k=3,4\), set
\[
 G_k=(s_{i+j})_{0\le i,j<k},\qquad
 b^{(k)}=(b_0,\ldots,b_{k-1})^T,\qquad
 D_k=\det G_k,\quad N_k=(b^{(k)})^T\operatorname{adj}(G_k)b^{(k)}.
                                                               \tag{7}
\]
Whenever \(D_k>0\),
\[
 \boxed{\Psi\ge N_k/D_k.}                                 \tag{8}
\]
Indeed let \(T=\sum_\lambda\Pi_\lambda ww^*\Pi_\lambda\) on \(A\).
Each block is rank one or zero, so \(\|T\|_F^2=\Psi\).
The matrices \(I_A,C_A,\ldots,C_A^{k-1}\) have Frobenius Gram \(G_k\),
and their inner products with \(T\) are \(b_i\), since they commute
with the spectral projections. Squared norm of the projection of
\(T\) onto their span is \(N_k/D_k\), proving (8).

If \(C_A\) has four distinct eigenvalues, these four powers span the
whole commutant on \(A\). Thus (8) is **equality for k=4**. This yields
an exact active moment formula for \(\Psi\), without computing roots.
The three-moment inequality remains useful close to triple-label
collisions, where the four-moment determinant degenerates.

For completeness, the active characteristic polynomial is
\[
 H(\lambda)=\prod_i(\lambda-t_i)^{m_i},\quad
 R(\lambda)=\prod_i(\lambda-t_i)^{m_i-1},\quad
 Q(\lambda)=\sum_i m_i\prod_{j\ne i}(\lambda-t_j),
 \qquad H'=RQ,
\]
\[
 \det(\lambda I_A-C_A)=Q(\lambda)/8.                       \tag{9}
\]
On distinct labels, the usual rank-one compression identity gives the
secular equation \(\sum_i m_i/(\lambda-t_i)=0\). Its derivative is
strictly negative between successive levels and its limits have
opposite infinite signs. There is exactly one root in each of the four
intervals. This proves strict interlacing and distinct active eigenvalues.
Polynomial continuity then gives (9) at coincident labels.
The Vandermonde matrix of these eigenvalues gives
\[
 D_4=\prod_{i<j}(\lambda_i-\lambda_j)^2
                      =\operatorname{Disc}(Q)/8^6.         \tag{10}
\]
This discriminant interpretation is a written identity; the checker
uses the moment determinant and Newton recurrence, and does not claim
a second independently computed discriminant formula.

Expanding the rank-one factors \(P=I-ee^*\) in
\(\operatorname{tr}(\operatorname{diag}(\theta)P)^r\) gives the trace
polynomials through degree 6. A word with \(h\) rank-one choices and
cyclic gaps \(g_1,\ldots,g_h\) contributes
\((-1)^h8^{-h}\prod\mu_{g_i}\); the word with no choices gives \(\mu_r\).
The checker performs this expansion, subtracts the difference-space
traces in (5), and checks Newton identities from (9) in all three raw
saturation cases. It verifies the full 8x8 polynomial trace and (6)
through \(r=6\) and \(i=3\) in one raw case, as a separate route.

Substituting (8) into (1), it suffices for either k to prove
\[
 F_k=(786\mu_2-122\mu_2^2-224\mu_4)D_k+5760N_k\ge0.       \tag{11}
\]
The exact source derives \(F_4,F_3\) and their adjugates symbolically.
It also checks every entry of \(G_4\operatorname{adj}G_4=D_4I\) in
one raw case and of the corresponding three-moment identity in all
three cases. Generic distinct levels give \(D_4,D_3>0\).

A third certificate uses only the four-dimensional active space:
at most four distinct modes carry positive weight, whose sum is
\(\|w\|^2=\mu_2/8\). Hence
\[
 \Psi\ge\mu_2^2/256,\qquad
 J\le\tfrac{199}{2}\mu_2+224\mu_4/\mu_2
                         \le\tfrac{199}{2}\mu_2+224.       \tag{12}
\]
Thus \(1124-199\mu_2\ge0\) is sufficient for (2), uniformly also at
collisions. No assertion about equality in this relaxation is needed.

## 3. Complete saturation sections and six closed cubes

Reflection and permutations preserve (1). Some label is saturated;
reflect it to \(-1\). There are exactly three inequivalent saturation
masses,3,2,1. The raw affine balanced labels used by the checker are

| Case | Masses | Levels |
|---|---|---|
| triple | 3,2,1,1,1 | -1,x,y,z,3-2x-y-z |
| double | 2,3,1,1,1 | -1,x,y,z,2-3x-y-z |
| singleton | 1,3,2,1,1 | -1,x,y,z,1-3x-2y-z |

Only equal-mass labels are ordered. For the first two cases denote the
other heavy label by \(a\) and order the three singleton deficits
\(0\le\beta_1\le\beta_2\le\beta_3\le2\).
For triple saturation balance gives \(\sum\beta_i=2a\), \(0\le a\le1\).
For double saturation it gives \(\sum\beta_i=1+3a=s\in[0,4]\).
Let
\[
 C_s=(s/3,s/3,s/3),\quad A_s=(0,0,s),\quad B_s=(0,s/2,s/2),
\]
\[
 D_s=((s-2)/2,(s-2)/2,2),\quad E_s=(0,s-2,2).             \tag{13}
\]
For \(0\le s\le2\), the ordered section is the triangle \(C_sA_sB_s\).
For \(2\le s\le4\), it is the quadrilateral \(C_sD_sE_sB_s\), covered
by triangles \(C_sD_sE_s\) and \(C_sE_sB_s\). One can enumerate the
vertices by imposing two boundary equalities among
\(\beta_1=0,\beta_1=\beta_2,\beta_2=\beta_3,\beta_3=2\) in the sum
plane. The lists in (13) are exactly the feasible vertices. At s=0,2,4
the same closed triangles, possibly degenerate, still cover the section.
For any listed triangle with center \(C_s\) and other vertices \(U,V\),
use
\[
 \beta=C_s+Y[(1-Z)U+ZV-C_s],\qquad 0\le Y,Z\le1.         \tag{14}
\]
These are all convex combinations in that triangle, so coverage is
complete, including its edges and zero radial width.

For singleton saturation put the other labels \((a,b,c,d)\) at masses
\((3,2,1,1)\), with \(c\ge d\). Setting \(q=3a+2b\), balance gives
\[
 -1\le q\le3,\quad (q-2)/3\le a\le\min(1,(q+2)/3),
 \quad b=(q-3a)/2,
\]
\[
 c=(1-q)/2+v,\quad d=(1-q)/2-v,\qquad
 0\le v\le1-|1-q|/2.                                    \tag{15}
\]
The a-interval follows from \(-1\le a,b\le1\); the c,d-interval
follows from \(c+d=1-q\) and \(-1\le d\le c\le1\).
The upper bound for a and the bound for v change at q=1. The latter
bound is \((q+1)/2\) for \(q\le1\) and \((3-q)/2\) for \(q\ge1\).

The following are the six charts. In each row \(X,Y,Z\in[0,1]\).

| Chart | Parameters and section | Labels |
|---|---|---|
| triple | a=X, s=2X, triangle C,A,B in(14) | -1,a,1-beta1,1-beta2,1-beta3 |
| double0 | s=2X, a=(s-1)/3, triangle C,A,B | -1,a,1-beta1,1-beta2,1-beta3 |
| double1 | s=2+2X, a=(s-1)/3, triangle C,D,E | -1,a,1-beta1,1-beta2,1-beta3 |
| double2 | s=2+2X, a=(s-1)/3, triangle C,E,B | -1,a,1-beta1,1-beta2,1-beta3 |
| singleton0 | q=-1+2X, a=(q-2+4Y)/3, b=1-2Y | -1,a,b,1-X+XZ,1-X-XZ |
| singleton1 | q=3-2X, a=(1-2X+(2+2X)Y)/3, b=1-(1+X)Y | -1,a,b,-1+X(1+Z),-1+X(1-Z) |

The singleton rows set \(v=XZ\) in (15); they cover q in [-1,1] and
[1,3] respectively. Conversely every point of the section has these
coordinates, with a zero-width coordinate set arbitrarily to zero.
The source implements these inverses and rational triangle barycentric
inverses. It checks 60 closed round trips, including every cube corner
and the degenerate sections. The universal section argument, rather
than these finite controls, establishes exhaustive coverage.

## 4. Closed continuous certificates and collision extension

Pull back (11) by the charts. The following factors divide both \(F_4\)
and \(D_4\) exactly:

| Chart | Removed nonnegative factor | Four-moment leaves | Three-moment leaves | Moment leaves |
|---|---|---:|---:|---:|
| triple | X^2Y^2 | 2 | 6 | 5 |
| double0 | X^2Y^2 | 0 | 0 | 1 |
| double1 | Y^2 | 3 | 3 | 4 |
| double2 | Y^2 | 1 | 0 | 1 |
| singleton0 | 1 | 2 | 4 | 6 |
| singleton1 | X^2 | 2 | 4 | 5 |
| Total | | 10 | 17 | 22 |

The source checks exact divisibility and multiplication back for both
polynomials. Nonnegative reduced \(F_4\) implies nonnegative original
\(F_4\); no rational quotient is evaluated on a zero factor. The
three-moment leaves use the full unreduced \(F_3\); moment leaves
use \(1124-199\mu_2\). The cover has 49 leaves, maximum depth 8.

Every leaf is a **closed** dyadic box. In tensor Bernstein form the
basis is nonnegative and sums to1 on its whole box. Every coefficient
is checked nonnegative using exact fractions. The totals are 59,671
bound entries and 320 physical/order entries. The latter verify
\(-1\le t_i\le1\) and required equal-mass ordering for each whole chart;
balance is checked as a polynomial identity.
Inverse reconstruction verifies the initial power-to-Bernstein basis
conversion. Exact de Casteljau midpoint subdivision computes each child
coefficient array; 147 one-dimensional basis identities verify this rule
on every axis and all degrees used. For each method used in each chart,
one whole leaf array is also compared against an independent direct
affine substitution, giving 15 such comparisons.

cover.json supplies only the six names and complete binary bisection
trees with terminal method names. The checker independently requires
exactly the six charts, both closed children at every split, valid axes,
and complete volume conservation recursively. There is no omitted gap
or grid-sampling inference. expected.json is a regression record, not
a sign oracle: every sign, matrix control and recorded hash is rebuilt.

For points with five distinct labels, strict interlacing gives
\(D_4,D_3>0\). Each leaf therefore implies \(J\le786\) on its generic
profiles by (11) or (12). It remains to justify every singular profile.

Here a general spectral observation suffices. Suppose Hermitian
\(C_n\to C\) and \(w_n\to w\) in a fixed finite-dimensional space.
Group the eigenvalues of \(C_n\) according to the distinct limiting
eigenvalues of C. Their total orthogonal projections converge. If the
nonnegative weights in one split cluster are \(\alpha_{j,n}\), then
\[
 \sum_j\alpha_{j,n}^2\le\left(\sum_j\alpha_{j,n}\right)^2,
 \qquad \sum_j\alpha_{j,n}\longrightarrow\|\Pi_\lambda w\|^2.
\]
Thus \(\limsup\Psi(C_n,w_n)\le\Psi(C,w)\). In (1) the moments are
continuous and \(\mu_2>0\), so J is lower semicontinuous:
\[
 J(\theta)\le\liminf_n J(\theta_n).                       \tag{17}
\]
This inequality is sufficient to pass an upper bound to collisions.
No generic formula is divided by a singular determinant. In every
chart each pairwise level difference is a nonzero polynomial, as
checked exactly; its zero set has empty interior. Every cube point
is therefore approached by five-distinct-label profiles in the same
cube. The generic upper bounds and (17) prove (2) on all cube faces,
radial collapses and collisions. Together with Section 1's credited
two-cohort bounds, this proves Theorem1 on all of \(\mathcal F_5\).

## 5. A whole complex five-phase displacement basin bracket

Let \(p(z)=b(z-a)\prod_{j=1}^8(z-z_j)\), \(b\ne0\), have a simple
marked real root \(0<a<1\) and \(|z_j|\le1\). Other original roots
and critical points may repeat; critical multiplicities count. Put
\[
 G_a=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}-16/(1+a),\quad
 \rho_p=\max|z_j+1|,\quad\kappa=(1+a)(a-5/8),\quad d_0=13/8.
\]
For \(\rho_p\le1/2\), write uniquely
\(z_j=-(1-\tau_j)e^{i\phi_j}\), with \(\tau_j\ge0\) and small
principal real phases. Require at most five distinct phase values.
Depths \(\tau_j\) vary independently even within phase blocks;
there is no real-coefficient assumption. Let \(R_5(a)\) be the
supremum of radii \(r\in[0,1/2]\) for which every polynomial in this
class with \(\rho_p\le r\) satisfies \(G_a\ge0\).

**Corollary 2.** This whole class obeys
\[
 \boxed{\frac{53248}{1965}
 \le\liminf_{a\downarrow5/8}\frac{R_5(a)^2}{\kappa}
 \le\limsup_{a\downarrow5/8}\frac{R_5(a)^2}{\kappa}
 \le\frac{106496}{5J_*}.}                                \tag{18}
\]
The lower endpoint is 27.0982188..., and the credited upper endpoint
lies in (27.106707,27.106708). This does not establish existence or
value of a five-phase basin limit.

The analytic inputs are the credited
[joint all-disk expansion and negative-gap bootstrap](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sharp_energy_basin/PROOF.md)
and the
[original-root variational reduction](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_displacement_variational_basin/PROOF.md).
With \(T=\sum\tau_j\), \(M=\sum\phi_j\),
\(s=\|\phi-(M/8)\mathbf1\|\), \(\eta=(\phi-(M/8)\mathbf1)/s\),
and \(q_\infty=\max\eta_j^2\), they give uniformly on a negative-gap
sequence with \(a\downarrow5/8\) and \(\rho_p\to0\):
\[
 s>0,\quad T=O(s^4),\quad M^2=O(s^4),\quad\kappa=O(s^2),
\]
\[
 G_a=\kappa E_a+\frac{128}{169}T+\frac{40}{2197}M^2
                            -K(\eta)E_a^2+o(E_a^2),
 \quad E_a=\sum|(a-z_j)^{-1}-(1+a)^{-1}|^2,
 \quad\rho_p^2/E_a=d_0^4q_\infty+o(1).                    \tag{19}
\]
Directions and critical collision types may vary. Centering and
normalization preserve the number of distinct phase values. The
credited homogeneity conversion, with \(p_8=10985/33554432\), gives
\[
 \frac{K(\eta)}{q_\infty}
   =p_8J(\eta/\sqrt{q_\infty})\le786p_8,
 \qquad d_0^4/p_8=106496/5.                              \tag{20}
\]
Drop the nonnegative penalties in (19). Negativity implies
\(0<\kappa/E_a\le K(\eta)+o(1)\), with bounded right side.
Since \(q_\infty\ge1/8\), (19) can be inverted uniformly to yield
\[
 \kappa d_0^4/\rho_p^2\le K(\eta)/q_\infty+o(1)
                                      \le786p_8+o(1).     \tag{21}
\]
For any fixed \(0<\beta<106496/(5\cdot786)=53248/1965\), a failure
with \(\rho_p^2\le\beta\kappa\) along \(a\downarrow5/8\) would
contradict (21). Displacement zero has \(G_a=0\), so it cannot be a
failure. Hence all these strictly smaller squared radii are sufficient
for sufficiently small positive \(a-5/8\), proving the liminf bound.

The four-phase class is contained in this five-phase class, so
\(R_5(a)\le R_4(a)\). The credited sharp four-phase basin
\(R_4(a)^2/\kappa\to106496/(5J_*)\) proves the limsup bound. It
also supplies actual boundary-root failure families within four phases.
Neither their scalar optimum nor the four-phase basin is claimed anew.

No effective cutoff, finite-radius crossing, endpoint sign or equality
classification for five phases is asserted. The collapsed comparison
at the cutoff is \(128/13>8\); negative gaps relative to it are not
first-power counterexamples. The unrestricted displacement optimum and
degree-nine first-power Tang--Zhang endpoint remain unresolved here.

## 6. Reproduction and trust boundary

Run both commands in [README.md](README.md). Python 3.11.2 and the
standard library reproduce 74,275 checks, the 49 closed leaves and the
complete record SHA256

    fd2b8eb1a0208fab9fb2d3120eccc31a4bca960bb43bd7bd67c0eb8757f245f4

Explicit guards survive Python optimization. Missing cover/manifest,
omitted cube, missing child and altered coefficient or compression
records were rejected. The full defining pinching is separately computed
by rational projection onto the symmetric commutant for 19 distinct
normalized profiles, including collisions; nine raw quotient controls
also compare the moment route against that definition. These are author
controls, not independent review. All continuous signs are rebuilt without
floating-point arithmetic. There is no runtime import from earlier
sources or the campaign. The spectral projection proof, section and
collision arguments, cited cohort inequalities and joint analytic
asymptotics remain ordinary mathematical trust boundaries outside a
formal proof kernel. Exact provenance is in [LITERATURE.md](LITERATURE.md).
