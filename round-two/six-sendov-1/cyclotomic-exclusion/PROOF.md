# A complex coefficient chamber and a quantitative cyclotomic exclusion

Actual author **six-sendov-1**, role **researcher**, 2026-10-02. This is
a complete ordinary analytic author proof with exact finite coefficient
and constant checks. It is unformalized and independently unreviewed.
The shared campaign signature does not establish independent authorship.

## 1. Statements and quantifiers

Put $e=2^{-16}$, $0<\eta\le e$, and $a=1-\eta$. Write

$$
 p(z)=z^9+\sum_{k=0}^8 c_kz^k,\qquad
 F(p,a)=\sum_{j=1}^8|a-\zeta_j|^{-1},\qquad
 H=\sum_{j=1}^8|\zeta_j|^2,
$$

where the eight zeros of $p'$ are counted with algebraic multiplicity.
A zero denominator means $+\infty$. Define the **coefficient chamber**
by the literal conditions

$$
                  |c_k|\le2\eta\quad(1\le k\le8).       \tag{1}
$$

The constant coefficient is unrestricted in this analytic chamber. For
every complex monic polynomial in (1), all eight critical points have
modulus less than (1/4), and

$$
 F(p,a)>8+\frac H6-193\eta
       \ge8+\frac43(|c_1|/9)^{1/4}-193\eta.              \tag{2}
$$

In particular, for **every** such polynomial with $F(p,a)\le8+3\eta$,

$$
 H<1176\eta,\qquad
 |c_k|<\frac9k\binom8{9-k}(147\eta)^{(9-k)/2}
                   \quad(1\le k\le8),                 \tag{3}
$$

and $ |c_1|<4202539929\eta^4$. These are universal inequalities on
the stated chamber and whole positive interval, including critical
collisions. Neither disk-rootedness nor $p(a)=0$ is needed for (2)--(3).
The latter condition is needed when these statements are used in the
assigned marked-root problem.

Let $M(\eta)$ be the infimum of $F(p,1-\eta)$ over all monic complex
degree-nine polynomials whose zeros are in the closed unit disk and
which vanish at $1-\eta$. No attainment is assumed. Let

$$
 P_a(z)=(z-a)(1+z+\cdots+z^8)
       =z^9-1+\eta(1+z+\cdots+z^8).                    \tag{4}
$$

For every disk-rooted monic complex $p$ with $p(a)=0$ and the **full
lower-coefficient maximum norm** condition

$$
 \max_{0\le k\le8}|c_k(p)-c_k(P_a)|\le\frac78\eta,     \tag{5}
$$

we have the strict quantitative exclusion

$$
                   F(p,a)-M(\eta)>(\eta/72)^{1/4}.     \tag{6}
$$

For $P_a$ itself the stronger gap is $>(\eta/9)^{1/4}$. The ball (5)
contains actual strictly interior feasible polynomials, not only a
boundary example. Its coefficient geometry places the whole ball
outside both the sufficient antipodal entry test in9357 and the
displayed branch coefficient ball in9373; the precise imported scopes
for this last comparison are stated in Section7.

The chamber is a specified partial region. The actual legal comparison
branch has $c_8>4\eta$ and lies outside (1); hence entry of every
low-valued competitor into this chamber is false. Determining the
physical feasibility of its reduced sublevel box, covering other
coefficient regions, whole-window branch global optimality and the
unrestricted first-power inequality require further work. Small-
$\eta$ qualitative critical concentration and holomorphic trace
methods were already prior mathematics; Section8 preserves that credit.

## 2. Critical localization from the whole derivative

The entire derivative is

$$
 p'(z)=9z^8+\sum_{k=1}^8 k c_k z^{k-1}.                \tag{7}
$$

For $0<r<1$, differentiating the convergent geometric series gives
$\sum_{k\ge1}kr^{k-1}=(1-r)^{-2}$. The finite sum is smaller.
On $|z|=r=1/4$, (1) therefore gives

$$
 |p'(z)-9z^8|\le2\eta\sum_{k=1}^8kr^{k-1}
                  <\frac{2\eta}{(1-r)^2}<9r^8.        \tag{8}
$$

The sufficient endpoint margin for the last inequality is exactly
$9r^8-2e/(1-r)^2=49/589824>0$. Rouché gives eight zeros of $p'$
strictly inside the circle, with multiplicity, accounting for its
whole degree. Since $a>255/256>1/4$, all terms of (F) are finite.
If $p(a)=0$, that marked original root is automatically simple.
No assumption of simple critical points or numerical root isolation
has entered the proof.

## 3. An exact square decomposition that retains critical energy

For $|t|<1$, choose the analytic square root $s(t)=\sqrt{1-t}$ with
$s(0)=1$, and put $G(t)=1/s(t)$. Exactly,

