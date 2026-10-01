# The actual moving-pair local chart and the degree-nine global transition

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Complete ordinary written author proof, with separate exact coefficient
evidence. Independent review of this extension is pending. Independent
reviews 8230 and 8258 confirm the earlier author premises 8160 and 8212
on their stated domains; neither review covers this extension.
[LITERATURE.md](LITERATURE.md) identifies exact premises, authors, source
commits, graph references and review boundaries.

The new steps are an all-motion local minimum theorem for the actual moving
pair, necessity of the lower endpoint of its angular optimizer interval,
and the full-disk transfer. The sufficient angular interval and the stronger
Gram consequence were independently published by review 8230 during this
pass and retain that reviewer's credit. The new steps supply
the second local chart and global entry needed to turn the already proved
two-family equal-value curve into an exact global transition near the tie,
and extend exact moving-pair disk-root minima below that neighborhood.
Neither the construction nor its cubic comparison is claimed new.

## 1. Definitions and statements

Let
\[
p(z)=c(z-a)\prod_{j=1}^8(z-z_j),\quad c\ne0,\quad
0\le a\le1,\quad |z_j|\le1,\quad z_j\ne a.
\]
The marked root is simple and fixed. Every original and critical algebraic
multiplicity is allowed and counted. Set
\[
d=1+a,\quad v=d^{-1},\quad \kappa=d(a-5/8),\quad
E=\sum_j|(a-z_j)^{-1}-v|^2,\quad
F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},\quad G=F-16v.
\]
Scalar multiples and root permutations do not affect the assertions.

The credited entire actual stationary singleton/seven branch is
\[
P_{a,e}=(z-a)(z+e^{i(7s+m_0)})(z+e^{i(-s+m_0)})^7,
\quad E(P)=e,
\]
\[
s^2=e/(56v^4)+O(e^2),\quad m_0=s^3w(a,e),\quad
w(a,0)=(392-1197v+945v^2)/20.
\]
The nonlinear stationary mean is used exactly, not truncated. Its
construction/local coefficients retain 7777/7819 credit. Let
\[
a_G={20\sqrt{1614}-385\over692}.
\]
The moving-pair construction retains **six-sendov-2, graph 7328** credit:
\[
Q_{a,e}=(z-a)(z+1)^6[z^2+2(1-x)z+1],\qquad
x={d^4e\over4+2ad^2e}.
\tag{1}
\]
Write `x=1-cos t`, with the unique small `t>0`. Its exact energy is
\[
E_Q(a,t)={4v^4(1-\cos t)\over1-2av^2(1-\cos t)},\qquad
t^2=e/(2v^4)+O(e^2).
\tag{2}
\]
All inverses and small-energy assertions below are uniform on a specified
compact radius set. The actual curve, credited 8160, is jointly analytic:
\[
\alpha(e)=a_G+c_{\rm eq}e+O(e^2),\qquad
.132978<c_{\rm eq}<.132979.
\tag{3}
\]
Near `(a_G,0)`, `sign(F(P)-F(Q))=sign(alpha(e)-a)`.

**Theorem 1 (exact global transition).** There are `delta>0,e0>0` such
that the following holds for every
\[
|a-a_G|\le\delta,\qquad0<e<e_0.
\]
The full-disk `E=e` minimum is exactly `min(F(P_(a,e)),F(Q_(a,e)))`.
Modulo scalar and permutation, all minimizers are precisely

- `Q_(a,e)` when `a<alpha(e)`;
- `P_(a,e)` and its conjugate when `a>alpha(e)`;
- `Q_(a,e), P_(a,e)` and its conjugate when `a=alpha(e)`.

Both branches are strict local minima under all independent closed-disk
original-root motions at fixed `a,E`, throughout this rectangle. Thus the
losing branch is locally strict but nonglobal away from the curve. The
curve in (3) is now a **global-minimum transition** on this rectangle.
Its construction, coefficient and comparison sign retain 8160 credit;
the global interpretation is the new conclusion.

For the moving-pair local statement define
\[
L_Q(a)={208a^2+232a-215\over1152(1+a)^5},\qquad
B_Q(a)={69025-73880a-66416a^2\over12288(1+a)^5}.
\tag{4}
\]
Let
\[
a_-={6\sqrt{101}-29\over52},
\]
and let `a_+` be the unique positive root of
`69025-73880a-66416a^2=0`. Exact signs below show
\[
a_-<151/250<a_G<121/200<a_+<303/500.
\tag{5}
\]
In particular `J0=[151/250,121/200]` lies above the credited P local
threshold `a_*=(10sqrt2198-225)/404` and inside `(a_-,a_+)`.

