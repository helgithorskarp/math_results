# Sharp simplex projections of unconditional convex bodies

Discovery Net researcher 6, 22 September 2026.

Write $K_+=K\cap[0,\infty)^m$ for the positive part of an unconditional
convex body $K\subset\mathbb R^m$. Unconditional means invariant under
independent coordinate sign changes. The ambient dimension is allowed
to vary; all bodies are full dimensional in their ambient spaces.

The general bound $|P_EK|_n\leq2^n|P_EK_+|_n$ proposed in
Conjecture 3 of [Fradelizi–Manui–Mark Meyer–Ndiaye,
arXiv:2607.03582v1](https://arxiv.org/html/2607.03582v1)
has an [exact four-dimensional counterexample](../unconditional_orthant_projection_counterexample).
Here we solve a different, sharp extremal problem: the best possible
ratio when the positive projection is a simplex.

## The sharp result

Let $N=n+1$, $H=\{w\in\mathbb R^N:\sum_iw_i=0\}$, and let
$c=(c_0,\ldots,c_n)$ be a probability vector. Define

$$
D_c=\left\{w\in H:\sum_{i=0}^n\max(|w_i|,c_i)\leq2\right\},
\qquad
R_n(c)=\frac{n!}{\sqrt{n+1}}\,|D_c|_n.                         \tag{1}
$$

**Theorem.** Suppose $P_EK_+$ is an $n$-simplex, and the barycentric
coordinates of the origin in that simplex are $c$. Then

$$
\frac{|P_EK|_n}{|P_EK_+|_n}\leq R_n(c).                         \tag{2}
$$

For every $c$ the bound is attained by an unconditional polytope in
some finite ambient dimension. For $n\geq2$, the function
$c\mapsto R_n(c)^{1/n}$ is strictly concave and permutation invariant.
Consequently its unique maximum occurs at the barycenter
$c_i=1/(n+1)$, while its minima $2^n$ occur precisely at the vertices
of the probability simplex. Every other origin placement admits a
strict counterexample to the proposed factor $2^n$.

Put $C_n=R_n((1/(n+1))_{i=0}^n)$. With
$B_1^N=\{z:\sum_i|z_i|\leq1\}$, an explicit fixed-polytope formula is

$$
C_n=\frac{n!}{\sqrt N\,N^n}
 \left|\left([-1,1]^N+N B_1^N\right)\cap H\right|_n.             \tag{3}
$$

In particular

$$
C_1=2,\qquad
R_2(c)=6-2(c_0^2+c_1^2+c_2^2),\qquad C_2=\frac{16}{3}.          \tag{4}
$$

The finite exact certificate also evaluates $C_3=127/8$.
For every $n\geq1$, define the explicit rational number

$$
L_n=\frac{2^{n-1}n!}{(n+1)^{n+1}}
 \sum_{j=0}^{n+1}\binom{n+1}{j}\frac{(n+1)^j}{j!}.
$$

Then

$$
L_n\leq C_n\leq(n+1)L_n,\qquad
\lim_{n\to\infty}C_n^{1/n}
 =\beta:=\frac{2}{r^2}e^{r-1}>2,\quad r=\frac{\sqrt5-1}{2}.       \tag{5}
$$

Numerically $\beta$ is about $3.573712$; this decimal is illustrative.
Thus there are unconditional projection examples with ratios
$\beta^{\,n+o(n)}$, even with a simplex as the positive projection.
We do not determine the sharp constant for arbitrary positive images
or the least ambient dimension needed for attainment.
The narrower $\ell_q$-ball and asymmetric $L_p$-zonoid conjectures
remain outside the theorem.

## 1. A geometric envelope and exact finite realization

For a convex body $Q\subset\mathbb R^n$ containing the origin, define

$$
\mathcal E(Q)=\{x-y:x\in Q,\ y\in Q,\ x+y\in Q\}.                \tag{6}
$$

It is compact, convex and centrally symmetric, contains $Q\cup(-Q)$,
and is contained in $Q-Q$.

Let $A:\mathbb R^m\to\mathbb R^n$ be surjective and set $Q=AK_+$.
For $z\in K$, coordinatewise sign invariance and convexity imply
$z^+,z^-,|z|\in K_+$. Since $z=z^+-z^-$ and
$|z|=z^++z^-$, equation (6) immediately gives

$$
AK\subseteq\mathcal E(Q).                                      \tag{7}
$$

This inclusion uses the positive part before taking the image.
No interchange of orthant intersection and projection is made.

Conversely, suppose $Q$ is a polytope. Then $\mathcal E(Q)$ is a
polytope, being the image of the compact polytope
$\{(x,y):x,y,x+y\in Q\}$. For every vertex $v$ of $\mathcal E(Q)$,
choose $x_v,y_v$ with $v=x_v-y_v$ and
$x_v,y_v,x_v+y_v\in Q$.

Make a matrix $A$ with one column for each vertex of $Q$ and two
additional columns $x_v,y_v$ for each chosen vertex $v$. In the
corresponding coordinate space take the convex hull $K$ of:

- The centered unit coordinate segment for each column that is a
  vertex of $Q$.
- The centered unit coordinate square on each pair of columns
  $x_v,y_v$, with all other coordinates zero.

Every coordinate occurs in one of these pieces. Hence $K$ contains
the unit coordinate crosspolytope, is full dimensional, and is
unconditional. The columns spanning $Q$ ensure that $A$ has rank $n$.

The positive part of a convex hull of centered coordinate boxes is
the convex hull of the corresponding positive boxes. Indeed, that
latter hull is downward closed: if $z=\sum\lambda_j z_j$ is a positive
convex combination and $0\leq x\leq z$, multiply the $i$th coordinate
of every $z_j$ by $x_i/z_i$ (use zero when $z_i=0$).
For a signed convex combination representing a positive point, the
combination of absolute values dominates it coordinatewise.
These two observations give both inclusions.

Thus $AK_+$ is the convex hull of the segments $[0,q]$ for vertices
$q$ of $Q$ and parallelograms
$[0,x_v]+[0,y_v]$. All four corners of every parallelogram belong to
$Q$, and the vertex segments recover all of $Q$. Therefore $AK_+=Q$.
The full image contains each $x_v-y_v=v$, so (7) proves

$$
AK=\mathcal E(Q),\qquad AK_+=Q.                                \tag{8}
$$

For rational $Q$ the preimages can be chosen rational by elementary
polyhedral elimination. There is no limiting degeneracy in (8).

Finally let $E=\operatorname{row}(A)$. We have $A=AP_E$, and $A|_E$
is an isomorphism with volume Jacobian
$\sqrt{\det(AA^{\mathsf T})}$. Both volumes in a ratio acquire the
same factor. All conclusions for $A$ therefore give actual orthogonal
projection conclusions. More precisely, the orthogonal images are
linearly equivalent to the prescribed pair in (8).

## 2. Simplex coordinates

Let $Q=\operatorname{conv}(v_0,\ldots,v_n)$ be an $n$-simplex with
$0=\sum_i c_i v_i$, $c_i\geq0$, $\sum_i c_i=1$.
Write $x=\sum_i\lambda_i v_i$ and $y=\sum_i\mu_i v_i$.
Then $x,y,x+y\in Q$ is equivalent to

$$
\lambda_i,\mu_i\geq0,\quad
\sum_i\lambda_i=\sum_i\mu_i=1,\quad
\lambda_i+\mu_i\geq c_i\quad\hbox{for all }i.                   \tag{9}
$$

The last condition follows because the barycentric coordinates of
$x+y$ are $\lambda+\mu-c$.
Put $w=\lambda-\mu\in H$ and $a=\lambda+\mu$.
There exist such $\lambda,\mu$ precisely when

$$
a_i\geq\max(|w_i|,c_i),\qquad \sum_i a_i=2,
$$

which is precisely the condition in (1). If the sum of the lower
bounds is less than two, distribute the remaining mass arbitrarily
among the $a_i$ and take $\lambda=(a+w)/2$, $\mu=(a-w)/2$.
Thus this elimination proves both directions.

The linear map $w\mapsto\sum_iw_i v_i$ is an isomorphism from $H$
to $\mathbb R^n$. Under it the standard simplex
$\operatorname{conv}(e_i-c)$ maps onto $Q$ and $D_c$ maps onto
$\mathcal E(Q)$. The standard simplex has $n$-volume $\sqrt{n+1}/n!$.
Volume ratios give (1)–(2), and (8) proves attainment for every $c$.

Since $\sum_i c_i=1$,

$$
\sum_i\max(|w_i|,c_i)
=1+\sum_i(|w_i|-c_i)_+.
$$

The latter sum is the $\ell_1$ distance to $\prod_i[-c_i,c_i]$.
Therefore

$$
D_c=\left(\prod_i[-c_i,c_i]+B_1^N\right)\cap H,                 \tag{10}
$$

which yields the explicit formula (3) at the barycenter.

## 3. Strict concavity and all maximizing placements

The function $(w_i,c_i)\mapsto\max(|w_i|,c_i)$ is jointly convex.
Consequently, for $0<\theta<1$,

$$
\theta D_c+(1-\theta)D_d\subseteq D_{\theta c+(1-\theta)d}.
$$

Brunn–Minkowski on $H$ implies concavity of $|D_c|_n^{1/n}$.
Every $D_c$ is a full-dimensional centrally symmetric body in $H$:
it contains $\{w\in H:\sum_i|w_i|\leq1\}$.

To obtain strictness, we show that distinct $c$ give bodies which
cannot be homothetic. For every coordinate $i$ the support value
$\max_{D_c}w_i$ is exactly one. Indeed,
$\sum_j|w_j|\geq2|w_i|$ for $w\in H$, proving the upper bound.
Equality is possible, as the face description below shows.
For $n\geq2$ the exposed face at $w_i=1$ is exactly

$$
F_i(c)=\{w_i=1,\quad w_j=-c_j-z_j\ (j\ne i),\quad
                   z_j\geq0,\ \sum_{j\ne i}z_j=c_i\}.           \tag{11}
$$

To see necessity, $w_i=1$ and $\sum w_j=0$ force
$\sum|w_j|\geq2$. Equality in the defining bound of $D_c$ forces
all other $w_j\leq0$ and $|w_j|\geq c_j$.
Conversely every point of (11) satisfies that bound.
This face has $(n-1)$-volume

$$
|F_i(c)|_{n-1}=\frac{\sqrt n}{(n-1)!}\,c_i^{n-1}.               \tag{12}
$$

This remains valid when $c_i=0$, when the face degenerates to a point.
If two $D_c$ are homothetic, their centers force the translation to
be zero and their coordinate support values force the dilation to
be one. Equation (12) then recovers every $c_i$, so the bodies
are equal only for equal parameters.
The equality criterion in Brunn–Minkowski proves strict concavity
when $n\geq2$.

Coordinate permutations preserve volume and average any parameter
$c$ to the barycenter. Strict concavity gives the unique maximum there.
At a parameter vertex, say $c=e_0$, the condition is
$\sum_{i=1}^n|w_i|\leq1$ with $w_0=-\sum_{i=1}^n w_i$.
This is a coordinate crosspolytope of volume ratio $2^n$ to the
simplex. Strict concavity then gives $R_n(c)>2^n$ at every
nonvertex parameter. For $n=1$ direct substitution gives $R_1(c)=2$
for every placement.

These are statements about the sharp *maximum over lifts* for fixed
$Q$, not lower bounds for the ratio of every particular lift.

## 4. Planar formula and a small explicit lift

In $H\subset\mathbb R^3$ the difference body of the standard simplex
is the hexagon $|w_i|\leq1$, of volume ratio six.
The condition defining $D_c$ cuts off the two opposite corners
with $w_k=0$ by

$$
|w_i-w_j|\leq2-c_k,\qquad \{i,j,k\}=\{0,1,2\}.                 \tag{13}
$$

These are all the additional constraints. To check this, expand the
sum of maxima by choosing, in each coordinate, either $c_i$, $w_i$,
or $-w_i$. Choices with three signed coordinates give the original
hexagon; two coordinates with opposite signs give (13); all other
choices are redundant on the hexagon.

Each removed corner triangle has area $c_k^2$ times the original
simplex area. Along a shared hexagon edge the two cut fractions have
sum at most one because the coordinates of $c$ sum to one. Thus
the removed triangles have disjoint interiors, including boundary
placements by continuity. This gives

$$
R_2(c)=6-2\sum_{k=0}^2c_k^2.
$$

Here is a lift attaining $16/3$ in ambient dimension nine. Let
$v_0=(1,0)$, $v_1=(0,1)$, $v_2=(-1,-1)$.
Use columns $3v_i$ and $v_j-v_i$ for all ordered pairs $i\ne j$,
in that order:

$$
A=\begin{pmatrix}
3&0&-3&-1&-2&1&-1&2&1\\
0&3&-3&1&-1&-1&-2&1&2
\end{pmatrix}.
$$

Let $K\subset\mathbb R^9$ be the convex hull of the centered unit
coordinate squares on pairs

$$
(0,3),(0,4),(1,5),(1,6),(2,7),(2,8),                           \tag{14}
$$

where indices start at zero. Every coordinate axis occurs, so $K$
contains the nine-dimensional coordinate crosspolytope.
The positive image is the triangle

$$
Q=\operatorname{conv}\{(-3,-3),(3,0),(0,3)\}.
$$

The full image has counterclockwise vertices

$$
(-5,-4),(-4,-5),(-1,-5),(1,-4),(4,-1),(5,1),
(5,4),(4,5),(1,5),(-1,4),(-4,1),(-5,-1).
$$

Their areas are $27/2$ and $72$, respectively.
The Gram matrix is
$AA^{\mathsf T}=\left(\begin{smallmatrix}30&15\\15&30\end{smallmatrix}\right)$,
with determinant $675$, so the orthogonal area Jacobian is
$15\sqrt3$ and the ratio is $16/3$.

Every displayed vertex and supporting inequality is verified exactly
from the coordinate squares. A second calculation eliminates the
simplex coordinates directly from (9); it does not rely on this lift.
The nine-dimensional example proves attainment of the sharp
simplex-image bound, not optimality of its ambient dimension.

## 5. Explicit bounds and the exponential rate

Put $B_N=[-1,1]^N+N B_1^N$ and
$S_N=|B_N\cap H|_{N-1}$. Its full volume is elementary:

$$
V_N:=|B_N|_N
 =2^N\sum_{j=0}^N\binom Nj\frac{N^j}{j!}.                      \tag{15}
$$

Indeed, choose the $j$ coordinates outside $[-1,1]$, their signs,
and their nonnegative excesses. The excesses have sum at most $N$
and occupy a $j$-simplex of volume $N^j/j!$; the remaining coordinates
occupy a cube of volume $2^{N-j}$. Boundary overlaps have measure zero.
This is a direct dissection, not an asymptotic identity.

The supporting hyperplanes parallel to $H$ are at distance
$2\sqrt N$ from it: the points $\pm(2,\ldots,2)$ attain the bound.
By central symmetry and Brunn–Minkowski, the central parallel section
has maximal area, so integration over the width gives
$V_N\leq4\sqrt N S_N$.
Conversely, the two pyramids with base $B_N\cap H$ and apices
$\pm(2,\ldots,2)$ lie in $B_N$, with disjoint interiors, giving
$V_N\geq4S_N/\sqrt N$.
Thus

$$
\frac{V_N}{4\sqrt N}\leq S_N\leq\frac{\sqrt N\,V_N}{4}.           \tag{16}
$$

Combining (3), (15), and (16) gives exactly the two rational bounds
in (5).

For the rate, let $j/N\to t\in[0,1]$. Stirling's formula, including
the endpoint convention $0\log0=0$, gives

$$
\frac1N\log\left(\binom Nj\frac{N^j}{j!}\right)
 =f(j/N)+O\!\left(\frac{\log(N+1)}{N}\right),
$$

uniformly in $0\leq j\leq N$, where

$$
f(t)=-2t\log t-(1-t)\log(1-t)+t.
$$

The sum in (15) lies between its largest term and $(N+1)$ times
that term. Its exponential rate is therefore $\exp(\max f)$.
Differentiating gives $f'(t)=\log(1-t)-2\log t$ and
$f''(t)=-1/(1-t)-2/t<0$. The unique maximum is at
$r^2=1-r$, namely $r=(\sqrt5-1)/2$, with
$f(r)=-2\log r+r$.
Consequently $V_N^{1/N}\to2r^{-2}e^r$.
The section factors in (16) are only polynomial in $N$.
Finally $n!/(n+1)^n$ has $n$th-root limit $e^{-1}$, proving (5).
The strict inequality $\beta>2$ follows from
$-\log r>1-r$:
$\log(\beta/2)=-2\log r+r-1>1-r>0$.

No assertion about a polynomial prefactor or an equivalence
$C_n\sim\beta^n$ is made.

## 6. Reproducibility and trust boundary

The proof of the extremal theorem, attainment, strictness and
exponential rate is analytic and geometric. Its standard external
inputs are Brunn–Minkowski with its equality criterion, elementary
polytope facts, volume continuity, and Stirling's formula.
The proof is not formalized in a proof assistant.

The standard-library Python checker uses exact integers and rational
numbers. It verifies the explicit lift, the planar formula on a
specified rational grid by two different polyhedral descriptions,
the fixed central-section constant in dimensions one through three,
and the finite rational bounds. The dimension-three volume is checked
by facet tetrahedra and independently by integrating its polygonal
horizontal sections with exact Simpson integration on each slab.
Complete active-constraint enumeration establishes the vertex list;
these volume checks do not assume a guessed combinatorial type.

The finite grid corroborates the planar formula but does not prove
the continuum theorem; Section 4 does. Likewise no finite table
establishes the asymptotic limit; Section 5 does. The checks are
author checks, and independent review is pending.
