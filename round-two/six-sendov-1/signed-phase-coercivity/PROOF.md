# Signed phase coercivity of the degree-nine origin polynomial

Actual **six-sendov-1**, role **researcher**, 2026-10-03.
**Complete ordinary author proof**, UNFORMALIZED and
independently UNREVIEWED. Exact whole finite identities and endpoint checks
corroborate this analytic proof; they do not formalize the norm, subset,
Maclaurin, path, sign or actual-polynomial implication bridges.

## 1. Standalone theorem and quantified actual applications

Define the classical degree-eight multiaffine origin polynomial

    O_a(q)=9 integral_0^1 product_(j=1)^8(1-a s q_j) ds.

For EVERY finite complex eight-tuple z, let R_j=|z_j|,
B_j=Re z_j, d_j=R_j-B_j>=0, y_j=Im z_j,
Delta=sum d_j and Y=sum y_j. Put rho=norm_2(R-1).
For Delta<=1/1000 the following standalone bounds hold:

    rho<=1/16  => O_1(R)-Re O_1(z)<=-Delta/8+Y^2/56,
    rho<=1/40  => O_1(R)-Re O_1(z)<=-7Delta/48+Y^2/56.      (1)

At Delta=0 the difference and Y vanish. At positive Delta both bounds
are strict, by the strictly positive complete endpoint gaps below.
These are universal tuple estimates, not an assumption or assertion of
original-disk feasibility. Arbitrary nonconjugate phases and coordinate
collisions are allowed. The radial classes imply positive R_j.

For actual complex monic degree nine with ALL nine originals in the CLOSED
unit disk, marked a=1-eta, EVERY0<eta<=e=1/12000, ALL eight critical
multiplicities and ONLY F=sum|a-zeta_j|^-1<=8+3eta, let q_j=(a-zeta_j)^-1,
r_j=|q_j|, Delta_q=F-Re sum q_j and Y_q=Im sum q_j. Infinity is used at
zero denominators, hence those cases are outside this finite low arm.
The genuine9930 entry H=sum|zeta_j|^2<37eta<1/320 and its polar estimate
Delta_q<(17/2)eta give

    O_a(r)-Re O_a(q)<=-a Delta_q/8+a^2 Y_q^2/56.          (2)

This application needs no LC mean/variance/radius box. It uses the genuine
entry only AFTER that entry was proved; it is not a new entry or interval.
The separately fixedH<=1/320 implication, retaining the actual polar
Delta bound and low cut, is valid with the same proof.

Using the already proved actual receiving tuple of9974 (also9954), with
m=M+iD,nu=zeta-m,W=sum|nu|^2,t=|m|,

    W<5eta, |D|<eta/3, t<13eta/15,

one obtains the stronger actual comparison

    O_a(r)-Re O_a(q)<=-7a Delta_q/48+a^2 Y_q^2/56
                    <-7a Delta_q/48+(8/7)a^2 eta^2.     (3)

The classical original-disk communication bound Re O_a(q)<=product r_j
therefore yields the same upper bounds for O_a(r)-product r_j.
In particular, on this established actual LC class,

    O_a(r)>=product r_j  => Delta_q<(384/49)a eta^2.       (4)

Equation(4) is CONDITIONAL on the stated real radial-gap sign; that sign
is not imposed on every actual polynomial. No sharp first-power slope,
objective/physical/motion remainder, larger domain or global endpoint is
inferred. Parent and receiving review scopes remain separate.

## 2. Full mixed coefficients near the real unit tuple

Finite integration and elementary symmetric expansion give

    O_1(1+x)=sum_(k=0)^8 c_k e_k(x),
    c_k=(-1)^k/binom(8,k).

For a fixed set I of k distinct indices, with m=8-k remaining indices,

    partial_I O_1(1+x)=sum_(ell=0)^m c_(k+ell)e_ell(x_(I^c)).

Repeated-coordinate derivatives vanish. For norm_2(x)<=sigma and m>0,
subset Cauchy and nonnegative Maclaurin give

    |e_ell(x_(I^c))|<=binom(m,ell)(sigma/sqrt(m))^ell.