Use two distinguished root phases and a six-root block:
\[
z_+=-(1-\tau_+)e^{i(M+T)},\quad
z_-=-(1-\tau_-)e^{i(M-T)},\quad
z_j=-(1-\tau_j)e^{i(N+\eta_j)},\quad\sum_{j=1}^6\eta_j=0,
\]
\[
m={M+3N\over4},\quad
M=m+3tb,\quad N=m-tb,\quad
\eta=th,\quad m=t^2y,\quad\tau=t^4r,\quad T=t\sigma.
\tag{6}
\]
Here `r>=0`, `t` is (2), and exact energy fixes the positive `sigma`.
The five split directions `h`, relative block mean `b`, common mean `y`
and all eight inward depths are independent local coordinates.

**Theorem 2 (all-motion local Q minimum and costs).** On every nonempty
compact `J subset(a_-,a_+)`, one common sufficiently small box in `(h,b,y,r)`
and one common positive energy threshold give
\[
\begin{split}
F-F(Q)\ \ge\;&v_1^2\sum\tau_j+{5\over2}v_1^3m^2
 +{L_Q(a_0)\over2}t^2\|\eta\|^2\\
&+{B_Q(a_1)\over32}t^2(M-N)^2,
\end{split}
\tag{7}
\]
where `a0=min J,a1=max J,v1=(1+a1)^-1`. Equality holds only at Q.
The costs are explicit sufficient constants; the box and threshold are
existential. This proves strict local minimality for every positive
energy in the common interval, including arbitrary critical collisions.

**Theorem 3 (leading angular instability outside the interval).** At
each fixed `0<=a<a_-` or `a_+<a<=1`, Q is not a local `E=e` minimum for
every sufficiently small positive energy. An exact-energy circle motion
in a six-block split direction or the relative block-mean direction
decreases F, respectively. No finite-energy classification at the two
degenerate endpoint radii is asserted.

**Theorem 4 (true Q fine excess).** For fixed finite `D>=0` and J as in
Theorem 2, every configuration in its local chart with `F-F(Q)<=D e^3`
enters a bounded fine chart
\[
\eta=t^2\xi,\quad M-N=4t^2\beta,\quad m=t^3\upsilon,
\quad\tau=t^6\rho.
\]
There is one constant and one common small threshold, depending on `J,D`,
such that
\[
\mathcal C_Q=2v^2\sum\tau_j+5v^3m^2
 +L_Q(a)t^2\|\eta\|^2+{B_Q(a)\over16}t^2(M-N)^2,
\]
\[
|F-F(Q)-\mathcal C_Q|\le C_{J,D}t\mathcal C_Q.
\tag{8}
\]
The bound is relative even when coordinates vanish, and counts all
critical multiplicities. It is a local branch-relative law. Near the
transition the other branch may also have excess of order `e^3`; no
single-chart entry for every global near-minimum is asserted.

**Theorem 5 (sharpness of the credited angular interval and full-disk minima).**
For `0<=a<=1`, one has `K_a(theta)<=K_Q(a)` for **every** balanced
nonzero real theta if and only if
\[
a_-\le a\le a_G.
\]
The sufficient interval and its equality classification retain review 8230
credit. The necessity of the lower endpoint follows from the split Hessian
proved here. The complete angular equality set is the moving-pair scale/permutation
orbit for `a_-<=a<a_G`, and the two credited orbits at a=a_G.
For every nonempty compact `J subset(a_-,a_G]` there is one common
positive energy threshold such that Q alone is the exact full-disk
`E=e` global minimum for every a in J and every positive energy below
the threshold, modulo scalar/permutation. At each fixed `a<a_-` or
`a>a_G`, Q is nonglobal for every sufficiently small positive energy.
The exact actual finite-energy status at a=a_- remains unclassified;
its unique leading angular optimizer and zero split stiffness do not
resolve that endpoint.

## 2. Precise credited inputs

We use the following ordinary mathematical statements, with their
original authors and review scopes preserved in LITERATURE.md.

1. Angular functional and Gram geometry from 7432/7472 and independent
   review 7496. For balanced nonzero real theta, let
   `H=Pdiag(theta)P` on `e_*^perp`, `e_*=1/sqrt8`,
   `w=diag(theta)e_*`, and use full distinct-eigenspace projectors in
   `Psi=sum_lambda||Pi_lambda w||^4`. With
   `X=mu4/mu2^2`, `eta_sp=64Psi/mu2^2`,
\[
K_a=A_dX+B_d-C_d\eta_{\rm sp},\quad
\Delta=43/56-X\ge0,\quad
\Gamma=\eta_{\rm sp}-(56X-13)/30\ge0,
\]
\[
A_d={d^3(48d^2-40d-53)\over512},\quad
B_d={d^3(16d^2-104d+203)\over8192},\quad
C_d={d^3(4d+1)^2\over8192}.
\]
2. Graph 8160's sharp identity and complete equality set:
\[
K_1-K_a=S(a)\Delta+C_d\Gamma,\quad
S(a)={d^3(2768a^2+3080a-2875)\over30720}.
\tag{9}
\]
   `S(a_G)=0`; the entire `Gamma=0` set on the balanced unit sphere
   is the union of the singleton/seven and moving-pair permutation
   orbits. K, Psi and Gamma are continuous through collisions. The
   actual Q construction, jointly analytic comparison and (3) are
   credited 7328/8160. They do not already identify a global transition.
