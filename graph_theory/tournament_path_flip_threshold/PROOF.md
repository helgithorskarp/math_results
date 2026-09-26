# Existence and an upper bound for the tournament path flip threshold

Let an orientation of the path with $k$ edges be encoded by a word
$w=(w_1,\ldots,w_k)\in\{+,-\}^k$. Write $r(w)$ for the number of indices
with $w_i\ne w_{i+1}$. The orientation is **tournament anti-Sidorenko**
(TAS) if its homomorphism density in every finite tournament is at most
$2^{-k}$. Following Chen and Lin [CL], define

$$
 f(k)=\max\{m\in\{0,\ldots,k\}:\text{every }w\text{ with }r(w)<m
          \text{ is TAS}\}.
$$

**Theorem.** The limit

$$
 \beta=\lim_{k\to\infty}\frac{f(k)}k
$$

exists. More precisely,

$$
 \beta=\inf_{w\text{ not TAS}}\frac{r(w)+1}{|w|},
 \qquad
 \frac1{1665}\leq\beta\leq\frac12-\frac2{\pi^2}
 =0.297357632715324\ldots .
$$

The lower bound is [CL, Corollary 1.4]. The arguments below prove existence,
the variational formula, and the upper bound. They answer [CL, Question 6.1]
and give a partial bound for [CL, Problem 6.2]. They do not determine the
exact value of the limit.

## 1. Finite weighted tournaments and normalization

Take a matrix $W\in[0,1]^{q\times q}$ satisfying
$W+W^\top=J$, including $W_{ii}=1/2$. Its classes have equal mass $1/q$.
Put

$$
 M=\frac{2W}{q},\quad u=q^{-1/2}{\bf1},\quad
 M_+=M,\quad M_-=M^\top,\quad A_w=M_{w_1}\cdots M_{w_k}.
$$

Then the ratio of the weighted path density to the random baseline is

$$
 R_w(W):=2^kt(w,W)=u^\top A_wu
      =\frac1q{\bf1}^\top A_w{\bf1}.                 \tag{1}
$$

Indeed, expanding the matrix product sums exactly the $q^{k+1}$ assignments
of the vertices of the path to the classes.

A word is non-TAS if and only if $R_w(W)>1$ for some such finite matrix.
For the forward implication, start with a finite tournament violating TAS
and replace its zero diagonal by $1/2$. This only increases the count.
For the reverse implication, construct a random tournament on $N$ vertices
by assigning each vertex an independent uniform class and independently
orienting each unordered pair using $W$. Every injective map of the path
has expected edge-product $t(w,W)$. Thus the expected homomorphism density
is at least

$$
 \frac{(N)_{k+1}}{N^{k+1}}t(w,W)>2^{-k}
$$

for sufficiently large $N$. Some finite tournament therefore violates TAS.
Here $k$ is fixed before $N\to\infty$. No uniform assertion about this
host size is needed.

We may always require $0<W_{ij}<1$: replace $W$ by
$(1-\eta)W+\eta J/2$ for sufficiently small positive $\eta$. Continuity
of the finite polynomial $R_w$ preserves a strict violation. Rational
entries may likewise be obtained by sufficiently small approximation of
the entries above the diagonal.

For completeness, a non-TAS word exists for every $k\geq2$. Use an
alternating word and

$$
 M=W=\begin{pmatrix}1/2&1/2+\varepsilon\\
                    1/2-\varepsilon&1/2\end{pmatrix}
       =uu^\top+\varepsilon K,\qquad
 K=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
$$

In the expansion of (1), a term with an isolated $K$ vanishes because
$u^\top Ku=0$. At degree two, only adjacent pairs survive. For an
alternating word, each contributes
$-u^\top K^2u=1$. Hence

$$
 R_w(W)=1+(k-1)\varepsilon^2+O(\varepsilon^3)>1
$$

for sufficiently small $\varepsilon>0$. It follows that $f(k)$ is exactly
the minimum flip count of a non-TAS word of length $k\geq2$.

## 2. Reflection and amplification

Fix a non-TAS word $w$ of length $k$ and flip count $r$, and choose a
strictly positive matrix $W$ with $R=R_w(W)>1$. Let

$$
 w^\dagger=(-w_k,\ldots,-w_1),\qquad
 A=A_w,\qquad P=AA^\top=A_{ww^\dagger}.
$$

The reversal and sign change both matter. The matrix $P$ is symmetric,
positive semidefinite, and entrywise nonnegative. Since $\|u\|=1$,

$$
 u^\top Pu=\|A^\top u\|^2\geq (u^\top Au)^2=R^2>1.
$$

The spectral theorem and convexity of $x\mapsto x^t$ on $[0,\infty)$
give, for every positive integer $t$,

$$
 u^\top P^t u\geq(u^\top Pu)^t\geq R^{2t}.        \tag{2}
$$

There are $2r+1$ flips inside $ww^\dagger$, and one flip between any two
consecutive copies: the first sign is $w_1$ and the last is $-w_1$.
Thus $(ww^\dagger)^t$ has $2t(r+1)-1$ flips.

