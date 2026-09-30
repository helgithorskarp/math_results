# Degree-nine first power on a monotone symmetry axis and under angular loss

Author: **six-sendov-1**, role **researcher**. Date: 2026-09-29–30.
Status: complete ordinary written proof with exact finite checks and an
explicit previously published input. Independent review of this contribution
is pending; no formalization or historical-priority claim is made.

Let $p$ have degree nine and all its zeros in the closed unit disk. Count
its eight critical points $\zeta_j$ with multiplicity and put

$$S_1(p,a)=\sum_{j=1}^8|a-\zeta_j|^{-1}$$

at a zero $a$, with a zero denominator interpreted as infinity.

**Monotone-axis case.** If $p$ is real up to multiplication by a nonzero
constant, $a$ is real, and $p$ is monotone on the real segment joining $0$
to $a$, then $S_1(p,a)\ge8$, strictly when $|a|<1$. Monotonicity means
that, for a real representative $P$, $P'(x)P'(a)\ge0$ throughout that
segment; if $P'(a)=0$ the sum is already infinite. Complex zeros and
complex critical points are allowed. Equality $S_1=8$ in this class holds
exactly for $|a|=1$ and $p(z)=C(z^9-a^9)$.

There is an affine version. Let $L$ contain $a$ and let $c$ be the
perpendicular projection of $0$ onto $L$. Suppose the zero multiset of $p$
is invariant under reflection in $L$ and the monic polynomial obtained by moving
$c$ to $0$ and $L$ to the real axis is monotone between $0$ and the
transformed root. If $h=\operatorname{dist}(0,L)<1$, then

$$S_1(p,a)\ge\frac8{\sqrt{1-h^2}}, \tag{1}$$

strictly if $|a|<1$. If $h=1$ the sum is infinite.

**Angular-loss case.** Rotate an interior root to $a=|a|\in[0,1)$, and
rotate the critical points with it. If all reciprocals are finite, define

$$q_j=(a-\zeta_j)^{-1},\quad r_j=|q_j|,\quad
d_j=r_j-\operatorname{Re}q_j,\quad A=\sum_jd_j. $$

Then

$$A\le\frac{1-a}{2400}\quad\Longrightarrow\quad S_1(p,a)>8. \tag{2}$$

In particular, with principal arguments $\theta_j=\arg q_j$,

$$\max_j|\theta_j|\le\sqrt{\frac{1-a}{9600}}
\quad\Longrightarrow\quad S_1(p,a)>8. \tag{3}$$

The signed and coordinate-weighted necessary loss budgets in Section 4
retain more information than these conservative constants. These are cases
of the first-power Tang--Zhang endpoint, not a proof of the full conjecture.

## 1. Published input and classical identities

We use the positive-coordinate origin inequality proved in
[the preceding source, Section 3](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_first_power/PROOF.md),
source commit `177818bdbd7e23f16ec46bacfc3077d7a22a8aca`, graph lemma
`bafkreihcaireletdhn563ajzos46pfqtjeha3iv3ceg5x4i33qu62eilw4`:
for $0\le a<1$, $r_j\ge1/(1+a)$, and $\sum_jr_j\le8$,

$$O_a(r)-\prod_jr_j\ge m(a):=\frac{8(1-a^9)}{(1+a)^8}
\ge\frac9{32}(1-a)>0,
\qquad O_a(v)=9\int_0^1\prod_j(1-atv_j)\,dt. \tag{4}$$

Its symmetric multiaffine minimizer argument reduces to eight profiles.
All 636 rational Bernstein coefficients are independently reconstructed by
two different exact algorithms in that source. Both checkers were replayed
for this contribution. A concurrent
[independent review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_review3/README.md),
source `18c89c2ca1ffbbfc173867ddace5b1c82c5e7d6d`, confirms the complete input
and independently reconstructs the same certificate by direct tensor
Bernstein multiplication. The present extension has not been independently
reviewed.

After monic normalization and rotation to $a\in[0,1)$, a finite sum makes
$a$ a simple zero. Write the other eight zeros as $z_i$. Gauss--Lucas gives
$r_j\ge1/(1+a)$. The classical origin and polar identities give

$$O_a(q)=\prod_i z_i\prod_jq_j,\qquad |O_a(q)|\le\prod_jr_j, \tag{5}$$

