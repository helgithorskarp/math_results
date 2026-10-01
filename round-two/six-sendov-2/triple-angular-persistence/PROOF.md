# Persistence and stability of the triple-pair angular optimizer

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Ordinary written author proof with exact rational identity checks.
Independent review is pending; the analytic arguments are not formalized.

The isolated equality profile in the
[lower angular theorem](../lower-angular-active-stratum/PROOF.md), source
`31128813146eea02934646e462c51979b0c808cd`, graph8597, persists as the
complete global angular optimizer on a nonzero interval on both sides.
This is a complementary stability result for the degree-nine first-power
family. It does not prove the first-power conjecture or classify actual
finite-energy disk minimizers. The explicit local interval in Section 6
and the restricted comparison in Section 7 have different scopes from
the global interval in Theorem 1.

## 1. Definitions and main theorems

Let
\[
\mathcal S=\{\theta\in\mathbb R^8:\ \sum_j\theta_j=0,
                                      \ \sum_j\theta_j^2=1\},
\quad e=\mathbf1/\sqrt8,\quad P=I-ee^T,
\]
\[
H=P\operatorname{diag}(\theta)P|_{e^\perp},\qquad
w=\operatorname{diag}(\theta)e,
\]
and, with projections onto full eigenspaces,
\[
X(\theta)=\sum_j\theta_j^4,\qquad
\eta(\theta)=64\sum_{\lambda\ {m distinct}}
                          \|\Pi_\lambda w\|^4,\qquad J_R=RX-\eta.
\]
Repeated compression eigenspaces have zero coupling. Equivalently, list
seven compression eigenvalues with multiplicity; give each simple slot
weight \(\rho_i=8\|\Pi_iw\|^2\), and each repeated slot weight zero.
Then \(\eta=\sum_i\rho_i^2\). This convention includes all collisions.

