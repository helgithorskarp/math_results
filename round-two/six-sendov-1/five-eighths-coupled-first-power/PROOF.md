# Complex degree-nine first-power inequality on the marked five-eighths disk

Actual author **six-sendov-1**, role **researcher**, 2026-10-03.
Complete ordinary analytic author proof with finite exact rational sufficient
inequalities; **unformalized and independently unreviewed**. The unrestricted
first-power conjecture and optimal marked radius remain open in this work.

## 1. Statements and precise dependence

For a finite complex eight-tuple write

\[
r_j=|q_j|,\quad F=\sum r_j,\quad \mu=\tfrac18\sum q_j=u+iv,
\quad w=v^2,\quad E=\sum|q_j-1|^2,
\]
\[
T=\sum(r_j-1)^2,\quad \Pi=\sum(r_j-\Re q_j)=F-8u,
\quad S=\sum|q_j-\mu|^2.
\]
The two communication channels are

\[
O_a(q)=9\int_0^1\prod(1-atq_j)\,dt,\qquad
J_a(q)=\int_0^1\prod[a+(1-a^2)tq_j]\,dt.
\]

**Channel lemma.** For every real $a\in[3/5,5/8]$, every such tuple with
$r_j\ge1/(1+a)$, $F\le8$ and $|J_a(q)|\ge1$ obeys

\[
F>184/25,\quad E<23/5,\quad |\mu|\le1,\quad
u>253/400,\quad |O_a(q)|>2049/2048.                 \tag{1}
\]

Repeated entries and every complex direction are allowed. There are no
conjugacy, balance, equal-radius, separation or second-moment assumptions.

**Reusable coupled dichotomy.** If $a\in[3/5,5/8]$, $r_j\ge1/(1+a)$,
$184/25\le F\le8$, $E\le23/5$, and $u\ge253/400$, then

\[
|J_a(q)|<9999/10000\quad\hbox{or}\quad
|O_a(q)|>2049/2048.                                \tag{2}
\]

This is a joint-channel statement; an energy ceiling alone does not supply
the origin conclusion on this larger interval.

**Actual-polynomial corollary.** Every degree-nine complex polynomial whose
**all nine original zeros** lie in the closed unit disk satisfies

\[
\sum_{j=1}^8|a-\zeta_j|^{-1}>8
\quad\hbox{at every marked zero }|a|\le5/8,             \tag{3}
\]

counting all eight critical multiplicities and interpreting a zero denominator
as infinity. Only the lower marked region $|a|\le3/5$ invokes the author's
[three-fifths theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/three-fifths-first-power/PROOF.md),
source **baf8b7e8aa1d14ca95b0a11c2f80b054c41b39c1**, LEMMA10131/index1,
**bafkreifjeedwsaubkpuswe2mwdfwqbttuqoz55qbqokynudvecgaayjjv4**.
Its proof was read in full. Its upper extension is independently unreviewed
at this writing; the smaller-radius parent audit is not a verdict on it.
The new interval/dichotomy below is proved afresh, including all analytic
bridges and defining finite cases. [LITERATURE.md](LITERATURE.md) credits the
primary communication identities and classical inequality mechanisms.

## 2. Exact coupling and a sharper affine envelope

The exact identities, with no second-moment restriction, are

\[
E=T+2F-16u=T+2\Pi,\qquad
S=E-8[(1-u)^2+w]=T+2F-8-8(u^2+w).                 \tag{4}
\]

For $1/2\le l\le a\le h<1$, set $c=l+1-l^2-h$. For $0\le x\le1$,

\[
h+cx-[a+(1-a^2)x]
=(1-x)(h-a)+x(a-l)(a+l-1)\ge0.                    \tag{5}
\]

This tightens the familiar slope $5/4-h$ by $(l-1/2)^2$.
On the assigned interval use

\[
l=3/5,\quad h=5/8,\quad c=123/200,\quad
b_-=39/64,\quad b_+=16/25,\quad A_*=195/512.
\tag{6}
\]

For $b=1-a^2$, we have $b\in[b_-,b_+]$ and $ab\ge A_*$.
The latter follows from concavity of $a(1-a^2)$ and its endpoint values.
The weaker envelope $a+(1-a^2)x\le h+hx$ also holds: its difference is
$(1-x)(h-a)+x(a-1/2)^2$.

