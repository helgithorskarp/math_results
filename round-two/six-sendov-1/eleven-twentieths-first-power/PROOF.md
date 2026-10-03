# Degree-nine complex first-power inequality for marked modulus at most 11/20

Actual author **six-sendov-1**, role **researcher**, 2026-10-03.
Ordinary analytic author proof with finite exact rational inequalities;
**unformalized and independently unreviewed**. The unrestricted first-power
conjecture, optimal radius and optimal constants are not settled.

## 1. Statements and dependencies

For a finite nonzero complex eight-tuple $q$, write

\[
r_j=|q_j|,\quad F=\sum_{j=1}^8r_j,\quad
\mu=\tfrac18\sum q_j,\quad E=\sum|q_j-1|^2,
\]
\[
O_a(q)=9\int_0^1\prod_{j=1}^8(1-atq_j)\,dt,\qquad
J_a(q)=\int_0^1\prod_{j=1}^8[a+(1-a^2)tq_j]\,dt.
\]

**Channel lemma.** For every $a\in[1/2,11/20]$, the hypotheses

\[
r_j\ge20/31\quad(j=1,\ldots,8),\qquad F\le8,\qquad |J_a(q)|\ge1
\tag{1}
\]

imply

\[
F>38/5,\quad E<3,\quad |\mu|\le1,\quad
\Re\mu>61/80,\quad |O_a(q)|>257/256.             \tag{2}
\]

Only the radius floor is used; no individual critical-disk condition,
conjugacy, balance, equal radius, separation or second-moment hypothesis
is imposed. Repeated entries are allowed.

**Reusable origin lemma.** For every complex eight-tuple (zero entries
are allowed here) with $F\le8$, $E\le3$, and $\Re\mu\ge61/80$,

\[
|O_a(q)|>257/256\quad\text{for every }a\in[1/2,11/20]. \tag{3}
\]

This lemma has no radius-floor or polar-channel assumption.

**Actual-polynomial corollary.** Every degree-nine complex polynomial
with all nine original zeros in the closed unit disk satisfies

\[
\sum_{j=1}^8|a-\zeta_j|^{-1}>8
\quad\text{at every marked zero }|a|\le11/20,       \tag{4}
\]

counting all critical multiplicities and interpreting a zero denominator
as $+\infty$. The proof of (4) **uses the previously published half-disk
lemma10092** for $|a|\le1/2$, then uses the new channel lemma for the rest.
The complete [parent proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/half-disk-first-power/PROOF.md),
source **f3636003fe88e443e8cc3046bd1e4cf8c87334b2**, is a mathematical
dependency of that lower-radius part only. Sections2–6 below prove the
new standalone lemmas without importing the parent's finite cases or
constants. Classical identities, Newton's identities and the polar
mechanism retain their credit; see [LITERATURE.md](LITERATURE.md).

## 2. A safe affine envelope and the mass floor

Set $h=11/20$, $c=7/10$, and $b_*=1-h^2=279/400$.
For every $a\in[1/2,h]$ and $x\in[0,1]$,

\[
a+(1-a^2)x\le h+cx,                             \tag{5}
\]

because the difference is exactly

\[
(1-x)(h-a)+x(a-1/2)^2\ge0.
\]

This replaces the monotonicity in $a$ that holds below1/2 and fails above
it. Triangle inequality and AM–GM give

\[
|J_a(q)|\le\int_0^1[a+(1-a^2)tF/8]^8dt.          \tag{6}
\]

If $F\le38/5$, then $tF/8\le19/20$ and (5) implies

\[
|J_a(q)|\le\int_0^1[11/20+(133/200)t]^8dt
=\frac{22195148562855892471}{23040000000000000000}<1. \tag{7}
\]

The binomial integral includes every coefficient. Thus (1) forces
$F>38/5$.

## 3. Radial and phase deficits for the polar channel

Put $e_j=r_j-1$, $T=\sum e_j^2$ and
$\Pi=\sum(r_j-\Re q_j)$. Then

\[
\sum e_j=F-8\le0,\quad \Pi\ge0,\quad E=T+2\Pi. \tag{8}
\]

The radius floor gives

\[
0\le T\le T_*:=6776/961,
\qquad e_j>0\Longrightarrow e_j\le\sqrt{7T/8}.    \tag{9}
\]

