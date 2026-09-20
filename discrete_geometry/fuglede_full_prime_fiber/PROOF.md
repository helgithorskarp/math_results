# A full prime fiber forces a binary tiling structure

Write $G=\mathbb Z_n\times\mathbb Z_p$, where $p$ is prime and
$\gcd(n,p)=1$, and use characters

$$
\chi_{b,u}(a,j)=\zeta_n^{ab}\zeta_p^{ju}.
$$

A pair $(A,\Lambda)$ is **spectral** if $|A|=|\Lambda|$ and the
character matrix has orthogonal columns. Its rows are then orthogonal
as well, since the matrix is square and is a scalar multiple of a
unitary matrix. A **full prime fiber** is a coset
$\{a_0\}\times\mathbb Z_p$. A **level** fixes the second coordinate;
fibers and levels therefore refer to different directions here.

The general theorem uses the following explicit local hypothesis:

> **Base hypothesis.** $\mathbb Z_n$ has no spectral subset of
> cardinality $p$.

We do not assert this hypothesis for every coprime pair $n,p$.

**Theorem.** Assume the base hypothesis. Let $|A|=2p$ and suppose
$\{0\}\times\mathbb Z_p\subset A$. Then $A$ is spectral if and only if
$n$ is even and, for some $0\le t<v_2(n)$,

$$
A=(\{0\}\times\mathbb Z_p)\ \sqcup\
  \{(a_j,j):j\in\mathbb Z_p\},
\qquad v_2(a_j)=t\quad\text{for every }j.
$$

Here each $a_j$ is represented in $\{1,\ldots,n-1\}$. Since
$t<v_2(n)$, the condition is well-defined modulo $n$.
Every such set has the explicit spectrum

$$
\Lambda_t=\{0,n/2^{t+1}\}\times\mathbb Z_p
$$

and tiles with the explicit complement

$$
T_t=
\{(x,0):0\le x<n,\quad x\bmod 2^{t+1}<2^t\}.
$$

For a fiber based at $a_0$, translate the first coordinate by $-a_0$
before applying the criterion. The same spectrum and complement still
work after translating back. The sufficiency and the displayed tiling
construction do not require the base hypothesis.

## A graph-spectrum dichotomy

**Lemma.** Suppose $(C,\Gamma)$ is a spectral pair of cardinality $p$ in
$\mathbb Z_n\times\mathbb Z_p$, and

$$
\Gamma=\{(b_j,j):j\in\mathbb Z_p\}.
$$

Then either $C$ has exactly one point on every level, or $C$ lies on a
single level and its first-coordinate projection is a $p$-point spectral
subset of $\mathbb Z_n$.

