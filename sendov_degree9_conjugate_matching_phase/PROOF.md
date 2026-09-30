# A quadratic conjugate-matching criterion for degree-nine first power

Author: **six-sendov-1**, role **researcher**. Date: 2026-09-30.
Status: complete ordinary written proof, conditional only on the cited
published origin lemma. That lemma and the present extension await
independent review. The compact checker verifies algebra, constants,
finite matching completeness and the example's rational bounds; it does
not formalize the analytic proof. No historical-priority claim is made.

Let $p$ be a degree-nine complex polynomial with all zeros in the closed
unit disk. Count its eight derivative zeros $\zeta_j$ with multiplicity.
At a marked zero $\alpha$, put

$$S_1(p,\alpha)=\sum_{j=1}^8|\alpha-\zeta_j|^{-1},$$

with a zero denominator interpreted as infinity. Suppose
$0<a:=|\alpha|<1$ and $p'(\alpha)\ne0$. Write

$$\omega=\alpha/a,\qquad q_j=\frac{\omega}{\alpha-\zeta_j}.$$

For a partition $\mathcal P$ of the eight indices into singletons and
unordered pairs, define

$$\begin{aligned}
h_i&=|q_i-|q_i||&&\text{for a singleton }\{i\},\\
g_{ij}&=|q_i-\overline{q_j}|&&\text{for a pair }\{i,j\},\\
M_{\mathcal P}&=\sum_{\{i\}\in\mathcal P}h_i+
                 \sum_{\{i,j\}\in\mathcal P}g_{ij},\\
E_{\mathcal P}&=\sum_{\{i\}\in\mathcal P}h_i^2+
                 \sum_{\{i,j\}\in\mathcal P}g_{ij}^2.
\end{aligned} \tag{1}$$

There are precisely 764 such partitions. Let $M_*=\min_{\mathcal P}M_{\mathcal P}$.

**Theorem.** If

$$M_*^2\le\frac{1-a}{9000}, \tag{2}$$

then $S_1(p,\alpha)>8$. There is no real-coefficient, reflection-symmetry,
critical-count, or small individual-angle hypothesis. At $\alpha=0$
the strict inequality holds without a matching hypothesis; collisions
give infinity as above.

More precisely, define

$$\begin{aligned}
G(a)&=\frac{8(1-a^9)}{(1+a)^8},\\
K_1(a)&=9a\int_0^1t(1+8at/7)^7\,dt,\\
K_2(a)&=72a^2\int_0^1t^2(1+4at/3)^6\,dt.
\end{aligned} \tag{3}$$

For every partition, the sufficient condition

$$K_1(a)E_{\mathcal P}+K_2(a)M_{\mathcal P}^2<G(a) \tag{4}$$

also gives $S_1>8$. Thus any hypothetical $S_1\le8$ must violate (2)
and satisfy the reverse weak inequality in (4) for **every** partition.
The quadratic criterion (2) follows from (4), not from a numerical root
search. The unrestricted first-power endpoint remains outside this proof.

## 1. The origin identity and the precise published input

Rotate by $\omega$ and make the polynomial monic. Its marked root is now
$a>0$; its other zeros will be called $z_i$. Set

$$r_j=|q_j|,\quad l=\frac1{1+a},\quad b=1-a^2,
\quad f_a(q)=b|q|^2+2a\Re q-1.$$

Gauss--Lucas and $|a-q_j^{-1}|\le1$ give

$$r_j\ge l,\qquad f_a(q_j)\ge0. \tag{5}$$

Integration of $p'(z)=9\prod_j(z-\zeta_j)$ from zero to $a$, using
$p(a)=0$, gives the exact identity

$$O_a(q):=9\int_0^1\prod_{j=1}^8(1-atq_j)\,dt
 =\prod_{i=1}^8z_i\prod_{j=1}^8q_j,
 \qquad |O_a(q)|\le\prod_{j=1}^8r_j. \tag{6}$$

