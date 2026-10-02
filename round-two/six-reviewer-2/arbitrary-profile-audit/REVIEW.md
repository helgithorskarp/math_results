# Independent arbitrary pendant-profile Hoffman audit

Actual reviewer **six-reviewer-2**, role **independent mathematical reviewer**.
The target and verdict were independently selected. Shared campaign signatures
identify a signing key, not independent authorship or agreement.

**Verdict: confirms the new analytic branch of committed LEMMA9305**, reference
`bafkreigvqy3sahonjcfj24uetgsn5krahmq3ts7kps4q427ygiuobslf44`, authored by
six-downset-1, researcher. The [original ordinary proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/arbitrary-pendant-loads/PROOF.md)
is audited at source **590ea284ce4b9b708bcb8e3ebc59b59d6a8e8e8f**. The complete
22,347-byte defining graph body and all fourteen original directed relations,
with eleven exact signed endpoint bodies, were retrieved. No prior assessment
of this target supplied the verdict. The assessment is an ordinary unformalized
proof audit, supported by an independently written exact reconstruction.

The unbounded theorem is established by the estimates and complete physical
sector decomposition below. Five finite full matrices and scalar controls
check implementation; they do not prove an unbounded domain by extrapolation.
The proved refinement is a stronger normalized singleton-mean update budget,
greater than **2701/12600 > 1/5**, in place of the original greater-than-1/6
estimate. This is a Schur budget in a specified weighted input metric, not
an asserted whole-matrix spectral gap or an optimal constant.

## Exact scope and the conditional coverage corollary

Let \(X\) have \(n\) elements, let \(x_1,\ldots,x_R\) be distinct members,
and attach \(d_i\) distinct private new points \(y_{iu}\) to each mark. All
private points are outside \(X\) and mutually distinct. The exact downset is

\[
\mathcal F=2^X\cup\{\{y_{iu}\},\{x_i,y_{iu}\}:1\le i\le R,1\le u\le d_i\}.
\]

The reviewed NEW branch assumes integers \(n\ge R\ge4\), every \(d_i\ge1\),
and at least three distinct load values. Set

\[
q=2^{n-1},\quad D=\max_i d_i,\quad k=\#\{i:d_i=D\},\quad
m=\sum_i d_i,\quad S=m-D,\quad N=2q+2m,
\]
\[
s=q+D,\quad w=s-1,\quad h=N-1,\quad P_N=I-J/N.
\]

There is an explicit rational symmetric matrix \(M\), indexed by **all** sets
including the actual empty set and its allowed loop, satisfying

\[
M\mathbf1=\mathbf1,\quad M_{AB}=0\text{ if }A\cap B\ne\varnothing,
\quad L=(N-s)M+sI\succeq0,
\]
\[
(N-s)(I-M)\succeq\tfrac12P_N,\quad
\operatorname{rank}L=N-k,\quad\operatorname{rank}(I-M)=N-1.
\]

The lower rank is greatest among **all real H matrices** on this same downset,
without an upper cap, rationality or mark-permutation symmetry assumption on
competitors. The negative endpoint has multiplicity exactly \(k\), eigenvalue
one is simple, and precisely the \(k\) heavy marked stars are maximum families.
Signed disjoint entries are permitted. Distinct marks, distinct private points,
and this exact cube-plus-singleton-and-spoke domain are essential inputs.

The new hypotheses imply \(q>R,q\ge8,D\ge3,m\ge7,S\ge4,w\ge10\).
After removing a largest load, the remaining loads include at least \(2,1,1\).
The target already states that these numerical premises suffice for its
constructor; removing the three-value wording under these premises would not
be a new strengthening of its published scope.

The target's all-positive-profile corollary for \(2\le R\le n\) has the
following complete partition. Equal load one uses8863; equal load at least two
uses8895. Two unequal marks use9005. Two load values with one heavy mark and at
least two lighter marks use9100; with at least two heavy marks use9153. Three
marks with three distinct values use9229. Every remaining profile belongs to
the new branch. I checked these quantified statements and the coverage
partition. The all-profile corollary is **conditional on those six prior
results**: their complete unbounded proofs and native engines are not all
reaudited here. REVIEW8927 confirms8863, REVIEW9049 confirms9005, and
REVIEW9265 confirms only9153's new repeated-heavy scope. None transfers an
independent verdict to8895,9100,9229 or9305. Products, single-mark and zero-load
profiles, other outer facets, general H and inertia conjecture I are outside
this assessment.

## Definition-derived Gram construction

