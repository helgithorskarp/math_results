# Independent critical-phase audit and stronger energy entry

Actual author **six-reviewer-1**, role **independent mathematical reviewer**,
2026-10-02. Target selected independently from committed evidence; no
researcher assignment, desired verdict or quota. A shared signing key is
not evidence of independent authorship. This is an ordinary unformalized
review with independent exact controls.

## Target, verdict and exact scope

Target **LEMMA9307/0**, **Collective critical-phase energy estimate and
expanded original-root stability entry in degree nine**, actual author
six-sendov-1, researcher, reference
**bafkreiapzgjpqy7ehb2zu7dr52e5xs4p3wlkpty2l7dbrzodyst2ji3qmu**.
Original source commit **6b6a8c755c6e565fee9df0cb15899a29563069f1**:
[complete source proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/energy-phase-routing/PROOF.md),
[original checker](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/energy-phase-routing/verify.py),
[original fixture](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/energy-phase-routing/expected.json).
The complete committed body and directed neighborhood were read, as were
the precise parent statements. No existing sufficient assessment of9307
was found in the bounded committed campaign context. Other reviewers'
active or sufficient scopes were respected.

**CONFIRMS the new spectral phase theorem, original-to-critical entry,
aggregate-domain containment and legal strict-enlargement witness.**
The Schur step is valid for arbitrary complex, nonnormal matrices and
colliding light eigenvalues. The heavy root is simple by a separated
one-root count, rather than an assumed smooth branch. The actual-polynomial
coefficient bridge preserves all eight critical multiplicities. No gap
was found in the target's new ordinary argument.

**PROVED REFINEMENTS under the same hypotheses:** writing
\(t=\epsilon/\ell\),
\[
 \rho^2\le\left(\frac{1+15t/4}{1-t}\right)^2\frac{E}{\ell^2}
 \le\frac{51}{50}\frac{E}{\ell^2},
 \qquad A\le0\ \Longrightarrow\ S\le\frac{12}{5}E.
\]
These improve the target's sufficient phase coefficient \(41/40\) and
its inherited radial bound \(10E\). They imply entry already when
\[
 E\le\frac{\gamma}{163200d^2}
 \quad\text{or}\quad
 B_{\rm orig}:=\sum_{k=1}^8|z_k+1|^2\le\frac{d^2\gamma}{164000},
\]
where the original denominators were164000 and165000, respectively.
Both sufficient domains enlarge strictly; separate exact legal \(A=0\)
witnesses below certify this. The constants are sufficient, not optimal.

The final stability surplus and its equality classification are confirmed
**as the stated implication from the explicit LEMMA9189 stability
premise**. This review does not independently validate9189's higher
majorants or full heavy-fiber certificate. The entry proof below rederives
the localized-root and radial pieces used from9257; it supplies no verdict
on that contribution's unrelated chart comparisons. No verdict transfers
to7348,7290,9111,9168 or9289 through citations. The global first-power
conjecture, effective global competitor entry and a largest known baseline
region are outside this review.

## 1. Definitions and the actual reciprocal polynomial

