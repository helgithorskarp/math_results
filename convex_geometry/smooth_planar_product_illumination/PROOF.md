# Illumination of a smooth convex body times a smooth planar body

This is an author proof, not an independently reviewed or formalized theorem.
The finite checker is corroboration of the construction, not a proof for all
dimensions. Historical priority of the higher-dimensional formula is unresolved;
see [SOURCES.md](SOURCES.md). The cases of an interval and of two smooth planar
bodies are classical.

## Statement

A convex body is a compact convex set with nonempty interior in its ambient
space. Call it **smooth** if each boundary point has a unique supporting
hyperplane. A nonzero vector $w$ illuminates a boundary point $z$ of a convex
body $M$ if $z+tw\in\operatorname{int}M$ for all sufficiently small $t>0$.
Write $I(M)$ for the minimum number of directions illuminating its boundary.

**Theorem.** Let $d\geq1$, let $K\subset\mathbb R^d$ be a smooth convex body,
and let $L\subset\mathbb R^2$ be a smooth convex body. Then

$$
 I(K\times L)=
 \begin{cases}
  2d+3,&d\text{ even},\\
  2d+4,&d\text{ odd}.
 \end{cases}                                                     \tag{1}
$$

In fact there is one integer list of optimal directions, depending only on $d$
and the chosen factor coordinates, which works for every such $K,L$.
No central symmetry, strict convexity, or positive curvature is assumed.
The result is invariant under independent invertible affine changes of the two
factors: translate the bodies and apply the linear parts to the directions.
It consequently also applies to direct vector sums in complementary subspaces.

## 1. Normal vectors and positive spanning

If $z\in\partial K$ has unique outer unit normal $u$, a vector $a$
illuminates $z$ exactly when $u\cdot a<0$. Necessity follows from the
supporting hyperplane. Here is a proof of sufficiency that includes flat boundary
pieces. On the unit sphere, the continuous nonnegative function

$$
 g(n)=h_K(n)-n\cdot z
$$

vanishes only at $u$. Choose a neighborhood $U$ of $u$ and $c>0$ such
that $n\cdot a<-c$ throughout $U$. On the compact complement of $U$,
$g\geq\delta>0$. For sufficiently small $t>0$, all supporting inequalities
for $z+ta$ are strict, with slack at least $tc$ on $U$ and
$\delta-t|a|>0$ off $U$. Their minimum slack is positive, so $z+ta$ is
interior. In dimension one the same argument uses the two-point unit sphere.

Every unit vector is the outer normal at some boundary point of a smooth body:
take a maximizer of its scalar product with the body. Therefore a finite list

$$
 (a_i,b_i)\in\mathbb R^d\times\mathbb R^2,\qquad 0\leq i<N,
$$

illuminates $K\times L$ exactly when

$$
 \forall u\in S^{d-1}\ \forall v\in S^1\quad
 \exists i:\quad a_i\cdot u<0\quad\hbox{and}\quad b_i\cdot v<0.    \tag{2}
$$

Necessity follows by considering products of boundary points with these normals.
For sufficiency, (2) covers points with both coordinates on their respective
boundaries. If only one coordinate is on the boundary, choose any auxiliary
normal for the interior factor and use (2); sufficiently small displacement
keeps that factor interior. This covers the entire product boundary.

A pair with either component zero contributes nothing to (2) and can be
discarded. For a fixed nonzero $v\in\mathbb R^2$, put

$$
 A(v)=\{a_i:b_i\cdot v<0\}.
$$

By elementary separation, (2) is equivalent to

$$
 0\in\operatorname{int}\operatorname{conv} A(v)
 \quad\text{for every nonzero }v.                              \tag{3}
$$

Indeed, failure of interior containment supplies a nonzero $u$ with
$u\cdot a\geq0$ for every member of $A(v)$, and conversely. We call (3)
positive spanning. A positively spanning set in $\mathbb R^d$ has at least
$d+1$ members, since its convex hull has affine dimension $d$.

If exactly $d+1$ vectors $a_0,\ldots,a_d$ positively span, their matrix has
rank $d$, and its one-dimensional kernel has a vector with all entries
strictly positive. Equivalently, there are unique barycentric coefficients
$\lambda_i>0$, with sum one, such that