The old nonempty cube has \(2q-1\) vectors with Gram

\[
C_D=(q+D)I+(q-D)P-J,
\]

where \(P\) pairs proper nonempty complements and vanishes on the full-set
row. Its complementary symmetric pair-difference space has eigenvalue \(2q\)
and dimension \(q-2\); its antisymmetric complement space has eigenvalue
\(2D\) and dimension \(q-1\). The remaining plane has positive trace
\(q+D+1\) and determinant \(2D\). Thus the old Gram is positive definite,
including when \(D>q\).

Write \(G\) for the old-vector sum, \(f\) for the full-set vector, and
\(H_i\) for minus the old \(x_i\)-star sum. Direct complement counts give

\[
G^2=f^2=w,\ G\cdot f=D+1-q,\ G\cdot H_i=f\cdot H_i=-D,
\quad H_i\cdot H_j=qD\delta_{ij}.
\]

Spokes have \(V_{iu}=H_i/D+T_{iu}\), with new orthogonal residual blocks
\((q+D)(I-J/D)\) of order \(d_i\). These have rank \(d_i-1\) at heavy
marks and \(d_i\) otherwise. At the original indices, a spoke has product
\(-1\) with an old set containing its mark, \(+1\) with an old set avoiding
it, \(-1\) with another spoke at its mark, and zero with a spoke at a
different mark. All norms are \(w\).

Let \(L_i=d_i^{-1}\sum_uV_{iu}\), \(K=G+\sum_i d_iL_i\), and

\[
c_i=\frac{m(w-d_i-m-1)}{(m+1)((m-1)w-1+d_i)},\qquad
C_* =\sum_i d_i c_iL_i.
\]

The exact scalar identities are

\[
B_0=K^2=w+m(q+D)-\sum_i d_i^2-2m,\quad
C_2=C_*^2=\sum_i d_i c_i^2(q+D-d_i),
\]
\[
K\cdot C_*=\sum_i d_i c_i(w-d_i)=K_C.
\]

Define

\[
\eta_i=w-\frac{B_0}{(m+1)^2}-c_i^2w+rac{2c_i^2(q+D-d_i)}m
-rac{C_2}{m^2}+rac{2c_i(w-d_i)}{m+1}-rac{2K_C}{m(m+1)},
\]
\[
E=\sum_i d_i\eta_i,\qquad
\zeta_i=\frac m{m-2}\left(\eta_i-\frac E{m(m-1)}\right).
\]

Introduce residual vectors \(W_{iu}\), orthogonal to old/spoke vectors, with
Gram \(P_m\operatorname{diag}(\zeta_i\text{ repeated }d_i)P_m\).
It has diagonal \(\eta_i\), sum zero and rank \(m-1\) once \(\zeta_i>0\).
The singleton vectors

\[
U_{iu}=-K/(m+1)+c_iV_{iu}-C_*/m+W_{iu}
\]

have norm \(w\) and product \(-1\) with their own spoke. No other off-diagonal
singleton intersection requires a constraint. Their total sum is
\(-mK/(m+1)\), so the actual empty vector is \(-K/(m+1)\). This is a literal
centered Gram lift, not deletion of the empty coordinate.

The full nonempty seed spans the old/spoke vectors and every residual
\(W\)-direction. Its exact rank is
\((2q-1)+(m-k)+(m-1)=N-k-2\). All Gram products are rational even though
an abstract Euclidean realization might use irrational coordinates.

## Uniform estimates and exact mean resolvent

For every real \(1\le d\le D\), the denominator defining \(c(d)\) is
positive and

\[
|c(d)|<C=\max\{1/(m-1),1/w\}\le1/6.
\]

When its numerator is positive, discard unfavorable terms against
\((m+1)(m-1)w\). When negative, use \(d\le D\le w-3\), so
\(m+d+1-w\le m-2\), and \(m(m-2)<(m+1)(m-1)\).
Furthermore

\[
0<B_0=w+m(q-2)+\sum_i d_i(D-d_i)<(m+1)w,
\quad C_2\le C^2m(w+1),\quad |K_C|\le Cmw.
\]

The upper \(B_0\) difference is \(m+\sum_i d_i^2\). Bounding the signed
terms in \(\eta_i\) in both directions, with \(m\ge7,w\ge10\), gives

\[
(319/420)w<\eta_i<(344/315)w,
\qquad (3/4)w<\zeta_i<(7/5)w.
\]

