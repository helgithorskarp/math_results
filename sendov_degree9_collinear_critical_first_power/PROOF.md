# Degree-nine first power with a collinear critical set and distinguished root

Author: six-sendov-1, researcher. Date: 2026-09-29.

Let $p$ be a complex polynomial of degree nine, all of whose zeros lie in the closed unit disk. Write its critical points, with multiplicity, as $\zeta_1,\ldots,\zeta_8$. For a zero $a$ define

$$S_1(p,a)=\sum_{j=1}^8\frac1{|a-\zeta_j|},$$

interpreting a zero denominator as $+\infty$.

**Claim.** Suppose $a,\zeta_1,\ldots,\zeta_8$ lie on one affine line $L$. Then $S_1(p,a)\ge8$, strictly if $|a|<1$. More precisely, if $h=\operatorname{dist}(0,L)<1$, then

$$S_1(p,a)\ge\frac8{\sqrt{1-h^2}}. \tag{1}$$

Equality in the unit-disk bound $S_1=8$ holds exactly when $|a|=1$ and

$$p(z)=C(z^9-a^9)\quad\hbox{or}\quad p(z)=C(z-a)(z+a)^8,\qquad C\ne0. \tag{2}$$

The other polynomial zeros need not lie on $L$. A further corollary in Section 3 proves strict first power for arbitrary complex critical points whose reciprocal phase deviation is at most $(1-|a|)/2000$. These are structural cases of the first-power Tang-Zhang conjecture; they do not prove the general complex case. Boundary equality classification in (2) uses the [previous proved lemma](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/PROOF.md). All remaining parts are proved here. The finite positivity certificate below is checked by two distinct exact algorithms, without floating-point arithmetic.

## 1. Diameter normalization and the two classical identities

First suppose the critical points and $a$ are real. Multiply $p$ by a nonzero scalar to make it monic, and reflect the variable if necessary so $0\le a\le1$. If $p'(a)=0$ there is nothing to prove. Otherwise $a$ is simple; write its other zeros as $z_1,\ldots,z_8$ and put

$$q_j=\frac1{a-\zeta_j},\quad r_i=\frac1{a-z_i},\quad b=1-a^2.$$

The $q_j$ are nonzero real numbers. Gauss-Lucas gives $-1\le\zeta_j\le1$. Thus

$$|q_j|\ge l:=\frac1{1+a},\qquad q_j<0\Longrightarrow |q_j|\ge\frac1{1-a}\quad(a<1). \tag{3}$$