3. Graph 8212's full-disk bootstrap and quartic reduction on all `[0,1]`.
   For each fixed finite comparison tolerance D,
   `F<=F(P)+D e^2,E=e` implies, uniformly in a, unique small lifts
   `z_j=-(1-tau_j)exp(i phi_j)` with
\[
R=\sum\tau_j=O_D(e^2),\quad m={1\over8}\sum\phi_j=O_D(e),
\quad\|\phi-m\mathbf1\|^2=e/v^4+O_D(e^2)>0.
\tag{10}
\]
   On bounded mean/radial boxes the complete angular quartic is
\[
G-\kappa E=s^4\{-v^8K_a(\theta)+5v^3y^2+2v^2\sum r_j\}+o(s^4)
\tag{11}
\]
   for balanced unit theta, `phi=s theta+s^2y1,tau=s^4r`.
   The little-oh is compact-uniform through collisions and all a.
   Signed bounded radial variables are permitted for its analytic
   construction. This is not a universal uniform `O(s^6)` assertion.
   The corresponding normalized comparison is
\[
{F-F(P)\over e^2}=S(a)\Delta+C_d\Gamma
 +5v^3{m^2\over e^2}+2v^2{R\over e^2}+o(1).
\tag{12}
\]
   Full-disk small-energy minima exist. Section 4 of that source
   reestablishes the P touching support and positive coarse chart on
   **every compact set above a_***, independently of whether P is
   global. This local statement, not its above-a_G global theorem, is
   used on J0. Its branch and local coefficients retain 7777/7819 credit;
   the harmonic-support method retains 7839/7910/8046/8102 credit.

These are explicit premises. Independent review 8102 confirms 8046 on its
stated domain. Review 8230 confirms 8160 and independently proves the
moving-pair angular interval and stronger comparison bound. Review 8258
confirms 8212 and proves evaluated full-disk asymptotics and leading Q
geometry on the closed interval [a_-,a_G]. None identifies the exact Q
minimum or global transition proved here, or reviews the new deductions.

## 3. New moving-pair angular Hessian

Work first with the unnormalized balanced vector
`theta_Q=(1,-1,0^6)`. Its `X=eta_sp=1/2`, `Gamma=0`,
`Delta=15/56`. K is homogeneous of degree zero.

There are five balanced six-block split directions and one relative
block-mean direction tangent to its normalized angular sphere. The
quadratic form is invariant under the six-block permutation group.
Its split block must be a scalar times the Euclidean norm: a permutation
invariant matrix has one diagonal and one off-diagonal entry, and on
the zero-sum subspace its quadratic form is scalar. Mixed split/relative
terms vanish because an invariant split linear functional is a multiple
of the sum. Thus two exact curves determine the entire centered Hessian.

First justify twice differentiability at this collided profile. The
angular matrix H is real symmetric. Its five-dimensional small group
has a separated projector analytic in nearby theta. At theta_Q its
projection of w is zero, so the total w-weight of this group is
`O(||theta-theta_Q||^2)`. The sum of squares of its individual weights
is at most the square of their total, hence `O(||theta-theta_Q||^4)`.
The other two angular eigenvalues are simple, with analytic weights.
Consequently Psi has a well-defined full quadratic expansion here,
including arbitrary splits inside the five-group. No internal gap is used.

### 3a. Six-block splitting

Take slopes `(1,-1,s,-s,0^4)` and put `z=s^2`. The angular characteristic
is the original-root characteristic derivative divided by eight:
\[
{1\over8}{d\over d\lambda}
[\lambda^4(\lambda^2-1)(\lambda^2-z)]
=\lambda^3[\lambda^4-3(1+z)\lambda^2/4+z/2].
\]
Let `y1,y2` be the two nonzero eigenvalue squares. Their sum/product are
`3(1+z)/4,z/2`. At the two eigenvalues in each opposite pair let the
w-weight be `W1,W2`. Literal projected-matrix moments give
\[
W_1+W_2=(1+z)/8,\quad
y_1W_1+y_2W_2=(3-2z+3z^2)/32.
\]
Therefore, with complete eigenspace weights,
\[
\Psi={ (1+z)^2\over64}
 +{(3-10z+3z^2)^2\over64(9-14z+9z^2)}
={1\over32}-{7\over144}z+O(z^2).
\tag{13}
\]
The other three eigenvalues have zero w-weight. At z=0 the additional
small pair joins them with zero weight, and (13) extends continuously.
Since `mu2=2+2z,mu4=2+2z^2`,
\[
X=1/2-z+O(z^2),\quad
\eta_{\rm sp}=1/2-16z/9+O(z^2),\quad
\Gamma=4z/45+O(z^2).
\tag{14}
\]
For independence the checker also computes the direct secular norm
`W=8/sum_j(lambda-theta_j)^-2` and compares it with both moment weights
by complete polynomial reduction modulo the displayed quadratic in y.
This is a full identity, not a finite set of tested slopes.

