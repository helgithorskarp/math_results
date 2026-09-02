# Lucas–Bergeron–Vessenes: sign rigidity, an infinite case, and verification

## Setup

Put $e_1=q+t$, $e_2=qt$, and define Lucas polynomials by

\[
L_0=0,\qquad L_1=1,\qquad L_{n+1}=e_1L_n+e_2L_{n-1}.
\]

The Lucas binomial is

\[
\left\{\begin{matrix}n\\k\end{matrix}\right\}
=\frac{L_n!}{L_k!L_{n-k}!}.
\]

It is the image of the homogeneous Gaussian binomial under the involution
$\mathcal A:e_1\mapsto e_1,\ e_2\mapsto-e_2$. Bergeron's 2026 overview
conjectures that, whenever

\[
1\le a\le b,c\le d,\qquad ad=bc,
\]

the difference

\[
\Delta_L=
\left\{\begin{matrix}b+c\\b\end{matrix}\right\}
-\left\{\begin{matrix}a+d\\a\end{matrix}\right\}
\tag{1}
\]

is Schur-positive up to a global sign. That source reports an exact check
through $ad=bc\le36$.

The results below concern nontrivial comparisons. After swapping $b,c$ if
needed, these have

\[
1\le a<b\le c<d,\qquad N:=ad=bc.
\]

## 1. The global sign is forced

**Lemma.** In the two-variable Schur expansion

\[
\Delta_L=\sum_{i=0}^{\lfloor N/2\rfloor}
g_i s_{(N-i,i)}(q,t),
\]

one has

\[
g_0=\cdots=g_a=0,
\qquad g_{a+1}=(-1)^{a+1}.
\tag{2}
\]

Consequently, if (1) is Schur-positive up to a global sign, that sign must be
$(-1)^{a+1}$. The conjecture has the unambiguous normalized form

\[
(-1)^{a+1}\Delta_L\quad\text{is Schur-positive}.\tag{3}
\]

**Proof.** Dehomogenize the ordinary Gaussian difference

\[
\Delta_G(q)=
{b+c\brack b}_q-{a+d\brack a}_q.
\]

The coefficient of $q^r$ counts partitions of $r$ in the relevant
rectangle. For $0\le r\le a$, every partition of $r$ fits in both the
$a\times d$ and $b\times c$ rectangles, so these coefficients vanish in
$\Delta_G$. At $r=a+1$, every partition fits in the $b\times c$
rectangle, while exactly $1^{a+1}$ fails to fit in the $a\times d$
rectangle. Thus the first nonzero coefficient of $\Delta_G$ is $+1$ at
degree $a+1$.

Write the homogeneous form as

\[
\Delta_G=\sum_j\gamma_j e_1^{N-2j}e_2^j.
\]

After setting $t=1$, the $j$-th basis term starts with $q^j$ with
coefficient one. Triangularity therefore gives
$\gamma_0=\cdots=\gamma_a=0$ and $\gamma_{a+1}=1$. Applying
$\mathcal A$ changes $\gamma_j$ by $(-1)^j$, so the first nonzero
monomial coefficient of $\Delta_L(q,1)$ is $(-1)^{a+1}$ at degree
$a+1$. Finally, for a symmetric homogeneous polynomial with
$P(q,1)=\sum p_iq^i$, its Schur coefficient at $s_{(N-i,i)}$ is
$p_i-p_{i-1}$. This proves (2). ∎

## 2. The complete $b=2$ family

**Theorem.** For every integer $c\ge2$, the admissible comparison
$(a,b,c,d)=(1,2,c,2c)$ satisfies the exact identity

\[
\boxed{
\left\{\begin{matrix}c+2\\2\end{matrix}\right\}
-\left\{\begin{matrix}2c+1\\1\end{matrix}\right\}
=e_2^2\left\{\begin{matrix}c\\2\end{matrix}\right\}.}
\tag{4}
\]

In particular, (1) is $e$-positive, hence Schur-positive, throughout this
infinite family.

