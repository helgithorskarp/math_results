# A complete threshold certificate for a deep simplex-flap cell

Complete author proof with exact computation, 27 September 2026.
Independent review is pending. The unrestricted R3 Gaussian-majorisation
question remains open. This theorem is at covariance I_3; it asserts no
all-variance class or new Kneser--Poulsen volume consequence.

## 1. The input and the sign

Let V consist, in order, of

    (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1).

There are sixteen labels: four cores i, followed by the twelve ordered
pairs (i,j), i!=j, in lexicographic order. Define reference sites

    a_i=v_i/2,                 b_i=(63/64)v_i/2,
    a_ij=(v_j-2v_i)/2,         b_ij=(63/64)(v_j+2v_i)/2.    (1)

Every label has weight 1/16. The continuous parameter cell consists of
ALL independently chosen source and target sites with

    |x_l-a_l|_infinity<=1/2048,
    |y_l-b_l|_infinity<=1/2048.                            (2)

Write gamma for the Gaussian with covariance I_3, C=(2pi)^(-3/2),
f=(1/16)sum gamma(.-x_l), g=(1/16)sum gamma(.-y_l), F=f/C, G=g/C, and
use the adverse sign convention

    H(u)=integral(f-Cu)_+-integral(g-Cu)_+.

**Theorem.** Every member of (2) is a strict contraction and satisfies

    H(u)<=0                         for every u>=0,
    H(u)<=-C u/2                    for 0<u<=1/512,
    H(u)<-1/128                     for 1/512<=u<=9/32.    (3)

Consequently every convex-energy comparison holds at this fixed variance.
The 96 coordinate parameters in (2) are independent. A slice fixing the
two label-0 sites has 90 parameters; separate translations then put both
label-0 sites at zero. No symmetry is imposed on actual cell members.

The depth-two geometry is motivated by classical simplex flaps. The team's
all-variance selector closure concerns orthocentric depth one, and does not
state (3). The undamped full labelled flap has the classical obstruction
to a contracting motion in R5. We do **not** transfer that obstruction to
the damped or perturbed cell, nor exclude every alternative positive proof.
The contribution here is a signed computation covering an entire rational
frontier cell with extended, nonpoint targets. Its low tail uses integrated
superlevel volumes. It is not a new classification of flap depths.

## 2. Geometry, normalization, and rational-frontier membership

Put e=1/1024. The Euclidean displacement in (2) is less than e. Reference
means are zero, and direct exact computation gives

    min_(l!=m)(|a_l-a_m|^2-|b_l-b_m|^2)=127/2048,
    min_(l!=m)|a_l-a_m|^2=2,
    min_(l!=m)|b_l-b_m|^2=3969/4096,
    E|a_l|^2=15/4.

Every actual source lies in B(0,R_X), R_X=9/4, and every actual target in
B(0,R_Y), R_Y=27/16. In perturbing a pair, its two endpoint difference
vectors move by at most 2e each. The lower source-distance bound is
positive. Squaring lower/upper distance bounds cancels the 4e^2 terms, so

    actual loss >=127/2048-4e(2R_X+2R_Y)=1/32.             (4)

Both endpoints remain injective. The six paired differences at labels
1,2,3,4,7,10 from label 0 have determinant -250047/4096 at the reference
input. Thus the cell contains paired-rank-six inputs, including a relatively
open neighborhood of that input. Rank six is not assumed for every member.

Subtract x_0 and y_0 separately. This preserves pair losses and both hinge
profiles; the radii are at most 2R_X=9/2 and 2R_Y=27/8, both below 6.
The lattice slice of (2) with denominator 2048 therefore lies, after that
anchoring, in R3's unchanged family R^c_2:

    A_2=888, L_2=2048, W_2=7104, weight units=444 per label.

There are 16<=888 labels, and (4) exceeds its required loss 1/4096.
The cell contains lattice moves of one full coordinate unit. Fixing the
two initial sites to their reference positions gives a literal
90-coordinate box in the anchored gauge, after a fixed translation.
The finite-to-global-map interpretation uses the same Kirszbraun extension
premise as the rational frontier. The endpoint inequalities need no extension.

## 3. Turn the low hinge into a volume sign

