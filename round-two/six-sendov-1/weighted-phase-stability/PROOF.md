# A factor envelope and weighted phase stability for the degree-nine origin

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.
Complete ordinary author proof with compact exact algebra checks; unformalized;
independent review of this extension pending. The standalone factor and phase
estimates are proved here. The larger first-power annulus explicitly inherits
the published radial-defect, polar-mean and mean-tube lemmas. The full complex
first-power endpoint remains open. [LITERATURE.md](LITERATURE.md) records the
primary problem, precise dependencies and prior phase estimate.

## 1. Factor envelope

For \(0\le\tau\le1\) and \(r\ge1/2\),
\[
             |1-\tau r|\le(1-\tau/2)^{3/2-r}.          \tag{1}
\]
At \(\tau=0\) both sides equal one. Otherwise set
\(u=\tau/2\in(0,1/2]\), \(t=2r-1\ge0\),
\(v=u/(1-u)\) and \(c=-\frac12\log(1-u)>0\).
The integral bound for \(-\log(1-u)\) gives
\[
 -\log(1-u)=\int_0^u\frac{dx}{1-x}\ge u+u^2/2,
 \qquad \frac vc\le\frac2{(1-u)(1+u/2)}\le\frac{16}5.
\]
The last denominator is at least5/8 because
\[
 (1-u)(1+u/2)-5/8=(1/2-u)(3/4+u/2)\ge0.
\]
If \(vt\le1\), then \(|1-vt|\le1\le e^{ct}\).
Otherwise, putting \(s=ct\ge0\),
\(vt-1\le(16/5)s-1<e^s\). The last inequality follows from
\(e^s\ge1+s+s^2/2+s^3/6\) and the exact positive identity
\[
 2-\frac{11}5s+\frac12s^2+\frac16s^3
 =\frac56(s-71/50)^2+\frac{959}{3000}
                         +\frac16s(s-1)^2>0.           \tag{2}
\]
Consequently
\[
 |1-\tau r|=(1-u)|1-vt|
       \le(1-u)e^{ct}=(1-u)^{1-t/2},
\]
which is (1). No asymptotic, floating-point or limiting hypothesis is used.
Optimality of this envelope is not asserted.

## 2. A radius-budget product bound

For eight radii \(r_j\ge1/2\), \(\sum r_j\le8\), and a subset I
of m coordinates, their sum is at most \(4+m/2\). Multiplying (1) gives
\[
 \prod_{j\in I}|1-\tau r_j|
 \le(1-\tau/2)^{3m/2-\sum_{I}r_j}
 \le(1-\tau/2)^{m-4}.                                \tag{3}
\]
For m=0 the empty product is one and the upper bound is at least one.
For m>=4 the bound is at most one. In particular the seven-factor product
is bounded by \((1-\tau/2)^3\), and the six-factor product by
\((1-\tau/2)^2\). The same proof works for d radii with total at most d:
the exponent is m-d/2. Only d=8 is needed for the assigned family.

## 3. Adaptive weighted phase estimate

Let \(0\le a\le1\), arbitrary complex q with
\(r_j=|q_j|\ge1/2\), \(\sum r_j\le8\), and
\[
d_j=q_j-r_j,\qquad \epsilon=\sum|d_j|,
 \qquad \Delta=\sum(r_j-\Re q_j)\ge0.
\]
Define \(O_a(q)=9\int_0^1\prod(1-atq_j)dt\). For all phases,
\[
 \boxed{\Re O_a(q)\ge O_a(r)-f(a)\Delta
             -\frac{g(a)}4(e^{2\epsilon}-1-2\epsilon).}       \tag{4a}
\]
For \(\epsilon<1/2\), a rational upper bound gives
\[
 \boxed{\Re O_a(q)\ge O_a(r)-f(a)\Delta
                  -\frac{g(a)}{2(1-2\epsilon)}\epsilon^2,}     \tag{4}
\]
where the exact degree-four polynomials are
\[
 \begin{split}
 f(a)&=9a\int_0^1t(1-at/2)^3dt
      =\frac92a-\frac92a^2+\frac{27}{16}a^3-\frac9{40}a^4,\\
 g(a)&=9a^2\int_0^1t^2(1-at/2)^2dt
      =3a^2-\frac94a^3+\frac9{20}a^4.
 \end{split}                                                \tag{5}
\]
In particular \(f(a)<3/2\) and \(g(a)\le6/5\) on [0,1]. Thus
for \(\epsilon\le1/100\),
\[
 \boxed{\Re O_a(q)\ge O_a(r)-\frac32\Delta
                                -\frac{30}{49}\epsilon^2.}   \tag{6}
\]
The radii lower bound1/2 suffices here; no marked-root disk constraints,
polar channel, mean or multiplicity hypothesis is needed.
The phase identity \(|d_j|^2=2r_j(r_j-\Re q_j)\) also gives
\(\Delta\le\sum|d_j|^2\le\epsilon^2\), so (6) implies
\[
 \Re O_a(q)\ge O_a(r)-\frac{207}{98}\epsilon^2
                  \qquad(\epsilon\le1/100).                 \tag{6a}
\]
If additionally \(r_j\ge1/(1+a)\), \(a<1\),
\(\epsilon\le1/100\) and \(\Delta\le(1-a)/41\), then
\[
 \boxed{\Re O_a(q)-\prod_jr_j
                    \ge\frac{369}{64288}(1-a)>0.}            \tag{6b}
\]
Indeed \(\epsilon^2\le2(\sum r_j)\Delta\le16\Delta\),
so the loss in (6) is at most \((1107/98)\Delta\). The inherited real
gap in7244 is at least \(9(1-a)/32\); subtract and use
\(9/32-1107/(98\cdot41)=369/64288\).
This supplies a conditional signed angular sufficient region with an
explicit origin margin. Weighted angular criteria are already present in
[claim7254](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_origin_angular_monotone/PROOF.md).
The new estimate uses the factor envelope and a small-phase Taylor bound;
quadratic order and the use of a weighted angular budget are inherited ideas.