**Proof.** The Lucas addition identity gives
$L_{2c+1}=L_{c+1}^2+e_2L_c^2$. Since $L_2=e_1$, the left side of (4) is

\[
\frac{L_{c+2}L_{c+1}}{e_1}-L_{2c+1}
=e_2L_c\left(\frac{L_{c+1}}{e_1}-L_c\right)
=e_2^2\frac{L_cL_{c-1}}{e_1},
\]

using $L_{c+1}-e_1L_c=e_2L_{c-1}$. The last expression is the right side
of (4). Lucas binomials lie in $\mathbb N[e_1,e_2]$, so the final claim
follows. ∎

## 3. Exact finite theorem

**Computer-assisted theorem.** For every positive quadruple satisfying

\[
1\le a<b\le c<d,\qquad ad=bc\le500,
\]

the normalized polynomial (3) is Schur-positive. There are exactly 2,898
nontrivial rectangle comparisons in this range.

The production computation uses the factorization

\[
L_n=\prod_{r\mid n,\ r>1}A_r,
\qquad
\left\{\begin{matrix}n\\k\end{matrix}\right\}
=\prod_{r=2}^n
A_r^{\lfloor n/r\rfloor-\lfloor k/r\rfloor-\lfloor(n-k)/r\rfloor},
\tag{5}
\]

where every exponent in (5) is zero or one. It constructs each $A_r$ by
exact monic division in $\mathbb Z[q]$ after the lossless homogeneous
specialization $t=1$. All factor pairs $x\le y$ of every $N\le500$
are enumerated, and every ordered pair of distinct factor pairs gives exactly
one canonical quadruple $a<b\le c<d$.

If $P(q,1)=\sum_{i=0}^Np_iq^i$ is symmetric, then

\[
P(q,t)=\sum_{i=0}^{\lfloor N/2\rfloor}
(p_i-p_{i-1})s_{(N-i,i)}(q,t),\qquad p_{-1}=0.\tag{6}
\]

The program checks every sign-normalized coefficient in (6), checks (2) on
every instance, and hashes the complete sequence of coefficient vectors.

## Reproduction

Requires CPython 3.11 or newer and no third-party packages.

```bash
python3 lucas_bergeron_vessenes/enumerate.py \
  --max-product 500 \
  --expect lucas_bergeron_vessenes/certificate.json

python3 lucas_bergeron_vessenes/independent_check.py
```

The independent checker does not use atoms or import the production code. It
constructs each Lucas binomial directly from its defining factorial quotient,
performs a separate exact monic division, and compares the full canonical
coefficient-record hash with `certificate.json`.

## Trust boundary and scope

The finite theorem trusts the CPython interpreter, integer arithmetic, file
I/O for the compact certificate, SHA-256 as a record binding, and inspection
of the two short programs. There is no floating point, randomized search,
external CAS, solver, native extension, or omitted data. The independent
checker uses a different mathematical decomposition but the same interpreter.

The finite theorem is not evidence for cases with $ad>500$, and the two
symbolic results do not settle the full conjecture. Equation (4) is elementary;
its value here is that it closes one infinite family in the newly proposed
Lucas version. No literature-priority claim is made.

## Primary sources

- François Bergeron, *A (q,t)-Overview of q-Analogs*, arXiv:2608.30979,
  especially the Lucas analogue of the Bergeron–Vessenes conjecture:
  <https://arxiv.org/abs/2608.30979>.
- Charles Brittenham, Andrew Carroll, T. Kyle Petersen, and Connor Thomas,
  *Unimodality via alternating gamma vectors*, for the anti-involution and
  Lucas-binomial gamma interpretation: <https://arxiv.org/abs/1601.04979>.
- Bruce Sagan and Carla Savage, *Combinatorial interpretations of binomial
  coefficient analogues related to Lucas sequences*, for positivity and the
  rectangle model of Lucas binomials: <https://arxiv.org/abs/0911.3159>.
- Fabrizio Zanello, *On Bergeron's positivity problem for q-binomial
  coefficients*, for the ordinary Gaussian precursor and its $a\le3$
  cases: <https://arxiv.org/abs/1709.06187>.