Indeed, with $s=11/31$, write $r_j=20/31+x_j$, $x_j\ge0$,
$X=\sum x_j\le8s$. Then
$T=8s^2-2sX+\sum x_j^2\le8s^2-2sX+X^2\le56s^2$,
by convexity of the last quadratic and its two endpoint values. If
$e_j>0$, the other seven entries sum to at most $-e_j$, so
Cauchy–Schwarz gives $T\ge e_j^2+e_j^2/7$.

For $b=1-a^2$, $B=a+bt$, $C=B+btd$ with $d\ge0$ an upper
bound for all $e_j$, the pointwise inequality is

\[
\prod_j|a+btq_j|\le B^8\exp\left[-\frac{b^2t^2T}{2BC}
                                      -\frac{abt\Pi}{C^2}\right].\tag{10}
\]

Here is its proof, including negative radial deviations. For $x>-1$,
$x\le v$, $v\ge0$,

\[
\log(1+x)\le x-\frac{x^2}{2(1+v)}.              \tag{11}
\]

For $x\ge0$, integrating $s/(1+s)\ge s/(1+x)$ on $[0,x]$
yields $x-\log(1+x)\ge x^2/[2(1+x)]$. For $-1<x\le0$,
reversing the integral over $[x,0]$ yields
$x-\log(1+x)\ge x^2/2$. Both imply (11).
Apply (11) to $x=bte_j/B$ and $v=btd/B$. Since the linear terms
sum to a nonpositive number,

\[
\prod_j(a+btr_j)\le B^8\exp[-b^2t^2T/(2BC)].
\]

Each radial factor is positive. The phase identity, with
$\pi_j=r_j-\Re q_j\ge0$, is

\[
|a+btq_j|^2=(a+btr_j)^2-2abt\pi_j.
\]

If any complex factor is zero, (10) holds directly. Otherwise
$\tfrac12\log(1-x)\le-x/2$ gives an extra loss at least
$abt\pi_j/(a+btr_j)^2\ge abt\pi_j/C^2$. Summing proves
(10), also at $t=0$ by direct evaluation.

## 4. Fifty-seven closed cells force E<3

Suppose $E\ge3$. For each $k=0,\ldots,56$, use the closed cell

\[
L=k/8,\quad U=\min((k+1)/8,T_*),\quad T\in[L,U],
\quad P=\max(0,(3-U)/2),\quad
 d=\frac{\lceil256\sqrt{7U/8}\rceil}{256}.        \tag{12}
\]

All57 cells meet consecutively and cover $[0,T_*]$, including both
endpoints. By (8)–(9), $\Pi\ge P$ and $e_j\le d$.
Uniformly on the full marked interval,

\[
B\le\widehat B=h+ct,\quad
C\le\widehat C=h+\tfrac34(1+d)t,\quad
b\ge b_*,\quad ab\ge3/8.                       \tag{13}
\]

The first bound is (5) at $x=t$; the second uses $a\le h$ and
$b\le3/4$. The last holds because $a(1-a^2)$ is increasing on
$[1/2,h]$, where $h^2<1/3$.

Let $M_B=5/4$, $M_C=h+\tfrac34(1+d)$,
$\alpha=c/M_B=14/25$ and $\nu=\tfrac34(1+d)/M_C$.
Both $\alpha,\nu$ lie in $[0,1)$. With $z=1-t$, define

\[
G_1(t)=\frac1{M_BM_C}\sum_{n=0}^4
             \left(\sum_{j=0}^n\alpha^j\nu^{n-j}\right)z^n,
\quad
G_2(t)=\frac1{M_C^2}\sum_{n=0}^4(n+1)\nu^nz^n. \tag{14}
\]

These are lower bounds for $1/(\widehat B\widehat C)$ and
$1/\widehat C^2$, respectively: expand the convergent geometric series
about $t=1$ and retain only their nonnegative first five terms.
Consequently the logarithmic loss in (10) is at least the nonnegative
polynomial

\[
K(t)=\tfrac12b_*^2Lt^2G_1(t)+(3P/8)tG_2(t).      \tag{15}
\]

Taylor's theorem, or integrating the positive second derivative, gives
$e^{-x}\le1-x+x^2/2$ for every $x\ge0$. Also
$1-x+x^2/2>0$. Hence

\[
|J_a(q)|\le\int_0^1\widehat B(t)^8[1-K(t)+K(t)^2/2]dt.\tag{16}
\]

Every one of the57 rational integrals in (16) is **strictly less than
999/1000**. The largest is at $[L,U]=[5/4,11/8]$ and equals

\[
\frac{689466923700377868054595120861197258681151353350923295992543487917316249757338161}
{691186232274696332931365603534838787479922669444335657348632812500000000000000000}
<999/1000.                                      \tag{17}
\]

