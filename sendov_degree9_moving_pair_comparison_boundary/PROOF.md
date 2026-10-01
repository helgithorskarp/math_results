# A sharp angular threshold and an actual moving-pair comparison boundary

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Complete ordinary written author proof, with exact algebra checks.
Independent review of these new conclusions is pending. The analytic
arguments and credited geometry are outside a formal kernel.
[LITERATURE.md](LITERATURE.md) gives dependency and method attribution.

## 1. Definitions, actual families and conclusions

For a degree-nine polynomial
\[
p(z)=c(z-a)\prod_{j=1}^8(z-z_j),\qquad
c\ne0,\quad 0\le a\le1,\quad |z_j|\le1,\quad z_j\ne a,
\]
the marked root is simple. Count all original and critical algebraic
multiplicities. Put
\[
d=1+a,\quad v=d^{-1},\quad \kappa=d(a-5/8),\quad
E=\sum_j|(a-z_j)^{-1}-v|^2,\quad
F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}.
\]
Simplicity excludes a critical point at a. Rotation gives the same
statements at a marked root of modulus a, using rotated coordinates.
Nonzero scalar factors and root permutations have no effect.

Use the credited **entire actual stationary singleton/seven branch**
\[
P_{a,e}(z)=(z-a)(z+e^{i(7t+m)})(z+e^{i(-t+m)})^7,
\quad E(P_{a,e})=e,
\]
\[
t^2={e\over56v^4}+O(e^2),\quad
m=w(a,e)t^3,\quad w(a,e)=\beta(v)+O(e),\quad
\beta(v)={392-1197v+945v^2\over20}.                       \tag{1}
\]
The actual mean and energy inverse exist analytically and uniformly for
a in [0,1] by the [local theorem and independent audit](LITERATURE.md).
In (1), t is the small positive solution. The claim is not that the
truncated mean beta times t cubed is exactly stationary at nonzero energy.

The comparison uses the credited actual moving-pair construction, with
the following explicit solution of its credited exact energy identity:
\[
x(a,e)={d^4e\over4+2ad^2e},\qquad
Q_{a,e}(z)=(z-a)(z+1)^6\{z^2+2[1-x(a,e)]z+1\}.          \tag{2}
\]
For 0<e<=1/4, one has 0<x<=1, so the other roots are six copies of -1
and -exp(plus or minus it), where cos(t)=1-x. They lie on the unit
circle and are distinct from the marked root. Section 3 proves E(Q)=e
exactly. Thresholds for subsequent objective expansions are smaller.

Set
\[
a_G={20\sqrt{1614}-385\over692},\qquad
P_G(a)=2768a^2+3080a-2875,
\]
\[
{604757\over10^6}<a_G<{604758\over10^6},\qquad
K_1={d^3(516d^2-528d-393)\over7168},\quad
K_Q={d^3(784d^2-856d-443)\over16384}.                    \tag{3}
\]

**Theorem 1 (sharp all-balanced angular threshold).** For every balanced
nonzero real theta in R^8, the angular coefficient K_a(theta) of Section 2
satisfies K_a(theta)<=K_1(a) for all such theta **if and only if a>=a_G**.
For a>a_G, equality consists exactly of the nonzero scale/permutation
orbit of (7,-1,...,-1). At a=a_G, equality consists exactly of that
orbit and the nonzero scale/permutation orbit of the moving pair
(1,-1,0,...,0). Equivalently, these are the complete Gamma=0 set in
Section 2. Below a_G the moving pair strictly beats K_1.

**Theorem 2 (uniform actual comparison through the quartic tie).** There
is one existential e_0>0, independent of a in [0,a_G], such that
\[
0<e<e_0\quad\Longrightarrow\quad
F(P_{a,e})-F(Q_{a,e})
\ge {77\over10000}\{(a_G-a)e^2+e^3\}>0.                 \tag{4}
\]
In particular the actual stationary branch is nonglobal at a=a_G,
although it attains the optimal leading balanced angular coefficient.

**Theorem 3 (analytic equal-value curve for the two actual families).**
There exist fixed delta>0, e_1>0 and a unique real-analytic alpha(e)
near e=0, with
\[
\alpha(0)=a_G,\qquad \alpha(e)=a_G+c_{\rm eq}e+O(e^2),
\qquad {132978\over10^6}<c_{\rm eq}<{132979\over10^6}.    \tag{5}
\]
For |a-a_G|<delta and 0<e<e_1, both actual families are admissible,
and the sign of F(P)-F(Q) is the sign of alpha(e)-a. This is a
comparison/equal-value curve for these two families; it does not assert
a global phase boundary or that Q is a minimizer.