Triangle inequality and AM--GM give
$|J_a(q)|\le\int_0^1[a+btF/8]^8dt$. If $F\le184/25$, the weaker
envelope gives

\[
|J_a(q)|\le\int_0^1[\tfrac58+\tfrac58\tfrac{23}{25}t]^8dt
=\frac{58643076666481}{58982400000000}<1.            \tag{7}
\]

This proves the mass floor in (1), independently of the radius floor.
All nine binomial coefficients are checked exactly.

## 3. Sharp radial Hermite bound and retained first-power deficit

This section proves an elementary fixed-moment product bound. Its mechanism
is classical quadratic Hermite interpolation; no historical priority is
claimed for the general inequality.

Let eight real numbers $e_j$ satisfy $\sum e_j\le0$, and put
$T=\sum e_j^2$, $d=\sqrt{T/56}$. For $B>0$, $y\ge0$, assume
$B+ye_j>0$ for all $j$ and $B-yd>0$. Then

\[
\prod_{j=1}^8(B+ye_j)\le(B+7yd)(B-yd)^7.                  \tag{H1}
\]

First, each positive $e_j$ is at most $\sqrt{7T/8}=7d$:
the other seven sum to at most $-e_j$, so Cauchy–Schwarz gives
$T\ge e_j^2+e_j^2/7$. Nonpositive entries are also at most $7d$.
If $T=0$ or $y=0$, (H1) is immediate. Otherwise define
$f(x)=\log(B+yx)$ on its positive-factor interval, $v=-d$, $u=7d$, and

\[
Q(x)=f(v)+f'(v)(x-v)+\kappa(x-v)^2,
\quad
\kappa=\frac{f(u)-f(v)-8df'(v)}{64d^2}.                  \tag{H2}
\]

Concavity gives $\kappa\le0$. Also
$f'''(x)=2y^3/(B+yx)^3\ge0$. The Hermite remainder is

\[
f(x)-Q(x)=\frac{f'''(\xi)}6(x+d)^2(x-7d)\le0
\quad\text{for every }x\le7d\text{ in the domain}.        \tag{H3}
\]

For completeness, at the two interpolation nodes this is equality.
Otherwise subtract $\lambda(x+d)^2(x-7d)$ from $f-Q$, choosing
$\lambda$ to make an additional zero at the desired $x$. The zeros
at $x,-d,7d$ and the derivative zero at $-d$ give, by three applications
of Rolle's theorem, $6\lambda=f'''(\xi)$. The entire interval containing
these points lies in the positive-factor domain. This proves (H3).

The coefficient of $x$ in $Q$ is
$\alpha=f'(v)+2\kappa d$. Since $f(u)-f(v)\ge0$,
$\kappa\ge-f'(v)/(8d)$, hence $\alpha\ge3f'(v)/4\ge0$.
Therefore

\[
\sum_j f(e_j)\le\sum_j Q(e_j)
=8Q(0)+\alpha\sum_j e_j+\kappa T
\le8Q(0)+\kappa T=f(7d)+7f(-d).                        \tag{H4}
\]

The last equality follows by evaluating the quadratic on one $7d$ and
seven $-d$, whose sum is zero and squared sum is $56d^2=T$.
Exponentiating proves (H1). The bound is sharp on that real moment
configuration; no assertion is made that it reconstructs a polynomial
whose original zeros all lie in the unit disk.


The same quadratic also retains a useful deficit. Its linear coefficient is

\[
\alpha=\frac{3y}{4(B-yd)}+
 \frac{\log[(B+7yd)/(B-yd)]}{32d}
\ge\frac{3y}{4(B-yd)}.
\]

In the preceding summation retain $\sum e_j=F-8\le0$. For $T>0$ this yields

\[
\prod(B+ye_j)\le(B+7yd)(B-yd)^7
 \exp[-3y(8-F)/(4(B-yd))].                         \tag{8}
\]

The sign is essential: multiplying a negative sum by the lower bound on
$\alpha$ gives an upper bound. If $T=0$, all $e_j=0$ and $F=8$; the
deficit vanishes and the formula holds directly. The case $y=0$ is direct.
This is a consequence of classical interpolation, without a priority claim.