Proof: first partial derivatives at r are real. The seven-factor case of
(3), with \(\tau=at\), bounds each first partial by f(a). Since
\(\Re d_j=-(r_j-\Re q_j)\), the real linear phase loss is at most
\(f(a)\Delta\).

For a mixed second partial along \(r+sd\), \(0\le s\le1\), its
other six factors are bounded by
\[
 |1-\tau(r_j+sd_j)|\le|1-\tau r_j|+\tau|d_j|.
\]
Let \(L=1-\tau/2>0\). Expand this nonnegative product, and apply (3)
to every remaining real subset. With k selected phase factors, their
elementary symmetric sum is at most \(\epsilon^k/k!\). Therefore
\[
 \prod_{j\ne i,l}|1-\tau(r_j+sd_j)|
 \le L^2\sum_{k=0}^6\frac{(\tau\epsilon/L)^k}{k!}
 \le L^2 e^{\tau\epsilon/L}
 \le\frac{L^2}{1-2\epsilon}.                         \tag{7}
\]
We used \(\tau/L\le2\) and \(e^x\le1/(1-x)\) for \(0\le x<1\),
by comparing its series with the geometric series. Hence the mixed
second partials are at most \(g(a)/(1-2\epsilon)\); pure second
partials vanish by multiaffinity. Exact integral Taylor expansion gives
the remainder at most this constant times \(\sum_{i<l}|d_i||d_l|\),
which is at most \(\epsilon^2/2\). This proves (4), with no unspecified
Taylor remainder. The argument adapts the quadratic phase proof of
[review7244](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_review3/README.md)
but supplies new factor bounds and retains the weighted first-order phase
cost.

For (4a), retain s in the product expansion: its bound before the geometric
majorant is \(L^2e^{\tau s\epsilon/L}\le L^2e^{2s\epsilon}\).
Thus every mixed second partial is at most \(g(a)e^{2s\epsilon}\).
The ordered pair sum is at most \(\epsilon^2\), and exact Taylor
integration bounds the remainder by
\[
 g(a)\epsilon^2\int_0^1(1-s)e^{2s\epsilon}ds
       =\frac{g(a)}4(e^{2\epsilon}-1-2\epsilon).
\]
This identity holds for positive epsilon by integration by parts; at zero
epsilon the phase perturbation and both sides vanish. No phase-size
restriction is needed for (4a).

For g, its derivative factors as
\[
 g'(a)=\frac{3a}{20}\{7+(1-a)(33-12a)\}\ge0;
 \qquad g(1)=6/5.                                    \tag{8}
\]
For f, every degree-four Bernstein coefficient of \(3/2-f\) is positive
on three complete cells [0,1/2], [1/2,3/4], [3/4,1]. Their minima are
57/320,159/10240,39/20480. The complete15 coefficients are regenerated
in the checker by affine power conversion and midpoint de Casteljau routes,
with full inverse expansion. Thus f<3/2 throughout. At epsilon<=1/100,
\((6/5)/(1-2\epsilon)\le60/49\), proving (6).

## 4. A larger explicit annulus

This section inherits the committed
[radial defect theorem8656](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/radial-defect-annulus/PROOF.md),
the [polar mean8533](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/general-polar-mean/PROOF.md),
and the [mean-tube origin8591](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/near-mean-origin/PROOF.md).
Define
\[
 C_a(q)=\int_0^1\prod_j(a+(1-a^2)tq_j)dt,
 \qquad N_a(q)=|O_a(q)|^2/\prod_j|q_j|^2.
\]
**Joint-channel exclusion.** For \(1-10^{-7}\le a<1\), no eight
nonzero complex coordinates simultaneously satisfy
\[
 \sum_j|q_j|\le8,\qquad |C_a(q)|\ge1,\qquad N_a(q)\le1,
 \qquad 2a\Re q_j+(1-a^2)|q_j|^2\ge1\quad(1\le j\le8).
                                                        \tag{9a}
\]
Consequently every degree-nine polynomial with all original roots in the
closed unit disk has
\[
 \sum_{j=1}^8|\alpha-\zeta_j|^{-1}>8
       \quad\text{whenever }1-10^{-7}\le|\alpha|<1,\ p(\alpha)=0,
                                                        \tag{9b}
\]
where critical points are counted with multiplicity and a collision gives
infinity. The proof below inherits8591's ordinary author proof, still
independently unreviewed. The graph8656 statement retains its original
10^-10 width; this is a subsequent extension.

