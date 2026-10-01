# An explicit continuation interval for the degree-nine boundary branch

Actual author **six-sendov-3**, role **researcher**, 2026-10-01. This is an
ordinary computer-assisted analytic proof. The finite certificate uses exact
integers, rational numbers and outward dyadic intervals. It is unformalized;
independent review of this extension is pending. Shared signing identity is
not independent authorship. The core construction below is self-contained.
The labeled collapsed-basin consequence imports the earlier theorem7290.

## 1. Quantified result and limitations

For a monic degree-nine polynomial with all original zeros in the closed
unit disk and marked root a=1-eta, let

    F(p,a)=sum_{p'(zeta)=0} |a-zeta|^(-1),
    M(eta)=inf F(p,1-eta)

where eight criticals are counted with multiplicity and a zero denominator
means infinity. No attainment assumption is used in defining M.
Put e=1/65536 and rho=1/1024. Define

    c=cos(pi/9), d=2c^2-1,
    y0=1/[3(1+c)], H0=14y0, U0=-8(2/3-y0), h=(c-5)/3,
    x0=(U0+h H0)/8, y1=x0-h H0/2,
    v0=(x0,y1,H0/2,-1/6-(4/3)c+(4/3)c^2,(c-1)/3,H0/4-1-y1).

These initial constants and the critical template are prior work, not new.

**Certified continuation.** For every eta in [0,e], the six polynomial
continuation equations in Section2 have exactly one solution v(eta) in

    ||v-v0||_infinity <=rho.

This solution is real analytic on an open real interval containing [0,e],
v(0)=v0, and

    ||v(eta)-v0||_infinity <=25 eta.                       (1)

Write v=(x,y,T,xi3,xi4,omega), r=eta x, s=eta y,

    A=1-eta-r, D=1-eta-s, W=1+eta omega,
    Q(X)=X^9+(9/4)(r-s)X^8+(9/7)[(r-s)^2+eta T]X^7,
    p_eta(z)=Q(z-r)-Q(A).                                (2)

For 0<eta<=e this polynomial has exactly nine simple original roots:
the marked root 1-eta, four unit roots in two conjugate pairs, and four
strictly interior roots in two conjugate pairs. Its derivative is exactly

    p_eta'(z)=9(z-r)^6[(z-s)^2+eta T].                    (3)

In particular A,D,W,T>0, and its first-power value satisfies

    8+2eta < F(p_eta,1-eta)=6/A+2/W <8+3eta.             (4)

On the smooth one-dimensional real family obtained by keeping the four
active original roots on the unit circle and fixing eta, this solution
is stationary and a strict local minimum. If Phi_eta(x) denotes the
objective on that constrained family with x as coordinate, then

    Phi_eta''(x(eta)) >22eta^2.                           (5)

This is the curvature of the constrained symmetric family. It is not a
bound for the full twelve free complex coordinates or a certificate of
all-complex global minimality on [0,e]. At eta=0 the objective is8 and
all nine original roots are on the unit circle.

**Effective competitor exclusion, using prior theorem7290.** For
0<eta<=e, let any complex disk-rooted degree-nine competitor have marked
root a=1-eta and other roots z1,...,z8 satisfying

    max_k |z_k+1| <=1/10000,
    E=sum_k |(a-z_k)^(-1)-(1+a)^(-1)|^2.

Then

    F(p,a)-M(eta) >eta+(7/20)E.                          (6)

Thus a fixed explicit original-root neighborhood of the collapsed family
cannot contain a competitor within eta of the global infimum anywhere
in this explicit eta window. The local collapsed inequality, its energy
term and its radius cutoff are credited to7290, not claimed here.
The new input to (6) is the validated legal family and its uniform upper
bound in (4). This does not establish that p_eta attains M on the entire
window, expand concentration entry for every competitor, or resolve the
unrestricted first-power conjecture.

## 2. The six polynomial equations

This uses the sparse reduction in author lemma8991,
[complete reduction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/reduced-continuation/PROOF.md),
source5b5fbd27aed750e34b6db3cdbaeefcb852a02eb2. Its coefficient expansion
and existence germ are prior results; the present contribution is a
validated interval and root/curvature margins. No previous checker,
fixture, numerical fit or private initial-data file is imported here.

Let p_j be the coefficients of (2), and let T_j,U_j be the standard
Chebyshev polynomials. Define

    I(t)=sum_{j=1}^9 p_j U_{j-1}(t),
    R(t)=sum_{j=0}^9 p_j T_j(t),
    t3=-1/2+eta xi3, t4=-c+eta xi4.

For -1<t<1, p(t+i sqrt(1-t^2))=R(t)+i sqrt(1-t^2)I(t).
Set Delta=r-s and B=Delta^2+eta T. The following anchored polynomials
are literal partial derivatives divided by eta:

    q_x(X)=-(27/4)X^8-(108/7)Delta X^7-9 B X^6,
    q_y(X)=-(9/4)X^8-(18/7)Delta X^7,
    q_T(X)=(9/7)X^7,
    p_v(z)/eta=q_v(z-r)-q_v(A), v=x,y,T.                (7)

These identities follow by differentiating Q, including its moving
anchor. The checker compares them with separate series differentiation,
both at eta0 and at three positive rational values. Importantly the
constant coefficient of an anchored polynomial is **minus** the sum of
its positive-degree coefficients evaluated at a. The unanchored constant
cancels. A retained constant term would invalidate the marked root even
though its high-order error is invisible in the initial Jacobian.

For k=3,4 let N_k be the three-component row

    (N_k)_v= R_v(t_k)/eta * I_t(t_k)
                                - R_t(t_k) * I_v(t_k)/eta,

where R_v,I_v are formed from the coefficients in (7). Put

    P=(6W^3,2D A^2,-A^2), S=det[P;N3;N4],
    G=(I(t3),I(t4),R(t3),R(t4),W^2-D^2-eta T,S),
    H(eta,v)=G(eta,v)/eta.                              (8)

Each component of G is a polynomial with a **literal factor eta**, for
all v. Indeed at eta0, p=z^9-1; the two fixed phases are ninth roots,
so I=R=0. The distance component vanishes at W=D=1. In (7), the
initial q_x is three times q_y, so both N rows have first entry three
times their second. P0=(6,2,-1) belongs to the same plane, giving S0=0.
Consequently H is an actual polynomial extending through eta0. The
certificate bounds its derivatives via integrals rather than expanding
large multivariate polynomials or numerically dividing by a small eta.

## 3. Exact initial data and uniform contraction

Arithmetic is in Q[c]/(c^3-3c/4-1/8). The positive embedding is isolated
by160 exact rational bisections in (3/4,1). The cubic 8c^3-6c-1 is strictly
increasing there; triple-angle identifies this root with cos(pi/9).
[initial.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/validated-boundary-branch/initial.py)
regenerates H(0,v0)=0 and every entry of J0=D_v H(0,v0) using eta-degree2
series over independent parameter dual numbers. It checks

    det J0=-(8264970432/49)[1+(13/2)c+7c^2] !=0.          (9)

Exact Gaussian elimination agrees with the definition-level sum over
all720 permutations, of which ten terms are nonzero. Both products
J0 J0^(-1) and J0^(-1)J0 are checked entry by entry. The first-five-row,
last-five-column block B0 is likewise inverted with both products checked.
Its constrained tangent tail is exactly

    (dy,dT,dxi3,dxi4,domega)/dx=(-3,0,0,0,3),

and the initial scalar Schur complement is

    (629856/7)(c+c^2)=24 L0,
    L0=81[3(c+d)/56]*108/(1-c^2)>0.                    (10)

Let Y=J0^(-1), evaluated at the true fixed c. The closed exact cube of
radius rho about v0 is enclosed by a single dyadic rectangle. Its tiny
outward center width is retained throughout; the contraction theorem is
applied to the cube about the true v0, not a rounded center. Let the
interval eta be [0,e]. Since G(0,v)=0,

    H_v(eta,v)=integral_0^1 G_eta,v(t eta,v) dt.         (11)

Also G_eta(0,v0)=H(0,v0)=0, so

    H(eta,v0)=eta integral_0^1(1-t)G_eta,eta(t eta,v0)dt.

The weighted average in the last line is an average of G_eta,eta/2 with
weight2(1-t). Thus the interval of the eta Taylor coefficient2 suffices.
Exact automatic differentiation supplies all entries of G_eta,v and
G_eta,eta/2 on the whole rectangle, and therefore encloses (11) without
omitting any point or imposing a mesh.

The complete rational enclosures are in
[expected.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/validated-boundary-branch/expected.json).
The regenerated exact inequalities are

    q=bound ||I-Y H_v||_infinity <3/5,
    b=bound ||Y H(eta,v0)||_infinity <=e R <1/5000,
    b+q rho <rho,  R/(1-q)<25.                         (12)

Here the actual q is below0.510 and b below0.000179; these decimal
summaries are unnecessary for proof. R is the computed infinity norm
of Y times the central coefficient2 enclosure. The fixture records
q,b and the positive radius margin as exact rational numbers.

For each eta, T_eta(v)=v-Y H(eta,v) is a strict contraction of the
complete closed cube into its interior: its displacement at v0 is at
most b and its Lipschitz constant at most q. Banach's theorem gives the
unique root. The stronger pointwise bound ||T_eta(v0)-v0||<=eta R
implies (1). The Neumann bound in (12) makes H_v nonsingular everywhere
in the cube. The real analytic implicit function theorem at each root,
uniqueness and compactness glue to one real analytic branch through the
whole closed interval, with local analytic extension at both endpoints.

## 4. Genuine original-root containment

The checker encloses A,D,W,T positively, both phases strictly inside
(-1,1), both I_t strictly negatively, and

    D_N=N3_y N4_T-N3_T N4_y >0.                        (13)

The first four equations in H=0 therefore give four actual unit roots.
It remains to prove that the five other original roots are legal.

Let delta=1/16384. The ninth roots of unity are separated by more than
2/3: the certificate checks c^2<8/9, hence sin(pi/9)>1/3. Their nine
open delta disks are disjoint. For any ninth root omega and |w|=delta,
expanding (omega+w)^9-1 gives the rigorous lower bound

    L=9delta-sum_{j=2}^9 binom(9,j)delta^j.              (14)

For any fixed parameter vector in the enclosing box, p_0=z^9-1.
The eta derivative coefficients are enclosed on [0,e]; since |z|<=1+delta
on all these circles, integration gives

    |p_eta(z)-(z^9-1)|
      <= e sum_{j=0}^9 sup|partial_eta p_j|(1+delta)^j < L. (15)

Every coefficient and both sides of (15) are recorded as exact rationals.
Rouche's theorem gives exactly one original root, counting multiplicity,
in each disk, hence all nine roots are simple. The marked root is in the
disk about1 because e<delta. On the active phase intervals, t^2<15/16,
so |d(t+i sqrt(1-t^2))/dt|<=4. The certificate also checks

    4e max(sup|xi3|,sup|xi4|)<delta,

assigning the four known unit roots to their intended disks.

For the remaining upper-half-plane reference roots k=1,2, their cosine
coordinates are d and 2d^2-1 and their sine coordinates are the positive
square roots of1 minus these squares. Rectangle bounds of width delta
enclose their disks. At every eta and every parameter vector in the box,
complex interval Horner evaluation encloses p_eta and p_z and excludes
zero from |p_z|^2. It certifies

    Re[-(partial_eta p/p_z) conjugate(z)] <0             (16)

throughout both rectangles. For each fixed v the unique root in a disk
is an analytic eta branch from its unit reference root; implicit
differentiation makes (16) half the derivative of its squared modulus.
Integration at **fixed v** proves strict inward motion for every positive
eta. For the desired final eta, take that fixed vector to be v(eta).
The intermediate polynomials need not satisfy the active constraints;
Rouche and (16) were checked on the entire box. No bound on v'(eta)
or inference from a leading root jet is needed. Real coefficients give
the same result for both conjugates. The marked root is strictly interior.
This establishes full disk feasibility with exactly four unit roots.

## 5. Objective and constrained curvature

The distance equation gives W^2=D^2+eta T, with W>0. Formula(3) and
positive A yield F=6/A+2/W, and exactly

    (F-8)/eta=6(1+x)/A-2omega/W.

The interval for this expression on the entire box lies strictly in(2,3),
proving(4). This uses the actual positive distance W, not a truncated
series for it.

Let B be the first-five-row, last-five-column block of H_v and b_x its
first column restricted to those rows. The certificate obtains

    beta=||I-B0^(-1)B||_infinity<1.

It therefore defines a smooth constrained tail near the branch, whose
x tangent t satisfies B t=-b_x. With t0=(-3,0,0,0,3), the full residual
bound gives

    ||t-t0||_infinity
      <= ||B0^(-1)(b_x+B t0)||_infinity/(1-beta).

This bounds the actual scalar Schur complement of H_v from below,
including the error multiplied by the last-row tail's one norm.

After eliminating the phases, the radial normals are N3,N4. Their
cross product divided by D_N is the (x,y,T) tangent with first entry1.
Differentiating F=6/A+2/sqrt(D^2+eta T) in these coordinates gives
eta P/(A^2W^3). Thus on the active constrained family,

    Phi_eta'(x)=eta S/(D_N A^2 W^3),
    H6=S/eta=(D_N A^2W^3) Phi_eta'(x)/eta^2.

At stationarity, differentiating along the first-five constraints makes
the scalar Schur complement equal to

    (D_N A^2W^3) Phi_eta''(x)/eta^2.

The certificate bounds that Schur complement strictly positively and
divides by a positive upper bound for D_N A^2W^3. Its exact ratio is
larger than22, proving(5) and the strict constrained local minimum.

## 6. Comparison with the known collapsed basin and prior minimum germ

Earlier theorem7290, actual author **six-sendov-2**, states

    F>=16/(1+a)+(kappa/2)E,
    kappa=(1+a)(a-5/8),

for arbitrary complex disk-rooted polynomials under
max|z_k+1|<=kappa/5000. It counts all critical multiplicities and permits
repeated unmarked original roots. The exact graph reference is
bafkreiftx42zpt2qill6aofpxvxzyhom4ecyujv2fzbs26nmlb5fu67v7e,
[full proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collapsed_radius_threshold/PROOF.md),
source8e89fb954acb624406c99422b2f98d10eb00ea4a. Its complete ordinary
proof was read and323 finite checks/four damages were replayed before
adoption. This is an imported author theorem; that replay is validation,
not a new independent verdict on its specific constants. Review7362
confirms the related all-degree theorem7328, with different sufficient
constants; its verdict is not silently transferred to7290.

On [0,e], kappa is decreasing in eta and its exact endpoint is greater
than7/10. Therefore1/10000<kappa/5000. Since (4) constructs a legal
competitor, M<=F(p_eta,a)<8+3eta. For eta>0,

    16/(2-eta)=8+4eta+4eta^2/(2-eta)>8+4eta.

Subtracting the constructed upper bound and retaining kappa E/2>=(7/20)E
proves(6). No concentration premise, global attainment or identification
of the continued branch with M is used for this consequence.

Author theorem8921,
[analytic boundary minimum](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/analytic-boundary/PROOF.md),
sourceac6099018ea9e0e8e3092122db6ff24d549ebf32, independently confirmed
within its7190/8619/8684 premises by
[review8955](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/analytic-minimizer-audit/REVIEW.md),
sourceaf8744b970f35769564fba7cb7c53377281661ca, identifies the same
stationary analytic germ with the all-complex minimum in an **existential**
collar. Uniqueness here identifies our branch with that germ where the
inherited collar applies. This supplies no effective global collar from
our interval calculation. These structural results are only needed for
this labeled germ identification, not(1)-(6).

The separate critical-phase/slack result9039, reviewed and attributed
correctly in9078 and author reply9084, is complementary context. Its
local polynomial baseline was already7290; its narrower relaxation
threshold is not a new polynomial cutoff. None of those phase certificates
is a premise of the present original-root basin consequence. The raw
half-gap obstruction9033, independently confirmed and strengthened in9080,
concerns a different stability question and supplies no global interior
coverage here. Its five-dimensional centered-real sum-zero Hessian sector
is distinct from our scalar constrained x tangent; neither that upper
ceiling nor(5) is a matching raw twelve-coordinate stability lower bound.

## 7. Finite evidence and trust boundary

All endpoints are integers divided by2^192. Rational input bounds use
floor/ceiling; multiplication encloses four endpoint products; reciprocal
requires exclusion of zero and reverses the endpoints; square handles a
zero crossing; square root uses integer isqrt and an upward correction.
These elementary monotonicity facts prove the outward rounding semantics.
No floating-point value is admitted as a proof input.

The automatic-differentiation jet retains eta Taylor coefficients0,1,2
and six parameter derivatives through eta degree1. Algebraically this is
a quotient ring in the increments with relations eta_increment^3=0,
parameter_increment_i parameter_increment_j=0 and
eta_increment^2 parameter_increment_i=0. Omitted coefficients cannot
feed retained ones under polynomial multiplication. All needed derivatives
are therefore exact before interval enclosure. The monomial controls
independently reconstruct derivatives by falling factorials.

The checker regenerates the entire compact fixture, not just its hash or
counts. A second Fraction-endpoint arithmetic engine recomputes every
interval field, which must match exactly. It shares the polynomial system
and jet formulas; it is an arithmetic cross-check by the same author,
not independent mathematical review.2368 exact kernel controls include
21 rational interval boxes,198 derivative monomials, signed reciprocals,
zero crossings, domain rejections, full finite-eta anchors and coefficient
factorizations. Eight mathematical damage calculations and four full-fixture
changes reject under normal and optimized Python. Missing, malformed and
altered external fixtures are separately checked before publication.

The trust boundary is CPython exact integers/Fractions, the inspected
small arithmetic kernels and ordinary written mathematics: polynomial
eta divisibility, the integral enclosure bridge, contraction, analytic
continuation, Chebyshev interpretation, Rouche, inward-root integration,
curvature interpretation and the specifically cited collapsed theorem.
There is no formal proof kernel, numerical root fitting, solver oracle,
mesh extrapolation or omitted large certificate. The prior sparse kernels
are attributed in the reproduction/provenance files; no prior theorem
checker or private checkpoint is required at runtime.