These are complete degree20 polynomials (all21 coefficients), not point
samples. [verify.py](verify.py) checks each coefficient by convolution
and by direct expansion of the nonnegative $t^r(1-t)^n$ kernel basis;
it also integrates the whole expression both coefficientwise and by
exact beta integrals. The finite inequality is reproducible without
external numerical data. Thus (1) contradicts $E\ge3$, proving $E<3$.
Since $F>38/5$ and $\Pi<3/2$,

\[
|\mu|\le F/8\le1,\quad
\Re\mu=(F-\Pi)/8>19/20-3/16=61/80.             \tag{18}
\]

## 5. Full centered origin expansion with coupled variance

We now prove the reusable lemma(3). Write $\mu=u+iv$, $w=v^2$,
$s=|\mu|^2=u^2+w$ and $z_j=q_j-\mu$. The exact variance identity is

\[
S:=\sum|z_j|^2=E-8|\mu-1|^2
\le3-8[(1-u)^2+w].                              \tag{19}
\]

It follows that

\[
u\in[61/80,1],\quad w\in[0,3/8],\quad
u^2+w\le1,\quad (1-u)^2+w\le3/8.               \tag{20}
\]

For the centered elementary symmetric functions $e_l(z)$, set
$c_0=1$, $c_1=0$ and

\[
c_l=\frac1l\sum_{k=2}^l c_{l-k}\quad(2\le l\le8).
\]

Then $|e_l(z)|\le c_l S^{l/2}$, with

\[
(c_2,\ldots,c_8)=(1/2,1/3,3/8,11/30,53/144,103/280,2119/5760).
\tag{21}
\]

To see this, $p_1(z)=0$, and for $k\ge2$,
$|p_k(z)|\le\sum|z_j|^k\le S^{k/2}$. The last inequality follows
by normalizing by $\sqrt S$ so every $|z_j|/\sqrt S\le1$ and their
squares sum to1; $S=0$ is immediate. Newton's identities
$l e_l=\sum_{k=1}^l(-1)^{k-1}e_{l-k}p_k$ give (21) by induction.
The full expansion is

\[
\prod_j(1-atq_j)=\sum_{l=0}^8e_l(z)(-at)^l(1-at\mu)^{8-l}.
\tag{22}
\]

The $l=1$ term vanishes. **Every term from2 through8 is retained**.

Consider a closed box $a\in[A,B]$, $u\in[U,V]$,
$w\in[W,X]$ within the root rectangle in (20). Put

\[
s_+=\min(1,V^2+X),\quad S_+=3-8[(1-V)^2+W],
\quad\beta(t)=1-2AUt+A^2s_+t^2.                \tag{23}
\]

For a feasible point, $s\le s_+$, $0\le S\le S_+$ and
$|1-at\mu|^2\le\beta(t)$. Indeed the quadratic in $a$ is
nonincreasing for $a\le h$, since $u\ge61/80>h$ and $s\le1$;
then decrease $u$ to $U$ and increase $s$ to $s_+$.
Here $s_+\ge U^2$ and
$\beta(t)\ge(1-AUt)^2>0$. Moreover $U>A s_+$, so $\beta$
is decreasing on $[0,1]$ and $0<\beta(1)<1$.

For odd powers use the sharper positive root upper bound

\[
\sqrt{\beta(t)}\le Q(t):=1-AUt+
               \frac{A^2(s_+-U^2)}{2(1-AU)}t^2. \tag{24}
\]

This follows from $\sqrt{x^2+d}\le x+d/(2x)$ for $x>0$, $d\ge0$,
with $x=1-AUt\ge1-AU>0$. Define

\[
H_l(t)=\begin{cases}
\beta(t)^{(8-l)/2},&l\text{ even},\\
\beta(t)^{(7-l)/2}Q(t),&l\text{ odd}.
\end{cases}
\tag{25}
\]

Let $d_s,d_\beta,d_S$ be upper rational ceilings of
$\sqrt{s_+},\sqrt{\beta(1)},\sqrt{S_+}$, respectively, each with
fixed denominator1024. The complete origin remainder is bounded by

\[
R=9\sum_{l=2}^8 B^lc_lS_+^{\lfloor l/2\rfloor}
                 d_S^{,l\bmod2}\int_0^1t^lH_l(t)dt.        \tag{26}
\]

For the diagonal term, $\mu\ne0$ and direct integration gives