$$1\le\int_0^1\prod_j|a+(1-a^2)tq_j|\,dt. \tag{6}$$

These follow by differentiating and integrating the root factorization;
see [Tao, Lemma 6](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
and [Zhang, Lemma 3.1](https://arxiv.org/html/2609.19126).
At $a=0$, (4)--(5) exclude $S_1\le8$ without any additional premise, so
below the nontrivial arguments assume $0<a<1$.

## 2. One negative real reciprocal suffices, even with other complex points

Assume $S_1\le8$ and one $q_j=-r$ is real and negative. Its critical point
is real and lies to the right of $a$, so $r\ge1/(1-a)$. Together with the
seven lower bounds $1/(1+a)$ this gives $a\le3/4$.
Put $b=1-a^2$. Since $br\ge1+a$, convexity yields the nonnegative chord

$$|a-brt|\le a+(br-2a)t\qquad(0\le t\le1).$$

For every other coordinate, complex or real, the triangle inequality gives
$|a+btq_i|\le a+btr_i$. AM--GM on these eight nonnegative bounds implies

$$\prod_j|a+btq_j|\le[a+(1-a^2-a/4)t]^8. \tag{7}$$

The preceding source checked that this integral is less than one on
$[0,3/4]$. Its three rational upper bounds, respectively on
$[0,1/2]$, $[1/2,5/8]$, $[5/8,3/4]$, are

$$\frac{58871586708267913}{101330991615836160},\qquad
\frac{43046721}{60817408},\qquad
\frac{3939120870619581}{4503599627370496},$$

all strictly less than one. This contradicts (6). The extension here is
that the remaining coordinates need not be real. Consequently a critical
point on the real ray $(a,1]$ already ensures $S_1>8$.

## 3. Conjugate pairs and the monotone-axis case

Normalize a real polynomial to be monic and reflect the variable if needed
so $0<a<1$. Assume $S_1\le8$. Section 2 rules out all real critical points
larger than $a$; a critical point at $a$ would make the sum infinite.
Every real critical point in $(0,a)$ has even multiplicity, since the
derivative has a fixed sign on $[0,a]$. Pair these equal coordinates.
Every nonreal critical point, and therefore its reciprocal, has a conjugate
partner of the same multiplicity. Leave the real critical points in
$[-1,0]$ as individual coordinates. For an individual coordinate one has
$0<q_j=r_j\le1/a$, hence $1-atq_j\ge0$ on $[0,1]$.

For a conjugate pair $q,\overline q$, writing $r=|q|$, we have exactly

$$ (1-atq)(1-at\overline q)
=(1-atr)^2+2at(r-\operatorname{Re}q)\ge(1-atr)^2\ge0. \tag{8}$$

The same formula applies to the paired equal positive real coordinates,
with zero added term. Multiply (8) over all pairs and the nonnegative
individual factors. This proves the pointwise comparison

$$\prod_j(1-atq_j)\ge\prod_j(1-atr_j)\ge0\qquad(0\le t\le1). \tag{9}$$

Thus $O_a(q)\ge O_a(r)>\prod_jr_j$ by (4), contradicting (5). This
establishes strictness for every interior root in the stated monotone case.

At $|a|=1$ the usual reciprocal other-root identity proves $S_1\ge8$.
The previously proved degree-nine boundary classification
[Section 7](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/PROOF.md)
gives only $C(z^9-a^9)$ and $C(z-a)(z+a)^8$. After normalization $a=1$,
the latter has derivative $(z+1)^7(9z-7)$ and is not monotone on $[0,1]$;
the former is monotone there. This proves the equality assertion.

For (1), rotate $L$ to $\operatorname{Im}z=h$ and translate by $-ih$.
The transformed polynomial is real up to a scalar. Conjugate transformed
zeros $w=x\pm iy$ correspond to original disk zeros, so

$$|w|^2\le1-h^2-2|h||y|\le1-h^2.$$

All transformed zeros therefore lie in a disk of radius
$R=\sqrt{1-h^2}$. Scale by $R$, retain monotonicity along the real
segment, and apply the result just proved. Distances scale by $R$.
If $|a|<1$, the real transformed root has modulus strictly less than $R$.
If $h=1$, reflection and disk containment force every zero to the unique
point where $L$ meets the disk, so the sum is infinite.

## 4. Signed and weighted angular loss

This part does not assume conjugate symmetry. Under a hypothetical
$S_1\le8$ put

$$\Delta_k=e_k(r)-\operatorname{Re}e_k(q)\ge0\quad(1\le k\le8),
\qquad \Delta_1=A.$$

For each $k$-subset, telescoping its unit phases and Cauchy--Schwarz give
$1-\cos(\sum\theta_j)\le k\sum(1-\cos\theta_j)$. This is standard
machinery, already used in
[six-sendov-2's effective-boundary proof, Section 5](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_effective_boundary_first_power/PROOF.md).
Multiplying by the radial product and summing all subsets yields the
coordinate-weighted bound

$$0\le\Delta_k\le k\sum_{i=1}^8d_i e_{k-1}(r_{\widehat i}), \tag{10}$$

where the hat omits coordinate $i$. Maclaurin further gives

$$e_{k-1}(r_{\widehat i})\le\binom7{k-1}
\left(\frac{8-r_i}{7}\right)^{k-1}
\le\binom7{k-1}\left(\frac{15}{14}\right)^{k-1}. \tag{11}$$

The last step uses $r_i\ge1/(1+a)\ge1/2$; all sums and bases here are
nonnegative under $\sum r_i\le8$.

Expand the origin integral exactly. If

$$G_a(q)=9\sum_{\substack{2\le k\le8\\k\ {
m even}}}
\frac{a^k\Delta_k}{k+1}
-9\sum_{\substack{1\le k\le7\\k\ {
m odd}}}
\frac{a^k\Delta_k}{k+1},$$

then $G_a(q)=O_a(r)-\operatorname{Re}O_a(q)$. Equations (4)--(5) force
the **signed necessary budget**

$$m(a)\le G_a(q). \tag{12}$$

Odd angular losses help the estimate; bounding all terms by their absolute
values loses this fact. Retaining $\Delta_1$ and dropping only the other
helpful odd terms gives the **weighted necessary budget**

$$m(a)\le G_a(q)\le\sum_i\left(C_i(a,r)-\frac{9a}{2}\right)d_i,
\quad C_i(a,r)=9\sum_{k=2,4,6,8}\frac{k a^k}{k+1}
e_{k-1}(r_{\widehat i}). \tag{13}$$

The first bound in (11) retains the coupling between a coordinate's angular
loss and the radial budget of the other seven. It can be used instead of
the following uniform constant:

$$C_i(a,r)\le K_*:=9\sum_{k=2,4,6,8}\frac{k}{k+1}
\binom7{k-1}\left(\frac{15}{14}\right)^{k-1}
=\frac{3930935355}{6588344}<600. \tag{14}$$

If (2) held under $S_1\le8$, then (13)--(14) would give
$G_a(q)<600A\le(1-a)/4<m(a)$, a contradiction. If $A=0$, directly
$G_a(q)=0<m(a)$, so the strict comparison with $600A$ is unnecessary.
Equivalently, every hypothetical interior failure must have
$A>(1-a)/2400$ and satisfy the stronger signed and weighted budgets.

For (3), $1-\cos\theta\le\theta^2/2$ and the failure budget imply
$A\le4\max_j\theta_j^2\le(1-a)/2400$. This proves the sector case.
For comparison, the preceding source used
$\epsilon=\sum_j|q_j-r_j|\le(1-a)/2000$. Since

$$A=\frac12\sum_j\frac{|q_j-r_j|^2}{r_j}
\le\sum_j|q_j-r_j|^2\le\epsilon^2,$$

that entire preceding phase condition is contained in (2). The present
sector has half-angle proportional to $\sqrt{1-a}$. The concurrent review
already proves a quadratic phase condition
$\epsilon^2\le(1-a)/1250$, by integral Taylor bounds; the order enlargement
is therefore not claimed as new here. The contribution of (10)--(14) is the
signed parity information and the radial-weighted loss $A$, with a separately
proved sufficient region. Neither region is asserted to contain the other.

## 5. Exact scope controls and the literature boundary

The elementary product-distance criterion already appears in
[marius.cobzarenco+maths's August 22 comment on Tao's exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/):
$\prod_i|a-z_i|\le9$ gives $S_1\ge8$ by the derivative product and AM--GM.
It is prior work. In particular, this contribution does not claim to supply
the first open region of configurations for the endpoint.

The following explicit monotone family is outside that product region.
For $0<e\le10^{-6}$ let

$$P_e(z)=z^9-1-e(z^8-z)+2e(z^7-z^2),\quad
R=1-e/100,\quad p_e(z)=R^9P_e(z/R). \tag{15}$$

On the unit circle, $P_e(e^{i\theta})/(2i e^{9i\theta/2})$ is the real
function

$$\sin(9\theta/2)-e\sin(7\theta/2)+2e\sin(5\theta/2).$$

On each of the nine disjoint arcs centered at $2\pi k/9$ with half-width
$\pi/18$, the first term has opposite endpoint signs and magnitude
$1/\sqrt2$, whereas the perturbation has magnitude at most
$3e<1/2$. The intermediate value theorem yields nine distinct unit-circle
zeros, including $1$. Degree nine accounts for every zero. Thus all zeros
of $p_e$ have modulus $R<1$, and $a=R$ is one of them.

Exactly,
$P'_e(x)=9x^8+e(1-4x+14x^6-8x^7)>0$ for every real $x$.
For $x\le0$ positivity is termwise. On $[0,1/5]$ the bracket is at least
$1/5-8/5^7>0$. On $[1/5,1]$ the whole derivative is at least
$9/5^8-11e\ge301/25000000>0$. For $x\ge1$, group
$9x^8-8ex^7>0$ and $1-4x+14x^6>0$.
So the new monotone case applies. Nevertheless Bernoulli's inequality gives

$$\prod_i|a-z_i|=p'_e(R)=R^8(9+3e)
\ge9+\frac{57}{25}e-\frac6{25}e^2>9. \tag{16}$$

This rigorously separates (15) from the published product sufficient
condition. At $e=10^{-6}$ a critical point has modulus greater than
$99/1000$, by $\prod_j|\zeta_j|=R^8e/9$; the family is not confined to
the tiny clustered-critical region. Its derivative has no real zero, while
its critical-point average is $R e/9\ne R$, so the critical set and chosen
root cannot all lie on one line.

The weighted criterion has actual disk-root examples outside the concurrent
review's quadratic sufficient region.
Use the previously proved small-parameter family
[six-sendov-2, Section 5](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_boundary_stability/proof.md),
whose critical points are six zeros and $3u\pm i\sqrt u$ and whose
distinguished zero is $1$. Scale inward by $1-\delta$ and set
$u=\delta/4000$. Its original roots remain in the disk for sufficiently
small positive $\delta$. Put $B=1-5u+9u^2$ and $R=1-\delta$. Exactly,

$$A=\frac2R\left(B^{-1/2}-\frac{1-3u}{B}\right),\qquad
\epsilon^2=\frac8{R^2\sqrt B}
\left(B^{-1/2}-\frac{1-3u}{B}\right).$$

The bracket is $u/2+O(u^2)$, so $A\sim\delta/4000$ and
$\epsilon^2\sim\delta/1000$.
Thus (2) holds while both $\epsilon^2\le\delta/1250$ and the older
$\epsilon\le\delta/2000$ fail for sufficiently small $\delta$.
This is a scope separation, not a disproof of either sufficient condition.
It credits the existing root-containment
construction; no new numerical admissibility interval is asserted.

The remaining generic complex phase range and reflection-symmetric
polynomials with sign changes on the relevant segment are not settled by
the present comparison. Pairing alone does not justify (9) in the presence
of an unpaired real factor that becomes negative.

## Verification boundary

`verify.py` checks the full formal origin expansion by comparing iterative
polynomial multiplication against direct subset expansion (all 6561 complex
monomials), the conjugate-pair and phase-energy polynomial identities, exact
constants, polar bounds, example coefficients, monotonicity margins and the
product-distance separation. It rejects three altered identities/constants.
It uses only standard-library exact integer/rational arithmetic.

The universal arguments are ordinary written mathematics: Gauss--Lucas,
Maclaurin, the communication identities, fixed-sign multiplicities,
pairwise comparison, the phase telescoping inequality, the intermediate
value theorem and the previously proved origin gap. No floating root
search, solver, exhaustive polynomial enumeration, private data, omitted
large certificate or proof-assistant certification is used.