**Corollary (all-disk strict local but nonglobal minima).** Write
\[
a_*={10\sqrt{2198}-225\over404}<a_G.
\]
For every compact J subset (a_*,a_G], the actual P branch and its
conjugate are strict local but nonglobal minima at every sufficiently
small positive energy, uniformly over a in J. The credited local
strictness covers all eight independent closed-disk root motions; its
configuration neighborhood may depend on a,e. Choose delta in Theorem 3
so [a_G-delta,a_G+delta] is contained in (a_*,1]. In this neighborhood,
the same strict-local/nonglobal conclusion holds whenever a<alpha(e),
including an interval of order e above a_G. Equality or the reverse
two-family comparison is not a claim of global minimality.

These results concern small-energy configurations near eight copies of
-1. They do not resolve the unrestricted first-power inequality or
identify all fixed-energy global minimizers below 5/8.

## 2. The all-radius angular coefficient and its sharp threshold

Let mu_k=sum(theta_j^k), u_*=1/sqrt(8) times the all-ones vector,
P=I-u_*u_*^*, and
\[
H=P\operatorname{diag}(\theta)P|_{u_*^\perp},\quad
w=\operatorname{diag}(\theta)u_*,\quad
\Psi=\sum_{\lambda\ {m distinct}}\|\Pi_\lambda w\|^4,
\quad X={\mu_4\over\mu_2^2},\quad \eta={64\Psi\over\mu_2^2}.
\]
Use full eigenspace projections, including repeated eigenvalues.
The invariant, moment bound and Gram bound are credited inputs from
[the angular work and independent audit](LITERATURE.md):
\[
\Delta={43\over56}-X\ge0,\qquad
\Gamma=\eta-{56X-13\over30}\ge0.                         \tag{6}
\]
The equality set Delta=0 is precisely the singleton/seven orbit.
That orbit has eta=1. The already credited moving pair has X=eta=1/2,
so Delta=15/56 and Gamma=0.

We extend the **pure angular** coefficient and its uniform bridge from
the earlier [full-radius theorem](LITERATURE.md), whose global-minimum
scope was [5/8,1], to all a in [0,1]. For z_j=-exp(is theta_j),
\[
F=16v+\kappa E-K_a(\theta)E^2+o(E^2),\quad
K_a=A_dX+B_d-C_d\eta,                                   \tag{7}
\]
\[
A_d={d^3(48d^2-40d-53)\over512},\quad
B_d={d^3(16d^2-104d+203)\over8192},\quad
C_d={d^3(4d+1)^2\over8192}>0.                            \tag{8}
\]
The little-oh is uniform on a in [0,1] and sum theta=0, mu_2=1.
There is no general O(E^3) assertion for arbitrary varying theta.

Here is why the extension is valid. Direct differentiation gives the
critical-reciprocal characteristic 9R(q)-qR'(q), R=product(q-u_j),
u_j=(a+exp(is theta_j))^-1. Its matrix is similar to
(P+3u_*u_*^*)diag(u)(P+3u_*u_*^*). The background has a sevenfold v
near eigenvalue and a simple 9v far eigenvalue, with external gap
8v>=4 throughout the enlarged interval v in [1/2,1]. Reciprocal Taylor
coefficients and the literal trace identities from the full-radius
independent audit are identities with v left symbolic. They involve no
sign assumption a>=5/8.

For clarity, the near effective matrix is
\[
T=vI-iv^2Hs+s^2(c_2H^2+c_Rww^*)+O(s^3),\quad
c_2=v^2/2-v^3,\quad c_R=c_2+9v^3/8.                     \tag{9}
\]
Every repeated H eigenspace has zero w weight: its eigenvectors satisfy
(diag(theta)-lambda I)y=sigma u_*. At a diagonal value sigma=0 and
w^*y=lambda u_*^*y=0; away from diagonal values the possible eigenspace
is one-dimensional. Thus the second coefficient on a repeated space
is the scalar c_2 lambda^2 I.