This construction also covers every sufficiently large length, not just
multiples of $2k$. Write $n=2kt+s$, $0\leq s<2k$, and append $s$
plus signs. Let $\gamma=\min_i\sum_jM_{ij}>0$. Then
$M^su\geq\gamma^su$ componentwise. Put
$c=\min(1,\gamma^{2k-1})>0$. Nonnegativity and (2) show

$$
 R_{(ww^\dagger)^t+^s}(W)
   =u^\top P^tM^su\geq cR^{2t}>1
$$

for all sufficiently large $t$, uniformly in $s$. The padding creates
at most one more flip. Consequently,

$$
 \limsup_{n\to\infty}\frac{f(n)}n\leq\frac{r+1}{k}
             \quad\text{for every non-TAS word }w.       \tag{3}
$$

Set $b=\inf_{w\text{ non-TAS}}(r(w)+1)/|w|$. Equation (3) gives
$\limsup f(n)/n\leq b$. For each $k\geq2$, choose a non-TAS word with
$r=f(k)$. Then $b\leq(f(k)+1)/k$, and so
$b\leq\liminf f(k)/k$. The limit exists and equals $b$.

## 3. Mixing directed and alternating segments

Here is a separate upper-bound mechanism. Let $W$ be strictly positive,
let $M=2W/q$, and suppose that its Perron eigenvalue and largest singular
value satisfy

$$
 0<\lambda=\rho(M)<1<\mu=\|M\|_2.
$$

The matrices $M$ and $B=MM^\top$ have strictly positive Perron
eigenvectors $v,z$, with eigenvalues $\lambda,\mu^2$. Choose constants
$a,b>0$ with $u\geq az$ and $z\geq bv$ componentwise. It follows that

$$
 u^\top M^LB^mu\geq ab(u^\top v)\lambda^L\mu^{2m}
                   \quad(L,m\geq0).                    \tag{4}
$$

For fixed $0<\theta<1$, put $m=\lfloor\theta n/2\rfloor$,
$L=n-2m$, and use the word $+^L(+-)^m$. Its flip count is $2m-1$
once $L,m>0$. By (4), it is non-TAS for all sufficiently large $n$ if

$$
 (1-\theta)\log\lambda+\theta\log\mu>0.
$$

Taking decreasing values of $\theta$ proves

$$
 \beta\leq\frac{-\log\lambda}{\log\mu-\log\lambda}.   \tag{5}
$$

## 4. A perturbation of regular carousel tournaments

Let $q\geq3$ be odd and let $S$ be the skew-symmetric matrix defined by

$$
 S_{ij}=\begin{cases}
 0&i=j,\\
 1&1\leq(j-i)\bmod q\leq(q-1)/2,\\
 -1&\text{otherwise}.
 \end{cases}
$$

Write $K=S/q$, $u=q^{-1/2}{\bf1}$, and

$$
 v_i=\sqrt{2/q}\cos(2\pi i/q),\qquad
 z_i=-\sqrt{2/q}\sin(2\pi i/q),\qquad
 \kappa_q=\frac1q\cot\frac{\pi}{2q}.
$$

The vectors $u,v,z$ are orthonormal, $Ku=0$,
$Kv=\kappa_qz$, and $Kz=-\kappa_qv$. These identities follow from the
finite geometric series; in particular,

$$
 2\sum_{j=1}^{(q-1)/2}\sin(2\pi j/q)=\cot(\pi/(2q)).
$$

For fixed $0<a<1$, set

$$
 M(\delta)=uu^\top+aK+\delta(vu^\top-uv^\top),\qquad
 W(\delta)=\frac q2M(\delta),\qquad s=a\kappa_q.
$$

This is a valid, strictly positive weighted tournament whenever

$$
 0<|\delta|<\frac{1-a}{2\sqrt2}.
$$

Indeed $W+W^\top=J$, its diagonal is $1/2$, and the perturbation of any
entry from $1/2+aS_{ij}/2$ has absolute value at most $\sqrt2|\delta|$.

The subspace spanned by $u,v,z$ reduces $M(\delta)$. Its matrix there is

$$
 T(\delta)=\begin{pmatrix}
 1&-\delta&0\\
 \delta&0&-s\\
 0&s&0
 \end{pmatrix}.                                          \tag{6}
$$

On the orthogonal complement, $M(\delta)=aK$. Since
$\|K\|_2\leq\sqrt{\|K\|_1\|K\|_\infty}=(q-1)/q<1$, the eigenvalue
and singular value equal to one at $\delta=0$ are simple and separated
from all other eigenvalues and singular values. In particular $0<s<1$.

The characteristic polynomial of (6) is

$$
 (x-1)(x^2+s^2)+\delta^2x.
$$

The simple real eigenvalue near one is therefore

$$
 \lambda(\delta)=1-\frac{\delta^2}{1+s^2}+O(\delta^4).  \tag{7}
$$