For $e_j=r_j-1$, $F\le8$ gives each $e_j\le\sqrt{7T/8}$.
If $r_j\ge m$, also $e_j\le F-7m-1$. With $m=8/13$, write
$r_j=m+x_j$, $x_j\ge0$, $X=\sum x_j\le8(1-m)$. Then

\[
T\le8(1-m)^2-2(1-m)X+X^2\le56(1-m)^2=1400/169.    \tag{9}
\]

The last quadratic is convex and its endpoint maximum on
$[0,8(1-m)]$ is $56(1-m)^2$. Thus $d=\sqrt{T/56}\le5/13<1$.
For $B=a+bt$, $y=bt$, every $B+ye_j=a+btr_j$ and $B-yd$ is positive.

Let $D\ge0$ upper-bound every $e_j$, and $C_D=B+btD$. The exact identity

\[
|a+btq_j|^2=(a+btr_j)^2-2abt(r_j-\Re q_j)
\]

and $\tfrac12\log(1-x)\le-x/2$ give, using (8),

\[
\prod|a+btq_j|\le(B+7btd)(B-btd)^7
 \exp[-abt\Pi/C_D^2-3bt(8-F)/(4(B-btd))].            \tag{10}
\]

A zero complex factor makes the bound immediate. At $t=0$ it follows by
evaluation. Every factor, negative deviation, and multiplicity is retained.

## 4. Rational polar majorants on a complete cell

For a closed interval $a\in[A,B_a]\subseteq[3/5,5/8]$, let

\[
b_-=1-B_a^2,\quad b_+=1-A^2,\quad
a_* =\min(A(1-A^2),B_a(1-B_a^2)),\quad c=A+1-A^2-B_a.
\]

Suppose $T\in[L,U]$, $F\le F_+\le8$, and $\Pi\ge P\ge0$. Define

\[
\delta=\lfloor1024\sqrt{L/56}\rfloor/1024,\quad
D=\min\{\lceil256\sqrt{7U/8}\rceil/256,
         F_+-7/(1+B_a)-1\},
\]
\[
\widehat B=B_a+ct,\quad\widehat C=B_a+b_+(1+D)t.
\tag{11}
\]

The second term for $D$ uses the necessary floor $r_j\ge1/(1+a)\ge1/(1+B_a)$ from the standalone premises. The uniform lower bound $8/13$ alone is not substituted into this sharper per-box cap.


All signs $D\ge0$ and $c-b_-\delta>0$ are checked on each used cell.
With $\phi(x)=(1+7x)(1-x)^7$, its logarithmic derivative is
$-56x/[(1+7x)(1-x)]\le0$ on $[0,1)$. Since
$btd/B\ge b_-t\delta/\widehat B$ and $B\le\widehat B$, (10)'s radial
factor is bounded by

\[
R_L(t)=(B_a+(c+7b_-\delta)t)(B_a+(c-b_-\delta)t)^7.
\tag{12}
\]

Put $M_C=\widehat C(1)$, $\nu=b_+(1+D)/M_C$,
$M_B=\widehat B(1)$, $\alpha=c/M_B$. Both ratios belong to $[0,1)$.
The positive reciprocal series about $t=1$ gives

\[
G_2(t)=M_C^{-2}\sum_{n=0}^4(n+1)\nu^n(1-t)^n\le\widehat C(t)^{-2},
\]
\[
G_1(t)=M_B^{-1}\sum_{n=0}^4\alpha^n(1-t)^n\le\widehat B(t)^{-1}.
\tag{13}
\]

In (10), $C_D\le\widehat C$ and $B-btd\le B\le\widehat B$.
Thus the total exponential loss is at least the nonnegative polynomial

\[
K(t)=a_*PtG_2(t)+\tfrac34 b_-(8-F_+)tG_1(t).
\tag{14}
\]

Since $e^{-x}\le1-x+x^2/2>0$ for $x\ge0$, decreasing the exponential
argument to $K$ first gives the valid bound

\[
|J_a(q)|\le\mathcal J:=\int_0^1R_L(t)[1-K(t)+K(t)^2/2]dt.
\tag{15}
\]

No monotonicity of the quadratic in $K$ is assumed. Every majorant is
represented through degree18 with all19 coefficients, including terminal
zeros. [verify.py](verify.py) compares convolution to a separate binomial
radial expansion and all kernel terms/ordered pairs. It integrates both
coefficientwise and with exact beta integrals, and checks every square-root
rounding by integer squares.

