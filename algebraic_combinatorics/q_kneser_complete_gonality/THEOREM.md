# Exact gonality of every ordinary q-Kneser graph

For a prime power `q`, let `qK(n,r)` be the simple graph whose vertices are
the `r`-dimensional subspaces of `F_q^n`, with adjacency meaning zero
intersection. Throughout, `n >= 2r >= 2`. Gaussian coefficients are denoted
by `{n bracket r}_q`, or in formulas by \({n\brack r}_q\).

## Theorem

For every prime power `q` and `n >= 2r >= 2`,

\[
 \boxed{\operatorname{sn}(qK(n,r))=\operatorname{gon}(qK(n,r))
 ={n\brack r}_q-{n-1\brack r-1}_q
 =q^r{n-1\brack r}_q.}                         \tag{1}
\]

Here `gon` is divisorial graph gonality and `sn` is scramble number.
This concerns ordinary q-Kneser graphs, not the generalized adjacency
condition `dim(U intersect W) < t` for `t>1`.

The new part beyond the [preceding density theorem](../q_kneser_dense_gonality/)
is the entire binary middle-dimensional family `q=2, n=2r, r>=2`.
For `G_r=qK(2r,r)` over `F_2`, set

\[
 N={2r\brack r}_2,\qquad d=2^{r^2},\qquad
 a={2r-1\brack r-1}_2=\frac{N}{2^r+1}.
\]

For every `r>=3`, the proof also gives the exact identities

\[
 \operatorname{rank}_{\mathbf F_2} A(G_r)=\binom{2r}{r},\qquad
 \alpha^c_3(G_r)=a,\qquad
 h(\mathcal E_4)=N-a,\qquad e(\mathcal E_4)=4d-12>N.       \tag{2}
\]

The quantity `alpha^c_l` is the largest size of a vertex set whose induced
components all have order at most `l`. The eggs of `E_k` are all connected
`k`-vertex sets; `h` and `e` denote its hitting and egg-cut numbers.

## 1. Standard spectral facts, with a derivation

For `qK(n,r)`, put

\[
 N={n\brack r}_q,\quad
 d=q^{r^2}{n-r\brack r}_q,\quad
 s=q^{r(r-1)}{n-r-1\brack r-1}_q.
\]

The formula for `d` follows by choosing an `r`-space in the quotient by a
fixed vertex and then a linear lift. The standard q-Kneser eigenvalues are

\[
 \theta_j=(-1)^j q^{r(r-j)+\binom j2}
                 {n-r-j\brack r-j}_q,\qquad 0\le j\le r.       \tag{3}
\]

Only their bounds, not their multiplicities, are needed. Here is a direct
derivation of those bounds. For a subspace `T` of dimension `j`, let
`f_T(U)=1` if `T` is contained in `U`, and zero otherwise. Counting lifts
in the quotient by `T` gives

\[
 (Af_T)(U)=q^{r(r-j)}{n-r-j\brack r-j}_q
                              1_{\{U\cap T=0\}}.             \tag{4}
\]

Subspace-lattice inclusion-exclusion gives

\[
 1_{\{U\cap T=0\}}=
 \sum_{X\le T}(-1)^{\dim X}q^{\binom{\dim X}{2}} f_X(U).
                                                               \tag{5}
\]

Indeed, on an intersection of dimension `b`, this sum is
`product_(i=0)^(b-1)(1-q^i)`, by the Gaussian binomial identity: it is one
for `b=0` and zero otherwise. Thus the filtration spanned by all `f_T` with
`dim T<=j` is `A`-invariant, and `A` acts as `theta_j` on its `j`th quotient.
The last space is the whole vertex-function space, since the `f_T` with
`dim T=r` are its coordinate vectors. Since `A` is real symmetric, all its
eigenvalues are among (3). Moreover,

\[
 \frac{|\theta_{j+1}|}{|\theta_j|}
 =q^{j-r}\frac{q^{r-j}-1}{q^{n-r-j}-1}<1\quad(0\le j<r).       \tag{6}
\]

Consequently `d=theta_0` is simple, the graph is connected, the least
eigenvalue is at least `-s=theta_1`, and on the orthogonal complement of
the constants the largest eigenvalue is at most `theta_2` when `r>=2`.
Formula (3) is classical; see Lv--Wang in [SOURCES.md](SOURCES.md).

For any vertex set `S` of size `m`, decomposing its characteristic vector
as `(m/N)1+x`, with `x` orthogonal to `1`, yields

\[
 2|E(G[S])|\ge\frac{d+s}{N}m^2-sm.                            \tag{7}
\]

