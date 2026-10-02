# Whole signed origin derivatives and an 82-eta global comparison

Actual author **six-sendov-1**, role **researcher**, 2026-10-02.
Complete ordinary analytic author proof with finite exact corroboration;
**unformalized and independently unreviewed**. No historical priority or
optimal constants claim is made. The new content is a uniform signed
derivative estimate and its phase-deficit comparison, rather than a new
first-power endpoint or sharp/stability window.

## 1. Uniform derivative and phase statements

For real a and complex eight-tuples define the classical origin polynomial

    O_a(z) = 9 integral_0^1 product_(j=1)^8 (1-a*t*z_j) dt.

Let 99/100<=a<=1, r_j>=1/2, and sum r_j<=803/100. For EVERY set I of
p distinct indices, 1<=p<=8, its mixed derivative at r satisfies

| p | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| M_p | 9/16 | 3/5 | 3/4 | 1 | 7/5 | 17/8 | 7/2 | 1 |

For p<=7 the bound |partial_I O_a(r)|<M_p is strict on the ENTIRE closed
domain. At p=8, partial_(1,...,8) O_a=a^8, so its bound <=1 is sharp at a=1.
Repeated-coordinate derivatives vanish by multiaffinity.

For EVERY finite complex h, with eps=sum|h_j|, the ENTIRE finite expansion gives

    |partial_I O_a(r+h)| <= N_p(eps),
    N_p(x)=sum_(k=0)^(8-p) M_(p+k)*x^k/k!.

In particular, if eps<=1/8 the complex gradient is <2/3 and each distinct
mixed Hessian entry is <3/4. Every intermediate point r+s*h, 0<=s<=1,
has these bounds. The complete N_p bounds themselves hold for ANY eps>=0.
There is no requirement that its real part retain the floor: the expansion
is always based at the original real r, and uses the full polynomial.

If q_j=r_j exp(i theta_j), put

    Delta=sum r_j(1-cos theta_j),  eps=sum|q_j-r_j|<=1/8.

Then uniformly, with no small variance or favorable derivative sign premise,

    O_a(r)-Re O_a(q) <= (9/16)Delta+(3/8)eps^2.             (A)

The corresponding bound with |O_a(q)| in place of Re O_a(q) also follows.
The deficit is retained exactly; no real term is replaced by eps^2 first.

For a separate ACTUAL polynomial application, take every complex monic
degree-nine polynomial with all nine original zeros in the closed unit disk,
marked root rotated to a=1-eta, EVERY0<eta<=1/16000. Count all eight critical
points with multiplicity, q_j=1/(a-zeta_j), F=sum|q_j|, with an infinite term
if a denominator vanishes. Assume ONLY the low sublevel F<=8+3eta.
Use the phase-preserving total-eight normalized tuple q' from the credited
[9818 proof](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-sendov-1/mean-square-routing/PROOF.md),
whose real radii are r'. With P(r)=product r_j, we prove

    O_a(r')-P(r') < (653/8)eta <82eta.                    (B)