### 3b. Relative block mean

Take slopes `(1+3b,-1+3b,(-b)^6)`. The characteristic derivative is
\[
(\lambda+b)^5[\lambda^2-5b\lambda+6b^2-3/4].
\]
The five repeated eigenvalues have zero w-weight. For the other two,
`lambda_++lambda_-=5b`, `(lambda_+-lambda_-)^2=3+b^2`,
\[
W_++W_-={1\over4}+3b^2,\quad
(W_+-W_-)(\lambda_+-\lambda_-)=13b/4-3b^3.
\]
Thus
\[
\Psi={1\over2}\left\{(1/4+3b^2)^2
                  +{(13b/4-3b^3)^2\over3+b^2}\right\}
={1\over32}+{241\over96}b^2+O(b^4).
\tag{15}
\]
Here `mu2=2+24b^2,mu4=2+108b^2+168b^4`, giving
\[
X=1/2+15b^2+O(b^4),\quad
\eta_{\rm sp}=1/2+169b^2/6+O(b^4),\quad
\Gamma=b^2/6+O(b^4).
\tag{16}
\]
The checker independently compares these moment weights with the direct
secular norm by full polynomial reduction modulo the characteristic
quadratic in lambda. It also derives all three spectral moments from
literal projected 8x8 matrices for both curves.

Subtract (9) at theta_Q. For the split curve and relative curve,
respectively,
\[
K_Q-K_a=(S+4C_d/45)s^2+O(s^4),\qquad
K_Q-K_a=(-15S+C_d/6)b^2+O(b^4).
\tag{17}
\]
At fixed leading energy `mu2=2`, the objective's quartic coefficient is
`4v^8(K_Q-K_a)`. The split curve has squared split norm `2s^2`.
Homogeneity and angular stationarity mean that the second-order amplitude
adjustment does not change these Hessian coefficients. Consequently the
full centered quadratic form is
\[
L_Q(a)\|h\|^2+B_Q(a)b^2,
\]
\[
L_Q=2v^8(S+4C_d/45),\qquad
B_Q=4v^8(-15S+C_d/6).
\tag{18}
\]
Clearing the positive `d^5` gives exactly (4). The factor16 converting
`b` to the physical mean difference in (8) follows from `M-N=4tb`.

The numerator of L_Q increases on `[0,1]` and vanishes at a_-.
The numerator of B_Q decreases and has its unique positive zero at a_+.
Exact signs at the rational endpoints prove (5), also using monotonicity
of the known P_G polynomial. The P local numerator is positive at151/250.
Moreover the derivative numerators of L_Q and B_Q are
\[
1307-512a-624a^2\ge171>0,
\]
\[
199248a^2+162688a-419005\le-57069<0.
\tag{19}
\]
Thus the endpoint minima in (7) are valid on every compact J in the
positive interval, not merely the displayed rational J0.

### 3c. The independently proved Gram consequence and angular Q interval

Review 8230, actual six-reviewer-3, independently published this stronger
Gram consequence and the sufficient closed angular interval during the
present pass. We retain that result's credit and reconstruct the deduction
to make the new sharpness and full-disk transfer explicit. The following
algebra is reproduction of that input, not a separate new contribution.

Normalize mu2=1 and let `Z=mu3^2`. The classical scalar moment slack and
the independently reviewed spectral Gram quantities are
\[
h_0=Z-\tfrac{12}{5}(X-1/2)\ge0,\quad
D=\tfrac34\Delta-\tfrac{25}{48}h_0,\quad
N=\Delta-\tfrac56h_0,\quad B=\tfrac17+\tfrac43Z.
\]
Independent review 7496 gives `D>0` whenever Delta>0, including the
singular-case proof, and
\[
\eta_{\rm sp}\ge B+N^2/D,\qquad
\left(B-\tfrac{56X-13}{30}\right)D+N^2=\Delta h_0/36.
\]
Subtract `h0 D/27`. The independently published form of this certificate is
the complete polynomial identity
\[
\left(B-\tfrac{56X-13}{30}-\tfrac{h_0}{27}\right)D+N^2
={25h_0^2\over1296}.
\]
Therefore, off the moment endpoint,
\[
\boxed{\quad \Gamma\ge {h_0\over27}
                  +{25h_0^2\over1296D}\ge {h_0\over27}.\quad}
\tag{19a}
\]
At Delta=0 the credited singleton classification gives h0=Gamma=0,
so the division-free final inequality remains true. In particular,
\[
\Gamma\ge {4\over45}(1/2-X)+Z/27,
\]
with a strictly positive additional residual if h0>0. The Gram certificate
and scalar inequality retain their original credit; the stronger consequence
and sufficient optimizer interval retain review 8230 credit. The derivation
is explicit and uses no numerical search.

