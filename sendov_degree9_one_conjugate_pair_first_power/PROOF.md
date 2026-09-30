# Degree-nine first power with at most one nonreal critical pair

Author: **six-sendov-1**, role **researcher**. Date: 2026-09-30.
Status: complete ordinary written proof, with a finite exact polynomial
certificate. Independent review of this extension is pending. No external
formalization was rebuilt and no historical-priority claim is made.

Let $p$ have degree nine, with all zeros in the closed unit disk. Count its
eight critical points $\zeta_j$ with multiplicity, and set

$$S_1(p,a)=\sum_{j=1}^8|a-\zeta_j|^{-1}$$

at a zero $a$, interpreting a zero denominator as infinity.

**Theorem.** Suppose $p$ is real up to a nonzero scalar, $a$ is real, and
at least six of its eight critical points are real, counted with
multiplicity. Then $S_1(p,a)\ge8$, strictly if $|a|<1$. The two remaining
critical points may form a nonreal conjugate pair. The derivative may
change sign on the segment from $0$ to $a$. Equality holds exactly when
$|a|=1$ and

$$p(z)=C(z^9-a^9)\quad\text{or}\quad p(z)=C(z-a)(z+a)^8,
\qquad C\ne0.$$

**Affine version.** Suppose the zero multiset is invariant under reflection
in an affine line $L$ containing $a$, and at least six critical points lie
on $L$. If $h=\operatorname{dist}(0,L)<1$, then

$$S_1(p,a)\ge\frac8{\sqrt{1-h^2}}, \tag{1}$$

strictly if $|a|<1$. If $h=1$, the sum is infinite.

These are cases of the first-power Tang--Zhang conjecture. They do not
establish the unrestricted endpoint. The new finite lemma below permits
one conjugate pair without a sign condition on the other six origin
factors. This is distinct from the previous monotone-axis result.

## 1. Normalization and published inputs

Make $p$ monic and, if necessary, reflect its variable so $0\le a\le1$.
If $p'(a)=0$, the sum is infinite. Otherwise $a$ is simple. Set

$$q_j=(a-\zeta_j)^{-1},\qquad r_j=|q_j|,
\qquad l=\frac1{1+a},\qquad b=1-a^2.$$

Gauss--Lucas gives $r_j\ge l$. The classical origin identity is

$$O_a(q):=9\int_0^1\prod_j(1-atq_j)\,dt
=\prod_{i=1}^8z_i\prod_jq_j,
\qquad |O_a(q)|\le\prod_jr_j, \tag{2}$$

where $z_i$ are the other eight original zeros. The polar identity gives

$$1\le\int_0^1\prod_j|a+btq_j|\,dt. \tag{3}$$

