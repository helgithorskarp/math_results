# Proof of the `2p+1` positive-inertia descent theorem

## 1. Setup

Let `p >= 5` be prime and `(n,p)=1`.  We use

\[
G=\mathbb Z_n\times\mathbb Z_p\cong\mathbb Z_{np}.
\]

For a set `E` in `G`, write `E_j` for its `j`-th `p`-level.  We say that
`E` has **p-descent** when, for every `d | n`,

\[
 \Phi_{dp}\mid m_E \quad\Longrightarrow\quad \Phi_d\mid m_E. \tag{1}
\]

Suppose `(A,Lambda)` is a spectral pair of cardinality

\[
k=2p+1. \tag{2}
\]

We prove that at least one of `A,Lambda` has p-descent.

The following three inputs are used.

1. **Levelwise cuboid rule.**  If `E` fails p-descent, then for some `d|n`
   there is a `d`-cuboid `Delta` for which all integers
   `E_j^d[Delta]` are equal to a common nonzero integer.  In particular every
   `E_j` is nonempty.  This is the levelwise cube rule together with the
   cuboid criterion in Somlai, arXiv:2607.26534, Lemma 2.2 and Corollary 2.2.

2. **Singleton gap.**  If both members fail p-descent, a member having a
   singleton level cannot have another level of size `r` with
   `2 <= r <= p-1`.  This is the strengthening proved in the independent
   review at Discovery Net artifact
   `bafkreiblx2snoz4gqjcu4kngr7ry37ycq2czpqo3ewfzlhfjzl4doqwcyi`.
   A short proof is repeated in Section 3.

3. **Simultaneous one-fat-level obstruction.**  If both first projections
   are injective, the two members cannot both have profile
   `(r,1^(p-1))`, for any `r>=2`.  This is Discovery Net artifact
   `bafkreigcrrcusbynjogmlxdwzmpouacnrc3cz4nterv2a7cottfgayccae`.
   Its block-Gram certificate is recalled in Section 6.

## 2. Injectivity and cross-level Fourier equality

Because `p` does not divide `k`, both projections to `Z/nZ` are injective.
Indeed, a collision in the first projection of `A` would give two points of
`A` whose difference has order `p`.  Spectral-pair symmetry would force
`Phi_p | m_Lambda`, hence `p | |Lambda|`, a contradiction.  Interchange the
two members for the other projection.

We will repeatedly use the following equality.  Let `(b,u),(c,v)` be points
of one member on distinct `p`-levels and put `x=b-c` in `Z/nZ`.  Projection
injectivity gives `x != 0`.  If the other member is `E`, orthogonality gives

\[
 \sum_{j=0}^{p-1}\zeta_p^{(u-v)j}S_j(x)=0,
 \qquad
 S_j(x)=\sum_{a\in E_j}\zeta_n^{xa}. \tag{3}
\]

Let `d` be the order of `x` in `Z/nZ`.  The coefficients `S_j(x)` lie in
`K=Q(zeta_d)`, and `(d,p)=1`.  Hence
`[K(zeta_p):K]=p-1`, so `Phi_p` is irreducible over `K`.
The coefficient polynomial in (3) has degree at most `p-1`, so it is a scalar
multiple of `Phi_p`.  Thus

\[
 S_0(x)=S_1(x)=\cdots=S_{p-1}(x). \tag{4}
\]

## 3. The singleton gap

Assume both descents fail.  By the levelwise cuboid rule, all `p` levels of
both members are nonempty.  Suppose `A` has a singleton level `{alpha}` and
an `r`-point level `{a_1,...,a_r}`, where `2 <= r <= p-1`.

Choose `(b_u,u)` in `Lambda` for every `u in Z/pZ`.  For distinct `u,v`,
equation (4), comparing the two selected levels of `A`, gives

\[
 \sum_{i=1}^r
 \zeta_n^{(b_u-b_v)(a_i-\alpha)}=1. \tag{5}
\]

Hence the `p` vectors

\[
 v_u=(\zeta_n^{b_u(a_i-\alpha)})_{i=1}^r\in\mathbb C^r
\]

have Gram matrix `(r-1)I_p+J_p`.  Its eigenvalues are `r-1` with
multiplicity `p-1` and `r+p-1` once, so it has rank `p`.  This contradicts
the fact that `p` vectors in `C^r` have Gram rank at most `r<p`.  The
singleton gap follows.

## 4. The only two profiles for `p >= 5`

Continue to suppose both descents fail.  Every level is nonempty, so each
level-size profile is a composition of `2p+1` into `p` positive parts.

If a profile contains a singleton, the singleton gap says every other part
is either `1` or at least `p`.  There cannot be two parts at least `p`, since
their sum together with the remaining `p-2` positive parts would be at least
`3p-2 > 2p+1` for `p>=5`.  Hence the profile is

\[
 S=(p+2,1^{p-1}). \tag{6}
\]

