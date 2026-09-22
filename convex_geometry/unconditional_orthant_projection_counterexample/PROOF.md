# A counterexample to the unconditional orthant projection conjecture

Discovery Net researcher 6, 22 September 2026.

## Statement and scope

Write $K_+=K\cap[0,\infty)^m$. Here an **unconditional** convex body
is invariant under independent changes of coordinate signs; permutation
invariance is not assumed. Volumes of projections use Euclidean measure
on the target subspace.

Fradelizi, Manui, Mark Meyer and Ndiaye formulate the inequality

$$
|P_EK|_n\leq 2^n|P_EK_+|_n                                      \tag{1}
$$

for all unconditional convex bodies $K\subset\mathbb R^m$ and
$n$-dimensional subspaces $E$ as Conjecture 3 of
[arXiv:2607.03582v1](https://arxiv.org/html/2607.03582v1#S1.SS2).
We give a counterexample in the smallest possible ambient dimension.
Together with the known line and hyperplane cases, this determines
exactly the dimension pairs for which (1) holds universally.

**Theorem.** For $1\leq n\leq m$, (1) holds for every such $K,E$
if and only if $n=1$ or $m-n\leq1$. In every other dimension pair there
are examples with

$$
\frac{|P_EK|_n}{2^n|P_EK_+|_n}
 =\left(\frac{61}{60}\right)^{\lfloor\min(n,m-n)/2\rfloor}>1.       \tag{2}
$$

The basic example in $\mathbb R^4$, projected onto a plane, is the
convex hull of three coordinate boxes. A one-parameter family describes
its failure mechanism. There is also an explicit unconditional body in
$\mathbb R^4$ with smooth boundary and positive Gaussian curvature
violating (1).

The line and hyperplane positive results are already Propositions 4
and 3 of the cited paper. Section 5 recalls proofs to make the dimension
classification self-contained. No optimal replacement constant is
asserted. This example does not settle the narrower $\ell_q$-ball or
asymmetric $L_p$-zonoid conjectures (Conjectures 2 and 1).

## 1. Positive parts of convex hulls of boxes

Let $w_j=(w_{j1},\ldots,w_{jm})$ have nonnegative coordinates, and put

$$
B_j=\prod_i[-w_{ji},w_{ji}],\quad
D_j=\prod_i[0,w_{ji}],\quad K=\operatorname{conv}\bigcup_j B_j.
$$

Then

$$
K_+=\operatorname{conv}\bigcup_j D_j.                            \tag{3}
$$

To prove this, first observe that $D=\operatorname{conv}\bigcup_jD_j$
is closed under coordinatewise decrease within the positive orthant.
Indeed, if $z=\sum_j\lambda_j y_j$, $y_j\in D_j$, and $0\leq x\leq z$,
set $\theta_i=x_i/z_i$ when $z_i>0$, and $\theta_i=0$ otherwise.
Then $x=\sum_j\lambda_j(\theta_i y_{ji})_i\in D$.
For $x\in K_+$, choose $x=\sum_j\lambda_j z_j$ with $z_j\in B_j$.
Coordinatewise,
$0\leq x\leq\sum_j\lambda_j|z_j|\in D$, so $x\in D$.
The reverse inclusion follows from $D_j\subset K_+$ and convexity.

Thus both $AK$ and $AK_+$ can be obtained by applying a linear map
$A$ to finitely many box corners. We never interchange projection
and intersection with an orthant.

## 2. The four-dimensional example and the actual orthogonal plane

For $17/6\leq t\leq3$ define

$$
\begin{aligned}
B_0&=[-1,1]^4,\\
B_1(t)&=[-1,1]\times[-t,t]\times\{0\}\times\{0\},\\
B_2&=\{0\}^3\times[-3,3],\\
K_t&=\operatorname{conv}(B_0\cup B_1(t)\cup B_2).
\end{aligned}                                                    \tag{4}
$$

These are full-dimensional unconditional convex bodies: each box is
sign-invariant, and $K_t$ contains $B_0$.
Consider

$$
A=\begin{pmatrix}2&0&-2&1\\0&2&0&3\end{pmatrix},
\qquad E=\operatorname{row}(A)\subset\mathbb R^4.
$$

Its Gram matrix and orthogonal projector are

$$
AA^{\mathsf T}=\begin{pmatrix}9&3\\3&13\end{pmatrix},\quad
\det(AA^{\mathsf T})=108,
$$

$$
P_E=A^{\mathsf T}(AA^{\mathsf T})^{-1}A
 =\frac1{27}
\begin{pmatrix}
13&-3&-13&2\\
-3&9&3&12\\
-13&3&13&-2\\
2&12&-2&19
\end{pmatrix}.                                                   \tag{5}
$$

In particular $A=A P_E$, and $A|_E$ is an isomorphism with
area Jacobian $\sqrt{108}=6\sqrt3$. For every measurable $S$,

$$
|AS|_2=6\sqrt3\,|P_ES|_2.                                        \tag{6}
$$

Consequently all area ratios below are ratios for genuine orthogonal
projections, even though $A$ itself is not an orthogonal projection.

## 3. Polygon calculation and the two added triangles

In counterclockwise order the polygons
$P_t=AK_t$ and $Q=A(K_t)_+$ have vertices

$$
\begin{aligned}
P_t:\;&(-5,-5),\,(-3,-9),\,(2,-2t),\,(3,-5),\,(5,1),\\
     &(5,5),\,(3,9),\,(-2,2t),\,(-3,5),\,(-5,-1),\\
Q:\;&(-2,0),\,(2,0),\,(3,3),\,(3,9),\,(-1,5),\,(-2,2).
\end{aligned}                                                    \tag{7}
$$

At $t=17/6$ the third and eighth listed points of $P_t$ are collinear
with their neighboring points and may be omitted.
Here are direct ways to check both the vertex lists and their areas.

The image of $B_0$ is the zonotope
$[-2,2]\times\{0\}+\{0\}\times[-2,2]+[-2,2]\times\{0\}
+[-(1,3),(1,3)]$.
Adding $AB_2=[-(3,9),(3,9)]$ gives the octagon

$$
P_0:\quad (-5,-5),(-3,-9),(3,-5),(5,1),
          (5,5),(3,9),(-3,5),(-5,-1).                            \tag{8}
$$

The notation $P_0$ in (8) means the base polygon before adding $B_1(t)$.
It has area $120$ by the shoelace formula.
The positive image of this base body is $Q$: apply (3) to the
positive unit cube and the segment $[0,3e_4]$.
For example its six facet inequalities are

$$
y\geq0,\quad y\geq3x-6,\quad x\leq3,\quad
y\leq x+6,\quad y\leq3x+8,\quad x\geq-2.                         \tag{9}
$$

Every image of a positive cube corner and of $3e_4$ satisfies these
inequalities, and every vertex in (7) is one of these images.
The shoelace sum for $Q$ is $60$, giving $|Q|_2=30$.
The additional positive rectangle $AB_1(t)_+=[0,2]\times[0,2t]$
satisfies (9) whenever $t\leq3$. Thus the positive image stays fixed.

The full added rectangle is $[-2,2]\times[-2t,2t]$.
For $17/6<t\leq3$, just two of its corners lie outside $P_0$:
$(2,-2t)$ and $(-2,2t)$.
They add triangles along the edges from $(-3,-9)$ to $(3,-5)$
and from $(3,9)$ to $(-3,5)$ respectively. Each triangle has area

$$
\frac12\left|\det\big((6,4),(5,9-2t)\big)\right|=6t-17.
$$

All the remaining facet inequalities continue to hold; this can
also be checked directly from the ten listed vertices and the
box corners. Therefore

$$
|P_t|_2=120+2(6t-17)=86+12t,\qquad |Q|_2=30,                    \tag{10}
$$

and

$$
\frac{|P_EK_t|_2}{4|P_E(K_t)_+|_2}
 =\frac{43+6t}{60}>1\qquad (17/6<t\leq3).                       \tag{11}
$$

In particular, at $t=3$,

$$
|AK_3|_2=122,\quad |A(K_3)_+|_2=30,\quad
\frac{|P_EK_3|_2}{|P_E(K_3)_+|_2}=\frac{61}{15}>4.              \tag{12}
$$

The actual Euclidean projection areas are
$61/(3\sqrt3)$ and $5/\sqrt3$; their excess in (1) is
$1/(3\sqrt3)>0$.

**Exact finite certificate.** The companion verifier enumerates every
corner of all three boxes and checks every supporting-edge determinant
against every image generator. It also verifies that each proposed
polygon vertex is an image generator. These two inclusions identify
the convex hull exactly. Shoelace areas are cross-checked by vertical
sections of the raw image generators, without using the polygon lists.
An extremum of such a section uses at most two generators (a linear
program with the two constraints on total weight and horizontal
coordinate); the upper and lower hull boundaries are linear between
successive generator horizontal coordinates.

The verifier checks the whole parameter interval by its endpoints:
all labeled generator and proposed vertex horizontal coordinates are
fixed, while vertical coordinates are affine in $t$. Every supporting
determinant is therefore affine in $t$. Nonnegativity at both endpoints
proves nonnegativity throughout. The two moving polygon vertices are
the displayed rectangle corners for every $t$; all other vertices are
fixed base generators. This explains why endpoint testing here is a
continuum certificate rather than sampling.

## 4. Every remaining dimension pair and amplification

Let $d=m-n$ and suppose $n,d\geq2$. Put
$k=\lfloor\min(n,d)/2\rfloor\geq1$.
In mutually orthogonal coordinate blocks, take

$$
\begin{aligned}
\widetilde K&=K_3^k\times[-1,1]^{n-2k}
                         \times[-1,1]^{d-2k}\subset\mathbb R^m,\\
\widetilde E&=E^k\oplus\mathbb R^{n-2k}\oplus\{0\}^{d-2k}.
\end{aligned}
$$

A zero exponent means the corresponding factor is absent.
Positive parts and these orthogonal projections commute with the
Cartesian product, and the projected volumes multiply. Each
four-dimensional block contributes ratio $61/15$, each fully
projected coordinate interval contributes $2$, and hidden coordinate
intervals contribute $1$. Thus

$$
\frac{|P_{\widetilde E}\widetilde K|_n}
     {|P_{\widetilde E}\widetilde K_+|_n}
 =\left(\frac{61}{15}\right)^k2^{n-2k}
 =2^n\left(\frac{61}{60}\right)^k.
$$

This proves the negative direction of the classification and (2).

## 5. The known positive cases

These cases are included for completeness and are not new claims.
When $m=n$, the coordinate orthants partition $K$ into $2^m$
congruent pieces up to measure-zero boundaries, giving equality.

For a line $E=\mathbb Ru$ with $|u|=1$, unconditionality gives
$h_K(u)=h_K(|u|)$. Choose $x\in K_+$ with
$|u|\cdot x=h_K(|u|)$.
Coordinatewise decrease preserves $K_+$, since averaging coordinate
sign changes and convexity preserves $K$. Keeping separately the
coordinates where $u_i$ is nonnegative or negative shows

$$
h_{K_+}(u)+h_{K_+}(-u)
 \geq\sum_i |u_i|x_i=h_K(u).
$$

The projected lengths are respectively $2h_K(u)$ and
$h_{K_+}(u)+h_{K_+}(-u)$, proving (1) for $n=1$.

For the hyperplane case, first let $K\subset\mathbb R^m$ be an
unconditional polytope with nonempty interior. Let $\Gamma$ be the
part of its boundary in the strictly positive orthant; write $\nu$
for its outer unit normal and $dS$ for surface area.
Its normal coordinates are nonnegative: decreasing any positive
coordinate of a point of $K$ stays in $K$.
The remaining facets of $K_+$ are the coordinate cuts
$F_i=K_+\cap\{x_i=0\}$. The balance of facet normals gives
$|F_i|_{m-1}=\int_\Gamma\nu_i\,dS$.

Cauchy's projection formula, or equivalently counting the two
endpoints of almost every line through a projected point, now gives
for a unit normal $u$,

$$
\begin{aligned}
|P_{u^\perp}K|_{m-1}
 &=2^{m-1}\int_\Gamma
       \mathbb E_\varepsilon\left|\sum_i\varepsilon_i u_i\nu_i\right|dS,\\
|P_{u^\perp}K_+|_{m-1}
 &=\frac12\int_\Gamma
       \left(\left|\sum_i u_i\nu_i\right|+\sum_i|u_i\nu_i|\right)dS.
\end{aligned}                                                    \tag{13}
$$

Here the signs $\varepsilon_i$ are independent and uniform.
For arbitrary real $a_i$ we have

$$
\mathbb E\left|\sum_i\varepsilon_i a_i\right|
\leq\frac{\sum_i|a_i|+|\sum_i a_i|}{2}.                          \tag{14}
$$

Indeed, group positive and negative $a_i$, and let their total
absolute masses be $a,b\geq0$. The corresponding signed sums are
independent, centered random variables in $[-a,a]$ and $[-b,b]$.
A centered random variable in $[-a,a]$ is dominated for every
convex function by the uniform distribution on $\{-a,a\}$:
apply the secant-line bound and take expectations.
Apply this fact successively to the absolute value of the sum.
Its expectation is at most
$\mathbb E|a\varepsilon+b\delta|=\max(a,b)$, which equals
the right side of (14). Zero groups cause no difficulty.

Substituting (14) into (13) proves the factor $2^{m-1}$.
For a general unconditional body, approximate it by unconditional
polytopes containing the origin in their interiors. Such approximants
can be obtained as convex hulls of finite sign orbits of increasingly
dense boundary samples. Since $K$ contains a ball about the origin,
Hausdorff convergence can be sandwiched by dilates
$(1-\epsilon)K$ and $(1+\epsilon)K$.
Intersecting with the positive orthant and projecting preserves
these inclusions, so projected volumes converge. The inequality
passes to the limit. This completes the positive direction.

## 6. An explicit smooth counterexample

The failure is stable under smoothing. Here is a formula with a
verified rational margin, without relying only on qualitative
approximation. Fix the half-width rows of (4) at $t=3$:

$$
w_0=(1,1,1,1),\quad w_1=(1,3,0,0),\quad w_2=(0,0,0,3).
$$

For an integer $k\geq1$ and $u\in\mathbb R^4$, set

$$
s_{j,k}(u)=\sum_{i=1}^4w_{ji}
       \sqrt{u_i^2+|u|^2/k^2},\qquad
h_k(u)=\left(\sum_{j=0}^2s_{j,k}(u)^{2k}\right)^{1/(2k)}.         \tag{15}
$$

Each square root is the support function of a full-dimensional
centered ellipsoid. Thus $s_{j,k}$ is a support function and
$h_k$ is the support function of their Firey $L_{2k}$ sum; alternatively,
subadditivity follows directly from the $\ell_{2k}$ triangle
inequality and coordinatewise monotonicity of that norm.
Let $K^{(k)}$ be the body with support function $h_k$.
It is unconditional.

For completeness, the claimed regularity is stronger than strict
convexity alone. Every ellipsoid term is smooth away from the origin.
For a positive definite matrix $T$, the Hessian of
$u\mapsto\sqrt{u^{\mathsf T}Tu}$ is positive on every nonzero
direction not parallel to $u$, by the strict Cauchy--Schwarz
inequality for $T$. Hence each $D^2s_{j,k}(u)$ is positive definite
on $u^\perp$. The outer $\ell_{2k}$ norm is smooth on the strictly
positive vector $(s_{j,k}(u))_j$, convex, and has positive partial
derivatives. The chain rule shows that $D^2h_k(u)$ is also positive
definite on $u^\perp$. The support parametrization
$u\mapsto\nabla h_k(u)$ on the unit sphere therefore gives a smooth
strictly convex boundary with positive principal radii and positive
Gaussian curvature.

Write $h=h_{K_3}=\max_j\sum_iw_{ji}|u_i|$.
The row sums of $w_j$ are at most $4$, and $h(u)\geq|u|$ because
$K_3$ contains the unit cube. Using
$|u_i|\leq\sqrt{u_i^2+|u|^2/k^2}\leq|u_i|+|u|/k$ gives

$$
h(u)\leq h_k(u)
\leq3^{1/(2k)}(1+4/k)h(u).
$$

Thus, with $\lambda_k=3^{1/(2k)}(1+4/k)$,

$$
K_3\subset K^{(k)}\subset\lambda_kK_3.
$$

The same inclusions hold after taking positive parts. Monotonicity
and degree-two homogeneity of the two projected areas imply

$$
\frac{|P_EK^{(k)}|_2}{4|P_E(K^{(k)})_+|_2}
\geq\frac{61}{60\lambda_k^2}.                                  \tag{16}
$$

Take $k=1000$. The strict binomial inequality
$(501/500)^{1000}>1+1000/500=3$ yields

$$
\lambda_{1000}^2
=3^{1/1000}(251/250)^2
<\frac{501}{500}\left(\frac{251}{250}\right)^2
=\frac{31563501}{31250000}
<\frac{61}{60}.
$$

In particular the ratio in (16) is strictly greater than
$95312500/94690503>1$. Formula (15) with $k=1000$ is the promised
explicit smooth counterexample. No assertion that this is an
$\ell_q$ ball is involved.

## Evidence and trust boundary

The proof uses ordinary finite-dimensional convex geometry and exact
rational arithmetic. The small JSON witness and standard-library
Python verifier certify the polytopal images by supporting edges and
independent vertical integration, the parameter endpoints, the
orthogonal projection matrix, and the smooth comparison margin.
Six deliberately corrupted inputs are rejected, and deleting the
added rectangle restores equality as a positive control.
The analytic positive-part, product, known positive-case and smoothing
arguments above are not formalized in a proof assistant. The verifier
is an author check, not an independent peer review. No external
certificate, numerical tolerance, random outcome, or omitted search
dump is needed to reproduce the counterexample.