These identities are inherited from
[Tao, Lemma 6](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
and [Zhang, Lemma 3.1](https://arxiv.org/html/2609.19126).

The published
[positive-coordinate origin lemma](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_first_power/PROOF.md),
source `177818bdbd7e23f16ec46bacfc3077d7a22a8aca`, graph
`bafkreihcaireletdhn563ajzos46pfqtjeha3iv3ceg5x4i33qu62eilw4`, states
that for eight positive coordinates $v_j\ge l$ with $\sum v_j\le8$,

$$O_a(v)-\prod_jv_j\ge m(a):=\frac{8(1-a^9)}{(1+a)^8}
\ge\frac9{32}(1-a)>0\quad(a<1). \tag{4}$$

It is a dependency here, and was independently confirmed by
[six-reviewer-3](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_review3/README.md),
source `18c89c2ca1ffbbfc173867ddace5b1c82c5e7d6d`, graph
`bafkreibdsmdxcby5ie76hbjc2j5bq2xip3vkkuimwcvkvmlcxrbjrkxte4`.
That review does not cover the present extension.

We also use the
[negative-real-coordinate exclusion, Section 2](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_origin_angular_monotone/PROOF.md),
source `7eb0bac3d54294930118ac2ac0aa37cdb73b52b1`, graph
`bafkreibmpkev3bekc2s2eixm3vprwycinocfzv4i6idhyzmvspedckjcae`:
under a hypothetical $S_1\le8$ at an interior real root, every real $q_j$
is positive, even when the other coordinates are complex. Briefly, a
negative coordinate has modulus at least $1/(1-a)$, so the budget forces
$a\le3/4$. Its polar factor satisfies the nonnegative chord bound
$|a-brt|\le a+(br-2a)t$. For the other coordinates use
$|a+btq_i|\le a+btr_i$. AM--GM gives

$$\prod_j|a+btq_j|\le[a+(1-a^2-a/4)t]^8.$$

The cited source's three rational integral upper bounds on
$[0,1/2],[1/2,5/8],[5/8,3/4]$ are all less than one, contradicting (3).

## 2. A one-pair origin lemma

Fix $0<a<1$. Suppose $s_1,\ldots,s_6,r\ge l$, with

$$\sum_{i=1}^6s_i+2r\le8,
\qquad \frac{1-br^2}{2a}\le x\le r. \tag{5}$$

Define the real expression

$$E_a(s,r,x)=9\int_0^1\prod_{i=1}^6(1-at s_i)
\bigl(1-2atx+a^2t^2r^2\bigr)\,dt-r^2\prod_{i=1}^6s_i.$$

**Lemma.** Throughout (5),

$$E_a(s,r,x)\ge g(a):=\frac{44(1-a^9)}{7(1+a)^8}
\ge\frac{99}{448}(1-a)>0. \tag{6}$$

No assertion that the factors $1-at s_i$ have one sign is needed.

For fixed $s,r$, the expression is affine in $x$. The lower endpoint
$x_0=(1-br^2)/(2a)$ satisfies $x_0\le r$, since $r\ge l$.
At the upper endpoint $x=r$, (4) applied to
$(s_1,\ldots,s_6,r,r)$ gives $E_a\ge m(a)\ge g(a)$.
It therefore suffices to establish (6) at $x=x_0$. At that endpoint the
paired factor is exactly

$$1-2atx_0+a^2t^2r^2=1-t+(bt+a^2t^2)r^2. \tag{7}$$

If $x_0<-r$, the lower endpoint is not a complex point of modulus $r$.
This causes no problem: $E_a$ is a real affine expression in $x$, and
bounding both endpoints of this larger interval bounds every feasible
complex point. In particular the reduction works for all $0<a<1$;
there is no omitted $a<1/2$ range.

## 3. Complete finite profile reduction

Fix $a,r$ and $x=x_0$. The domain in the six $s_i$ is compact and
nonempty. The expression $E_a$ is symmetric and multiaffine in these
six variables. Choose a global minimizer with the fewest coordinates
strictly above $l$. For two such coordinates, with all others fixed,
the expression has the form

$$A+B(s_i+s_j)+C s_i s_j.$$

If $s_i\ne s_j$, the two-sided fixed-sum variation
$(s_i+t,s_j-t)$ is feasible for small $t$. Stationarity gives
$C(s_j-s_i)=0$, hence $C=0$. The expression is then constant along the
whole feasible fixed-sum segment. Move one coordinate to $l$, contradicting
minimality of the number above $l$. Thus every free coordinate has a
common value $s$.

Let $k$ be the number fixed at $l$, and $m=6-k$. It is enough to consider
$k=0,\ldots,5$; the all-$l$ point is included by $u=0$ below. The budget
gives

$$l\le r\le4-3l=\frac{1+4a}{1+a}.$$

With $D=1+a$, the profiles are parametrized by $0\le u,v\le1$ as

$$r=\frac R D,\quad R=1+4av,
\qquad s=\frac C D,\quad C=1+\frac{8a}{m}(1-v)u. \tag{8}$$

Indeed the upper bound for $s$ is $(8-2r-kl)/m$, and (8) covers the
entire interval from $l$ to that upper bound. No saturation of the budget
is assumed.

After multiplying the profile's value by $D^8$, (7) gives a polynomial
in the three independent variables $a,u,v$:

$$P_k(a,u,v)=9\int_0^1(D-at)^k(D-at C)^m
\left[D^2(1-t)+(bt+a^2t^2)R^2\right]dt-R^2C^m. \tag{9}$$

The following finite formula specifies it without quadrature. Set $n=i+j$:

$$\begin{aligned}
P_k={}&9\sum_{i=0}^k\sum_{j=0}^m(-1)^n
\binom ki\binom mj a^nD^{6-n}C^j
\left[\frac{D^2}{(n+1)(n+2)}
+\frac{R^2}{n+2}-\frac{a^2R^2}{(n+2)(n+3)}\right]-R^2C^m.
\end{aligned} \tag{10}$$

It follows directly by integrating the powers of $t$ in (9).

## 4. Exact Bernstein certificate and the uniform gap

Write $B_i^d(t)=\binom di t^i(1-t)^{d-i}$. At the tensor degrees in the
table, the complete expansion is

$$P_k(a,u,v)=\sum_{i,j,h}\beta_{ijh}^{(k)}
B_i^{d_a}(a)B_j^{d_u}(u)B_h^{d_v}(v). \tag{11}$$

If $c_{rst}$ are the power coefficients from (10), every coefficient is
specified by the rational formula

$$\beta_{ijh}^{(k)}=
\sum_{r\le i,\ s\le j,\ t\le h}c_{rst}
\frac{\binom ir}{\binom{d_a}r}
\frac{\binom js}{\binom{d_u}s}
\frac{\binom ht}{\binom{d_v}t}. \tag{12}$$

| $k$ | Tensor degrees $(d_a,d_u,d_v)$ | All coefficients | Minimum positive coefficient | Zero indices |
|---:|---:|---:|---:|---:|
| 0 | $(16,6,12)$ | 1547 | $8$ | none |
| 1 | $(15,5,7)$ | 768 | $8$ | none |
| 2 | $(14,4,6)$ | 525 | $8$ | none |
| 3 | $(13,3,5)$ | 336 | $8$ | none |
| 4 | $(12,2,4)$ | 195 | $8$ | none |
| 5 | $(11,1,3)$ | 96 | $44/7$ | $(11,1,0)$ |

All **3467** entries are rational and are nonnegative. The $k=0$ profile
has actual $v$ degree eight, elevated to twelve for a nonnegative
certificate. A negative coefficient before elevation would not establish
a negative value of $P_0$. Every coefficient with $i=0$ is exactly eight.

The standard-library checker `verify.py` reconstructs (10), independently
multiplies the defining factors in the four variables $(a,u,v,t)$ and
integrates them, and compares all resulting power coefficients. It then
computes every coefficient in (12) and checks all sign, minimum and zero
conditions in the table. Finally it expands every Bernstein basis element
back to powers and verifies all six complete polynomial identities. Thus
the basis conversion is checked in the reverse direction as well.

`expected.json` stores small deterministic summaries and SHA-256 hashes of
all coefficients in lexicographic index order. The full coefficients are
specified by (9)--(12) and regenerated locally. No omitted search corpus,
floating arithmetic, solver result or incomplete enumeration is evidence.

Nonnegative Bernstein bases sum to one. Hence $P_k\ge8$ for $k\le4$.
For $k=5$, let $c=44/7$. Its sole zero term has weight
$a^{11}u(1-v)^3$, so

$$P_5\ge c[1-a^{11}u(1-v)^3]
\ge c(1-a^{11})\ge c(1-a^9).$$

All profiles therefore satisfy $P_k\ge c(1-a^9)$. This applies at a
global minimizing profile and proves the same bound on the entire
six-coordinate domain. Dividing by $D^8$ and taking the affine minimum
over $x$ proves the first bound in (6). Its second bound follows from
$g=(11/14)m$ and the published linear bound in (4).
The constants are conservative, without an optimality claim.

## 5. Applying the lemma to the polynomial

Assume $0<a<1$ and $S_1\le8$. Negative real $q_j$ are excluded in
Section 1. If all eight critical points are real, (4) already contradicts
(2). Otherwise the reciprocals consist of six positive real coordinates
$s_i$ and one conjugate pair $q=x+iy,\overline q$, of common modulus $r$.
Their sum of moduli gives the budget in (5).

For the associated critical point $\zeta=a-1/q$, its unit-disk condition
is exactly

$$|\zeta|^2\le1
\quad\Longleftrightarrow\quad br^2+2ax-1\ge0.$$

Together with $x\le r$, this is (5). The paired origin factor is
$(1-atq)(1-at\overline q)=1-2atx+a^2t^2r^2$.
Thus (6) gives

$$O_a(q)\ge r^2\prod_i s_i+g(a)>\prod_j|q_j|,$$

contradicting (2). At $a=0$, the same hypothetical budget and $r_j\ge1$
force all $r_j=1$, while $O_0(q)=9>1=\prod_jr_j$. This completes
strictness for every interior real marked root.

At $a=1$, the classical identity
$\sum_jq_j=2\sum_i(1-z_i)^{-1}$ and
$\operatorname{Re}(1/(1-z_i))\ge1/2$ give $S_1\ge8$.
The full degree-nine first-power
[boundary classification, Section 7](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/PROOF.md),
source `728857924504f28020dea5de6590ae3458b7bc90`, graph
`bafkreideaathnoyujdk5pmy4d3qmhu45tyevkegmjmtgmwyvoq2b2pjnue`,
gives the two equality families in the statement. Both have eight real
critical points after normalization, so both are included here.

For the affine version, rotate $L$ to $\operatorname{Im}z=h$ and translate
by $-ih$. The transformed monic polynomial is real. Conjugate transformed
zeros $w=x\pm iy$ give

$$|w|^2\le1-h^2-2|h||y|\le1-h^2.$$

Scale by $\sqrt{1-h^2}$ and apply the real theorem, retaining the count of
critical points on the axis. Distances scale by this radius, proving (1).
An original interior marked root becomes an interior root of the scaled
disk. If $h=1$, reflection and containment force every zero to the unique
unit-disk point of $L$, so the sum is infinite.

## 6. A strict scope example

The following exact rational example has a real derivative zero in
$(0,a)$, six real critical points and a nonreal pair:

$$p(z)=(z-3/4)(z+3/4)^6\bigl((z+3/4)^2+1/16\bigr),
\qquad a=3/4.$$

Its original zeros are $3/4$, $-3/4$ six times, and
$-3/4\pm i/4$. Their moduli are at most one; the complex pair has squared
modulus $5/8$. With $w=z+3/4$,

$$p'(z)=w^5\left(9w^3-12w^2+\frac7{16}w-\frac9{16}\right).$$

The real cubic's discriminant is $-4174875/1024<0$, so it has exactly
one real zero and one simple nonreal conjugate pair. Its values at
$w=3/4$ and $w=3/2$ have opposite signs; the former is $-51/16$, the
latter is positive. Its unique real zero therefore lies at $0<z<a$.
Consequently $p'(0)<0<p'(a)$ and the preceding monotone-axis theorem
does not apply. The original zeros are not collinear and the critical
points are not all real.

Moreover

$$\prod_{i=1}^8|a-z_i|=(3/2)^6(9/4+1/16)
=\frac{26973}{1024}>9.$$

Thus the elementary derivative-product criterion
$\prod|a-z_i|\le9$ does not cover this example either. This example
separates scopes; it is not a sharpness claim.

## 7. Remaining real case and trust boundary

Combine this theorem with the preceding monotone-axis theorem. Any
hypothetical $S_1\le8$ at a real interior root of a real degree-nine
polynomial must have **exactly two or three nonreal conjugate critical
pairs**, counted with multiplicity, and at least one real critical point
of odd multiplicity in the open segment from $0$ to $a$ after reflection
to $a>0$. Four nonreal pairs would make the monic derivative positive on
the whole real axis, so that case is already monotone. Zero or one pair
is covered here. If no real critical point of odd multiplicity lies in
$(0,a)$, the derivative has a fixed sign on that segment and is again
covered by the monotone theorem. This is a structural reduction of the
remaining real-polynomial problem, not a solution of it.

The new finite endpoint lemma is useful independently of actual polynomial
realizability. It uses only the reciprocal budget, radial lower bounds and
the conjugate pair's critical-point disk constraint. The general complex
case and the remaining two- and three-pair real cases are unresolved here.

Written mathematics supplies complex factorization, Gauss--Lucas, the
classical communication identities, the minimizer reduction, convexity
in $x$, Bernstein positivity and the affine geometry. Exact computation
checks the finite algebraic certificate and scope example. The published
positive-coordinate gap, negative-real exclusion, monotone case and
boundary classification are explicitly cited dependencies. The independent
input review does not imply an independent review of this new theorem.
