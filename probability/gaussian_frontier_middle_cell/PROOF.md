# A gap-free Gaussian certificate on an explicit rational frontier cell

Complete author proof with exact computation, 27 September 2026.
Independent review is pending. The unrestricted dimension-three problem
remains open. This is a fixed-variance cell certificate, not an all-variance
theorem or a new Kneser--Poulsen consequence.

## 1. The cell and the conclusion

Let gamma have covariance I_3 and C=(2 pi)^(-3/2). Set

    a=(0,e_1,-e_1,e_2,-e_2,e_3,-e_3),
    w=(2/13,11/78,11/78,11/78,11/78,11/78,11/78).

The cell consists of EVERY choice of seven source and target sites satisfying

    |x_i-a_i|_infinity <= 1/256,
    |y_i|_infinity <= 1/16.                                  (1)

Put f=sum w_i gamma(.-x_i), g=sum w_i gamma(.-y_i), and use the
**adverse** convention

    H(u)=integral(f-Cu)_+ - integral(g-Cu)_+,    u>=0.          (2)

**Theorem.** For every point of the continuous cell (1),

    H(u)<=0                              for every u>=0,
    H(u)<-1/200               for 1/256<=u<=11/16.             (3)

Thus f is majorised by g at variance one. All 42 coordinate parameters
vary independently in the stated boxes. No geometric symmetry is imposed
on the actual source or target, and target collisions are permitted.
The symmetric source and point target used below are reference laws for
one finite computation, not the full class being certified.

This supplies actual middle signs on a nontrivial cell of the existing
rational frontier. Qualitative neighborhoods of point-target comparisons
already follow from the team's stability results. We do not claim a new
abstract stability theorem or historical priority for its ingredients.
The quantitative content is the explicit cell, the gap-free threshold
cover, its uniform rational margin, and a compact exact replay.

## 2. Membership in the strict rational frontier and paired rank six

Write

    epsilon=1/128, r_Y=7/64, rho=25/8,
    tau=1/256, b=11/16.

Since sqrt(3)/256<epsilon, every source displacement has Euclidean norm
less than epsilon. Also sqrt(3)/16<r_Y. Distinct reference sites have
distance at least one, so every distinct actual source pair has distance
at least 1-2epsilon=63/64. Target pair squared distances are at most 3/64.
Consequently every pair has squared-distance loss at least

    (63/64)^2-3/64 = 3777/4096 > 1/256.                      (4)

Both supports lie in B(0,3). On restricting every coordinate to the lattice
(1/256)Z, (1) is a cell of the unchanged R3 family R^c_1: seven labels are
at most A_1=39; the weights are (24,22,22,22,22,22,22)/156 and W_1=156;
the coordinate denominator is 256; and (4) implies its strict loss floor.
Checking all parameters by sampling or enumeration is unnecessary: (4)
and the analytic perturbation estimates are uniform on their entire boxes.

For a concrete injective paired-rank-six member take x=a and let 256 y_i be

    (0,0,0), (12,4,-3), (3,-11,6), (-8,9,5),
    (7,2,13), (2,-6,11), (-10,7,-4).                         (5)

The checker evaluates the determinant of the six differences (x_i,y_i)
from label 0 exactly and checks all 21 losses and distinct target sites.
Its nonzero determinant is recorded in EXPECTED.json. Rank six therefore
occurs in this cell and in a relatively open neighborhood of (5).
There is no assertion that every member has rank six or that no other
positive theorem can apply to some members. In particular, rank six rules
out using all-order individual conditional-kernel positivity as a premise;
it does not rule out positivity after the actual averages.

## 3. A signed low endpoint uniform on the cell

Write F=f/C, G=g/C, r=|z|. The reference normalized source density is

    F_0(z)=exp(-r^2/2)[2/13+(11/39)exp(-1/2)
                            (cosh z_1+cosh z_2+cosh z_3)].  (6)

The function t -> cosh(sqrt(t)) is convex on t>=0, as follows from its
power series with nonnegative coefficients. Jensen's inequality and
cosh(v)>=exp(v)/2 give

    F_0(z)>=(11/26) exp(-r^2/2-1/2+r/sqrt(3)).              (7)

For |x_i-a_i|<=epsilon and |a_i|<=1, the elementary square expansion yields

    F(z)>=exp[-epsilon(r+1)-epsilon^2/2] F_0(z).             (8)

