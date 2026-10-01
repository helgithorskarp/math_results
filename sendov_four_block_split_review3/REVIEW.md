# Independent four-root split audit and compact uniform descent

Actual reviewer **six-reviewer-3**, role **independent mathematical reviewer**,
2026-10-01. All campaign signatures share an identity; the independent
methodology and explicit agent names establish the attribution here.

**Verdict: confirmed, within the precise ordinary-proof scope below.**
Committed lemma **8405**, actual author **six-sendov-3**, proves that the
degree-nine negative-side two-pair stationary branch has three negative
balanced angular modes and a positive transfer direction. Its exact split
derivative, analytic continuation, relative sign throughout every fixed
bounded radius window, angular Taylor form at the critical collision, and
lower limiting-radius corollary withstand this independent audit. The
prior family minimum and stationarity are explicitly credited inputs
8315/8364, independently reviewed in8378. This review neither turns a
within-family minimum into an unrestricted minimum nor determines the
other four angular eigenvalues.

Target reference:
**bafkreideq2iyeuzase6x7jitqmfay5jo4oinsw5dvk7fjggg6wwni3jpoa**.
Target source commit:
**38e10b3164b770e210dc4f549aa3e6b34e56fbc0**.
The [complete target proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_four_block_split_instability/PROOF.md)
and all six original source files were inspected. The complete committed
body embeds that proof, with its literature link expanded to a reader URL.
The new computation imports no author program or fixture during its
derivation.

## Exact claim and parameter scope

Fix a simple marked real root \(0\le a\le1\), and put
\[
p(z)=(z-a)\prod_{j=1}^8(z-z_j),\qquad
v=(1+a)^{-1},\quad b=1-a^2,
\]
\[
E=\sum_{j=1}^8|(a-z_j)^{-1}-v|^2,\qquad
F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}.
\]
Multiplicities count. The irrelevant nonzero leading coefficient can be
restored. All roots considered in this local claim lie on the unit circle
and differ from \(a\); all critical reciprocals remain finite and nonzero.
Use the credited7328 actual pair
\[
A_{a,s}(z)=z^2+2(1-x(a,s))z+1,\qquad
x(a,s)=\frac{(1+a)^4s}{4+2a(1+a)^2s}.
\]
It contributes exactly \(s\) to \(E\). Define
\[
R_{a;e,f}=(z-a)(z+1)^4 A_{a,e-f}A_{a,f},\qquad
T_{a;e,f,g}=(z-a)(z+1)^2 A_{a,e-f-g}A_{a,f}A_{a,g}.
\]
Thus \(E=e\) exactly and \(T_{g=0}=R\). The physical ranges are
\(0<f<e\) and \(0\le g\le e-f\), with energies sufficiently small.

For reference, the credited8315 coefficients are
\[
H(a,e)=\partial_fF(R_{a;e,f})|_{f=0+}
       =h_1(a)e+h_2(a)e^2+O(e^3),
\]
\[
h_1=\frac{208-184v-239v^2}{2304v^5},\qquad
h_2=\frac{-245888+771984v-786792v^2+246931v^3}{4718592v^8}.
\]
Write
\[
a_-=\frac{6\sqrt{101}-29}{52},\quad
v_-=\frac{24\sqrt{101}-92}{239},\quad
\lambda_-=\frac{\sqrt{101}}{48v_-^3}>0,\quad
\gamma(a)=\frac{(4+v)^2}{10368v^5}.
\]
There is an analytic curve \(H(a_Q(e),e)=0\). On
\(a=a_Q(e)+ce\), the credited8364 branch has
\[
f_*=e^2\rho_*(e,c),\qquad
\rho_*=-\frac{\lambda_-}{2\gamma_-}c+O_C(e|c|),\qquad
\rho_*(e,0)=0.
\]
It is stationary under all seven fixed-\(E\) circle angular directions
and has positive two-pair transfer second derivative. The original
window was \(|c|\le1/5\). Review8378 proves the extension to every fixed
finite \(C>0\), \(|c|\le C\), after reducing an energy threshold depending
on \(C\). Those hypotheses and dependencies are retained here.

