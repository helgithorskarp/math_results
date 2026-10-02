# A nonzero quartic mass coefficient at every distinct angular stationary profile

Actual author **six-sendov-2**, role **researcher**. Complete ordinary
algebraic lemma with a portable exact certificate; unformalized and
independently unreviewed. Fixed Sylvester matrices, elimination, integer
Gauss, and exact interpolation are classical. The preceding same-author
stationary reduction is an explicit theorem premise.

## 1. Statement, input, and usefulness

Use the **complete** five-by-three polynomial matrix of
[LEMMA9550](../degree-five-triangular/PROOF.md), source
**cb4cf7d9d83f3d376d3763b65cbe2fddd50637f4**. Its rows are
\((A_i,L_i,C_i)\), indexed zero through four in the order
\((tO_2,tO_1,tO_0,K_1,K_0+4)\), and its five scalar equations are

\[
R_i=A_it^2+L_it+C_i=0.
\]

The letter \(L_i\) distinguishes a row's linear coefficient from the
critical coefficient \(B\). The matrix is defined over
\(\mathbb Q[B,E,r,s]\); its **entire coefficients**, including zero
entries, are regenerated from the
[pinned source](../degree-five-triangular/verify.py) and
[whole typed fixture](../degree-five-triangular/expected.json).

**Algebraic theorem.** For every \(B,E,r\in\mathbb C\), the five
polynomials \(R_i(B,E,r,0,t)\) have **no common finite complex root**
\(t\). This includes \(t=0\). Matrix rank alone is not the assertion:
a rank-two matrix can have its kernel off the scalar conic.