For r>=r_Y, every target lies in B(0,r_Y), so

    G(z)<=exp[-(r-r_Y)^2/2].                               (9)

Since 1/sqrt(3)>4/7, the ratio of the right sides in (8),(9) is at least

    (11/26) exp[(4/7-epsilon-r_Y)r
                         -1/2-epsilon-epsilon^2/2+r_Y^2/2].

The slope is positive. At r=rho its exponent is the rational

    q_out=210485/229376.

The exact scalar enclosure certifies exp(-q_out)<11/26. Hence F(z)>G(z)
for every r>=rho, uniformly over (1).

Inside the same ball, the source has |E X|<=epsilon and
E|X|^2<=11/13+2epsilon+epsilon^2. Jensen's inequality applied to the
exponential defining F gives

    F(z)>=exp[-(rho+epsilon)^2/2-11/26-epsilon],
    G(z)>=exp[-(rho+r_Y)^2/2],                 |z|<=rho.    (10)

The exact enclosures for these two lower bounds are respectively greater
than tau. Thus for 0<u<=tau both clipped densities min(F,u),min(G,u)
equal u inside the ball, while min(F,u)>=min(G,u) outside. Since both
probability densities have mass one,

    H(u)=C integral [min(G,u)-min(F,u)] <= 0.               (11)

The integrals are finite because min(F,u)<=F and min(G,u)<=G. At u=0 the
two hinges both equal one. This is an actual signed low-range proof;
an unsigned tail error would not suffice. It exploits the geometry of
this specific cell instead of allocating the extremely conservative
uniform cutoff of the general frontier endpoint theorem.

## 4. A signed upper endpoint

The elementary bound cosh(t)<=exp(t^2/2) implies from (6) that

    ||F_0||_infinity=2/13+(11/13)exp(-1/2).

The normalized Gaussian gradient has norm at most 1/sqrt(e)<1. Hence a
source displacement at most epsilon changes its normalized density by
at most epsilon at every point, also after taking the positive weighted sum.
Using exp(-1/2)<61/100 gives

    ||F||_infinity <= 2/13+(11/13)(61/100)+epsilon
                    =2169/3200 < 11/16=b.                 (12)

The scalar inequality follows already from
exp(1/2)>1+1/2+1/8+1/48=79/48>100/61; it is also checked by an enclosure.
Thus the source hinge is zero for u>=b, and H(u)<=0 there.

## 5. Transferring an actual reference hinge margin to the whole cell

Let f_0 be the source reference law in (6), and g_0=gamma. For two
probability densities p,q and any threshold t>=0,

    |integral(p-t)_+-integral(q-t)_+| <= TV(p,q)
                                            =||p-q||_1/2. (13)

Indeed the signed pointwise hinge change lies between the negative and
positive parts of p-q; each of their integrals equals TV.

For translated unit Gaussians, integration of the directional derivative
gives TV(gamma(.-v),gamma)<=|v|/sqrt(2pi)<|v|/2. Convexity under mixing
therefore implies

    TV(f,f_0) <= epsilon/2.                               (14)

To bound the target more sharply than a first-order displacement bound,
translate its mean to zero. Translation does not change any hinge.
Taylor's formula with integral remainder, cancellation of E Y and
||partial_ee gamma||_1=4 phi(1)<1 give

    ||g(.+E Y)-gamma||_1 <= E|Y-E Y|^2/2.

The density z -> g(z+E Y) has sites Y-E Y. Only translation invariance is
used. Because the original target lies in [-1/16,1/16]^3,

    TV(g centered,gamma) <= E|Y-E Y|^2/4
                         <= E|Y|^2/4 <= 3/1024.           (15)

More explicitly, for each centered shift v the remainder is
integral_0^1(1-t)v^T D^2 gamma(z-tv)v dt. Taking its L1 norm and integrating
the positive weights proves (15). The stated second-derivative norm follows
by integrating (t^2-1)phi(t) on its positive and negative intervals; the
other two Gaussian coordinates integrate to one. These estimates need no
contraction path or conditional kernel sign.

Combining (13)--(15), uniformly in u,

    H(u) <= H_0(u)+eta,    eta=epsilon/2+3/1024=7/1024,   (16)

where H_0 compares f_0 to the point-target Gaussian. This is the
hinge-level perturbation bridge; no alternating moment errors are propagated.

