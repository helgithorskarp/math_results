# Degree-nine complex first-power inequality on the marked three-fifths disk

Actual author **six-sendov-1**, role **researcher**, 2026-10-03.
Complete ordinary analytic author proof with finite exact rational inequalities;
**unformalized and independently unreviewed**. The unrestricted first-power
conjecture and the optimal marked radius are not settled.

## 1. Statements and dependencies

For a complex eight-tuple $q$, write

\[
r_j=|q_j|,\quad F=\sum_{j=1}^8r_j,\quad
\mu=\tfrac18\sum q_j,\quad E=\sum|q_j-1|^2,
\]
\[
O_a(q)=9\int_0^1\prod_{j=1}^8(1-atq_j)\,dt,\qquad
J_a(q)=\int_0^1\prod_{j=1}^8[a+(1-a^2)tq_j]\,dt.
\]

**Channel lemma.** For every $a\in[11/20,3/5]$, every finite nonzero
complex eight-tuple satisfying

\[
r_j\ge5/8\quad(j=1,\ldots,8),\qquad F\le8,\qquad |J_a(q)|\ge1
\tag{1}
\]

obeys

\[
F>186/25,\quad E<17/4,\quad |\mu|\le1,\quad
\Re\mu>1063/1600,\quad |O_a(q)|>257/256.         \tag{2}
\]

No individual critical-disk condition, conjugacy, balance, equal radius,
separation or second-moment hypothesis is imposed. Repeated entries are allowed.

**Reusable origin lemma.** For every finite complex eight-tuple, including
zero entries, with $F\le8$, $E\le17/4$, and $\Re\mu\ge1063/1600$,

\[
|O_a(q)|>257/256\quad\text{for every }a\in[11/20,3/5].       \tag{3}
\]

There is no radius-floor or polar-channel premise in this origin lemma.

**Actual-polynomial corollary.** Every degree-nine complex polynomial
with all nine original zeros in the closed unit disk satisfies

\[
\sum_{j=1}^8|a-\zeta_j|^{-1}>8
\quad\text{at every marked zero }|a|\le3/5,                 \tag{4}
\]

counting all critical multiplicities and interpreting a zero denominator as
$+\infty$. The lower marked region $|a|\le11/20$ uses the author's
[previous complete proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/eleven-twentieths-first-power/PROOF.md),
source **5753b0379d8ed14bb1c64ce6044a709b3cd0fe51**, committed LEMMA10101/0.
That dependency applies only to the lower region. Sections2–7 prove the new
standalone interval and origin lemmas without importing the parent's finite
case data or constants. See [LITERATURE.md](LITERATURE.md) for primary credit.

## 2. The affine envelope and a first-power mass floor

Put

\[
h=3/5,\quad c=13/20,\quad b_-=16/25,\quad b_+=279/400,
\quad m=93/100,\quad A_*=3069/8000.
\]

For $a\in[11/20,h]$ and $x\in[0,1]$,

\[
a+(1-a^2)x\le h+cx,                                      \tag{5}
\]

because the difference equals $(1-x)(h-a)+x(a-1/2)^2\ge0$.
Triangle inequality and AM–GM give

\[
|J_a(q)|\le\int_0^1[a+(1-a^2)tF/8]^8dt.
\]

If $F\le186/25$, use (5) with $x=tF/8\le m$ to obtain

\[
|J_a(q)|\le\int_0^1[h+cmt]^8dt
=\frac{250634863328462439487299369}
       {256000000000000000000000000}<1.                    \tag{6}
\]

All nine binomial coefficients are included in the exact integral. This
contradicts (1), so $F>186/25$.

## 3. A sharp radial product from a quadratic Hermite majorant

This section proves an elementary fixed-moment product bound. Its mechanism
is classical quadratic Hermite interpolation; no historical priority is
claimed for the general inequality.

Let eight real numbers $e_j$ satisfy $\sum e_j\le0$, and put
$T=\sum e_j^2$, $d=\sqrt{T/56}$. For $B>0$, $y\ge0$, assume
$B+ye_j>0$ for all $j$ and $B-yd>0$. Then

\[
\prod_{j=1}^8(B+ye_j)\le(B+7yd)(B-yd)^7.                  \tag{7}
\]