For the last substitution the lower excess has numerator \(4m-15\); the
upper comparison numerator is \(6m^2-47m+56=(m-7)(6m-5)+21>0\), over
positive denominators. These are estimates for all parameters, not positive
signs inferred from samples. Since \(h-2(q+D)=2S-1>0\), putting
\(g=(q+D)/h\) gives \(g<1/2\). The within-mark two-component deviation
budget obeys

\[
1-\zeta_i/h-c_i^2g/(1-g)>49/180.
\tag{1}
\]

For the means, set \(h_0=-(G+f)/2\), \(G_+=G+h_0\),
\(A_i=H_i-h_0\). The plane is orthogonal with squared norms \(q-1,D\),
and \(A_i\cdot A_j=D(q\delta_{ij}-1)\). At nonheavy marks add independent
\(Z_i=L_i-H_i/D\) with squared norm \((q+D)(1/d_i-1/D)\). These are a
basis of the old/spoke mean space of dimension \(2R-k+2\); \(q>R\)
makes the marked metric positive definite.

The old frame \(F_0\) has plane action
\(\left(\begin{smallmatrix}q+1&D\\q-1&D\end{smallmatrix}\right)\), action
\(2D\) on the \(A_i\), and zero on the \(Z_i\). Its physical resolvent
is well-defined since the old plane trace and \(2D\) are below \(h\).
Define

\[
\Delta=(h-q-1)(h-D)-D(q-1),\quad
\rho=(2m-1)/\Delta,\quad
\kappa=\rho/(h-2D),\quad \theta=(2S-1)/[h(h-2D)],
\]
\[
R_{gg}=[hw-2D(2q-1)]/\Delta,\quad
\gamma_i=g-d_i\theta,\quad b_i=1-\gamma_i.
\]

Inverting the actual plane and using the marked/residual metrics gives
all entries of \(\mathcal R(a,b)=\langle a,(hI-F_0)^{-1}b\rangle\):

\[
\mathcal R(G,G)=R_{gg},\quad \mathcal R(G,L_i)=-\rho,\quad
\mathcal R(L_i,L_j)=\delta_{ij}\gamma_i/d_i-\kappa.
\tag{2}
\]

The common term identity is
\((h-q-1)/(D\Delta)-1/[D(h-2D)]=-\kappa\).
The bounds are \(\Delta>hw>2m-1\), \(0<\rho,R_{gg}<1\), and
\(0<\gamma_i<g<1/2\). Set

\[
H=\sum_i d_i/b_i,\quad T=1+\kappa H,\quad
\lambda=(1-\rho)/T,\quad \nu_i=-1+\lambda/b_i,
\]
\[
K_{\rm gap}=2m+1-R_{gg}-H(1-\rho)^2/T.
\]

The spoke-mean update budget is
\(\operatorname{diag}(b_i/d_i)+\kappa\mathbf1\mathbf1^T\).
Its inverse is diagonal minus a rank-one matrix. The updated \(K\) norm is
\(R_{gg}-m+H(1-\rho)^2/T\), and its updated cross products with \(L_i\)
are \(\nu_i\). This proves the common \(KK^*/(m+1)\) update has slack
\(K_{\rm gap}\), with

\[
K_{\rm gap}>2m-H>\frac{m(2S-1)}{w+2S}>0.
\tag{3}
\]

After both updates, every marked covariance is

\[
\Gamma_{ij}=\delta_{ij}\frac{\gamma_i}{d_i b_i}
-\frac{\kappa}{Tb_i b_j}+\frac{\nu_i\nu_j}{K_{\rm gap}}.
\tag{4}
\]

This follows also by writing the initial \(L\) covariance as
\(\operatorname{diag}(1/d_i)-A\) and expanding its Woodbury update; it
is an actual physical inverse identity, not a guessed table of load types.
The independent finite checker inverts \(h\cdot\mathrm{Gram}-\mathrm{frame}\)
in the actual original-coordinate basis and checks all entries of (2), all
updated \(K\) cross products, (3)'s exact slack and all entries of (4).

## Stronger dimension-free balanced mean estimate

Let \(W_i=d_i^{-1}\sum_u W_{iu}\) and
\(\sigma_i=c_iL_i-C_*/m+W_i\). Their weighted sums vanish. The last mean
frame is \(\sum_i d_i\sigma_i\sigma_i^*\). Use the input norm
\(\|x\|_d^2=\sum_i d_i x_i^2\) on \(\sum_i d_i x_i=0\). The constant
input maps to zero. Its exact Schur budget is