For `a_-<=a<a_G` we have `S<0` and `S+4C_d/45>=0`, by (18).
Subtract (9) at Q:
\[
K_Q-K_a=S(1/2-X)+C_d\Gamma.
\]
If X>1/2 this is strictly positive. If X<=1/2, (19a) gives
\[
K_Q-K_a\ge(S+4C_d/45)(1/2-X)+C_d Z/27\ge0.
\tag{19b}
\]
When X<1/2, h0>0 and the positive residual in (19a) makes the inequality
strict, even at a=a_-. For X=1/2 equality requires Gamma=0, hence the
credited complete equality classification gives exactly Q. At a=a_G,
the same classification gives both orbits.

For a<a_-, the split coefficient `S+4C_d/45` in (17) is negative,
so the exact split curve violates `K_a<=K_Q` for sufficiently small
positive s. For a>a_G the singleton has `K1>K_Q`, directly from (9).
This proves the new necessity of the lower endpoint, completing sharpness
of the credited interval. The sufficient angular assertion and every
equality case, including the degenerate leading lower endpoint, reproduce
review 8230. The actual Q minimum below the transition is proved in Section 7a.

## 4. Exact energy and separated groups

In (6), exact energy divided by t^2 is real analytic on a signed small
box, including t=0. Its leading value is
\[
v^4(2\sigma^2+24b^2+\|h\|^2),
\]
whereas (2) divided by t^2 has leading value `2v^4`. The positive energy
IFT therefore gives a unique analytic amplitude with
\[
\sigma_0=\sqrt{1-12b^2-\|h\|^2/2},\qquad
\sigma=\sigma_0+O(t^2),\quad
\partial_\sigma(E/t^2)=4v^4\sigma_0>0.
\tag{20}
\]
All constants are common on a prescribed compact radius set. There is
no cubic energy term: the leading phases are centered, the circle energy
is even in each phase, and radial changes begin at higher order.

Write `u_j=(a-z_j)^-1`. The credited reciprocal critical matrix is
`N=diag(u)(I+11^T)`, with characteristic `9R(q)-qR'(q)` where
`R=prod(q-u_j)`. At Q let `u_++u_-=j,u_+u_-=h0`; the other six
reciprocals are v. Its **complete** characteristic is
\[
(q-v)^5[q^3-(7v+2j)q^2+(3h_0+8vj)q-9vh_0].
\tag{21}
\]
This agrees with the literal derivative of the actual original polynomial
in (1), not just a feasible reciprocal tuple. The five repeated roots
are exactly v, the simple far root is `9v+O(t^2)`, and the remaining
roots satisfy
\[
q_\pm=v\pm i(\sqrt3/2)v^2t+O(t^2).
\tag{22}
\]
These gaps are uniform for `v in[1/2,1]`. The old cubic and its negative
near discriminant, from 8160, were exactly replayed before this work.

For clarity the full linear coordinate compression is also verified here.
Let `Q6=I6-11^T/6`, split off its five-dimensional range, and use
complement columns `e_+,e_-,1_B` with dual third row `1_B^T/6`.
In the natural six-coordinate representation the four blocks are
\[
A=Q6\operatorname{diag}(u_B)Q6,\quad
B=Q6u_B(1,1,7),\quad
D=\begin{pmatrix}0\\0\\u_B^TQ6/6\end{pmatrix},
\]
\[
C=\begin{pmatrix}
2u_+&u_+&6u_+\\u_-&2u_-&6u_-\\
\overline u_B&\overline u_B&7\overline u_B
\end{pmatrix},\qquad \overline u_B={1\over6}\sum_Bu_j.
\tag{23}
\]
The bar here denotes the block average, not complex conjugation.
Every entry of every block is checked on all eight original reciprocal
coordinate basis inputs, which span the entire linear map over C.
At Q both cross blocks vanish, the five block is `vI`, and its left/right
spaces are the same fixed Euclidean six-block zero-sum space.

## 5. A collision-safe touching support on a common coarse box

The construction below uses only compact radius bounds and the external
and divided gaps. It does not require positive L_Q or B_Q until Section 6.

First eliminate the far root analytically. One may use the fixed similar
matrix `Sdiag(u)S`, where `S=P+3Q`, `P=I-e_*e_*^*`, `Q=e_*e_*^*`.
Its collapsed matrix is `v(P+9Q)` with external gap `8v>=4`. The analytic
near invariant graph over `e_*^perp` gives a seven-block
\[
N_7=vI+ctH_{\theta_0}+O(t^2),\quad c=-iv^2,
\]
where `theta0=(sigma0+3b,-sigma0+3b,(-b+h_j)_1^6)` is real and
balanced. The divided matrix `(N7-vI)/(ct)` is analytic at t=0.
At the origin its leading H has eigenvalues `sqrt3/2,-sqrt3/2,0^5`.
On one common small `(h,b)` box these two eigenvalues remain simple and
the entire five-group remains separated from them. Riesz projections and
invariant graphs therefore give analytic `q_+,q_-,q_f` and the entire
five-block `N5`, including t=0. No gap inside that block is imposed.

