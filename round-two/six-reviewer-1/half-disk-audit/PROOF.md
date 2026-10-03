# Independent half-disk audit and an explicit first-power margin

Actual author **six-reviewer-1**, role **independent mathematical reviewer**.
This is an ordinary, unformalized proof. The defining written proof and
rational tables of six-sendov-1's LEMMA10092 were exposed; the audit is
**not blind**. Its executable and expected fixture were unopened during
this reconstruction. The argument below credits that lemma's analytic
architecture and independently audits its continuous bridges. No global
Tang–Zhang conclusion, optimal constant or literature priority is claimed.

## 1. Exact statements

For a finite nonzero complex eight-tuple, define
\[
r_j=|q_j|,\quad F=\sum r_j,\quad \mu=\tfrac18\sum q_j,\qquad
J_a=\int_0^1\prod_{j=1}^8[a+(1-a^2)tq_j]dt,\qquad
O_a=9\int_0^1\prod_{j=1}^8(1-atq_j)dt.
\]

Put \(\eta=0\) or \(\eta=1/1000\), and \(m=1+\eta/8\).
For **every** \(a\in[2/5,1/2]\) and every such tuple satisfying
\[
r_j\ge2/3,\qquad F\le8+\eta,\qquad |J_a|\ge1,
\tag{1}
\]
we prove
\[
F>39/5,\quad E:=\sum|q_j-1|^2<3,\quad
|\mu|\le m,\quad \Re\mu>63/80,
\quad |O_a|>\frac{15}{8m}-\frac{111}{128}>m^8.
\tag{2}
\]
The hypotheses do not require any individual critical-disk inequality
beyond the radius floor, or reality, conjugacy, separation, equal radii,
balance or a second-moment bound. Repeated tuple entries are allowed.
For \(\eta=0\), (2) is the **complete standalone conclusion** of10092,
including its strict \(|O_a|>129/128\) bound. For \(\eta=1/1000\),
the enlarged budget and explicit uniform polynomial margin below are
refinements of10092, not claims made by its author.

Consequently, every degree-nine complex polynomial with all nine original
zeros in the **closed unit disk** satisfies, at every marked zero
\(|a|\le1/2\),
\[
\boxed{\sum_{j=1}^8|a-\zeta_j|^{-1}>8001/1000.}
\tag{3}
\]
Every critical multiplicity is retained; a zero denominator contributes
infinity. Arbitrary original multiplicities and closed endpoints are included.

## 2. Original-polynomial communication and endpoints

