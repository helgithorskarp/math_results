# An analytic fifth-order inward repair of the balanced-mean family

**six-reviewer-1 / independent mathematical reviewer.** Ordinary exact
computer-assisted mathematics, **unformalized**. This is a derivative of
LEMMA10280, with independent polynomial and original-root arithmetic.
The current author's programs, expected records and private corpora are not inputs.

## 1. Domain and proved refinement

For a monic degree-nine polynomial with all nine original roots in the
closed unit disk and marked root \(a=1-\eta\), put
\[
 F(p,a)=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},\qquad
 \mathcal I(\eta)=\inf_{\text{actual }p}F(p,1-\eta).
\]
All eight critical multiplicities are counted. A collision contributes infinity.

Let \(c=\cos(\pi/9)\), \(8c^3-6c-1=0\), and define
\[
 C=\frac83+\frac1{3(1+c)},\quad
 B_*=\frac{2311}{108}+\frac{4934}{27}c-\frac{1976}{9}c^2,
\]
\[
 T_*=-\frac{60800959}{17496}-\frac{307083769}{17496}c
                         +\frac{10980067}{486}c^2,
 \quad M_3(\eta)=8+C\eta+B_*\eta^2+T_*\eta^3,
\]
\[
 G_*=\frac{183619658945}{2519424}
       +\frac{444829186913}{1259712}c-\frac{288729410449}{629856}c^2,
 \quad
 L=-\frac{101920}{243}-\frac{1218245}{486}c+\frac{251888}{81}c^2,
\]
\[
 G(\mu)=G_*+L\mu+\frac43\mu^2,\quad
 \mu_*=-\frac38L,\quad G_{\rm mean}=G_*-\frac3{16}L^2.
\]
These constants and the balanced real critical means are credited to
10152/10212/10280. They are definitions, not freshly discovered parent results.

**Refinement.** For every fixed real \(R\ge0\), set
\[
 \tau_R=8+13R+2R^2.
\]
Replace the common inward term \(\eta^{9/2}\) in the explicit 10280 family
by \(\tau_R\eta^5\). For all \(|\mu|\le R\), on a common positive
existence collar the resulting polynomial has all nine original roots
simple and strictly interior, no critical collision, and
\[
 F=M_3(\eta)+G(\mu)\eta^4+
        [f_5(\mu)+8\tau_R]\eta^5+O_R(\eta^6).                 \tag{1}
\]
The polynomial coefficients and original-root branches are analytic in
\(\eta\); there is no fractional inward term.

At \(R=16\), \(\tau_{16}=728\) and \(8<\mu_*<16\). The exact fifth coefficient is
\[
 D_{16}=f_5(\mu_*)+5824
 =-\frac{1554380464593574777}{69657034752}
  -\frac{1219260700409103133}{11609505792}c
  +\frac{397722967460633563}{2902376448}c^2,
 \qquad -71<D_{16}<-70.                                    \tag{2}
\]
In particular,
\[
 \limsup_{\eta\downarrow0}
 \frac{\mathcal I(\eta)-M_3(\eta)-G_{\rm mean}\eta^4}{\eta^5}
 \le D_{16}<-70,                                           \tag{3}
\]
and for all sufficiently small positive \(\eta\),
\[
 \mathcal I(\eta)<M_3(\eta)+G_{\rm mean}\eta^4-70\eta^5.      \tag{4}
\]
These are actual upper comparisons. No universal fourth or fifth lower
coefficient, existence of either universal limit, effective collar,
sharp fifth optimum or global first-power theorem is asserted.

## 2. Complete definition of the critical family

Put

\[
 y=\frac1{3(1+c)},\quad x=\frac23-y,\quad H=14y,
 \quad U_0=-8x,\quad \rho=\frac{c-5}{3},
\]

\[
 u_z=\frac{U_0+\rho H}{8},\qquad
 u_p=u_z-\frac{\rho H}{2},\qquad
 W_* =\frac{2512}{27}+\frac{5840}{9}c-\frac{21392}{27}c^2,
 \quad w_2=W_*/8,
\]

\[
 \Gamma=\frac{13}{36}+\frac{1253}{72}c-\frac{50}{3}c^2,
\]

\[
 m_0=-\frac{17403419}{34992}-\frac{45702565}{17496}c
                                 +\frac{180635}{54}c^2,
\]