Indeed the triangle inequality over all ell-subsets, then Cauchy over
those subsets, reduces the bound to e_ell(|x|^2). Its Maclaurin bound is
binom(m,ell)(sigma^2/m)^ell. Zero coordinates and arbitrary signs are
included; ell=0 is direct. At k=8 there are no remaining coordinates
and the derivative is exactly1, without dividing by m.
The ENTIRE coefficient identity is

    binom(8-k,ell)/binom(8,k+ell)
       =binom(k+ell,k)/binom(8,k).                        (5)

All36 coefficients across k=1,...,8 are retained. The general-a shifted
coefficients are likewise the complete polynomials

    c_k(a)=9(-a)^k integral_0^1 s^k(1-a s)^(8-k) ds
          =sum_(ell=0)^(8-k)
             9(-1)^(k+ell)binom(8-k,ell)a^(k+ell)/(k+ell+1).

The two complete constructions agree on all45 coefficients. No sampled
parameter or omitted degree supplies a bound.

## 3. Signed Hessian and the exact even phase expansion

Fix a radial threshold r0 (here1/16 or1/40), d0=1/1000 and
sigma=r0+d0. The real segment R-v d,0<=v<=1 satisfies
norm_2(R-vd-1)<=r0+norm_2(d)<=sigma. Choose four scales b_k with
(8-k)b_k^2>=sigma^2,k=1,2,4,6. Define the COMPLETE finite quantities

    g=1/8-sum_(ell=1)^7(ell+1)b_1^ell/8,
    h=sum_(ell=1)^6(ell+1)(ell+2)b_2^ell/56,
    c=1/56-(7/2)h,
    D4=sum_(ell=0)^4 binom(ell+4,4)b_4^ell/70,
    D6=sum_(ell=0)^2 binom(ell+6,6)b_6^ell/28.

Equation(5) proves every real gradient partial_j O_1<=-g on the ENTIRE
real segment, and every distinct Hessian at B satisfies
|partial_(i,j)O_1(B)-1/28|<=h. The mixed fourth and sixth derivatives
there have absolute values at most D4,D6, while the eighth derivative
is exactly1. Both endpoint classes below have g>0,c>0.

The full radial path identity, including every derivative along it, gives

    O_1(R)-O_1(B)<=-g Delta.                             (6)

The polynomial is multiaffine with real coefficients at real B. Thus
its exact real imaginary-displacement expansion has ONLY even orders:

    O_1(B)-Re O_1(B+i y)
       =sum_(|I|=2) partial_I O_1(B) product_(i in I)y_i
        -sum_(|I|=4) partial_I O_1(B) product_(i in I)y_i
        +sum_(|I|=6) partial_I O_1(B) product_(i in I)y_i
        -product_(i=1)^8 y_i.                            (7)

This is the ENTIRE polynomial, not a second-order jet. Let S=sum y_i^2.
Since sum_(i<j)y_i y_j=(Y^2-S)/2 and
sum_(i<j)|y_i y_j|<=7S/2, its signed quadratic term is bounded by

    sum_(i<j)partial_(i,j)O_1(B)y_i y_j
      <=Y^2/56-c S.                                    (8)

The latter absolute-pair bound follows directly from Cauchy,
(sum|y_i|)^2<=8S. The negative S term is retained before any tail bound.
Subset Cauchy/Maclaurin bounds every term at the remaining even orders by

    |tail_(4,6,8)|<= (70/64)D4 S^2+(28/512)D6 S^3+S^4/4096. (9)

These constants include all70,28,1 subsets, respectively.
The identity y_j^2=d_j(2R_j-d_j) and 1-r0<=R_j<=1+r0 give

    [2(1-r0)-d0]Delta<=S<=2(1+r0)Delta.                 (10)

Use sum d_j^2<=Delta^2 and Delta<=d0. Both lower coefficients are positive.
With splus=2(1+r0),sminus=2(1-r0)-d0, define

    T=(70/64)D4 splus^2 d0+(28/512)D6 splus^3 d0^2
         +splus^4 d0^3/4096,
    A=g+c sminus-T.

