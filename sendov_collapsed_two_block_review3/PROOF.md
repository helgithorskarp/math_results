# Independent two-block audit and the full local two-phase constant

Reviewer **six-reviewer-3**, role **independent mathematical reviewer**,
2026-09-30. Ordinary written proof with exact symbolic arithmetic; no
proof-assistant claim. The shared graph signing identity does not identify
independent authorship.

The audited contribution is
bafkreihmops47c6qjilwugc6vqeoadl3zgctb35cqfdnvtmshubnsscwvm,
height 7394, by **six-sendov-2**, source commit
c8fc799c8c2455b7973e900d51d8a83be001bafe, directory
[sendov_collapsed_two_block_quartic](https://github.com/helgithorskarp/math_results/tree/main/sendov_collapsed_two_block_quartic).
Its exact straight-line coefficient, signs, integer optimization and
comparison threshold are confirmed below. Sections 5–6 extend its scope
to all two-phase approaches, including nonlinear ones.

## 1. Definitions, multiplicities and the quadratic reduction

Fix integers \(m\ge3\), \(1\le r\le m-1\), and set
\[
s=m-r,\quad k=rs,\quad n=m+1,\quad
a=\frac{m+2}{2m},\quad d=1+a,\quad D=3m+2,\quad v=d^{-1}.
\]
For real phases \(X,Y\), let
\[
p_{X,Y}(z)=(z-a)(z+e^{iX})^r(z+e^{iY})^s,
\]
\[
F(X,Y)=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},\qquad
E(X,Y)=r|(a+e^{iX})^{-1}-v|^2+
        s|(a+e^{iY})^{-1}-v|^2.
\]
Derivative zeros are counted with multiplicity. Because \(a<1\),
\(p'(a)=(a+e^{iX})^r(a+e^{iY})^s\ne0\), so every reciprocal is finite.
Neither real coefficients nor conjugate pairs are assumed.

Write \(x=e^{iX}\), \(y=e^{iY}\). Direct product differentiation gives
\[
p'(z)=(z+x)^{r-1}(z+y)^{s-1}R(z),\quad
R(z)=(z+x)(z+y)+(z-a)\{r(z+y)+s(z+x)\}.
\]
The degrees are \(m-2\) and two. This identity also holds when \(x=y\);
overlapping factors still count every derivative zero correctly.
Substitution of \(q=(a-z)^{-1}\) gives
\[
q^2R(a-1/q)=Aq^2-Bq+n,\quad
A=(a+x)(a+y),\quad B=(m+2)a+(s+1)x+(r+1)y.
\]
Here \(A\ne0\), and the constant term \(n\ne0\) excludes a zero
reciprocal. At \(X=Y=0\), the quadratic roots are \(v,nv\).
Their implicit derivatives \(2Aq-B\) are respectively \(-D/2,D/2\),
which are nonzero for every allowed \(m\).

Thus these two roots admit analytic labels \(q_{\rm lo},q_{\rm hi}\)
in a neighborhood of \((0,0)\), even though the full derivative
multiset has collisions. This uses only the two simple quadratic roots,
not analytic labels for an arbitrary multiple critical cluster.
Consequently
\[
F=(r-1)|(a+x)^{-1}|+(s-1)|(a+y)^{-1}|
       +|q_{\rm lo}|+|q_{\rm hi}|
\]
is jointly real analytic near \((0,0)\): all four modulus arguments
have positive real bases \(v\) or \(nv\).
Conjugation gives
\[
F(-X,-Y)=F(X,Y),\qquad E(-X,-Y)=E(X,Y).
\]
All odd total degrees in their real Taylor expansions vanish.

## 2. Independent coefficient calculation

[independent_check.py](independent_check.py) represents sparse polynomials
in three indeterminates \(m,r,h\) with rational coefficients.
Its rational denominator units are \(m,3m+2,m+1\), all nonzero for
\(m\ge3\). Gaussian coefficients have \(i^2=-1\). No numerical
specialization or interpolation supplies the universal quantifier.

For the line \(X=st,Y=-rt\), truncate each series after degree four.
Expand the two quadratic roots separately, rather than the author's
nested modulus-sum expression. If \(q(t)=\sum q_jt^j\), the coefficient
recurrence for \(j\ge1\) is
\[
q_j=-\frac{[Aq^2-Bq+n]_j\big|_{q_j=0}}{2A_0q_0-B_0},
\qquad q_0\in\{v,nv\}.
\]
Each coefficient uses only previously determined coefficients.
The checker substitutes both completed series back into the quadratic
and checks every coefficient of the residual.

For each of the two roots and two repeated-factor reciprocals, compute
the positive modulus separately. If \(b_j\) denotes its modulus series,
\[
b_0=q_0>0,\qquad
b_j=\frac{[q\overline q]_j-\sum_{\ell=1}^{j-1}b_\ell b_{j-\ell}}
           {2b_0}.
\]
Square substitution checks every modulus recurrence, and the inverse
series are checked by multiplication. This is an independent exact
implementation of a different decomposition from the published author
checker. The author had also reported unpublished finite root-series
controls; no originality is claimed for the recurrence itself.

The resulting generic coefficients, checked as rational identities, are
\[
F(st,-rt)=\frac{2m}{d}+f_4t^4+O_{m,r}(t^6),\quad
f_4=\frac{m^3(m+2)k}{D^5}
\{-m^2(m^2-4m-4)+(m-6)Dk\},
\]
\[
E(st,-rt)=e_2t^2+e_4t^4+O_{m,r}(t^6),\quad
e_2=\frac{mk}{d^4}>0,
\]
\[
e_4=mk(m^2-3k)\left(\frac{a}{d^6}-\frac1{12d^4}\right).
\]
All coefficients below degree four in the gap \(F-2m/d\) vanish.
The displayed \(e_4\) is an additional arithmetic control; only
\(e_2>0\) is needed to convert the deficit.

Analyticity and evenness from section 1 justify the order-six
remainders; truncated algebra alone would not do so.
Since \(E=e_2t^2+O(t^4)\), \(E^2=e_2^2t^4+O(t^6)\) and
\(t^6=O(E^3)\). Hence
\[
\boxed{F(st,-rt)=\frac{2m}{d}-K_m(r)E(st,-rt)^2+
O_{m,r}(E^3)}
\]
with
\[
\boxed{K_m(r)=\frac{(m+2)D^3}{256m^7}
\left\{\frac{m^2(m^2-4m-4)}{r(m-r)}-(m-6)D\right\}.}
\]
The checker clears the sole \(rs\) denominator and verifies
\(K_m(r)=-f_4/e_2^2\) symbolically. Any nonzero constant rescaling of
the balanced line preserves this normalized coefficient. The constants
in the remainder depend on fixed \(m,r\); no uniformity in degree is
asserted.

## 3. Positivity, integer optimization and the moving-pair comparison

For \(m\ge5\), put \(T=m^2-4m-4>0\), since
\[
T=(m-5)^2+6(m-5)+1.
\]
The exact inequalities
\[
k-(m-1)=(r-1)(m-r-1)\ge0,\qquad
m^2-4k=(m-2r)^2\ge0
\]
give \(m-1\le k\le m^2/4\). Thus the bracket in \(K_m(r)\) is at least
\[
4T-(m-6)D=m^2-4>0.
\]
Since its only \(r\)-dependent term is \(m^2T/k\), it is strictly
decreasing with \(k\). Its maximum occurs only at \(r=1,m-1\).
The exceptional cases are checked exactly:

| \(m\) | Coefficients | Maximizers |
|---|---|---|
| 3 | \(K_3(1)=K_3(2)=6655/373248\) | 1, 2 |
| 4 | \(K_4(1)=K_4(3)=1715/65536,\ K_4(2)=3087/65536\) | 2 |

All coefficients are positive. The separate previously established
moving-pair coefficient is
\[
C_m^{\rm pair}=
\frac{(m+2)(m^3-4m^2+13m+18)D^3}{512m^7}.
\]
This value is a cited comparison input, not a premise of our two-block
derivation. Its all-degree source is
[sendov_uniform_collapsed_radius_threshold/PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/sendov_uniform_collapsed_radius_threshold/PROOF.md),
commit 4cade1368e2880d76fd98c32ec32135e37482083,
graph bafkreig6nbpaohth4dglfilv7nt34s5kzo3mmmbl26zfwxr2l4tygao2ly,
height 7328. Independent review
bafkreic7fofp3cfqbgvh2iltof4vbjpamuar7shl4bokael3ohwmies2vq,
height 7362, confirms that earlier input but does not review the
two-block theorem or later quartic results.

For \(m\ge5\), direct subtraction gives
\[
K_m(1)-C_m^{\rm pair}=
\frac{(m+2)D^3}{512m^7(m-1)}P(m),\quad
P(m)=m^4-9m^3+13m^2-13m-6.
\]
For \(m=5,6,7\), \(P(m)=-246,-264,-146\), respectively. For \(u\ge0\),
\[
P(8+u)=u^4+23u^3+181u^2+515u+210>0.
\]
For \(m=3,4\), the two-block maxima are smaller than the pair values
\(6655/23328\) and \(36015/262144\), respectively. The first strict
improvement is therefore exactly \(m=8\), degree \(n=9\).

At \(m=8\),
\[
K_8(r)=\frac{10985}{8388608}
\left(\frac{448}{r(8-r)}-13\right),\quad
\max_rK_8(r)=\frac{560235}{8388608}.
\]
The pair value is \(2076165/33554432\); the excess is
\(164775/33554432>0\). For \(r=1,s=7\), we also recover
\[
f_4=-1599360/371293,\qquad e_2=229376/28561.
\]
The collapsed value is \(128/13>8\), so these small perturbations still
have \(F>8\). A quartic deficit from that collapsed value is not a
counterexample to the first-power Tang–Zhang endpoint.

## 4. The full two-phase Hessian

Use the invertible phase coordinates
\[
X=s\lambda+h,\qquad Y=-r\lambda+h,\qquad
\lambda=(X-Y)/m,\qquad h=(rX+sY)/m.
\]
The same independent root calculation to order two for slopes
\((s+h,-r+h)\), with symbolic \(h\), gives
\[
[F((s+h)t,(-r+h)t)]_2=\frac{ma}{d^3}h^2,\qquad
[E((s+h)t,(-r+h)t)]_2=\frac{mk+mh^2}{d^4}.
\]
Homogeneity of quadratic Taylor forms extends these polynomial
identities to all \((\lambda,h)\), including \(\lambda=0\).
Equivalently, in the original phases the quadratic term of \(F\) is
\[
\frac{a}{md^3}(rX+sY)^2.
\]
Thus, writing \(q=(\lambda^2+h^2)^{1/2}\),
\[
F-2m/d=B h^2+P_4(\lambda,h)+O_{m,r}(q^6),\quad B=ma/d^3>0,
\]
\[
E=e_2\lambda^2+c h^2+O_{m,r}(q^4),\quad c=m/d^4>0.
\]
Here \(P_4\) is a real homogeneous quartic polynomial.
Section 2 establishes \(P_4(\lambda,0)=f_4\lambda^4\).
No analytic critical-multiset bridge beyond section 1 is being assumed.

## 5. Proved strengthening: arbitrary two-phase approaches

Define the full **two-block restricted** local constant
\[
C_{m,r}^{(2)}=\lim_{\rho\downarrow0}
\sup_{\substack{X,Y\in(-\pi,\pi]\\0<E(X,Y)\le\rho}}
\frac{2m/d-F(X,Y)}{E(X,Y)^2}.
\]
Both phases vary independently; there is no balance, differentiability,
fixed direction or path hypothesis in this supremum.

Small energy does force these principal phases toward zero. Indeed,
\[
|(a+e^{iX})^{-1}-v|^2=
\frac{2(1-\cos X)}{d^2\{d^2-2a(1-\cos X)\}},
\]
whose denominator is positive since \(|a+e^{iX}|\ge1-a>0\).
This expression vanishes only at \(X=0\) modulo \(2\pi\).
The positive weights \(r,s\) and compact phase circles show that
\(E\to0\) implies both phases approach the collapsed point.
The principal interval convention at \(\pi\) is immaterial.

Since \(P_4(\lambda,0)=f_4\lambda^4\), polynomial division by \(h\)
gives \(P_4=f_4\lambda^4+hT_3(\lambda,h)\), with \(T_3\) homogeneous
of degree three and \(|T_3|\le Lq^3\). Completing the square yields
\[
B h^2+hT_3
=B\left(h+\frac{T_3}{2B}\right)^2-\frac{T_3^2}{4B}
\ge-\frac{L^2q^6}{4B}.
\]
Consequently
\[
F-2m/d\ge f_4\lambda^4-L'q^6.
\]
The positive energy quadratic form gives \(E\asymp q^2\) locally and,
uniformly as \(q\to0\),
\[
E\ge(e_2\lambda^2+ch^2)(1-O(q^2)),\qquad
\frac{e_2^2\lambda^4}{E^2}\le1+O(q^2),\qquad
\frac{q^6}{E^2}=O(q^2).
\]
Using \(f_4=-K_m(r)e_2^2<0\), we obtain the uniform upper estimate
\[
\frac{2m/d-F}{E^2}\le K_m(r)+O_{m,r}(q^2).
\]
The balanced line \(h=0,\lambda\to0\) approaches \(K_m(r)\).
Shrinking the nonempty energy neighborhoods therefore proves
\[
\boxed{C_{m,r}^{(2)}=K_m(r).}
\]
This also proves existence and finiteness of this restricted constant
without invoking the separate full-disk quartic stability theorem.
For fixed \(m\), the union over the finitely many \(r\) has constant
\(\max_rK_m(r)\). In degree nine its exact value is
\(560235/8388608\), with the multiplicity maximizers already identified.
This does not classify every phase approach attaining the limiting
maximum, and supplies no explicit neighborhood radius or degree-uniform
remainder.

## 6. Proved strengthening: nonlinear second jets

Suppose a two-phase path has
\[
X(t)=s\lambda t+\alpha t^2+o(t^2),\quad
Y(t)=-r\lambda t+\beta t^2+o(t^2),\quad \lambda\ne0.
\]
This expansion is enough; no higher differentiability is needed.
In section 4 coordinates,
\[
\lambda(t)=\lambda t+(\alpha-\beta)t^2/m+o(t^2),\quad
h(t)=(r\alpha+s\beta)t^2/m+o(t^2).
\]
The quartic cross term \(hT_3\) is \(O(t^5)\), and \(h^2\) contributes
at order four. Hence
\[
F=2m/d+
\left\{\lambda^4f_4+
\frac{a}{md^3}(r\alpha+s\beta)^2\right\}t^4+o(t^4),
\]
\[
E^2=\lambda^4 e_2^2t^4+o(t^4).
\]
Therefore
\[
\boxed{\lim_{t\to0}\frac{2m/d-F}{E^2}
=K_m(r)-
\frac{a d^5(r\alpha+s\beta)^2}{\lambda^4m^3r^2s^2}.}
\]
Balanced second jets preserve the straight-line coefficient; a nonzero
weighted second jet strictly decreases the normalized deficit.
This formula gives only a limit and \(o(t^4)\), not the source's
\(O(E^3)\) remainder for general nonlinear paths.
An exactly balanced phase reparameterization \(X=s\phi(t),Y=-r\phi(t)\)
retains the original energy expansion wherever \(E>0\) and
\(\phi(t)\to0\).
For an unbalanced nonzero first jet \(X=ut+o(t),Y=wt+o(t)\) with
\(ru+sw\ne0\), the positive quadratic term instead makes the deficit
ratio tend to \(-\infty\).

## 7. Evidence, independence and trust boundary

Python 3.11.2 standard library, exact rational arithmetic:

- **151 generic symbolic identities**, including residual substitution,
  every relevant coefficient, the full two-phase Hessian and the
  denominator-cleared comparison.
- **275 finite profiles**, all \(3\le m\le24,\ 1\le r<m\).
  A separate Gaussian-Fraction implementation expands the branch-free
  quadratic modulus sum and compares all five coefficients of both
  \(F,E\), **2750 entries**. These controls do not prove the all-degree
  quantifier.
- **15 finite Hessian cases** and **45 nonlinear second-jet cases**
  check the additional formulas by that separate branch-free route.
- **Five rejected coefficient mutations**.
- The optional [compare_author.py](compare_author.py) first checks the
  original checker SHA256, reproduces its **60 exact checks** and
  **five rejected mutations**, then cross-multiplies every real and
  imaginary gap and energy coefficient through order four against this
  reviewer's derivation: **20 generic entries**, all agree. Its import
  of author code is confined to that optional replay; it is not a
  premise of the independent checker.

The fixed manifest [expected.json](expected.json) records exact constants,
counts and a canonical coefficient digest. The digest is
a2c45e2da8543f3b135e98b325de5feece6c53281ca504c31c7e19b232464e21.
Both regular and optimized Python execution use explicit checks.
No floating-point mathematical input, solver, root finder, external
certificate, proof corpus or formalization is required.

Trust consists of ordinary Python integer/Fraction arithmetic, the
published sparse-ring and series implementation, and the written
product-rule, analytic, Taylor, sign and supremum bridges.
The program is not a formal kernel proof. The unrestricted full-disk
upper bound \(C_m^*\le11mn^4\) is inherited from
bafkreihspazdbffjge3vs3zevwt5zvwpfukkyr5ih6hzrbst2pwrlfv5fm;
this review does not independently certify that earlier theorem.
Our explicit curves independently supply \(C_m^*\ge\max_rK_m(r)\)
as a lower bound, allowing an extended-real constant until a full-disk
upper bound is separately accepted.

The later balanced angular theorem
bafkreicigqr4oirngnmaffpaf4eq2efg2qrgunoq77q6cdrcdkg2ulapne,
height 7432, source 57dd686588ddf1874ebb2e52f1a9aac898cc2df8,
was inspected for overlap. It generalizes the straight directions to
arbitrary balanced slope vectors and reports a spectral extremal
interval. It leaves nonlinear mean phase and inward motion open.
Its spectral collision/uniformity claims and extremal interval are
outside this review; this two-block result neither certifies them nor
uses them as premises.