\[
 b_0=-\frac{1162307}{23328}-\frac{5484833}{11664}c
                                 +\frac{52426519}{93312}c^2,
\]

\[
 M_* =\frac{8148040331}{629856}
       +\frac{78878749667}{1259712}c-\frac{51194418673}{629856}c^2,
\]

\[
 \beta_* =\frac{27821775167}{17915904}
       +\frac{80418819893}{8957952}c-\frac{12650091319}{1119744}c^2.
\]

These constants and the real-mean repairs are credited to10152/10212/10280. Define

\[
 m(\mu)=m_0+\frac{56}{9}(c-c^2)\mu,
 \qquad b(\mu)=b_0+\left(\frac12+2c\right)\mu,
                                                               \tag{3}
\]

\[
 \widehat M(\mu)=M_*+
       \left(-\frac{51583}{972}-\frac{175385}{486}c+448c^2\right)\mu,
                                                               \tag{4}
\]

\[
 \widehat\beta(\mu)=\beta_*+
       \left(\frac{1771}{324}-\frac{94039}{1296}c
                             +\frac{12347}{162}c^2\right)\mu
       +\frac27(1+c)\mu^2.                                    \tag{5}
\]

Define the real centers and imaginary pair scale by

\[
 A=u_z\eta+(w_2-\mu/3)\eta^2+m(\mu)\eta^3
                         +\widehat M(\mu)\eta^4+\tau_R\eta^5,
\]

\[
 B=u_p\eta+(w_2+\mu)\eta^2+m(\mu)\eta^3
                         +\widehat M(\mu)\eta^4+\tau_R\eta^5,
\]

\[
 K_\eta=i\left[1+\Gamma\eta+b(\mu)\eta^2
                              +\widehat\beta(\mu)\eta^3\right],
\]

\[
 p'_{\eta,\mu}(z)=9(z-A)^6
       \left[(z-B)^2-\frac H2\eta K_\eta^2\right],
 \qquad
 p_{\eta,\mu}(z)=\int_{1-\eta}^{z}p'_{\eta,\mu}(w)\,dw.      \tag{6}
\]

The integral is the polynomial primitive with the displayed anchor, so
the polynomial is monic of degree nine and has marked root \(1-\eta\).
Its critical slots are six at \(A\) and the conjugate pair
\(B\pm\sqrt{H/2}\sqrt\eta K_\eta\). For sufficiently small \(\eta\),
the pair scale is nonzero and the critical distances from the anchor
are bounded away from zero, uniformly on compact \(\mu\) sets.


## 3. Independent finite derivation and fifth budgets

Our field is \(\mathbb Q(\zeta_{36})\), with
\(\zeta_{36}^{12}-\zeta_{36}^6+1=0\), \(i=\zeta_{36}^9\),
\(\omega=\zeta_{36}^4\), \(c=(\zeta_{36}^2+\zeta_{36}^{34})/2\).
Conjugation sends \(\zeta_{36}\) to its inverse. Every check is an
identity in this field with a formal real indeterminate \(\mu\), rather
than sampling real parameter values. The own field and rational interval
operations are credited to 10070/10272; no author arithmetic is imported.

Write \(S=1+\Gamma\eta+b(\mu)\eta^2+\widehat\beta(\mu)\eta^3\).
The derivative is
\[
 p'(z)=9(z-A)^6[(z-B)^2+(H/2)\eta S^2].
\]
The checker independently multiplies the dense derivative and integrates
every original \(z\) coefficient. A second route uses the translated
primitive, with \(w=z-A\) and \(d=A-B\),
\[
 w^9+\frac94 d\,w^8+\frac97[d^2+(H/2)\eta S^2]w^7,
\]
subtracting its value at \(a\). All ten original coefficient columns
through order five agree. Monicity and the entire marked-root anchor
are separately checked.

At \(\eta=0\) the primitive is \(z^9-1\). For each \(j=0,\ldots,8\),
put \(z_j=\omega^j\) and solve for \(Z_j=z_j+\sum_{n=1}^5 r_{j,n}\eta^n\).
At the \(n\)-th step the fresh coefficient of \(r_{j,n}\) is \(9z_j^8\).
The checker substitutes each completed branch into the entire original
primitive and verifies every coefficient through order five, including
the prescribed anchor branch. It also verifies the complete conjugation
pairing and each half-normal \(N_j=(Z_j\overline Z_j-1)/2\).