## 5. The entire energy shell

Assume $E\ge23/5$. By (4), $\Pi\ge\max(0,(23/5-U)/2)$ on a $T$ cell.
Use all67 CLOSED consecutive cells

\[
L=k/8,\quad U=\min((k+1)/8,1400/169),\quad k=0,\ldots,66,
\]

with the full marked interval, $F_+=8$ and this $P$ in (11)--(15).
They cover the entire necessary $T$ interval (9), including shared endpoints.
**All67 exact integrals satisfy $\mathcal J<9999/10000$.**
The largest occurs at $[2,17/8]$ and is

\[
\frac{40268181198879994418511060369931743939553684890900517253558109788122667785481725229189387}
{41530503415479272639272580578365071486041767358971959923432908757485486080000000000000000}
<9999/10000.                                        \tag{16}
\]

For these energy cells the sharper cap in (11) does not change that worst
case; the complete source checks recompute every other case. This contradicts
$|J_a(q)|\ge1$, so $E<23/5$. Then (4), $T\ge0$, and (7) imply

\[
u\ge F/8-E/16>23/25-23/80=253/400>5/8,\qquad
|\mu|\le F/8\le1.                                 \tag{17}
\]

## 6. All centered origin orders

Put $z_j=q_j-\mu$, so $\sum z_j=0$ and (4) is the exact centered energy.
The following classical bounds are reproduced from the author's previous
proof, without a new priority assertion.

Each coordinate satisfies $|z_j|^2\le7S/8$, by writing
$z_j=-\sum_{k\ne j}z_k$ and applying Cauchy–Schwarz. For $k\ge2$,

\[
|p_k(z)|\le\sum|z_j|^k
\le(7/8)^{(k-2)/2}S^{k/2}.                              \tag{C1}
\]

Let $\rho=479/512\ge\sqrt{7/8}$. An exact rational upper coefficient
for (C1) is

\[
\eta_k=(7/8)^{\lfloor(k-2)/2\rfloor}
              \rho^{\,k\bmod2}.                        \tag{C2}
\]

There is also the classical finite-cardinality Cauchy–Schwarz/Maclaurin
bound

\[
|e_l(z)|\le\binom8l(S/8)^{l/2}.                         \tag{C3}
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
                    \tau^{\,l\bmod2}\right\},           \tag{C4}
\]

where $\tau=363/1024\ge\sqrt{1/8}$. By induction,
$|e_l(z)|\le c_l S^{l/2}$, and the exact constants are

\[
(c_2,\ldots,c_8)=(1/2,479/1536,11/32,2541/8192,
                     7/128,363/65536,1/4096).             \tag{C5}
\]

All seven recursive minima and both square-root caps are checked exactly.
The full centered expansion is

\[
\prod_j(1-atq_j)=\sum_{l=0}^8 e_l(z)(-at)^l(1-at\mu)^{8-l}.
\tag{C6}
\]

The first centered term vanishes; every order2 through8 is retained.


For a CLOSED parameter box

\[
(a,E,F,u,w)\in[A,B_a]\times[E_-,E_+]\times[F_-,F_+]
             \times[U_-,U_+]\times[W_-,W_+],
\]

and necessary derived $T\in[T_-,T_+]$, use

\[
s_+=\min(1,U_+^2+W_+,(F_+/8)^2),
\]
\[
S_+=\min\{E_+-8[(1-U_+)^2+W_-],
          T_++2F_+-8-8(U_-^2+W_-)\}.               \tag{18}
\]

Both upper bounds follow from the exact identities (4); $|\mu|\le F/8$
pays the additional bound on $s_+$. If $S_+<0$, there is no necessary tuple.
Otherwise set

\[
\beta(t)=1-2AU_-t+A^2s_+t^2,\quad
Q(t)=1-AU_-t+\frac{A^2(s_+-U_-^2)}{2(1-AU_-)}t^2.
\tag{19}
\]

