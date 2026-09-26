# Full small-mass Gaussian majorisation from nested convex hulls

Author proof, 26 September 2026. Independent review pending.
The unrestricted three-dimensional conjecture remains open.

## 1. Statements and scope

Let $\nu$ be a compactly supported probability measure in $\mathbb R^3$,
$P=\operatorname{supp}\nu$, and let $T:\{0\}\cup P\to\mathbb R^3$ be
1-Lipschitz with $T(0)=0$. Put $Q=T(P)$ and

$$
L=\max_{p\in P}|p|,\qquad r=\max_{q\in Q}|q|.
$$

For a fixed variance $s>0$, let $\phi_s(z)=(2\pi s)^{-3/2}e^{-|z|^2/(2s)}$,

$$
f_\varepsilon=((1-\varepsilon)\delta_0+\varepsilon\nu)*\phi_s,
\qquad
g_\varepsilon=((1-\varepsilon)\delta_0+\varepsilon T_\#\nu)*\phi_s.
\tag{1}
$$

Write $H_f(a)=\int(f-a)_+$ and $D_\varepsilon(a)=H_{g_\varepsilon}(a)-H_{f_\varepsilon}(a)$.

**Theorem A (nested hulls).** Suppose

$$
Q\subseteq\operatorname{conv}(P\cup\{0\}),\qquad r<L.
\tag{2}
$$

For every fixed $s>0$ there is $\varepsilon_*>0$ such that

$$
D_\varepsilon(a)\ge0
\quad\text{for every }0<\varepsilon\le\varepsilon_*\text{ and every }a\ge0.
\tag{3}
$$

The inequality is strict for $0<a<\max g_\varepsilon$. Thus $f_\varepsilon$
is fully majorised by $g_\varepsilon$. The upper bound on $\varepsilon$ may
depend on $\nu,T,s$; no uniformity in these data or numerical value of
$\varepsilon_*$ is asserted.

There is a weaker sufficient hypothesis. For a compact nonempty set $K$ let
$h_K(\theta)=\max_{x\in K}\theta\cdot x$, and define, using unnormalised
surface measure on $S^2$,

$$
M_K(c)=\int_{S^2}(h_K(\theta)-c)_+\,d\sigma(\theta),\qquad
\Delta(c)=M_P(c)-M_Q(c),\quad c\ge0.
\tag{4}
$$

**Theorem B (geometric criterion).** Conclusion (3), including strictness,
holds if $r<L$ and $\Delta(c)>0$ for every $c\in[0,r]$.

Theorem A follows from B. A geometric reduction valid without either
additional hypothesis is proved in Section 3: at variance one, uniformly in
$0<\varepsilon\le1/2$, with $R=\sqrt{2\log(C/a)}$ and $C=(2\pi)^{-3/2}$,

$$
\frac{D_\varepsilon(a)}{aR^2}
=\Delta\!\left(\frac{\log(1/\varepsilon)}{R}\right)+o(1),\qquad R\to\infty.
\tag{5}
$$

In particular, an anchored contraction with $\Delta(c)<0$ at any $c>0$
would give actual Gaussian counterexamples by taking
$\varepsilon=e^{-cR}$, $a=Ce^{-R^2/2}$ and $R$ sufficiently large.
No such negative example is claimed here.

Theorems A and B allow arbitrary compact supports, not only finite sets.
Section 6 applies A to the classical tetrahedron flaps, at every depth
$0<b\le2$, with arbitrary positive rare-atom weights. With a dominant
origin these examples still admit no continuous contracting motion in
$\mathbb R^5$. That nonliftability is an existing theorem of
[Cheng--Tan--Zheng, Theorem 2.1](https://arxiv.org/abs/1107.0140).

These statements address the Gaussian conjecture in
[Aishwarya--Li, Conjecture 1.1](https://arxiv.org/abs/2609.07041).
They improve our earlier
[small-mass threshold theorem](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_small_mass/PROOF.md)
to **all** thresholds under (2). The proof below is self-contained and does
not assume that earlier result. This is not an all-variance theorem at one
fixed positive $\varepsilon$, nor a new Kneser--Poulsen theorem: that would
require additional control as $s\downarrow0$.

## 2. Fixed positive threshold floors

It suffices to work at $s=1$. Scaling $z=\sqrt{s}\,y$ replaces $P,Q$ by
$P/\sqrt{s},Q/\sqrt{s}$ and $a$ by $s^{3/2}a$, preserving (2), the sign
condition in B, and hinge comparisons. Throughout the proof $s=1$.

The assumption $r<L$ implies $|Tx|<|x|$ on a set of positive $\nu$-measure.
Indeed a neighbourhood in $P$ of a point with norm $L$ has positive mass
and norm greater than $r$. Write $F_P=\nu*\phi$, $F_Q=T_\#\nu*\phi$.
Then

$$
F_Q(0)-F_P(0)=C\int(e^{-|Tx|^2/2}-e^{-|x|^2/2})\,d\nu(x)>0.
\tag{6}
$$

For $0<a<C$ and $R=\sqrt{2\log(C/a)}$, the regular level sphere of $\phi$
gives the first hinge variation

$$
A(a):=\left.\partial_\varepsilon D_\varepsilon(a)\right|_{\varepsilon=0}
=\int_{B_R}(F_Q-F_P)>0.
\tag{7}
$$

For completeness, Gaussian mass in a fixed centred ball strictly decreases
as the norm of its centre increases. Slice the ball perpendicular to that
centre. For each nondegenerate slice $[-b,b]$, the derivative of the
one-dimensional Gaussian mass at displacement $t>0$ is
$\phi_1(b+t)-\phi_1(b-t)<0$. Integrating the slices proves the assertion.
Apply it pointwise to $x,Tx$, then integrate. The strict radial loss noted
above proves strictness in (7).

On each compact subinterval of $(0,C)$, the implicit-function theorem
applied to the regular spheres gives
$D_\varepsilon(a)=\varepsilon A(a)+O(\varepsilon^2)$ uniformly in $a$.
The moving level sets stay in a fixed ball, their gradients stay bounded
away from zero, and the perturbing densities have bounded derivatives
there. Hence this Taylor assertion has no tail or critical-level issue.

There is a simpler argument near the moving maxima in the present
radial-loss case. By (6), $F_Q-F_P\ge d>0$ on some $B_\eta$.
Choose $a_1$ strictly between $Ce^{-\eta^2/2}$ and $C$. For all sufficiently
small $\varepsilon$, $f_\varepsilon<a_1$ outside $B_\eta$, since
$F_P\le C$. On $B_\eta$ we have
$g_\varepsilon-f_\varepsilon\ge\varepsilon d$.
For every $a\ge a_1$ this directly implies $H_g(a)\ge H_f(a)$.
It is strict when $a<\max f_\varepsilon$; when
$\max f_\varepsilon\le a<\max g_\varepsilon$, only the latter hinge is
positive. A maximum of $f_\varepsilon$ lies in $B_\eta$ after decreasing
$\varepsilon$ if needed, so $\max g_\varepsilon>\max f_\varepsilon$.

Together with (7), this proves: for each fixed $a_0>0$, all sufficiently
small positive $\varepsilon$ give $D_\varepsilon(a)>0$ whenever
$a_0\le a<\max g_\varepsilon$. All larger thresholds give zero or a
nonnegative gap. This also covers thresholds approaching either maximum.

## 3. Uniform tail asymptotic

We first prove (5) for an arbitrary fixed compact probability law $\tau$
supported on $K\subset B_L$. Write
$F_\varepsilon=(1-\varepsilon)\phi+\varepsilon(\tau*\phi)$ and
$\lambda=\log(1/\varepsilon)$, where $0<\varepsilon\le1/2$.

### Radial boundaries

For all sufficiently large $R$ the set $\{F_\varepsilon>Ce^{-R^2/2}\}$ is
star-shaped, with radial boundary $\rho(\theta)=R+\zeta(\theta)$ satisfying

$$
-1\le\zeta(\theta)\le L+1.
\tag{8}
$$

In fact $(1-\varepsilon)\phi>a$ throughout $B_{R-1}$, and the bound
$F_\varepsilon(t\theta)\le Ce^{-(t-L)^2/2}$ makes it less than $a$ for
$t\ge R+L+1$. For $t>L$,

$$
\partial_t\log F_\varepsilon(t\theta)
=-t+\mathbb E_{\mathrm{posterior}}[\theta\cdot X]\le-t+L<0,
\tag{9}
$$

where the posterior includes the atom at zero. Thus the boundary between
these two radii is unique and the entire superlevel set is as stated.
These statements are uniform in $\varepsilon$.

### Uniform Laplace principle

Compact support with full support on $K$ gives

$$
\frac1t\log\int e^{t\theta\cdot x-|x|^2/2}\,d\tau(x)
\longrightarrow h_K(\theta)
\quad\text{uniformly in }\theta\in S^2.
\tag{10}
$$

For the upper bound use $\theta\cdot x\le h_K(\theta)$. For any $\delta>0$,
compactness of $S^2$ and continuity of its support function supply finitely
many angular neighbourhoods and corresponding positive-mass neighbourhoods
in $K$ on which $\theta\cdot x\ge h_K(\theta)-\delta$. The minimum of those
finitely many positive masses is positive. This gives a uniform lower
bound $m_\delta e^{t(h_K(\theta)-\delta)-L^2/2}$ and proves (10).

At the boundary the defining equation is

$$
R\zeta+\frac{\zeta^2}{2}
=\log\left(1-\varepsilon+
 e^{-\lambda}\int e^{(R+\zeta)\theta\cdot x-|x|^2/2}\,d\tau(x)\right).
\tag{11}
$$

By (8)--(10), division by $R$ yields

$$
\zeta(\theta)=\left(h_K(\theta)-\frac\lambda R\right)_++o(1)
\tag{12}
$$

uniformly in both $\theta$ and $0<\varepsilon\le1/2$. To see explicitly why
the second uniformity holds, if the rare logarithm is $R(h_K-\lambda/R)+e_R$
with $|e_R|=o(R)$, then taking its log-sum with a number in $[1/2,1]$
differs from $R(h_K-\lambda/R)_+$ by at most $|e_R|+\log2$.
No upper bound on $\lambda/R$ is required.

### Hinge deficit, including the outside mass

Let $V$ be the superlevel volume. Polar integration and (12) give

$$
V=\frac{4\pi}{3}R^3+R^2M_K(\lambda/R)+o(R^2)
\tag{13}
$$

uniformly in $\varepsilon$. The part of the probability mass outside the
superlevel set cannot be discarded without a bound. By (9), for $u\ge0$,

$$
F_\varepsilon((\rho(\theta)+u)\theta)
\le a e^{-(\rho(\theta)-L)u-u^2/2}.
$$

Consequently its integral is $O(aR)$, uniformly in $\varepsilon$, by
integrating $(\rho+u)^2e^{-(\rho-L)u}$ and using $\rho=R+O(1)$.
Since $F_\varepsilon$ has total mass one,

$$
\frac{1-H_{F_\varepsilon}(a)}a
=V+\frac1a\int_{\{F_\varepsilon\le a\}}F_\varepsilon
=\frac{4\pi}{3}R^3+R^2M_K(\lambda/R)+o(R^2).
\tag{14}
$$

Subtract the two versions of (14). The sign is
$H_g-H_f=(1-H_f)-(1-H_g)$, which proves (5).

### An explicit finite-mixture bound

If $\tau=\sum_iw_i\delta_{x_i}$, $w_i\ge w_*>0$ and $|x_i|\le\widehat L$,
put

$$
B=\widehat L+1,\qquad
E=\log(2/w_*)+\widehat L B+\widehat L^2/2+B^2/2,
\qquad K_{\rm err}=E+B^2+B^3/3+40.
$$

For $R\ge2B$, (11) gives
$|\zeta-(h_K-\lambda/R)_+|\le E/R$:
bound the rare sum above by its largest exponential and below by the
largest exponential times $w_*$, using $|\zeta|\le B$.
Expanding $(R+\zeta)^3/3$ proves a volume error at most
$4\pi R(E+B^2+B^3/3)$. The outside mass is at most $4\pi a\,40R$:
use $\rho\le2R$, $k=\rho-\widehat L\ge R/2$ and
$\rho^2/k+2\rho/k^2+2/k^3\le40R$. Thus

$$
\left|\frac{1-H_{F_\varepsilon}(a)}a-\frac{4\pi}{3}R^3
-R^2M_K(\lambda/R)\right|\le4\pi K_{\rm err} R.
\tag{15}
$$

For a pair of mixtures with a common bound $K_{\rm err}$, (15) bounds the
error in $D/(4\pi aR^2)$ by $2K_{\rm err}/R$.

## 4. The transition estimate from a shell

Suppose $r<L$, and fix any $m$ strictly between them. In this section only,
parametrise a threshold by the central Gaussian itself:

$$
a=(1-\varepsilon)C e^{-\rho^2/2}.
\tag{16}
$$

For a compact law $\tau$ define the increase in its capped integral over
the central Gaussian by

$$
J_\tau=\int\left[\min((1-\varepsilon)\phi+\varepsilon(\tau*\phi),a)
-\min((1-\varepsilon)\phi,a)\right].
$$

Inside $B_\rho$ the integrand vanishes. Outside, it is exactly

$$
\min\{\varepsilon(\tau*\phi)(z),\ a-(1-\varepsilon)\phi(z)\}.
\tag{17}
$$

The common central term cancels, and $D_\varepsilon(a)=J_\nu-J_{T_\#\nu}$.

Pick $p\in P$ with $|p|=L$. There are an angular cap $\Omega$ of positive
area and a neighbourhood $U$ of $p$ with $\nu(U)>0$ such that
$\theta\cdot x\ge m$ for $\theta\in\Omega$, $x\in U$. On the shell
$\rho+1/\rho\le t\le\rho+2/\rho$, for $\rho\ge1$, the free amount
$a-(1-\varepsilon)\phi(t\theta)$ is at least $(1-e^{-1})a$, while

$$
\varepsilon(\nu*\phi)(t\theta)
\ge a\varepsilon\nu(U)e^{m\rho-L^2/2-4}.
$$

The radial volume of the shell per unit solid angle is at least $\rho$.
Equation (17) therefore gives a constant $k_0>0$, independent of
$\varepsilon,\rho$, such that

$$
J_\nu\ge k_0 a\rho\min\{\varepsilon e^{m\rho},1\}.
\tag{18}
$$

Conversely, $Q\subset B_r$ gives

$$
J_{T_\#\nu}\le\varepsilon\int_{|z|\ge\rho}(T_\#\nu*\phi)(z)
\le k_1a\rho\varepsilon e^{r\rho}
\tag{19}
$$

for all sufficiently large $\rho$, uniformly in $0<\varepsilon\le1/2$.
One direct bound is
$4\pi C\int_\rho^\infty t^2e^{-(t-r)^2/2}\,dt$ for the tail probability;
write $t=\rho+u$, dominate by
$e^{-(\rho-r)^2/2}e^{-(\rho-r)u}$, and integrate the quadratic polynomial.
Finally use $Ce^{-\rho^2/2}=a/(1-\varepsilon)\le2a$.

If $\rho\le\lambda/m$, the minimum in (18) equals
$\varepsilon e^{m\rho}$. The ratio of (18) to (19) is at least
$(k_0/k_1)e^{(m-r)\rho}$. Thus there is a **fixed** $\rho_0$ such that

$$
D_\varepsilon(a)>0\quad\text{whenever}\quad
\rho_0\le\rho\le\lambda/m,quad 0<\varepsilon\le1/2.
\tag{20}
$$

This estimate covers the place where the rare Gaussian first affects the
far boundary; it does not rely on a Taylor expansion in $\varepsilon$ there.

## 5. Completing the geometric criterion and the nested-hull theorem

Each $M_K$ is continuous (indeed $4\pi$-Lipschitz) as a function of $c$.
The hypothesis in B therefore supplies $m\in(r,L)$ and $\eta>0$ with
$\Delta(c)\ge\eta$ for all $c\in[0,m]$.

Choose a large fixed $\rho_0$ for (20), and fix
$a_0=(C/2)e^{-\rho_0^2/2}$. Section 2 handles all $a\ge a_0$ for small
$\varepsilon$. Every remaining positive threshold can be written as (16)
with $\rho>\rho_0$, since $1-\varepsilon\ge1/2$.
If $\rho\le\lambda/m$, use (20). Otherwise, with the reference radius in
Section 3,

$$
R^2=\rho^2-2\log(1-\varepsilon)\ge\rho^2,
\qquad \lambda/R<m.
$$

Moreover $R\ge\lambda/m\to\infty$ as $\varepsilon\downarrow0$.
Uniformity in (5) now gives
$D_\varepsilon(a)/(aR^2)\ge\eta/2>0$, simultaneously at every threshold in
this last regime, after a single further decrease of $\varepsilon_*$.
At $a=0$ both hinges equal one. This proves B and its strictness claim.

Under (2), $(h_P-c)_+\ge(h_Q-c)_+$ pointwise for every $c\ge0$.
Set $m=(L+r)/2$, $\beta=(L-r)/4$, and choose $p\in P$ with $|p|=L$.
On the cap $\theta\cdot p\ge m+\beta$ the difference of the positive parts
is at least $\beta$ for all $0\le c\le m$, because $h_Q\le r$.
This cap has area $2\pi\beta/L$. In particular

$$
\Delta(c)\ge\frac{\pi(L-r)^2}{8L}>0,
\qquad 0\le c\le(L+r)/2.
\tag{21}
$$

Apply B. This proves A without assuming a general monotonicity theorem for
truncated support functions.

The function in (4) has the geometric interpretation
$M_P(c)=\int_{S^2}h_{\operatorname{conv}(P\cup cB)}\,d\sigma-4\pi c$.
Ordinary mean-width monotonicity under contractions does not by itself
compare these bodies: an extension of $T$ need not map the added ball onto
itself. That sign question remains open in this work.

For finite $P$ the same coefficient has a direct unequal-ball interpretation.
Fix $c\ge0$ and let

$$
W_P(R,c)=B(0,R)\cup\bigcup_{p\in P}B(p,R-c).
$$

For $R>c+L$ all these balls contain the origin. The radial endpoint of the
ball about $p$ is
$\theta\cdot p+\sqrt{(R-c)^2-|p|^2+(\theta\cdot p)^2}
=R+\theta\cdot p-c+O(1/R)$, uniformly in direction and label.
Taking the maximum with $R$ and integrating its cube gives

$$
|W_P(R,c)|=4\pi R^3/3+R^2M_P(c)+O(R).
\tag{21a}
$$

Thus a strictly negative $\Delta(c)$ for a finite anchored contraction
would also violate the unequal-radius Kneser--Poulsen inequality for these
large balls. Under nesting, the positive leading sign in (21a) follows
from the geometric containment hypothesis; we do not claim a new general
Kneser--Poulsen consequence from it.

During the final publication refresh, researcher 5 independently published
a [spherical tail and ball-hull theorem](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_spherical_tail/PROOF.md).
It treats fixed laws as variance tends to infinity, and relates comparison
of spherical log-Laplace averages for every weight vector to mean widths of
ball hulls with arbitrary radius offsets. Our $M_P(c)$ is the special
offset pattern with offset zero at the origin and offset $-c$ at every rare
point. The shared geometric test is complementary context; our uniform
fixed-variance, vanishing-mass limit and the all-threshold completion in
Theorems A--B are not conclusions of that result. Its complete proof and
scope were inspected before this contribution's graph submission.

## 6. Classical nonliftable flaps: every depth from zero to two

Take

$$
u_0=(1,1,1),\ u_1=(1,-1,-1),\ u_2=(-1,1,-1),\ u_3=(-1,-1,1).
$$

For $b>0$ let $P_b$ consist of the four fixed anchors $u_i$ and twelve
outward flap vertices $p_{ij}=u_j-bu_i$, $i\ne j$; send them to the same
anchors and $q_{ij}=u_j+bu_i$. Add $0\mapsto0$.
Since $u_i\cdot u_j=4\mathbf1_{i=j}-1$, the squared-distance deficits are

$$
\begin{array}{c|c}
\text{pair}&|x-x'|^2-|Tx-Tx'|^2\\ \hline
0,\ p_{ij}&4b\\
u_k,\ p_{ij}&16b\mathbf1_{k=i}\\
p_{ij},\ p_{kl}&16b(\mathbf1_{j=k}+\mathbf1_{l=i})
\end{array}
\tag{22}
$$

Pairs involving only fixed points have deficit zero. Thus this is an
anchored contraction for every $b>0$. It extends to an ambient
1-Lipschitz map by the classical Euclidean Kirszbraun extension theorem;
only its specified values are used here.

The extreme radii satisfy

$$
L_b^2=3+2b+3b^2,\qquad r_b^2=\max\{3,3-2b+3b^2\}<L_b^2.
\tag{23}
$$

For any direction sort its four tetrahedral projections as
$A\ge B\ge C\ge D$ with $A+B+C+D=0$. Then

$$
h_{P_b}=A-bD,
\qquad h_{Q_b}=\begin{cases}
\max\{A,A+bB\},&0<b\le1,\\
\max\{A,bA+B\},&b\ge1.
\end{cases}
\tag{24}
$$

The outward expression exceeds $A$, since $D\le0$. With nonnegative gaps
$u=A-B$, $v=B-C$, $w=C-D$, its excess over the other expression in (24) is

$$
\begin{cases}
b(u+w)/2,&0<b\le1,\\
((2-b)u+bw)/2,&1\le b\le2.
\end{cases}
\tag{25}
$$

Thus $Q_b\subseteq\operatorname{conv}P_b$ for $0<b\le2$.
For $b>2$ nesting fails in a direction with projections $(3,-1,-1,-1)$;
this is a failure of the sufficient hypothesis, not a majorisation
counterexample.

**Corollary.** Fix $0<b\le2$, any positive weights on all sixteen labels
of $P_b$, and any $s>0$. For all sufficiently small positive
$\varepsilon$, (1) gives full Gaussian majorisation for this contraction,
with strict hinge gap at every $0<a<\max g_\varepsilon$.

The paired affine rank is six for every $b>0$. The origin is a paired
point; the six paired rows given by anchors $u_0,u_1,u_2$ and flaps
$p_{03},p_{13},p_{23}$ have determinant $128b^3$.
More significantly, the sixteen-label subconfiguration has no continuous
contraction in dimension below six, by reversing
[Cheng--Tan--Zheng, Theorem 2.1](https://arxiv.org/abs/1107.0140).
Adding the fixed origin cannot remove that obstruction. Therefore the
corollary is not obtained by lifting this configuration to a continuous
contraction in dimension five. Neither the flap construction nor its
nonliftability is new here.

There is also a simple way to exclude a different deterministic matching
of the same two atomic laws. Index the sixteen rare input labels by
$j=0,\ldots,15$ and give them weights $2^j/(2^{16}-1)$. Take
$0<\varepsilon<1/2$. The atom at zero has mass greater than one half, so
any deterministic map with the prescribed output law must send it to zero.
It cannot send any other atom there. At each nonzero output point, the
remaining required mass specifies a sum of distinct powers of two, which
has a unique representing subset of input labels. Therefore every such
map agrees with the specified contraction on the entire input support.
This argument includes coincident output labels, such as $q_{ij}=q_{ji}$
when $b=1$. For these weights, no alternative deterministic realization of
the same pair of measures has paired rank at most five or an $\mathbb R^5$
continuous contraction.

This qualification matters because the concurrently published
[balanced-ray theorem](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_ray_relabelling/PROOF.md)
does obtain full majorisation for a different ray class by changing the
contracting realization while preserving its output law. Its balanced ray
conditions permit arbitrary mass at zero and every variance; its proof
does not permit the four fixed tetrahedron anchors here. The uniqueness
argument above excludes that deterministic-rematching route for a concrete
subclass of our theorem. It does not exclude other proof methods.

### A concrete rational tail certificate

At $b=1$, $L=\sqrt8$, $r=2$. Choose any outward vertex $p$ and the cap
$\theta\cdot p/\sqrt8\ge15/16$. Its area is $\pi/8$, and on it
$h_P\ge21/8$ because $8(15/16)^2>(21/8)^2$. Equations (24)--(25) imply
pointwise domination elsewhere. For $0\le c\le5/2$ it follows that

$$
\Delta(c)/(4\pi)\ge1/256.
\tag{26}
$$

For uniform rare weights $1/16$, take $\widehat L=3$, $B=4$ in (15).
Since $\log2<7/10$, $E<28$, and hence $2K_{\rm err}<632/3$.
For all $0<\varepsilon\le1/2$, $R\ge65536$, and
$\log(1/\varepsilon)/R\le5/2$, we consequently have

$$
\frac{D_\varepsilon(Ce^{-R^2/2})}{4\pi Ce^{-R^2/2}R^2}
>\frac1{256}-\frac{632}{3\cdot65536}
=\frac{17}{24576}>0.
\tag{27}
$$

This deliberately coarse bound checks an actual continuous tail region.
It is not a numerical value of the all-threshold $\varepsilon_*$.

## 7. Verification and dependencies

`verify.py` uses only Python integer and rational arithmetic. It checks
all 136 augmented-flap squared-distance polynomials; the degree-three
paired determinant; the radius and support-gap identities for the entire
depth intervals; an independent barycentric hull certificate at depth one;
and every rational inequality in (26)--(27). It checks degenerate depth zero
and a depth-three failure of nesting, and decodes the uniquely forced
matching for the binary rare weights at depth one. None of these checks samples or proves
the analytic uniformity in Sections 2--5: that is the written proof above.

The primary problem is
[Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/abs/2609.07041v2).
The geometric fixture and its nonliftability are from
[Cheng--Tan--Zheng, arXiv:1107.0140](https://arxiv.org/abs/1107.0140).
[Gorbovickis, arXiv:1006.0531](https://arxiv.org/abs/1006.0531) treats strict
ordinary mean-width comparison and large congruent balls. It is relevant
background, not a premise for the truncated comparison proved under (2).
Our earlier small-mass packet motivates the present tail analysis but is
not a logical premise. The teammate
[symmetric-flap quartic theorem](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_symmetric_flap_quartics/PROOF.md)
covers a different parameter regime: it gives quartic energies at every
scale for symmetric weights. Here all hinges are controlled near a dominant
atom, with arbitrary positive rare weights. We do not use the false
instantaneous positivity condition refuted in the
[local-lift obstruction](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_local_lift_obstruction/PROOF.md).
The later [sparse-energy theorem](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_replica_curvature_sparse_energies/PROOF.md)
compares convex polynomials with at most three nonlinear terms in every
degree when $s\ge2R_{\rm support}^2/5$, and sharpens the quartic range.
It was read at publication refresh and is complementary, not a premise.

No proof assistant, external solver, numerical quadrature or unpublished
data is required. The claim is an author proof with exact supplementary
checks, not an independently reviewed or formally verified theorem.