The newly audited transverse derivative is
\[
H_4(a,e,\rho)=
\partial_gF(T_{a;e,e^2\rho,g})|_{g=0+}.
\]
Its physical interpretation initially requires positive \(e,\rho\).
Its continuation through \(e=0,\rho=0\) is jointly analytic, and
\[
H_4=H+e^2\rho\,\mathcal J,\qquad
\mathcal J(a,0,\rho)=\mu(a)
=-h_1(a)-\frac74\gamma(a)
=\frac{-3856+3256v+4295v^2}{41472v^5}.
\tag{1}
\]
Consequently, for every fixed finite \(C>0\), one common small-energy
threshold works for **all** \(-C\le c<0\), including arbitrarily small
\(|c|\):
\[
H_4(a_Q(e)+ce,e,\rho_*)=
e^2c\left(\frac{15}{8}\lambda_-+O_C(e)\right)<0.
\tag{2}
\]
At each such fixed branch point, the three-dimensional balanced
four-original-root split space has the scalar quadratic-form eigenvalue
\[
\ell_4=2v^4H_4<0
\tag{3}
\]
in Euclidean original-phase coordinates, with convention
\(\frac12\ell_4\|h\|^2\). There is a positive transfer direction, so
the angular index is at least three and the branch is a stationary
saddle. Circle motions descend while remaining in the closed disk;
the branch is therefore neither a local nor a global minimum in either
fixed-energy space. No inward-direction Hessian conclusion is needed
for that exclusion.

## Independent exact derivation

The checker uses a standard-library sparse Laurent ring over the rationals.
Its arithmetic layer is adapted from this reviewer's earlier public
checker; all calculations for this target are independently implemented.
It removes the far root of the complete quintic **before** splitting the
remaining quartic. The author instead uses a quadratic-times-cubic
factorization and differentiates its normalized system. The distinct
factorization order supplies an independent check of the delicate
coefficient computation.

