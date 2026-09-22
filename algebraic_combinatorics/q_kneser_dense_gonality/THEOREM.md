# The half-density threshold and gonality of q-Kneser graphs

Write

\[
{m\brack s}_q=\prod_{i=0}^{s-1}\frac{q^{m-i}-1}{q^{s-i}-1}
\]

for a Gaussian binomial coefficient. Let `qK(n,r)` be the simple graph whose
vertices are the `r`-subspaces of `F_q^n`, with two distinct vertices adjacent
exactly when their intersection is zero.

## Theorem

Let `q` be a prime power and `n >= 2r >= 2`. Put

\[
N={n\brack r}_q,
\qquad
d=q^{r^2}{n-r\brack r}_q.
\]

Then `qK(n,r)` has `N` vertices and is `d`-regular. Moreover,

\[
d>\frac N2
\]

if and only if `(q,n,r)` is not in the family

\[
q=2,\qquad n=2r,\qquad r\ge2. \tag{1}
\]

Outside (1),

\[
\operatorname{sn}(qK(n,r))
=\operatorname{gon}(qK(n,r))
=N-{n-1\brack r-1}_q
=q^r{n-1\brack r}_q. \tag{2}
\]

Here `sn` is scramble number and `gon` is divisorial gonality.

## Proof

### 1. Vertex, degree, and independence counts

The vertex count is `N={n\brack r}_q`. Fix an `r`-subspace `R` and a
complement of it. An `r`-subspace disjoint from `R` projects injectively to an
`r`-subspace of the `(n-r)`-dimensional quotient. Conversely, after choosing
such an image, every linear map from it to `R` gives a distinct graph
subspace disjoint from `R`. There are `q^(r^2)` such maps. Hence every vertex
has degree

\[
d=q^{r^2}{n-r\brack r}_q. \tag{3}
\]

An independent set in `qK(n,r)` is a pairwise nontrivially intersecting
family of `r`-subspaces. For `n>=2r+1`, the vector-space Erdős--Ko--Rado
theorem gives

\[
\alpha(qK(n,r))={n-1\brack r-1}_q. \tag{4}
\]

For completeness, (4) at `n=2r` follows from a spread argument. Identify
`F_q^(2r)` with the two-dimensional space over `F_(q^r)`. Its one-dimensional
`F_(q^r)`-subspaces form an `r`-spread of `q^r+1` pairwise disjoint
`r`-subspaces. Take the orbit of this spread under `GL(2r,q)`. Transitivity on
`r`-subspaces implies that every vertex occurs in the same positive number
`c` of orbit spreads. If `A` is intersecting, it contains at most one member
of each spread. Double-counting incidences of a member of `A` with an orbit
spread gives

\[
|A|c\le |\mathcal P|,
\qquad
Nc=(q^r+1)|\mathcal P|,
\]

and hence

\[
|A|\le\frac{N}{q^r+1}={2r-1\brack r-1}_q.
\]

The family of all `r`-subspaces through a fixed line attains this bound. Thus
(4) holds also at `n=2r`. Only the extremal value, not uniqueness of the
extremal family, is needed below.

### 2. The Gaussian product is above one half off (1)

From (3),

\[
\begin{aligned}
\frac dN
&=q^{r^2}\frac{{n-r\brack r}_q}{{n\brack r}_q}\\
&=\prod_{j=0}^{r-1}
  \frac{1-q^{-(n-r-j)}}{1-q^{-(n-j)}}. \tag{5}
\end{aligned}
\]

Every denominator factor on the right of (5) lies strictly between zero and
one. Also, for numbers `0<=x_j<=1`, induction gives
`product(1-x_j) >= 1-sum(x_j)`. Therefore

\[
\frac dN
>
1-\sum_{j=0}^{r-1}q^{-(n-r-j)}. \tag{6}
\]

If `n>=2r+1`, the exponents in the sum in (6) are at least
`2,3,...,r+1`. Since `q>=2`,

\[
\sum_{j=0}^{r-1}q^{-(n-r-j)}
\le \sum_{h=2}^{r+1}2^{-h}<\frac12.
\]

Thus `d/N>1/2` throughout `n>=2r+1`.

It remains to take `n=2r`. If `q>=3`, then

\[
\sum_{j=0}^{r-1}q^{-(r-j)}
=\sum_{h=1}^{r}q^{-h}
<\frac1{q-1}\le\frac12,
\]

so (6) again gives `d/N>1/2`. If `q=2` and `r=1`, the graph is the complete
graph on three vertices, and `d/N=2/3`.

### 3. The omitted family is genuinely below one half

Let `q=2`, `n=2r`, and `r>=2`. Formula (5) becomes

\[
\frac dN=
\frac{\prod_{h=1}^{r}(1-2^{-h})}
     {\prod_{h=r+1}^{2r}(1-2^{-h})}. \tag{7}
\]

The numerator in (7) is at most
`(1-1/2)(1-1/4)=3/8`. For the denominator, the same elementary product
inequality gives

\[
\prod_{h=r+1}^{2r}(1-2^{-h})
\ge 1-\sum_{h=r+1}^{2r}2^{-h}
=1-2^{-r}(1-2^{-r})>\frac34.
\]

Consequently `d/N<(3/8)/(3/4)=1/2`. This proves the claimed exact
classification of the half-density threshold.

### 4. Scramble number and gonality

A theorem of Echavarria--Everett--Huang--Jacoby--Morrison--Weber says that a
simple graph `G` on `N` vertices with

\[
\delta(G)\ge \left\lfloor\frac N2\right\rfloor+1
\]

satisfies

\[
\operatorname{sn}(G)=\operatorname{gon}(G)=N-\alpha(G). \tag{8}
\]

Outside (1), `d>N/2`; since `d` is integral, the hypothesis of (8) holds.
Substitute (4). Finally the Gaussian recurrence

\[
{n\brack r}_q={n-1\brack r-1}_q+q^r{n-1\brack r}_q
\]

turns `N-alpha` into the last expression in (2). This proves (2).  QED

## Scope of the remaining boundary

For `q=2`, `n=2r`, `r>=2`, Section 3 proves only that the dense-graph bridge
cannot apply. It neither determines nor conjectures the exact scramble number
or gonality there. The smallest omitted graph, `qK(4,2)`, has `N=35` and
`d=16`.