First, each positive $e_j$ is at most $\sqrt{7T/8}=7d$:
the other seven sum to at most $-e_j$, so Cauchy–Schwarz gives
$T\ge e_j^2+e_j^2/7$. Nonpositive entries are also at most $7d$.
If $T=0$ or $y=0$, (7) is immediate. Otherwise define
$f(x)=\log(B+yx)$ on its positive-factor interval, $v=-d$, $u=7d$, and

\[
Q(x)=f(v)+f'(v)(x-v)+\kappa(x-v)^2,
\quad
\kappa=\frac{f(u)-f(v)-8df'(v)}{64d^2}.                  \tag{8}
\]

Concavity gives $\kappa\le0$. Also
$f'''(x)=2y^3/(B+yx)^3\ge0$. The Hermite remainder is

\[
f(x)-Q(x)=\frac{f'''(\xi)}6(x+d)^2(x-7d)\le0
\quad\text{for every }x\le7d\text{ in the domain}.        \tag{9}
\]

For completeness, at the two interpolation nodes this is equality.
Otherwise subtract $\lambda(x+d)^2(x-7d)$ from $f-Q$, choosing
$\lambda$ to make an additional zero at the desired $x$. The zeros
at $x,-d,7d$ and the derivative zero at $-d$ give, by three applications
of Rolle's theorem, $6\lambda=f'''(\xi)$. The entire interval containing
these points lies in the positive-factor domain. This proves (9).

The coefficient of $x$ in $Q$ is
$\alpha=f'(v)+2\kappa d$. Since $f(u)-f(v)\ge0$,
$\kappa\ge-f'(v)/(8d)$, hence $\alpha\ge3f'(v)/4\ge0$.
Therefore

\[
\sum_j f(e_j)\le\sum_j Q(e_j)
=8Q(0)+\alpha\sum_j e_j+\kappa T
\le8Q(0)+\kappa T=f(7d)+7f(-d).                        \tag{10}
\]

The last equality follows by evaluating the quadratic on one $7d$ and
seven $-d$, whose sum is zero and squared sum is $56d^2=T$.
Exponentiating proves (7). The bound is sharp on that real moment
configuration; no assertion is made that it reconstructs a polynomial
whose original zeros all lie in the unit disk.

## 4. Radial and phase bounds under the tuple hypotheses

In (1), put $e_j=r_j-1$, $T=\sum e_j^2$,
$\Pi=\sum(r_j-\Re q_j)$. Then

\[
\sum e_j=F-8\le0,\quad\Pi\ge0,\quad E=T+2\Pi,
\quad0\le T\le T_*:=63/8.                              \tag{11}
\]

To prove the last bound, write $r_j=5/8+x_j$, $x_j\ge0$, and
$X=\sum x_j\le3$. With $s_0=3/8$,

\[
T=8s_0^2-2s_0X+\sum x_j^2
\le8s_0^2-2s_0X+X^2\le56s_0^2=63/8.
\]

The last quadratic is convex on $[0,8s_0]$ and its endpoint maximum is
$56s_0^2$. Thus $d=\sqrt{T/56}\le3/8$ and $e_j\le7d$.
For $b=1-a^2$, $B=a+bt$ and $y=bt$, all radial factors are positive,
and $B-yd=a+bt(1-d)>0$. Consequently (7) applies.

For a nonnegative upper bound $D$ on all $e_j$, set $C_D=B+btD$.
The exact phase identity is

\[
|a+btq_j|^2=(a+btr_j)^2-2abt(r_j-\Re q_j).
\]

If a complex factor is zero, the desired upper bound below holds
immediately. Otherwise $\tfrac12\log(1-x)\le-x/2$ and
$a+btr_j\le C_D$ give

\[
\prod_j|a+btq_j|
\le (B+7btd)(B-btd)^7
       \exp[-abt\Pi/C_D^2].                            \tag{12}
\]

This also holds at $t=0$ by direct evaluation. Here we have separated the
sharp radial moment payment from the phase loss without discarding either.

## 5. Sixty-three closed cells force E<17/4

Suppose $E\ge17/4$. For $k=0,\ldots,62$, use

\[
L=k/8,\ U=(k+1)/8,\ T\in[L,U],\quad
P=\max(0,(17/4-U)/2),
\]
\[
\delta=\frac{\lfloor1024\sqrt{L/56}\rfloor}{1024},\qquad
D=\frac{\lceil256\sqrt{7U/8}\rceil}{256}.                 \tag{13}
\]

All cells are closed, consecutive and cover $[0,63/8]$, with shared
endpoints retained. Equations(11)–(13) give $\Pi\ge P$, $d\ge\delta$,
and $e_j\le D$. Uniformly on the full marked interval,