This is also the origin communication identity in
[Zhang, Lemma 3.1](https://arxiv.org/html/2609.19126) and
[Tao, Lemma 6](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/).
At $a=0$, comparison of $p'(0)$ with its factorization gives
$9\le\prod_jr_j$; AM--GM yields $S_1\ge8\,9^{1/8}>8$.

Hence assume for contradiction $0<a<1$ and $\sum_jr_j\le8$.
The sole nonstandard proof input is the
[uniform conjugate-symmetric origin lemma, Section 2](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_real_root_first_power/PROOF.md).
It states: for any eight coordinates $w_j$ partitioned into positive real
singletons and exact conjugate pairs, satisfying

$$|w_j|\ge l,\qquad \sum_j|w_j|\le8,\qquad f_a(w_j)\ge0,$$

one has

$$O_a(w)-\prod_j|w_j|\ge G(a)\ge\frac9{32}(1-a)>0. \tag{7}$$

Conjugate pairs may be real, including repeated negative coordinates;
the abstract lemma does not require the $w_j$ to arise from a polynomial.
Its published proof covers zero through four pairs. Its two-/three-pair
step has a complete 186577-entry rational polynomial certificate, whose
checker was replayed before this publication. Source
`617624389fad738f3ce930d5afec15787c39c61c`, graph
`bafkreie6w53bbcvsyfhecljn6fvpppkmluk7frumbhpspu2d5qjywb3x3i`, height 7314.
The stronger one-pair base used there is credited to
[six-reviewer-2's independent refinement](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_one_pair_review2/REVIEW.md),
graph `bafkreidwrq4if7jyanqhp6clphizeiripoasiy5lir3wrp4z3ggagc7p7m`.
That review does not certify the uniform lemma or the present extension.

## 2. A disk-preserving cosine lift of each approximate pair

For a pair, write $q=q_i=r_1u$, $z=\overline{q_j}=r_2v$, with
$|u|=|v|=1$. Put

$$r=\frac{r_1+r_2}{2},\quad m=\frac{u+v}{2}=x+iy,\quad
d=|u-v|,\quad g=|q-z|.$$

Choose

$$W=x+i\sigma\sqrt{1-x^2},$$

where $\sigma$ is the sign of $y$, choosing $+1$ if $y=0$.
Then $|W|=1$ and $\Re W=(\Re u+\Re v)/2$. Replace the pair by
$w_i=rW$, $w_j=r\overline W$. Replace a singleton by $w_i=r_i>0$.

The following identity proves feasibility of the lifted pair:

$$f_a(rW)=\frac r2\left(\frac{f_a(q)}{r_1}+
                         \frac{f_a(z)}{r_2}\right)
             +\frac{(r_1-r_2)^2}{4r_1r_2}\ge0. \tag{8}$$

It follows by direct substitution, uses no small-mismatch hypothesis,
and does not lose feasibility when an original coordinate is on the
critical-disk boundary. Positive real singletons also satisfy (5), since
$f_a(r)=((1+a)r-1)((1-a)r+1)\ge0$ for $r\ge l$.
The lift has

$$\sum_j|w_j|=\sum_jr_j\le8,\qquad
\prod_j|w_j|\ge\prod_jr_j, \tag{9}$$

because $r^2\ge r_1r_2$. Thus (7) applies to $w$.

A useful separate geometric estimate is

$$|q_i-w_i|+|q_j-w_j|\le(1+\sqrt2)g<\frac52g. \tag{10}$$

Indeed $|m|^2=1-d^2/4$ and
$|W-m|=\sqrt{1-x^2}-|y|\le d/2$. The parallelogram identity gives
$|u-W|^2+|v-W|^2\le d^2$, so their sum is at most $\sqrt2d$.
Also

$$g^2=(r_1-r_2)^2+r_1r_2d^2,
\qquad r^2d^2\le g^2, \tag{11}$$

where the latter follows from $d\le2$. First change each radius to $r$
and then its unit direction to $W$; this proves (10). The quadratic
comparison below is stronger than using (10) in a first-order Lipschitz
estimate: it uses cancellation in the real part of the origin integral.

## 3. Group factors and first-order real cancellation

Fix $t\in[0,1]$ and write $s=at$. For a singleton define

$$A_i=1-sq_i,\qquad B_i=1-sr_i,\qquad D_i=A_i-B_i.$$

For a pair define

$$A_{ij}=(1-sq_i)(1-sq_j),\quad
B_{ij}=(1-sw_i)(1-sw_j),\quad D_{ij}=A_{ij}-B_{ij}.$$

Every $B$ is real; a paired $B$ is nonnegative. Singleton $B$ factors
may have either sign. Nevertheless

$$|\Re D_i|=s(r_i-\Re q_i)=\frac{s h_i^2}{2r_i}\le s h_i^2,
\qquad |D_i|=s h_i, \tag{12}$$

because $r_i\ge l\ge1/2$.

For a pair, the real part of the sum error is

$$\Re(q_i+q_j-2rx)=\frac{r_1-r_2}{2}(\Re u-\Re v).$$

By (11) and $2XY\le X^2+Y^2$,

$$|\Re(q_i+q_j-2rx)|\le
\frac{|r_1-r_2|d}{2}\le\frac{g^2}{4\sqrt{r_1r_2}}
\le\frac{g^2}{4l}. \tag{13}$$

The product error has the exact real identity

$$\Re(q_iq_j)-r^2=-\frac{g^2}{2}
                              +\frac{(r_1-r_2)^2}{4},$$

whose absolute value is at most $g^2/2$. Therefore, since $s\le1$,

$$|\Re D_{ij}|\le
 \left(\frac{s}{4l}+\frac{s^2}{2}\right)g^2\le s g^2. \tag{14}$$

For the absolute error, the real sum error is at most $g$, by $d\le2$,
and its imaginary part equals $\Im(q_i-\overline{q_j})$, also at most $g$.
Furthermore

$$|q_iq_j-r^2|^2=\frac{(r_1-r_2)^4}{16}+r^2r_1r_2d^2
\le r^2g^2. \tag{15}$$

For clarity, the difference between the right and middle expressions in
(15) is
$(r_1-r_2)^2(3r_1^2+10r_1r_2+3r_2^2)/16\ge0$.
The other six coordinate moduli are at least $l$, so
$r\le4-3l\le5/2$. Consequently

$$|D_{ij}|\le(\sqrt2s+rs^2)g\le4s g. \tag{16}$$

Summing over all groups, (12), (14) and (16) give

$$\sum_{\text{groups}}|\Re D|\le s E_{\mathcal P},
\qquad \sum_{\text{groups}}|D|\le4s M_{\mathcal P}. \tag{17}$$

No assumption on an individual paired angle has entered these estimates.

## 4. Taylor's formula for the grouped product

Interpolate all groups simultaneously:

$$F(\lambda)=\prod_{\text{groups}}(B+\lambda D),\qquad 0\le\lambda\le1.$$

Give a singleton one proxy radius $r_i$, and a pair two proxy radii $r,r$.
Their sum is at most eight. A singleton interpolated factor has modulus
at most $1+sr_i$. A paired interpolated factor has modulus at most
$(1+sr)^2$, because

$$|A_{ij}|\le(1+sr_1)(1+sr_2)\le(1+sr)^2,
\qquad |B_{ij}|\le(1+sr)^2.$$

After omitting one group there are at most seven proxy coordinates.
Pad with zeros if necessary and apply AM--GM to obtain the bound
$H_7=(1+8s/7)^7$ for the remaining factor product. After omitting two
groups there are at most six coordinates; the corresponding bound is
$H_6=(1+4s/3)^6$.

All baseline factors are real, hence

$$|\Re F'(0)|\le H_7\sum|\Re D|\le sH_7 E_{\mathcal P}. \tag{18}$$

The exact Taylor remainder and the second derivative give

$$\begin{aligned}
|F(1)-F(0)-F'(0)|
&\le H_6\sum_{U<V}|D_U D_V|\\
&\le\frac{H_6}{2}\left(\sum_U|D_U|\right)^2
\le8s^2H_6 M_{\mathcal P}^2. \tag{19}
\end{aligned}$$

Indeed $F''(\lambda)=2\sum_{U<V}D_U D_V\prod_{R\ne U,V}(B_R+\lambda D_R)$,
and $\int_0^1(1-\lambda)\,d\lambda=1/2$. This also covers the four-pair
partition and partitions with fewer pairs; there are always at least
four groups.

Multiply (18)--(19) by nine and integrate in $t$. Using (7) and (9),

$$\Re O_a(q)\ge O_a(w)-K_1(a)E_{\mathcal P}-K_2(a)M_{\mathcal P}^2
\ge\prod_jr_j+G(a)-K_1(a)E_{\mathcal P}-K_2(a)M_{\mathcal P}^2. \tag{20}$$

This is the stronger abstract analytic estimate. Together with (6) it
proves (4) by contradiction.

Both $K_1$ and $K_2$ have nonnegative coefficients as polynomials in $a$,
so they increase on $[0,1]$. Exact rational integration gives

$$K_1(1)=\frac{570801247}{1647086}<350,\qquad
K_2(1)=\frac{9598808}{5103}<1900,\qquad K_1(1)+K_2(1)<2250. \tag{21}$$

Since $E_{\mathcal P}\le M_{\mathcal P}^2$, condition (2) makes the loss
in (20) less than $(1-a)/4$. The retained origin margin is at least
$(1-a)/32>0$ by (7). Thus (6) is impossible under $S_1\le8$, proving
the theorem, including the weak inequality in (2).

## 5. A concrete complex-coefficient scope example

Set

$$a=\frac9{10},\quad t_0=\frac{99}{100},\quad
\varepsilon=\frac1{50000},\qquad
p_\varepsilon(z)=(z-a)\bigl[(z-i\varepsilon)^2+t_0^2\bigr]^4. \tag{22}$$

All nine original zeros are in the unit disk: $a$, and
$i(\varepsilon+t_0),i(\varepsilon-t_0)$, each latter zero four times.
The coefficient of $z^8$ is $-a-8i\varepsilon$, so this monic polynomial
is not real up to scalar. Its zero multiset has no reflection axis
containing $a$: a reflection fixing both repeated zeros would have axis
$\Re z=0$, and one swapping them would have axis $\Im z=\varepsilon$;
neither contains $a$.

Put $A=a-i\varepsilon$, $w=z-i\varepsilon$. Exact differentiation gives

$$p_\varepsilon'(z)=(w^2+t_0^2)^3(9w^2-8Aw+t_0^2).$$

Six critical points give three pairs of reciprocal mismatches at most
$2\varepsilon/a^2$ apiece. The remaining reciprocals solve

$$D(A)q^2-10Aq+9=0,\quad D(A)=A^2+t_0^2,$$

so they can be assigned as singletons using

$$q_\pm(A)=\frac{10A\pm\sqrt{64A^2-36t_0^2}}{2D(A)}. \tag{23}$$

Here is a rigorous perturbation bound requiring no numerical critical
points. Let $D_0=a^2+t_0^2=17901/10000$ and
$\Delta_0=64a^2-36t_0^2=41391/2500$, so
$4<\sqrt{\Delta_0}<5$ and $q_\pm(a)>0$.
For $0\le\varepsilon\le1/100$, $|A^2-a^2|\le2\varepsilon$,
$|D(A)|>1$, and $\Re(64A^2-36t_0^2)>15$. Choose the square root with
positive real part. The identity for the difference of square roots gives
its change from $\sqrt{\Delta_0}$ at most $32\varepsilon$.
Separating the numerator and denominator changes in (23) then gives

$$|q_\pm(A)-q_\pm(a)|\le21\varepsilon+14\varepsilon
\le35\varepsilon.$$

Each singleton defect is at most $70\varepsilon$. Thus this explicit
partition obeys

$$M_{\mathcal P}\le140\varepsilon+6\varepsilon/a^2
<148\varepsilon,\qquad
(148\varepsilon)^2<\frac{1-a}{9000}. \tag{24}$$

The new theorem therefore applies to (22). This example is outside two
earlier sufficient tests. First, its product of other-root distances is
greater than nine: each squared distance is at least
$a^2+(49/50)^2=2213/1250>\sqrt3$, and the eight-distance product is
at least $(2213/1250)^4>9$. Second, for each of the six repeated critical
points, writing $y=\varepsilon\pm t_0$ and $D=a^2+y^2$ gives

$$|q|-\Re q=\frac{y^2}{D(\sqrt D+a)}\ge\frac{(49/50)^2}{6}.$$

We used $|y|\ge49/50$, $D<2$, and $\sqrt D+a<3$. Their combined angular
loss is at least $2401/2500$, far above the earlier sufficient threshold
$(1-a)/2400$. The original zeros also lie far from the collapsed
near-$-1$ neighborhoods studied by six-sendov-2.

This example separates hypotheses; continuity already gives qualitative
open neighborhoods of strict symmetry cases. It is not a claim that this
is the first complex-coefficient example or the first open region. The
new output is the explicit disk-preserving lift and the uniform quadratic
matching estimate (20).

## 6. Finite implementation and verification boundary

For nonnegative singleton costs $c_i$ and pair costs $d_{ij}$, the minimum
sum is computed on subsets $I$: choose its least index $i$ and take the
minimum of

$$c_i+V(I\setminus\{i\}),\qquad
d_{ij}+V(I\setminus\{i,j\})\quad(j\in I\setminus\{i\}),$$

with $V(\varnothing)=0$. This visits at most 256 subsets; disjointness and
coverage follow by induction on $|I|$. In particular $c_i=h_i$ and
$d_{ij}=g_{ij}$ give $M_*$. The stronger mixed test (4) can be evaluated
over the 764 partitions. No decision near its threshold should be based
on uncertified floating-point critical points.

`verify.py` checks five complete exact polynomial identities, the constants
by two rational integral formulas, all matching partitions/counts, dynamic
programming against enumeration, and every stated rational bound for (22).
It also checks the cited input's compact source hashes and rejects three
deliberately corrupted finite checks. These do not replace the replay of
the input certificate or the written geometric/Taylor arguments. There
is no solver, numerical root enumeration, proof assistant, or independent
review claim for the present extension. The exact remaining frontier is
arbitrary reciprocal multisets with matching loss at least the origin
gap; neither this estimate nor the cited origin lemma controls that regime.
