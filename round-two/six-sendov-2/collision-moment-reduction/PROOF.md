# Actual original-collision values, splitting signs and triple curvature

Actual author **six-sendov-2**, role **researcher**, 2026-10-03.
Complete ordinary author proof; **unformalized and independently unreviewed**.
This is real-original-root angular mathematics auxiliary to degree-nine
complex first-power Tang--Zhang. The classical compression, interpolation,
least-squares and Sherman--Morrison mechanisms retain their credit.

## 1. Actual domain and statements

Let eight real original coordinates have sum zero and squared norm one,
with original power sums mu3=mu5=0. Their entire octic chart is

\[
 f(z)=z^8-z^6/2+2Ez^4+4Gz^2+8Jz+c,\qquad
 h=f'/8=z^7-3z^5/8+Ez^3+Gz+J.                    \tag{1}
\]

For H=P diag(u) P on the orthogonal complement of the constant vector,
use **full** eigenspace masses m_lambda=||Pi_lambda u||², eta=sum m_lambda²
and D=mu4-1/8=3/8-8E. Set C=(1-eta)/D. This is the credited functional of
[7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md).
Repeated eigenspaces are always grouped. The charts below have D>0.
The previously proved [10105 collision reduction](../two-moment-parity-descent/PROOF.md)
puts every constrained maximum on an original collision; the present
result supplies actual boundary values and necessary conditions.

Choose a real original root x of multiplicity at least two. Exactly

\[
\begin{split}
 J&=-x^7+3x^5/8-Ex^3-Gx,\\
 c&=7x^8-5x^6/2+6Ex^4+4Gx^2,\\
 f&=(z-x)^2 Q(z),\qquad h=(z-x)r(z),                 \tag{2}
\end{split}
\]

where the **entire** remaining original sextic is

\[
\begin{split}
 Q(z)={}&z^6+2xz^5+(3x^2-1/2)z^4+(4x^3-x)z^3\\
 &+(5x^4-3x^2/2+2E)z^2+(6x^5-2x^3+4Ex)z\\
 &+7x^6-5x^4/2+6Ex^2+4G,                         \tag{3}\\
 r(z)={}&z^6+xz^5+(x^2-3/8)z^4+(x^3-3x/8)z^3\\
 &+(x^4-3x^2/8+E)z^2+(x^5-3x^3/8+Ex)z\\
 &+x^6-3x^4/8+Ex^2+G.                            \tag{4}
\end{split}
\]

**Actual feasibility is x real and all six Q roots real, with
multiplicity.** Assume additionally that r has six distinct real roots.
This covers an exact single double and an exact single triple, and some
additional double collisions. It excludes fourfold x and triples at a
second original level; they require further cancellation. A real r
spectrum alone does not certify real Q roots.

Put v(t)=(1,t,...,t^5)^T, tau_k=sum of the seven h roots to power k
**counting multiplicity**, tau0=7, and

\[
 K_{ik}=\tau_{i+k}-x^{i+k},\quad 0\le i,k\le5,\qquad
 \nu=(1,0,D,0,9/64-4E-24G,-56J)^T.                 \tag{5}
\]

**Theorem A (actual six-node value and full boundary gradient).**
K is positive definite and the actual grouped angular value is

\[
 \beta=K^{-1}\nu,\quad R=\nu^T K^{-1}\nu=\eta,
 \qquad \boxed{C=(1-R)/D}.                         \tag{6}
\]

For theta=x,E,G, use **total** derivatives after (2):

\[
 R_\theta=2\beta^T\nu_\theta-\beta^T K_\theta\beta,
 \quad C_x=-R_x/D,\quad C_G=-R_G/D,
 \quad C_E=(8C-R_E)/D.                             \tag{7}
\]

Equations (2),(4),(5) and monic Newton recurrence specify every entry
and its derivative without root isolation or an expanded rational
elimination. In particular critical nodes are not held fixed.

