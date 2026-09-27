# A uniform Gaussian sign margin at the zero-loss boundary

27 September 2026. Complete author proof, pending independent mathematical
review and formalization. The result is a uniform positive margin on bounded
volume ranges at every fixed radius and with a fixed positive covariance
floor. Its smallness assumption is on **mean pair-distance loss**, allowing
rare points to move a fixed distance. The loss cutoff is obtained by
compactness; this proof does not supply a numerical value for it.

This strengthens the team's accepted maximum-displacement neighborhood of
an isometry. It is a bridge to the remaining compact certification problem,
not a solution of unrestricted three-dimensional majorisation. Attribution,
precise dependencies, and the distinction from the geometric positive
classes are recorded in [SOURCES.md](SOURCES.md).

## 1. The uniform statement

Work first at Gaussian covariance `I_3`. Write

\[
 C=(2\pi)^{-3/2},\qquad \gamma(z)=C e^{-|z|^2/2},\qquad
 \omega_3=4\pi/3.
\]

Fix `R>0`, `kappa>0` and `V>0`. Let `mu` range over ALL probability laws
such that

\[
 \mathbb E X=0,\quad |X|\le R,\quad
 \operatorname{Cov}(X)\succeq\kappa I_3.                 \tag{1}
\]

A vacuous parameter choice causes no difficulty. Let `T` be 1-Lipschitz.
Center `T(X)` and apply an orthogonal Procrustes alignment, denoting the
result by `Y`. Thus `E Y=0`, and `A=E[XY^T]` is symmetric positive
semidefinite. Put