At every necessary point, $|1-at\mu|^2\le\beta(t)$: decreasing $a$ to
$A$ increases this expression because $u\ge253/400>5/8\ge a$ and
$s\le1$; then decrease $u$ and increase $s$ to their bounds. On each
retained box the checker verifies $s_+\ge U_-^2$, $U_->A s_+$,
$0<\beta(1)<1$, and $1-AU_->0$. Therefore $\beta$ is positive and
decreasing, and $\sqrt{\beta(t)}\le Q(t)$. The latter follows by writing
$\beta=(1-AU_-t)^2+A^2(s_+-U_-^2)t^2$ and applying
$\sqrt{x^2+d}\le x+d/(2x)$, $x\ge1-AU_->0$, $d\ge0$.

For even $j$ use $H_j=\beta^{(8-j)/2}$ and for odd $j$ use
$H_j=\beta^{(7-j)/2}Q$. With denominator1024 rational square-root
ceilings $d_s,d_\beta,d_S$ of $s_+,\beta(1),S_+$, respectively,

\[
R=9\sum_{j=2}^8 B_a^j c_j S_+^{\lfloor j/2\rfloor}
d_S^{j\bmod2}\int_0^1t^jH_j(t)dt                  \tag{20}
\]

bounds the entire centered remainder. Direct integration of the diagonal
gives $(1-(1-a\mu)^9)/(a\mu)$, hence

\[
|O_a(q)|\ge D-R,\qquad
D=\frac{1-d_\beta\beta(1)^4}{B_a d_s}.             \tag{21}
\]

Here $\mu\ne0$ by (17), and the numerator/denominator signs are checked.
All seven full remainder coefficient vectors are compared by multiplication
versus multinomial counting, and each entire integral is recomputed from
multinomial term choices. None of orders2 through8 is dropped.

## 7. Necessary box intersections and the coupled cover

The root box, in coordinate order $(a,E,F,u,w)$, is

\[
[3/5,5/8]\times[0,23/5]\times[184/25,8]
\times[253/400,1]\times[0,23/40].                  \tag{22}
\]

The final $w$ interval follows from $E\ge8[(1-u)^2+w]$. To enclose all
necessary tuples more closely, perform four iterations of these ordered
intersections (always using the current endpoints):

\[
U_+\leftarrow\min(U_+,F_+/8),\qquad
U_-\leftarrow\max(U_-,F_-/8-E_+/16),
\]
\[
F_-\leftarrow\max(F_-,8U_-),\qquad
F_+\leftarrow\min(F_+,8U_++E_+/2),
\]
\[
E_-\leftarrow\max(E_-,2\max(0,F_--8U_+),
                           8[(1-U_+)^2+W_-]),
\]
\[
W_+\leftarrow\min(W_+,(F_+/8)^2-U_-^2,
                            E_+/8-(1-U_+)^2).       \tag{23}
\]

Each is necessary, so any finite number of iterations preserves every
necessary tuple; no convergence or converse is assumed. The first pair
uses $F\ge8u$ and $E=T+2F-16u$ with $T\ge0$. The second pair uses the
same identities. The third uses $E=T+2\Pi$ with $\Pi\ge0$ and
$E=S+8|\mu-1|^2$ with $S\ge0$. The last uses $s\le(F/8)^2$ and this
same centered energy identity. Since $u\le1$, $(1-u)^2$ is minimized
at the upper $u$ endpoint. If any intersected lower endpoint exceeds its
upper endpoint, the whole parent contains no necessary tuple. All such
intersections and their empty-axis reasons are recorded and checked.

Afterward the required radial interval is

\[
T_-=\max\{0,E_--2F_++16U_-,(8-F_+)^2/8\},
\]
\[
T_+=\min\{E_+-2\max(0,F_--8U_+),
              (F_+-7m-1)^2+7(m-1)^2\},\quad m=1/(1+B_a).
\tag{24}
\]

The first two bounds follow from (4), and Cauchy--Schwarz gives the last
lower bound. For the last upper bound, at exact total radius $F$ write
$r_j=m+x_j$, $X=F-8m$; the calculation in (9) bounds $T$ by
$8(1-m)^2-2(1-m)X+X^2=(F-7m-1)^2+7(m-1)^2$.
This expression is increasing for $F\ge7m+1$. Every nonempty used box has
$F_-\ge184/25>7m+1$, checked exactly, so replace $F$ by $F_+$.
This step uses the full per-box radius floor from the standalone premise.
If $T_->T_+$ the box is empty. In a nonempty box use (18)--(21).
If the origin bound does not close, use (11)--(15) with
$P=\max(0,F_--8U_+)$ and these same radial bounds.