$$
 \sum_{i=0}^d\lambda_i a_i=0.                                  \tag{4}
$$

Every $d$ of these vectors are linearly independent. Otherwise the matrix
would have a kernel vector with one coefficient zero, independent of (4),
contradicting its rank. These observations require no general-position
assumption on the original illuminating list.

## 2. The lower bound and the parity obstruction

Discard pairs with a zero component. Choose a line through the origin and one
remaining $b_i$, and choose a nonzero normal $v$ to that line. Each of the
disjoint lists selected by $b_j\cdot v<0$ and $b_j\cdot v>0$ has at least
$d+1$ members by (3). At least one other member lies on the line. Hence

$$
 N\geq 2d+3.                                                   \tag{5}
$$

Suppose equality holds. Applying the same count to every line through a $b_i$
shows that exactly one member lies on each such line and that each of its open
halfplanes contains exactly $d+1$ members. In particular there are no equal or
antipodal planar rays. List $b_0,\ldots,b_{N-1}$ in cyclic order, and use
indices periodically modulo $N$. The open semicircle beginning immediately
after $b_j$ contains exactly the next $d+1$ rays. By (3), every cyclic block

$$
  a_j,a_{j+1},\ldots,a_{j+d}                                   \tag{6}
$$

positively spans $\mathbb R^d$.

Define the nonzero ordered determinants

$$
 D_j=\det(a_j,a_{j+1},\ldots,a_{j+d-1}).
$$

Apply (4) to (6). Expressing the last vector as a negative positive combination
of the first $d$ vectors and expanding the determinant gives

$$
 D_{j+1}=(-1)^d\frac{\lambda_j}{\lambda_{j+d}}D_j,
 \qquad
 \operatorname{sgn}D_{j+1}=(-1)^d\operatorname{sgn}D_j.           \tag{7}
$$

The sign is important: moving $a_j$ from the last column to the first
contributes $(-1)^{d-1}$, and its coefficient contributes one further minus.
If $d$ is odd, (7) changes the determinant sign at every step. But
$N=2d+3$ is odd, and the periodically ordered tuple defining $D_N$ is exactly
the tuple defining $D_0$. This is impossible. Thus

$$
 N\geq2d+4\quad\text{when }d\text{ is odd}.                    \tag{8}
$$

This argument includes all degeneracies: if some line contains more than one
planar component, equality in (5) is already impossible. Linear independence
in (7) is forced by positive spanning, not assumed.

## 3. Positive circuits on a signed moment curve

For integers $N>d\geq1$, define

$$
 a_i=(-1)^i(1,i,i^2,\ldots,i^{d-1}),\qquad 0\leq i<N.          \tag{9}
$$

**Lemma.** If $N-d$ is odd, every cyclic block of $d+1$ vectors in (9)
positively spans $\mathbb R^d$.

**Proof.** Sort the indices of such a block as $j_0<\cdots<j_d$. The successive
gaps are all one, except possibly one gap of size $N-d$, arising from a block
that crosses the end of the list. All these gaps are odd, so

$$
 j_r-r\equiv j_0\pmod2.                                      \tag{10}
$$

Let $P(t)=\prod_{r=0}^d(t-j_r)$. Comparing leading coefficients in Lagrange
interpolation for $1,t,\ldots,t^{d-1}$ gives