Assume (9a), and set delta=1-a, r=|q|,
mu=mean(r), m=mean(q), x=Re m. Individual critical disks give
r>=1/(1+a)>1/2 and r<9/2. The2/5 mean conclusion of8533 gives
\[
 x>a+\frac25\frac{\delta}{a(1+a)}\ge a+\delta/5,
 \quad \Delta=8(\mu-x)<\frac{32}5\delta.
\]
Consequently
\[
 \epsilon^2\le2(\sum r)\Delta<\frac{512}5\delta,
 \qquad \sum|d_j|^2\le9\Delta<\frac{288}5\delta.       \tag{9}
\]
For delta<=10^-7, epsilon<1/100, so (6) bounds the phase loss by
\[
 \frac32\Delta+\frac{30}{49}\epsilon^2
 \le\left(\frac32+\frac{480}{49}\right)\Delta
                   <\frac{17712}{245}\delta.         \tag{10}
\]

Let V=sum(r_j-mu)^2. Retain the exact finite variance cap proved in8656:
\[
 V/8\le v_*:=80001923/79997600\quad(\delta\le10^{-6}).
\]
For y=(1+a)r-1, the same exact identity used there gives
\[
e2(y)>28(1-3\cdot10^{-6})^2-16v_*
 =299965185132299811/24999250000000000>119/10.
\]
Indeed \(e_1(y)=8[(1+a)\mu-1]>8(1-3\delta)\), and
\(e_2(y)=7e_1(y)^2/16-(1+a)^2V/2\). Use \(V\le8v_*\)
and \((1+a)^2\le4\). Here \(e_k\) denotes the elementary symmetric
polynomial of degree k and \(D_a(r)=2ae_2(y)-e_3(y)\), as in8656.
Maclaurin as in8656 gives \(D_a(r)\ge e2(y)V/14\), hence
\(D_a(r)>(17/20)V\) whenever V>0. This is a retention of its exact
cap, not an independent concentration theorem.

If max|q_j/m-1|<=1/32,8591 gives N_a(q)>1. Otherwise
W=sum|q_j-m|^2>a^2/1024, while W<=2V+2sum|d_j|^2. By (9),
\[
 V>\frac{a^2}{2048}-\frac{288}5\delta
 \ge\frac1{2048}-(288/5+1/1024)\delta
 \ge\frac{24705083}{51200000000}>0.                  \tag{11}
\]
The mean is nonzero because \(|m|\ge x>a\). To check the norm bound,
write \(q_j-m=(r_j-\mu)+(d_j-\bar d)\), with
\(\bar d=\frac18\sum d_j\); then use the squared two-term bound and
\(\sum|d_j-\bar d|^2\le\sum|d_j|^2\).
The last expression evaluates the decreasing lower bound at delta=10^-7.
The new radial theorem gives
\[
 O_a(r)-\prod r>\frac{17}{1024}V
             >\frac{419986411}{52428800000000}.
\]
Subtracting the phase loss in (10), at its largest allowed delta, yields
\[
 \Re O_a(q)-\prod r>
 \frac{419986411}{52428800000000}-\frac{1107}{153125000}
              =\frac{2006956027}{2569011200000000}>0. \tag{12}
\]
Thus N_a(q)>1 in the outside-tube branch as well. This excludes the
joint system for1-10^-7<=a<1 and gives strict polynomial first power>8
there. For that polynomial implication, rotate a simple marked root to
\(a=|\alpha|\) and its critical points likewise, and put
\(q_j=(a-\zeta_j)^{-1}\). A hypothetical reciprocal sum at most eight
gives the radius budget. The classical origin and polar communication
identities give \(N_a(q)\le1\) and \(|C_a(q)|\ge1\); Gauss--Lucas
gives the individual disk inequalities in (9a). These identities are
attributed to Lemma3.1 of the current primary manuscript in LITERATURE.md.
The contradiction proves (9b); a multiple marked root is a critical
collision. No linear surplus or optimal radius is asserted.

## 5. Finite evidence and trust boundary

The finite checker reconstructs the full positive cubic identity,
logarithmic ratio polynomial identity, f/g in two integral coefficient
routes, all15 Bernstein coefficients with independent de Casteljau and
full inverse checks, the g derivative, and14 exact rational comparisons.
It rejects damaged fixtures. These checks do not formalize logarithm,
product exponent, complex segment, elementary-symmetric bound, exact Taylor,
or inherited mean-tube arguments. Normal and optimized Python reproduce the
same complete compact record and reject five damaged fixtures. Default runs
are read-only. The checker has no external imports, solver or floating-point
proof inputs. These author checks are neither independent review nor a proof
assistant formalization. The new lemma adds the factor envelope, all-phase
exponential estimate, small-phase weighted estimate and larger effective
annulus; the inherited radial gap and variance cap retain their attribution.
