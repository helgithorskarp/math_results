# Whole complex coefficient-chamber exclusion and its sharp boundary slope

Actual author **six-sendov-1**, role **researcher**, 2026-10-02.
Complete ordinary analytic author proof with exact finite coefficient and
budget checks; unformalized and independently unreviewed. Shared campaign
signatures do not establish independent authorship.

## 1. Statements, scope and comparison

Let $0<\eta\le e=2^{-16}$, $a=1-\eta$, and
$p(z)=z^9+\sum_{k=0}^8c_kz^k$. Count all eight critical points
$\zeta_j$ with algebraic multiplicity, and put
$F=\sum_j|a-\zeta_j|^{-1}$ and $H=\sum_j|\zeta_j|^2$.
The chamber is the literal condition

$$
             |c_k|\le2\eta\quad(1\le k\le8),                 \tag{1}
$$

with $c_0$ unrestricted. For **every complex monic polynomial** in this
chamber, without a marked-root, disk or conjugation assumption,

$$
 F\ge8+\frac{14}{3}\eta-147\eta^{3/2}>8+4\eta.               \tag{2}
$$

In particular the entire sublevel $F\le8+3\eta$ in (1) is empty.
This closes the physical feasible-intersection question posed after
[9428](../cyclotomic-exclusion/PROOF.md), by an analytic obstruction
that needs no original-root disk constraints.

Define $I_{\rm ch}(\eta)$ as the infimum of $F$ over (1), and
$I_{\rm disk}(\eta)$ as the infimum over those chamber polynomials that
also have $p(a)=0$ and all nine original zeros in the closed unit disk.
No attainment is assumed. We construct an actual marked disk-rooted
family in (1) with all nine original roots simple and strictly interior:

$$
 b=\frac{2\eta}{9},\quad v=\frac{7\eta}{18}-\frac{28\eta^2}{81}>0,
 \quad p_\eta'(z)=9((z+b)^2+v)^4,\quad p_\eta(a)=0.          \tag{3}
$$

It has $c_8=c_7=2\eta$, $|c_k|\le4\eta^2$ for $1\le k\le6$, and

$$
 F(p_\eta,a)=\frac8{\sqrt{1-7\eta/6+7\eta^2/27}}.
$$

Consequently both restricted infima have the **sharp first-order slope**

$$
 \lim_{\eta\downarrow0}\frac{I_{\rm ch}(\eta)-8}{\eta}
 =\lim_{\eta\downarrow0}\frac{I_{\rm disk}(\eta)-8}{\eta}
 =\frac{14}{3}.                                           \tag{4}
$$

Let $M(\eta)$ be the unrestricted marked disk-rooted infimum. The actual
legal comparison [9113](../../six-sendov-3/validated-boundary-branch/PROOF.md)
gives $M(\eta)<8+3\eta$, independently confirmed within the scope of
[9174](../../six-reviewer-3/certified-branch-audit/REVIEW.md). Thus every
physical chamber competitor satisfies $F-M(\eta)>\eta$, and every
actual $\eta$-near-minimizer $F-M(\eta)\le\eta$ must satisfy
$\max_{1\le k\le8}|c_k|>2\eta$.
The known comparison branch has $c_8>4\eta$ and remains outside the
chamber. Nothing here identifies the unrestricted minimizer or resolves
the global first-power inequality. The earlier quarter-power gap on
9428's smaller cyclotomic ball remains stronger on that smaller set.

## 2. Two exact critical traces with a retained energy term

Write $T_m=\sum_j\zeta_j^m$. Newton/Vieta for the entire monic derivative
$p'/9$ give, through every collision,

$$
       T_1=-8c_8/9,\qquad T_2=T_1^2-14c_7/9,\qquad H\ge|T_2|.       \tag{5}
$$

These classical identities also appear in the complementary peer
moment-entry work for a distinct normalized-collar purpose; no priority
for the identities is asserted.

For $G(t)=(1-t)^{-1/2}$ on $|t|<1$, choose $G(0)=1$ and
$s(t)=\sqrt{1-t}$ with $s(0)=1$. Exactly

$$
 |G(t)|^2=2\Re G(t)-1+|G(t)-1|^2,\quad
 G(t)-1=\frac{t}{s(t)(1+s(t))}.                            \tag{6}
$$

Suppose temporarily that all $|t_j|=|\zeta_j/a|\le r\le1/6$.
Since $|s(t)|^2\le1+r$ and
$\sqrt{1+r}\le1+r/2$, the denominator in the square of (6) is at most
$(1+r)(4+2r)\le4+8r$. Therefore

$$
 |G(t)-1|^2\ge(1/4-r/2)|t|^2.
$$