Set \(\xi=q-v\), \(k=(1+b\xi)/2\). Direct substitution
\(z=a-1/q\) into each actual pair gives its monic reciprocal factor
\(\xi^2+sk\), sum \(2v-bs/2\), product \(v^2+as/2\), and exact energy
\[
2(v^2+as/2)-2v(2v-bs/2)+2v^2=s,
\]
using \(bv+a=1\). All three physical substitutions are checked with
independent \(e,f,g\), before introducing a series. The full degree-eight
original reciprocal polynomial is
\[
\mathcal R_8=\xi^2
(\xi^2+(e-f-g)k)(\xi^2+fk)(\xi^2+gk).
\]
Direct differentiation gives the full critical characteristic
\(9\mathcal R_8-(v+\xi)\mathcal R_8'\), including all eight
multiplicities. These untruncated polynomials have total energy degree
at most three; the later energy-series cap cannot discard any of their
terms.

Write the characteristic as \(\xi C_7\). At \(g=0\),
\[
C_7=\xi^2 C_5,\qquad
C_5=\xi^2 C_3+f(e-f)J,\qquad C_5(0)=-vf(e-f)\ne0,
\]
\[
C_3=\xi^3+(-8v+be)\xi^2+\frac{7a-4}{2}e\xi-3ve,
\]
with the independently reconstructed \(J\). Factor the new critical pair
as \(\xi^2-\sigma(g)\xi+\pi(g)\). The two lowest derivative equations give
exactly
\[
\pi'(0)=\frac14,\qquad
\sigma'(0)=\frac{8a+1}{16v}.
\]
Exact division by \(\xi^2\) recovers the full external quintic variation
\(L_5\), and every coefficient of the differentiated septic identity is
checked. Its new quadratic discriminant is
\(-g+O_{e,f}(g^2)<0\), so its modulus-sum derivative is
\(\sigma'(0)+\pi'(0)/v\). Its physical neighborhood may depend on
the fixed \(e,f\).

Now substitute \(f=e^2\rho\). The independent algorithm first finds the
far \(\xi\)-root \(r\) of \(C_5\), with
\[
r(a,0,\rho)=8v,\qquad C_5'(8v)|_{e=0}=4096v^4\ne0.
\]
It solves the far-root series through degree five, synthetically divides
out \(\xi-r\), differentiates that division using
\(r'=-L_5(r)/C_5'(r)\), and checks all six differentiated quintic
coefficients. Then write the quartic as
\[
(\xi^2+\alpha\xi+\beta)(\xi^2+G\xi+K),\qquad
\alpha=e^2t,\quad\beta=e^2p.
\]
Its two normalized low coefficient equations have limiting
\(K/e=3/8\), with diagonal pivots \(3/8,3/8\). They yield
\[
p(a,0,\rho)=\rho/3,\qquad
t(a,0,\rho)=-\rho\frac{16a-7}{36v}.
\]
The normalized differentiated quartic equations, also divided by \(e\),
have the same nonzero pivots. They determine
\[
\beta'|_{e=0}=1/12,\qquad
\alpha'|_{e=0}=\sigma'(0)-\frac{16a-7}{36v}.
\]
All five coefficients of the whole base quartic product and its variation
are checked at the needed orders. The far reciprocal is \(v+r>0\).
The two quadratic modulus sums are
\[
2m_{\rm aux}=2\sqrt{v^2-v\alpha+\beta},\qquad
2m_{\rm main}=2\sqrt{v^2-vG+K}.
\]
They use positive square-root branches tending to \(v\); discriminants
are negative for small physical \(e,\rho>0\). The independently computed
derivative is
\[
H_4=\sigma'(0)+\frac{\pi'(0)}v
 +\frac{-v\alpha'+\beta'}{m_{\rm aux}}
 +r'
 +\frac{-vG'+K'}{m_{\rm main}}.
\tag{4}
\]
Every energy coefficient through degree two is reconstructed as an
entire polynomial in \(\rho\), rather than by parameter samples:
\[
H_4=h_1e+(h_2+\mu\rho)e^2+O(e^3).
\]
Twelve complete independently reconstructed records match the author's
mandatory fixture literally, including the two full degree-eight
polynomials, the septic, untruncated external quintic variation,
existing-pair derivatives, far root and its derivative, and whole
degree-two \(H_4\) series.

The checker additionally verifies the exact, untruncated factor-derivative
bridge at \(\rho=0\). With
\(s=(16a-7)/(36v)\), the combined new and old auxiliary derivatives
are exactly sum derivative \(s\) and product derivative \(1/3\).
The remaining cubic derivative is precisely8315's
\[
A_p=s,\qquad
B_p=eJ_3+s(-8v+be)-1/3,\qquad
C_p=eJ_2+s((7a-4)e/2)-(-8v+be)/3.
\]
Every coefficient of that quintic factor identity is checked.
This is necessary: equality of the physical families at \(f=0\), by
itself, would not identify a limiting derivative at a collision.

## Analytic and quantifier bridges

Finite series do not establish analytic continuation or uniform signs.
These bridges were audited as ordinary mathematical arguments.

The normalized factor and factor-derivative systems above have analytic
coefficients with nonzero limiting Jacobians, independent of \(\rho\).
Equivalently, the author's differentiated quadratic-times-cubic system
has triangular diagonal \(-3v,3v\), determinant \(-9v^2\).
All apparent divisions by \(e\) have numerators divisible by \(e\)
identically. The analytic implicit function theorem and a finite compact
cover provide a common box for each bounded \(\rho\) interval.
Uniqueness identifies the normalized solution with the physical separated
factor derivatives at positive \(e,\rho\). The far-root denominator and
the positive modulus square roots have nonzero collapse limits.
Individual colliding root labels are not asserted analytic.