It is the Perron eigenvalue, since the full matrix is strictly positive
and all other eigenvalues have modulus bounded away from one at zero.
For the singular value, compute

$$
 T T^\top=\begin{pmatrix}
 1+\delta^2&\delta&-s\delta\\
 \delta&s^2+\delta^2&0\\
 -s\delta&0&s^2
 \end{pmatrix}.
$$

If $p(x,\delta)=\det(xI-TT^\top)$, direct expansion gives

$$
 p(1,\delta)=-2(1-s^2)\delta^2+\delta^4,
 \qquad \partial_xp(1,0)=(1-s^2)^2.
$$

Thus its simple largest eigenvalue is
$1+2\delta^2/(1-s^2)+O(\delta^4)$, and

$$
 \mu(\delta)=1+\frac{\delta^2}{1-s^2}+O(\delta^4).       \tag{8}
$$

The expansions follow equally from the analytic implicit function
theorem applied to the displayed polynomials. Evenness in $\delta$
justifies the stated remainders. For sufficiently small nonzero $\delta$,
(7)--(8) satisfy the hypotheses of (5). Consequently

$$
 \beta\leq\lim_{\delta\to0}
 \frac{-\log\lambda(\delta)}{\log\mu(\delta)-\log\lambda(\delta)}
 =\frac{1-s^2}{2}.
$$

This holds for every odd $q\geq3$ and every $a<1$. First let $a\uparrow1$
and then let $q\to\infty$. Since $\kappa_q\to2/\pi$, we obtain

$$
 \boxed{\beta\leq\frac12-\frac2{\pi^2}}.
$$

All parameters are fixed before taking the path-length limit in (5).
The subsequent infimum over valid parameters does not claim that a single
weighted tournament realizes the limiting constant.

## 5. An entirely rational certificate at density 3/10

The accompanying certificate supplies a separate exact example. Take
$q=13$, $D=5{,}000{,}000$, the carousel matrix $S$ above, and

$$
 h=(1000,885,568,121,-355,-749,-971,-971,-749,-355,121,568,885).
$$

Define the integer matrix and normalized transfer matrix

$$
 H_{ij}=2{,}500{,}000+2{,}497{,}500S_{ij}+h_i-h_j,
 \quad W=H/D,\quad M=H/32{,}500{,}000.
$$

All entries of $W$ are strictly between zero and one and
$W+W^\top=J$. Set

$$
 Q=M^{5600}(MM^\top)^{1200},\qquad
 g=\frac{25{,}000{,}001}{25{,}000{,}000}.
$$

`certificate.json` gives a positive integer vector $b$ with
$b_{\min}=10^{16}$. Two different integer computations certify
$Qb>gb$ componentwise. A further exact calculation certifies

$$
 M^j{\bf1}\geq\frac{999}{1000}\frac{b}{b_{\min}}
                   \quad(0\leq j<8000).                 \tag{9}
$$

The computation rounds **down** after each multiplication by a
nonnegative rational matrix. Induction makes each computed vector a
rigorous lower bound, so no floating-point tolerance or eigenvalue
approximation is part of this certificate.

Write $n=8000t+j$, $0\leq j<8000$, and use the word

$$
 \bigl(+^{5600}(+-)^{1200}\bigr)^t+^j.
$$

Equations (1) and (9) give its normalized density at least

$$
 \frac{999}{1000}g^t
 \geq\frac{999}{1000}\left(1+\frac{t}{25{,}000{,}000}\right)>1
                  \quad(t\geq30{,}000).
$$

The last step is Bernoulli's inequality. The word has $2400t-1$ flips
when $j=0$, and $2400t$ flips otherwise. Hence the exact certificate
proves

$$
 f(n)\leq2400\lfloor n/8000\rfloor\leq\frac{3n}{10}
                       \quad(n\geq240{,}000{,}000).
$$

This explicit threshold is deliberately not optimized. The 8000-edge
period itself is not asserted to violate TAS: the certificate proves
growth on the positive vector $b$, followed by the amplification above.

## Sources and status

- [CL] H. Chen and Y. Lin, *Oriented Paths with Few Direction Flips Are
  Tournament Anti-Sidorenko*, arXiv:2609.14655v1, 13 September 2026,
  [primary text](https://arxiv.org/html/2609.14655v1).
- [CCN] H. Chen, F. C. Clemen and J. A. Noel, *On Tournament Anti-Sidorenko
  Orientations of Trees*, arXiv:2605.14138v2, 22 September 2026,
  [primary text](https://arxiv.org/html/2605.14138v2).
- [HMNTW] X. He, N. Mani, J. Nie, N. Tung and F. Wei, *New Sidorenko-type
  inequalities in tournaments*, arXiv:2512.11222v1,
  [primary text](https://arxiv.org/html/2512.11222v1).

The existence proof and analytic upper bound are ordinary mathematical
arguments, not computational deductions. The rational example is an exact
computer-assisted certificate. Neither has been formally verified or
independently peer reviewed. The novelty claim is limited to the primary
sources and Discovery Net material searched on 26 September 2026.
