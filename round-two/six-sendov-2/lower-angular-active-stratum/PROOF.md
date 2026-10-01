# A global angular optimizer below the first collision

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Ordinary written author proof, accompanied by exact rational checks.
Independent review is pending; the analytic argument is not formalized.

This extends the [spectral-square angular theorem](../angular-square-optimizer/PROOF.md)
(source commit `98d5ab7db206bc1f0716968a154b18f97ab3cc25`, graph8541).
The stronger degree-nine first-power conjecture remains open. The present
claim is an angular optimizer and stability result, with an existential
parameter interval. It does not identify an actual finite-energy minimizer.

## 1. Statement and precise scope

Use the normalized slope sphere
\[
\mathcal S=\{\theta\in\mathbb R^8:\ \sum\theta_j=0,
                                         \ \sum\theta_j^2=1\}.
\]
Let \(e=\mathbf1/\sqrt8\), \(P=I-ee^T\),
\(H=P\operatorname{diag}(\theta)P|_{e^\perp}\), and
\(w=\operatorname{diag}(\theta)e\). Put
\[
X=\sum\theta_j^4,\qquad
\eta=64\sum_{\lambda\text{ distinct}}\|\Pi_\lambda w\|^4,
\qquad J_R=RX-\eta.
\]
All projections refer to full eigenspaces. Repeated eigenspaces have zero
coupling; this convention includes all collisions. List seven compression
eigenvalues with multiplicity, with weights
\(\rho_i=8\|\Pi_iw\|^2\) at simple eigenvalues and zero in repeated slots.