For \(\tau=0\), all four individual active labels \(j=3,4,5,6\) have
zero half-normal coefficients at orders one through four. Each of the
five inactive first coefficients is
\[
 \nu_j=-\left(\frac13+x\cos\frac{2\pi j}9
                        +y\cos\frac{4\pi j}9\right)<0,
 \qquad j=0,1,2,7,8.                                      \tag{5}
\]
All nine equations are retained; label zero is the marked root.

Let \(q_{j,5}(\mu)=[\eta^5]N_j\) for the zero fifth-center family and
\(A_j=1-\cos(2\pi j/9)>0\) at the active labels. All four active ratios
\(q_{j,5}/A_j\) are quadratics \(r_{j,0}+r_{j,1}\mu+r_{j,2}\mu^2\).
The whole exact ratios in the field and their rational physical
enclosures are stored in EXPECTED.json. To make the result inspectable,
the three coefficients for the two reflected types are as follows;
each row displays coefficients in \(1,c,c^2\).

| Label | \(\mu\) power | coefficient triple |
|---|---:|---|
| 3,6 | 0 | \((-7293232089277697/69657034752,\ -5809710683424677/11609505792,\ 1889762375330027/2902376448)\) |
| 3,6 | 1 | \((486091517/279936,\ 2310714253/279936,\ -751884343/69984)\) |
| 3,6 | 2 | \((53/126,\ 31/54,\ 170/189)\) |
| 4,5 | 0 | \((-7549883884071265/17414258688,\ -70772795590721635/34828517376,\ 15402534234898513/5804752896)\) |
| 4,5 | 1 | \((-1068415519/279936,\ -2693216555/139968,\ 3472962359/139968)\) |
| 4,5 | 2 | \((2953/1134,\ 6073/567,\ -6883/567)\) |

Thus, separately for every active label,
\[
 |r_{j,0}|\le7,\qquad |r_{j,1}|\le13,\qquad |r_{j,2}|\le2.  \tag{6}
\]
The physical embedding is certified by the unique positive root of
\(8c^3-6c-1\), bracketed initially between \(939/1000\) and \(940/1000\),
then by sixty exact rational bisections. No floating-point sign is used.
Every conversion back to \(\mathbb Q(c)\) is checked against all twelve
original rational field coordinates.

Adding a common fifth center \(\tau\eta^5\) changes the fifth primitive
by \(9\tau(1-z^8)\), the fifth root coefficient by \(\tau(1-z_j)\), and
the fifth half-normal by \(-\tau A_j\). The two full fresh computations
at \(\tau=0\) and \(1\) verify every original primitive, root and normal
coefficient individually. Linearity for arbitrary real \(\tau\) follows
because any interaction with a lower perturbation has order at least six.

For \(|\mu|\le R\), (6) gives
\[
 \frac{q_{j,5}(\mu)}{A_j}\le7+13R+2R^2,
 \qquad q_{j,5}(\mu)-\tau_R A_j\le-A_j.                    \tag{7}
\]
This proves the uniform inward margin, including \(R=0\).
It is a coefficient bound for every real \(\mu\) in the interval,
not a finite test of selected parameters.

## 4. Actual analytic containment and uniform remainders

For fixed \(R\), the primitive is polynomial in \(\eta,\mu\) and has
the fixed ninth-root limit. Choose disjoint neighborhoods of all nine
ninth roots. Uniform coefficient convergence on \(|\mu|\le R\) and
Rouché's theorem put exactly one root, counted with multiplicity, in
each neighborhood for sufficiently small \(\eta\). Hence the roots
remain simple and exhaust degree nine. The complex implicit-function
theorem gives their analytic branches in \(\eta\); its Taylor
recursion is exactly the finite original-root recursion above.
One may first use a bounded complex neighborhood of the real parameter
interval. Compactness and the nonzero limiting derivatives give a common
collar and uniform analytic derivatives, hence uniform sixth-order
remainders. No assertion is made about a numerical value of that collar.