For u>0 let V_F(u)=|{F>u}| and V_G(u)=|{G>u}|. Equal total mass and layer
cake give exactly

    H(u)=-C integral_0^u [V_F(v)-V_G(v)]dv.                 (5)

Each clipped-density integral is finite; Tonelli justifies this identity
also as the lower limit tends to zero. It suffices to prove

    V_F(exp(-S^2/2))-V_G(exp(-S^2/2))>1/2,
                                             S>=7/2.    (6)

Indeed exp(-49/8)>1/512 is certified, so (5) proves the low part of (3).

Both superlevel sets in (6) are star shaped, with one radial boundary on
each ray. Here is a uniform verification, rather than an assumption about
mixture unimodality. Within |z|<=9/4, Jensen and the mean/norm bounds give

    F(z),G(z) >= exp[-141/32-(9/2)e-e^2/2]
               > exp(-49/8).                             (7)

For F this uses |E X|<=e and E|X|^2<=15/4+(9/2)e+e^2. The target has
a smaller reference second moment and obeys the same upper bound. Beyond
radius 9/4, every Gaussian summand decreases strictly along each ray,
because all its centers have smaller norm. The densities tend to zero.
Thus (7), continuity, and that monotonicity prove the claimed radial
description. Denote the radii at level exp(-S^2/2) by rho_F(S,theta) and
rho_G(S,theta). Both increase with S, and

    V_F-V_G=(1/3) integral_(S^2) (rho_F^3-rho_G^3)dOmega.   (8)

Sections 4--5 certify (6) on 7/2<=S<=64. Section 6 proves it for all S>=64.
This avoids extrapolating a finite threshold sample to the endpoint zero.

## 4. A complete angular cover and verified radial bounds

The reference arrays and equal weights are invariant under all coordinate
permutations and even sign changes, a group of order 24. Apart from walls
of spherical area zero, the sphere is covered once by that group's images
of the TWO patches

    theta_+(u,v)=(u,v,1)/sqrt(1+u^2+v^2),
    theta_-(u,v)=(-u,v,1)/sqrt(1+u^2+v^2),
                                      0<=u<=v<=1.        (9)

The surface Jacobian is J=(1+u^2+v^2)^(-3/2). The actual configurations
need not be symmetric: the same displacement estimates hold on every
image of a patch, after relabelling the symmetric reference centers.
Thus every bound below applies on the whole sphere to every member of (2).

For a positive integer n subdivide the triangle in (9) into squares

    i/n<=u<=(i+1)/n, j/n<=v<=(j+1)/n, 0<=i<j<n,

and the triangular halves of the diagonal squares i=j. Areas are 1/n^2
and 1/(2n^2), respectively. For a diagonal piece we enclose its containing
square. This only enlarges an enclosure, and does not double its area.

Let theta_c be the image of the square center. On the square,

    |theta-theta_c| <= d_ij
      := 3/[4n sqrt(1+(i/n)^2+(j/n)^2)].                  (10)

To prove this, the derivative norm of w/|w| is at most 1/|w|, and the
parameter distance to the square center is at most sqrt(2)/(2n)<3/(4n).
The straight parameter segment stays in the square. Bounds J^- and J^+
are obtained at its upper-right and lower-left corners.

For each source reference a_l and target reference b_l define rational
OUTWARD bounds, also rounding each dot/norm bound to denominator 2^40:

    d_l^- <= theta_c.a_l-|a_l|d_ij-e,
    n_l^+ >= |a_l|^2+2|a_l|e+e^2,
    d_l^+ >= theta_c.b_l+|b_l|d_ij+e,
    n_l^- <= |b_l|^2-2|b_l|e.                             (11)

Square roots and reciprocal square roots use pinned integer-square-root
enclosures. Signed dot products select the appropriate interval endpoint.
For all actual sites and all directions in that patch,

    F(r theta) >= (1/16) sum_l exp(-r^2/2+r d_l^- -n_l^+/2),
    G(r theta) <= (1/16) sum_l exp(-r^2/2+r d_l^+ -n_l^-/2). (12)

At each required S the program proposes r_F^-,r_G^+ in 2^(-20)Z, both
above 9/4. It then checks the two exact interval inequalities

    sum_l exp(S^2/2-(r_F^-)^2/2+r_F^- d_l^- -n_l^+/2)>16,
    sum_l exp(S^2/2-(r_G^+)^2/2+r_G^+ d_l^+ -n_l^-/2)<16. (13)