\[
B\le\widehat B=h+ct,\qquad
C_D\le\widehat C=h+b_+(1+D)t,\qquad
b\ge b_-,\quad ab\ge A_* .                             \tag{14}
\]

The last bound uses the concavity of $a(1-a^2)$ on the positive marked
interval and its two endpoint values: $3069/8000$ and $3072/8000$.

For $0\le x<1$, let $\phi(x)=(1+7x)(1-x)^7$. Its logarithmic
derivative is $-56x/[(1+7x)(1-x)]\le0$. In the radial product of (12),
$x=btd/B\le d\le3/8$ and
$x\ge b_-t\delta/\widehat B$. Both lower radial factors below are
positive, since $c-b_-\delta\ge13/20-(16/25)(3/8)=41/100>0$.
Therefore

\[
(B+7btd)(B-btd)^7=B^8\phi(btd/B)
\le\widehat B^8\phi(b_-t\delta/\widehat B)
=:R_L(t)
\]
\[
R_L(t)=(h+(c+7b_-\delta)t)(h+(c-b_-\delta)t)^7.           \tag{15}
\]

Put $M=\widehat C(1)$ and $\nu=b_+(1+D)/M\in[0,1)$. The positive
geometric series about $t=1$ gives

\[
G(t)=M^{-2}\sum_{n=0}^4(n+1)\nu^n(1-t)^n
\le\widehat C(t)^{-2}.                                  \tag{16}
\]

Define $K(t)=A_*PtG(t)\ge0$. The phase loss in (12) is at least $K$.
For all $x\ge0$, $e^{-x}\le1-x+x^2/2$ and the right side is positive.
Multiplying the nonnegative radial majorant yields

\[
|J_a(q)|\le\int_0^1R_L(t)[1-K(t)+K(t)^2/2]dt.             \tag{17}
\]

**Every one of these63 exact rational integrals is less than9999/10000.**
The largest occurs at $[L,U]=[3/2,13/8]$, where
$\delta=167/1024$, $D=153/128$, $P=21/16$, and equals

\[
\frac{56880153019542975632642352775658724623854290165303128556042063257110265739149114679}
{56886116417383244430268545717865500491891813800318452473773183467520000000000000000}
<9999/10000.                                           \tag{18}
\]

These are complete polynomials represented through degree18 with all19
coefficients, including zero terminal coefficients when $P=0$.
[verify.py](verify.py) compares the whole coefficient vectors by
convolution versus direct binomial/kernel-basis expansion, retaining
all ordered pairs in $K^2/2$. It separately integrates coefficientwise
and with exact beta integrals. All lower and upper root roundings are
checked by integer square comparisons. There is no sample or imported
numeric certificate. Thus (1) contradicts $E\ge17/4$, proving $E<17/4$.

Since $E=T+2F-16\Re\mu$ and $T\ge0$, (6) gives

\[
|\mu|\le F/8\le1,\qquad
\Re\mu\ge F/8-E/16>93/100-17/64=1063/1600.               \tag{19}
\]

## 6. All centered origin orders with finite-cardinality bounds

We prove the reusable origin lemma(3). Put $\mu=u+iv$, $w=v^2$,
$s=|\mu|^2=u^2+w$, $z_j=q_j-\mu$, and

\[
S:=\sum|z_j|^2=E-8|\mu-1|^2
\le17/4-8[(1-u)^2+w].                                  \tag{20}
\]

The hypotheses imply $u\in[1063/1600,1]$, $w\in[0,17/32]$,
$s\le1$, $S\ge0$, and $\sum z_j=0$.
Each coordinate satisfies $|z_j|^2\le7S/8$, by writing
$z_j=-\sum_{k\ne j}z_k$ and applying Cauchy–Schwarz. For $k\ge2$,

\[
|p_k(z)|\le\sum|z_j|^k
\le(7/8)^{(k-2)/2}S^{k/2}.                              \tag{21}
\]

Let $\rho=479/512\ge\sqrt{7/8}$. An exact rational upper coefficient
for (21) is

\[
\eta_k=(7/8)^{\lfloor(k-2)/2\rfloor}
              \rho^{\,k\bmod2}.                        \tag{22}
\]

There is also the classical finite-cardinality Cauchy–Schwarz/Maclaurin
bound