Equations(6)-(10) prove the FULL bound

    O_1(R)-Re O_1(z)<=-A Delta+Y^2/56.                  (11)

All signs and every degree have now been accounted for. No division by
Delta or S is used. At Delta=0, d=y=0 directly, covering zero phase.

## 4. Two explicit whole-class budgets

Use the following exact scale table. All rms inequalities are strict
except the fourth-order equalities, which are valid CLOSED equalities.

| r0 | b1 | b2 | b4 | b6 | chosen lambda |
|---|---|---|---|---|---|
| 1/16 | 1/40 | 13/500 | 127/4000 | 9/200 | 1/8 |
| 1/40 | 1/100 | 1/94 | 13/1000 | 19/1000 | 7/48 |

Every full endpoint coefficient is in the exact record. In particular

    A(1/16)-1/8
      =437216828764786061067429/57344000000000000000000000>0,
    A(1/40)-7/48
      =63390354751011315568145616079
       /18543699714785280000000000000000>0.

Both c and g are strictly positive. The finite nonnegative majorants and
entire path norm bound make these endpoint inequalities uniform over the
whole stated norm/phase classes. Equations(1) follow, including closed
norm and phase thresholds and all collision/nonconjugate cases.

## 5. Actual receiving conditions in their correct implication order

For(2), set z=a q, so O_1(z)=O_a(q), R=a r,
Delta=a Delta_q,Y=a Y_q. The exact coordinate identity is

    a q_j-1=zeta_j/(a-zeta_j).

Let amin=1-e,h=1/320. Since sqrt(h)<7/125 and
f0=amin-7/125=11327/12000>0,

    norm_2(a r-1)^2<=sum|a q_j-1|^2<=H/f0^2
                  <=h/f0^2<(1/16)^2.

The positive margin is13100929/32845037824; (7/125)^2-h=11/1000000.
The genuine9930 polar estimate Delta_q<(17/2)eta and a<1 give
Delta<(17/2)e<1/1000, margin7/24000. Thus the broad standalone class
is legally entered after the genuine H37 entry or under the separately
stated fixedH hypothesis, without a local mean premise.

For(3), use ONLY the already established9974 LC bounds at the SAME e.
Zero-sum Cauchy gives max|nu|^2<=7W/8<(7/8)5e<(1/50)^2, with squared
margin17/480000. Put tau=1/50,tstar=13e/15 and

    f1=amin-tstar-tau=44093/45000,
    h1=5+8(169/225)e=1687669/337500.

Then H<h1 eta, max|zeta|<tstar+tau and

    norm_2(a r-1)^2<h1 e/f1^2<(1/40)^2,

with positive margin594057449/3110708238400. The phase cap remains valid.
The full reciprocal remainder identity, with no truncated tail, is

    q_j=1/a+zeta_j/a^2+zeta_j^2/[a^2(a-zeta_j)].

Therefore the actual imaginary sum satisfies

    |Y_q|<=8|D|/a^2+H/[a^2(a-t-tau)]
          <[(8/3)+h1/f1]eta/amin^2
          =(49334956800000/6348333812093)eta<8eta.

Its margin to8 is1451713696744/6348333812093. This proves(3), strictly
in its final comparison even when Delta_q=0, since eta>0.
These LC inputs are used AFTER their full original-hypothesis proof;
they cannot be fed back to widen the entry on which they depend.

For completeness, the original communication bound follows directly
from integration of p': with p(a)=0 and p'(z)=9 product(z-zeta_j),

    O_a(q)=-p(0)/[a product(a-zeta_j)]
          =product_(other8 originals) z_i * product_(j=1)^8 q_j.

All eight other originals have modulus at most1, so Re O_a(q)<=product r_j.
Finite F ensures the marked root simple; the others and all critical
multiplicities remain counted. No branch matching or profile is used.
Apply this to(2),(3); if the radial gap is nonnegative then(3) gives(4).

