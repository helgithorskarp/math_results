# An effective five-level angular stability collar

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Complete ordinary author proof with finite exact certificates, unformalized;
no independent verdict on this contribution has been adopted.

The new result is an explicit collar in the remaining original multiplicity
type \(3+2+1+1+1\), **retaining the original threefold block and splitting the
fourfold block into2+1+1**, with Euclidean quadratic cost300. The known
three-level optimum and existential full-sphere local stability are credited
to [8753](../angular-three-level-transition/PROOF.md) and
[review8806](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/three-level-angular-audit/REVIEW.md).
The latter proves every coefficient below340.462200 locally, with an
existential radius. Here300 is smaller, but its restricted domain is explicit.
The other32111 coalescence chart, the whole32111 family, unrestricted angular
maximum and complex first-power endpoint remain open.

## 1. Definitions and precise theorem

For balanced norm-one \(\theta\in\mathbb R^8\), let

\[
e=\mathbf1/\sqrt8,\quad P=I-ee^T,\quad
H=P\operatorname{diag}(\theta)P|_{e^\perp},\quad
\rho_\lambda=\|\Pi_\lambda\theta\|^2,\quad
\eta=\sum_{\lambda\text{ distinct}}\rho_\lambda^2,\quad
\mathcal X=\sum\theta_i^4,\qquad
C(\theta)=\frac{1-\eta}{\mathcal X-1/8}.
\]

Each projection is onto a **full eigenspace**. The continuous uniform4+4
extension is16; the domain below is separated from that orbit. This equals
the \(8\|\Pi_\lambda\operatorname{diag}(\theta)e\|^2\) mass convention.
Distance is Euclidean distance on the balanced unit sphere.

Let alpha be the unique root of
\[
4575t^4+11695t^3+11175t^2+4737t+746=0
\]
in \((-853410556973738/10^{15},-853410556973736/10^{15})\), and put
\[
c_3=\frac{8(\alpha-1)^2(5\alpha+3)^2}
{(15\alpha^2+24\alpha+10)(35\alpha^2+38\alpha+11)}.
\]
The inherited theorem gives \(24.53389668<c_3<24.53389670\) and the finite
sign/permutation orbit \(\mathcal O_3\) of the normalization of
\((\alpha^4,1^3,-4\alpha-3)\). Profile exponents denote multiplicities.
Put \(X_*=-5\alpha-3\).

Define
\[
\begin{split}
u(X,U,\epsilon)&=(-5^3,(3+X-U)^2,
3+X+U+\epsilon,3+X+U-\epsilon,3-4X),\\
W&=4U^2+2\epsilon^2,\quad N=120+20X^2+W,\quad\theta=u/\sqrt N,\\
C_0(X)&=\frac{8X^2(X+8)^2}{21X^4-30X^3+23X^2-4X+20}.
\end{split}
\]

**Theorem.** Suppose \(5/4\le X\le13/10\), and either
\[
\boxed{0\le U\le1/4,\quad|\epsilon|\le1/4}
\quad\text{or}\quad
\boxed{-1/16\le U\le0,\quad|\epsilon|\le1/16}.             \tag{1}
\]
Then, including every collision in the closed boxes,
\[
\boxed{C(\theta)\le C_0(X)-2W
\le c_3-32(X-X_*)^2-2W},                                \tag{2}
\]
and
\[
\boxed{C(\theta)\le c_3-300\operatorname{dist}
(\theta,\mathcal O_3)^2}.                               \tag{3}
\]
All permutations and sign changes obey the same conclusions.
Equality \(C=c_3\) requires \(X=X_*,U=\epsilon=0\), giving the corresponding
members of \(\mathcal O_3\). Genuine five-level points in the domain are
strict. The union contains the symmetric collar
\(|U|,|\epsilon|\le1/16\) and extends the positiveU side further.

This restricted angular chart does not give an effective full-sphere ball
or the other32111 coalescence chart: fourfold3+1 and threefold2+1 simultaneous
splitting. No bound outside(1) is claimed.

## 2. Original derivative and exact fourth-moment correction