\[
|e_l(z)|\le\binom8l(S/8)^{l/2}.                         \tag{23}
\]

Indeed, triangle inequality followed by Cauchy–Schwarz over the
$\binom8l$ subsets gives
$|e_l(z)|^2\le\binom8l e_l(|z_1|^2,\ldots,|z_8|^2)$.
For nonnegative entries with sum $S$, the latter elementary symmetric
sum is at most $\binom8l(S/8)^l$. One direct proof maximizes it on the
compact simplex. For $S>0$, the maximum is positive, so it has at least
$l$ positive entries. Averaging any unequal pair increases that symmetric
sum by $(x-y)^2 e_{l-2}(\text{other entries})/4>0$; the residual factor is
positive because there are at least $l-2$ positive entries left. Hence a
maximizer has all entries equal. The cases $S=0$ and $l=1$ are immediate.
No novelty is claimed for these classical inequalities.

Newton's identities, with $p_1(z)=0$, let us choose recursively

\[
c_0=1,\quad c_1=0,\quad
c_l=\min\left\{\frac1l\sum_{k=2}^l c_{l-k}\eta_k,
               \binom8l 8^{-\lfloor l/2\rfloor}
                    \tau^{\,l\bmod2}\right\},           \tag{24}
\]

where $\tau=363/1024\ge\sqrt{1/8}$. By induction,
$|e_l(z)|\le c_l S^{l/2}$, and the exact constants are

\[
(c_2,\ldots,c_8)=(1/2,479/1536,11/32,2541/8192,
                     7/128,363/65536,1/4096).             \tag{25}
\]

All seven recursive minima and both square-root caps are checked exactly.
The full centered expansion is

\[
\prod_j(1-atq_j)=\sum_{l=0}^8 e_l(z)(-at)^l(1-at\mu)^{8-l}.
\tag{26}
\]

The first centered term vanishes; every order2 through8 is retained.

For a closed box $a\in[A,B]$, $u\in[U,V]$, $w\in[W,X]$, set

\[
s_+=\min(1,V^2+X),\quad S_+=17/4-8[(1-V)^2+W],
\quad\beta(t)=1-2AUt+A^2s_+t^2.                         \tag{27}
\]

At every feasible point, $s\le s_+$, $S\le S_+$ and
$|1-at\mu|^2\le\beta(t)$. To obtain the last inequality, decrease
$a$ to $A$: the derivative of $1-2atu+a^2t^2s$ is
$2t(-u+ats)\le0$, because $u\ge1063/1600>h\ge a$ and $s\le1$.
Then decrease $u$ to $U$ and increase $s$ to $s_+$.
On all boxes used below, $s_+\ge U^2$, $U>A s_+$, so
$\beta(t)\ge(1-AUt)^2>0$, $\beta$ is decreasing on $[0,1]$, and
$0<\beta(1)<1$. For odd powers use

\[
\sqrt{\beta(t)}\le Q(t):=1-AUt+
              \frac{A^2(s_+-U^2)}{2(1-AU)}t^2.            \tag{28}
\]

This follows from $\sqrt{x^2+d}\le x+d/(2x)$ for $x>0$, $d\ge0$,
with $x=1-AUt\ge1-AU>0$.
Let $H_l=\beta^{(8-l)/2}$ for even $l$, and
$H_l=\beta^{(7-l)/2}Q$ for odd $l$. Let $d_s,d_\beta,d_S$ be upper
rational square-root ceilings of $s_+,\beta(1),S_+$, respectively,
with denominator1024. The complete remainder in (26) has upper bound

\[
R=9\sum_{l=2}^8 B^l c_l S_+^{\lfloor l/2\rfloor}
             d_S^{\,l\bmod2}\int_0^1t^l H_l(t)dt.        \tag{29}
\]

Direct integration of the diagonal term, with $\mu\ne0$, gives

\[
O_a(\mu,\ldots,\mu)=\frac{1-(1-a\mu)^9}{a\mu},
\qquad |O_a(\mu,\ldots,\mu)|\ge
D:=\frac{1-d_\beta\beta(1)^4}{B d_s}.                    \tag{30}
\]

The numerator is positive on every box below. We used
$|1-a\mu|^9\le d_\beta\beta(1)^4$ and $|a\mu|\le B d_s$.
Triangle inequality in (26) now yields $|O_a(q)|\ge D-R$.

## 7. The complete closed origin cover

The root box is

\[
[11/20,3/5]\times[1063/1600,1]\times[0,17/32].             \tag{31}
\]

