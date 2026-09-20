# A hereditary obstruction for uniform Erdős–Szekeres blow-ups

## Setting and prior construction

Let $S=\{p_1,\ldots,p_N\}$ be a planar point set in general position,
ordered by strictly increasing first coordinate. Assume $N\ge2$,
$1\le L<N$, $m\ge3$, and that $S$ has no $m$ points in convex
position. Singletons and pairs are counted as convex subsets.

For $i\le L$, let $s_i$ be the largest size of a convex subset of **all
of $S$** whose rightmost point is $p_i$. For $i>L$, use the largest
size with leftmost point $p_i$. Write

$$
v_j=\#\{i:s_i=j\},\qquad V_j=\sum_{h=1}^jv_h.
$$

Then $v_1=2$, $v_j=0$ for $j\ge m$, and $V_{m-1}=N$.
Only $p_1,p_N$ have rank one, since every other appropriate endpoint
can be joined to a point on its designated side.

Fix an integer $x\ge1$, and put $k=m+2x$. Baek–Balko's uniform
$x$-blow-up with threshold $L$ is their general cluster construction
with

$$
(x_i,y_i)=
\begin{cases}
(x,k-1-x-s_i),&i\le L,\\
(k-1-x-s_i,x),&i>L.
\end{cases}
$$

Their Corollary 15 guarantees a $k$-gon-free blow-up of cardinality

$$
B=2\sum_{\ell=0}^{x}\binom{k-2}{\ell}
  +\sum_{j=2}^{m-1}v_j\binom{k-j-1}{x}. \tag{1}
$$

The construction, its polygon avoidance, and formula (1) are **prior
work**. The claims below concern the information carried by (1).
No particular realization of the clusters is needed in our proof.

## Theorem: exact excess and extraction

In this setting,

$$
\boxed{
B-2^{k-2}
=\binom{2x}{x}\bigl(N-2^{m-2}\bigr)
 +\sum_{j=2}^{m-2}\binom{k-j-2}{x-1}\bigl(V_j-2^j\bigr).
} \tag{2}
$$

All displayed coefficients are strictly positive. The sum is empty when
$m=3$. Consequently, if $B>2^{k-2}$, one can extract from $S$ a set
$T$ and an integer $3\le q\le m<k$ such that

$$
|T|>2^{q-2},\qquad T\text{ contains no convex }q\text{-gon}. \tag{3}
$$

Thus the uniform $x$-blow-up cannot produce a counterexample at the
**smallest polygon size** where the Erdős–Szekeres conjecture fails.
The extraction statement is unconditional: it does not assume the
conjecture at any size.

### A binary-word identity

Define a reference profile by

$$
v_1^*=2,\qquad v_j^*=2^{j-1}\ (2\le j\le m-2),\qquad v_{m-1}^*=0.
$$

Its total is $2^{m-2}$, and $V_j^*=2^j$ for $1\le j\le m-2$.
We first prove directly that its value in (1) is $2^{k-2}$:

$$
2\sum_{\ell=0}^{x}\binom{k-2}{\ell}
 +\sum_{j=2}^{m-2}2^{j-1}\binom{k-j-1}{x}=2^{k-2}. \tag{4}
$$

Count binary words of length $n=k-2\ge2x+1$. The words with at most
$x$ zeros and the words with at most $x$ ones are disjoint and give
the first term. For every remaining word, take its shortest suffix
containing at least $x+1$ of each symbol. If the suffix length is $t$,
then $2x+2\le t\le n$. Its first symbol occurs exactly $x+1$ times
in that suffix: removing it destroys the required property. Choose that
symbol in two ways, choose the other $x$ occurrences among the last
$t-1$ positions, and choose the prefix arbitrarily. This gives
$2^{n-t+1}\binom{t-1}{x}$ words. Substitution $j=k-t$ gives the
second term of (4). This also handles $m=3$, when there are no remaining
words. Identity (4), and a geometric realization of the reference profile,
also appear in Baek–Balko's sharp construction (Lemma 18/Theorem 19).

### Summation by parts

Set $w_j=\binom{k-j-1}{x}$. Subtract (4) from (1), and use
$v_1-v_1^*=0$. Finite summation by parts gives

$$
\sum_{j=2}^{m-1}(v_j-v_j^*)w_j
=w_{m-1}(N-2^{m-2})
 +\sum_{j=2}^{m-2}(w_j-w_{j+1})(V_j-2^j).
$$

Here $w_{m-1}=\binom{2x}{x}$, and Pascal's identity gives
$w_j-w_{j+1}=\binom{k-j-2}{x-1}>0$. This proves (2).

### Why a positive endpoint excess is a smaller counterexample

Define

$$
A_j=\{p_i:i\le L,\ s_i\le j\},\qquad
C_j=\{p_i:i>L,\ s_i\le j\}.
$$

Each of $A_j,C_j$ has no convex $(j+1)$-gon. Indeed, a convex subset
of $A_j$ with $j+1$ vertices would have a rightmost point $p_i\in A_j$,
forcing $s_i\ge j+1$. The argument for $C_j$ uses its leftmost point.
The ranks here are those computed in the original $S$, so deleting
other points creates no logical difficulty.

If $N>2^{m-2}$, take $T=S,q=m$. Otherwise, positivity in (2) forces
$V_j>2^j$ for some $2\le j\le m-2$. Since
$|A_j|+|C_j|=V_j$, one of these sets has more than $2^{j-1}$ points.
Take that set as $T$ and $q=j+1$. This proves (3).

## Conditional sharp bound and equality

Assume the Erdős–Szekeres upper bound holds for every polygon size
$3\le q\le m$: every general-position set with more than $2^{q-2}$
points has a convex $q$-gon. Then

$$
N\le2^{m-2},\qquad |A_j|,|C_j|\le2^{j-1},\qquad V_j\le2^j.
$$

Every summand of (2) is nonpositive, so $B\le2^{k-2}$. Equality holds
if and only if

$$
N=2^{m-2},\qquad V_j=2^j\quad(2\le j\le m-2), \tag{5}
$$

equivalently, $v_j=v_j^*$ for every $j$. For each $j$ in (5),
both $A_j$ and $C_j$ must individually attain $2^{j-1}$ points.
This classifies the **endpoint-count profile**, not the order types of
all equality configurations. The positivity of every coefficient is
essential for this equality conclusion.

More locally, the same conclusion holds whenever these cardinality
bounds are verified just for $S,A_j,C_j$, without any global conjecture.
As a known-case consequence, all seeds with no convex $m$-gon for
$m\le6$ satisfy the upper bound for every $x\ge1$ and every threshold.

## Boundaries of the result

- This is an obstruction for the uniform $x$-blow-up in Corollary 15.
  It does not bound the arbitrary $(X,Y)$-blow-ups of Lemma 14.
- It neither proves the general Erdős–Szekeres conjecture nor excludes
  counterexamples already present at smaller polygon sizes in the seed.
- For $x=0$, (1) reduces to $B=N$; descent in polygon size and strict
  coefficient positivity are the reasons we assume $x\ge1$.
- The threshold assumptions exclude $L=0,N$ and $N=1$, where the
  two-endpoint formula being studied is not the stated Corollary 15.
- The proof is an ordinary mathematical argument. The companion exact
  checks validate identities, conventions and examples; they are not a
  proof by finite enumeration of this all-parameter theorem.

See [REFERENCES.md](REFERENCES.md) for attribution and the limited novelty
audit, including the inaccessible 2026 journal full text.