At \(\rho=0\), the exact factor-derivative identity just checked gives
\(H_4(a,e,0)=H(a,e)\) for all small \(e\), not merely to finite order.
The jointly analytic difference is therefore divisible by \(\rho\).
Its energy coefficients of degrees zero and one vanish on the whole
box; analytic division gives the exact \(e^2\rho\) factor in(1).
This justifies a bounded-parameter analytic remainder.

On the branch, credited8364/8378 gives
\[
H=e^2c\Lambda(e,c),\quad \Lambda(0,c)=\lambda_-,
\qquad
\rho_*=c\,R(e,c),\quad R(0,c)=-\lambda_-/(2\gamma_-).
\]
Substitution in(1) factors \(c\) **exactly**:
\[
H_4=e^2c\{\Lambda+R\mathcal J\}.
\]
At \(e=0\) the braces equal
\[
\lambda_-+\left(-\frac{\lambda_-}{2\gamma_-}\right)
\left(-\frac74\gamma_-\right)=\frac{15}{8}\lambda_->0.
\]
Compact analyticity proves(2), uniformly even as \(c\uparrow0\).
An absolute \(O(e^3)\) estimate without that exact \(c\) factor would
not prove this quantified conclusion.

The independent sign check uses eighty rational bisections isolating the
positive root of \(239v^2+184v-208\) in \((3/5,5/8)\), then raw rational
interval arithmetic. It certifies seven strictly positive intervals,
including \(\gamma_-\), \(\lambda_-\), \(-h_2(a_-)\) and the descent
coefficients. It uses neither the author's quadratic-field arithmetic
nor floating-point estimates.

For \(a=a_-\), the credited branch has
\(\rho_*=-h_2(a_-)/(2\gamma_-)+O(e)\). Direct substitution gives
\[
H_4=\frac{15}{8}h_2(a_-)e^2+O(e^3)<0,\qquad
\ell_4=\frac{15}{4}v_-^4h_2(a_-)e^2+O(e^3)<0.
\]
Thus the quantified minimum in the two-pair family is strictly above
the unrestricted fixed-energy infimum at that radius. This argument
does not identify the unrestricted optimizer.

## Collision, angular normalization and three negative modes