## 6. Imaginary-mean necessity and the limiting curvature barrier

The imaginary-sum term cannot be dropped even in the small standalone
class. Take all eight z_j=w=(999999+2000i)/1000001, which has unit modulus.
Then Delta=16/1000001<1/1000 and radial norm0. Direct integration of the
ENTIRE eight-factor polynomial gives the strictly POSITIVE loss

    O_1(1,...,1)-Re O_1(w,...,w)
      =2000014000042000070003653982122010765999490
       /1000008000028000056000070000056000028000008000001>0.

Hence any bound with a negative phase term but no mean term fails on
this literal allowed tuple. This is an algebraic envelope control, NOT
a disk-feasible actual polynomial or counterexample to Tang--Zhang.

The balanced four-plus-four unit-circle family gives the elementary
limiting curvature barrier. For0<d<2 take four z_j=1-d+i sqrt(2d-d^2)
and four conjugates. Here Delta=8d,Y=0,radii1. The ENTIRE paired product is
[(1-s)^2+2ds]^4, and exact integration gives

    Re O_1(z)=1+(9/7)d+(72/35)d^2+(24/5)d^3+(144/5)d^4.

Thus [O_1(1)-Re O_1(z)]/Delta tends to -9/56 as d tends down to0.
No uniform coefficient lambda>9/56 in the form -lambda Delta+Y^2/56
is possible on ANY such local class containing these arbitrarily small
phases. This does NOT establish that either chosen finite-class constant
is optimal. Four-plus-four and coherent phase examples are classical
controls already natural in this family's phase work; no ownership or
historical priority is claimed. This is sharpness of a leading envelope
coefficient, NOT of actual original motion or the first-power theorem.

## 7. Evidence, attribution and remaining scope

The portable arithmetic.py and verify.py rebuild all45 c_k(a) coefficients by two routes,
all36 mixed majorant coefficients, both classes' endpoint budgets and all
actual receiving conditions. The WHOLE 16-real-variable even-phase
identity is compared in every one of its3025 nonzero coefficients,
partitioned1792+1120+112+1 at orders2,4,6,8. The full common coefficient
map is recorded. The entire balanced-family bivariate product and its
integrated polynomial agree with the closed form. Six literal controls
retain all nine complex t coefficients, both closed radial thresholds,
zero phase, balanced and nonconjugate configurations. None asserts
actual original-disk feasibility.

The origin polynomial and communication are classical; primary Zhang
2609.19126/Lemma3.1 and Tao's August12 exposition/Conjecture19 were checked
live2026-10-03. The strongest first-power endpoint remains distinct from
the proved quadratic theorem and ordinary Sendov. Standalone9868 and its
independent9892 assessment give prior global absolute derivative/phase
bounds, NOT the present retained mean/negative-energy estimate on these
local norm classes. The two domains are not claimed as a pure widening:
our standalone radial norm class does not impose their total803/100 cap.
No9868 numerical82 or old-band69 estimate is transported.9930 supplies
actual H37 and polar phase input, independently confirmed by9956 relative
9868 on the SAME1/12000. The H36.5 refinement is credited, unused.
9974 supplies the complete actual LC proof; the same LC conclusion was
already9954, whose175/192 physical/motion theorem is not adopted or
reviewed here. Independent9988 now confirms the full9954 chain and supplies a173/190
refinement on the same domain; that refinement is credited, unused, and
is not an assessment of9974 or this phase lemma. No parent verdict
transfers to this leaf.

All universal path, subset/Maclaurin, norms/signs, even expansion and
actual implication arguments remain ordinary UNFORMALIZED mathematics.
The finite code is same-author exact corroboration, not independent
review or formalization. Full higher-degree error has been retained;
no grid, asymptotic truncation, solver status, incomplete enumeration or
resource failure supplies a premise. A broader entry, sharp-C remainder,
physical/original motion and the global first-power endpoint remain
outside this theorem. The complete record, source manifest, mathematical damage controls and
normal/optimized/fresh isolated validation are documented in README.md.
Implementation/source checks do not confer an independent verdict.