The marked-radius angular functional is the credited
\[
K_a=B_d+C_dJ_{R(d)},\qquad d=1+a,
\]
\[
B_d=\frac{d^3(16d^2-104d+203)}{8192},\quad
C_d=\frac{d^3(4d+1)^2}{8192},\quad
R(d)=\frac{16(48d^2-40d-53)}{(4d+1)^2}.
\]
These definitions and the collision-uniform first-power reduction are
credited to [graph8160](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_moving_pair_comparison_boundary/PROOF.md)
and [review8230](https://github.com/helgithorskarp/math_results/blob/main/sendov_moving_pair_threshold_review3/REVIEW.md).
Put
\[
R_L=-\frac{112}{25},\quad b_L=-\frac85,\quad
a_L=\frac{10\sqrt{305}-105}{164},\quad \delta=R-R_L.
\]

**Theorem 1 (a complete active stratum).** There is \(\epsilon>0\) and
unique real analytic functions \(r(R),t(R)\), defined near \(R_L\), such that
for every \(R\in[R_L-\epsilon,R_L]\) the complete global maximizing orbit
of \(J_R\) on \(\mathcal S\) consists of the permutations of the roots of
\[
F_{r,t}(z)=(z^2-r)^2
                 [z^4-(1/2-2r)z^2+t].                         \tag{1}
\]
They have two double outer slopes and four simple inner slopes. The orbit
is invariant under simultaneous sign reversal. The functions are specified
uniquely by the stationary equations for the exact rational objective in
Section 5, together with
\[
\begin{split}
r(R)&=\frac{11}{56}+\frac{25}{6048}\delta+O(\delta^2),\\
t(R)&=\frac{11}{9408}-\frac{25}{124416}\delta+O(\delta^2).
\end{split}                                                    \tag{2}
\]
In particular, with \(M(R)=\max_{\mathcal S}J_R\),
\[
\boxed{M(R)=-\frac{177}{175}+\frac{29}{168}\delta
                  +\frac{5725}{3048192}\delta^2+O(\delta^3).}    \tag{3}
\]
Uniqueness is local for the stationary functions and global for the
maximizing root orbit on this interval. No explicit positive value of
\(\epsilon\) is established.

For \(b(R)=2-\sqrt{4-2R}\) let
\[
V_b=\frac{13R}{56}-\frac17+\frac{15b^2}{224}.
\]
The unattained formal-square upper value has the precise gap
\[
\boxed{V_{b(R)}-M(R)
             =\frac{3025}{3048192}\delta^2+O(\delta^3).}         \tag{4}
\]
Since \(R'(d)=2048(2d+3)/(4d+1)^3>0\), these conclusions give a
nonzero marked-radius interval immediately to the left of \(a_L\).

**Theorem 2 (collision stability).** After decreasing \(\epsilon\), there
is \(c>0\) such that for all \(R\in[R_L-\epsilon,R_L]\) and
\(\theta\in\mathcal S\),
\[
\boxed{M(R)-J_R(\theta)\ge c\{(R_L-R)
        \operatorname{dist}(\theta,\mathcal O_R)^2
                         +\operatorname{dist}(\theta,\mathcal O_R)^4\}.} \tag{5}
\]
Here \(\mathcal O_R\) is the orbit in Theorem 1. At \(R=R_L\) the
fourth power is sharp: there are normalized real slopes with distance
comparable to \(s\) and loss comparable to \(s^4\). The constants are
existential. Multiplication by \(C_d>0\) transfers the bound to \(K_a\).

Section 7 also proves an isolated equality point at
\(a_3=(3\sqrt{29}-11)/16\) and strict failure of square attainability on
the entire intervening interval \((a_3,a_L)\). Theorem 1 evaluates only
an unspecified nonzero portion adjacent to \(a_L\).

## 2. The square in a full coefficient neighborhood

The cited spectral-square theorem gives, for \(R=2b-b^2/2\),
\[
V_b-J_R(\theta)=\sum_{i=1}^7 E_i^2,
\quad E_i=\rho_i-\frac17-b(\lambda_i^2-3/28).             \tag{6}
\]
Its equality polynomial is
\[
f_b=z^8-\frac12z^6+
 \frac{15(4-3b)}{448(2-b)}z^4
-\frac{15(4-3b)^2}{12544(2-b)(4-b)}z^2
+\frac{15(4-3b)^3}{11239424(2-b)(4-b)}.                 \tag{7}
\]
It solves
\[
L_b f=\sigma_b f''-\beta_b zf'+8f=0,
\quad \sigma_b=\frac{4-3b}{224}+\frac b8z^2,
\quad\beta_b=1+\frac{7b}{8}.                          \tag{8}
\]
At \(b_L\), it is
\[
f_L=(z^2-11/56)^2(z^4-3z^2/28+11/9408).               \tag{9}
\]
Its derivative compression polynomial is
\[
g_L=f_L'/8=z(z^2-11/56)(z^4-5z^2/28+55/9408).         \tag{10}
\]
The seven roots of \(g_L\) are real and simple. The last quadratic in
\(y=z^2\) has discriminant \(5/588>0\) and positive roots; its value
at \(11/56\) is \(11/1176>0\), so no roots coincide. The four inner
roots of (9) are also real, simple and separated from the outer ones.

Consider all real normalized monic coefficient vectors near \(f_L\):
\[
f(z)=z^8-\tfrac12z^6+c_3z^5+c_4z^4+\cdots+c_8.
\]
They need not have real roots. Nevertheless \(g=f'/8\) retains seven
simple real roots \(\lambda_i\) locally. Define analytically
\[
\rho_i=-\frac{8f(\lambda_i)}{g'(\lambda_i)},\quad
X=\frac12-4c_4,\quad \eta=\sum\rho_i^2.               \tag{11}
\]
For real-rooted \(f\) these are precisely the compression quantities.
For the other coefficient vectors (11) is only an analytic extension;
some weights may be negative. Partial fractions give
\[
f/g=z-\frac18\sum_i\frac{\rho_i}{z-\lambda_i}.
\]
Coefficient comparison at infinity and Newton sums give
\[
\sum\rho_i=1,\quad\sum\rho_i\lambda_i^2=X-1/8,
\quad\sum\lambda_i^2=3/4,
\quad\sum\lambda_i^4=X/2+1/32.
\]
Thus exactly the same expansion of squares proves (6) throughout this
coefficient neighborhood. No assumption of positive extended weights is
used in this step.

At the equality polynomial, a normalized coefficient variation \(h\)
has degree at most five. Differentiating the residual at a root of \(g\)
gives
\[
\boxed{D_f E_i[h]=-(L_bh)(\lambda_i)/g'(\lambda_i).}    \tag{12}
\]
Indeed at any root of \(g\) the residual is \(-(L_b f)/g'\); at equality
\(L_bf\) vanishes identically, so its evaluation-point derivative vanishes.

At \(b_L\), the diagonal coefficient of \(L_b\) on \(z^m\),
\(0\le m\le5\), is
\[
\frac{(8-m)(5+m)}5>0.
\]
Its remaining term lowers degree by two. Hence \(L_{b_L}\) is invertible
on polynomials of degree at most five. Evaluation at the seven distinct
roots of \(g_L\) is injective on that space. Consequently (12) is
injective and the Hessian of \(J_{R_L}\) in the six free coefficients is
strictly negative definite, namely \(-2(DE)^T(DE)\).

## 3. Real-rootedness becomes two sign constraints

Factor any nearby normalized real polynomial into the separated clusters
of (9):
\[
f=[(z-c_+)^2-u_+][(z-c_-)^2-u_-]\prod_{k=1}^4(z-x_k). \tag{13}
\]
The centers, \(u_\pm\), and the labeled inner simple roots are real analytic
functions of the real coefficients. To justify this without choosing
square roots, separate the six coprime factors in (9). The derivative of
their multiplication map is invertible: reducing a zero product variation
modulo each factor forces that factor's variation to vanish. The analytic
implicit function theorem supplies the factorization. Each quadratic's
linear coefficient and constant term give its center and \(u\).

Balance and the squared-norm normalization become
\[
2c_++2c_-+\sum x_k=0,
\]
\[
2c_+^2+2c_-^2+2u_++2u_-+\sum x_k^2=1.               \tag{14}
\]
The two gradients in the six center/simple-root variables have rank two,
because their values are not all equal. Four local free variables \(h\),
together with \(u_+,u_-\), therefore give analytic coordinates on the
normalized coefficient manifold. In these coordinates
\[
f\text{ has eight real roots}\quad\Longleftrightarrow\quad
u_+\ge0,\ u_-\ge0.                                   \tag{15}
\]
The inner roots remain simple and real throughout this neighborhood.

Because the coefficient gradient vanishes at the endpoint, the Hessian
remains strictly negative definite after this change of coordinates.
Choose a small convex coordinate box and \(R\) near \(R_L\) on which this
negative definiteness persists. For each \((R,u_+,u_-)\), the equation
\(\partial_h J_R=0\) has a unique nearby analytic solution
\(h=h_*(R,u_+,u_-)\). Its reduced value
\[
Q_R(u_+,u_-)=J_R(h_*(R,u),u)
\]
has strictly negative definite Hessian in \(u\), by the Schur complement.
Changing every slope's sign exchanges \(u_+\) and \(u_-\), and preserves
the objective and the fibers in (13). Local uniqueness of \(h_*\) therefore
gives
\[
Q_R(u_+,u_-)=Q_R(u_-,u_+).                            \tag{16}
\]
This equality is independent of the arbitrary choice of four coordinates.

We now determine the sign of the boundary gradient. The unconstrained
stationary polynomial is \(f_{b(R)}\): (6), (7) show stationarity and
the local negative Hessian proves uniqueness. Its two cluster variables
are equal. Write \(f_b(z)=H_b(z^2)\), \(r_L=11/56\). Exact differentiation
of (7) gives
\[
\partial_b H_b(r_L)|_{b_L}=-\frac{6655}{309786624},
\qquad H_{b_L}''(r_L)=\frac{11}{294}.                 \tag{17}
\]
At a double positive root, its quadratic splitting variable satisfies
\[
u_b'=-\frac{\partial_bH_b(r_L)}{2r_LH_{b_L}''(r_L)}
          =\frac{55}{37632}.
\]
For example, evaluating (13) at the fixed double root eliminates the
center displacement to first order, and the remaining factor is
\(f_L''(\sqrt{r_L})/2=2r_LH_{b_L}''(r_L)\). Since
\(b'(R_L)=5/18\), both unconstrained splitting variables have expansion
\[
u_b(R)=k\delta+O(\delta^2),\qquad k=\frac{275}{677376}>0.         \tag{18}
\]

Let \(S=D_u^2 Q_{R_L}(0)\). It is negative definite, and (16) makes
its two row sums equal to a strictly negative number \(s\): the vector
\((1,1)\) has eigenvalue \(s<0\). Expanding
\(\nabla Q_R(u_b(R),u_b(R))=0\) gives
\[
\nabla Q_R(0)=-k s\delta(1,1)+O(\delta^2).             \tag{19}
\]
Both components are strictly negative for small \(\delta<0\). Strict
concavity and (15) therefore force the unique nearby constrained maximum
to be \(u_+=u_-=0\). At \(\delta=0\) the same conclusion follows from
the negative Hessian and zero gradient. This proves persistence of both
double pairs, without presupposing a symmetry of the global optimizer.

## 4. Why the local result is a global theorem

The function \(\eta\) is continuous on \(\mathcal S\), including collisions.
At a simple compression eigenvalue this follows from continuous spectral
projections. At a repeated eigenvalue the limiting coupling is zero: the
sum of the nonnegative weights in a coalescing cluster tends to zero,
so the sum of their squares does too. This also verifies continuity with
the full-eigenspace convention. Thus \(J_R\) is jointly continuous on the
compact sphere and on bounded parameter intervals.

At \(R_L\), the cited equality/ODE uniqueness result makes the root
multiset (9) the unique maximizing orbit. On the complement of any fixed
neighborhood of that orbit, the angular loss has a strictly positive
minimum. Joint continuity keeps that gap positive for all sufficiently
nearby \(R\). Hence every global maximizer lies in the factorization
neighborhood of Section 3, where its root multiset is the unique constrained
maximum. This supplies the global assertion and excludes asymmetric or
additional distant maximizing strata on this interval.

The constrained stationary polynomial at \(u_+=u_-=0\) is even by
reflection and uniqueness. Its double roots are \(\pm\sqrt r\); the four
simple roots form two inner opposite pairs. Balance and norm force exactly
the form (1). Analyticity of the constrained stationary solution gives
analytic \(r(R),t(R)\). Stationarity in \(r,t\) uniquely characterizes the
nearby even branch, since its two-dimensional Hessian is nonsingular.

## 5. The rational objective, response, and strict gap

For (1), put
\[
s=1/2-2r,\quad u=3/8-r,\quad v=t/2+r/8-r^2/2,
\quad X=12r^2-4r+1/2-4t.
\]
Direct differentiation gives
\[
g=F_{r,t}'/8=z(z^2-r)(z^4-uz^2+v).                  \tag{20}
\]
The two compression slots at \(\pm\sqrt r\) have zero weights. The
remaining eigenvalues are zero and two opposite pairs whose squares
\(y_1,y_2\) have sum \(u\) and product \(v\). Define
\[
p=\rho_0=\frac{8rt}{v},\qquad N=1-p,\qquad M=X-1/8.
\]
The value of \(p\) follows from the residue of \(F/g\) at zero. If the
weights at the positive and negative members of pair \(j\) equal \(q_j\),
the moment constraints are
\[
q_1+q_2=N/2,\qquad q_1y_1+q_2y_2=M/2.
\]
Solving these two equations and squaring proves the exact formula
\[
\boxed{\eta(r,t)=p^2+
 \frac{2M^2-2MNu+N^2(u^2-2v)}{2(u^2-4v)},\qquad
J_R(r,t)=RX(r,t)-\eta(r,t).}                         \tag{21}
\]
All denominators are nonzero in a neighborhood of
\((r_L,t_L)=(11/56,11/9408)\). The four inner roots remain simple and
strictly inside the double outer roots there.

The defining stationary equations are
\[
R(24r-4)=\partial_r\eta(r,t),\qquad
-4R=\partial_t\eta(r,t).                            \tag{22}
\]
At the endpoint they hold exactly, and the Hessian of (21) is
\[
\mathcal H=-\frac1{125}
\begin{pmatrix}73344&1064448\\1064448&24385536\end{pmatrix},
\quad \det\mathcal H=\frac{131096641536}{3125}>0.      \tag{23}
\]
With \(\nabla X=(24r_L-4,-4)^T\), implicit differentiation gives
\[
\binom{r'}{t'}=-\mathcal H^{-1}\nabla X
          =\binom{25/6048}{-25/124416},
\qquad X'(R_L)=\frac{5725}{1524096}.                 \tag{24}
\]
Since \(M'(R)=X(R)\), while \(X(R_L)=29/168\) and
\(M(R_L)=-177/175\), equations (3) follow.

For the unconstrained equality branch, Newton sums of (7) give
\[
X_b=\frac{52-11b}{112(2-b)},\qquad
\frac{dX_b}{dR}\bigg|_{R_L}=\frac{625}{108864}.
\]
The formal value \(V_b\) has derivative \(X_b\), as either differentiation
or (6) at stationarity shows. Its constant and first derivative agree
with the constrained value. Therefore their quadratic difference is
\[
\frac12\left(\frac{625}{108864}-\frac{5725}{1524096}\right)
                  =\frac{3025}{3048192},
\]
proving (4). An additional exact check of the splitting gradient gives
\(\partial_{u_\pm}Q_R(0)=(22/9)\delta+O(\delta^2)\), consistent
with the sign argument (19); the proof needs only its positive slope.

## 6. Stability and its endpoint order

On a smaller coordinate box, the Hessians in Section 3 are uniformly
negative definite. Equations (19) and (18) give, for \(\delta\le0\),
\[
\begin{split}
M(R)-J_R(h,u)\ge c_1\big(&\|h-h_*(R,u)\|^2\\
                 &+|\delta|(u_++u_-)+u_+^2+u_-^2\big),
\qquad u_\pm\ge0.                                  \tag{25}
\end{split}
\]
Indeed strong concavity in \(h\) supplies the first term. Taylor's
theorem for the reduced strictly concave function supplies the last
terms and the negative boundary gradient supplies the linear term in
the nonnegative \(u\)'s. These are uniform bounds after shrinking the box.

Label roots by their separated clusters and use their increasing order
within each pair. Root distance to the constrained orbit satisfies
\[
d_R^2\le C\{\|h-h_*(R,u)\|^2+u_++u_-\}.             \tag{26}
\]
The reason is direct: the double pair's two displacements contribute its
center displacement squared and \(2u\); all centers and inner roots are
analytic in \(h,u\); and \(h_*(R,u)-h_*(R,0)=O(\|u\|)\) uniformly.
The fourth power of (26) is bounded by a constant times
\(\|h-h_*\|^2+u_+^2+u_-^2\) on this bounded box. Thus (25) implies
(5) locally. The positive compactness gap in Section 4 extends it
globally with one smaller uniform constant.

For sharpness at \(R_L\), split one double pair into its center plus
\(s\) and minus \(s\), leave the other entries fixed, and divide all
slopes by \(\sqrt{1+2s^2}\). Balance and norm hold exactly, distance
to the original orbit is comparable to \(|s|\), and the coefficient
variation is \(O(s^2)\). The square (6) gives loss \(O(s^4)\), and (5)
gives a positive matching lower order. Hence a quadratic root-distance
bound with a positive endpoint constant is impossible.

## 7. The further equality point and intervening obstruction

At \(b_3=-8/3\), (7) factors exactly as
\[
f_{b_3}=(z^2-9/56)^3(z^2-1/56).                      \tag{27}
\]
This is a real balanced norm-one profile. Its compression weights are
\(3/7\) at zero, \(2/7\) at each of \(\pm\sqrt{3/56}\), and zero
in the two-dimensional spaces at \(\pm\sqrt{9/56}\). Thus
\[
X=61/392,\quad \eta=17/49,\quad R_{b_3}=-80/9.
\]
They match the equality weights in (6). The ODE coefficient recurrence
\[
k(1-b(8-k)/8)c_k+
 \frac{4-3b}{224}(10-k)(9-k)c_{k-2}=0,
\quad c_0=1,c_1=0,c_2=-1/2,
\]
has positive diagonal for \(3\le k\le8\) whenever \(b<0\). Thus equality
has exactly this root permutation orbit at \(R=-80/9\). The corresponding
marked radius is \(a_3=(3\sqrt{29}-11)/16\).

For \(-8/3<b<-8/5\), the formal equality polynomial has precisely four
real roots and four nonreal roots. Here is a complete continuation check.
At \(b_L\), the double root of \(H_b(y)\) at \(y=11/56\) has a separated
analytic quadratic factor. Its discriminant derivative from (17) is
\[
-8\,\partial_bH_b(11/56)/H_{b_L}''(11/56)
                      =605/131712>0.
\]
Thus just below \(b_L\) two positive \(y\) roots become a nonreal conjugate
pair; the other two stay real and positive. This gives the asserted
four-real/four-nonreal count locally.

The ODE excludes a multiple complex root wherever \(\sigma_b\ne0\):
successive differentiation would force every polynomial derivative at
the root to vanish. At the two zeros of \(\sigma_b\), whose squares are
\(\ell_b^2=-(4-3b)/(28b)\), the exact evaluation is
\[
f_b(\pm\ell_b)=
\frac{(4-3b)^3(7b+8)(5b+8)(3b+8)(b+8)}
     {78675968\,b^4(2-b)(4-b)}.                      \tag{28}
\]
None of its numerator factors vanishes in the open interval under
consideration. All coefficients are analytic there. Hence no root can
cross between real and nonreal without a collision, and the root count
continues throughout that interval.

Equality in (6) forces the unique polynomial (7), including at collisions,
so no real normalized slope vector attains the formal upper value there.
Compactness makes this an actual strict inequality:
\[
\max_{\mathcal S}K_a < B_d+C_dV_{b(R(d))},
                       \qquad a_3<a<a_L.             \tag{29}
\]
Theorem 1 and (4) quantify the gap only near the right endpoint.

## 8. First-power consequence and trust boundary

The prior [full-disk angular reduction, graph8212](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sharp_radius_global_minima/PROOF.md),
independently checked in [review8258](https://github.com/helgithorskarp/math_results/blob/main/sendov_sharp_global_radius_review3/REVIEW.md),
transfers the angular maximum to the leading fixed-energy disk minimum.
For marked simple \(a\) in the radius interval of Theorem 1, put
\[
E=\sum_{j=1}^8 |(a-z_j)^{-1}-(1+a)^{-1}|^2,\qquad
F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},
\]
with all critical multiplicities, and let \(F_{\min}(a,e)\) denote the
minimum among disk-root polynomials with \(E=e\). With \(d=1+a\), the
cited reduction gives
\[
F_{\min}(a,e)=\frac{16}{d}+d(a-5/8)e
                -[B_d+C_dM(R(d))]e^2+o(e^2).
\]
This is a consequence conditional on the cited reduction, whose analytic
proof is not repeated here. Normalized centered small-phase minimizers
approach the orbit (1). This is a leading asymptotic assertion, not a
finite-energy stationary-family classification or a proof of first power.

`verify.py` checks the exact polynomial, moment, stationary-response and
splitting calculations in rational arithmetic. Its independent trace
calculation uses residues at all seven compression roots without floating
root approximation. The implicit-function, concavity, compactness,
real-root continuity and stability arguments above are ordinary written
mathematics outside the checker. Interval length and stability constants
are not computed. No numerical scan establishes a mathematical claim here.