$$
 \sum_{r=0}^d\frac{j_r^k}{P'(j_r)}=0,
 \qquad 0\leq k<d.                                           \tag{11}
$$

Thus the coefficients

$$
 \mu_r=\frac{(-1)^{j_r}}{P'(j_r)}                              \tag{12}
$$

satisfy $\sum_r\mu_r a_{j_r}=0$. Since
$\operatorname{sgn}P'(j_r)=(-1)^{d-r}$, equations (10) and (12) show that all
$\mu_r$ have the same nonzero sign. Divide by their sum to obtain strictly
positive barycentric coefficients. Any $d$ vectors in (9) are independent
by the Vandermonde determinant. Hence these $d+1$ vectors have zero in the
interior of their convex hull. $\square$

## 4. An integer planar configuration

For $N\geq3$, let $h=\lceil N/2\rceil$, and define the following vectors
already in cyclic order:

$$
 b_i=
 \begin{cases}
  (1,2i),&0\leq i<h,\\
  (-1,-(2(i-h)+1)),&h\leq i<N.
 \end{cases}                                                  \tag{13}
$$

The first group has increasing arguments in $[0,\pi/2)$, and the second
has increasing arguments in $(\pi,3\pi/2)$. No two vectors lie on the same
line through the origin: the slopes in the two groups have opposite parity.
As an unordered set, (13) is just

$$
 \{(-1)^j(1,j):0\leq j<N\}.                                   \tag{14}
$$

**Lemma.** Every open halfplane through the origin contains at least
$\lfloor(N-1)/2\rfloor$ of these vectors.

**Proof.** For $v=(\alpha,\beta)\ne0$, the scalar products in the indexing
of (14) have signs of

$$
  (-1)^j(\alpha+\beta j),\qquad 0\leq j<N.                    \tag{15}
$$

If $\beta=0$, they alternate and the claim follows. Otherwise, multiplication
of all signs by minus one allows us to assume $\beta>0$. The affine function
$\alpha+\beta j$ changes sign at most once and is zero at at most one index.
Each strictly negative or strictly positive interval of this function gives an
alternating run in (15).

For completeness, when $N=2m+1$ and there is no zero, the two runs have
opposite length parity, so their sign imbalances add to $+1$ or $-1$.
There are at least $m$ signs of each kind. If the zero is at $j=r$, then:
when $r$ is even, the two remaining runs have even lengths; when $r$ is odd,
both runs have odd lengths but opposite imbalances. Thus the $2m$ nonzero
signs split equally. When $N=2m$ and there is no zero, the two alternating
runs have total imbalance of absolute value at most two. If there is a zero,
one run has even length and the other has odd length, so the imbalance has
absolute value one. In both cases at least $m-1$ signs have each kind.
This is the asserted bound for either open halfplane. $\square$

The selected vectors of (13) in any open halfplane form one contiguous cyclic
block, because that halfplane intersects the unit circle in a single open
semicircle. Strict halfplanes are essential here; the proof includes normals
perpendicular to one of the $b_i$.

## 5. Attaining the bound

Set

$$
 N=2d+3+(d\bmod2).                                            \tag{16}
$$

Use $a_i$ from (9) and $b_i$ from (13), paired according to their displayed
index $i$. This pairing matters: the unordered representation (14) is used
only to count signs, not to pair the factors.

For every nonzero planar normal $v$, the active indices with $b_i\cdot v<0$
form a cyclic block of length at least

$$
 \left\lfloor\frac{N-1}{2}\right\rfloor=d+1.
$$

Also $N-d$ is odd in both parity cases. Section 3 therefore supplies a
positively spanning $(d+1)$-subblock of its $a_i$. The entire active list
positively spans, and (3) proves that the $N$ directions illuminate
$K\times L$. The lower bounds (5) and (8) establish (1). $\square$

For example, the values for $d=1,2,3,4,5,6$ are $6,7,10,11,14,15$.
The odd-dimensional extra direction is forced for every possible illuminating
configuration, not just for the signed moment-curve construction.

## 6. Scope of the computation and of the result

The code uses integer directions and exact rational arithmetic. For $1\leq d\leq16$,
it checks each cyclic block by solving its affine barycentric system,
compares the solution with (12), and verifies full rank and positivity. It
partitions the planar normal circle by the exact rays perpendicular to every
$b_i$, checks a rational point on each boundary and in each open cell, and
finds a certified positive circuit in every active set. Scalar-product signs
are constant in each such open cell, so this is a complete check of all planar
normals in each tested dimension. It also constructs exact unilluminated normal
pairs for deliberately invalid configurations and for every single-direction
deletion in dimensions 1 through 6.

These finite checks do not establish the arbitrary-dimensional lower bound,
the smooth normal criterion, or the all-dimensional construction. Those are
the mathematical arguments above. No formal proof assistant, external solver,
floating-point calculation, or independent referee is part of the trust base.

The theorem determines the $(d,2)$ family in the prescribed-dimensions problem
formulated by Baladze–Boltyanski (2006), Problem 4. It does not determine products
of two arbitrary higher-dimensional factors, products of three or more general
smooth factors, or products with a nonsmooth planar factor. It is not a solution
of the general illumination conjecture. See SOURCES.md for the precise known
cases and the unresolved literature-access limitation.