$$
 |G(t)|^2=2\Re G(t)-1+|G(t)-1|^2,\qquad
 G(t)-1=\frac{t}{s(t)(1+s(t))}.                       \tag{9}
$$

The second identity follows from $(1-s)(1+s)=t$; the chosen branch
has $1+s\ne0$. For $t=\zeta_j/a$, Section2 and $a>255/256$ give
$|t|<64/255$. Thus

$$
 |s(t)|\le\sqrt{1+|t|}<9/8,\qquad |1+s(t)|<17/8,
$$

because $81/64-319/255=239/16320>0$. Consequently

$$
 |G(t)-1|^2\ge\frac{|t|^2}{6},                       \tag{10}
$$

using $4096/23409>1/6$, whose difference is (389/46818).
Since $ |G(\zeta/a)|^2=a/|a-\zeta|$, summing (9)--(10) yields

$$
 F(p,a)\ge\frac8a+\frac2a\Re\Theta+\frac{H}{6a^3},
       \qquad \Theta=\sum_{j=1}^8G(\zeta_j/a)-8.       \tag{11}
$$

In particular, a cubic Taylor tail has not subtracted from the positive
energy term. This square decomposition and the complex-analytic trace
formula below are classical algebra and complex analysis; their method
is not advertised as a new historical technique.

## 4. A uniform bound for the entire analytic trace

Set $h=p'/9$, $R=5/8$, and on a neighborhood of $|z|=R$ put

$$
 q(z)=\frac{h(z)-z^8}{z^8},\quad
 B=\frac{2}{9R^8(1-R)^2}=\frac{2147483648}{31640625}.
$$

The full coefficient bound (1) gives
$|q(z)|<B\eta<1/900$, since
$1/900-Be=9553/126562500>0$. These strict bounds hold on some
annulus about the circle. There

$$
 L(z)=\log(1+q(z))=\sum_{m\ge1}\frac{(-1)^{m+1}q(z)^m}{m}
$$

is single-valued and analytic, with
$|L(z)|\le |q|/(1-|q|)<B\eta(900/899)$. Absolute uniform
convergence on that annulus justifies the logarithm and its derivative.
We need this logarithm only near the contour; it is **not** asserted
analytic across $z=0$.

For $f(z)=G(z/a)$, analytic throughout the circle and its interior,
the argument principle, all eight critical roots being inside, gives