Use the generic chart
\[
u=(-5^3,(3+x)^2,3+y,3+z,3+w),\quad y+z+w=-2x,\quad
q=yz+yw+zw,\quad r=yzw.
\]
Let \(c(t)=t^3+2xt^2+qt-r\), \(L(z)=z-3-x\), \(K(z)=c(z-3)\). Then
\[
f(z)=(z+5)^3L(z)^2K(z),\qquad
f'(z)/8=(z+5)^2L(z)h(z),
\]
where
\[
h(z)=\frac{(5z+1-3x)K(z)+(z+5)L(z)K'(z)}8.               \tag{4}
\]
It is monic quartic with cubic coefficient \(x-7\). The checker expands
the original derivative, verifies(4) in \(\mathbb Q[x,q,r,z]\), and derives
all moments by the Newton recurrence. No fitted active polynomial is used.

Write \(S_j=\sum u_i^j,N=S_2\). Raw coupling moments are
\[
\mu_0=N,\quad\mu_1=S_3,\quad
\mu_2=m_2=S_4-N^2/8,\quad\mu_3=m_3=S_5-NS_3/4.           \tag{5}
\]
Indeed \(H_uu=(u_i^2-N/8)_i\), where
\(H_u=P\operatorname{diag}(u)P|_{e^\perp}\); its norm and next quadratic
form give(5). The characteristic polynomial is \(f'/8\).
Original-level eigenspaces have zero coupling, so all coupled eigenvalues
are among the roots of \(h\).

For four distinct roots \(\lambda_j\) of \(h\), include zero masses at
inactive roots and set \(r_j=\|\Pi_{\lambda_j}u\|^2\). Then
\[
\sum r_j=N,\qquad\sum\lambda_j^i r_j=\mu_i,\qquad
C=\frac{N^2-\sum r_j^2}{m_2}.                           \tag{6}
\]
Let \(p_i=\sum\lambda_j^i,p_0=4\), and
\(G_k=(p_{i+j})_{0\le i,j<k}\). The four-point Vandermonde matrix gives
\(G_4=VV^T,\mu=Vr\); hence
\[
\sum r_j^2=\mu^TG_4^{-1}\mu,\qquad
C=\frac{N^2\det G_4-\mu^T\operatorname{adj}(G_4)\mu}
{m_2\det G_4}.                                        \tag{7}
\]
A **positive common normalization** gives integer polynomials \(n_4,d_4\)
with168 and183 terms. The checker verifies all16 entries of the adjugate
identity as whole polynomial identities.

Set
\[
\nu=(N,S_3,m_2)^T,\quad v=(p_3,p_4,p_5)^T,\quad D_k=\det G_k,
\]
\[
R_3=\frac{N^2D_3-\nu^T\operatorname{adj}(G_3)\nu}{m_2D_3},
\qquad z=m_3D_3-v^T\operatorname{adj}(G_3)\nu.
\]
The complete fourth-moment Schur identity is
\[
\boxed{C=R_3-\frac{z^2}{m_2D_3D_4}}.                   \tag{8}
\]
The checker proves \(D_4=p_6D_3-v^T\operatorname{adj}(G_3)v\), compares
the24-permutation determinant, and cross-multiplies all of(8).
Schur complements and Vandermonde interpolation are classical. Their
use to obtain this explicit collar and expose the proposedR3-only
strategy is the deliverable here.

## 3. Complete positivity certificates

The cluster coordinates are the exact substitution
\[
x=X-U,\quad V=\epsilon^2,\quad
q=(X+U)^2-V-8X(X+U),\quad r=-4X((X+U)^2-V).             \tag{9}
\]
The entire Fraction substitution was compared with a separate SymPy1.14.0
expansion during discovery. The final checker rederives it from(4), without
a runtime CAS. It proves \(N=120+20X^2+W\). Substituted \(n_4,d_4\) have435
and467 terms.

Put \(n_b=8X^2(X+8)^2,d_b=21X^4-30X^3+23X^2-4X+20\) and define
\[
F=n_bd_4-d_bn_4-2(4U^2+2V)d_bd_4.                      \tag{10}
\]
Here \(n_4,d_4\) mean their complete substitutions(9). Positive primitive
scaling gives949 terms and multidegrees(18,18,8). The minimum weighted order
is4, assigning weight1 toU and2 toV.

Expand \(F(X,U,V)\) in the full tensor Bernstein basis on
\([5/4,13/10]\times[0,1/4]\times[0,1/16]\).
Expand \(F(X,-U,V)\) on
\([5/4,13/10]\times[0,1/16]\times[0,1/256]\).
Each has exactly3249 coefficients: **3135 positive and114 zero**.
There are no negative coefficients, omitted indices or subdivisions.
The minimum positive coefficients are, respectively,
\[
\frac{367312711002341796875}{112150186033152},\qquad
\frac{367312711002341796875}{28710447624486912}.
\]
The canonical full coefficient-list SHA256 values are:

    positiveU 79076f841a81e021f9cee6e48a0bb1f56cf7552882a19044c4ced0ce9e355cc3
    negativeU 4072b7facda73b2e43d6fa0f8327a42e2c5251953ab437d31e5c73759a3fd962

Signs are computed before hashing. Separate Bernstein-to-power transport
reconstructs each entire affine-transformed polynomial, without reusing
the forward matrices. A smaller dense expansion checks the tensor algorithm.
Bernstein basis functions are nonnegative, proving \(F\ge0\) on both
complete boxes. The physical denominators in Section4 then give the first
bound in(2).

For the branch, \(g=n_b'd_b-n_bd_b'\) gives
\[
C_0''=(g'd_b-2gd_b')/d_b^3.
\]
The primitive polynomial \(-(g'd_b-2gd_b')-64d_b^3\) has13 positive
degree12 Bernstein coefficients on \([5/4,13/10]\), minimum
\(2088714504458553/250000000000\). The denominator \(d_b\) has5 positive
coefficients, minimum11165/256. Whole basis reconstructions establish
\(d_b>0,C_0''\le-64\) throughout the interval.

The checker verifies the entire pullback of the inherited431 curve under
\(\alpha=-(X+3)/5\). Thus
\[
C_0(X)=C((-5^3,(3+X)^4,3-4X)/\sqrt{N_0}),\qquad
N_0=120+20X^2,\qquad C_0(X_*)=c_3.
\]
It also verifies
\[
g=-16X(X+8)(183X^4-143X^3+6X^2-24X-160)
\]
and isolates \(X_*\in(1267/1000,1268/1000)\). The quartic is exactly
the alpha polynomial after substitution and positive scaling, so
\(C_0'(X_*)=0\). Twice integrating \(C_0''\le-64\) proves
\(c_3-C_0(X)\ge32(X-X_*)^2\), finishing(2).

## 4. Positive denominators and all collisions

Both boxes keep the four upper entries in[15/4,24/5], the singleton
3-4X in[-11/5,-2] and the triple at-5. These three clusters are separated.
Balance is exact and \(N\ge605/4>0\). Also \(m_2>0\): equality in
\(S_4\ge N^2/8\) requires equal squared coordinates, contradicted by the
two separated negative magnitudes5 and[2,11/5]. We already proved \(d_b>0\).

If \((U,\epsilon)\ne(0,0)\), the upper cluster has three distinct values
with multiplicities2+1+1, or two distinct values with multiplicities2+2
or3+1. For original levels \(r_i\) with multiplicities \(m_i\), the
secular equation \(\sum m_i/(z-r_i)=0\) gives precisely one simple root
in every open gap. Other derivative roots are original levels, with
multiplicity \(m_i-1\), and zero coupling.

In the three-upper-level case, \(h\) has the four simple gap roots.
At2+2 collision it has three gap roots and the unremoved inactive
double-block level. At3+1 collision it has three gap roots and the
inactive triple-block level remaining after factorL. These four roots
are distinct in every case. Therefore \(G_4,G_3\) are positive definite,
\(D_4,D_3,d_4>0\), and(7)--(10) apply with zero inactive mass.

Only \(U=\epsilon=0\) gives a fourfold upper level. Now \(h\) has a double
inactive labeled root and \(D_4=0\); formula(7) is not used. This is the
actual431 profile, with \(C=C_0(X)\), which directly gives(2).
The checker verifies the entire collision ratio by exact deflation on
a symmetric splitting path and by a full8 commutant control at a base point.
No division by a zero discriminant establishes a collision case.
Inherited collision continuity agrees with this direct treatment.

## 5. Transfer to unit-sphere Euclidean distance

Write \(u=u_0(X)+\delta\), \(u_0=(-5^3,(3+X)^4,3-4X)\), with four
deviations \((-U,-U,U+\epsilon,U-\epsilon)\). Their sum is zero, so delta
is orthogonal to every branch vector \(u_0(Y)\). Thus
\[
\|\delta\|^2=W,\quad N_0=120+20X^2,\quad N=N_0+W.
\]
Let \(b(X)=u_0(X)/\sqrt{N_0(X)}\) and choose
\(\theta_*=b(X_*)\in\mathcal O_3\) with the same block ordering. The exact
derivative metric is
\[
\|b'(X)\|^2=2400/N_0(X)^2\le L=1536/14641.
\]
The fundamental theorem of calculus gives
\(\|b(X)-b(X_*)\|^2\le L(X-X_*)^2\). With \(v=W/N\),
\[
\|\theta-\theta_*\|^2
=2(1-\sqrt{1-v})+\sqrt{1-v}\|b(X)-b(X_*)\|^2.           \tag{11}
\]
Here \(W\le3/8,N\ge605/4\), so \(v\le3/1210\) and
\(1-v>(119/121)^2\). Consequently
\[
2(1-\sqrt{1-v})=\frac{2v}{1+\sqrt{1-v}}\le\frac{121}{120}v.
\]
The exact comparisons
\[
300(121/120)=605/2\le2N,\qquad
32-300L=7712/14641>0
\]
give, using(2),(11),
\[
300\|\theta-\theta_*\|^2
\le2W+32(X-X_*)^2\le c_3-C(\theta).
\]
The closest orbit point has no larger distance, proving(3).
The coefficient300 is in the unit-sphere Euclidean metric, with all
normalization factors retained.

## 6. A realizable obstruction to the R3-only strategy

Set \(x=1267/1000,\epsilon=1/1000,U=0,X=x\). This is the balanced
genuine32111 profile
\[
(-5,-5,-5,4267/1000,4267/1000,1067/250,2133/500,-517/250),
\quad N=76052891/500000,
\]
with \(q=-351157/31250,r=-254237487/31250000\). Its moment upper bound is
\[
R_3=\frac{408443088910088663985994343668603252766}
{16648108970037146461726340177533587875}.
\]
A different full8 symmetric-commutant projection, without the active
quartic or residues, gives
\[
C=\frac{527878513298889937919311013487599765961589319376375178}
{21516297166687196143751337653042672980987036482805633}.
\]
Exact rational comparisons give
\(C<24.53389668<c_3<24.53389670<R_3\). Positive gap fractions are recorded
in [expected.json](expected.json), and(8) exactly matches the omitted term.
Thus universal32111 \(R_3\le c_3\) is impossible. This is an obstruction
to that proposed upper-bound strategy, not to \(C\le c_3\) or first power.
Replacing2 by raw coefficient3 in(2) also fails at this literal point.

## 7. Reproduction and evidence boundary

[verify.py](verify.py), run as in [README.md](README.md), reconstructs34
complete records,6498 collar coefficients,13 curvature and5 denominator
coefficients, four whole basis reconstructions and eight different-route
full8 controls. The latter include genuine5 points, both four-level
collisions and a three-level base. Four mathematical damage controls
reject a missing Schur correction, wrong raw coefficient3, a changed
stationary derivative factor and a corrupted Bernstein constant.
Normal and optimized modes compare every expected-fixture entry.
There is no mathematical floating point, solver, runtime CAS, imported
campaign implementation or large proof corpus.

The ordinary proof uses the spectral theorem, secular/interlacing argument,
Newton/Vandermonde interpretation, Bernstein positivity, calculus and
Euclidean normalization. These written bridges are not proof-assistant
claims. Same-author alternate representations and exact controls remain
distinct from independent review. [LITERATURE.md](LITERATURE.md) credits
all dependencies and describes the prior scope.

Jobs were serial with one native thread and fixed50-second guards.
Wider trial boxes with negative coefficients do not establish nonexistence
or a larger-domain counterexample. The other32111 coalescence chart,
global32111/22211, six-to-eight levels, fullCstar/equality, effective
full-sphere/global stability and actual degree-nine first-power remain open.