The first origin and polar identities, in the normalization used by [Tao](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/) and [Zhang, Lemma 3.1](https://arxiv.org/html/2609.19126), imply

$$O:=9\int_0^1\prod_{j=1}^8(1-atq_j)\,dt=\prod_{i=1}^8z_i\prod_{j=1}^8q_j,
\qquad |O|\le\prod_{j=1}^8|q_j|, \tag{4}$$

$$1\le\left|\int_0^1\prod_{j=1}^8(a+btq_j)\,dt\right|
\le\int_0^1\prod_{j=1}^8|a+btq_j|\,dt. \tag{5}$$

For completeness, differentiating
$p(a+s)/p'(a)=s\prod_i(1+sr_i)$ gives
$\prod_j(1+sq_j)=(s\prod_i(1+sr_i))'$ and hence
$e_k(q)=(k+1)e_k(r)$. Integrating at $s=-a$ and using
$p'(a)=9\prod_j(a-\zeta_j)$ gives (4) for $a>0$; for $a=0$ it follows directly from this derivative product and $p'(0)=\prod_i z_i$. Coefficient comparison also gives

$$\int_0^1\prod_j(a+btq_j)\,dt
=\prod_i(a+br_i)=\prod_i\frac{1-az_i}{a-z_i}.$$

Every factor on the right has modulus at least one, since
$|1-az_i|^2-|a-z_i|^2=(1-a^2)(1-|z_i|^2)\ge0$. This proves (5). These identities are prior work, not new claims.

We show that $S_1\le8$ is impossible when $a<1$.

## 2. Any negative coordinate contradicts the polar identity

Suppose $\sum_j|q_j|\le8$ and at least one $q_j$ is negative. From (3),

$$\frac1{1-a}+\frac7{1+a}\le8.$$

For $a>0$ this gives $a\le3/4$; $a=0$ is already in that interval. Write $k\ge1$ for the number of negative coordinates and $\mu=\frac18\sum_j|q_j|\le1$. If $q_j=-r<0$, then $br\ge1+a$, so the convex chord bound is

$$|a-brt|\le(1-t)a+t(br-a)=a+(br-2a)t.$$

For a positive coordinate the corresponding factor is exactly $a+b|q_j|t$. The chords are nonnegative on $0\le t\le1$. Their arithmetic mean is $a+(b\mu-ka/4)t$, also nonnegative. AM-GM and $k\ge1$ therefore give

$$\prod_j|a+btq_j|\le[a+(b\mu-ka/4)t]^8
\le[a+c(a)t]^8,\qquad c(a)=1-a^2-a/4. \tag{6}$$

On $[0,3/4]$, $c(a)>0$ and

$$\int_0^1[a+c(a)t]^8dt
=\frac{(a+c(a))^9-a^9}{9c(a)}.$$

The endpoint $a+c(a)=1+3a/4-a^2$ has its maximum at $a=3/8$, and $c$ is decreasing. Dropping $a^9$ gives the following exact upper bounds.

| Interval for $a$ | Upper bound for $a+c(a)$ | Lower bound for $c(a)$ | Upper bound for the integral |
|---|---:|---:|---:|
| $[0,1/2]$ | $73/64$ | $5/8$ | $58871586708267913/101330991615836160<1$ |
| $[1/2,5/8]$ | $9/8$ | $29/64$ | $43046721/60817408<1$ |
| $[5/8,3/4]$ | $69/64$ | $1/4$ | $3939120870619581/4503599627370496<1$ |

Thus (6) contradicts (5). Any hypothetical $S_1\le8$ at an interior real root must have all $q_j>0$.

## 3. A positive-coordinate origin inequality

The following purely real inequality is the main new finite reduction. For $0\le a<1$, any eight real numbers $q_j\ge1/(1+a)$ with $\sum_jq_j\le8$ satisfy

$$E_a(q):=9\int_0^1\prod_{j=1}^8(1-atq_j)\,dt-\prod_{j=1}^8q_j
\ge\frac{8(1-a^9)}{(1+a)^8}\ge\frac9{32}(1-a)>0. \tag{7}$$

**Reduction to eight profiles.** The domain is nonempty and compact. $E_a$ is symmetric and multiaffine, meaning it has degree at most one in each $q_j$ separately. Choose a global minimizer with the fewest coordinates strictly above $l=1/(1+a)$. Holding all but two such coordinates fixed, symmetry and multiaffinity give

$$A+B(q_i+q_j)+Cq_iq_j.$$

If $q_i\ne q_j$, varying the pair by $(q_i+t,q_j-t)$ in a small two-sided interval stays feasible. Stationarity forces $C(q_j-q_i)=0$, hence $C=0$. The expression is then constant along the entire fixed-sum pair segment. Moving one coordinate to $l$ gives another global minimizer with fewer coordinates above $l$, a contradiction. Consequently all coordinates above $l$ equal one number $x$.

Such a minimizer has $k$ coordinates equal to $l$ and $m=8-k$ equal to $x$, where $0\le k\le7$ and

$$l\le x\le\frac{8-kl}{m},\qquad
x=\frac{1+(8a/m)u}{1+a},\quad0\le u\le1. \tag{8}$$

The all-$l$ point is included by $k=0,u=0$. At $a=0$ the domain consists of that one point, and (8) still represents it.

Multiply the value of $E_a$ at this profile by $(1+a)^8$. It becomes the bivariate polynomial

$$P_k(a,u)=9\int_0^1(1+a-at)^k
\left(1+a-at\left(1+\frac{8a}{m}u\right)\right)^m dt
-\left(1+\frac{8a}{m}u\right)^m. \tag{9}$$

**Exact positivity certificate.** Set $d=16-k$ and $e=8-k$. With
$B_i^d(a)=\binom di a^i(1-a)^{d-i}$, write

$$P_k(a,u)=\sum_{i=0}^d\sum_{j=0}^e\beta^{(k)}_{ij}B_i^d(a)B_j^e(u). \tag{10}$$

All the rational coefficients are recorded in `certificate.json`. They have the following exact properties.

| $k$ | Degrees $(d,e)$ | Coefficients | Zero coefficients |
|---:|---:|---:|---:|
| 0 | (16,8) | 153 | $(16,8)$ |
| 1 | (15,7) | 128 | none |
| 2 | (14,6) | 105 | none |
| 3 | (13,5) | 84 | none |
| 4 | (12,4) | 65 | none |
| 5 | (11,3) | 48 | none |
| 6 | (10,2) | 33 | none |
| 7 | (9,1) | 20 | $(9,1)$ |

Every other coefficient is at least $8$, and $\beta^{(k)}_{0j}=8$ for every $j$. The following explicit formulas specify the certificate without relying on numerical computation. Expand (9) as

$$9\sum_{i=0}^k\sum_{j=0}^m
\frac{\binom ki\binom mj(-a)^{i+j}}{i+j+1}
(1+a)^{8-i-j}\left(1+\frac{8a}{m}u\right)^j
-\left(1+\frac{8a}{m}u\right)^m.$$

If its power coefficients are $c_{rs}$, the Bernstein coefficients are exactly

$$\beta_{ij}^{(k)}=\sum_{r\le i,\ s\le j}
c_{rs}\frac{\binom ir}{\binom dr}\frac{\binom js}{\binom es}. \tag{11}$$

`verify.py` regenerates these 636 fractions and compares every entry with the certificate. `verify_interpolation.py` uses a distinct algorithm: rational grid evaluation by multiplication of the eight linear factors in $t$, exact integration, and inversion of two Bernstein sampling matrices. It independently reconstructs and compares all 636 entries. Both checkers use only Python's standard library and rational arithmetic. They certify this finite algebraic step; the minimizer argument and geometric reductions are written mathematical proofs, not formalized code.

Because the Bernstein basis is nonnegative on the unit square and its sums equal one, $P_k\ge8$ for $1\le k\le6$. For $k=0,7$, its sole zero coefficient is the top-right one, giving

$$P_k(a,u)\ge8(1-a^{16-k}u^{8-k})\ge8(1-a^9).$$

Thus every profile has $P_k\ge8(1-a^9)$. This holds at a global minimizing profile and therefore throughout the domain. For the simpler linear lower bound in (7), put $v=(1-a)/(1+a)\ge0$. The binomial identity

$$\frac{8(1-a^9)}{(1+a)^8}
=\frac{1-a}{32}(9+84v^2+126v^4+36v^6+v^8)
\ge\frac9{32}(1-a)$$

finishes the proof of (7). Its polynomial form after clearing denominators is checked exactly by `verify.py`.

Return to the polynomial. With all $q_j>0$ and $S_1\le8$, (7) gives
$O>\prod_jq_j>0$. This contradicts $|O|\le\prod_jq_j$ in (4). Together with Section 2, this proves $S_1>8$ for every interior real distinguished root with real critical points.

**Complex reciprocal phase corollary.** Drop collinearity. Rotate an interior distinguished root to $a=|a|\in[0,1)$, and suppose all its critical reciprocals $q_j=(a-\zeta_j)^{-1}$ are finite. Then

$$\sum_{j=1}^8|q_j-|q_j||\le\frac{1-a}{2000}
\quad\Longrightarrow\quad S_1(p,a)>8. \tag{12}$$

No reality assumption on the critical points or other zeros is made in (12). To prove it, assume $S_1\le8$ and set $r_j=|q_j|$. Gauss-Lucas gives $r_j\ge1/(1+a)$, so the real inequality (7) applies to $r$. Write $\epsilon=\sum_j|q_j-r_j|$. Telescoping the products in (4), and using AM-GM on the other seven factors, gives

$$\left|\prod_j(1-atq_j)-\prod_j(1-atr_j)\right|
\le at\epsilon\left(1+\frac{8at}{7}\right)^7.$$

Indeed, each of those seven factors, whether it uses $q_k$ or $r_k$, has modulus at most $1+atr_k$, and their $r_k$ sum is at most eight. Consequently

$$|O(q)-O(r)|\le K_0\epsilon,\qquad
K_0=9\int_0^1t\left(1+\frac{8t}{7}\right)^7dt
=\frac{570801247}{1647086}<500.$$

Here $O(q)$ denotes the origin integral in (4), which is valid for complex reciprocals as well. The triangle inequality, (7), and (12)'s hypothesis imply

$$|O(q)|\ge O(r)-K_0\epsilon
>\prod_jr_j+\frac9{32}(1-a)-\frac14(1-a)
=\prod_jr_j+\frac1{32}(1-a),$$

contradicting (4). A critical point at $a$ already gives an infinite first-power sum. The numerical cone constant is conservative, with no sharpness claim.

## 4. Boundary and affine lines

For a simple boundary root, normalize it to $a=1$. The classical logarithmic-derivative identity is

$$\sum_j\frac1{1-\zeta_j}=2\sum_i\frac1{1-z_i}.$$

Since $\operatorname{Re}(1/(1-z_i))\ge1/2$ for $|z_i|\le1$, taking real parts and then the triangle inequality proves $S_1\ge8$. This boundary inequality does not require collinearity. The full degree-nine boundary equality classification is (2), proved in the [prior source, Section 7](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/PROOF.md). Conversely, the two families in (2) have reciprocal coordinates respectively $1/a$ eight times, or $1/(2a)$ seven times and $9/(2a)$ once. Both have $S_1=8$ and satisfy the collinear-critical hypothesis. No boundary equality is asserted for a multiple distinguished root.

Now let $L$ be any affine line as in the claim. Rotate so $L=\{x+ih:x\in\mathbb R\}$ with signed $h$ and translate by $-ih$. Normalize the transformed polynomial $P$ to be monic. Its critical points are real, so $P'$ has real coefficients. All positive-degree coefficients of $P$ are therefore real; because its distinguished root is real, its constant coefficient is also real. Thus its zero multiset is invariant under conjugation.

For a zero $w=x+iy$ of $P$, both $x+iy$ and $x-iy$ correspond to zeros of the original polynomial. The original unit-disk hypothesis gives

$$x^2+(h+y)^2\le1,\qquad x^2+(h-y)^2\le1.$$

Consequently

$$|w|^2\le1-h^2-2|h|\,|y|\le1-h^2.$$

If $|h|=1$, the line intersects the unit disk in a single point, so the distinguished root and every critical point coincide and $S_1=+\infty$. Otherwise $R=\sqrt{1-h^2}>0$. All zeros of $P$ lie in the disk of radius $R$. Scale its variable by $R$ and apply the proved real-root/real-critical case. Reciprocal distances scale by $1/R$, proving (1). If the original $|a|<1$, the translated real root has absolute value strictly less than $R$, giving strictness. If $h\ne0$, (1) is already strictly greater than eight. Equality in the unit-disk bound is therefore exactly the boundary classification (2).

By the power-mean inequality, the same hypotheses also imply
$\sum_j|a-\zeta_j|^{-\lambda}\ge8(1-h^2)^{-\lambda/2}$ for every $\lambda\ge1$. The exponent-one case is the substantive endpoint proved here.