Define the algebraic projection comparison

\[
 M=K+v(x)v(x)^T=(\tau_{i+k}),\quad
 \beta_* =M^{-1}\nu,\quad p_*(t)=v(t)^T\beta_*,
 \quad R_6=\nu^T M^{-1}\nu,\quad \bar C=(1-R_6)/D,
\]
\[
 L_x=1-v(x)^T M^{-1}v(x)>0,\qquad T=p_*(x)^2/L_x.    \tag{8}
\]

**Theorem B (exact collision cost and strengthened skew penalty).**
For every actual profile in the stated r domain,

\[
 \boxed{\eta=R_6+T,\qquad C=\bar C(E,G,J)-T/D}.       \tag{9}
\]

If J is nonzero, the parity estimate of10105 extends to this domain and

\[
 \boxed{C<\bar C(E,G,0)-56J^2-T/D}.                \tag{10}
\]

The right-hand comparison is algebraic and unconstrained. It is not
an actual even-root maximum. At J=0 the identity (9) still holds.

**Theorem C (single-double local-maximum obstruction).** Suppose Q
is squarefree and Q(x) is nonzero, so x is the only original collision.
For t>=0 small, the primitive f_t=f-t Q(x) has eight distinct real
original roots and retains both zero odd moments. Its one-sided derivative
is

\[
 \boxed{\left.{dC(f_t)\over dt}\right|_{0+}
                ={64p_*(x)\over D L_x}.}            \tag{11}
\]

Thus p_*(x)>0 excludes a local maximum. If J is nonzero, every local
maximum on the full actual two-moment-zero locus with this single-double
pattern must satisfy **p_*(x)<0**, not merely <=0. It also must satisfy all
three stationary equations (7). On the local fixed-E,G double-root
branch, parameterized by J, its normalized collision cost Phi=T/D obeys

\[
 \boxed{J\,{d\Phi\over dJ}=-2J^2H/D<-112J^2,
 \quad H>196(D+1/14)^2.}                            \tag{12}
\]

This is a necessary compensation by the collision cost, not an
existence or sufficiency statement or a global feasible continuation.

**Theorem D (exact triple-root curvature).** Suppose Q is squarefree
and Q(x)=0. Then x has multiplicity exactly three and all other five
originals are simple. The full h has a repeated critical root x; r still
has six distinct real roots. In the legal three-parameter chart (2),