The last step follows from
$1/(4+8r)-(1/4-r/2)=r^2/(1+2r)\ge0$.
The binomial coefficients $g_m=\binom{2m}{m}/4^m$ are positive and
decreasing, because $g_{m+1}/g_m=(2m+1)/(2m+2)$. For every $m\ge3$,
$g_m\le g_3=5/16$. Absolute convergence gives the entire tail bound

$$
 |G(t)-1-t/2-3t^2/8|\le\frac5{16}\frac{|t|^3}{1-|t|}.
$$

Sum (6) over all eight criticals, use
$|G(\zeta/a)|^2=a/|a-\zeta|$, and divide by $a$.
The two-sided tail costs at most
$(5/8)rH/[a^3(1-r)]\le(3/4)rH/a^3$. Thus

$$
 F\ge\frac8a+\frac{\Re T_1}{a^2}
       +\frac{3\Re T_2}{4a^3}
       +(1/4-5r/4)\frac H{a^3}.                          \tag{7}
$$

The energy coefficient is at least $1/24$. Combining it with $H\ge|T_2|$
gives the useful general two-coefficient estimate

$$
 F\ge\frac8a+\frac{\Re T_1}{a^2}
             -(1/2+5r/4)\frac{|T_2|}{a^3}.                \tag{8}
$$

Weak inequalities are intentional and include $H=0$. The infinite-series
tail follows from the all-index recurrence and geometric series, not a
finite coefficient test. No individual critical label is differentiated.

## 3. Bootstrap and the complete positive parameter interval

9428 proves for every polynomial in (1) that all criticals have modulus
less than $1/4$ and

$$
                        F>8+H/6-193\eta.                 \tag{9}
$$

Use only that coarse bound as the analytic premise. If $F>8+5\eta$,
(2)'s first inequality already follows. Otherwise (9) gives
$H<1188\eta$. Since $a>255/256$, $\sqrt{1188}<35$, and
$35(256/255)<36$, every critical obeys

$$
 |\zeta_j/a|<36\sqrt\eta\le36/256=9/64<1/6.
$$

Apply (8) with $r=36\sqrt\eta$. The chamber and (5) give
$|T_1|\le16\eta/9$ and
$|T_2|\le28\eta/9+256\eta^2/81$. Hence

$$
 F\ge\frac8a-\frac{16\eta}{9a^2}
     -\frac{1}{2a^3}(28\eta/9+256\eta^2/81)
     -\frac{5r}{4a^3}(28\eta/9+256\eta^2/81).             \tag{10}
$$

All following inequalities hold on the entire positive interval:

$$
 a^{-3}<(256/255)^3<33/32,\quad
 28/9+256\eta/81<25/8,\quad
 \frac54\frac{33}{32}\frac{25}{8}36=\frac{37125}{256}<146.
$$

Thus the last term costs less than $146\eta^{3/2}$.
Subtract $8+(14/3)\eta$ from the first three terms of (10).
Their **entire** polynomial numerator is

$$
 \frac{\eta^2}{a^3}
             [-146/81-6\eta+(14/3)\eta^2]\ge-2\eta^2,
$$

because $(33/32)(146/81+6e)<2$. Since
$2\eta^2\le\eta^{3/2}/128$, (10) proves the first inequality of (2).
Finally
$14/3-147/256-4=71/768>0$ proves its strict second inequality.
No sampled eta value, solver verdict or enumeration supplies coverage.

## 4. Exact family and a whole complex parameter disk

In (3), integrate the entire derivative and subtract its value at $a$.
This fixes a unique monic marked polynomial. The critical polynomial is

$$
 ((z+b)^2+v)^4
   =(z^2+(4\eta/9)z+7\eta/18-8\eta^2/27)^4.
$$

Its two critical values $-b\pm i\sqrt v$ each have multiplicity four.
Full coefficient expansion gives $c_8=c_7=2\eta$; the cancellation in
$28b^2+4v$ is essential.

For feasibility allow $\eta$ complex, $|\eta|<\rho=1/128$, with
$a=1-\eta$. Put $B=2/9$ and $V=7/18+28\rho/81$. For $t=|\eta|$,
the positive polynomial $((z+Bt)^2+Vt)^4$ majorizes every derivative
coefficient. For $1\le k\le6$ its relevant coefficient has t-order at
least two. After multiplying by $9/k$, dividing by $t^2$, and taking
the monotone endpoint $t=\rho$, the six exact bounds are

$$
 \frac{260144641}{20061226008576},\
 \frac{2048383}{69657034752},\
 \frac{8241919}{1451188224},\
 \frac{96901}{6718464},\
 \frac{78029}{46656},\
 \frac{763}{243};
$$

all are less than4. Consequently $|c_k|\le4|\eta|^2$ for $k=1,\ldots,6$
on the entire complex disk. The exact upper two coefficients still have
modulus $2|\eta|$, not the larger positive majorant for $c_7$.
For $|z|\le17/16$, the anchored polynomial satisfies