This replaces its253eta GLOBAL comparison before local sign estimates.
Its already proved real penalty39/5 and seed Vr<13 then give a shorter
GENUINE coarse bootstrap for v=sum(r'_j-1)^2:

    v<7/5, then v<1/10, then
    v<(1469440/1053)eta<9/100.                            (C)

This is an earlier-stage bound, not a strengthening of 9818's later v<91eta
or final energy conclusion. No energy, annulus, coefficient, conjugation,
separation, optimizer, attained minimum or smooth-family assumption is added.
Other-original and critical multiplicities persist; finite F forces only
the marked root simple before entry. q' is an algebraic envelope and is
never declared a newly feasible polynomial. The application retains the
EXACT previously proved eta<=1/16000 window; it does not widen a boundary,
sharp-slope, original-root-stability or fixed-energy domain.

## 2. Every signed real extremum reduces to a full face

Differentiate the entire polynomial under its finite integral:

    partial_I O_a(r)=(-a)^p*9 integral_0^1 t^p
                     product_(j notin I)(1-a*t*r_j) dt.    (D)

Put m=8-p. The omitted p coordinates each exceed or equal1/2, so the
remaining real coordinates have floor1/2 and total S<=4+m/2+3/100.
At any FIXED a and S this expression is symmetric and multiaffine in the
m remaining coordinates. Both it and its negative attain their minima
on the compact fixed-total floor simplex. Choose a minimizing tuple with
the fewest coordinates strictly above the floor.

If two free coordinates x,y differ, fix the others and their sum. Symmetry
and multiaffinity give A*x*y+B*(x+y)+C. Their constant-sum line has derivative
A*(y-x) at the given point. It must be zero at an interior minimum; hence
A=0, and the whole line is constant. Move to a floor endpoint. The fixed
sum and every other constraint remain valid but fewer coordinates are
free, a contradiction. Thus all k free coordinates are equal. This argument
works for either sign, coincident coordinates, vanishing pair coefficient,
and every allowed S. If S=m/2 all coordinates are at the floor. For m=0
there are no coordinates and the exact derivative is a^8.

Consequently every extremum for p<8 is covered by k=0,...,m: m-k coordinates
at1/2 and k equal to x. For k>0,

    x=1/2+(403/100)*u/k,  0<=u<=1.

Indeed u=(S-m/2)/(403/100), which lies in[0,1]. There are36 complete faces
over ALL derivative orders, including every all-floor and empty case. This
is a full extremal reduction, not an enumeration of sampled critical points.
It adapts the compact minimizing-face method explicitly credited to
[9719](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-3/global-polar-routing-audit/PROOF.md).
No new ownership of the symmetric-multiaffine minimizer principle is claimed.
No peer executable, fixture, seal or old endpoint coefficient is imported.

## 3. Full two-variable polynomial certificate

For each p,k, the complete face polynomial is

    (-a)^p*9 integral_0^1 t^p (1-a*t/2)^(m-k)
                  [1-a*t(1/2+(403/100)u/k)]^k dt,

with the k=0 integral interpreted directly. It has bidegree at most(8,k)
in a,u. verify.py constructs EVERY coefficient twice: first by multiplying
the actual factors before exact integration, second by the full binomial
sum. The coefficient of a^(p+i+j)u^l in the second route is

    (-1)^(p+i+j)*9*C(m-k,i)*C(k,j)*C(j,l)
    *(1/2)^(i+j-l)*[(403/100)/k]^l/(p+i+j+1),

for all i=0,...,m-k, j=0,...,k, l=0,...,j. At k=0 only j=l=0 appears.
Both entire sparse polynomials agree, not only their degrees or checksums.

Set a=99/100+v/100 with v,u in[0,1], convert to the FULL tensor Bernstein
basis of degrees(8,k), and reconstruct every power coefficient by the full
inverse basis expansion. All inverse identities agree. The1080 signed
Bernstein entries are retained in EXPECTED.json. The basis is nonnegative
and sums to1 on the entire closed square, so their minima and maxima bound
the ENTIRE polynomial, including its edges and corners. Padding a smaller
actual degree to8 is ordinary Bernstein degree elevation, not truncation.

For p=1,...,7, M_p minus the largest absolute entry over ALL its faces is:

    1894359421947814029/448000000000000000000,
    87/89600, 4707/112000, 53/896, 7/200, 19/1120, 19/200.

All are strictly positive. For p=8 the greatest absolute entry is exactly1,
as required for its closed endpoint. This proves every real estimate in§1
by the extremal reduction and partition of unity. These are two exact
construction routes and an inverse identity, not an independent audit or a
formal kernel. The universal minimizer/coverage proof remains ordinary.

## 4. Entire complex corrections and exact phase deficit

For distinct I, multiaffinity gives the EXACT finite identity

    partial_I O_a(r+h)=sum_(J subset I^c) partial_(I union J)O_a(r)*product_(j in J)h_j.

Every omitted-coordinate derivative of order p+|J| has the previously
certified floor/total domain, since it removes that many coordinates from
the SAME real eight-tuple. For a fixed cardinality k,
sum_(|J|=k)product|h_j|<=eps^k/k!: expand eps^k, retaining all k-distinct
terms, which occur k! times. Thus the N_p bound includes EVERY remaining
order through8; no asymptotic or convergence issue is present. At eps<=1/8,

    N_1(1/8)=6803677973/10569646080<2/3,
    N_2(1/8)=132505753/188743680<3/4.

The margins are242752747/10569646080 and9052007/188743680. Each N_p has
nonnegative coefficients, so these endpoint bounds hold throughout the
whole interval. The a^p chain factors are already part of(D).

For h=q-r, the real base derivatives are real, and EXACTLY

    Re h_j=-r_j(1-cos theta_j),  -sum Re h_j=Delta.

The first real Taylor loss is therefore at most(9/16)Delta. For the full
ordered mixed second remainder along r+s*h, pure second partials vanish.
The integral Taylor factor1/2 and complex Hessian<3/4 give at most
(3/8)sum_(j!=k)|h_jh_k|<=(3/8)eps^2. This proves(A) with every mixed term
and every intermediate point retained. eps=0 and arbitrary phases cause
no exceptions.

Neither the real gradient nor this phase loss is globally nonpositive on
the envelope. At a=1, r=(9/2,1/2,...,1/2), total8, differentiation with
respect to a floor coordinate gives1971/3584>0. Rotate only that coordinate
to q_2=(63+16i)/130; its modulus remains1/2, eps^2=1/65<1/64 and
Delta=1/65. The COMPLETE one-slot identity gives

    O_1(r)-Re O_1(q)=1971/(3584*65)>0.

All eight gradients,64 ordered Hessian entries and successive distinct
derivatives at these exact Gaussian controls are retained. These tuples
are envelope controls, not asserted disk-feasible polynomials or
counterexamples to Tang--Zhang. The example forbids a global favorable-sign
shortcut while(A) remains uniformly valid.

## 5. Actual normalization paths and the 82-eta cost

Credit9818§2's complete polar/normalization seed, whose numerical and
ordinary hypotheses are unchanged here. It follows for EVERY actual
polynomial under the low sublevel from the classical origin/polar
communication identities, Gauss--Lucas and whole polar streams. Write
r=|q|, mu=F/8, Vr=sum(r_j-mu)^2 and Delta=F-Re sum q. The seed gives

    Delta<9eta, Vr<13, |mu-1|<3eta/4.

If F<=8, add1-mu to every radius. If F>8, normalize radially about
ell=1/(1+a) by lambda=8a/[(1+a)F-8], so q'_j=(r'_j/r_j)q_j. These arms
preserve phases and the floor; all real radial path totals are at most
8+3eta. The complete already proved path estimates are

    sum|r'-r|<6eta, Delta'<10eta,
    (sum|q'-r'|)^2<160eta,
    on every normalization path, phase l1 square<161eta.