These prove rho_F(S,theta)>=r_F^- and rho_G(S,theta)<=r_G^+.
The ordinary floating-point bisection in `root_proposal` only guesses the
two rational numbers. It is not a proof premise: any wrong guess fails
(13). Neither a floating Gaussian value nor a sampled radius is used to
accept a sign. A different proposal routine is permitted if every exact
check remains in place.

The interval exponential is integer arithmetic. For a dyadic q>=0 it
scales q to r<=1/8. Integer lower/upper recurrences enclose r^j/j! and
the alternating partial sums. An odd partial sum bounds exp(-r) from
below; the previous even sum bounds it from above. When the next odd
term is at most one working unit, those outward partial-sum bounds are
squared back, rounding outwards after each square. The working precision
is 50+2k+16 bits for k squarings. The output encloses exp(-q) at 50 bits
and has width at most two units; that invariant is checked. Positive
relative exponents use reciprocal bounds, with outward integer division.
All exponents in (13) are exact dyadics. The proof rests on the alternating
series and interval induction, not on comparison with a numerical library.

## 5. Signed finite windows, with no gaps

For each adjacent S-window [S_a,S_b], monotonicity in S implies

    rho_F(S,theta)^3-rho_G(S,theta)^3
          >= D_patch := r_F^-(S_a)^3-r_G^+(S_b)^3.         (14)

Multiply a nonnegative D_patch by J^- and a negative D_patch by J^+.
Then eight times the sum of these products times their parameter areas is
a lower bound in (8); the factor is 24/3. In particular negative patch
contributions are retained with the correct adverse rounding.

The finite cover is

| S range | step in S | angular n | signed patches | windows | verified radii |
|---|---:|---:|---:|---:|---:|
| [7/2,6] | 1/16 | 24 | 600 | 40 | 49,200 |
| [6,64] | 1/8 | 12 | 156 | 464 | 145,080 |

All 504 sums are strictly greater than 1/2. The smallest first-band bound
is greater than 20; the smallest second-band bound is

    2757227753172129861081079005694477
      /3894222643901120721397872246915072 > 1/2.           (15)

They occur on windows starting at 7/2 and 6, respectively. The table covers
all angular patches and all S in [7/2,64], including both transition values.
The stream digests and exact minima are in EXPECTED.json. The large list
of radial brackets need not be distributed: the generator proposes each
one and the verifier checks both its geometry and exponential inequality.

## 6. A uniform far-tail proof

Let h_X,h_Y be actual support functions. At the reference geometry each
undamped target in (1) is a midpoint of two source sites (cores use the
same site twice). The source hull also contains all six points +/-3e_i/2,
as averages of four explicitly listed source sites. The checker supplies
all these convex-combination witnesses. Hence the source support is at
least 6/7 in every direction, and actual perturbations give

    h_X-h_Y >= (1-63/64)(6/7)-2e =3/224-2e>0.             (16)

The actual target hull contains the origin in its interior: its core
tetrahedron has support at least (63/64)(2/7)-e>0. In particular
0<=h_Y<=h_X. The n=12 angular enclosure from (11), with negative gap
lower bounds replaced by zero using (16), gives a rigorous normalized
mean-support gap

    delta=(1/(4pi)) integral(h_X-h_Y)dOmega
       >=45482348743216177507234990463
          /163408085185670196286684397568 >1/4.           (17)

Its factor is 6/pi>=21/11, using pi<22/7, and it uses the LOWER Jacobian.
This is a signed angular enclosure, not sampled mean width.

Set A=269/25, B=277/200. Every actual source norm squared plus 2log16
is less than A, since log16<3. Every actual target norm squared is less
than 2B. The checker verifies these bounds with the perturbation allowance.
For S>=64, a single maximal-projection source summand and the target
upper envelope therefore imply

    rho_F >= S+h_X-A/S,
    rho_G <= S+h_Y+B/S.                                  (18)