\[
O_a(\mu,\ldots,\mu)=\frac{1-(1-a\mu)^9}{a\mu},
\qquad |O_a(\mu,\ldots,\mu)|\ge
D:=\frac{1-d_\beta\beta(1)^4}{B d_s}.           \tag{27}
\]

The numerator uses $|1-a\mu|^9\le d_\beta\beta(1)^4$; the
denominator uses $|a\mu|\le B d_s$. On every leaf below the
numerator is positive. Triangle inequality in (22) yields
$|O_a(q)|\ge D-R$.

## 6. A complete finite origin cover

The root is the closed box

\[
[1/2,11/20]\times[61/80,1]\times[0,3/8].         \tag{28}
\]

[COVER.json](COVER.json) specifies an entire binary cover:47 interior
nodes, each with an axis0(a),1(u),2(w) and two children obtained by exact
midpoint bisection of that axis. Paths use0 for the lower half and1 for
the upper half. Every internal node has both closed children, every leaf
is tested, and no boundary is discarded. Its48 leaves all have $S_+\ge0$;
none is declared empty. The verifier reconstructs boxes from the root,
checks the full path/axis/leaf census and exact endpoint containment,
then checks (23)–(27) on **every leaf**.

For all48 leaves the exact inequality is

\[
D-R>257/256.                                   \tag{29}
\]

The smallest bound is

\[
\frac{963860760474198632630122956662777365773581489}
{959262669724917061382465126400000000000000000}>257/256.       \tag{30}
\]

All seven integrated remainder polynomials are checked in full by
convolution versus multinomial expansion, including their highest-degree
coefficients and their rational integrals. All ceilings are constructed
and verified with integer square tests. This proves (3) on the whole
closed domain, without any search-completeness or floating-point premise.
Equations(7), (17), (18), and (3) prove the channel lemma.

## 7. The actual original-root corollary

For $|a|\le1/2$, invoke the explicitly credited parent theorem. For
$1/2<|a|\le11/20$, a marked multiple zero gives an infinite reciprocal.
Otherwise rotate so $a\in(1/2,11/20]$ is real, normalize to monic, and
write

\[
p(z)=(z-a)\prod_{j=1}^8(z-z_j),\quad
p'(z)=9\prod_{j=1}^8(z-\zeta_j),\quad q_j=(a-\zeta_j)^{-1}.
\]

The simple marked zero makes all $q_j$ finite and nonzero. Integrating
$p'$ from $a$ to0 and from $a$ to $1/a$ gives the classical identities

\[
O_a(q)=\prod_j z_jq_j,\qquad
J_a(q)=\prod_j\frac{1-az_j}{a-z_j}.              \tag{31}
\]

For the first, divide the integral by $-a p'(a)$ and use
$p(0)=-a\prod z_j$, $p'(a)=9\prod1/q_j$.
For the second, divide by $(1/a-a)p'(a)$; each normalized derivative
factor is $1+(1/a-a)tq_j=[a+(1-a^2)tq_j]/a$, and evaluating
$p(1/a)$ supplies the stated product. The original disk inequalities give

\[
|O_a(q)|\le\prod r_j,\quad |J_a(q)|\ge1,
\]

since $|1-az_j|^2-|a-z_j|^2=(1-a^2)(1-|z_j|^2)\ge0$.
Gauss–Lucas gives $|\zeta_j|\le1$, so
$r_j\ge1/(1+a)\ge20/31$.
If the desired sum were at most8, AM–GM would give
$\prod r_j\le(F/8)^8\le1$. All hypotheses of (1) hold, contradicting
$|O_a(q)|>257/256>1$. This proves (4), with all multiplicities and
closed endpoints included.

## 8. Scope, verification and limitations

The elementary logarithmic and centered arguments adapt the author's
parent method; this is **same-author validation**, not independent
reproduction. The new ingredients are the safe affine envelope above1/2,
positive reciprocal-series payments and a coupled mean/variance origin
cover using (24). The published quadratic inequality does not imply the
first-power assertion and is not a premise here.

The public checker regenerates all57+48 exact cases from their defining
inputs, compares full coefficient vectors under two algebraic derivations,
and checks every individual strict inequality. EXPECTED.json is only a
compact fingerprint and extrema record; its hash is **not** used as a
substitute for the whole-case checks. Verbose regenerated coefficient
corpora remain private and are unnecessary for replay. The proof trusts
ordinary analysis and CPython integer/Fraction semantics; it has no formal
kernel or independent referee certificate. No sampled profile, radius
optimization, global extra F-margin or unrestricted first-power theorem is
claimed. All reproduction instructions and guarded rejection controls are
in [README.md](README.md).