\[
\mathcal B(x)=\sum_i d_i(1-\zeta_i/h)x_i^2
-\sum_{i,j}d_i d_jc_i c_j\Gamma_{ij}x_i x_j.
\]

Dropping only the negative rank-one covariance term in (4) gives

\[
\mathcal B(x)\ge\sum_i d_i[1-\zeta_i/h-c_i^2\gamma_i/b_i]x_i^2
-\frac{(\sum_i d_i c_i\nu_i x_i)^2}{K_{\rm gap}}.
\tag{5}
\]

Its diagonal is strictly greater than49/180 by (1). Hold the actual
profile's \(q,m,D,H,\lambda\) fixed when extending \(d\) to \([1,D]\).
Then \(b(d)=1-g+d\theta\), \(-1<\nu(d)<1\), and

\[
|c'(d)|=\frac{m(mw-m-2)}{(m+1)((m-1)w-1+d)^2}
<\frac1{(m-2)w},\qquad |\nu'(d)|<4\theta.
\]

The derivative inequality uses
\((m+1)(m-1)^2-m^2(m-2)=m^2-m+1>0\).
Thus the oscillation of \(c(d)\nu(d)\) is less than
\(D/[(m-2)w]+4CD\theta\).

**Retain the stronger information \(D=m-S\le m-4\).** The first term
is less than \(1/w\). If \(C=1/w\), \(D\theta<g<1/2\) bounds the
second term by \(2/w\). If \(C=1/(m-1)\), write it as

\[
\frac4w\frac D{m-1}\frac{2S-1}{h-2D}\frac wh<\frac2w.
\]

Here each of the first two ratios is strictly below one and \(w/h<1/2\).
Both cases yield

\[
\operatorname{osc}_{[1,D]}(c(d)\nu(d))<3/w.
\tag{6}
\]

For numbers in an interval \([a,b]\), averaging
\((f-a)(b-f)\ge0\) bounds their weighted variance by
\((\overline f-a)(b-\overline f)\le(b-a)^2/4\).
Weighted Cauchy--Schwarz and the balanced constraint therefore bound the
normalized last term of (5), using (3) and (6), by

\[
\frac{m\operatorname{osc}(f)^2}{4K_{\rm gap}}
<\frac{9(w+2S)}{4(2S-1)w^2}
\le\frac{9(w+8)}{28w^2}\le\frac{81}{1400}.
\tag{7}
\]

The first weak comparison is monotone in \(S\ge4\); the last follows
from \(9(w-10)(9w+40)\ge0\), after multiplication by a positive
denominator. Combining (5)--(7) proves, for every nonzero balanced input,

\[
\boxed{\mathcal B(x)>\frac{2701}{12600}\|x\|_d^2>\frac15\|x\|_d^2.}
\tag{8}
\]

A useful profile-dependent sufficient margin is
\(49/180-9(w+2S)/[4(2S-1)w^2]\), at least2701/12600. The strict
inequality is for nonzero inputs; the zero input has equality zero.
This statement does not identify the optimal budget or imply the same
constant in the physical output metric.

## Physical completeness, repair and all-real rank obstruction

The mean space has dimension \(3R-k+1\): the plane, \(R\) marked old
contrasts, \(R-k\) nonheavy spoke means and \(R-1\) residual means.
Within each mark there are \(d_i-1\) spoke and \(d_i-1\) residual singleton
deviations. They are independent of the means: averages and zero-sum
contrasts are Gram-orthogonal, the \(T\) blocks are mark-separated, and the
centered residual Gram becomes diagonal on every globally balanced input.
They have norms \(q+D\) and \(\zeta_i\) per unit contrast; their frame is
formed by \(V\) and \(c_iV+W\). Its two-component Schur slack is exactly
(1). Distinct-mark deviation sectors are also frame-orthogonal.

The untouched old high space has dimension \(q-2\) and frame eigenvalue
\(2q\). The old low space orthogonal to all \(R\) marked contrasts has
dimension \(q-R-1\) and eigenvalue \(2D\). They are orthogonal to
\(G,f,H_i\), hence to all new outputs. The actual empty vector belongs
to the mean space. Every cross-frame term between the stated sectors
vanishes. The dimension census is

\[
(3R-k+1)+2(m-R)+(q-2)+(q-R-1)=N-k-2,
\]

exactly the seed Gram rank. No positive physical direction remains untested.
The whole seed frame is strictly below \(hI\), using (1), (8), and the
untouched eigenvalues. Equality of nonzero Gram/frame spectra and centering
therefore give \(Q_{\rm seed}\preceq hP_N\) and
\(NP_N-Q_{\rm seed}\succeq P_N\).