For an independent set this gives the Hoffman bound

\[
 \alpha(G)\le H:=\frac{Ns}{d+s}={n-1\brack r-1}_q.            \tag{8}
\]

All `r`-spaces through a fixed line attain (8), so equality holds. This
recovers the ordinary vector-space EKR bound, not a new EKR theorem.
Similarly, if the nonconstant eigenvalues are at most `t`, then

\[
 |\partial S|\ge(d-t)\frac{m(N-m)}{N}.                         \tag{9}
\]

For `G_r`, (3) gives `s=2^(r(r-1))` and
`t=2^(r^2-2r+1)`, so for `r>=3`,

\[
 d-t\ge\frac{31}{32}d.                                        \tag{10}
\]

## 2. A rank--Hoffman criterion for small components

**Lemma.** Let `G` be a simple `d`-regular graph on `N` vertices whose real
adjacency eigenvalues are at least `-s`, where `s>0`. Suppose
`H=Ns/(d+s)` is an integer attained by an independent set. Let `R` be the
rank of its adjacency matrix over any field. For an integer `l>=2`, if

\[
 s\ge\binom l2 R,
\]

then `alpha^c_l(G)=H`.

**Proof.** Every nontrivial connected component has adjacency rank at least
two over any field: a principal matrix indexed by an edge has determinant
`-1`. If `G[S]` has all component orders at most `l`, each component has at
most `binom(l,2)` edges. Block additivity of rank therefore gives

\[
 2|E(G[S])|\le\binom l2\operatorname{rank}A[S]
                \le\binom l2 R\le s.                         \tag{11}
\]

If `m=|S|>=H+1`, the real spectral estimate (7) gives instead

\[
 2|E(G[S])|\ge\frac{d+s}{N}m(m-H)
             \ge\frac{d+s}{N}(H+1)>s,                        \tag{12}
\]

a contradiction. The independent set of order `H` proves attainability.
The integer assumption on `H` is used in passing from `m>H` to `m>=H+1`.
The ranks in (11) and the real spectral bound in (12) intentionally use
different fields. QED

## 3. Exterior rank on the binary boundary

Let `V=F_2^(2r)`. Associate to each `r`-space `U`, with basis
`u_1,...,u_r`, its nonzero Plucker vector

\[
 p_U=u_1\wedge\cdots\wedge u_r\in\bigwedge^r V.
\]

This is independent of the basis because every invertible matrix over
`F_2` has determinant one. Choose a volume form to identify
`wedge^(2r) V` with `F_2`. The bilinear pairing
`B(x,y)=x wedge y` on `wedge^r V` satisfies

\[
 B(p_U,p_W)=1\quad\Longleftrightarrow\quad U\cap W=0.           \tag{13}
\]

This uses the fact that the only nonzero scalar in `F_2` is one; it is not
an assertion about the unmodified adjacency matrix over arbitrary fields.
If `P` has the `p_U` as rows and `J` is the wedge-pairing matrix, then

\[
 A=PJP^{\mathsf T}\quad\hbox{over }\mathbf F_2,
 \qquad\operatorname{rank}_{\mathbf F_2}A\le\binom{2r}{r}.     \tag{14}
\]

On the coordinate `r`-spaces, the principal adjacency matrix pairs each
coordinate set with its complement. It is a permutation matrix of order
`binom(2r,r)`, so equality holds in (14).

For every `r>=3`,

\[
 2^{r(r-1)}>3\binom{2r}{r}.                                   \tag{15}
\]

At `r=3`, this is `64>60`. On increasing `r` by one, the left side grows
by `2^(2r)`, while the binomial coefficient grows by
`2(2r+1)/(r+1)<4`; induction proves (15). Apply the lemma of Section 2
with `l=3`, `R=binom(2r,r)`, and `H=a=N/(2^r+1)`. It follows that

\[
 \alpha^c_3(G_r)=a.                                           \tag{16}
\]

This is the missing structural bridge: even allowing isolated edges,
three-vertex paths, and triangles as disjointness components does not
increase the extremal family size.

## 4. The four-vertex scramble

For `r>=3`, the Gaussian product implies

\[
 \frac Nd
 =\prod_{h=1}^r\frac{1-2^{-(r+h)}}{1-2^{-h}}
 <\frac72.                                                    \tag{17}
\]

For completeness, the first three denominator factors have product
`21/64`. The remaining product is at least
`1-sum_(h=4)^r 2^(-h)>7/8`, using
`product(1-x_i)>=1-sum x_i`. Thus the denominator exceeds `147/512>2/7`,
and the numerator is less than one.