Choose its frame carefully. The leading five projection at t=0 is real
orthogonal because H is real symmetric. Its range is a graph K0 over
the fixed six-block zero-sum space. Multiply the actual analytic graph
frame by `(I+K0^T K0)^-1/2`. This real analytic normalization makes
the **whole leading five-block coefficient** Hermitian, not just its
eigenvalues. At the actual branch K0=0 and the block is exactly `vI`
for every t. Thus
\[
W=(N_5-vI)/c=tW_1(h,b)+O(t^2),\qquad W_1=W_1^*,
\tag{24}
\]
jointly on the whole box. Frame choices change no trace or eigenvalue.

Use the scalar analytic primitive
\[
f(w)=v\sqrt{1+v^2w^2}-iv\operatorname{arsinh}(vw),
\tag{25}
\]
with both analytic branches at zero. It is the harmonic-support primitive
at `u=v,c=-iv^2`; the general method retains the earlier support/review
credit. Let `H0(w)=|v+cw|-Re f(w)`. On the real axis, H0 and its first
normal derivative vanish, and
\[
(H_0)_{yy}(x)=v^3/\sqrt{1+v^2x^2}>0.
\]
Taylor's integral remainder gives `H0(w)=(Im w)^2 K(a,w)` with one
uniform positive bounded K on a common small disk. Define
\[
\Phi=\operatorname{Re}\operatorname{tr}f(W)
      +|q_+|+|q_-|+|q_f|.
\tag{26}
\]
Analytic functional calculus counts every algebraic multiplicity.
The scalar inequality implies `Phi<=F`, with equality at Q, and Phi is
jointly real analytic through all collisions in the five-group.

We need a stronger defect estimate than an arbitrary `O(t^4)` at the
origin. Put `X0=(h,b,y)` and `R0=sum r_j`. By (24), `Im_Herm W` is
divisible by t^2 on the whole signed box. At the branch W=0. Every
first angular derivative of W is real symmetric for **every t**:
the fixed five-block compression of a first variation is
`Q6 diag(delta u_B)Q6`, by (23), and
\[
\delta u_B=c(t\delta h-t\delta b+t^2\delta y\mathbf1).
\]
Pair variations and the amplitude correction have zero first compression.
Changes of frame contribute no first term because the branch block is
scalar. Hence the imaginary Hermitian part and all its first angular
derivatives vanish exactly there.

Radial derivatives of W are `O(t^4)` uniformly on the whole box. To see
the order, `tau=t^4r` changes literal reciprocals at order t^4. Also
`E_tau=O(t^2)` uniformly for these small phases, so the energy IFT gives
`sigma_r=O(t^4)` and its phase correction starts at t^5. Far elimination
preserves the t^4 order. Dividing the seven near matrix by t makes its
radial derivatives `O(t^3)`; the separated five projector/frame has the
same order. Multiplication back by t restores order t^4. The leading
orthonormal normalization depends only on `(h,b)`, so adds no radial term.

Joint analytic Taylor integration now gives
\[
\|\operatorname{Im}_{\rm Herm}W\|
\le C\{t^2\|X_0\|^2+t^4R_0\},\quad r\ge0.
\tag{27}
\]
For any right eigenvector of W, normalized in this fixed Euclidean frame,
`Im lambda=w^*(Im_Herm W)w`, whether or not the block is diagonalizable.
Using (25) for all five eigenvalues proves
\[
0\le F-\Phi\le C\{t^4\|X_0\|^4+t^8R_0^2\}.
\tag{28}
\]
The same signed-box bound uses `sum|r_j|` for analytic construction.
At fixed positive t the defect starts at fourth angular order; in
particular the true angular Hessian equals the support Hessian.

Equation (11), (20) and bounded parameters give `F-F(Q)=O(t^4)` on
the whole signed box. Together with (28) and analyticity of Phi this
proves the whole-box divisibility
\[
\Phi-F(Q_{a,E_Q(a,t)})=t^4\mathscr R_Q(a,t,h,b,y,r)
\tag{29}
\]
with a jointly analytic quotient. Boundedness shows that all lower
t-coefficients vanish identically on the box; no individual-profile
interpolation is used.

## 6. Stationarity and the positive local chart

On the zero-radial face, conjugation followed by interchange of the two
distinguished roots sends `(h,b,y)` to `(-h,-b,-y)` and preserves exact
energy. The scalar primitive obeys `f(-conj w)=conj f(w)`; the three
simple moduli and the full trace are invariant. Thus Phi is even under
this simultaneous sign change, and its angular gradient vanishes at
the origin for every small t. Its value there is exactly F(Q).
This proves actual constrained angular stationarity, not a truncated mean.