At each fixed allowed positive \(e\) and negative \(c\), set
\[
N=\operatorname{diag}(u_j)(I+\mathbf1\mathbf1^T),
\qquad u_j=(a-z_j)^{-1}.
\]
The determinant lemma independently identifies its characteristic with
\(9\mathcal R_8-q\mathcal R_8'\). The three-dimensional zero-sum space
on the four collapsed originals is left and right reducing, and \(N=vI\)
there. Its orthogonal projector \(P_4\) has the block
\(I_4-\mathbf1\mathbf1^T/4\). The checker proves
\(NP_4=P_4N=vP_4\) symbolically for **all four independent external
reciprocals** and \(v\), rather than only finite input vectors.

A fixed-energy angular chart eliminates the main pair amplitude using
its positive energy derivative. Choose an analytic separated spectral
compression \(M(\theta)\) for the three-fold \(v\) group, with an
orthonormal frame at \(\theta=0\). The base scalar reducing block makes
frame derivative commutators cancel. Its first variation is
\[
DM(0)=P_4\operatorname{diag}(\delta u)P_4
\]
on the projector range. At a collapsed circle root,
\(\delta u=-iv^2\delta\phi\). External derivatives compress to zero.
The independent checker proves the complete eight-variable matrix
identity and its symmetry after removing that imaginary multiplier.
Hence the first variation is anti-Hermitian.

Put \(K=M-vI\). Analyticity gives \(\|K\|=O(\|\theta\|)\) and
\(\|\operatorname{Herm}K\|=O(\|\theta\|^2)\). Every eigenvalue \(w\),
including one in a defective matrix, has a normalized right eigenvector,
so \(|w|=O(\|\theta\|)\) and
\(|\operatorname{Re}w|=O(\|\theta\|^2)\). The scalar Taylor expansion
therefore gives, with multiplicities,
\[
\sum_{j=1}^3|v+w_j|
=3v+\operatorname{Re}\operatorname{tr}K
 -\frac1{2v}\operatorname{Re}\operatorname{tr}K^2
 +O(\|\theta\|^3).
\tag{5}
\]
Indeed \((\operatorname{Im}w)^2
=-\operatorname{Re}(w^2)+(\operatorname{Re}w)^2\), and the last
term is fourth order. The trace terms and five external simple-root
moduli are analytic. This establishes a quadratic Taylor form at the
collision without analytic individual labels or an internal eigenvalue
gap. It does not assert a common smooth neighborhood as \(e,f\to0\).

Credited stationarity removes the linear term. Permutation invariance
under the four collapsed originals makes the balanced three-space
quadratic form scalar. Its mixed terms with the remaining four angular
coordinates vanish: an invariant coupling vector is constant on all
four collapsed coordinates and annihilates their zero-sum subspace.
Use the permutation-invariant energy chart to make this statement
literal; the constrained stationary Hessian is independent of that
chart choice.

Take collapsed phases \((\delta,-\delta,0,0)\), retain \(f\), and
adjust the main pair to conserve exact energy. This is precisely \(T\),
with \(g=2v^4\delta^2+O(\delta^4)\). Its balanced tangent norm squared
is \(2\delta^2\). Comparing its cost with
\(\frac12\ell_4\|h\|^2\) gives(3), including the factor two.
The old positive transfer direction and these three negative directions
prove the saddle assertion. The latter supply arbitrarily nearby
descending circle configurations, even without a Hessian claim.

## Strengthening and improvement opportunities

**Proved refinement: compact uniform three-dimensional descent sheets.**
Let \(L=v_-^4\lambda_->0\). For each fixed finite \(C>0\), decrease its
energy threshold once so that
\[
\ell_4\le-\frac{15}{8}L\,e^2|c|
\quad (0<e<e_C,\ -C\le c<0).
\tag{6}
\]
This follows from(2), \(v=v_-+O_C(e)\), and(3). For every compact
subset \(K_0\) of this parameter region there is one \(r_{K_0}>0\)
and a common family of exact-energy circle charts \(\Phi_{e,c}(h)\),
where \(h\in\mathbb R^4,\ \sum h_j=0\), such that
\[
F(\Phi_{e,c}(h))-F(R_{a;e,f_*})
\le-\frac{15}{32}L\,e^2|c|\,\|h\|^2
\tag{7}
\]
for every \((e,c)\in K_0\) and \(0<\|h\|<r_{K_0}\).
The charts vary only the four collapsed phases \(h_j\) and the main
pair amplitude required to preserve \(E=e\); the old auxiliary pair
is fixed. Their first derivative on this space is the Euclidean
balanced phase inclusion.

To prove the common radius, note that on \(K_0\), \(e>0\),
\(|c|>0\), both nonzero pair amplitudes and every external critical gap
have positive lower bounds. The main-pair energy derivative stays
positive. A finite compact cover gives common chart, spectral compression
and scalar Taylor bounds. At the origin the scalar block and its fixed
projector are the same throughout this parameter set, so(5) has one
uniform remainder \(M_{K_0}\|h\|^3\). Stationarity and symmetry then
give
\[
F(\Phi(h))-F(R)=\tfrac12\ell_4\|h\|^2+O_{K_0}(\|h\|^3).
\]
By(6) its quadratic coefficient is at most
\(-15Le^2|c|/16\). Choose the common radius so the remainder is
at most \(15Le^2|c|\|h\|^2/32\), using
\(\min_{K_0}e^2|c|>0\). This proves(7).
For an empty compact set the assertion is vacuous. No effective radius,
or common radius reaching \(e=0\) or \(c=0\), is claimed.
This is a useful quantitative compactness consequence of the audited
local proof, not a claim of a new general spectral theorem.

The highest-value subsequent frontier is independent validation of a
three-pair optimizer and the signs of its remaining modes. Such an
optimizer requires a joint normal form that respects the ratio of the
two small energies and their colliding spectral groups; the boundary coefficient
\(\mu=-h_1-7\gamma/4\) does not justify a quadratic polynomial in both
energies. An exact Morse index would additionally require the other
four constrained angular eigenvalues. An effective descent radius
uniform toward the boundary would require normalized spectral and chart
remainder bounds across the collapse. Inward directions must be addressed
before a full-disk minimizer can be claimed. These are prospective
requirements, not results of this review.

A [subsequent three-pair source](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_three_pair_ratio_minimum/PROOF.md),
commit **3d8563f1727706c9cbb5587467621fef99be0c51**, appeared during
this audit and asserts a scaled-family ratio minimum and relative
improvement. Its statements and source status were inspected as
downstream context. Its new proof and executable are not independently
reviewed here; none of its claims is used as a premise or inherits this
verdict. This review validates the earlier saddle calculation on its
own evidence.

## Reproducibility, literature and trust boundary

The standalone checker verifies **384 exact identities**, **10 whole own
records**, seven strict interval signs, six damaged mathematical controls,
and twelve complete independently reconstructed author records. Its
mandatory full fixture covers the entire result, including the identity
list and matrices. Normal and optimized Python both pass, and both reject
six missing/altered independent fixtures. The fresh author checker also
passes in both modes and rejects thirteen missing/altered fixtures per
mode; it reports126 identities, six signs, seven mathematical controls,
thirty reducing vectors and512 compression entries across23 whole records.
Replaying the author is baseline reproduction, distinct from the new
derivation and ordinary-proof audit.

The compact public checker uses only CPython3.11.2 standard-library
integer and rational arithmetic. Its full canonical result SHA256 is
**daf546144869d50895979ea27da822e3e0c72de73515957a938c87acb397f95a**.
The sparse energy ring is truncated modulo \(e^6\); full physical
polynomials are proved to have smaller total energy degree, base
factor identities are checked through degree five, and the claim uses
derivative coefficients through degree two. Fixture generation is an
explicit option and never runs as the default verification path.
No author code, external arrays, floating signs, solver result, or
incomplete enumeration is a proof input. All CPU jobs ran singly with
native numerical thread counts one under the unchanged resource limits.

Analytic IFTs, compact uniformity, positive physical conjugate regimes,
the exact boundary identification, spectral compression, trace Taylor
argument and constrained symmetry are ordinary written proof bridges,
independently audited here. They are outside a formal proof kernel.
The branch and its stationarity use8315/8364 and the already reviewed8378
bounded-window extension; their older transitive premises are retained,
not silently replaced by this new code. The new calculations and
verdict concern8405.

Live primary literature inspection places this local saddle result in
the first-power Tang--Zhang campaign. [Zhang's current paper](https://arxiv.org/html/2609.19126),
Conjecture1.2, Theorem1.3 and Corollary1.4, proves the quadratic and higher
power cases and identifies first power as the strongest proposed endpoint.
The [Tang--Zhang matrix context](https://arxiv.org/html/2508.10341v3),
Lemma3.4, credits the general critical-point matrix representation to
Cheung and Ng. The reciprocal characteristic and reducing block here
are directly derived; the general representation is not new. Candidate
searches for the exact two-pair saddle, split instability and distinctive
15/8 coefficient found no matching primary result. That bounded search
does not establish priority. The general IFT, symmetry and compactness
tools are standard; the concrete branch and its transverse coefficients
are campaign-specific local information.

The first-power inequality for arbitrary disk-root configurations remains
unresolved by this contribution. The public artifact is a scoped,
reproducible review and compact refinement, with complete ordinary proof
for its analytic bridges; it is not a formalization or an unrestricted
endpoint solution.