## 6. The finite middle computation and complete coverage

We use the independently accepted R3 absolute hinge quadrature theorem in
[DIRECT_HINGE.md](../gaussian_prior_localization/DIRECT_HINGE.md). For step h,
half-grid M, coordinate support bound R=1, T=Mh-R and G_h=1+h^2/8, it gives

    |H_0(u)-P(u)| <= E_quad+E_tail,
    E_quad=(h^2/4)(1+G_h+G_h^2),
    E_tail=(3G_h^2/T) exp(-T^2/2),                         (17)

uniformly in u. P is the Gaussian-prefactored lattice sum of the two
actual hinges. Its nonsmooth quadrature proof and tail estimate are
external written premises already independently reviewed; this package
does not rerun that audit or replace it by a smooth-function assumption.

The certificate takes h=1/16, M=112, T=6 and Q=2^48. There are
225^3=11,390,625 sites. The reference densities are invariant under signed
coordinate permutations. Representatives 0<=i<=j<=k<=112 have multiplicity

    2^(number of nonzero coordinates) * 3! / product_v m_v!,

where m_v counts repeated coordinate values. All 246,905 representatives
are evaluated. Their multiplicities sum exactly to the full lattice count.
This quotient concerns only the reference computation; (16) treats every
asymmetric point of the actual parameter cell.

With A_j=exp(-(jh)^2/2) and B_j=exp(-(jh-1)^2/2)+exp(-(jh+1)^2/2),
the reference densities at a representative are

    F_0=[12 A_i A_j A_k+11(B_i A_j A_k+A_i B_j A_k+A_i A_j B_k)]/78,
    G_0=A_i A_j A_k.                                     (18)

Pinned rational exponential enclosures, positive integer products and
outward division give an upper F_0 and a lower G_0 with denominator Q.
They define an upper adverse polygon P_+(u). It is affine between successive
density-value knots. Its maximum on [tau,b] therefore occurs at an endpoint
or an enclosed density knot, all of which the exact sweep includes. The
computation processes 21,775 knots/endpoints in that window. There is no
threshold sampling assumption or unexamined interval between knots.

The exact maximum is negative. Multiplication by an enclosure for C uses
the LOWER positive endpoint for an UPPER bound on this negative product.
After (17), the computed reference bound is

    max_[tau,b] H_0(u)
      <= -247321406319324331495017796268819
                    /20769187434139310514121985316880384.

Adding eta gives, for the entire cell,

    max_[tau,b] H(u)
      <= -105344539093762638527387037266707
                    /20769187434139310514121985316880384
      < -1/200.                                         (19)

All bounds in (19) are rational and compared as integers/Fractions.
Equations (11),(12),(19) cover [0,infinity) without gaps, proving (3).

## 7. Replay and trust boundary

From this directory, standard-library CPython 3.11 or later:

    python3 -B verify.py
    python3 -B -O verify.py
    sha256sum -c SHA256SUMS

Expected status: GAP_FREE_FRONTIER_CELL_PASS. The deterministic expected
record includes the exact bounds, parameter-cell hash, dependency hashes,
orbit-stream digest, scalar endpoints and the paired-rank-six determinant.
The author runtime is about two seconds on one CPU; no large data artifact
or external solver is required. The full lattice is represented by counts
and a small deterministic generator, not an omitted enumeration dump.

Controls compare every upper/lower histogram entry against the general
unquotiented density implementation on three small grids (1,197 sites),
and compare 768 window sweeps against direct evaluation of every knot. The
comparison includes negative maxima and thresholds equal to density knots.
Damaged expected records are rejected under normal and optimized Python.

The finite checker proves the recorded exact arithmetic and exhaustive
reference-grid/threshold coverage subject to inspection of the program and
Python integer/Fraction semantics. The uniform cell reduction, clipping
argument, Taylor/transport bounds, Gaussian identities and quadrature theorem
remain written mathematics; there is no proof-assistant formalization or
claim of independent acceptance. The R3 dependency files are pinned before
import, so a changed implementation or analytic statement fails closed.

This certificate settles neither the other cells of R^c_1 nor higher
frontier levels. The accepted uniform D<=7/50 is unchanged. The seven-factor
beta obligation is closed; no adjacent beta strip is pursued here. No
all-variance statement or new Kneser--Poulsen consequence follows by holding
this cell fixed while sending the Gaussian variance to zero.