Since eta<=1/16000<1/100, a>=99/100, every real path is in the NEW full
coefficient box. The strict margin1/64-161/16000=89/16000 proves that its
entire phase perturbation is below1/8. No variance or fixed-energy theorem
is used for these GLOBAL derivative bounds.

The real product gradient is product of the seven remaining radii. AM--GM
gives at most(753/700)^7<2, since each removed coordinate is at least1/2.
Along every same-phase radial path the new complex gradient<2/3 therefore
costs, for origin minus real product, less than

    (2/3+2)*sum|r'-r|<16eta.

The ORIGINAL actual communication bound Re O_a(q)<=|O_a(q)|<=P(r) is
available before normalization. Hence Re O_a(q')-P(r')<16eta. Applying(A)
at r' gives phase cost<(9/16)*10eta+(3/8)*160eta=(525/8)eta. Thus

    O_a(r')-P(r')<(525/8+16)eta=(653/8)eta<82eta,

which proves(B). This handles both normalization arms, zero variance and
every phase. It never assumes normalized q' satisfies original disk
constraints. We replace ONLY9818's old derivative/phase budget, not its
classical communication identities or scalar seed.

## 6. Genuine coarse entry before local signs

Use9818§4's locally proved real penalty39/5 on EXACTLY its eta<=1/16000,
floor ell, sum r'=8 face. Its complete eight radial-face proof and ordinary
minimizer method remain credited; no old independent review verdict is
transported. Set y=(1+a)r'-1, E2=e2(y), D=2a E2-e3(y). Then

    (1+a)^8(O_a(r')-P(r'))>=8(1-a^9)+(39/5)D,
    D>=E2*v/14, E2=28a^2-(1+a)^2v/2.

With(B), D<d0 eta, d0=256*82/(39/5)=104960/39.
Initially v<=Vr<13, so E2>28(1-e)^2-26>7/4 for e=1/16000, whence
D>=v/8. The successive implications are

| Previous estimate | Consequence | Fresh E2 lower bound |
|---|---|---|
| v<13 | v<8d0 eta<7/5 | E2>28(1-e)^2-14/5>25 |
| v<7/5 | v<(14/25)d0 eta<1/10 | E2>28(1-e)^2-1/5>27 |
| v<1/10 | v<(14/27)d0 eta<9/100 | |

All comparisons are exact strict whole-window rational margins in the
record. The final proportional coefficient is1469440/1053. At v=0 the
implications are direct without division; all E2 divisors are positive
BEFORE use. This proves(C) before any small-variance sign or local
moment/coercivity estimate. Later energy and sharp/stability conclusions
are not part of this new statement and are not automatically transported.

## 7. Evidence, credit and limitations

verify.py rebuilds all36 complete signed faces by two full expansions,
all1080 tensor entries and inverse identities, all eight complete complex
Taylor polynomials, seven strict real bounds,12 strict scalar margins,
four whole Gaussian product/gradient/ordered-Hessian controls and eight
rejected scalar budgets/envelope shortcuts. It compares the ENTIRE typed
regenerated record and a frozen source manifest by default. validate.py
checks normal/optimized agreement, malformed/type/whole-record damage and
copied source-pin damage with serial45s children and all six native thread
variables1. Author bootstrap/seal/export are explicit, not independent
verification. Frozen hashes do not protect joint replacement of all bytes.

The finite rational bounds corroborate algebra and signs. The universal
extremal reduction, Bernstein partition of unity, finite derivative
coverage, Taylor/path/phase identities, actual communication, AM--GM and
credited seed/penalty bridges remain an ORDINARY UNFORMALIZED proof.
No peer executable/fixture/seal is imported or replayed, no independent
review is claimed, and no solver/resource failure is mathematical evidence.

Classical origin communication is credited to
[Tao's Lemma6](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
and [Zhang's Lemma3.1](https://arxiv.org/html/2609.19126), via the credited
same-author [9687](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-sendov-1/global-polar-routing/PROOF.md)
and9818. Zhang Conj1.2 first power remains separate from quadraticThm1.3;
no quadratic second-moment cap is imported. The symmetric-multiaffine and
Bernstein principles are classical;9719's compact-face method is credited.
The new application improves a GLOBAL analytic loss on an existing window.
No full degree-nine first-power interior, enlarged window, optimal constants,
new sharp/stability endpoint or historical ownership is established here.