The abstract statement assumes
\(1/2\le\ell\le1\), \(u_k=\ell+v_k\),
\(\epsilon=\max_k|v_k|\le1/1000\),
\(E=\sum|v_k|^2\), \(M=\sum v_k\), \(A=\Re M\).
Let \(g(q)=\prod(q-u_k)\), \(\chi(q)=9g(q)-qg'(q)\),
and let all eight zeros of \(\chi\) be counted algebraically.

For the physical corollary,
\[
 p(z)=C_0(z-a)\prod_{k=1}^8(z-z_k),\quad C_0\ne0,\quad
 5/8<a\le1,\quad |z_k|\le1,\quad d=1+a,\quad
 \ell=d^{-1},\quad\gamma=a-5/8.
\]
A finite energy hypothesis requires a simple marked root;
\(u_k=1/(a-z_k)\). A multiple marked root has infinite reciprocal
energy and infinite critical sum, rather than a finite counterexample.
In the shift \(w=z-a\), up to a nonzero constant,
\(p(a+w)=w\prod(1+u_kw)\). Its derivative has ascending coefficients
\((k+1)e_k(u)\). Substituting \(w=-1/q\) and multiplying by \(q^8\)
gives exactly
\[
 \chi(q)=\sum_{k=0}^8(-1)^k(k+1)e_k(u)q^{8-k}.
\]
The change is invertible at every finite critical point because
\(p'(a)\ne0\); \(u_k\ne0\) makes \(\chi(0)\ne0\).
Thus these zeros are precisely \(q_j=1/(a-\zeta_j)\), with multiplicity.
Its first coefficient gives \(\sum q_j=2\sum u_k\).
This calculation uses no distinctness of original or critical roots.

Set \(H=J/8\), \(P=I-H\), \(S_0=P+3H=I+J/4\).
These real Hermitian matrices satisfy
\(S_0^2=I+J\), \(S_0^{-1}=P+H/3\).
The complex symmetric matrix
\(L=S_0\operatorname{diag}(u)S_0\) is similar to
\(\operatorname{diag}(u)(I+J)\).
Each principal minor on a subset of size \(k\) is
\((k+1)\prod u_i\): the all-ones matrix has one eigenvalue \(k\)
and \(k-1\) zero eigenvalues. The characteristic coefficient formula
therefore gives \(\det(qI-L)=\chi(q)\) identically.
This matrix framework is already explicit in7348; it is credited.
Complex symmetric does not mean Hermitian or normal.

## 2. Separated disks and a finite heavy-root remainder

This classical localization is rederived to close the reviewed bridge.
For \(q\) outside \(|u-\ell|\le\epsilon\), the image of that disk under
\(u\mapsto1/(q-u)\) is the convex closed disk with center
\(\overline{q-\ell}/(|q-\ell|^2-\epsilon^2)\) and radius
\(\epsilon/(|q-\ell|^2-\epsilon^2)\). It excludes zero.
At a zero of \(\chi\) outside the small disk,
\(\sum1/(q-u_k)=9/q\). The average equals \(1/(q-u_*)\)
for some \(|u_*-\ell|\le\epsilon\), whence \(q=9u_*\).
Zeros at repeated \(u_k\) are already in the small disk; no pole is used.
Every zero is therefore in one of the two disks
\[
 |q-\ell|\le\epsilon,\qquad |q-9\ell|\le9\epsilon.
\]
Along the homotopy \(u_k=\ell+\tau v_k\), \(0\le\tau\le1\), the
circle centered at \(9\ell\) of radius \(4(\ell+\epsilon)\) separates
the disks because \(5\epsilon<4\ell\). Its root count stays fixed.
At \(\tau=0\), \(\chi=(q-\ell)^7(q-9\ell)\), so there are exactly
seven light zeros and one heavy zero \(q_1\). All have positive real
parts. The heavy root is simple, including when light roots collide.
Polynomial root continuity, or the argument principle on this fixed
circle, justifies the count; no numerical root enumeration is involved.

Put \(w=q_1-9\ell\). The heavy secular equation
\(\sum u_k/(q_1-u_k)=1\) implies the exact identity
\[
 w(q_1-\ell)=q_1\left[M+\sum_k\frac{v_k^2}{q_1-u_k}\right].
\]
Thus
\[
 R:=w-\frac98M
 =-\frac{wM}{8(q_1-\ell)}
   +\frac{q_1}{q_1-\ell}\sum_k\frac{v_k^2}{q_1-u_k}.
\]
Our closed hypotheses give
\(|q_1-\ell|\ge7\ell\), \(|q_1-u_k|>3\),
\(|q_1/(q_1-\ell)|\le8/7\),
\(|w|\le9\epsilon\le9\sqrt E\), and \(|M|\le\sqrt{8E}<3\sqrt E\)
when \(E>0\). Consequently
\[
 |R|\le\left(\frac{27}{28}+\frac8{21}\right)E
       =\frac{113}{84}E<2E.
\]
This retains the target's credited9257 finite remainder calculation.
At \(E=0\) all displacements and remainders vanish exactly.

## 3. Full collective phase budget, including nonnormal collisions

Write \(v=x+iy\), \(E_y=\sum y_k^2\), \(b=\sum y_k\), and
\(V=S_0\operatorname{diag}(v)S_0\).
The Hermitian imaginary part is \(K=(L-L^*)/(2i)=S_0\operatorname{diag}(y)S_0\).
Complete matrix expansion gives
\[
 \|K\|_F^2=3E_y+b^2\le11E_y,
 \quad \|PKP\|_F^2=\frac34E_y+\frac{b^2}{64},
 \quad \|PV\|_F^2=\frac{15}{8}E-\frac{|M|^2}{8}\le\frac{15}{8}E.
\]
These are whole quadratic identities. They include the off-diagonal
rank-one terms and the real and imaginary components, rather than only
sampled directions. The independent checker rebuilds their entire
coefficient matrices by exact polarization of the literal matrices.

Choose a unit **right** eigenvector \(\psi\) for the heavy root, and set
\(P_\psi=I-\psi\psi^*\). From
\((q_1-\ell)P\psi=PV\psi\),
\[
 \|P\psi\|\le\frac{\sqrt{15/8}}{7\ell}\sqrt E.
\]
For two rank-one orthogonal projections, their difference has operator
norm equal to the sine of the angle between their ranges. Hence
\(\|P_\psi-P\|_{\rm op}=\|P\psi\|\).
Telescoping both factors around \(K\) gives
\[
 \|P_\psi KP_\psi-PKP\|_F
 \le2\|P_\psi-P\|_{\rm op}\|K\|_F
 \le\frac{2\sqrt{165/8}}7\frac{E}{\ell}.
\]
This inequality does not select light eigenvectors or differentiate them.

Complete \(\psi\) to a unitary basis \((\psi,W)\).
The first column of the transformed \(L\) is \((q_1,0,\ldots,0)^T\).
Its lower block \(B=W^*LW\) therefore has exactly the seven remaining
characteristic roots with multiplicity. The Hermitian imaginary part of
this block is \(W^*KW\). Apply unitary Schur triangularization to \(B\).
The diagonal of its transformed Hermitian imaginary part consists of
\(\Im q_j\), \(j\ge2\). Their squared sum is at most the full squared
Frobenius norm, which is unitarily invariant. It follows that
\[
 \left(\sum_{j=2}^8(\Im q_j)^2\right)^{1/2}
 \le\left(\frac34E_y+\frac{b^2}{64}\right)^{1/2}
      +\frac{2\sqrt{165/8}}7\frac{E}{\ell}.
\]
This argument explicitly handles nonnormal matrices and any light-root
collision. Schur is applied to the full block, not an assumed diagonalization.
The heavy remainder gives the correctly scaled additional estimate
\[
 \frac{|\Im q_1|}{9}\le\frac{|b|}{8}+\frac{113}{756}E.
\]
Combine these two nonnegative bounds in the Euclidean norm of
\(\mathbb R^2\). The leading squared budget is
\(3E_y/4+b^2/32\le E_y\le E\), by \(b^2\le8E_y\).
The squared error budget is
\[
 \left[\frac{165}{98}\frac{E^2}{\ell^2}
       +\left(\frac{113}{756}\right)^2E^2\right]
 \le t^2 E\left[\frac{660}{49}
                +8\left(\frac{113}{756}\right)^2\right]
 <\left(\frac{15t}{4}\right)^2 E,
\]
because \(E\le8\epsilon^2\) and \(\ell\le1\).
Every square-root comparison was replaced by its exact positive rational
squared margin in the checker. Consequently
\[
 \left[\sum_{j=2}^8(\Im q_j)^2+(\Im q_1/9)^2\right]^{1/2}
 \le(1+15t/4)\sqrt E.\tag{*}
\]
For positive real parts, \(|\arg q|\le|\Im q|/\Re q\).
Light real parts are at least \(\ell-\epsilon\); the heavy real part
divided by9 has the same lower bound. Thus
\[
 \rho^2\le\left(\frac{1+15t/4}{1-t}\right)^2\frac{E}{\ell^2}.
\]
The displayed rational function increases on \([0,1/500]\). At the
closed upper endpoint it is \((2015/1996)^2<51/50\), proving the stated
refinement. This also independently proves the target's weaker bound.
The target's own coarser path \(((1+5t)/(1-t))^2\le(505/499)^2<41/40\)
has a strictly positive exact margin and is valid.

The leading coefficient1 is necessary, as claimed in the target: for all
\(u_k=\ell+i\tau\), the zeros are \(\ell+i\tau\) seven times and
\(9(\ell+i\tau)\) once. Then
\(\rho^2/(E/\ell^2)=[\arctan(\tau/\ell)/(\tau/\ell)]^2\to1\).
For the physical case \(\ell=1/(1+a)\), putting
\(z_k=a-1/(\ell+i\tau)\) is legal, since the reciprocal disk excess
is \((1-a^2)\tau^2\ge0\). This is a limiting necessity statement;
neither51/50 nor41/40 is asserted to be optimal.

## 4. Stronger radial estimate and complete physical entry

Gauss--Lucas puts all critical points in the unit disk. For the small
principal arguments, the critical disk constraint is
\((1-a^2)r^2+2ar\cos\theta\ge1\). Its positive threshold is the
stated \(h(a,\theta)\). It remains nonsingular at \(a=1\), where it
is \(1/(2\cos\theta)\). All phases here are small by localization;
\(h\ge\ell\). The seven slacks are nonnegative.

The exact first trace and remainder give
\[
 \sum_{j=2}^8(\Re q_j-\ell)=\frac78A-\Re R.
\]
Also \(|q|-\Re q=(\Im q)^2/(|q|+\Re q)\).
When \(A\le0\), using \((*)\),
\[
 S\le\frac{113}{84}E+
       \frac{(1+15t/4)^2}{2(\ell-\epsilon)}E
 \le\left[\frac{113}{84}
           +\frac{(403/400)^2}{499/500}\right]E
 <\frac{12}{5}E.
\]
Use a weak inequality at \(E=0\). This proof explains the improvement:
it uses the collective imaginary budget rather than bounding each of the
seven imaginary parts separately by the maximum displacement. It proves
the reviewed radial statement directly, without importing9257's bound.

Under \(E\le\gamma/(163200d^2)\),
\[
 \epsilon^2\le E\le\frac{3/8}{163200(13/8)^2}<10^{-6},
 \quad\rho^2\le\frac{51}{50}d^2E\le\frac{\gamma}{160000},
 \quad S\le\frac{12}{5}E\le\frac{\gamma}{64}.
\]
Thus the complete explicit entry domain of9189 is reached. The same
proof verifies the target's original, smaller energy domain.

For the aggregate original-root sufficient condition, set
\(\delta=\max|z_k+1|\), \(x=\delta/d\).
From \(B_{\rm orig}\le d^2\gamma/164000\) we get
\(x\le\sqrt{\gamma/164000}<1/640\): use
\(\gamma\le3/8<25/64\), \(164000>400^2\).
Hence \(|a-z_k|\ge d-\delta>0\); the marked root is simple. Exactly,
\[
 E=\sum_k\frac{|z_k+1|^2}{d^2|a-z_k|^2}
 \le\frac{B_{\rm orig}}{d^2(d-\delta)^2}
 <\frac{\gamma}{164000d^2(639/640)^2}
 <\frac{\gamma}{163200d^2}.
\]
The last margin \(164000(639/640)^2-163200\) is positive exactly.
The inverse-distance cost is retained. Entry is not inferred from an
uncorrected aggregate energy approximation.

The older9257 maximum-distance domain
\(\delta\le d\sqrt\gamma/1200\) implies
\(B_{\rm orig}\le d^2\gamma/180000\), so it is retained in both the
original9307 and the strengthened aggregate domain. The author witness,
\(a=1\), six roots \(-1\), and two roots
\(-999999/1000001\pm i2000/1000001\), has
\(A=0\), \(E=1/2000000\), \(B_{\rm orig}=8/1000001\), and
\(\delta^2=4/1000001>1/960000\). It is legal and lies in9307's
aggregate domain but outside9257's maximum-distance domain.
It already meets7348's older baseline criterion
\(E<(3/4)/1154736\); this is a new coordinate entry, not a newly
established baseline.

For strictness of each new domain, take \(a=1\), six reciprocals \(1/2\),
and \(u_\pm=1/2\pm i/h\), defining roots \(z_\pm=1-1/u_\pm\).
Their moduli equal1, \(A=0\), \(E=2/h^2\),
\(B_{\rm orig}=32/(h^2+4)\).
For \(h=1868\),
\[
 \frac{3/8}{164000\cdot4}<E\le\frac{3/8}{163200\cdot4}.
\]
For \(h=1872\),
\[
 \frac{4(3/8)}{165000}<B_{\rm orig}\le\frac{4(3/8)}{164000}.
\]
These are separate witnesses. A sufficient aggregate condition is more
restrictive than the corresponding reciprocal-energy condition; neither
witness is asserted to satisfy both strictness comparisons.

## 5. Exact inherited premise, first trace and equality

The only unreproduced mathematical premise for the final surplus is
**LEMMA9189/0**,
**bafkreigmvirwpqszpawjcrqchwuwtued64ah4sunjc464jruwo7h6oyobq**,
[explicit stability theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/effective-squared-basin/PROOF.md),
source **ba5ede34ad28773c2409b64e8fdc500280cf5f6d**:
for \(5/8<a\le1\), positive critical radii with the seven nonnegative
slacks and the entry domain above, the origin constraint
\[
 |O|\le\prod r_j,\qquad
 O=9\int_0^1\prod_j(1-atq_j)\,dt
\]
and the polar constraint \(|C|\ge1\) for \(a<1\), where
\(C=\int_0^1\prod_j(a+(1-a^2)tq_j)\,dt\), imply
\[
 F\ge16/d+\gamma[(3/10)S+\rho^2/100].
\]
At \(a=1\) replace the polar condition by \(\Re\sum q_j\ge8\).
No upper bound on the heavy radius is a hypothesis. The complete9189 body was retrieved; its theorem statement and
application boundary were read;
its complete higher-order certificate is not independently audited here.
The coefficients3/10 and1/100, inherited via9189 from review9168,
retain that upstream credit.

For completeness, actual polynomials satisfy these communication
conditions, independently of our matrix estimates. Write \(e_k(q)\)
for critical elementary symmetric polynomials. The exact coefficient law
\(e_k(q)=(k+1)e_k(u)\) gives
\[
 O=9\sum_k\frac{(-a)^k e_k(q)}{k+1}
   =9\prod_k(1-au_k)=\left(\prod_j q_j\right)\left(\prod_k z_k\right),
\]
using eight factors and \(\prod q_j=9\prod u_k\).
It gives also
\[
 C=\sum_k\frac{a^{8-k}(1-a^2)^k e_k(q)}{k+1}
   =\prod_k[a+(1-a^2)u_k]
   =\prod_k\frac{1-az_k}{a-z_k}.
\]
The disk identity
\(|1-az|^2-|a-z|^2=(1-a^2)(1-|z|^2)\ge0\)
proves the polar modulus inequality. At \(a=1\), every original
reciprocal has real part at least1/2; the first trace gives the required8.
These are classical identities, not new communication laws.

For \(A>0\), the first trace directly gives
\(F=16\ell+2A+\sum_j(|q_j|-\Re q_j)>16\ell\).
Thus the nonpositive-trace surplus above and this positive-trace argument
cover the two cases, without asserting a uniform energy surplus in the
positive-trace case. With the9189 premise, equality forces \(S=\rho=0\),
then \(q=(9\ell,\ell^7)\). Comparing all characteristic coefficients
forces \(g=(q-\ell)^8\), hence every original root is \(-1\).
Conversely the collapsed polynomial gives equality.
This known equality family is rechecked, not claimed new.

For a complex marked root \(\alpha=a\omega\), \(|\omega|=1\), rotate
by \(\overline\omega\). The normalized reciprocals are
\(\omega/(\alpha-z_k)\) and \(\omega/(\alpha-\zeta_j)\);
the aggregate shift is \(\sum|z_k+\omega|^2\).
Norms, principal phase conventions, characteristic multiplicities and all
inequalities above are preserved.

## Strengthening and improvement opportunities

**Proved here:** the dynamic phase coefficient with15/4, uniform51/50,
radial bound12/5, denominators163200/164000 and exact separate strict
witnesses. These require no stronger hypotheses or parent theorem.
The existing moving-projection and Schur architecture belongs to9307;
this review keeps sharper norm budgets and combines its collective
imaginary estimate with the radial identity. No exclusive literature
priority is asserted for these sufficient constants.

**Next consequential bridge:** independent audit of9189's full explicit
majorants and unrestricted heavy-radius argument would remove the stated
inherited trust boundary from the quantitative surplus application. The
model verdict in9168 alone does not establish that domain.

**Possible further sharpening:** retain \(E_y\), \(b\), \(|M|\) in the
projection estimates and \(\ell\) in the error coefficient before taking
uniform endpoints. The exact leading loss is
\(E-E_y+(8E_y-b^2)/32\). It may improve entry for nonuniform imaginary
perturbations. A complete error-versus-loss inequality is needed before
claiming a better uniform coefficient or larger domain. The coefficient1
limit for equal imaginary displacements prevents decreasing the leading
constant below1, but does not prove an optimal finite-radius coefficient.

**Broader-degree route:** the classical matrix has
\(P+\sqrt n H\) for general degree. A degree-dependent collective
phase and finite heavy-remainder proof, followed by a separately established
critical stability theorem, would be required. Matrix representation and
Schur alone are classical; merely restating them is not a new general theorem.

**Global scope:** a local antipodal entry region does not cover every
possible minimizer or competitor. A global original-to-critical reduction
or complementary-domain proof is required for the unrestricted first-power
endpoint. No finite sample or repeated packaging supplies that bridge.

## Reproducibility, independence and trust

[Independent checker](check.py), [full compact expected record](expected.json),
[optional shared-record comparison](compare_author.py),
[validation evidence](VALIDATION.json), and [reproduction commands](README.md).
CPython3.12.14, standard-library exact integers/Fraction and the reviewer's
own Gaussian rational pairs. One serial mathematical job; six native thread
variables1; unchanged1CPU2GiB;90-second independent internal/110-second
outer guards; original author45-second outer guards.

The independent implementation uses literal8-by8 matrices, complete
quadratic polarization, two determinant algorithms on all256 principal
minors, Faddeev--LeVerrier characteristic reconstruction and direct
shifted-polynomial derivative coefficients. It constructs a rational
nonnormal example with an exact heavy right eigenvector and five colliding
light roots. Every projector entry, sine identity, nonlinear Frobenius
control, heavy remainder and original communication control is compared.
Three exact physical witnesses and closed rational endpoints include
\(E=0\), \(\epsilon=1/1000\), \(\ell=1/2,1\), and \(a=1\).
The finite controls do not enumerate an unbounded complex domain;
the ordinary proof supplies that bridge.

The first entire independent fixture was
recorded **before reading the author's executable or expected fixture**.
The original committed body, ordinary proof and credited defining matrix
were already visible, so this is independent implementation rather than
blind review. Subsequent sharper radial constants, direct communication
controls and optional shared-record comparison were added after reading
the author engine; they import no author code. Native original normal and
optimized replays are separately identified. Own semantic damage controls
remain active under optimization. Entire fixture equality rejects changes
to any field, including added fields; it is not a hash-only comparison.

The final fixture contains19 strict margins and761 exact predicates
including8 semantic damage rejections; exact measured output and hashes
are recorded inVALIDATION.json. The optional comparison reconstructs all
6 shared matrices,8 whole polynomial records,256 minor records,17 original
margins and the complete original witness without importing author code.
Native full original normal/optimized runs and their8 damage controls
pass. Source links, full remote bytes and frozen normal/optimized replay
are checked before graph submission; actual commitment is checked separately.

Trust boundary: inspected small exact arithmetic/matrix code; ordinary
finite-dimensional spectral theory, disk inversion/root counts, Schur
triangularization, projection/Frobenius norms, Cauchy--Schwarz, argument
inequality and Gauss--Lucas; elementary polynomial communication laws;
and the explicitly imported9189 premise for the final surplus. No proof
assistant, floating eigensolver, interval root output, CAS, SAT/LP solver,
random trial or private corpus establishes the theorem. No mathematical
nonexistence is inferred from operational limits. Shared keys, author
replays and publication are distinct from independent proof evidence.

## Primary literature and prior art

The candidate-specific live primary-source check on2026-10-02 includes
[Teng Zhang, quadratic Tang--Zhang inequality](https://arxiv.org/html/2609.19126),
Conjecture1.2 and Theorem1.3. The paper distinguishes the stronger
first-power endpoint from its established quadratic case. The present
local result does not resolve that endpoint. [Tao's August2026 account](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
reports the ordinary Sendov/Phelps--Rodriguez resolution; that historical
seed is distinct from this campaign's active stronger target.

[Chaiya--Hinkkanen, critical points paper](https://www.bc.umcs.pl/Content/21935),
page2, states Walsh's two-circle localization. The disk geometry used here
is classical and is rederived with multiplicities above.
[Kushel--Tyaglov, Circulants and critical points of polynomials](https://arxiv.org/pdf/1512.07983),
Theorem2.6 and Section3, supplies explicit classical Schur/Frobenius and
Schoenberg context. [Khavinson--Pereira--Putinar--Saff--Shimorin](https://arxiv.org/pdf/1010.5167),
Section6, discusses diagonal operators, differentiator compressions and
polynomial variance geometry. These mechanisms are credited, not claimed
new. The live exact-constant and distinctive-phase search found no primary
paper supplying the literal reviewed51/50 entry statement; that bounded
search is not proof of historical priority.

Within the campaign,7348 already has the linear reciprocal matrix,
quartic stability, square-root scale and a stronger original-energy
baseline surplus.7290 owns its earlier baseline/cutoff/equality.9257 owns
the previous maximum-distance routing and finite remainder.9307 owns the
new moving heavy projection, collective phase architecture and aggregate
entry.9189 owns its effective critical stability domain and inherits the
stronger model coefficients from9168.9289 separates the complementary
complex branch from the antipodal domain in its precise scope; it is
context only. Review readiness here concerns the new9307 content and
proved refinements; the inherited9189 application boundary remains explicit.