Along any convergent sequence of radii, normalized theta and s tending
to zero, group H eigenvalues by distinct limiting values. Intergroup
elimination in (T-vI)/s uses only fixed gaps between limiting groups.
Its group matrix is -iv^2 H_group+s C_group+O(s^2). In a repeated
limiting group, C_group tends to c_2 lambda^2 I. The real part of a
normalized right-eigenvector equation eliminates the anti-Hermitian
first term. A simple group has the ordinary scalar coefficient. Hence
the compact-uniform real-square limit, through every collision, is
\[
s^{-4}\sum_{\rm near}[\Re(q-v)]^2\longrightarrow
c_2^2(\mu_4/2+\mu_2^2/32)
 +2c_2c_R(\mu_4/8-\mu_2^2/64)+c_R^2\Psi.                 \tag{10}
\]
A repeated limiting group's total w weight tends to zero, so the sum
of squares of its split weights does also; Psi is continuous. Near
real displacements are uniformly O(s^2), imaginary ones O(s). The
fixed-contour moment/modulus calculation therefore remains valid on
the enlarged compact interval and gives
\[
[s^4](F-16v-\kappa E)
=(-3v^3/32+5v^4/64+53v^5/512)\mu_4
 +(-v^3/512+13v^4/1024-203v^5/8192)\mu_2^2
 +(v^3/8+v^4/16+v^5/128)\Psi.                            \tag{11}
\]
Together with E=v^4 mu_2 s^2+O(s^4), this proves (7). This repeats
the necessary analytic bridge, rather than importing an earlier
global theorem outside its hypotheses. It uses no retained full-disk
cubic estimate or global-entry claim below 5/8.

Exact substitution of (6) into (7)--(8) gives
\[
K_1-K_a={d^3P_G(a)\over30720}\Delta+C_d\Gamma.            \tag{12}
\]
P_G is strictly increasing on [0,1] and has the unique positive zero
a_G. For a>a_G, positivity in (12) and the Delta equality classification
give the singleton/seven optimizer. At a=a_G, (12) is C_d Gamma.
For the moving pair below a_G,
\[
K_1-K_Q={d^3P_G(a)\over114688}<0.                        \tag{13}
\]
This proves the threshold necessity and sufficiency. We now close its
remaining equality classification using the credited Gram certificate.
Normalize mu_2=1 and write s=mu_3, z=s^2,
\[
h=z-{12\over5}(X-1/2)\ge0,\quad
D={3\over4}\Delta-{25\over48}h,\quad
N=\Delta-{5\over6}h,\quad B={1\over7}+{4\over3}z.
\]
The independent angular audit proves D>0 whenever Delta>0, including
the singular-case argument, and gives
\[
\eta\ge B+N^2/D,\qquad
\left(B-{56X-13\over30}\right)D+N^2={\Delta h\over36}.
\]
Consequently Gamma=0 with Delta>0 forces h=0. The following equality
deduction reconstructs the scalar moment proof's real-root mechanism;
it is not an assumption about a finite list of profiles.

Let f(y)=product(y-theta_j), a real-rooted degree-eight polynomial.
Its relevant coefficients are c_2=-1/2, c_3=-s/3,
c_4=1/8-X/4. Equality h=0 gives X=1/2+5s^2/12, hence
\[
f^{(4)}(y)=1680y^4-180y^2-40sy-(5/2)s^2.                \tag{13a}
\]
We use the elementary repeated-root lifting fact: a repeated root of
g' of multiplicity k>=2, for real-rooted g, must be a root of g of
multiplicity k+1. Indeed, off its roots, g'/g=sum m_j/(y-r_j) is
strictly decreasing, so every off-root zero of g' is simple. At a
root of g the multiplicity drops by exactly one. Rolle's theorem
keeps every derivative real-rooted, so this fact can be iterated.

If s is nonzero, the quartic (13a) has nonzero constant and its reversed
quartic R(y)=y^4 f^(4)(1/y) is real-rooted of degree four. Direct
differentiation gives
\[
R'(y)=-10y(sy+6)^2.                                    \tag{13b}
\]
Its nonzero double root -6/s lifts to a triple root of R, hence a
triple root -s/6 of f^(4). Four further lifts give a sevenfold root
of f. Balance and normalization therefore give the singleton/seven
orbit, contradicting Delta>0. Thus s=0. Now X=1/2 and
f^(4)(y)=y^2(1680y^2-180) has a double root at zero. Four lifts give
at least six original zero slopes. Balance and normalization force
exactly six zeros and the remaining two slopes +1/sqrt(2),-1/sqrt(2).
This is the moving-pair orbit. At Delta=0 the already classified
singleton/seven orbit has Gamma=0, and the credited pair also has
Gamma=0. This proves both directions of the complete equality set
and finishes Theorem 1. No full-disk optimizer classification follows
from this angular equality statement alone.

The finite
8x8 operator controls in verify.py check the credited pair via
H^3=(3/4)H, H^2w=(3/4)w and w^*Hw=0. There are two active opposite
eigenvalues with equal weights; all other full near eigenspaces have
zero coupling weight. Those controls do not replace the universal
moment/Gram argument.