\[
 p_*(x)=0,\quad T=0,\quad L_x=1/2,\quad C_x=0,
\]
\[
 \boxed{C_{xx}={2J h''(x)H-4p_*'(x)^2\over D}.}       \tag{13}
\]

A local maximum therefore must have C_E=C_G=0 and
J h''(x)H<=2p_*'(x)^2. This gives a computable second-order obstruction
at an actual repeated critical point. No universal sign of (13) is
claimed. The two exact triple controls below have positive curvature,
and hence are specifically excluded as local maxima.

## 2. Full compression resolvent, including zero-mass eigenspaces

Here is a definition-level justification that avoids simple-h residues
at a repeated critical point. Let e be the normalized constant vector
and A=diag(u). Relative to e plus e-perp, A has blocks 0,u^T/sqrt8,u/sqrt8,H.
The Schur complement identity for sufficiently large real z gives

\[
 {1\over8}\sum_i{1\over z-u_i}
 ={1\over z-\frac18 u^T(z-H)^{-1}u}.
\]

Since sum_i1/(z-u_i)=f'/f=8h/f, this proves the rational identity

\[
 u^T(z-H)^{-1}u
 =8\left(z-{f(z)\over h(z)}\right)
 =8\left(z-{(z-x)Q(z)\over r(z)}\right).             \tag{14}
\]

At an original level a with multiplicity n>=2, the supported zero-sum
space has dimension n-1, eigenvalue a, and is perpendicular to u. It
has **zero full mass**. The complementary active eigenvalues are the
simple interlacing zeros of sum_i1/(z-u_i); its derivative is strictly
negative between distinct original levels. Thus no active eigenvalue
coincides with an original level.

Because r is squarefree, (14) has only simple possible poles at its
six roots lambda. The corresponding actual masses, allowing zeros, are

\[
 m_\lambda=-{8(\lambda-x)Q(\lambda)\over r'(\lambda)}.
                                                               \tag{15}
\]

Any original eigenvalue removed or counted once rather than twice in
r has zero full mass. Consequently the sum of the six squared masses
in (15) equals the actual **grouped** eta, including at a triple x.
No inverse of h'(x)=0 is used there.

Expanding (14) at infinity gives exactly the six moments nu in (5).
The canceled numerator 8[zr-(z-x)Q] has degree five. If V has columns
v(lambda) over the six distinct r roots, then V is invertible,
Vm=nu and K=VV^T. Therefore m=V^T K^{-1}nu and
eta=m^Tm=nu^T K^{-1}nu. This proves (6), positivity of K and (7)
by ordinary differentiation of a matrix inverse. It also proves D>0:
D=0 would force every original square to equal1/8, leaving only two
original levels and no six-distinct-r spectrum.

## 3. Rank-one loss and the endpoint parity comparison

M=K+v(x)v(x)^T is positive definite. Sherman--Morrison, or direct
multiplication by this rank-one update, gives

\[
 L_x={1\over1+v(x)^T K^{-1}v(x)}>0,\quad
 \nu^T K^{-1}\nu=\nu^T M^{-1}\nu+p_*(x)^2/L_x.
                                                               \tag{16}
\]

This proves (9). The factor L_x is essential; a cost p_*(x)^2 alone
would be incorrect.

For clarity the credited parity estimate of10105 remains valid at the
present endpoint. In power order (0,2,4;1,3,5), write

\[
 M=\begin{pmatrix}A&JU\\JU^T&B\end{pmatrix},\quad
 \nu=\binom u{Jv_0},\quad
 U=\begin{pmatrix}0&0&0\\0&0&-7\\0&-7&-27/8\end{pmatrix},
\]

where A,B,u,v0 are the exact even blocks and moments specified in10105.
They are independent of J. Set

\[
 y=A^{-1}u,\quad w=v_0-U^Ty,\quad W=U^TA^{-1}U,\quad
 S=B-J^2W,\quad H=w^TS^{-1}BS^{-1}w.
\]

M positive definite implies S positive definite, and exact Schur
elimination gives R6_J=2JH. The uniform estimate
H>196(D+1/14)^2 uses only M positive definiteness, real h traces counted
with multiplicity, tau2=3/4 and D>0. These premises all hold here even
when h has one double root. In particular the strict q-norm bound,
nonzero mismatch q.w=-3(D+1/14), and trace bound Bop<=9/4 in10105
are unchanged; no distinctness of all seven h entries is used in them.
Thus barC_J=-2JH/D holds for the algebraic comparison on its open
positive-definite matrix domain, including the repeated-h endpoint.

The h of our domain has either seven simple real roots or exactly
one double root and five other simple roots. Rolle's theorem in either
case gives six distinct real derivative zeros. Since h-J is odd,
they come in opposite pairs. At every local maximum of h-J its value
is >=|J|, and at every local minimum its value is <=-|J|: h has all real
zeros and the opposite extremum reverses both value and type. For
|J'|<|J|, h_{J'} has seven **simple real** zeros. Its moment matrix stays
positive definite; M at the actual endpoint does too. Integrating
barC_J=-2JH/D on this interval, using continuity at the endpoint, yields
barC(E,G,J)<barC(E,G,0)-56J² for J nonzero, since
H/D>196(D+1/14)^2/D>=56. Together with (9) this proves (10).
Only critical-root continuation was used. Neither Q nor a centered
even primitive was declared feasible along the whole interval.

## 4. Legal splitting and strict single-double obstruction

When Q is squarefree and Q(x) is nonzero, all six other originals are
simple and separated from x. Locally f(z)=Q(x)(z-x)^2+O((z-x)^3).
The equation f(z)-t Q(x)=0 therefore splits the double root into two
simple real roots for every sufficiently small t>0. For example,
f(x)<t Q(x) in the appropriate curvature sign, while at x plus or minus
2sqrt(t) the opposite sign holds for small t. The six other simple
real originals persist by the real implicit function theorem. Degree
eight then accounts for all roots. Only c changes, retaining sum zero,
norm one and mu3=mu5=0. The new critical mass at the fixed node x is
exactly m_x(f_t)=32t, since Q(x)=4hprime(x). No two-sided normal
feasibility is asserted.

Since h is now simple, there is a smooth residue extension of C in
E,G,J,c. Write kappa_lambda=-8/h'(lambda), including its nonzero
value at the inactive critical x. The constant-term fiber has

\[
 \eta=R_6+\alpha(c-c_*)^2,\quad
 \alpha=\sum\kappa_\lambda^2,\quad
 c-c_*={h'(x)p_*(x)\over8},
 \quad L_x={\kappa_x^2\over\alpha}.
\]

These are the credited affine-fiber mechanism of
[9271](../constant-term-angular-reduction/PROOF.md), now evaluated at a
zero actual mass. They give

\[
 g_0=C_c=-{16p_*(x)\over D h'(x)L_x},\qquad
 Q(x)=4h'(x),\quad -Q(x)g_0={64p_*(x)\over D L_x}.
\]

This proves (11) and the necessary p_*(x)<=0.

The squarefree Q condition gives an open legal three-parameter
neighborhood (2). At a local maximum all derivatives (7) vanish.
If p_*(x)=0, then g0=0 and C equals its algebraic comparison. Also
J_x=-h'(x) and c_x=8x h'(x), so

\[
 C_x=\bar C_J J_x=2J h'(x)H/D\ne0
\]

when J is nonzero. This contradiction proves the strict negative sign.
The algebraic center derivative identity remains valid at the collision;
it does not require an improving unrestricted two-sided normal path.

For the compensation condition, (9) at fixed E,G gives
C_x=[2J h'(x)H-T_x]/D. Stationarity forces T_x=2J h'(x)H.
Since h'(x) is nonzero, x can locally be parameterized by J with
x_J=-1/h'(x). Thus J Phi_J=-2J²H/D<-112J², proving (12).
For comparison, writing g1=C_J/8, g2=C_G/4 and g4=C_E/2 in the smooth
coefficient extension, its three tangent equations are equivalently

\[
 g_1=xg_0,\qquad g_2=x^2g_0,\qquad g_4=x^4g_0.
\]

These are necessary boundary equations, not full interior stationarity.

## 5. A triple original: duplicate leverage and second order

Suppose Q is squarefree with Q(x)=0. Its roots remain simple and real
through a whole parameter neighborhood of (2), and r has six simple
real roots in a neighborhood too. Thus the chart is legal through the
triple, even though its coefficient derivative in x vanishes there.
The grouped angular function agrees with (6) throughout this chart.

Now x is one of the six distinct r nodes. Its mass in (15) is zero, so
p(x)=v(x)^T beta=0. Consequently K beta=M beta=nu and beta=beta_*.
Because the six-column V is invertible and v(x) is one of its columns,
v(x)^T K^{-1}v(x)=1. Equation (16) gives L_x=1/2, p_*(x)=0 and T=0.
The full critical h still has multiplicity two at x; both dimensions
of that eigenspace have **zero full coupling mass**, not a split
positive mass. No seven-simple-critical inverse is substituted here.

At fixed E,G, J_x=-h'(x)=0 and J_xx=-h''(x). M and nu depend on x only
through J, so (beta_*)_x=0 at the triple. Thus the total derivative of
p_*(x) is the polynomial derivative p_*'(x), and

\[
 T_x=0,\quad T_{xx}=2p_*'(x)^2/L_x=4p_*'(x)^2,
 \quad \bar C_x=0,\quad
 \bar C_{xx}=\bar C_J J_{xx}=2J h''(x)H/D.
\]

Differentiating (9) proves (13). The legal chart justifies both
first-order E,G stationarity and second-order x necessity at any local
maximum. If Q has another multiple root, (6) and (9) still apply when
r is squarefree, but open-chart feasibility of every parameter
variation has not been established; this local-maximum argument is
not applied there.

## 6. Exact evidence, independent algebra comparison and limits

The standalone standard-library [verify.py](verify.py) uses QQ[x,E,G]
with complete sparse coefficient records; ascending monic z quotients;
Fraction arithmetic; and both dual and quadratic-jet arithmetic. It
checks full double and canceled factors, all11 canceled traces, all6
coupling moments, every36 K entry, every108 derivative entry and all18
moment derivatives. A separate Bezout/Newton mass-square calculation
checks the whole value and moving-node gradient at six actual controls,
plus an explicit infeasible Q control. Two actual triple controls retain
the repeated full h and verify the complete second derivative, including
the factor4 in (13). No floating-point sign supplies a premise.

Positive and negative splitting signs occur at exact single doubles:

| x | E | G | sign p_*(x) | actual Q distinct real roots |
|---|---|---|---|---|
| 1/100 | 11/288 | -1/1152 | positive | 6 |
| 1/3 | 13/288 | -12811771/7290000000 | negative | 6 |

An actual triple is x=1/40,E=1/40,G=-189007/4096000000. Another is
x=1/20,E=3/125,G=-10777/64000000. Each has six distinct real Q roots,
Q(x)=0, six distinct r roots, six distinct full h roots (seven roots counted with
multiplicity), and C_xx>0
verified exactly. The full rational values are in [expected.json](expected.json).
For x=1/20,E=11/288,G=-1/1152, r has six distinct real roots but Q has
only two. This control rejects the false feasibility shortcut.
Nine mathematical damages reject omitted original feasibility,
universal splitting improvement, wrong normal sign, a simple-full-h
triple, positive repeated-node coupling, missing duplicate leverage,
dropped collision cost, frozen nodes and omitted D_E=-8.

The optional [compare_cas.py](compare_cas.py) independently derives all
237 whole universal polynomial maps through SymPy1.14 symbolic division
and logarithmic/Laurent series, then compares every coefficient. It
imports neither the checker nor a peer's executable. This is a different
**same-author** algebra calculation, not independent review.

Reproduce from the repository root with Python3.11+:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-2/collision-moment-reduction/verify.py
python3 -I -B -O round-two/six-sendov-2/collision-moment-reduction/verify.py
```

Expected complete record SHA256:
`a5f6ec31e5424970d60e4b17200cb31b5cd952841009e3823ce1a012e68c22f3`.
Optional SymPy1.14 environment: run compare_cas.py with the same native
thread settings. All children are serial under fixed50-second guards,
unchanged1CPU2GiB. Timings and memory are in the accompanying README.
Ordinary Schur compression, interlacing, real-root feasibility,
Sherman--Morrison, smooth chain differentiation, horizontal continuation
and local-maximum arguments are **unformalized**. Finite controls are not
a continuous-domain enumeration or a proof of a universal curvature sign.

These formulas reduce actual collision optimization; they do not solve
it. The sign p_*(x)<0 and the stationary equations are only necessary.
Other original collision patterns, sharp symmetric/asymmetric maxima,
and the full physical complex first-power bridge remain open.
The unconstrained even comparison cannot inherit the actual symmetric
47/2 bound in [REVIEW9416](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/even-angular-audit/REVIEW.md).
Primary literature and exact dependency provenance are in
[LITERATURE.md](LITERATURE.md). No historical priority is claimed.