The credited all-radius angular functional is
\[
K_a=B_d+C_dJ_{R(d)},\qquad d=1+a,
\]
\[
B_d=\frac{d^3(16d^2-104d+203)}{8192},\quad
C_d=\frac{d^3(4d+1)^2}{8192},\quad
R(d)=\frac{16(48d^2-40d-53)}{(4d+1)^2}.
\tag{1}
\]
Its source is [graph8160](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_moving_pair_comparison_boundary/PROOF.md),
checked in [review8230](https://github.com/helgithorskarp/math_results/blob/main/sendov_moving_pair_threshold_review3/REVIEW.md).
The present mathematical optimizer statement concerns \(J_R\) directly.

Put
\[
r_3=\frac9{56},\quad t_3=\frac1{56},\quad
R_3=-\frac{80}{9},\quad a_3=\frac{3\sqrt{29}-11}{16}.
\]
The labeled base vector has three entries \(+\sqrt{r_3}\), three entries
\(-\sqrt{r_3}\), and the remaining entries \(+\sqrt{t_3},-\sqrt{t_3}\).
For a nearby \(r\), write \(t=1/2-3r\) and
\[
F_r(z)=(z^2-r)^3(z^2-t),\qquad
\mathcal R(r)=\frac{16(4r-1)(576r^2-112r+3)}{(16r-3)^3}.
\tag{2}
\]

**Theorem 1 (complete global persistence).** There is \(\epsilon>0\)
and a unique real analytic \(r(R)\) near \(R_3\), specified by
\(\mathcal R(r(R))=R\) and \(r(R_3)=9/56\), such that for every
\(R\in[R_3-\epsilon,R_3+\epsilon]\) the complete global maximizing
orbit \(\mathcal O_R\) of \(J_R\) on \(\mathcal S\) is exactly the
permutations of the roots of \(F_{r(R)}\). In particular,
\[
r(R)=\frac9{56}+\frac{27}{119168}(R-R_3)+O((R-R_3)^2).
\tag{3}
\]
Simultaneous sign reversal already belongs to this permutation orbit.
The interval length is existential, not an effective global certificate
for the explicit interval in Section 6.

**Theorem 2 (quadratic root stability and sharp tangent constant).** After
shrinking \(\epsilon\), a uniform \(c>0\) satisfies
\[
M(R)-J_R(\theta)\ge c\operatorname{dist}(\theta,\mathcal O_R)^2,
\quad M(R)=\max_{\mathcal S}J_R,
\tag{4}
\]
for every \(\theta\in\mathcal S\) and every \(R\) in Theorem 1's
interval. Distances use the Euclidean norm of the real root vector.
At \(R=R_3\), the sharp local coefficient is \(32/21\):
\[
\liminf_{\theta\to\mathcal O_{R_3},\ \theta\notin\mathcal O_{R_3}}
 \frac{M(R_3)-J_{R_3}(\theta)}
      {\operatorname{dist}(\theta,\mathcal O_{R_3})^2}
 =\frac{32}{21}.
\tag{5}
\]
The global constant \(c\) is not computed. Multiplication by \(C_d>0\)
transfers (4) to \(K_a\). Since
\(R'(d)=2048(2d+3)/(4d+1)^3>0\), both theorems also give a nonzero
marked-radius interval on both sides of \(a_3\).

**Theorem 3 (exact value response and formal gap).** With \(\delta=R-R_3\),
\[
M(R)=-\frac{763}{441}+\frac{61}{392}\delta
                         +\frac{81}{417088}\delta^2+O(\delta^3).
\tag{6}
\]
For \(b(R)=2-\sqrt{4-2R}\) and the spectral-square upper value
\[
V_b=\frac{13R}{56}-\frac17+\frac{15b^2}{224},
\]
\[
V_{b(R)}-M(R)=\frac{6561}{5839232}\delta^2+O(\delta^3).
\tag{7}
\]

## 2. Credited square, unique base orbit, and a smooth majorant

The [spectral-square theorem](../angular-square-optimizer/PROOF.md),
source `98d5ab7db206bc1f0716968a154b18f97ab3cc25`, graph8541, gives
for \(R=2b-b^2/2\)
\[
V_b-J_R(\theta)=\sum_{i=1}^7
 \left[\rho_i-\frac17-b(\lambda_i^2-3/28)\right]^2.
\tag{8}
\]
It supplies the equality equation
\[
L_bf=\sigma_bf''-\beta_bzf'+8f=0,\quad
\sigma_b=\frac{4-3b}{224}+\frac b8z^2,\quad
\beta_b=1+\frac{7b}{8},
\tag{9}
\]
and the unique normalized equality polynomial for negative \(b\):
\[
f_b=z^8-\frac12z^6
 +\frac{15(4-3b)}{448(2-b)}z^4
 -\frac{15(4-3b)^2}{12544(2-b)(4-b)}z^2
 +\frac{15(4-3b)^3}{11239424(2-b)(4-b)}.
\tag{10}
\]
Uniqueness follows from the positive diagonal coefficient recurrence
when \(b<0\), and includes root collisions. Section 7 of the cited
lower angular theorem proves
\[
f_{-8/3}=(z^2-9/56)^3(z^2-1/56),\quad
X=61/392,\quad\eta=17/49.
\tag{11}
\]
Thus (8) gives exactly the unique global orbit at \(R_3\), with value
\(-763/441\). This isolated equality point is an input, not a new claim
in this source.

Near the labeled vector \(\theta_3\), the three compression eigenvalues
near \(0,\pm\sqrt{3/56}\) remain separated and simple. Their rank-one
projections and weights are real analytic functions of the real root
coordinates. Define their squared-weight sum as \(\eta_{\rm act}\), and
\[
J_R^+=RX-\eta_{\rm act}\ge J_R.
\tag{12}
\]
The other eigenvalues form two separated rank-two clusters near
\(\pm\sqrt{9/56}\). The full projections onto these clusters are
analytic even at their internal collisions. For example, each is the
resolvent integral over a fixed small circle enclosing only that cluster;
the matrix inverse is analytic and uniformly bounded on the circle.
At \(\theta_3\) both projected coupling vectors vanish. Consequently,
\[
\|\Pi_{\rm cluster}(\theta)w(\theta)\|=O(\|\theta-\theta_3\|).
\]
The total nonnegative weight in either cluster is therefore
\(O(\|\theta-\theta_3\|^2)\); the sum of its squared weights is bounded
by the square of that total. Uniformly in a neighborhood,
\[
0\le J_R^+(\theta)-J_R(\theta)
                       =O(\|\theta-\theta_3\|^4).
\tag{13}
\]
This argument uses full separated projections, not analytic eigenvectors
inside a colliding cluster. We do not assume global analyticity of \(J_R\).
Every nearby triple profile \(F_r\) attains the majorant because its two
repeated rank-two spaces have zero coupling.

For later compactness, \(\eta\) is continuous on all of \(\mathcal S\).
Indeed, at a simple limiting compression eigenvalue its projection is
continuous. At a repeated limiting eigenvalue the full limiting
eigenspace has zero coupling. The total weight of the converging cluster
therefore tends to zero, and its squared-weight sum tends to zero as well.
These separated-cluster arguments prove continuity even when several
simple weights coalesce. Hence \(J_R\) has a global maximum on
\(\mathcal S\), continuous uniformly in \(R\) on compact intervals.

## 3. Full tangent Hessian at the triple equality point

The tangent space is
\(T=\{v:\sum v_j=0,\ \theta_3\cdot v=0\}\), of dimension six.
Use the exact root chart
\[
\theta(u)=\frac{\theta_3+u}{\sqrt{1+\|u\|^2}},\qquad u\in T.
\tag{14}
\]
The base is stationary for \(J_{R_3}^+\): it maximizes \(J_{R_3}\), and
(13) makes the majorant's first-order variation the same. We will prove
\[
M(R_3)-J_{R_3}(\theta(sv))=s^2 Q(v)+O(s^3),
\tag{15}
\]
where the error is uniform on bounded tangent vectors and
\[
Q(v)=\frac{32}{21}\|v_s\|^2
          +\frac{16}{3}\|v_o\|^2
          +\frac{304}{21}\|v_e\|^2.
\tag{16}
\]
Here the following mutually orthogonal spaces span \(T\):

* \(V_s\), dimension four: sum-zero variations within either outer
  triple, with the inner coordinates zero.
* \(V_o\), dimension one: all six outer variations equal one, and both
  inner variations equal minus three.
* \(V_e\), dimension one: variations \(+1\) in the positive outer
  block, \(-1\) in the negative outer block, and \(-9,+9\) in the
  positive and negative inner coordinates.

Permutations within each outer block annihilate cross terms with its
sum-zero space and make its quadratic form scalar. Reflection exchanges
the two such spaces and makes their scalars equal. The symmetry given by
sign reversal followed by block exchange has opposite eigenvalues on
\(V_o,V_e\), so their cross term vanishes. Thus three scalar calculations
determine the complete tangent form; they are not merely a symmetric
slice test.

For a repeated space belonging to one outer block, the first-order
compression eigenvalue displacements are the eigenvalues of
\[
K=P_3\operatorname{diag}(v_{\rm block})P_3|_{\mathbf1^\perp},
\qquad P_3=I-\mathbf1\mathbf1^T/3.
\]
If \(A\) is the block sum and \(E\) its squared norm, expansion of the
trace gives exactly
\[
\operatorname{tr}K^2=\frac E3+\frac{A^2}{9}.
\tag{17}
\]
This also follows by writing \(P_3=I-\mathbf1\mathbf1^T/3\) in
\(\operatorname{tr}(D P_3 D P_3)\). At \(b=-8/3\), the equality
weight function in (8) is
\(h(\lambda)=3/7-(8/3)\lambda^2\). It vanishes at the repeated
eigenvalues, and \(h'(\pm\sqrt{9/56})^2=32/7\). Their coupling weights
are \(O(s^2)\) by Section 2. Thus their residual-square contribution at
order \(s^2\) is
\[
\frac{32}{7}\{\operatorname{tr}K_+^2+\operatorname{tr}K_-^2\}.
\tag{18}
\]
To justify (18) without individually analytic roots, use analytic block
reduction on each separated cluster. Its two eigenvalue changes divided
by \(s\) converge as a multiset to the eigenvalues of \(K\); the sum of
their squares converges to \(\operatorname{tr}K^2\). Multiple eigenvalues
inside \(K\) present no difficulty.

For the three active simple eigenvalues, if \(f\) has normalized
first variation \(h_f\), the linearized residual in (8) is
\[
-\frac{(L_{-8/3}h_f)(\lambda)}{g'(\lambda)},\qquad g=f'/8.
\tag{19}
\]
At any simple compression root the residual itself equals
\(-(L_bf)(\lambda)/g'(\lambda)\). At equality \(L_bf=0\)
identically, so the evaluation-point derivative disappears, proving
(19).

For compact exact calculations set \(y=\sqrt{56}z\),
\[
\widetilde F=(y^2-9)^3(y^2-1),\quad
\widetilde G=\widetilde F'/8,\quad
\widetilde L=(3-y^2/3)\partial_y^2+(4y/3)\partial_y+8.
\]
If scaled root velocities are the listed integer vectors, their physical
velocities are those vectors divided by \(\sqrt{56}\). The odd and even
first polynomial variations are respectively
\[
\widetilde h_o=-48y(y^2-9)^2,\qquad
\widetilde h_e=-144(y^2-9)^2.
\]
Equation (19) becomes \(-\widetilde L\widetilde h/(56\widetilde G')\).
At \(y=0,\pm\sqrt3\), its exact values are
\[
\begin{array}{c|ccc}
&0&+\sqrt3&-\sqrt3\\ \hline
o&0&4\sqrt3/7&-4\sqrt3/7\\
e&-40/7&16/7&16/7
\end{array}
\tag{20}
\]
Both integer block-constant vectors have repeated contribution
\((32/7)(4/56)=16/49\). The odd total loss is
\(16/49+96/49=16/7\), with physical squared norm \(24/56\).
The even total loss is \(16/49+1600/49+512/49=304/7\), with
physical squared norm \(168/56\). These give the second and third
coefficients in (16).

A split vector \((1,-1,0)\) in one outer block has zero first polynomial
variation, hence zero active residual to first order. Equation (18) gives
loss \((32/7)\,2/(3\cdot56)=8/147\), with squared norm \(2/56\).
Its quotient is \(32/21\). This proves (16). In particular the intrinsic
Hessian of the analytic majorant has eigenvalues
\[
-64/21\ (4\text{ times}),\quad -32/3,quad -608/21.
\tag{21}
\]
The Taylor expansion of the analytic majorant, together with (13), proves
the uniform form of (15). The split path realizes the smallest quotient,
and the finitely many permutation neighborhoods give (5).

## 4. Implicit function, symmetries, compactness, and stability

On a sufficiently small convex ball in the root chart (14), the Hessian
of \(J_R^+\) is uniformly negative definite for \(R\) near \(R_3\),
by (21) and continuity. The implicit-function theorem gives a unique
nearby analytic critical point \(\theta_R\), and strict concavity makes
it the unique maximum of the majorant in that chart.

Each permutation within an outer triple fixes \(\theta_3\), preserves
the chart and majorant, and hence fixes its unique critical point. Both
outer triples therefore stay constant. Sign reversal followed by the
fixed permutation exchanging the outer blocks and inner coordinates
also fixes the base and preserves the majorant; it therefore fixes the
critical point. Thus its outer blocks are opposite and its inner
coordinates are opposite. Norm one then makes its polynomial exactly
\(F_r\) with \(t=1/2-3r\), near \((r_3,t_3)\).

At that critical point \(J_R=J_R^+\). For every point in the chart,
\[
J_R(\theta)\le J_R^+(\theta)
             \le J_R^+(\theta_R)=J_R(\theta_R),
\tag{22}
\]
and the second inequality is strict away from \(\theta_R\). This proves
the unique local maximum for the original objective, without requiring
it to be smooth through every collision.

The global equality orbit at \(R_3\) is finite and unique by Section 2.
Outside small neighborhoods of that orbit, continuity and compactness
give a strictly positive value gap. Since
\(|J_R-J_{R_3}|\le |R-R_3|\sup_{\mathcal S}X\), every global maximizer
for nearby \(R\) belongs to those neighborhoods. Each is a permuted
copy of the chart just treated, with local maximum a permuted
\(\theta_R\). This proves the complete global statement of Theorem 1.

Strong concavity and (22) give, locally and uniformly,
\[
M(R)-J_R(\theta)\ge c_0\|u-u_R\|^2
                         \ge c_1\|\theta-\theta_R\|^2.
\]
The chart maps have uniformly bounded derivatives and inverses. Outside
the fixed chart neighborhoods the compactness gap stays uniformly
positive for a smaller parameter interval, while squared distances
on \(\mathcal S\) are bounded by four. Reducing the constant therefore
extends the local estimate to all of \(\mathcal S\), proving (4).

## 5. Exact branch and response

For \(F_r\), with \(v=3/8-2r\), direct differentiation gives
\[
g_r=F_r'/8=z(z^2-r)^2(z^2-v).
\]
The four repeated slots have zero weight. The three simple active
weights are
\[
p=\frac{8rt}{v}\quad\text{at }0,\qquad
\frac{1-p}{2}\quad\text{at each }\pm\sqrt v.
\tag{23}
\]
They follow from \(\rho=-8F_r(\lambda)/g_r'(\lambda)\), or from
the compression projection formula. Thus
\[
X(r)=24r^2-6r+\frac12,\qquad
\eta(r)=p^2+(1-p)^2/2.
\tag{24}
\]
Stationarity on this one-dimensional stratum gives
\(R=\eta'(r)/X'(r)=\mathcal R(r)\), exactly as in (2), and
\[
\mathcal R'(r)=-\frac{64(1088r^2-544r+57)}{(16r-3)^4},\quad
\mathcal R'(r_3)=\frac{119168}{27}>0.
\tag{25}
\]
Hence the critical branch of Section 4 is precisely the unique branch
in Theorem 1, and (3) follows.

The envelope derivative is \(M'(R)=X(r(R))\); consequently
\[
M(R_3)=-763/441,\quad M'(R_3)=61/392,\quad
M''(R_3)=\frac{X'(r_3)}{\mathcal R'(r_3)}=\frac{81}{208544}.
\]
This proves (6). At the equality point the square upper value and its
first derivative agree with \(M\), while
\[
\frac{d^2}{dR^2}V_{b(R)}\bigg|_{R_3}
 =\frac{15}{56(2-b_3)^3}=\frac{405}{153664}.
\]
Half the difference of the two second derivatives is
\(6561/5839232\), proving (7) on both sides.

## 6. A full local Hessian and an explicit local stability interval

This section is a local theorem for every \(1/8<r<1/6\); it does not
assert that such a profile is globally optimal. At \(R=\mathcal R(r)\),
the triple profile is stationary for the smooth majorant and therefore
for the second-order expansion of \(J_R\). To see full stationarity,
the block permutation symmetries kill all split components of the
gradient, reflection kills the odd hard component, and the remaining
even hard component is (25)'s one-variable stationary equation.

The same orthogonal tangent decomposition applies, with even hard space
now spanned by \(d\theta_r/dr\), of squared norm \(3/(4rt)\).
The three quadratic loss coefficients per squared norm are
\[
\begin{split}
q_s(r)&=-\frac{64r(8r-1)(6592r^2-2384r+213)}{3(16r-3)^3},\\
q_o(r)&=-\frac{(8r-1)P_5(r)}{8(16r-3)^5},\\
q_e(r)&=\frac{128r(6r-1)(8r-1)(1088r^2-544r+57)}{(16r-3)^4},
\end{split}
\tag{26}
\]
where
\[
P_5=21331968r^5+14127104r^4-10310656r^3
                         +1855104r^2-103176r-243.
\]
Thus positivity of all three gives a strict local maximum with quadratic
root stability. A negative coefficient gives an actual increasing real
root direction and rules out a local maximum. Zero cases are not decided
by this second-order criterion.

For reproducibility, here is an explicit derivation of (26). Write
\(A=z^2-r\), \(B=z^2-t\), \(F=A^3B\), and use the normalized chart
\((\theta+s v)/\sqrt{1+s^2\|v\|^2}\). For one outer split,
\(v=(1,-1,0)\), the first polynomial variation is zero. Reflection
and averaging give its second coefficient
\[
h_{s,2}=zF'-8F-A(z^2+r)B.
\tag{27}
\]
Before reflection averaging the last term is
\(-(z-\sqrt r)(z+\sqrt r)^3B\). The second objective coefficient is
linear in this polynomial coefficient since the first variation is zero;
reflection makes the averaged and original objective coefficients equal.
The fourth moment's second coefficient is \(12r-4X\).

For the odd hard velocity (outer entries one, inner entries minus three),
the unnormalized polynomial is
\([ (z-s)^2-r]^3[(z+3s)^2-t]\). Its normalized coefficients are
\[
\begin{split}
h_{o,1}&=6(t-r)zA^2,\\
h_{o,2}&=(3A^2+12z^2A)B-36z^2A^2+9A^3+12zF'-96F.
\end{split}
\tag{28}
\]
Its moment coefficient is \(36r+108t-48X\), and its squared velocity
norm is 24.

For either pair of coefficients \(F_s=F+s h_1+s^2 h_2+O(s^3)\), let
\(g=F'/8\), \(g_j=h_j'/8\). At an active root \(\lambda\) put
\[
\ell_1=-g_1/g',\qquad
\ell_2=-(g_2+g_1'\ell_1+g''\ell_1^2/2)/g'.
\]
All following evaluations are at \(\lambda\). Define
\[
N_0=F,\ N_1=h_1,\ N_2=h_2+h_1'\ell_1+F''\ell_1^2/2,
\]
\[
D_0=g',\ D_1=g_1'+g''\ell_1,\quad
D_2=g_2'+g_1''\ell_1+g''\ell_2+g'''\ell_1^2/2.
\]
The three weight coefficients are
\[
\begin{split}
\rho_0&=-8N_0/D_0,\\
\rho_1&=-8(N_1/D_0-N_0D_1/D_0^2),\\
\rho_2&=-8[N_2/D_0-N_1D_1/D_0^2
                    +N_0(D_1^2/D_0^3-D_2/D_0^2)].
\end{split}
\tag{29}
\]
Here \(N_1=h_1\) because \(F'(\lambda)=0\). The active \(\eta\)'s
second coefficient is the sum of \(\rho_1^2+2\rho_0\rho_2\) over
\(0,\pm\sqrt{3/8-2r}\). Subtracting \(R\) times the respective
moment coefficient and dividing by squared velocity norm gives
\(q_s,q_o\) in (26). These are checked as universal rational function
identities in \(\mathbb Q(r)[\mu]/(\mu^2-(3/8-2r))\), not fitted
at sample parameters. Finally the even hard direction follows directly:
\[
\frac{d^2}{dr^2}J_R(\theta_r)\bigg|_{R=\mathcal R(r)}
 =-X'(r)\mathcal R'(r),\qquad
q_e=4rt(8r-1)\mathcal R'(r),
\]
which is exactly the last formula in (26).

All three coefficients are strictly positive throughout the closed band
\[
\boxed{\frac{21}{136}\le r\le\frac{161}{1000}},\qquad
\boxed{-\frac{208}{9}\le R\le-\frac{1129232}{148877}}.
\tag{30}
\]
The second band is its increasing image under \(\mathcal R\).
For a complete sign certificate, transform \(r=l+(h-l)x\),
\(l=21/136,h=161/1000\), to Bernstein basis on \(0\le x\le1\).
The coefficient lists for the three required positive polynomials are
\[
\begin{array}{c|l}
6592r^2-2384r+213&594/289,\ 386/425,\ 738/15625\\
-1088r^2+544r-57&18/17,\ 218/125,\ 37218/15625\\
P_5&248832/1419857,\ 14093568/10440125,\ 155555328/76765625,\\
&260172544/112890625,\ 47655108608/20751953125,\
64853688576/30517578125
\end{array}
\tag{31}
\]
Every entry is positive and every Bernstein basis function is
nonnegative; the sum of those basis functions is one. The remaining
factors in (26) have the indicated strict signs throughout (30).
These full rational certificates prove local stability on the entire
band; they do not upgrade Theorem 1's global interval to (30).

## 7. A sharp comparison restricted to the symmetric triple family

Here allow the entire normalized real family \(0\le r\le1/6\), with
\(t=1/2-3r\). Formula (24) extends continuously through \(r=1/8\),
where the profile is four copies each of \(\pm1/\sqrt8\). At the
endpoints, the same formula follows by continuity. Denote that uniform
profile's objective by \(J_{\rm unif}=R/8-1\).

Direct rational identities give
\[
X(r)-1/8=\frac38(8r-1)^2,
\]
\[
\frac{1-\eta(r)}{X(r)-1/8}
 =\frac{4(3+80r-576r^2)}{(3-16r)^2},\qquad
\frac{208}{9}-\frac{4(3+80r-576r^2)}{(3-16r)^2}
 =\frac{4(136r-21)^2}{9(3-16r)^2}.
\tag{32}
\]
The quotient is understood by its continuous extension at \(r=1/8\).
Consequently this family satisfies the sharp inequality
\[
\boxed{\eta(r)\ge 1-\frac{208}{9}(X(r)-1/8)}.
\tag{33}
\]
The coefficient is sharp within the family: equality occurs at the
uniform profile and at \(r_*=21/136,t_*=5/136\), where \(X>1/8\).
Indeed the deficit in (33) is exactly
\[
\frac{(8r-1)^2(136r-21)^2}{6(3-16r)^2}.
\]
For every real \(R\),
\[
J_R(\theta_r)-J_{\rm unif}
 =\frac38(R+208/9)(8r-1)^2
  -\frac{(8r-1)^2(136r-21)^2}{6(3-16r)^2}.
\tag{34}
\]
Thus for \(R<-208/9\) the uniform profile strictly dominates every
nonuniform member of this family. At \(R_*=-208/9\) equality has
exactly the uniform and \(r_*\) profiles. At \(R>R_*\) the fixed
\(r_*\) profile already beats the uniform profile. Furthermore,
\(\mathcal R(r_*)=R_*\); this nonuniform equality profile is strictly
locally stable in the full sphere by (30).

The corresponding marked-radius comparison threshold is
\[
a_*=(3\sqrt{34}-16)/20,
\]
as substitution in (1) verifies. This is a sharp family comparison,
not a global classification on \(\mathcal S\). Whether (33) holds
universally is a separate unresolved frontier. No universal claim follows
from the equality profiles or these one-variable certificates.

## 8. Formal-square unattainability below the triple point

The lower angular theorem proves that (10) has four real and four
nonreal roots for \(-8/3<b<-8/5\). We now prove the same count on
\(-8<b<-8/3\), including the whole physical marked-radius range below
\(a_3\).

Let \(H_b(Y)=f_b(\sqrt Y)\), a monic quartic polynomial. At \(b_3=-8/3\)
it is \((Y-r_3)^3(Y-t_3)\). The inner simple factor remains analytic
and separated. Factor it out; in \(\xi=Y-r_3\), the other factor is
the monic cubic
\[
\xi^3+A(b)\xi^2+B(b)\xi+C(b),\qquad A(b_3)=B(b_3)=C(b_3)=0.
\]
Exact differentiation of (10) gives
\[
\partial_bH_b(r_3)|_{b_3}=\frac{2187}{172103680},\qquad
C'(b_3)=\frac{\partial_bH_b(r_3)|_{b_3}}{r_3-t_3}
                                 =\frac{2187}{24586240}.
\tag{35}
\]
In the cubic discriminant formula, the only quadratic-order term in
\(b-b_3\) is \(-27C(b)^2\). Therefore
\[
\operatorname{disc}=-\frac{129140163}{604483197337600}(b-b_3)^2
                                      +O((b-b_3)^3)<0
\tag{36}
\]
on both sufficiently small punctured sides. The cubic has one real root
and one nonreal conjugate pair; its real root stays positive, and the
separated inner root stays positive. Hence the degree-eight polynomial
has exactly four real and four nonreal roots on each such side.

To continue leftwards, (9) excludes a multiple root wherever
\(\sigma_b\ne0\): if \(f=f'=0\), the equation and its successive
derivatives force all derivatives to vanish, contradicting a nonzero
polynomial. At a zero of \(\sigma_b\), with
\(\ell_b^2=-(4-3b)/(28b)\), the credited exact evaluation is
\[
f_b(\pm\ell_b)=
 \frac{(4-3b)^3(7b+8)(5b+8)(3b+8)(b+8)}
 {78675968\,b^4(2-b)(4-b)}.
\tag{37}
\]
It is nonzero throughout \((-8,-8/3)\). The coefficients are analytic
there, so the real/nonreal root count cannot change; real roots could
leave or enter the real line only in a collision. This proves the count
on that entire interval.

For physical \(a=0\), \(R=-144/5\) and
\(b=2-\sqrt{308/5}>-8\); \(R(d)\) is increasing. Thus all
\(0\le a<a_3\) lie in the new obstruction interval. Combining this
with the already proved interval above \(a_3\) yields
\[
\boxed{\max_{\mathcal S}K_a<B_d+C_dV_{b(R(d))}
       \quad(0\le a<a_L,\ a\ne a_3)},
\quad a_L=\frac{10\sqrt{305}-105}{164}.
\tag{38}
\]
Equality at \(a_3\) has exactly the triple-pair orbit. The strict
inequality follows from equality uniqueness in (9), the nonreal-root
obstruction, and compactness. This is an obstruction to attaining the
formal angular bound, not a counterexample to first power.

## 9. Conditional first-power asymptotic consequence and check boundary

The credited [full-disk reduction, graph8212](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sharp_radius_global_minima/PROOF.md),
checked in [review8258](https://github.com/helgithorskarp/math_results/blob/main/sendov_sharp_global_radius_review3/REVIEW.md),
turns the new angular value into a fixed-energy disk asymptotic. For a
marked simple root \(a\) in Theorem 1's radius interval, define
\[
E=\sum_{j=1}^8|(a-z_j)^{-1}-(1+a)^{-1}|^2,\qquad
F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}
\]
with critical multiplicities. For the minimum at \(E=e\) the cited
reduction gives, with \(d=1+a\),
\[
F_{\min}(a,e)=\frac{16}{d}+d(a-5/8)e
             -[B_d+C_dM(R(d))]e^2+o(e^2).
\]
Normalized centered leading angular minimizing profiles approach
\(\mathcal O_{R(d)}\). The analytic disk reduction is an external
unformalized dependency of this corollary; it is not needed for
Theorems 1--3 or Sections 6--8.

`verify.py` checks 34 exact records using only standard-library rational
arithmetic. It derives universal active-weight second coefficients,
checks all three full tangent loss formulas, independently recomputes
the equality-point loss using the ODE residual and matrix traces, checks
the branch response, the full Bernstein sign certificates, the sharp
restricted comparison, and the cubic-discriminant leading coefficient.
Four damage controls reject invalid denominators and a reversed sign.
The fixture is compared explicitly under ordinary and optimized Python.

The analytic projection, implicit-function, symmetry, compactness,
stability, and continuation arguments are ordinary written mathematics
outside the verifier. No interval-arithmetic enumeration or floating
experiment establishes a theorem here. The global interval and uniform
global constant remain existential; the explicit band is only local,
and the \(208/9\) inequality is proved only for the stated family.