## 3. An exact-energy original-root family and its cubic objective

The moving-pair construction, exact energy and local cubic/modulus
reduction were already proved in the all-degree cutoff work7328;
[LITERATURE.md](LITERATURE.md) records that earlier attribution.
We reproduce and specialize them before deriving the new cubic-energy
comparison. For the pair u_+,u_- corresponding to -exp(plus or minus it),
put x=1-cos(t). Direct arithmetic, using their conjugacy, gives
\[
E={4x\over d^2(d^2-2ax)},\quad
h=u_+u_-={1\over d^2-2ax},\quad
j=u_++u_-={2(d-x)\over d^2-2ax}.                         \tag{14}
\]
Solving the first identity gives exactly (2). Substitution then simplifies
\[
h=v^2+ae/2,\qquad j=2v+(a^2-1)e/2,\qquad
2h-2vj+2v^2=e.                                          \tag{15}
\]
The six fixed original roots contribute no energy.

Actual polynomial differentiation gives
\[
Q'=(z+1)^5D_3(z),
\]
\[
D_3=(z+1)(z^2+2cz+1)
 +(z-a)\{6(z^2+2cz+1)+(z+1)(2z+2c)\},\quad c=1-x.
\]
Normalizing q^3 D_3(a-1/q)/D_3(a) yields
\[
C_3(q)=q^3-(2j+7v)q^2+(3h+8vj)q-9vh,                  \tag{16}
\]
which is
\[
(q-v)^2(q-9v)+e\left\{{(2v-1)q^2\over v^2}
              +{(11-19v)q\over2v}-{9(1-v)\over2}\right\}.
\]
The far root q_f has constant 9v and simple derivative 64v^2 at e=0.
Analytic IFT and compactness give a real positive far branch uniformly
on a in [0,1]. The two near roots have sum 2j+7v-q_f and product
9vh/q_f. Their discriminant is
\[
(2j+7v-q_f)^2-36vh/q_f=-3e/2+O(e^2),                    \tag{17}
\]
uniformly on that interval. For small positive e they are a nonreal
conjugate pair, with positive product. Counting the five within-block
critical modes, the actual objective is therefore
\[
F(Q_{a,e})=5v+q_f+2\sqrt{9vh/q_f}.                       \tag{18}
\]
The square root has positive constant v. This expression extends
analytically in (a,e) near the compact zero-energy interval, without
labeling individual near roots on their square-root splitting scale.

Coefficient recursion in (16), or independently the far secular equation
\[
{jq_f-2h\over q_f^2-jq_f+h}+{6v\over q_f-v}=1,
\]
whose collapse derivative is -1/(8v), gives
\[
F(Q_{a,e})=16v+\kappa e-K_Qe^2+C_Qe^3+O(e^4),           \tag{19}
\]
\[
C_Q={1127d^8\over65536}-{6855d^7\over131072}
        +{52737d^6\over1048576}-{28853d^5\over2097152}.
\]
Both exact routes are checked entrywise in verify.py. The actual
analytic formula, rather than numerical eigenvalues, justifies a
uniform fourth-order energy remainder for this selected family.

## 4. The entire stationary branch and the cubic difference

The credited independent local audit supplies the complete mean polynomial
for P(t,w t^3), with E the actual family energy:
\[
F=16v+\kappa E-K_1E^2+t^6\{P_0+P_1w+5v^3w^2\}+O(t^8),
\]
\[
P_0={931v^3\over2}+{15897v^4\over8}-{168525v^5\over32}
                 -{9639v^6\over8}+{678993v^7\over128},
\quad P_1=-10v^3\beta.
\]
These coefficients retain their earlier credit. On the actual branch
w(a,e)=beta+O(e), and t^6=e^3/(56^3v^12)+O(e^4). Substitution uses
the entire actual mean and gives, uniformly on [0,1],
\[
F(P_{a,e})=16v+\kappa e-K_1e^2+C_Pe^3+O(e^4),           \tag{20}
\]
\[
C_P={P_0-5v^3\beta^2\over56^3v^{12}}
=-{297d^9\over35840}+{78387d^8\over1003520}
 -{741429d^7\over4014080}+{15471d^6\over100352}
 -{15303d^5\over458752}.
\]
The O(e) correction to w first affects the O(e^4) remainder; this
does not identify the exact nonlinear mean with its leading coefficient.
Our checker reconstructs the literal original residual quadratic and
its closed radical roots, includes all six within-block modes, and
reproduces the complete credited mean polynomial before this substitution.