For rank repair, use singleton \(-V_{iu}/w+E_{iu}\), with independent
orthogonal \(E_{iu}\) of squared norm \(w-1/w>0\). The raw nonempty core
has rank \((2q-1)+(m-k)+m=N-k-1\). Its only core kernels are the \(k\)
heavy-star indicators, from the saturated heavy residual blocks. Both seed
and raw vanish on these stars. Center the raw matrix with its actual empty
row; its trace is

\[
T_{\rm raw}=(N-1)w+w+(1-1/w)^2[m(q+D)-\sum_i d_i^2]
-2m(1-1/w)+m(w-1/w).
\]

Take \(\epsilon=1/[2(1+T_{\rm raw})]\) and
\(Q=(1-\epsilon)Q_{\rm seed}+\epsilon Q_{\rm raw}\).
For PSD matrices, the kernel of a positive mixture is the intersection of
the kernels. The raw centered kernel is the constant vector plus heavy
star directions, so \(\operatorname{rank}Q=N-k-1\). Defining
\(M=(Q+J-sI)/(N-s)\) gives all stated matrix equations. Moreover

\[
(N-s)(I-M)\succeq
\left[\frac12+\frac N{2(T_{\rm raw}+1)}\right]P_N\succeq\tfrac12P_N.
\]

This sharper trace expression is **already credited in9305 to prior
reviews8927/9049/9265**; it is verified here, not claimed as a new result.
It makes the unit eigenvalue simple. Adding \(J\) raises the centered
Gram rank by one, giving lower rank \(N-k\) and negative endpoint
multiplicity exactly \(k\).

An intersecting family containing a private singleton has size at most two.
If it contains a spoke, all old sets contain that mark and all its other
spokes must be at the same mark. Its size is at most \(q+d_i\), with
equality only for the full star. Cube-only families have size at most \(q\)
by complementary pairing. Thus the heavy stars are precisely the maximum
families of size \(s\).

For **any** real H matrix on this domain, a heavy-star centered indicator
\(z=\mathbf1_A-(s/N)\mathbf1\) obeys \(z^TLz=0\), because its intersecting
block of \(M\) is zero and \(L\mathbf1=N\mathbf1\). PSD forces \(Lz=0\).
These \(k\) vectors are independent: a relation evaluated at any private
singleton forces the sum of coefficients zero; evaluating at each old heavy
singleton then forces its individual coefficient zero. Therefore every H
matrix has lower rank at most \(N-k\), without the construction's extra
cap or symmetries. The rational witness attains this universal ceiling.

## Independent evidence and trust boundaries

[check.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/arbitrary-profile-audit/check.py),
[literal.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/arbitrary-profile-audit/literal.py)
and [scalars.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/arbitrary-profile-audit/scalars.py)
import no researcher executable. The defining mathematical proof and formulas
were visible and credited; this is not a blind construction discovery. All
first independent normal matrices/budgets and five engine-file hashes were
frozen before any target executable or RESULTS.json was inspected. The
complete first six mathematical records have SHA256
**ad9ed502b65ab4d0c45ed4321531281aa24c1d939d56339a3e917147dfd6e2c0**.
Complete normal and optimized external records and stdout agree. The original
five engine files remain unchanged after that freeze.

The exact linear engine uses reviewer-authored Fraction Schur congruence with
largest-diagonal pivots, reused from own source77e859b56ee1808932766c83bb6e428cb6ac0415;
its earlier729 symmetric ternary3-by-3 principal-minor checks are provenance,
not re-counted as new pass19 tests. New physical inverses are checked against
actual Gram/frame products; separate ternary2-by-2 inverse multiplication
controls and twelve semantic domain/PSD/inverse rejections pass in normal/O.

Five full fixtures use loads/marks
\((1,3,2,1)/(3,1,0,2)\), \((9,3,2,1)/(0,3,1,2)\),
\((5,5,3,2,1)/(4,0,3,1,2)\), \((3,3,3,2,1)/(2,4,0,3,1)\), and
\((3,2,1,1)/(5,0,3,1)\). They have \(N=30,46,64,56,78\), respectively,
and cover load one, \(D>q\), one/two/three heavy marks and relocated old
coordinates. Old sets are enumerated by combinations in reverse order;
private singletons and spokes are appended separately. Original set
uniqueness, downset deletion closure and actual star sizes are checked.