For each inactive label (5) gives
\(N_j=\nu_j\eta+O_R(\eta^2)<0\) uniformly on a smaller collar.
For each active label, (7) gives
\[
 N_j=[q_{j,5}(\mu)-\tau_R A_j]\eta^5+O_R(\eta^6)
       \le-A_j\eta^5+O_R(\eta^6)<0.
\]
All nine original roots are therefore strictly interior, individually.
The centers tend to zero and \(S\to1\) uniformly; \(H>0\), so the
critical pair is distinct and the sixfold critical center is retained.
Every critical distance from \(a\to1\) stays bounded away from zero.
Monicity, the anchor and all eight critical multiplicities follow from
the literal derivative and anchored primitive, with no converse
feasibility assumption.

The earlier 10280 \(\eta^{9/2}\) family is also independently supported
by the zero active coefficients and the checked ninth
\(\epsilon=\sqrt\eta\) root response \(1-z_j\):
\(N_j=-A_j\epsilon^9+O_R(\epsilon^{10})\).
This is a scoped reproduction of its explicit actual construction;
the present new result uses the paid fifth normals instead.

## 5. Complete scalar cost and the fifth upper comparison

For this actual critical multiset the scalar sum is exactly
\[
 F=\frac6{a-A}
   +\frac2{\sqrt{(a-B)^2+(H/2)\eta S^2}}.                  \tag{8}
\]
The positive scalar branches are analytic near \(\eta=0\), uniformly
for the bounded real parameters. Our separate reciprocal recurrence
and inverse-square-root binomial expansion verify (8) through order five.
Their products with the original denominator and squared denominator
are checked identically. All lower coefficients are exactly
\(8,C,B_*,T_*,G(\mu)\).

For zero fifth center, \(f_5(\mu)=f_{5,0}+f_{5,1}\mu+f_{5,2}\mu^2\).
Their exact coefficient triples in \(1,c,c^2\) are

\[
 f_{5,0}=
 \frac{46162779724939271}{69657034752}
 +\frac{36338752485008003}{11609505792}c
 -\frac{11846579474774765}{2902376448}c^2,
\]
\[
 f_{5,1}=\frac{932974693}{279936}
          +\frac{6209560805}{279936}c
          -\frac{1933889279}{69984}c^2,
 \qquad
 f_{5,2}=-\frac{809}{54}-\frac{3545}{54}c+\frac{166}{3}c^2.
\]
The whole fifth common-center cost response is \(8\tau\),
verified by both fresh scalar expansions and evident from the eight
limiting unit critical distances. The uniform scalar Taylor remainder
in (8) proves (1). Completing the fourth square gives
\[
 G(\mu)=G_{\rm mean}+\frac43(\mu-\mu_*)^2.
\]
The physical rational intervals certify \(L<0\), \(8<\mu_*<16\),
\(G_{\rm mean}<G_*<0\), as well as the strict bounds (2).
Substituting the actual family with \(R=16,\mu=\mu_*\) into the
definition of the infimum proves (3), without assuming attainment or
a limit of the infimum. Since \(D_{16}<-70\), the uniform \(O(\eta^6)\)
remainder is smaller than the fixed fifth margin on a smaller collar,
which proves (4).

## 6. Scope, provenance and trust boundaries

The theorem is an explicit analytic comparison family, not a
classification of arbitrary actual competitors. The full lower bound
and complete fourth/fifth optimization over all means, imaginary
residuals, shrinking skew and moving normal budgets remain open.
The new fifth coefficient is not claimed optimal.

The original 10280 definitions and whole written proof are exposed
inputs. Own Q(zeta36) and rational interval arithmetic are reused from
10272 with attribution to10070. The current author and current peer
native/EXPECTED/validation files, baseline fixtures and private
records were not read, imported or executed. Two literal integration
algorithms and a different field representation provide independent
evidence, but this was not a blind audit of the written statement.

All finite arithmetic is ordinary CPython integer/Fraction computation.
The analytic branch, compactness, Rouché, simple-root and Taylor bridges
are written ordinary proof, not checked in a proof assistant.
Core seals detect changes to the listed source/fixture before imports;
they do not prevent coordinated replacement of the source and seals.
The complete deterministic coefficient record is compact EXPECTED.json;
all normal/optimized/local/cold comparisons are whole-record and
strictly typed. Matching counts alone are not a proof premise.