Define C(a)=C_P(a)-C_Q(a) and D_0(a)=K_Q(a)-K_1(a). Equations
(19)--(20) yield the jointly analytic removable quotient
\[
H(a,e)={F(P_{a,e})-F(Q_{a,e})\over e^2}
       =D_0(a)+C(a)e+O(e^2),\qquad
D_0(a)=-{d^3P_G(a)\over114688}.                         \tag{21}
\]
Analyticity supplies uniform remainders on [0,1]. Exact quadratic-field
arithmetic with the positive sqrt(1614) proves
\[
{30800\over10^6}<C_G:=C(a_G)<{30802\over10^6}.           \tag{22}
\]
In particular C_G>0, so (20) exceeds (19) at the quartic tie for all
sufficiently small positive energy. No floating-point value enters
this sign or the following curve.

For completeness, prove the stronger uniform estimate (4). On [0,a_G],
\[
D_0(a)={d^3(a_G-a)\{2768(a_G+a)+3080\}\over114688}
       \ge m_*(a_G-a),\quad
m_*={2768a_G+3080\over114688}.
\]
Choose a fixed delta>0 so C(a)>=C_G/2 on [a_G-delta,a_G]. If the
uniform O(e^2) term in (21) is bounded by M e^2, reduce e so
M e<=C_G/4. On this terminal interval,
\[
H(a,e)\ge m_*(a_G-a)+(C_G/4)e.
\]
On the remaining compact interval, D_0 has a positive minimum, so
another common small energy bound gives H>=m_*(a_G-a)/2. Require
also e<=delta; there (a_G-a)+e<=2(a_G-a). Exact arithmetic checks
\[
\min\{m_*/4,C_G/4\}>{77\over10000}.
\]
Combining the two intervals proves (4) with one common existential
threshold. No positivity of C(a) on the whole interval is assumed.

## 5. The equal-value curve and the local/nonglobal consequence

At (a_G,0), H=0 and
\[
H_a=-{(1+a_G)^3(5536a_G+3080)\over114688}<0,\qquad
H_e=C_G>0.                                             \tag{23}
\]
Analytic IFT supplies the unique alpha(e). Its derivative is
\[
c_{\rm eq}={114688C_G\over(1+a_G)^3(5536a_G+3080)}>0.     \tag{24}
\]
The exact coefficient is an element of Q(sqrt(1614)), with its complete
rational/radical pair in expected.json. Exact field signs give the
two rational bounds in (5). Shrink a fixed common neighborhood so H_a
stays negative. For fixed positive small e it follows that H is positive
below alpha(e), zero there, and negative above. This proves Theorem 3.

Finally the numerator 1616a^2+1800a-1675 of the credited local stiffness
is strictly increasing for a>=0 and is positive at 151/250, whereas
P_G(151/250)<0. Thus a_*<151/250<a_G. The independent all-disk local
theorem applies on every compact J in (a_*,a_G] and on a common compact
neighborhood of a_G. Combine that strictness with (4) or the positive
side of (23)--(24) to obtain the corollary. Q is an actual different
admissible configuration at exactly the same energy, so it disproves
global minimality of P even though P remains locally strict.

A full-disk minimum at these small energy levels exists: reciprocals
lie in a compact ball about v bounded away from zero; the original
roots are the continuous transforms a-1/u, and the closed-disk
constraint plus E=e gives a compact nonempty level. The critical
reciprocal matrix has a continuous eigenvalue multiset, hence F is
continuous through all collisions. This observation identifies no
global optimizer.

## 6. Exact evidence and trust boundary

The self-contained standard-library checker uses exact Laurent/Gaussian
jets and quadratic-field sign comparisons. It verifies 157 identities,
17 strict signs and all 59 complete records, including the universal
Gram equality polynomial, reversed-quartic factor, a finite 8x8 pair
profile and eight rejected damaged mathematical expressions. Missing,
malformed or altered required fixtures fail under optimization.
The exact energy inverse, physical cubic, independent far secular route,
physical stationary quadratic, radical roots and credited mean-polynomial
controls have different mathematical roles; matching checks are not an
independent peer review of the new conclusions.

Uniform collision analysis, analyticity, compactness, IFT, interval
splitting, and the credited universal moment/Gram and local strictness
theorems remain ordinary mathematics. The global minimum theorem on
[5/8,1] remains credited and is not extended here to all a>a_G. The
all-motion stability of a competing branch and the actual global
transition near (a_G,0) remain open in this source.