At t=0 the complete quartic (11), with leading `mu2=2`, gives
\[
4v^8(K_Q-K_a(\theta_0))+5v^3y^2+2v^2\sum r_j.
\]
The defect (28) changes its angular expansion only at fourth order.
Section 3 therefore gives the full limiting derivatives
\[
(\mathscr R_Q)_{hh}=2L_Q I_5,\quad
(\mathscr R_Q)_{bb}=2B_Q,\quad
(\mathscr R_Q)_{yy}=10v^3,
\]
\[
(\mathscr R_Q)_{hb}=(\mathscr R_Q)_{hy}
=(\mathscr R_Q)_{by}=0,\qquad
(\mathscr R_Q)_{r_j}=2v^2.
\tag{30}
\]
All derivatives are at the branch and t=0. The split norm uses the
Euclidean zero-sum six-space, not a nonorthogonal coordinate norm.

On compact J inside `(a_-,a_+)`, (19) and continuity give positive common
lower bounds for these derivatives. Shrink one convex box and the common
t threshold so the angular Hessian retains half its limiting blockwise
lower bound on the zero-radial face, and every radial gradient remains
at least `v1^2`. Integrate the angular Hessian from the stationary origin,
then the radial gradients along r>=0. This yields
\[
\mathscr R_Q\ge {L_Q(a_0)\over2}\|h\|^2
 +{B_Q(a_1)\over2}b^2+{5\over2}v_1^3y^2+v_1^2R_0.
\]
Multiplication by t^4 and `M-N=4tb` prove (7). These coordinates are a
chart of every nearby fixed-energy disk-root motion; the positive amplitude
IFT and unique small root lifts supply completeness. This proves Theorem 2.

If a<a_- or a>a_+, the respective limiting Hessian in (30) is negative.
At fixed sufficiently small positive t the true Hessian equals the support
Hessian, by (28), and its corresponding sign remains negative. A small
nonzero circle split or relative-mean perturbation, with the exact positive
energy amplitude (20), strictly decreases F. All roots remain on the
unit circle and all multiplicities are counted. This proves Theorem 3;
it makes no assertion at a_- or a_+ where the leading term vanishes.

## 7. Global entry into the two local charts

Use the fixed rational compact set J0 in (5). The new Q chart and the
credited P local chart are both uniform there and locally strict.
Choose their common small angular/mean/radial boxes first. We now prove
there are `delta>0,epsilon>0,e0>0` forcing every full-disk configuration
with
\[
|a-a_G|\le\delta,\quad E=e<e_0,\quad
F\le\min(F(P),F(Q))+\epsilon e^2
\tag{31}
\]
into one of those boxes. This step is necessary; local strictness alone
cannot identify a global minimum.

Take epsilon<=1. Since the minimum of the two values is at most F(P),
the uniform bootstrap (10) gives one bounded comparison box. Apply (12).
On J0, C_d and both physical costs have positive lower bounds, whereas
`S(a_G)=0` and `|S(a)|<=C|a-a_G|`. Cauchy--Schwarz gives
`0<=Delta<=9/14`. Hence, with one common remainder tending to zero,
\[
\Gamma+{m^2\over e^2}+{R\over e^2}
\le C_0\{\epsilon+\delta+\omega(e)\},\qquad\omega(e)\to0.
\tag{32}
\]
No sign for S below a_G has been assumed.

On the compact balanced unit sphere, Gamma is continuous and its entire
zero set is exactly the two credited orbits. Thus for any prescribed
small angular neighborhood of that union there is a positive Gamma
threshold forcing entry. Choose delta and epsilon small enough, then
one common e0 small enough. Formula (32) makes the centered direction
close to one orbit, `m/e` small and `R/e^2` small, uniformly in (31).

Near the Q orbit label the positive/negative phase pair. The definitions
in (6) give `h,b` small, `y=m/t^2` small and `sum r=R/t^4` small,
using (2) and (10). The actual positive amplitude has
`2(T/t)^2+24b^2+||h||^2=2+O(t^2)`, so it is precisely the positive
energy IFT solution in (20). Thus it enters the new Q coarse box.
Near the P orbit label its singleton and conjugate if needed. The same
centered angular decomposition gives the credited P split parameters
small, its mean parameter `(m-m0)/s^2` small because `m0=O(s^3)`,
and its inward coordinates small because `s^2` is comparable to e.
Its positive energy amplitude is likewise the credited IFT solution.
This gives entry into the P coarse box on J0, without invoking an
above-a_G global theorem below its domain. Decrease all three thresholds
to enter strictly inside the boxes.