**Original-root corollary.** For every balanced stationary profile of
eight **distinct real original coordinates**, the mass interpolant has
\(p_4\ne0\). In particular the normalized chart has \(s\ne0\).
This uses the original framework of
[7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and the exact-degree-five/strict-feasibility premise of
[9496](../mass-stationary-chart/PROOF.md), as imported by9550.
There is no maximum, high-value, energy, small-variance or separation
premise. The normalized chart retains \(N=1,t=p_5>0\), seven simple
real critical roots, strict \(p(\lambda_j)>0\), and **all five equations**.
Normalization and reflection preserve the condition \(p_4=0\), and
\(p_4=st\), so the algebraic theorem proves the corollary.

The individual condition \(B=0\), equivalently zero third original
moment, is not excluded here when \(s\ne0\). No quantitative lower
bound for \(|p_4|\), original collision extension, full rank-two
classification, or global angular optimum is claimed. The complex
parameters in the algebraic theorem do not represent arbitrary actual
complex disk-rooted original polynomials.

This closes the previously retained \(s=0\) scalar branch of
[9602](../regular-linear-pencil/PROOF.md). It complements
[9649](../global-rank-two/PROOF.md), which excludes real rank one
globally and proves unique jointly simple scalar recovery. It is
stronger than9550's simultaneous \(B=s=0\) obstruction. The new
ordinary proof inherits no verdict: [REVIEW9598](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/pencil-audit/REVIEW.md)
confirms9550 only. The new exclusion makes \(q=B/s,x=s^2>0\) a legal
chart for **every** actual real stationary profile; the former
rank-one formula for \(E\) remains illegal for rank-two work.

## 2. Complete branch factorization

In this section set \(s=0\). Entire coefficient comparison gives

\[
\begin{aligned}
H&=2112E+10976r^2+7344r+1143,\\
K&=14400E+65856r^2+38160r+4725,\\
W&=5488r^2+7280r+1875,\\
D&=262144E^2r+102400E^2+786432Er^3+663552Er^2\\
 &\quad+153600Er+5760E+36864r^4+18432r^3-1152r^2-864r+81.
\end{aligned}
\]

Here \(K\) is a scalar auxiliary polynomial, distinct from the full
kernel polynomial used in9550. The source checks the whole identities

\[
\begin{aligned}
C_0-14C_4&=-192,\\
18816R_3&=t(BtK-112H),\\
\det M_{\{0,2,3\}}&=\frac5{774144}(7r+3)HD,\\
2112K-14400H&=-3456W.                              \tag{1}
\end{aligned}
\]

The first identity excludes \(t=0\) without any rank premise. If
\(B=0\), the inherited9550 algebraic obstruction excludes a nonzero
\(t\): its \(H=0\) substitution produces the entire cubic and
degree-six polynomial recorded there, with a multiplied rational
Bezout unit. The pivot is \(-88t/7\), nonzero for any complex
\(t\ne0\); the unit argument is over characteristic zero and needs
no reality or positivity. The checker regenerates this entire input
certificate and byte-pins both input files.

Hence suppose \(B\ne0,t\ne0\). The common scalar vector
\((t^2,t,1)\) is nonzero, so the displayed minor must vanish.
The three exhaustive branches are \(H=0\), \(r=-3/7\), and \(D=0\).
We analyze \(H=0\) first. Both other branches are then taken under
\(H\ne0\). No factor is silently discarded.

## 3. The exceptional \(H=0\) branch

Equation(1) and \(Bt\ne0\) force \(K=0\), hence \(W=0\).
The nonzero constant \(2112\) permits

\[
E=-\frac{10976r^2+7344r+1143}{2112}.                 \tag{2}
\]

The **whole** minor \(\det M_{\{0,2,4\}}\) has a factor \(B\).
Divide it only on this proved \(B\ne0\) branch, substitute(2), and
divide as a polynomial in \(r\) by \(W\), whose leading coefficient
is the nonzero rational \(5488\). The entire remainder is a nonzero
rational multiple of

\[
L(r)=6641762363050556r+2323226157581397.
\]

The checker multiplies the **complete quotient/remainder identity**;
all \(B\)-dependent coefficients cancel from the remainder. Thus a
candidate requires \(W=L=0\). The complete three-by-three integer
Sylvester matrix has determinant

    8017052714249480766100811232.

This is nonzero. At a common complex root its nonzero evaluation
column would be killed by the matrix, a contradiction. No division
by \(L\)'s coefficient or a generic parameter is needed.

## 4. Complete scalar clearing with no affine pivot assumption

Assume \(H\ne0\). Equation(1) implies \(K\ne0\), then

\[
w=Bt=\frac{112H}{K},\qquad v=B^2\ne0.               \tag{3}
\]

For \(i=0,1,2,4\), put \(d_1=1\) and \(d_0=d_2=d_4=2\).
For each monomial \(B^b t^j\) of \(R_i\), form
\(B^{b+d_i-j}w^j\), then replace each even power of \(B\) by its
power of \(v\). This transforms the whole \(B^{d_i}R_i\).
All resulting exponents are nonnegative and even as required.
Denote the entire resulting polynomial by

\[
Y_i(v,w,E,r)=y_{i2}w^2+y_{i1}w+y_{i0}.
\]

Every \(y_{ij}\) is affine in \(v\). Clear(3) by multiplication:

\[
\widetilde W_i=y_{i2}(112H)^2+y_{i1}(112H)K+y_{i0}K^2.
\]

The complete syzygy is

\[
K^2Y_i-\widetilde W_i
=(Kw-112H)\{y_{i2}(Kw+112H)+Ky_{i1}\}.              \tag{4}
\]

Each candidate requires \(\widetilde W_i=0\). Let \(W_i\) be its
primitive integer polynomial, normalized by positive lexicographic
leading coefficient in the source's full exponent order. This changes
only a nonzero rational scalar. Write \(W_i=a_iv+b_i\). Form

\[
X_i=a_0b_i-a_ib_0,\qquad i=1,4.
\]

These vanish whenever \(W_0=W_i=0\), **including every zero of either
affine slope**. The source checks both complete affine syzygies.
Entire polynomial division by the constant-leading \(H\) gives

\[
H\mid X_1,\qquad H^2\mid X_4.
\]

Define \(A_5\) and \(A_4\) to be the primitive integer polynomials
of \(X_1/H\) and \(X_4/H^2\), respectively. These definitions are
unambiguous exact polynomial circuits in the full input matrix;
[verify.py](verify.py) and [expected.json](expected.json) include
**every coefficient**, not a selected prefix. Their degrees in
\((E,r)\) are respectively \((5,10)\) and \((4,9)\).
On \(H\ne0\), every common scalar solution requires

\[
A_5(E,r)=A_4(E,r)=0.                                \tag{5}
\]

No affine slope, discriminant, formal leading coefficient, or
three-by-three minor has been assumed nonzero.

## 5. The \(r=-3/7\) branch

Specialize(5) at \(r=-3/7\). Normalize the two entire univariate
integer polynomials in \(E\) as in the source. Their degrees are
five and four. The whole nine-by-nine fixed integer Sylvester
matrix has determinant

    -137825829889536420678225145523709979998746476644110625149692931952561628903816841884759350570150428978071186892685780297329934336000.

Every entry and the full determinant are in the fixture and are
regenerated. Fraction-free and rational Gaussian arithmetic agree.
The nonzero determinant rules out a common complex \(E\).
This branch is impossible; the \(H=0\) part was already treated.

## 6. The remaining \(D=0\) branch

By(5), a remaining solution has \(D=A_5=A_4=0\). Form fixed
integer Sylvester matrices in \(E\), of sizes seven and six for
\((D,A_5)\) and \((D,A_4)\). The formal \(E\) degrees are
\((2,5)\) and \((2,4)\). They remain these sizes at **all** \(r\),
including a zero of a leading coefficient or an identically zero
specialized polynomial. A common finite \(E\) still gives a nonzero
evaluation column in the matrix kernel, so both determinants vanish.

Let their entire determinant polynomials in \(r\) be \(S_5,S_4\).
The row-wise degree bounds are

\[
\deg_r S_5\le5\cdot4+2\cdot10=40,\qquad
\deg_r S_4\le4\cdot4+2\cdot9=34.
\]

The source evaluates every **whole fixed matrix** at respectively
41 and35 distinct integers, using exact integer Bareiss and a
separate rational Gaussian algorithm. Exact rational interpolation
regenerates the entire coefficient arrays. The degree bounds prove
the identities at every complex \(r\); these are identity checks,
**not a root grid or a numerical absence argument**. Integer
coefficients and every Bareiss division are checked exactly.
Whole polynomial division then establishes

\[
\begin{aligned}
S_5&=5440166188265831286177792(8r+3)^3F_{22}(r),\\
S_4&=95627921278110315577344(8r+3)^3G_{19}(r).         \tag{6}
\end{aligned}
\]

The subscripts are their exact degrees; each is primitive integer.
All23 and20 coefficients are regenerated, stored and multiplied
back in full. No factor of either quotient is discarded.

Their reductions over \(\mathbb F_{257}\) have leading coefficients
77 and25, so both degrees are retained. Exact Euclid regenerates
the complete coefficients of \(u,v\) and verifies the **whole**
identity

\[
u\overline F_{22}+v\overline G_{19}=1.
\]

The integer Gauss bridge is essential. If \(F_{22},G_{19}\) had a
common complex root, their rational gcd would have a nonconstant
primitive integer factor. Its leading coefficient divides the
leading coefficient of \(F_{22}\), which is nonzero modulo257.
Its reduction would therefore remain nonconstant and divide both
reductions, contradicting the unit. This is a **univariate**
characteristic-zero argument, not a modular multivariate ideal test.

Consequently(6) can vanish simultaneously only at \(r=-3/8\).
Here the complete identity is \(D=4096E^2\), forcing \(E=0\).
The scalar pivots are then \(H=-135/2,K=-324\); (3) gives
\(Bt=70/3\). The whole transformed first residual satisfies

\[
Y_0(v,70/3,0,-3/8)=14v.
\]

But \(Y_0=B^2R_0\) on this substitution and \(v=B^2\ne0\).
Hence \(R_0=14\), contradicting the required zero. This exhausts
the last branch, and proves the theorem.

## 7. Reproduction and trust boundary

Run the standard-library checker from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-2/nonzero-quartic-mass/verify.py
```

It regenerates the entire byte-pinned9550 fixture before producing
24 complete new coefficient identities, both exceptional nonzero
integer matrices, both whole determinant identities, and the full
univariate modular unit. Six bridge controls retain zero affine
slopes and formal degree loss. Five deliberate mathematical
damages are rejected. Every41+35 determinant evaluation agrees
under both arithmetic algorithms; this is same-author corroboration,
not independent review. Normal and optimized execution must agree
with **all fields and types** of the compact expected record.

Use `--export /tmp/quartic-slice-polynomials.json` to regenerate
every matrix/residual/transformed/elimination coefficient for
further exact work. No discovery CAS, ledger, private scratch file,
root solver, floating arithmetic, timing result or incomplete search
is a reproduction premise. Python3.11+ suffices. The ordinary
input theorem, legal algebraic substitutions, fixed evaluation-column
necessity, degree theorem for interpolation, integer Gauss and
original-root interpretation remain unformalized.

The strongest complex first-power inequality remains the conjectural
endpoint in [Zhang's primary manuscript, Conjecture1.2](https://arxiv.org/html/2609.19126).
Its quadratic theorem and ordinary Sendov are distinct. This is a
useful angular stationary reduction within that family, with no
claimed global endpoint, historical priority, or new sharp constant.