After rotation and monic normalization, a simple marked zero has real
\(0<a\le1/2\), and
\[
p(z)=(z-a)R(z),\quad R(z)=\prod_{j=1}^8(z-z_j),\quad
p'(z)=9\prod_{j=1}^8(z-\zeta_j),\quad q_j=(a-\zeta_j)^{-1}.
\]
Simplicity ensures that all eight denominators and \(R(a)\) are nonzero.
Integrating \(p'\) from \(a\) to0, and then from \(a\) to \(1/a\), gives
\[
O_a=9R(0)/R(a)=\prod z_jq_j,\qquad
J_a=a^8R(1/a)/R(a)=\prod\frac{1-az_j}{a-z_j}.
\tag{4}
\]
The power \(a^8\) in the second equality cancels the eight denominators
from evaluating \(R(1/a)\); the factor9 is retained in the origin identity.
These classical identities are credited to Tao's communication Lemma6
and Zhang's Lemma3.1. They are proved here without invoking a quadratic
inequality or a peer's numerical theorem.

Since \(|z_j|\le1\), each
\[
|1-az_j|^2-|a-z_j|^2=(1-a^2)(1-|z_j|^2)\ge0.
\]
Thus \(|J_a|\ge1\) and \(|O_a|\le\prod r_j\).
Gauss–Lucas gives \(|\zeta_j|\le1\), hence \(r_j\ge1/(1+a)\ge2/3\).
If \(F\le8+\eta\), AM–GM gives \(\prod r_j\le m^8\).
Therefore (2) contradicts these necessary original-polynomial conditions.
No converse from these conditions to original-root feasibility is used.

For \(0<a\le2/5\), triangle inequality and AM–GM directly give
\[
|J_a|\le\int_0^1[a+(1-a^2)mt]^8dt
\le\int_0^1[2/5+(21/25)mt]^8dt<1.
\tag{5}
\]
The pointwise derivative in \(a\) is \(1-2amt\ge1-(4/5)m>0\)
on this smaller interval. This is still valid for the enlarged budget;
monotonicity on the entire half interval with \(m>1\) is neither asserted
nor needed. The final strict rational integral is checked exactly.

At \(a=0\), simplicity gives
\(\prod r_j=9/\prod|z_j|\ge9>m^8\), so AM–GM implies \(F>8m\).
If the marked root is multiple, it is also critical and \(F=+\infty\).
Other repeated original or critical roots require no limiting argument.
Rotation preserves every distance. This proves all cases of (3) once (2)
is established.

## 3. Mass, radial variance and logarithmic payment

Regardless of the enlarged upper budget, \(F\le39/5\) would imply
\[
|J_a|\le\int_0^1[1/2+(117/160)t]^8dt
=424265002554558889/429496729600000000<1.
\tag{6}
\]
Here the pointwise monotonicity is used with \(F/8\le39/40<1\)
and \(a\le1/2\), so its derivative is nonnegative. Hence (1) forces
\(F>39/5\).

Write
\[
e_j=r_j-1,\quad T=\sum e_j^2,\quad
\Pi=\sum(r_j-\Re q_j),\qquad E=T+2\Pi.
\]
We have \(\Pi\ge0\) and \(\sum e_j\le\eta\).
Writing \(r_j=2/3+x_j\), with \(x_j\ge0\) and
\(X=\sum x_j\le8/3+\eta\), shows
\[
T=8/9-(2/3)X+\sum x_j^2
\le8/9-(2/3)X+X^2
\le T_*:=56/9+(14/3)\eta+\eta^2.
\tag{7}
\]
The quadratic is convex; the right endpoint exceeds the left endpoint's
value8/9. If \(e_j>\eta\), the other seven entries sum to at most
\(-(e_j-\eta)\). Cauchy–Schwarz and \(e_j^2\ge(e_j-\eta)^2\)
therefore give \(T\ge(8/7)(e_j-\eta)^2\). For all entries,
\[
e_j\le\eta+\sqrt{7T/8}.
\tag{8}
\]
At \(\eta=0\), this recovers10092's positive radial ceiling.

Put \(b=1-a^2\), \(B=a+bt\), and \(C=B+btd\), where
\(e_j\le d\) for all entries and \(d\ge0\). For \(u>-1\),
\(u\le v\), \(v\ge0\),
\[
\log(1+u)\le u-\frac{u^2}{2(1+v)}.
\tag{9}
\]
For nonnegative \(u\), integrate \(s/(1+s)\ge s/(1+u)\)
between0 and \(u\). For negative \(u\), reversing the integral's
orientation gives \(u-\log(1+u)\ge u^2/2\); this is stronger than (9).
Applying (9) to \(u=bte_j/B\), with \(v=btd/B\), is legitimate
because \(a+btr_j>0\). Its linear terms sum to at most \(\eta bt/B\le\eta\).

The separate phase identity is
\[
|a+btq_j|^2=(a+btr_j)^2-2abt(r_j-\Re q_j).
\]
For a vanishing complex factor the product bound below holds directly.
Otherwise, apply \(\tfrac12\log(1-u)\le-u/2\) to its relative
phase loss, which lies in \([0,1)\). Since \(a+btr_j\le C\),
summing both losses yields the pointwise bound
\[
\prod|a+btq_j|\le
e^{\eta}B^8\exp\left[-\frac{b^2t^2T}{2BC}-\frac{abt\Pi}{C^2}\right].
\tag{10}
\]
The sole change to10092's logarithmic bound is the explicit \(e^\eta\)
payment; it cannot be silently dropped when \(F>8\).

## 4. Complete closed concentration cover

Assume \(E\ge3\). Use both closed marked intervals
\([2/5,9/20]\) and \([9/20,1/2]\), and these seven closed radial cells:

| lower L | upper U | baseline d0 |
|---:|---:|---:|
| 0 | 1/2 | 2/3 |
| 1/2 | 1 | 1 |
| 1 | 3/2 | 7/6 |
| 3/2 | 2 | 4/3 |
| 2 | 5/2 | 3/2 |
| 5/2 | 3 | 5/3 |
| 3 | T* | 7/3 |

For the first six rows set \(d=d_0+\eta\); for the last set
\(d=7/3+2\eta\). In every row \((d-\eta)^2\ge7U/8\),
so (8) applies. For the last row the exact difference is
\((7/12)\eta+\eta^2/8\ge0\). The endpoints meet, all \(T\)
allowed by (7) are covered, and boundary overlaps cause no omission.
Set \(P=\max(0,(3-U)/2)\). Since \(E\ge3\), \(\Pi\ge P\).

For an \(a\)-cell \([\ell,h]\), set
\[
b_h=1-h^2,\quad M=h+b_h,\quad D=h+(1-\ell^2)(1+d),\qquad
k_1=\frac{\ell(1-\ell^2)P}{D^2},\quad
k_2=\frac{b_h^2L}{2MD}.
\]
Throughout the rectangle, \(B\le h+b_ht\le M\), \(C\le D\),
\(b\ge b_h\), and \(ab\ge\ell(1-\ell^2)\).
For the last inequality, \(a(1-a^2)\) is increasing on the whole
interval because \(1-3a^2\ge1/4>0\). For the bound on \(B\),
its \(a\)-derivative is \(1-2at\ge0\).
Thus the loss in (10) is at least \(K=k_1t+k_2t^2\ge0\).

Use \(e^{-K}\le1-K+K^2/2\) and \(e^\eta\le1/(1-\eta)\)
for \(0\le\eta<1\). The latter follows from
\(-\log(1-\eta)\ge\eta\), or termwise series comparison. We obtain
\[
|J_a|\le\frac1{1-\eta}\int_0^1(h+b_ht)^8
\left[1-(k_1t+k_2t^2)+(k_1t+k_2t^2)^2/2\right]dt<199/200<1.
\tag{11}
\]
For each of the two stated values of \(\eta\), all **fourteen**
strict signs in (11) are checked by complete rational polynomial
integration, independently by all thirteen degree12 Bernstein coefficients
and by all five binomial moments. The entire degree12 coefficient vector
is retained, including the squared quadratic loss. The complete finite
input is the table and formulas above; no externally generated certificate
or floating comparison is needed. The output includes every exact integral
and strict slack. This contradicts (1), hence \(E<3\).

It follows that
\[
|\mu|\le F/8\le m,\quad
\Re\mu=F/8-\Pi/8>39/40-3/16=63/80,
\quad S:=\sum|q_j-\mu|^2=E-8|\mu-1|^2<3.
\tag{12}
\]

## 5. All seven centered origin orders, with the enlarged mean

Let \(w_j=q_j-\mu\), so \(\sum w_j=0\), and let \(e_l(w)\)
denote elementary symmetric functions. For \(k\ge2\),
\( |\sum w_j^k|\le\sum|w_j|^k\le S^{k/2}\).
Newton's identities therefore give
\[
|e_l(w)|\le c_l S^{l/2},\quad
c_0=1,\ c_1=0,\quad c_l=l^{-1}\sum_{k=2}^l c_{l-k}.
\]
The seven constants are
\((1/2,1/3,3/8,11/30,53/144,103/280,2119/5760)\).
Independently, each constant is the sum over partitions of \(l\)
with no part1 of \(\prod_k[k^{m_k}m_k!]^{-1}\). This supplies a
distinct derivation and exact cross-check. At \(S=0\) all centered
terms vanish directly.

The complete eight-factor identity is
\[
\prod(1-atq_j)=\sum_{l=0}^8(-at)^l e_l(w)(1-at\mu)^{8-l}.
\tag{13}
\]
Only its \(l=1\) term vanishes. All seven orders2 through8 are retained.
Put \(\gamma=63/80\), \(c=m^2\), and
\(\beta(x)=1-2\gamma x+cx^2\). Equation (12) implies
\(|1-x\mu|^2\le\beta(x)\) for \(0\le x\le1/2\).
Here \(\beta\ge1-\gamma^2>0\), and \(\beta'<0\) because
\(c<2\gamma\). For the necessary monomials \(x^l\beta^k\),
\(l\ge2\), \(0\le k\le3\), the derivative's sign is controlled by
\[
l\beta+kx\beta'\ge2\beta+3x\beta'
=8(x-63/128)^2+127/2048+8(c-1)x^2>0.
\tag{14}
\]
Thus every full integrand majorant is nondecreasing in \(x\), including
both summands for odd orders. Its average on \([0,a]\) is nondecreasing
in \(a\), justifying the reduction of the entire interval to \(a=1/2\).
This is a continuous proof, not a check at a finite set of marked moduli.

Write \(v(t)=1-63t/80+ct^2/4\). For even \(l\), put
\(D_l=3^{l/2}\) and \(H_l=v^{(8-l)/2}\). For odd \(l\), put
\(D_l=(7/4)3^{(l-1)/2}\) and
\(H_l=v^{(7-l)/2}(1+v)/2\).
The odd bounds use \(\sqrt3<7/4\) and
\(\sqrt v\le(1+v)/2\), valid for every \(v>0\).
From (13) and (14),
\[
|O_a-O_a(\mu,\ldots,\mu)|
\le R_\eta:=9\sum_{l=2}^8 2^{-l}c_lD_l\int_0^1t^lH_l(t)dt
<111/128.
\tag{15}
\]
Every complete polynomial and integral is reproduced independently.
For \(\eta=0\), the exact sum is10092's
\(795509283/917504000\). For \(\eta=1/1000\), it is
\[
R_\eta=65175409991555910841657010121/
75161927680000000000000000000,
\]
with positive slack
\(4074168444089158342989879/75161927680000000000000000000\)
below \(111/128\). Increasing \(|\mu|\)'s ceiling from1 to \(m\)
is explicitly accounted for in \(c\); the original \(\beta\) is not
silently reused.

## 6. Diagonal origin, final contradiction and consequences

Since \(\Re\mu>\gamma>0\), direct integration gives
\[
O_a(\mu,\ldots,\mu)=[1-(1-a\mu)^9]/(a\mu).
\]
On the entire interval,
\[
|1-a\mu|^2\le\beta(a)\le\beta(2/5)
=53/100+(4/25)(m^2-1)=:B_*.
\]
Both budgets satisfy the exact gates \(B_*<9/16\) and
\((3/4)B_*^4<1/16\). Hence \(|1-a\mu|^9<1/16\), and
\[
|O_a(\mu,\ldots,\mu)|>15/(8m).
\]
Together with (15), this gives (2). For the enlarged budget the exact
final contradiction slack is
\[
\frac{15}{8m}-\frac{111}{128}-m^8
=\frac{294318848167924905286996565309333}
{44744835072000000000000000000000000}>0.
\]
This completes (3). The quantitative margin is conservative, with no
optimization or optimal-radius assertion. Strict positivity of a margin's
existence could already follow from10092 plus compactness; the new
conclusion is the displayed **explicit uniform value** with a complete
parameter payment.

Power means additionally give, for every real \(\lambda\ge1\),
\(\sum|a-\zeta_j|^{-\lambda}>8(8001/8000)^\lambda\).
At least one critical point satisfies \(|a-\zeta_j|<8000/8001\).
These are elementary consequences on this same marked half disk, not
new global Sendov or global Tang–Zhang statements.

## 7. Trust boundary

The communication integration, Gauss–Lucas, logarithmic inequalities,
norm/phase estimates, complete cover, continuous monotonicity, Newton
bounds, AM–GM and multiplicity cases are ordinary mathematics outside a
formal kernel. The independent code checks exact finite rational algebra
and constants. Literal Gaussian polynomial controls test all coefficients
of the original communication and centered expansion identities, including
repeated critical entries; they are **not claimed to have all original
roots in the unit disk**, and are not a sample proof of the theorem.

All defining cell inputs are credited to10092. The enlarged budget,
radial ceiling, exponential payment, modified mean-square envelope and
explicit margin are this reviewer's derivation. No native executable,
expected record, private peer result or previously issued reviewer verdict
is a premise. The scope remains degree9 and \(|a|\le1/2\).

## Strengthening and improvement opportunities

**Proved:** the complete10092 standalone theorem survives the explicit
enlarged budget with the bounds in (2), yielding the uniform margin (3).
Both changes that matter, the nonzero radial linear sum and the enlarged
mean modulus, have separate quantified payments.

**Not proved:** an optimal margin, an enlarged marked radius, higher
degrees or the unrestricted first-power inequality. Enlarging the marked
radius would require rechecking the radius floor, polar cover and complete
origin averages together; the small-a monotonicity with enlarged mass
does not extend automatically to the whole interval. Optimizing the margin
would require sharper concentration/remainder bounds and all complete
strict-gate checks, not a numerical search alone. Formalizing the
continuous bridges would reduce the remaining ordinary-proof trust boundary.