[COVER.json](COVER.json) gives271 internal nodes and272 leaves of one
complete binary tree. Axis0 is $a$, axis1 is $u$, axis2 is $w$.
Every internal node bisects that axis at its exact rational midpoint.
Path0 denotes the lower closed child and path1 the upper closed child.
Both children, shared endpoints and all leaves are retained; there are
no discarded or declared-empty boxes. The checker reconstructs every
box, checks all path/axis types, containment, both-child completeness
and the entire543-node census. It verifies (27)–(30) on each leaf,
including all positivity and root-rounding conditions.

For every one of the272 leaves,

\[
D-R>257/256.                                           \tag{32}
\]

The smallest exact bound, on leaf0101101000, is

\[
\frac{4551321089049644152139495331958504244464559677691254265373631933}
{4533294942532471298329887731669010481152000000000000000000000000}
>257/256.                                             \tag{33}
\]

Every one of the seven remainder polynomials is checked in full by
convolution versus multinomial counting, and integrated separately by
multinomial term choices. Neither highest-degree coefficients nor
orders7/8 are discarded. Thus (32) holds on the whole closed root box,
proving (3). Combining (6), (18), (19), and (3) proves (2).

## 8. The actual original-root conclusion

For $|a|\le11/20$, invoke the explicitly credited parent10101.
For $11/20<|a|\le3/5$, a marked multiple zero gives an infinite term.
Otherwise rotate to real $a\in(11/20,3/5]$, normalize the polynomial to
monic, and write

\[
p(z)=(z-a)\prod_{j=1}^8(z-z_j),\qquad
p'(z)=9\prod_{j=1}^8(z-\zeta_j),\qquad q_j=(a-\zeta_j)^{-1}.
\]

All $q_j$ are finite and nonzero, with all eight critical multiplicities.
Integrate $p'$ from $a$ to0 and from $a$ to $1/a$. The classical
communication identities are

\[
O_a(q)=\prod_j z_jq_j,\qquad
J_a(q)=\prod_j\frac{1-az_j}{a-z_j}.                     \tag{34}
\]

For the first, divide the integral by $-a p'(a)$ and use
$p(0)=-a\prod z_j$, $p'(a)=9\prod1/q_j$.
For the second, divide by $(1/a-a)p'(a)$; each normalized derivative
factor is $1+(1/a-a)tq_j=[a+(1-a^2)tq_j]/a$, and evaluating
$p(1/a)$ gives the displayed product. Simplicity of the marked zero
ensures each $a-z_j\ne0$. Since every original zero lies in the
closed disk,

\[
|O_a(q)|\le\prod r_j,\qquad |J_a(q)|\ge1,
\]

using $|1-az_j|^2-|a-z_j|^2=(1-a^2)(1-|z_j|^2)\ge0$.
Gauss–Lucas gives $|\zeta_j|\le1$, hence
$r_j\ge1/(1+a)\ge5/8$. If the required sum were at most8,
AM–GM would give $\prod r_j\le(F/8)^8\le1$. All hypotheses of (1)
would hold, contradicting $|O_a(q)|>257/256>1$. This proves (4),
including every original/critical multiplicity and the closed endpoints.
The tuple conditions are only necessary conditions for this application;
no equivalence to actual all-original feasibility is asserted.

## 9. Evidence and limits

The new analytic step is the sharp Hermite radial payment replacing a
coarse logarithmic radial payment. It supplies a compatible energy
threshold and combines with classical finite-cardinality centered
coefficient bounds and an entire origin cover. These sufficient estimates
extend the actual complex marked disk from11/20 to3/5. The general
Hermite/Newton/Cauchy–Schwarz/Maclaurin tools are credited as classical.
The quadratic Sendov theorem is not a mathematical premise.

The same author's earlier checker architecture was adapted. All individual
coefficient vectors, integrals, inequalities and cover entries are checked
before the compact fingerprint in [EXPECTED.json](EXPECTED.json).
A count or hash alone does not establish a mathematical case. Full
regenerated coefficient records remain private; all defining inputs and
checks are public. Trust consists of the ordinary unformalized analytic
bridges and CPython integer/Fraction semantics. Validation is same-author,
without a formal kernel or independent verdict for this new result.
No global first-power theorem, optimal radius, optimal constant or uniform
additional margin above8 is claimed. Reproduction and rejection controls
are in [README.md](README.md).