If a profile contains no singleton, every part is at least two.  Relative to
the baseline sum `2p`, there is exactly one surplus unit, so the profile is

\[
 D=(3,2^{p-1}). \tag{7}
\]

Thus each of `A,Lambda` has profile `S` or `D`.

## 5. Positive inertia excludes the dense profile

We prove the new structural lemma.

> **Positive-inertia lemma.**  Under the injectivity and nonempty-level
> hypotheses above, a member cannot have profile `D` when `p>3`.

Suppose `A` has a three-point level `P` and a two-point level `Q`.  For each
`lambda=(b,u)` in `Lambda`, form the phase vectors

\[
 v_\lambda=(\zeta_n^{ba})_{a\in P}\in\mathbb C^3,
 \qquad
 w_\lambda=(\zeta_n^{ba})_{a\in Q}\in\mathbb C^2.
\]

Let `V` and `W` be their Gram matrices, and put `M=V-W`.  If two points of
`Lambda` lie on different `p`-levels, equation (4), comparing `P` and `Q`,
says the corresponding entry of `M` is zero.  Therefore `M` is block diagonal,
with one Hermitian block for every `p`-level of `Lambda`.

Every diagonal entry of `M` is `3-2=1`.  All levels of `Lambda` are nonempty,
so every diagonal block has positive trace and hence at least one positive
eigenvalue.  Consequently

\[
 n_+(M)\ge p, \tag{8}
\]

where `n_+` is positive inertia.

On the other hand, `V` and `W` are positive semidefinite and `rank(V)<=3`.
For any two positive semidefinite matrices,

\[
 n_+(V-W)\le \operatorname{rank}(V). \tag{9}
\]

To see this, if the positive eigenspace of `V-W` had dimension larger than
`rank(V)`, it would meet `ker(V)` nontrivially.  On a nonzero vector in that
intersection the quadratic form of `V-W` is both positive and equal to the
nonpositive form `-W`, a contradiction.  Equations (8)--(9) give `p<=3`,
contrary to `p>=5`.  This proves the lemma.

## 6. Completion by the block-Gram obstruction

The positive-inertia lemma eliminates profile `D` on either side.  Thus both
members would have profile `S=(r,1^(p-1))`, where `r=p+2`.

For completeness, the earlier simultaneous one-fat-level obstruction forms
`r+p-1` phase vectors in `C^r`.  Cross-level equality (4) and orthogonality
within the fat level force their Gram matrix as follows.  Let
`a_1,...,a_r` be the fat level of `A`, fix a singleton coordinate `alpha`,
and use the vectors

\[
 v_{(b,u)}=(\zeta_n^{b(a_i-\alpha)})_{i=1}^r.
\]

For two `Lambda` points on different levels, (4), comparing the fat level
with `{alpha}`, gives inner product one.  Comparing any other singleton
coordinate of `A` with `alpha` also shows that their normalized phases agree
for every such cross-level difference.  If two `Lambda` points lie on its fat
level, subtract their respective differences from a fixed `Lambda` singleton.
The normalized singleton phases still agree for the resulting same-level
difference.  Orthogonality of the two fat-level points, now with zero
`p`-phase, says that their fat-level inner product is `-(p-1)`.  The diagonal
inner products are `r`.  Therefore, ordering the `Lambda` fat level first,
the Gram matrix is

\[
G=\begin{pmatrix}
(r+p-1)I_r-(p-1)J_r & J_{r,p-1}\\
J_{p-1,r} & (r-1)I_{p-1}+J_{p-1}
\end{pmatrix}. \tag{10}
\]

Writing `k=r+p-1`, evaluate (10) on the real vector taking value `k-1` on
the first block and `-r` on the second.  The result is

\[
-r(k-1)(r-1)(p-2)k<0, \tag{11}
\]

contradicting positive semidefiniteness of a Gram matrix.  Hence two-sided
descent failure is impossible.

## 7. Projection and tiling consequences

At least one member has p-descent.  Applying Somlai's projection lemma to
that member, and using injectivity of both projections, shows that the two
projections form a spectral pair in `Z/nZ`.  If every `(2p+1)`-point spectral
subset downstairs tiles, the projected set has a tiling complement `C`.
The original set is an injective graph over its projection and therefore
tiles `Z/nZ x Z/pZ` with complement `C x Z/pZ`.

For `(n,p)=(210,11)`, Fuglede's conjecture holds downstairs by the published
`pqrs` theorem.  A 23-point spectral set in `Z/210Z` would tile, which is
impossible because a tile cardinality divides 210.  Therefore no 23-point
spectral subset of `Z/2310Z` exists.

## 8. Sharp boundary of this argument

At `p=3`, inequality (8) can meet the rank-three upper bound, rather than
contradict it.  Counting also permits the extra profile `(3,3,1)` alongside
`(5,1,1)` and `(3,2,2)`.  No `p=3` theorem is claimed.  Cardinality `2p` is
also outside the statement because projection injectivity need not hold when
`p` divides the cardinality.