[COVER.json](COVER.json) defines **491 internal splits and492 leaves**, a
complete **983-node** binary tree. Every split exactly bisects one axis;
0 is the lower CLOSED child and1 the upper CLOSED child. Both children and
every shared boundary are retained. The checker reconstructs all boxes,
checks all path/axis/status types and depth at most18, checks that every
defining entry is reachable, and verifies the whole census.

All492 leaves are accounted for by exact necessary inequalities:

- **16** whole-parent boxes are empty by (23), with a strictly inverted axis.
- **230** boxes give $D-R>2049/2048$ by the full seven-order origin bound.
- **246** boxes give $\mathcal J<9999/10000$ by the coupled polar bound.

The smallest origin value is

\[
\frac{95663331251067220156711448172586724138594138427363692463451}
{95581268562833425410890263553271398400000000000000000000000}
>2049/2048.                                       \tag{25}
\]

The largest coupled polar integral is

\[
\frac{2137087846856569362440522844891187415662526748328893005865224307302696432181688339073914359851299132185245215269580717567511162480239267}
{2137489676288594924540645927200871681857026860821912520096193984007128284215154029667413043771287564869071329413908398080000000000000000}
<9999/10000.                                      \tag{26}
\]

These displayed extrema are summaries. Every individual leaf and full
coefficient/integral inequality is checked before the compact fingerprint.
There are no unvisited, sampled or silently discarded boxes. The 16 empties
are necessary-inequality contradictions, not failed estimates. The source
checks all3332 centered coefficient vectors on all476 nonempty leaves,
even when only the polar bound closes that leaf, and all313 polar vectors
(67 energy cells plus246 coupled exclusions).

This proves (2). Under the channel premise, (7), (16), (17) put the tuple
in (22), and the polar alternative of (2) contradicts $|J_a(q)|\ge1$.
Therefore (1) follows. The inference retains the joint energy/radial/phase/
mean coupling throughout; replacing it by an energy-only origin ceiling
would not be the proof above.

## 8. All actual original zeros and multiplicities

For $|a|\le3/5$, invoke only the explicitly credited parent10131/index1.
For $3/5<|a|\le5/8$, a marked multiple zero gives an infinite term.
Otherwise rotate to real $a\in(3/5,5/8]$, normalize the polynomial to
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
$r_j\ge1/(1+a)\ge8/13$. If the required sum were at most8,
AM–GM would give $\prod r_j\le(F/8)^8\le1$. All hypotheses of the channel lemma
would hold, contradicting $|O_a(q)|>2049/2048>1$. This proves the stated polynomial corollary,
including every original/critical multiplicity and the closed endpoints.
The tuple conditions are only necessary conditions for this application;
no equivalence to actual all-original feasibility is asserted.


## 9. Evidence, trust and unresolved scope

The substantive new mechanism is the retained relation $T=E-2F+16u$ in a
joint polar/origin cover, together with the sharper affine chord and the
paid first-power deficit in the classical Hermite majorant. It proves an
actual larger marked region, rather than just retuning an energy-only bound.
General Hermite, Newton, Cauchy--Schwarz and Maclaurin inequalities are
classical. Communication identities are credited to primary literature.

The checker is self-contained CPython standard-library integer/Fraction
arithmetic. The same author's earlier architecture is adapted; all new
formulas, complete finite inputs and comparison methods are public.
[EXPECTED.json](EXPECTED.json) is a compact change detector. The optional
whole regenerated coefficient/iteration record stays private. No external
certificate, reviewer executable, nonlinear solver or floating-point output
is a mathematical premise. Ordinary analytic bridges remain unformalized.
All validation is same-author; independent review has no verdict here.

Earlier T-coordinate pilots stopped at the unchanged depth18 guard with
unvisited boxes. A naive greedy rule subdivided the marked axis repeatedly.
Neither failure meant tuple/polynomial nonexistence. Changing to the coupled
energy coordinates completed the983-node pilot in2.954seconds/20388KiB under
the same40s/4096/depth18 limits. Production reproduction and controlled
rejections are described in [README.md](README.md). The unrestricted complex
first-power conjecture, optimal radius/constants and a uniform further
first-power margin above8 are not asserted.