For the first inequality solve the source quadratic and use
sqrt(S^2-A)>=S-A/S. For the second use
sqrt(S^2+h_Y^2)<=S+h_Y^2/(2S). The first radius in (18) is positive.
Expanding cubes, retaining the nonnegative terms from h_X>=h_Y>=0,
and bounding the two shifts by the derivative of t^3, (8) gives

    V_F-V_G >=4pi S^2 [delta-E(S)],
    E(S)=A/S (1+R_X/S)^2
                   +B/S (1+R_Y/S+B/S^2)^2.              (19)

E decreases with S. Exact arithmetic gives

    E(64)=1743464522020333/8589934592000000 <21/100.

Thus delta-E(S)>1/25, and (19) exceeds 12S^2/25>1/2 for every S>=64.
Together with Section 5, this proves (6) and the entire signed low endpoint.

## 7. The middle and high endpoint

Let F_0,G_0 denote the reference densities normalized by C. Moving a
Gaussian center by e changes its total variation by at most e/2; use
the directional L1 derivative sqrt(2/pi)<1. Mixture convexity gives the
same bound for each endpoint. An equal-mass hinge changes by at most TV,
so uniformly in u and over (2),

    H(u)<=H_0(u)+e.                                      (20)

The separately reviewed R3 absolute-hinge quadrature is used with
h=1/16, half-grid M=120, coordinate support bound 3/2 and tail T=6.
Its pair error is

    h^2(1+G_h+G_h^2)/4+3G_h^2 exp(-T^2/2)/T,
    G_h=1+h^2/8.                                        (21)

The 241^3=13,997,521 grid sites are represented by 597,861 reference
orbits under the same group of order 24. For absolute coordinates
0<=i<=j<=k<=120, a zero coordinate gives one orbit of multiplicity
2^(number of nonzero coordinates)*6/product(multiplicity factorials).
Otherwise there are two representatives (i,j,k),(-i,j,k), each with half
that multiplicity. This quotient does not restrict the actual cell.

Density values use 48-bit exponential bounds and positive integer sums
of the sixteen product kernels. Source values are rounded up and target
values down. Their adverse hinge polygon is affine between density knots.
An exact sweep includes all 124,991 relevant knots and endpoints in
[1/512,9/32]; thus its maximum bounds the WHOLE interval. Multiplication
of a negative maximum by C uses the LOWER enclosure of C. After (21)
and (20), the uniform adverse bound is

    -345085628268564267007366684564175
       /41538374868278621028243970633760768 < -1/128.      (22)

Finally |grad F_0|<=exp(-1/2)<61/100. Every point in the grid cube is
within 7/128 of a grid point. Outside the cube F_0<=exp(-18). The same
gradient bound and the displacement e imply

    ||F||_infinity <=969464083099761/3518437208883200
                      <9/32.                            (23)

So the source hinge vanishes above 9/32. Equations (5)--(23) prove (3)
with no uncovered thresholds or parameter points.

## 8. Replay and precise trust boundary

Run from this directory, standard-library CPython 3.11 or later:

    python3 -B verify.py
    python3 -B -O verify.py
    sha256sum -c SHA256SUMS

Expected status: GAP_FREE_DEEP_FLAP_CELL_PASS. One author's complete run
takes about two minutes on one CPU. No solver, external dataset, numerical
integration library, or omitted large certificate is required. Floating
arithmetic proposes radial brackets only; every accepted bound is checked
using Python unbounded integers and Fraction. A proposal failure is an
error, never an accepted sign. EXPECTED records this implementation's
diagnostic stream; another valid proposal stream may have different hashes.

The controls compare exponential intervals with higher-precision pinned
rational enclosures, compare every density histogram entry with an
unquotiented implementation on 495 sites, verify 768 sweeps directly at
every knot, check the 24 reference symmetries and exact geometry, and reject
two deliberately wrong radial endpoints. Normal and optimized runs are
author checks, not independent review. The universal radial, symmetry,
layer-cake, perturbation and quadrature reductions remain written mathematics.
Source pinning records the inputs consumed; it does not transfer independent
acceptance to the new computation or its analytic bridges.

This cell does not cover all of R^c_2 or the unrestricted compact frontier.
The accepted global 7/50 defect bound remains unchanged. The seven-factor
beta result and the newly reviewed eighth entry are preserved; no adjacent
beta obligation is computed here. Holding this cell fixed as variance
tends to zero is outside the theorem, so no new ball-volume limit follows.