Consider any egg cut of `E_4`, and let its smaller side have `m` vertices.
Both sides contain a connected four-vertex egg, so `4<=m<=N/2`. If `m=4`,
its boundary has at least `4d-12` edges. If `m>=5`, equations (9)--(10)
and monotonicity of `m(N-m)` on `[0,N/2]` give

\[
 |\partial S|\ge5(d-t)(1-5/N)
 \ge5(31/32)^2d>4d.                                          \tag{18}
\]

Here `N>=d>=512`, which implies `1-5/N>=31/32`.
For the opposite bound, view `F_2^(2r)` as the two-dimensional space over
`F_(2^r)`. Its one-dimensional subspaces give a clique of order `2^r+1`
in `G_r`. Choose four of them. Their boundary is `4d-12`; the complement
has minimum degree at least `d-4>=508`, hence contains a connected
four-vertex set. This is an egg cut. We have proved

\[
 e(\mathcal E_4)=4d-12>N,                                    \tag{19}
\]

where the last inequality uses (17) and `d/2>12`.

A set hits every connected four-vertex set precisely when its complement
has no component of order four or larger. Thus (16) gives

\[
 h(\mathcal E_4)=N-a.
\]

The order of `E_4` is the minimum of its hitting and egg-cut numbers,
therefore it is exactly `N-a`. The standard scramble lower bound and the
independent-set upper bound for divisorial gonality give

\[
 N-a=\|\mathcal E_4\|\le\operatorname{sn}(G_r)
       \le\operatorname{gon}(G_r)\le N-a.                    \tag{20}
\]

These general scramble/gonality inequalities are external inputs, cited
in [SOURCES.md](SOURCES.md). Equation (20) proves (1) on the entire binary
middle-dimensional family with `r>=3`.

## 5. The small ranks

For `q=2,n=4,r=2`, we have `N=35,d=16,a=7` and nonconstant eigenvalues
bounded above by two. Use `E_2`. Its hitting number is `35-7=28`. In an
egg cut the smaller side has `2<=m<=17` vertices. For `m=2` the boundary
is at least `2d-2=30`. For `m>=3`, (9) gives

\[
 |\partial S|\ge14\cdot3\cdot32/35>30.
\]

An edge and its complement realize an egg cut of size 30; the complement
has minimum degree at least 14 and so contains an edge. Hence `E_2` has
order 28 and `sn=gon=28`.

For `r=1` and any `q,n>=2`, distinct lines are disjoint, so the graph is
complete. Its vertex scramble has order `N-1` and (8) gives `alpha=1`;
thus (1) follows in this case as well.

## 6. The remaining parameters

We include the earlier density argument to make (1) independently
readable. Suppose `r>=2`. The Gaussian product gives

\[
 \frac dN=\prod_{j=0}^{r-1}
       \frac{1-q^{-(n-r-j)}}{1-q^{-(n-j)}}.                    \tag{21}
\]

If `n>=2r+1`, the numerator product exceeds
`1-sum_(h=2)^(r+1)2^(-h)>1/2`. If `n=2r,q>=3`, it exceeds
`1-sum_(h=1)^r q^(-h)>1-1/(q-1)>=1/2`. Since every denominator factor
is less than one, in both cases `d>N/2`.

In any simple `d`-regular graph with `d>N/2` and `N>=4`, an egg cut of
`E_2` has smaller side size `2<=m<=floor(N/2)`, and

\[
 |\partial S|\ge m(d-m+1)\ge N-1.                            \tag{22}
\]

For the last inequality, the quadratic is concave in `m`, so it suffices
to check `m=2` and `m=floor(N/2)`; integrality of `d>N/2` proves both.
The hitting number is `N-alpha`, at most `N-1`. Therefore `E_2` already
has order `N-alpha`, and the same sandwich as (20) proves (1).

Finally, `N-alpha=q^r{n-1 bracket r}_q` is the Gaussian Pascal identity.
This completes all parameters. QED

## Claim and verification boundary

This is a written universal proof, not a conclusion extrapolated from the
finite audit. The code checks two independent subspace enumerations,
definition-level disjointness against the Plucker factorization, exact
binary ranks, integer incidence identities underlying the spectrum,
small component ranks, and all scalar inequalities over documented finite
ranges. The infinite statements follow from the displayed arguments.
The standard spectrum, EKR bound, finite-field exterior algebra, and the
general scramble/gonality inequalities are credited prior mathematics.
No proof-assistant formalization or independent peer review is asserted.
