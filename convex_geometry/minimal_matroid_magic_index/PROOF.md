# The exact magic index of a minimal matroid

**Status:** a complete elementary proof, with finite exact checks supplied
separately. The proof does not rely on computation or numerical roots.

Let $T_{k,n}$ be the connected minimal matroid of rank $k$ on $n$
elements, where $n\ge2$ and $1\le k\le n-1$, and let $D_{k,n}(x)$
be the Ehrhart polynomial of its base polytope. A degree-$d$ polynomial
is *magic positive* when all coefficients in the basis

$$
 x^i(x+1)^{d-i},\qquad 0\le i\le d,
$$

are nonnegative. Here $d=n-1$.

**Theorem.** For every real $a>0$,

$$
 D_{k,n}(ax)\text{ is magic positive}
 \quad\Longleftrightarrow\quad
 a\ge\max\{k,n-k\}.
$$

Consequently

$$
 \mathrm{m\text{-}index}\bigl(B(T_{k,n})\bigr)=\max\{k,n-k\}.
$$

In the range $k\le n/2$, this answers Question 5.5 of
[Konoike, arXiv:2504.21395v1](https://arxiv.org/html/2504.21395v1#S5.SS2).
The positive real dilation parameter in the theorem refers to the
polynomial substitution, whether or not the dilated polytope is integral.

## 1. The known factorization and its counting interpretation

Write $r=n-k$. A realization of $T_{k,n}$ has bases

$$
 [k],\qquad ([k]\setminus\{i\})\cup\{j\}
 \quad(1\le i\le k<j\le n).
$$

These are the spanning trees of a cycle of length $k+1$ with one edge
replaced by $r$ parallel edges (including the usual parallel-edge
interpretation when $k=1$). This is Ferroni's realization of the
minimal matroid. Its base polytope is

$$
 P_{k,r}=\left\{z\in[0,1]^{k+r}:
 \sum_{i=1}^{k+r}z_i=k,\quad\sum_{i=k+1}^{k+r}z_i\le1\right\}.
$$

For completeness, put $y_i=1-z_i$ for $i\le k$, and retain the last
$r$ coordinates as $w_j$. This is an affine lattice isomorphism to

$$
 \left\{(y,w)\ge0:\sum_i y_i=\sum_j w_j\le1\right\}
 =\operatorname{conv}\bigl(0,\{(e_i,e_j):i\in[k],j\in[r]\}\bigr).
$$

Indeed, at a common sum $t>0$, coefficients $y_iw_j/t$ give a
convex combination of these nonzero vertices of total weight $t$;
the remaining weight $1-t$ goes to zero. The case $t=0$ is immediate.
This also exhibits the symmetry between $k$ and $r$. Thus we may
assume $1\le k\le r$.

For an integer $m\ge0$, stars and bars now gives

$$
 D_{k,k+r}(m)
 =\sum_{t=0}^{m}\binom{t+k-1}{k-1}\binom{t+r-1}{r-1}.
 \tag{1}
$$

Ferroni's factorization, recorded in Corollary 3.4, equation (3.11) of
[arXiv:2003.02679](https://arxiv.org/html/2003.02679#S3), is

$$
 D_{k,k+r}(x)
 =\frac{1}{\binom{k+r-1}{k-1}}\binom{x+r}{r}\,Q_{k,r}(x),
 \qquad
 Q_{k,r}(x)=\sum_{j=0}^{k-1}\binom{r-1+j}{j}\binom{x+j}{j}.
 \tag{2}
$$

All binomial expressions in $x$ denote polynomials over $\mathbb Q$.
One can derive (2) directly from (1): Vandermonde's identity followed
by the hockey-stick identity gives

$$
 \frac{D_{k,k+r}(x)}{\binom{x+r}{r}}
 =\sum_{j=0}^{k-1}\binom{k-1}{j}\frac{r}{r+j}\binom{x}{j}.
 \tag{3}
$$

On the other hand, expanding $\binom{x+j}{j}$ in the basis
$\binom{x}{\ell}$ in (2) gives the coefficient

$$
 \sum_{j=\ell}^{k-1}\binom{r-1+j}{j}\binom{j}{\ell}
 =\binom{r-1+\ell}{\ell}\binom{r+k-1}{k-1-\ell}.
$$

Dividing this by $\binom{k+r-1}{k-1}$ gives exactly
$\binom{k-1}{\ell}r/(r+\ell)$, proving (2).
Equality first holds at every nonnegative integer $x$, hence as a
polynomial identity. These factorizations and the counting interpretation
are prior work; they are not novelty claims here.

## 2. A sign certificate for every residual root

**Lemma.** Suppose $r\ge k\ge1$. For $1\le h\le k$,

$$
 Q_{k,r}(-h)=(-1)^{h-1}\binom{r-1}{h-1}.
 \tag{4}
$$

Moreover, $Q_{k,r}$ has exactly one simple root in each interval
$(-h-1,-h)$, $1\le h\le k-1$, and no other roots.

*Proof.* At $x=-h$, the summands in (2) with $j\ge h$ vanish,
while for $0\le j<h$,

$$
 \binom{-h+j}{j}=(-1)^j\binom{h-1}{j}.
$$

Using the generalized binomial identity
$(-1)^j\binom{r-1+j}{j}=\binom{-r}{j}$, followed by Vandermonde,
we obtain

$$
 Q_{k,r}(-h)
 =\sum_{j=0}^{h-1}\binom{-r}{j}\binom{h-1}{h-1-j}
 =\binom{h-1-r}{h-1}
 =(-1)^{h-1}\binom{r-1}{h-1}.
$$

Vandermonde here follows by taking the coefficient of $z^{h-1}$
in $(1+z)^{-r}(1+z)^{h-1}$; only finitely many terms contribute.
Since $r\ge k$, all binomial coefficients on the right of (4) are
strictly positive. The signs therefore alternate at $-1,-2,\ldots,-k$.
The intermediate value theorem gives one distinct root in every open
interval between these points. The degree of $Q_{k,r}$ is $k-1$,
with positive leading coefficient, so these are all its roots and they
are simple. For $k=1$, $Q_{1,r}=1$, and the root assertion is empty. ∎

**Root-location consequence.** In addition to the roots $-1,\ldots,-r$
from the binomial factor, $D_{k,k+r}$ has one simple root in each of

$$
 (-2,-1),(-3,-2),\ldots,(-k,-k+1).
$$

All $k+r-1$ roots are simple and lie in $[-r,-1]$.
In particular, the leftmost root is exactly $-r$.
This concerns the Ehrhart polynomial itself. The real-rootedness of its
$h^*$-polynomial was already proved in the prior literature.

## 3. From negative real roots to the sharp threshold

**Lemma.** Let $f(x)=c\prod_{j=1}^d(x+\alpha_j)$, where $d\ge1$, $c>0$,
and every $\alpha_j>0$. For $a>0$, $f(ax)$ is magic positive
if and only if $a\ge\max_j\alpha_j$.

*Proof.* If $a\ge\alpha_j$, then

$$
 ax+\alpha_j=\alpha_j(x+1)+(a-\alpha_j)x
$$

is magic positive of degree one. Multiplying these identities gives
nonnegative coefficients in the degree-$d$ magic basis.

Conversely, a nonzero magic-positive polynomial of degree $d$ has no
root in $(-\infty,-1)$: at any such real $x$, all basis terms
$x^i(x+1)^{d-i}$ have the same sign $(-1)^d$, and at least one has
a positive coefficient. If $a<\max_j\alpha_j$, the polynomial
$f(ax)$ has a root at $-\max_j\alpha_j/a<-1$, a contradiction. ∎

Apply the lemma to the root-location consequence of (2)–(4). Its positive
leading coefficient and leftmost root $-r$ give the threshold $a=r$.
The symmetry $k\leftrightarrow r$ proves the theorem in all ranks. ∎

At $a=r$, the top magic coefficient is zero and every other magic
coefficient is strictly positive. At $a>r$, all magic coefficients
are strictly positive. These claims follow directly from the product
of the linear factors above; the root $-r$ is simple and every other
root has smaller absolute value.

## 4. A rational positive decomposition, without locating roots

There is also an exact coefficient certificate for the upper bound.
Lagrange interpolation at $-1,\ldots,-k$, using (4), gives

$$
 Q_{k,r}(x)=
 \sum_{h=1}^{k}
 \frac{\binom{r-1}{h-1}}{(h-1)!(k-h)!}
 \prod_{\substack{1\le j\le k\\j\ne h}}(x+j).
 \tag{5}
$$

Every coefficient multiplying a product is positive. When $a\ge r\ge k$,
every factor $ax+j=j(x+1)+(a-j)x$ is magic positive. All terms of
(5) have the same degree $k-1$, so their sum is magic positive in
that degree. Multiplying by $\binom{ax+r}{r}$ proves the upper bound
using rational coefficients alone. The root $-r$ still supplies the
lower bound.

This avoids a tempting invalid shortcut: positive sums of magic-positive
polynomials of different degrees need not be magic positive. For example,
$1$ and $x+1$ are individually magic positive, while
$x+2=2(x+1)-x$ is not. The original summands in (2) have different
degrees; the interpolation decomposition (5) fixes that issue.

## Scope and verification

The argument establishes a uniform theorem in every admissible $k,n$.
No finite verification range is used to infer that universal claim.
The accompanying standard-library checker compares two exact polynomial
formulas, the interpolation decomposition, the sign certificates, magic
coefficients at and around the threshold, and small direct lattice counts.
The optional SymPy checker verifies the residual interpolation identity
over $\mathbb Q[r,x]$ for a finite set of degrees.

The trust boundary is the written argument, elementary binomial
identities, and the identification of the displayed matroid as the
standard minimal matroid. The finite checks additionally trust Python
integer and rational arithmetic, or SymPy when that optional script is
used. There is no floating-point, external-dataset, solver, or formal
proof-assistant dependency. No independent peer review is claimed.