**Proof.** For two points $(a,r),(a',s)\in C$ with $r\ne s$, row
orthogonality gives

$$
\sum_{j=0}^{p-1}\zeta_n^{(a-a')b_j}\zeta_p^{(r-s)j}=0.
$$

Over $\mathbb Q(\zeta_n)$ the minimal polynomial of $\zeta_p$ is
$1+X+\cdots+X^{p-1}$. Indeed, the cyclotomic degree ratio is
$\varphi(np)/\varphi(n)=p-1$. Multiplication of the indices by
$r-s$ permutes them, so all coefficients in this relation are equal.
Consequently

$$
\zeta_n^{(a-a')(b_j-b_0)}=1\quad\text{for every }j.
$$

Let $H\le\mathbb Z_n$ be the common kernel of the characters
$x\mapsto\zeta_n^{x(b_j-b_0)}$. Thus first-coordinate differences
between points on different levels lie in $H$.

If $C$ occupies at least two levels, this holds for *all* its
first-coordinate differences: connect any same-level pair through a
point on another level and subtract the two differences. Two points
on the same level would then have row inner product
$p\zeta_n^{(a-a')b_0}\ne0$, a contradiction. There is at most one
point per level, and the cardinality makes it exactly one per level.

If $C$ occupies just one level, its first coordinates are distinct.
The column phases from that level can be removed without changing
orthogonality. The $b_j$ must also be distinct, since otherwise two
columns would be proportional. The remaining character matrix is a
spectral pair of cardinality $p$ in $\mathbb Z_n$. This proves the
second alternative. $\square$

Coprimality matters: in $\mathbb Z_3\times\mathbb Z_3$, the points
$(0,0),(1,0),(1,1)$ are spectral with spectrum
$\{(j,j):j\in\mathbb Z_3\}$, but their level sizes are $(2,1,0)$.

## Delete the full fiber and halve each spectral level

Assume $A$ is spectral, with spectrum $\Lambda$, and put
$F=\{0\}\times\mathbb Z_p$ and $C=A\setminus F$.
Orthogonality between the $p$ rows indexed by $F$ implies that the
level counts of $\Lambda$ have vanishing nonconstant Fourier
coefficients. Their total is $2p$, so every level has two elements:

$$
\Lambda_j=\{b_j,c_j\}.
$$

Fix $(a,r)\in C$. Orthogonality with *each* row $(0,s)\in F$ says

$$
\sum_{j=0}^{p-1}\zeta_p^{(r-s)j}
       \bigl(\zeta_n^{ab_j}+\zeta_n^{ac_j}\bigr)=0
\quad\text{for every }s\in\mathbb Z_p.
$$

Fourier inversion on $\mathbb Z_p$ gives

$$
\zeta_n^{a(c_j-b_j)}=-1
\quad\text{for every }j\text{ and every }(a,r)\in C. \tag{1}
$$

For any two residual points $(a,r),(a',s)\in C$, division of their
instances of (1) gives
$\zeta_n^{(a-a')(c_j-b_j)}=1$. Their original row inner product is
therefore

$$
2\sum_{j=0}^{p-1}\zeta_n^{(a-a')b_j}\zeta_p^{(r-s)j}.
$$

For distinct points it vanishes. Thus

$$
\left(C,\{(b_j,j):j\in\mathbb Z_p\}\right)
$$

is itself a spectral pair of cardinality $p$. Either choice of the
two frequencies on each level works. This deletion identity is valid
before imposing the base hypothesis.

Apply the graph-spectrum dichotomy. Its one-level alternative would
give a $p$-point spectral set in $\mathbb Z_n$, contrary to the base
hypothesis. Hence
$C=\{(a_j,j):j\in\mathbb Z_p\}$.

## The common binary valuation

Choose any frequency level and let
$\delta=c_j-b_j\in\mathbb Z_n$. Equation (1) says
$\zeta_n^{a_r\delta}=-1$ for every residual point. In particular,
$n$ is even and

$$
\delta a_r\equiv n/2\pmod n.
$$

Write $n=2^s m$ with $m$ odd. Reducing the congruence modulo $2^s$
shows that $v_2(\delta)<s$ and

$$
v_2(a_r)=s-1-v_2(\delta)
$$

for all $r$. This is one common value $t<s$, proving necessity.
It also shows directly that odd $n$ cannot support such a spectral
set with a full fiber, even without the base hypothesis.

## Explicit spectrum and tiling complement

Conversely suppose the displayed normal form holds, and set
$\delta_t=n/2^{t+1}$. Each $a_j/2^t$ is odd, so
$\zeta_n^{\delta_t a_j}=-1$.

For two frequencies in $\Lambda_t$ with different first coordinates,
the two contributions on every level of $A$ cancel. For equal first
coordinates and distinct second coordinates, the inner product is
$2\sum_j\zeta_p^{uj}=0$ for some nonzero $u$. Thus $\Lambda_t$
is a spectrum of $A$.

The first-coordinate part of $T_t$ is the inverse image of the first
half of $\mathbb Z_{2^{t+1}}$. Each $a_j$ is congruent to $2^t$
modulo $2^{t+1}$, so its translate is exactly the inverse image of
the other half. Consequently

$$
\{0,a_j\}\oplus\{x:(x,0)\in T_t\}=\mathbb Z_n
$$

on every level, with unique representations. This proves
$A\oplus T_t=G$. $\square$

## The size-22 family in $\mathbb Z/2310\mathbb Z$

Take $n=210$ and $p=11$. The
[Kiss–Malikiosis–Somlai–Vizer four-prime theorem](https://link.springer.com/article/10.1007/s00041-022-09972-0)
implies that a spectral set in $\mathbb Z_{210}$ tiles. An
11-point set cannot tile a group of order 210, so the base hypothesis
holds.

Since $v_2(210)=1$, the theorem has only $t=0$. After translating
a contained full 11-fiber to $\{0\}\times\mathbb Z_{11}$, a
22-point set is spectral exactly when its other points are
$(a_j,j)$ with **every $a_j$ odd**. All these sets share spectrum
$\{0,105\}\times\mathbb Z_{11}$ and complement
$2\mathbb Z_{210}\times\{0\}$.

Under the usual point CRT map
$\mathbb Z_{2310}\to\mathbb Z_{210}\times\mathbb Z_{11}$,
the complement is $22\mathbb Z_{2310}$, of size 105. Its
annihilator, $105\mathbb Z_{2310}$, is a common cyclic spectrum.
Thus every size-22 spectral non-tile, if one exists, must avoid every
coset of the order-11 subgroup. This is a restriction on a named
family, not a classification of all size-22 spectral sets.

## Evidence and trust boundary

The argument is a written universal proof. The checker uses integer
cyclotomic remainders for exact character sums and a Fourier-zero
clique search independent of the proposed normal form. It exhausts
4,890 small sets containing a specified full fiber, finding 116
spectral sets and exact agreement with the criterion. For one found
spectrum of every positive case, all 1,720 total choices in the
deletion step are verified. It separately checks 14,375
graph-spectrum candidate pairs, including 713 spectral pairs.

Explicit fixtures include prime powers in $n$, several allowed binary
valuations, and $(n,p)=(210,11)$. Every asserted tiling is checked by
counting all translations. A noncoprime example and malformed spectra
and complements test the boundaries. These finite checks corroborate
the proof; they do not establish the all-size theorem by enumeration.

Only the size-22 specialization imports the four-prime theorem.
The general result assumes its local base hypothesis, and uses
elementary Fourier inversion, cyclotomic degrees, and exact
orthogonality. No cuboid theorem, numerical tolerance, solver,
external dataset, or proof-assistant formalization is involved.