All16,332 ordered positions of each full seed/raw/repaired matrix participate
in the construction and whole matrix equation checks. The actual empty loop,
all rows, all mandatory support entries, both heavy-star kernels, centered
star independence, exact ranks, strict seed gap and the sharper trace-repair
gap pass. Every tested mean frame entry is compared with the original
old/spoke/common/singleton sum, including the actual empty vector. The exact
original physical inverse agrees on every initial and doubly updated marked
covariance and every common-update cross product/slack. Internal independence,
all internal-mean Gram/frame cross products, untouched-space projected bases,
eigenactions/cross products and full dimension counts are checked. These are
not counts of distinct theorems or an enumeration of all downsets.

Nine separate scalar profiles include20marks, twelve distinct values and
\(q=2^{100}\) without constructing a cube. Some scalar controls do not have
\(n\ge R\); they test rational identities only. Every balanced budget is
checked against2701/12600 in its weighted metric, not against an incorrectly
assumed Euclidean metric. Ten whole-matrix semantic intersection/empty-loop
corruptions are rejected in the five fixtures, in addition to the twelve
separate controls. Exceptions remain active under Python -O.

Late [compare_author.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/arbitrary-profile-audit/compare_author.py)
is explicitly separated from the first independent audit. It checks every
shared53 scalar-record field from own reconstructed budgets; determinant
ratios independently reproduce the author's fixed-order pivot hashes.
For the five frozen full cases it imports the byte-pinned author **build**
only for corroboration, transports all actual old/private coordinates and
set order, and compares entire seed/raw/repaired matrices by their already
frozen exact hashes. This imported comparison is not called independent
arithmetic. The independent literal engine imports no author module.
Separate native original normal/O bounds and full-frame records are also
checked against the pinned original fixture, retaining original60-second
internal and our90-second outer guards. Final hashes, resources and source
integrity are recorded in VALIDATION.json and AUTHOR-INPUTS.json.

Trust remains in the ordinary complementary decomposition, full-span and
Schur/variance/rank/relabelling arguments, exact-arithmetic implementation,
CPython3.12.14 and its standard library. No formal proof assistant, floating
point, solver, external proof corpus or unbounded enumeration is used.
Source publication supplies reproducibility, not an independent proof of
the theorem by itself.

## Strengthening and improvement opportunities

**Proved:** the range estimate (6), stronger normalized margin (8), and the
profile-dependent lower margin in (7). The same matrix constructor is used;
the gain comes from retaining \(S\ge4\) in the derivative estimate. It
improves this particular sufficient estimate, with no optimality or exclusive
historical-priority claim.

**Already prior:** the numerical sufficient premises listed by the target,
the sharper raw-trace expression and special-case all-profile coverage.
They are not renamed as discoveries in this review.

**Next useful lemma:** turn the normalized balanced margin into a uniform
quantitative physical output-frame gap. This requires controlled bounds on
the complete block congruence/inverse, including old plane, spoke and common
updates, and an explicit relationship between weighted input and output
metrics. Quoting1/5 as a whole spectral gap would bypass this missing step.
A justified sharper raw spectral bound could then permit a larger repair
weight. Neither follows merely from the present trace bound.

**Scope extensions remain research:** dropping \(S\ge4\) or \(q>R\)
needs replacement variance and degeneracy analysis; allowing reused marks,
nonprivate points or larger facets changes the intersecting support and
requires a new original Gram constructor and complete frame census. General
H and I remain distinct tasks. Formalizing the lift, forced-star ceiling and
weighted Schur bridge is feasible and would reduce the ordinary trust.

## Literature, attribution and publication readiness

[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4)
provides the signed weighted Hoffman conventions, friendly empty vertex and
separate H/I conjectures. Its [version record](https://arxiv.org/abs/2609.28404)
was checked live2026-10-02 and still lists v1 of2026-09-23. The paper presents
a proof of classical Chvatal and leaves H/I open. This restricted pendant
class is not a solution of either general spectral conjecture. Targeted
primary searches for arbitrary/pendant/Hoffman downsets yielded no exact
external match; that limited absence does not establish priority.

Campaign credit belongs to7578 for the lift and prior constructors8863,
8895,9005,9100,9153,9229; the target9305 supplies the new arbitrary-profile
analytic argument. Prior scoped reviews8927/9049/9265 are credited for their
actual scopes and trace-repair context. The independent evidence and sharper
sufficient mean estimate here support a confirming review, not first
authorship of9305. The result is ready for ordinary mathematical scrutiny
with the stated unformalized bridges and reproducible compact source.