$$
 \sum_j f(\zeta_j)=\frac1{2\pi i}\int_{|z|=R} f(z)\frac{h'(z)}{h(z)}\,dz.
$$

On the contour $h'/h=8/z+L'$. Its first term integrates to $8f(0)=8$.
Integration of the derivative of the single-valued function (fL)
around the closed contour is zero. Therefore the **whole** trace is

$$
               \Theta=-\frac1{2\pi i}\int_{|z|=R}f'(z)L(z)\,dz.       \tag{12}
$$

This identity holds through all critical collisions, since the argument
principle counts multiplicities and uses a fixed contour without
individual root labels.

On that contour $R/a<32/51$ and $1-R/a>19/51$. We have

$$
 |G'(z/a)|\le\frac1{2(1-R/a)^{3/2}}<9/4,
$$

as $(19/51)^3-4/81=925/397953>0$. The contour length in (12), the
chain factor (1/a), and the logarithm bound now give

$$
 |\Theta|<\frac{R}{a}\frac94,B\frac{900}{899}\eta
        <\frac{24}{17}B\frac{900}{899}\eta
        =\frac{68719476736}{716390625}\eta<96\eta.       \tag{13}
$$

The final margin is $54023264/716390625>0$. Equations (11)--(13),

$$
  2(256/255)96<193\quad
       (\text{margin }21/85>0),\qquad a<1,
$$

prove the strict first inequality of (2). The derivative constant term
in (7) gives exactly $\prod_j\zeta_j=c_1/9$, since the degree is
eight. AM--GM on the eight nonnegative numbers $|\zeta_j|^2$ gives
$H\ge8(|c_1|/9)^{1/4}$, including $c_1=0$. This proves (2).

## 5. The weighted coefficient reduction for the entire sublevel set

Combining $F\le8+3\eta$ with the strict first inequality of (2) gives
$H<6(193+3)\eta=1176\eta$. For $m=1,\ldots,8$, Cauchy--Schwarz
over all $\binom8m$ subsets gives

$$
 |e_m(\zeta)|^2\le\binom8m e_m(|\zeta_1|^2,\ldots,|\zeta_8|^2)
                  \le\binom8m^2(H/8)^m.               \tag{14}
$$

The last inequality is the standard Maclaurin bound for nonnegative
numbers with fixed sum. One can prove this particular bound by
averaging any two entries: their sum stays fixed, and their product
increases, so $e_m$ does not decrease. Its maximum on the compact
fixed-sum simplex is therefore attained when all entries equal; zero
entries follow by continuity. This proves the displayed bound without
any unknown sign of a complex elementary symmetric sum.

The whole derivative factorization in (7) identifies

$$
            \frac{k c_k}{9}=(-1)^{9-k}e_{9-k}(\zeta).
$$

Apply (14) and $H/8<147\eta$ to obtain every one of the eight strict
bounds in (3). For $k=1$ the multiplier is9 and the exponent4;
$9\cdot147^4=4202539929$. These are additional chamber restrictions,
not sufficient conditions for disk-rootedness or for branch entry.
In particular the first coefficient collapse does not by itself locate
six criticals at order $\eta$ and two at order $\sqrt\eta$.

## 6. The actual feasible exclusion ball and its comparison value

The imported legal comparison theorem **9113** gives, for every

$0<\eta\le2^{-16}$, an actual disk-rooted monic degree-nine polynomial
with marked root $a$ and objective $F_{\mathrm{branch}}<8+3\eta$.
Its precise source is [validated branch proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/validated-boundary-branch/PROOF.md).
This legal-family assertion, independently confirmed within its scope
by9174, is the only substantive external input to (6). It implies

$$
               0\le M(\eta)\le F_{\mathrm{branch}}<8+3\eta,\qquad
 F(p,a)-M(\eta)>\frac43(|c_1|/9)^{1/4}-196\eta.         \tag{15}
$$

We do not identify $M$ with that branch value.

The identity (4) makes $c_k(P_a)=\eta$ for $k=1,\ldots,8$.
Condition (5) thus implies $ |c_k(p)|\le15\eta/8<2\eta$ and
$|c_1(p)|\ge\eta/8$. Set $v=(\eta/72)^{1/4}>0$. Throughout the
whole positive interval,

$$
 \frac{588\eta}{v}\le1,
 \quad\text{because }588^4\,72\,e^3<1
 \quad\left(1-588^4\,72\,e^3
                 =\frac{133236413543}{137438953472}>0\right).
$$

All quantities are nonnegative, so fourth powers preserve the
comparison; no fractional-power rounding is used. Now (15) gives
$F-M>\frac43v-196\eta\ge v$, proving (6). For $P_a$, use
$|c_1|=\eta$ and the same absorption with72 replaced by9.

Its eight unmarked roots are exactly the ninth roots of unity other
than1; $a<1$ is distinct from them. Hence $P_a$ itself is feasible.
To obtain strictly interior feasible points, let
$\tau=\eta/16$, $r=1-\tau$, and define

$$
 P_{a,r}(z)=(z-a)\sum_{k=0}^8r^{8-k}z^k.              \tag{16}
$$

Its roots are $a$ and $r\omega$ for the eight ninth roots of unity
$\omega\ne1$; they are all simple and strictly inside the disk.
The coefficients are $c_0=-ar^8$ and
$c_k=r^{8-k}(\eta-\tau)$, $1\le k\le8$. Thus

$$
 |\Delta c_0|=a(1-r^8)<8\tau=\eta/2,
 \quad |\Delta c_k|\le\tau+7\eta\tau<\eta/8.
$$

These strict bounds lie inside (5). Simple-root continuity at this
particular interior polynomial gives a nonempty open feasible subset
relative to the complex coefficient hyperplane $p(a)=0$, still inside
(5). That last openness argument is qualitative; (5)--(6) themselves
are the literal explicit neighborhood and inequality.

## 7. Comparison with the two sufficient local tests

This paragraph uses two precisely identified published test domains,
not their full analytic proofs as premises of (2)--(6).

In **9357**, [the antipodal coefficient interface](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/anisotropic-entry/PROOF.md),
entry requires $\max_j|(a-Z_j)^{-1}-(1+a)^{-1}|\le1/1000$.
Its elementary necessary consequence is
$|c_8(p)-(8-a)|\le16/499$. For any polynomial in (5),
$|c_8|\le15\eta/8$ and $8-a=7+\eta$, giving

$$
 |c_8-(8-a)|\ge7-7\eta/8>6>16/499.                   \tag{17}
$$

Thus every feasible polynomial in the new ball fails that epsilon
test, irrespective of its remaining energy or signed-trace budgets.

The same legal branch **9113** has

$$
 p_0'(z)=9(z-\eta x)^6[(z-\eta y)^2+\eta T],\qquad
 c_8(p_0)=-\frac94\eta(3x+y)>4\eta.                  \tag{18}
$$

For clarity, the last bound follows from its exact initial data
$3x+y=U/2$, $U=-8(2/3-Y)$,
$Y=1/[3(1+\cos(\pi/9))]\in(1/6,4/21)$, and its componentwise
continuation cube of radius1/1024. The change in (3x+y) is at most
1/256, so
$c_8(p_0)/\eta>30/7-9/1024>4$. This is the branch bound already
used in9357; no new branch computation or verdict is asserted.

Therefore for all of (5),

$$
             |c_8(p)-c_8(p_0)|>17\eta/8.              \tag{19}
$$

The improved literal branch coefficient neighborhood in **9373**,
[normalized neighborhood proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/normalized-neighborhood/PROOF.md),
has radius $\delta^6 2^{-1999}\eta^{13}$ for
$\delta=(1/2-33\eta/16)-k$, $0\le k<1/2-33\eta/16$.
In particular $0<\delta\le1/2$, so this radius is less than
$2^{-2005}\eta^{13}<\eta$. Equations (19) and this last elementary
comparison make the two balls disjoint, including its sufficient
$k=1/4$ radius $2^{-2017}\eta^{13}$.
We import no9373 radius review and do not claim the entire two basins
are joined by a common entry theorem. The present proof instead
**excludes one explicit region missed by both displayed tests**.

The benchmark $z^9-a^9$ remains outside (5), since its $c_1=0$
differs from $c_1(P_a)=\eta$. Its critical points all vanish and its
objective $8/a>8$ satisfies (2); this method does not route it into
the branch collar. The actual legal branch (18) is itself a
low-valued competitor outside (1), so universal sublevel entry into
this chamber is impossible, not merely an outstanding proof obligation.

## 8. Prior art, checks and remaining obligations

[Current primary literature](LITERATURE.md) separates the conjectured
first-power endpoint from the proved quadratic Tang--Zhang inequality.
Ordinary Sendov is reported resolved; it is not renamed as this work.
The published **8530** leading-profile theorem and **8608** independent
audit already credit asymptotic critical concentration
$H=O(\eta)$, coefficient bootstrap and holomorphic trace methods.
The scales $\sqrt\eta$ and $\eta^4$ in (3) are not claimed as new
qualitative asymptotic phenomena. The new objects here are the literal
full-window **complex coefficient chamber**, its complete weighted
sublevel bounds, and the positive quarter-power **feasible coefficient
ball exclusion** (6), with actual comparison value and test separation.

Signed canonical graph intake through9378, bounded concepts among162
relevant family contributions, recent pertinent reports and repository
commits, and the final9373 statement were inspected before claiming
these objects. A major signed refresh through9395 inspected the newer
9385/9388 independent review scopes as context, with no imported
calculation or transferred verdict. No quarter-power family exclusion matched that bounded
scan. This is not an exhaustive literature search, an absence theorem,
or a historical priority certificate. The elementary square identity,
Rouché, the argument principle, contour integration by parts, logarithmic
series, Cauchy--Schwarz, Maclaurin and AM--GM remain classical inputs.

[verify.py](verify.py) uses only exact rational arithmetic and sparse
polynomials. It regenerates **entire coefficient dictionaries** for the
cyclotomic/anchored/radial identities, the full general derivative and
Vieta correspondence, and12 independent Newton versus logarithmic
coefficient traces. It also checks every finite sufficient constant,
the whole positive interval via monotone endpoint bounds, every
coefficient in (3), the ball/domain/separation margins and meaningful
damaged hypotheses. The full regenerated record must equal
[EXPECTED.json](EXPECTED.json); malformed/missing/changed fixtures
reject explicitly even under optimized Python. Finite trace checks
are exact identity verification, not a substitute for the analytic
whole-trace argument (12)--(13).

The analytic square-root branch, the multiplicity-counting Rouché and
argument-principle steps, the annular logarithm, whole-contour integration,
Maclaurin/AM--GM passage, feasible comparison9113 and simple-root
openness remain ordinary written mathematics. The checker does not
formally verify complex analysis or independently audit the imported
branch certificate. No solver, numerical roots, finite eta grid,
timeout, incomplete enumeration or resource failure supplies a proof.

Concrete next frontier: determine whether the reduced box (3) can
contain a disk-rooted polynomial with the marked root and
$F\le8+3\eta$, using actual original-root disk constraints to
restrict its retained $c_8,c_7$ terms. An impossibility proof would
exclude the whole chamber; a feasible witness would identify a further
comparison problem. Neither conclusion is proved here. Coverage of
other coefficient regions must explicitly include the known comparison
branch rather than assume it enters (1). Resources remain exact
arithmetic, one serial job and one native thread in the existing1CPU/
2GiB scope. Additional workers, larger limits, review direction and
operational control changes are unnecessary.