\[
 h=Y-X,\quad M=\mathbb E|h|^2,\quad
 \Delta(x,x')=|x-x'|^2-|Y(x)-Y(x')|^2\ge0,\quad
 D=\mathbb E\Delta(X,X').                                \tag{2}
\]

For `f=mu*gamma`, let `E_f(v)={f>a_f(v)}` be its unique top set of
volume `v`. Put `g=law(Y)*gamma` and

\[
 L_p(v)=\sup_{|E|=v}\int_Ep,\qquad
 H(u)=\int(g-Cu)_+-\int(f-Cu)_+.                         \tag{3}
\]

**Theorem 1.** There exist `c=c(R,kappa,V)>0` and
`D_*=D_*(R,kappa,V)>0` such that, uniformly over (1), all such contractions,
and every `0<v<=V`,

\[
 0<D\le D_*\quad\Longrightarrow\quad
 \boxed{\ \frac1v\int_{E_f(v)}(g-f)\ge cD.\ }            \tag{4}
\]

Consequently `L_g(v)-L_f(v)>=cvD`. If `v(u)=|{f>Cu}|` belongs to
`(0,V]`, then `H(u)>=c v(u)D`. For `D=0`, the source and target laws
agree after the chosen rigid alignment, and both differences are zero.
The profile and hinge statements are invariant under that alignment;
the tested-set statement (4) explicitly uses it.

The constants have no dependence on the number of atoms, a smallest atom
mass, or a positive lower bound for `D`. No small-radius/high-noise
condition is imposed. The covariance floor and the finite upper volume
bound ARE hypotheses. `D_*` and part of `c` are non-effective in the
present proof.

**Corollary 2 (the entire interval above a fixed threshold).** For each
`0<u_0<=1`, there is a `D_*(R,kappa,u_0)>0` such that (1) and `D<=D_*`
imply

\[
 H(u)\ge0\qquad(u_0\le u\le1).                           \tag{5}
\]

Indeed use Theorem 1 with

\[
 V=\omega_3\big(R+\sqrt{2\log(1/u_0)}\big)^3.             \tag{6}
\]

The Gaussian upper tail bound contains every nonempty `{f>Cu}` in this
ball when `u>=u_0`. Empty source top sets already give `H(u)>=0`.
For `u_0=1` this last observation suffices. No single positive `D_*`
for all `u_0 downarrow0` is asserted.

At covariance `s I_3`, apply the theorem to `X/sqrt(s)` and `Y/sqrt(s)`:
the arguments of the constants are `R/sqrt(s)`, `kappa/s`, and
`V/s^(3/2)`, and (4) reads
`integral_E(g_s-f_s)>=c (v/s^(3/2))(D/s)`.
This scaling statement does not make the cutoff uniform in `s`.

## 2. Uniform top-set estimates and the credited first variation

Write `r_V=(V/omega_3)^(1/3)` and set

\[
 a_0=C e^{-(r_V+R)^2/2},\quad
 w_0=e^{-(r_V+3R)^2},\quad
 w_1=(C/a_0)^2,\quad c_0=a_0w_0/4.                       \tag{7}
\]

For `E=E_f(v)`, `0<v<=V`, and `a=a_f(v)`, Gaussian tail bounds give

\[
 a\ge a_0,\qquad E\subset B(0,r_V+2R),\qquad
 w_0\le\frac{\gamma(z-x)\gamma(z-b)}{f(z)^2}\le w_1
 \quad(z\in E,\ x,b\in\operatorname{supp}\mu).            \tag{8}
\]

The lower bound also holds for any `x in B(0,R)`. For example,
`f(z)>=C exp(-(r+R)^2/2)` on the ball of volume `v`, proving the level
bound; the upper Gaussian tail then gives the containing ball.

Define the top-set kernel

\[
 k_E(x)=\int_E\gamma(z-x)\,dz.
\]

The posterior-divergence identity used in the accepted
[near-isometry proof, Section 3](../gaussian_contact_near_isometries/PROOF.md)
has the following pointwise version, including points outside the support:

\[
 \nabla k_E(x)=-a\int_E\int
 (x-b)\frac{\gamma(z-x)\gamma(z-b)}{f(z)^2}\,d\mu(b)\,dz.
                                                               \tag{9}
\]

At a regular level this follows by applying the divergence theorem to
`gamma(z-x)/f(z)` and using `f=a` on the boundary. Approximate a critical
positive level by regular values. A Gaussian mixture is real analytic,
nonconstant and tends to zero; each positive level has Lebesgue measure
zero. The sets stay in a common compact ball. Dominated convergence
therefore gives (9) also at critical levels. Differentiation in `x` under
the integral is justified by the bounded Gaussian derivatives.

For any unit vector `e`,

\[
 \|\partial_{ee}\gamma\|_\infty\le C,
 \qquad \|D^2k_E\|_{\rm op}\le Cv.                      \tag{10}
\]

The first bound reduces to `|t-1|exp(-t/2)<=1` for `t>=0`.
These estimates require no regularity of the top-set boundary.

## 3. A uniformly strict one-point comparison

**Lemma 3.** For the same `R,kappa,V` there is `b>0` such that the
following holds uniformly. Take a law `nu` satisfying (1), its density
`f`, `E=E_f(v)`, `0<v<=V`, and `x in B(0,R)`, `y in B(0,2R)` with

\[
 |y-z|\le|x-z|\quad\hbox{for every }z\in\operatorname{supp}\nu.
                                                               \tag{11}
\]

Then, with `q=|x|^2-|y|^2`,

\[
 \frac{k_E(y)-k_E(x)}v\ge bq.                            \tag{12}
\]

Here `q>=0`, and `q=0` forces `x=y`. Two ingredients in the proof are
classical two-point polarization and compactness. We give all details,
particularly the potentially singular limits `x=y` and `v=0`.

### 3.1. Coercivity and small displacements

Put `h=y-x` and `l=|h|`. Condition (11) is
`q+2z.h>=0`. Its `nu` average is `q`. For `l>0`, the centered random
variable `U=z.h/l` has variance at least `kappa`, is at most `R`, and is
at least `-q/(2l)`. The inequality
`(U+q/(2l))(R-U)>=0` gives

\[
 q\ge 2\kappa l/R.                                      \tag{13}
\]

In particular `|y|<=|x|<=R`. By (9), (8), and
`-2(x-z).h=q+2z.h+l^2`,

\[
 \frac{\nabla k_E(x).h}{v}\ge 2c_0(q+l^2).
\]

Taylor's theorem and (10) imply

\[
 \frac{k_E(y)-k_E(x)}v\ge2c_0q-\frac C2l^2\ge c_0q
 \quad\hbox{if }l\le\frac{4c_0\kappa}{CR}.              \tag{14}
\]

Thus division by `q` causes no loss near `x=y`.

### 3.2. Strict positivity for a fixed positive volume

Suppose `x!=y`. Let `sigma` reflect in their perpendicular bisector,
and let `P` be the open half-space containing `y`. All centers of `nu`
lie in its closure, and a positive mass lies in `P`: otherwise the
covariance would be singular. Hence

\[
 f(z)>f(\sigma z),\qquad
 \gamma(z-y)>\gamma(z-x)\quad(z\in P).
\]

Pairing reflected points gives exactly

\[
 k_E(y)-k_E(x)=
 \int_P[1_E(z)-1_E(\sigma z)]
              [\gamma(z-y)-\gamma(z-x)]\,dz>0.          \tag{15}
\]

For strictness, `E` has a point in `P` (reflect a point in the other
half-space if needed). A path inside `P` to a sufficiently distant point
crosses the level `f=a`. At this crossing `f(sigma z)<a`; just inside
there is an open set with `f(z)>a>f(sigma z)`. Both factors in (15) are
strictly positive there. This argument uses neither convexity of `E`
nor a unique mode of `f`.

### 3.3. Volumes tending to zero

The laws in (1) form a weakly compact set. For a convergent sequence of
such laws, the Gaussian convolutions and their derivatives converge
uniformly on compact sets, with a uniform tail bound. If `v_j downarrow0`,
then `a_{f_j}(v_j)->max f`. Any weak limit of
`1_{E_{f_j}(v_j)} dz/v_j` is a probability measure supported on the modes
of the limiting density. The top sets lie in the fixed ball in (8).

At any mode `z`, the Gaussian score equation gives
`z=E[Z | Z+G=z]`, so `|z|<=R`. The posterior density relative to `nu`
is at least `exp(-2R^2)`. Averaging the nonnegative quantities in (11),

\[
 |z-x|^2-|z-y|^2\ge e^{-2R^2}q.
\]

Since `|z-x|<=2R` and `exp(t)-1>=t` for `t>=0`,

\[
 \gamma(z-y)-\gamma(z-x)
 \ge b_{\rm mode}q,\qquad
 b_{\rm mode}=\frac C2e^{-4R^2}>0.                        \tag{16}
\]

The same bound holds after averaging over any limiting distribution on
possibly multiple or degenerate modes.

### 3.4. Uniformization

If (12) had no positive uniform `b`, take a sequence with the ratio
in (12) divided by `q` tending to zero. Bound (14) keeps `l` away from
zero, and (13) then keeps `q` away from zero. Extract convergent laws,
points, and volumes in `[0,V]`. Condition (11) is closed: equivalently,
the integral of the negative part of `q+2Z.h` is zero.

If the limiting volume is positive, the top sets converge in measure:
subsequential convergence of their levels and the null-level-set property
identify the unique limiting level. Equation (15) contradicts the zero
ratio. If the volume tends to zero, (16) gives the contradiction. This
proves Lemma 3. Notice that its uniform constant is not evaluated by this
compactness argument. QED.

## 4. The bulk displacement has a smaller quadratic remainder

We use the Procrustes inequality already proved in
[the accepted local result, Section 2](../gaussian_contact_near_isometries/PROOF.md):

\[
 M\le\frac{\mathbb E\Delta^2}{2\kappa}
   \le K_0D,\qquad K_0=\frac{2R^2}{\kappa}.              \tag{17}
\]

For completeness, the centered coordinate operators `U,W:R^3->L^2(mu)`
satisfy `UU*-WW*=-(1/2)J Delta J`, where `J` removes constants.
Procrustes alignment gives
`||UU*-WW*||_HS^2 >= (kappa/2)||U-W||_HS^2`.
Combining these two statements proves the first inequality; the second
uses `0<=Delta<=4R^2`.

The centered aligned map is still 1-Lipschitz on the whole ball, and

\[
 |Y(x)|=|Y(x)-\mathbb EY(X)|\le\mathbb E|x-X|\le2R
 \quad(|x|\le R).                                       \tag{18}
\]

Fix `delta>0` and split the labels into

\[
 A_\delta=\{|h|\le\delta\},\quad B_\delta=A_\delta^c,
 \quad\alpha=\mu(B_\delta)\le K_0D/\delta^2.             \tag{19}
\]

We claim, for fixed `delta` and sufficiently small `D`,

\[
 M_A:=\int_{A_\delta}|h|^2d\mu
 \le\frac{32R}{\kappa}\delta D+2L^2\alpha^2,
 \qquad L=96R^3/\kappa+6R.                              \tag{20}
\]

It is important that the last error is `alpha^2`, not `alpha`.
Merely applying (17) to the whole law would not give (20).

Here are alignment details. For small enough `D`,
`A=E[XY^T]>=kappa I/2`, since
`||A-Cov(X)||_op<=R sqrt(M)`. Conditional on `A_delta`, the source
covariance is at least `kappa I/2` when
`alpha<=min(1/2,kappa/(8R^2))`. This follows by removing a mass `alpha`
from `E[XX^T]` and subtracting the conditional mean; the covariance
changes downward by at most `4alpha R^2 I`.

Let `B` denote the conditional centered cross-covariance. The bounds
`|X|<=R`, `|Y|<=2R`, `E X=E Y=0` give

\[
 \|B-A\|_F\le12\alpha R^2.                              \tag{21}
\]

The conditional means have norms at most `2alpha R` and `4alpha R`.
Let `Q` be any optimal conditional alignment. Optimality and `A>=kappa I/2`
give

\[
 \frac\kappa4\|I-Q\|_F^2
 \le\operatorname{tr}((I-Q)A)
 \le\|I-Q\|_F\|B-A\|_F,
 \quad \|I-Q\|_F\le48\alpha R^2/\kappa.                 \tag{22}
\]

Transposes in the cross-covariance convention do not change this estimate.
Its conditional translation has norm at most `6alpha R`. Thus the
conditional aligned image differs from `Y` by at most `L alpha`
uniformly on the ball.

For two core labels, contraction and `|h|<=delta` imply
`Delta<=8R delta`. Apply the first inequality in (17) to the conditional
law, whose covariance floor is `kappa/2`. Its optimal mean square error
is at most
`(8R delta/kappa) D/(1-alpha)^2`. Restoring the original alignment,
using `|u+w|^2<=2|u|^2+2|w|^2`, and `1-alpha>=1/2`, proves (20).

## 5. The core supplies its own pair-loss margin

For measurable label sets `A,B`, abbreviate the UNNORMALIZED pair loss by

\[
 D_{AB}=\iint_{A\times B}\Delta(x,x')\,d\mu(x)d\mu(x').
\]

Use the core and its complement from (19). Then
`D=D_AA+2D_AB+D_BB`. Apply (9) to
`I_A=integral_A grad k_E(x).h(x) dmu(x)`. On `A x A`, symmetry and

\[
 -2(x-x').(h(x)-h(x'))=\Delta(x,x')+|h(x)-h(x')|^2
\]

give a positive contribution. The remaining `A x B` contribution is
bounded using (8), `a<=C` and `|x-x'|<=2R`. Therefore

\[
 \frac{I_A}{v}\ge c_0D_{AA}-K_2\alpha\sqrt M,
 \qquad K_2=2RCw_1.                                    \tag{23}
\]

Taylor's theorem (10), followed by (20), proves

\[
 \frac1v\int_A[k_E(Y(x))-k_E(x)]d\mu(x)
 \ge c_0D_{AA}-K_1\delta D-CL^2\alpha^2-K_2\alpha\sqrt M,
 \qquad K_1=16CR/\kappa.                                \tag{24}
\]

For each fixed `delta`, the last two errors are `o(D)` as `D downarrow0`
by (17) and (19). All bounds here are uniform in `0<v<=V` and the law.
This first variation is on the actual source top set and retains the
separate core--core and core--rare pair-loss contributions.

## 6. Rare displacements retain a uniform positive margin

We prove the remaining assertion sequentially; this is the non-effective
step that produces `D_*`. Suppose `D_j downarrow0`. Align and center as
above. Along a subsequence the laws converge weakly to `mu_0`, and the
aligned 1-Lipschitz maps converge uniformly on `B(0,R)` to `T_0`, by (18)
and Arzela--Ascoli. Equations (17) and weak convergence imply

\[
 T_0(x)=x\quad\hbox{on }\operatorname{supp}\mu_0.          \tag{25}
\]

The limit still satisfies (1). For every `x in B(0,R)`, contraction and
(25) give `|T_0(x)-z|<=|x-z|` for all `z in supp(mu_0)`.

Also take a subsequential limit of `v_j in (0,V]`. Set
`ell_j(x)=k_{E_{f_j}(v_j)}(x)/v_j`. These functions converge uniformly
on `B(0,2R)` along a further subsequence. If the limiting volume is
positive, the limit is the normalized top-set kernel of `mu_0`.
If it is zero, the limit is `integral gamma(z-x) d sigma(z)` for a
probability measure `sigma` on the modes of `mu_0*gamma`, as in Section 3.3.
Uniform convergence follows either from convergence of sets or from weak
convergence of these probability measures and equicontinuity of Gaussian
kernels on the fixed compact ball.

Let

\[
 \beta=\min(b,b_{\rm mode})>0,
 \qquad q_0(x)=|x|^2-|T_0(x)|^2.
\]

Lemma 3, or (16) at zero volume, gives for every `x in B(0,R)`

\[
 \ell_0(T_0(x))-\ell_0(x)\ge\beta q_0(x),\qquad
 q_0(x)\ge(2\kappa/R)|T_0(x)-x|.                         \tag{26}
\]

For fixed `delta>0`, on `B_j={|Y_j(x)-x|>delta}` we have
`|T_0(x)-x|>=delta/2` eventually, uniformly. Thus
`q_0(x)>=kappa delta/R` there. The actual loss against an independent
label is

\[
 q_j(x):=\int\Delta_j(x,x')d\mu_j(x')
        =|x|^2-|Y_j(x)|^2+D_j/2.                         \tag{27}
\]

This formula uses both centered means and
`D_j=2(E|X_j|^2-E|Y_j|^2)`. It converges uniformly to `q_0`.
The uniform convergences in (26)--(27), and the positive lower bound for
`q_0` on `B_j`, imply

\[
 \ell_j(Y_j(x))-\ell_j(x)\ge(\beta/2)q_j(x)
 \quad(x\in B_j)                                       \tag{28}
\]

for all sufficiently large `j`. Integrating gives

\[
 \frac1{v_j}\int_{B_j}[k_{E_j}(Y_j(x))-k_{E_j}(x)]d\mu_j(x)
 \ge(\beta/2)(D_{BA}+D_{BB}).                            \tag{29}
\]

This is a sign for finite rare displacements, not a Taylor expansion of
them. The common limiting background is fixed by the map, so each such
displacement moves closer to every background center. That fact is what
permits the polarization argument.

## 7. Completing the uniform proof

Put `c_*=min(c_0,beta/4)>0`, and fix
`0<delta<=c_*/(4K_1)`. Combining (24) and (29), and keeping `delta`
fixed while `D_j->0`, yields

\[
 \frac1{v_j}\int_{E_j}(g_j-f_j)
 \ge c_*D_j-K_1\delta D_j-o(D_j)
 \ge(3c_*/4)D_j-o(D_j).                                 \tag{30}
\]

All pair-loss terms have been retained: the coefficient of `D_AB` in
(29) is at least `2c_*`, and that of `D_BB` is at least `c_*`.

If no uniform `D_*>0` made (4) true with `c=c_*/2`, a violating sequence
with `0<D_j->0` would exist. The compactness argument just given would
produce a subsequence contradicting (30). Thus `D_*` exists. The profile
bound follows by testing `g` on `E_f(v)`. For a hinge, test its variational
formula on `{f>Cu}`. Equation (17) treats `D=0`. This proves Theorem 1
and its stated consequences. QED.

## 8. A genuine difference from maximum-displacement stability

This exact calibration is a familiar fold, not a new positive map class.
Give the four points

\[
 (-1,0,0),\quad(-2,1,0),\quad(-2,0,1),\quad(-2,-1,-1)
\]

equal total mass `1-alpha`, and give `(1,0,0)` mass `alpha`, with
`0<alpha<=1/2`. Apply `T(x_1,x_2,x_3)=(-|x_1|,x_2,x_3)`.
After separate centering, the identity is a Procrustes alignment. The
source lies in `B(0,3)` and its covariance is at least `(3/32)I`.
Direct calculation gives

\[
 D=14\alpha(1-\alpha),\quad M=4\alpha(1-\alpha),\quad
 \|h\|_\infty=2(1-\alpha).                              \tag{31}
\]

The four-point bulk has squared displacement
`4alpha^2(1-alpha)`. Moreover `E Delta^2/D=52/7` does not tend to zero.
After scaling every coordinate by `1/6`, the centered radius is at most
`1/2`, the covariance is at least `1/384 I`, and the second-to-first
loss ratio is `13/63`. This meets the radius and covariance requirements
of the concurrent [quartic loss guard](../gaussian_loss_moment_middle/PROOF.md)
but fails its `Q<=2^-48 d` requirement for every positive `alpha`.
The present theorem instead applies for sufficiently small `alpha` at
any fixed upper volume bound. Thus `D->0` while the maximum aligned displacement
tends to two. Theorem 1 uniformly covers this type of rare motion without
claiming it was absent from previously known geometric classes.
[verify.py](verify.py) checks these identities, the exact covariance and
Procrustes certificates, and the pair-loss decomposition with rational
arithmetic. It does not evaluate `b`, `c`, or `D_*`, and it is not a
numerical certificate of Theorem 1.

## 9. Minimal certification handoff and remaining boundary

For a compact input family with fixed `R` and covariance floor `kappa`,
Theorem 1 removes `D downarrow0` as a possible adverse contact on ANY fixed
bounded source-volume range. A separately established uniform low-threshold
sign `H>=0` for `u<=u_0` combines with Corollary 2 to give **all-threshold
majorisation for every sufficiently small mean loss in that family**.
Such a uniform tail is an extra hypothesis, not supplied here. The
existing finite-input signed endpoints are compatible when their constants
are made uniform on the chosen family.

After the zero-loss neighborhood is removed, the remaining middle search
has `D>=D_*`. R3's loss-preserving cubature and R2's exact moment production
can then be used with the [Jackson reconstruction](../gaussian_jackson_certification/PROOF.md).
The current theorem gives a qualitative reason the normalized margin does
not collapse at the full-rank zero-loss boundary. Turning its compactness
constants into a runnable cutoff is still necessary for a practical cover.
No replacement approximation operator or adjacent signed cell is proposed.

The genuinely unrestricted boundaries still include vanishing source
covariance, unbounded source-volume ranges at fixed variance, and positive
loss away from this neighborhood. Neither a new Kneser--Poulsen class nor
an improved universal numerical defect constant follows from this proof.