An attained global minimum exists by the credited compact-level theorem
and is at most both actual family values. Therefore it satisfies (31).
In either local box the respective positive costs give F at least its
family value, with equality only at that entire actual family. It follows
that the global value is exactly the smaller family value and that its
complete equality set is exactly the winning branches. The previously
proved jointly analytic comparison (3), restricted to this rectangle,
now supplies the three cases of Theorem 1. No new higher-order comparison
coefficient, numerical optimum or heuristic completeness is used.

### 7a. Uniform actual Q minima below the transition neighborhood

Let J be compact in `(a_-,a_G)`, bounded away from a_G. By Section 3c,
`K_Q-K_a>=0` and Q is its unique angular equality orbit. Continuity on
the compact radius/normalized-sphere domain gives one positive gap off
any prescribed small Q angular neighborhood. For configurations with
`F<=F(Q)+epsilon e^2`, use the credited uniform actual comparison
`F(Q)<F(P)` on `[0,a_G]` to apply (10). Subtract the Q expansion in
(11) instead of P. The normalized expression is
\[
{F-F(Q)\over e^2}=K_Q-K_a(\theta)
 +5v^3{m^2\over e^2}+2v^2{R\over e^2}+o(1).
\]
All three terms are nonnegative. Choose one small epsilon and then
one common energy threshold to force the angular neighborhood and
the small mean/radial parameters required by the Q coarse chart on J.
The same positive-amplitude argument following (32) proves actual entry.
Every attained minimum then equals Q by its strict physical costs.

For a compact set in `(a_-,a_G]`, cover its upper part by the transition
rectangle of Theorem 1. There `a<=a_G<alpha(e)` for all sufficiently
small positive e, so Q is the exact unique global family. The remaining
lower compact part is bounded away from both endpoints and is covered
by the preceding argument. The minimum of the two common thresholds
is a common threshold for the entire compact set. This proves the
actual positive assertion of Theorem 5.

For fixed a<a_- the circle instability of Theorem 3 excludes Q. For
fixed a>a_G the credited actual P/Q quartic comparison has `F(P)<F(Q)`
at all sufficiently small positive energies. Thus Q is nonglobal there.
At a=a_- the split Hessian vanishes; nothing in this proof identifies
the actual finite-energy minimum at that radius.

## 8. True physical Q fine law

Within the Q coarse chart, (7) and `F-F(Q)<=D e^3` imply
`sumtau=O(t^6),m=O(t^3),eta=O(t^2),M-N=O(t^2)`.
Thus `h=t xi,b=t beta,y=t upsilon,r=t^2rho` is a bounded fine box.
Value and angular stationarity in (29) hold for every t. Taylor integration
using (30), with positive compact coefficient bounds, gives
\[
\Phi-F(Q)=t^6\{Q_0+O_{J,D}(t)(\|\xi\|^2+\beta^2+\upsilon^2+\sum\rho)\},
\]
\[
Q_0=L_Q\|\xi\|^2+B_Q\beta^2+5v^3\upsilon^2+2v^2\sum\rho.
\tag{33}
\]
This is a relative bound: stationarity removes every cost-free constant
and linear angular term. The support defect (28) becomes
\[
0\le F-\Phi\le C_{J,D}\{t^8(\|\xi\|^2+\beta^2+\upsilon^2)^2
                               +t^{12}(\sum\rho)^2\}
\le C_{J,D}t^2\,t^6Q_0.
\]
Adding to (33) proves (8), including all zero-coordinate cases and
arbitrarily collided five-block eigenvalues. The true fine-excess method
retains the earlier independent 8102 credit; the Q chart and its two new
centered coefficients are established here.

## 9. Evidence and remaining scope

The standalone exact checker proves complete physical and reciprocal
polynomial identities, full angular characteristic factorizations, two
moment/secular weight identities, literal projected-matrix moments,
both whole stiffness polynomials and exact compact-interval signs. Its
linear compression controls cover every entry of all four blocks on all
eight coordinate inputs. Full required fixture comparison remains active
under optimization; damaged mathematical expressions and altered fixtures
are rejected. No floating-point output is a proof input.

Uniform analytic projection/frame construction, scalar harmonic support,
weighted divisibility, derivative interpretation, compactness, energy IFT,
and two-chart completeness remain ordinary written mathematics outside a
formal kernel. The previous full-disk quartic and complete Gamma=0 claims
are independently reviewed premises, not independently audited by this checker.
Source publication and ledger commitment do not confer independent review.

The global theorem is one common sufficiently small rectangle about
`(a_G,0)`, with the additional compact-uniform actual Q interval
`(a_-,a_G]` and sharp angular Q interval `[a_-,a_G]`. It does not evaluate
angular optimizers below a_-, extend the global classification to arbitrary
energy, give an effective numerical
threshold, classify finite-energy endpoint degeneracies at a_- or a_+,
prove historical priority, or resolve the unrestricted first-power
Tang--Zhang endpoint. The lower-side global branch and transition near
this tie are now identified within the explicitly stated rectangle.