$$
 |p_\eta(z)-(z^9-1)|\le P|\eta|,\quad
 P=9(1+\rho)^8+2[(17/16)^8+(1+\rho)^8]
  +2[(17/16)^7+(1+\rho)^7]
  +4\rho\sum_{k=1}^6[(17/16)^k+(1+\rho)^k]
  =\frac{1480778418455293707}{72057594037927936}<21.       \tag{11}
$$

## 5. Actual original-root disk feasibility

Let $\omega$ run over the nine ninth roots of unity and draw the fixed
circle of radius $d=1/16$ about each. Their separation exceeds $1/2$
(for instance $\sin(\pi/9)>\sin(\pi/12)>1/4$), so the disks are disjoint.
Taylor's complete remainder for $z^9$ gives on each boundary

$$
 |z^9-1|\ge9d-36(1+d)^7d^2>1/4,
 \qquad |p_\eta-(z^9-1)|<21/128<1/4.
$$

Rouché gives exactly one original root counted with multiplicity in each
disk. Every section $Z_\omega(\eta)$ is therefore simple and uniquely
holomorphic on the whole complex eta disk. The marked section is exactly
$a$. For a root within the disk,

$$
 |(Z^9-1)/(Z-\omega)|\ge9-36d(1+d)^7>5,
 \qquad |Z_\omega-\omega|<5|\eta|.
$$

At $Z=\omega$ use the limiting quotient; the displacement bound is then
trivial. Define the holomorphic companion half-normal

$$
 \alpha_\omega(\eta)=[Z_\omega(\eta)Z_{\bar\omega}(\eta)-1]/2.
$$

For real eta the polynomial has real coefficients, so this equals the
actual $(|Z_\omega|^2-1)/2$. It vanishes at eta0, and
$|\alpha_\omega|\le(5+25\rho/2)|\eta|<6|\eta|$.
The quotient $\beta_\omega=\alpha_\omega/\eta$ is removable and
holomorphic, bounded by6 on $|\eta|<\rho$. Cauchy's coefficient bounds,
first on smaller circles and then their limit, give

$$
 |\beta_\omega(\eta)-\beta_\omega(0)|
       \le6\,\frac{|\eta|/\rho}{1-|\eta|/\rho}
       \le6/511\quad(0<\eta\le e).                       \tag{12}
$$

The full first polynomial jet is
$p_\eta=z^9-1+\eta(2z^8+2z^7+5)+O(\eta^2)$.
Implicit differentiation of the simple originals gives, for
$\omega=e^{i\theta}$,

$$
 \beta_\omega(0)=-[5+2\cos\theta+2\cos2\theta]/9
               =-[4(\cos\theta+1/4)^2+11/4]/9
               \le-11/36.
$$

Together with (12),
$\beta_\omega(\eta)\le-11/36+6/511=-5405/18396<0$.
Thus **all nine original roots are strictly inside the unit disk**
for every positive eta in the stated interval. This proves physical
feasibility, rather than inferring it from the small critical points.

## 6. Sharp restricted infima and remaining frontier

For real positive eta, (3) has $v>0$ and
$(a+b)^2+v=1-7\eta/6+7\eta^2/27>0$, proving the exact objective.
Its analytic right derivative at eta0 is $14/3$. Its lower coefficients
lie in the chamber because $4\eta^2<2\eta$.
For every eta the physical family is a legal test for both restricted
infima, so

$$
 8+(14/3)\eta-147\eta^{3/2}
 \le I_{\rm ch}(\eta)\le I_{\rm disk}(\eta)
 \le8/\sqrt{1-7\eta/6+7\eta^2/27}.
$$

Divide by eta after subtracting8 and squeeze as eta decreases to zero:
(4) follows. No optimizer, compactness theorem or attainment is used.

The actual unrestricted near-minimum comparison remains9113, with9174's
scope review. This sharp chamber slope is different from a global
boundary slope or normalized branch-entry power. Classical repeated
critical templates and the already known degree-nine4+4 first-power
class retain credit; the family is an explicit chamber sharpness test,
not a new proof of that full class.

The concrete next frontier is complementary coefficient coverage.
Low-valued competitors must leave (1); use the two-trace inequality (7)
to characterize which $c_8,c_7$ directions permit near-minimum values
and then impose actual original-root feasibility. The known branch
must remain among the admissible complementary directions. An
infimum gap, sharp restricted slope and failure of a local entry test
do not identify the global branch minimizer or prove the endpoint.

[verify.py](verify.py) checks whole polynomial and quotient identities,
all finite parameter budgets and meaningful damaged hypotheses.
Root continuation, Cauchy, Rouché, infinite binomial convergence and
the imported9428/9113 analytic premises remain ordinary written
mathematics, not a formal proof or independent audit.
