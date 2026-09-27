# Spatial localization of a certified adverse Gaussian contact

Complete author proof, 27 September 2026; independent review pending.
No adverse joint contact is supplied. The full R3 Gaussian majorisation
problem remains open, and its accepted adverse-defect bound is unchanged.

The result replaces the input-atom/minimum-weight dependent finite cover
in [R7's contact transfer, Section 6](../gaussian_two_body_contact_transfer/PROOF.md)
by a spatial cover. Its size depends only on radius, variance range,
threshold floor and adverse volume margin. It works for diffuse laws and
at critical levels, without a covariance floor. It is a quantitative
conditional counterexample conversion, not a new positive map class or a
new equivalence. The ball representation and Gaussian-to-ball principle
are prior work; see [SOURCES.md](SOURCES.md).

## 1. Domain, sign and finite-witness statement

Let R,J be integers at least one, S>=1, and K_A,K_B compact convex subsets
of B(0,R) in R3. Let I_A,I_B be Euclidean isometries satisfying

    |I_A p-I_B q| <= |p-q|       (p in K_A, q in K_B).             (1)

They agree on the overlap and define a contraction T on the union. Take
arbitrary Borel probability laws mu_A,mu_B on the two bodies, component
variances s_A,s_B in [1,S], and normalized thresholds a,b in [2^-J,1).
Write, for k=A,B,

    F_k(x)=integral exp(-|x-p|^2/(2s_k)) dmu_k(p),
    G_k(x)=F_k(I_k^(-1)x).

The Gaussian peak constants have been removed separately; the variances
need not agree. Suppose an actual adverse joint-volume bound is certified:

    |{F_A>a} intersection {F_B>b}|
       - |{G_A>a} intersection {G_B>b}| >= delta > 0.              (2)

Put

    U=ceil sqrt(2SJ), B=R+U,
    B0=2R+ceil sqrt(2(J+1)), r=32B0^2-1, C=48S^2 B0^3,
    eta=min(1/2, 2^(-J-3)(delta/(4C))^r),
    m=ceil sqrt(3R^2/(8eta)), Nbar=2(2Bm+1)^3.                   (3)

**Theorem.** There is a labelled finite list of at most Nbar source
centres in K_A union K_B, with their images under the SAME T, and radii
0<r_i<=U, whose target ball union has volume at least delta/2 larger
than its source ball union. For any

    0<epsilon<=min(1, delta/[2Nbar(32U+64)]),                     (4)

define Z=sum_i exp(r_i^2/(2epsilon)), w_i=exp(r_i^2/(2epsilon))/Z,
h=(2pi epsilon)^(-3/2)/Z. Then the actual common-variance Gaussian
mixtures at these new source and target centres satisfy

    integral(g-h)_+ - integral(f-h)_+ < -h delta/4.               (5)

The finite witness bound has no dependence on the original atom count,
minimum atom mass, covariance or squared-distance loss. At fixed R,S,J
it is polynomial in inverse delta, with an explicit exponent O(R^2+J).
The centres, weights and common variance are generally different from
those of the input contact. Kirszbraun extension gives a global short map,
so (5), IF (2) is supplied, is a counterexample to the original headline.

This is an effective cardinality bound, not an algorithm for evaluating an
arbitrary unencoded measure. A constructive implementation needs certified
profile/posterior integrals and the adverse-volume premise. Section 6 gives
an optional rational output interface when the two bodies have rational
finite presentations.

## 2. Posterior geometry and a three-dimensional cover

For one component, let mu be any probability law in B(0,R), s>=1, and
F(x)=integral exp(-|x-p|^2/(2s)) dmu(p). Define the posterior pi_z by
dpi_z/dmu=exp(-|z-p|^2/(2s))/F(z), and

    psi(z)=log integral exp(z.p/s-|p|^2/(2s)) dmu(p).

Differentiating under the bounded integral gives

    grad psi(z)=E_(pi_z) P/s,
    Hess psi(z)=Cov_(pi_z)(P)/s^2 <= (R^2/s^2) I.

The last inequality follows by bounding the second moment in any unit
direction by R^2; no lower covariance bound is involved. The exact
relative-entropy identity and Taylor's theorem with integral remainder give

    KL(pi_z || pi_x)
      =psi(x)-psi(z)-grad psi(z).(x-z)
      <= R^2 |x-z|^2/(2s^2).                                   (6)

Every posterior has finite entropy relative to mu, since its log density
is bounded on the support for fixed z. This includes diffuse, singular and
atomic laws, with arbitrarily small or zero original atomic weights.

Let c_z=E_(pi_z)P, V_z=E_(pi_z)|P-c_z|^2, E_z=KL(pi_z||mu).
At any level t in (0,1), the classical posterior ball has

    rho_z(t)^2=-2s log t-V_z-2s E_z
              =|z-c_z|^2+2s log(F(z)/t).                         (7)

Discard nonpositive squared radii. For every x,

    log F(x)-[-|x-c_z|^2/(2s)-V_z/(2s)-E_z]
      = KL(pi_z||pi_x) >= 0.                                    (8)

Thus B_open(c_z,rho_z(t)) is contained in {F>t}; also rho_z(t)^2
<=-2s log t, since V_z,E_z>=0. The same label and radius move rigidly
under I_k, with centre I_k c_z. Convexity puts c_z in K_k.

Suppose now that a TIGHTENED adverse datum with common eta>0 is available:

    |{F_A>a exp(eta)} intersection {F_B>b exp(eta)}|
       -|{G_A>a} intersection {G_B>b}| >= Delta > 0.              (9)

Every source level at a or b lies in B(0,B), since
F_k(x)<=exp(-(|x|-R)_+^2/(2s_k)) and log(1/a),log(1/b)<=J.
Take the grid Z_m=(m^-1 Z^3) intersection [-B,B]^3, with
m>=sqrt(3R^2/(8eta)). Each x in the cube has a nearest z in this grid
with |x-z|^2<=3/(4m^2), including boundary points and ties. Equations
(6)--(8) show that the balls labelled by Z_m at level a, respectively b,
cover the corresponding tightened SOURCE level. Their target block unions
are contained in the corresponding UNTIGHTENED target levels. Each block
has at most (2Bm+1)^3 labels. All nonempty radii are at most U.

The source intersection of the two finite ball unions therefore exceeds
the target intersection by at least Delta. Each single-block union has
the same volume before and after its rigid motion. Inclusion-exclusion
gives a target-minus-source TOTAL union gap at least Delta. All centres
contract by (1). This proves the finite cover with bound

    Nbar=2(2Bm+1)^3,                                            (10)

directly for arbitrary laws. Unlike the posterior-simplex grid in R7's
Section 6, its dimension is the ambient dimension three, not the number
of input atoms. This conclusion uses a verified covering inequality;
uncertified random posterior samples are not a substitute.

## 3. Effective tightening, including critical levels

Here is the covariance-free strip lemma from
[the all-radius localization proof, Section 3](../gaussian_all_radius_loss_localization/PROOF.md),
restated with its elementary proof. Its enclosing loss-relative theorem
requires covariance; this lemma does NOT. The source, including this lemma,
was independently accepted at graph height 6578; see the
[independent review](../gaussian_all_radius_loss_localization_review2/REVIEW.md).

For q(x)=E exp(-|x-P|^2/2), |P|<=2R, and 2^-J<=u<=v<=1,

    |{u<=q<=v}| <= 48 B0^3 (4(v-u)2^J)^(1/r).                  (11)

Positive levels are null because q is nonconstant real analytic and
decays at infinity. For v>u the strip is inside [-B0,B0]^3. Fix the last
two coordinates, and write Q for the resulting subprobability mixture of
unit one-dimensional Gaussians. At x=B0, Q(B0)<=2^(-J-1). Let a strip
section have length b0>0. Choose n=32B0^2=r+1 quantile points in this
compact section; their separations are at least |i-j|b0/r. Interpolating
Q-u at these points gives a polynomial P of degree r with

    |P(B0)| <= (v-u)(12B0/b0)^r.

For m0=16B0^2, the Fourier formula for a Gaussian yields
sup |Q^(2m0)| <= (2m0)!/(2^m0 m0!). The real interpolation remainder
at B0 is consequently at most

    (2B0^2)^m0/m0! <= (3/8)^m0 <= 2^(-J-2).

Here m0!>=(m0/e)^m0, e<3, and m0>=J+2. Since |Q(B0)-u|>=2^(-J-1),
we get b0<=12B0(4(v-u)2^J)^(1/r). Integrating the two remaining
coordinates proves (11). No regular-level or gradient assumption occurs.

For s in [1,S], rescale x by sqrt(s). Its support radius becomes at most
R, and the volume multiplier s^(3/2) is at most S^2. If 0<eta<=1/2,
then a(exp(eta)-1)<=2eta, since a<=1. Applying (11), with an upper
threshold clipped to 1 when necessary, bounds EACH source strip lost
by raising the level a to a exp(eta) by

    C (2^(J+3) eta)^(1/r).                                     (12)

The choice in (3) makes (12) at most delta/4. The two lost strips remove
at most delta/2 from the source intersection, while the target levels
are unchanged. Thus (2) implies (9) with Delta=delta/2. Sections 2 and 4
complete the theorem. The proof applies at critical levels and uniformly
over every family with common R,S,J,delta and the two-rigid-body premise.

## 4. Accepted conversion to a Gaussian hinge counterexample

For completeness, the calculation in R7's accepted Sections 5--6 is short.
Suppose N balls of radii at most U have an adverse union gap Delta>0.
Use the exponential weights in Section 1 and write F_P=f/h. Then

    integral min(F_P,1)=V_P+E_P,
    0<=E_P<=4pi[epsilon sum_i r_i
                      +N sqrt(pi/2) epsilon^(3/2)].              (13)

Inside the ball union the integrand is one. Outside it, bound the sum of
exponentials term by term and integrate radially. Integration by parts
and (r+v)^2-r^2>=v^2 give (13). Thus

    epsilon<=min(1, Delta/[Nbar(32U+64)])

implies E_P<Delta/2. Equal total Gaussian mass gives

    H_g(h)-H_f(h)=h[(V_P+E_P)-(V_Q+E_Q)] < -h Delta/2.

This proves (4)--(5). Repeated centres can be merged, since contraction
makes their target images agree. No assumed sign has been hidden in (13):
the adverse volume bound (2) remains the essential external input.

## 5. Symbolic dyadic schedule

An implementation need not form eta or the grid when they are enormous.
For rational R,S,delta as above (R integer) use exact logarithmic ceilings:

    b0=max(0,ceil log2(4C/delta)), t=max(1,J+3+r b0),
    eta=2^-t, v=ceil log2 R+ceil(t/2), m=2^v,
    n=6+3 ceil log2 B+3v, Nbar=2^n.                              (14)

Then 3R^2/(8m^2)<=eta, and 2(2Bm+1)^3<=2^n. Equation (12) still
costs at most delta/4 per strip. A suitable variance is epsilon=2^-E,
where E=max(0,n+ceil log2(2(32U+64)/delta)). The program outputs t,v,n,E
without constructing these grids or powers. In particular, at fixed
R,S,J, n=O(1+log_+(1/delta)); uniformly the coefficient of that logarithm
is O(R^2+J). This is a cardinality estimate, not a practical runtime bound.

## 6. Optional rational geometry and priors

Suppose each K_k is the convex hull of a supplied finite rational list,
and the matched image vertices under I_k are rational. The input laws
can still be diffuse. The two lists and their isometries, not merely a
pointwise pairing of nonrigid blocks, are part of this additional input.

Set Nbar=2^n from (14), and define

    ell=max(0,n+ceil log2(192 U^2/delta)), e0=2^-ell,
    M=2^(ell+ceil log2(6R)).                                    (15)

For each posterior centre, Caratheodory's theorem supplies a convex
representation by at most four vertices of its own block. Round the first
three coefficients down to multiples of 1/M and put the remainder into
the last coefficient. The total variation in coefficients is at most
6/M, so the centre moves by at most 6R/M<=e0. The target centre moves by
the same amount under its block isometry. Both new centres are rational.
The new whole configuration is still a contraction, since the source
centres remain in their respective convex bodies and use the SAME T.

Discard radii r_i<=2e0. Otherwise set

    r'_i=e0(floor(r_i/e0)-1),  r_i-2e0<=r'_i<=r_i-e0.

The new ball is inside the old one, and contains its concentric inner
ball of radius max(0,r_i-3e0). Therefore the loss of target union volume
is at most 12pi Nbar U^2 e0 < 48Nbar U^2 e0 <= delta/4. Shrinking
the source union cannot reduce the adverse target-minus-source gap.
The new rational ball list retains gap at least delta/4.

Choose now

    E=max(0,n+ceil log2(4(32U+64)/delta)), epsilon=2^-E.           (16)

Equation (13) gives H_g(h)-H_f(h)<-h delta/8. To make its weights
rational as well, observe that, for this new list,

    h>=2^-K,  K=U^2 2^E+n+5,                                  (17)

because (2pi epsilon)^(-3/2)>1/32, Z<=Nbar exp(U^2/(2epsilon)),
and exp(x)<2^(2x) for x>0. Set

    W=2^w, w=K+n+max(0,ceil log2(64/delta)).                    (18)

Round all but the last weight down to multiples of 1/W and put the
remainder in the last. The coefficient L1 error is at most 2N/W.
At the SAME threshold h each Gaussian mixture changes in L1 by at most
this error, and the difference of their hinge integrals changes by at
most 4N/W<=h delta/16. The resulting rational-prior Gaussian pair has

    H_g(h)-H_f(h)<-h delta/16.                                  (19)

Its centres, matched images, priors and variance are rational; the
known positive testing threshold h need not be rational. The symbolic
schedule records w=U^2 2^E+2n+5+max(0,ceil log2(64/delta)), not an
expanded double-exponential denominator. These very loose bounds do not
claim a practical exact search. No arbitrary-coordinate rounding, which
could violate contraction, is permitted. Existence of these choices does
not give a finite-data oracle for a noncomputable prior.

For finite input vertex lists, the whole-hull premise (1) can be checked
at cross vertices: rigidity cancels the within-block variance terms in
the squared-distance barycentric identity. This is R7's identity, not
a new extension principle. Merely checking nonrigid endpoint lists would
not justify this use of convex hulls.

## 7. Validation boundary and consequence

The proof is unformalized analysis using bounded integral differentiation,
entropy, Gaussian derivative bounds, interpolation, Caratheodory and
Kirszbraun. The exact standard-library controls check the spatial grid,
posterior covariance algebra, barycentric identity, coefficient rounding,
shell-volume estimates, dyadic schedules and source pins. They do not
integrate a Gaussian contact or certify an adverse datum.

The added information is a law-independent finite witness budget and an
optional explicit rational interface for R7's accepted conditional
transfer. The ball envelope, random posterior sampling, qualitative
finite transfer, and Gaussian-to-KP implication are credited prior work.
There is no new uniform positive middle family, no new all-threshold
positive class, and no new Kneser--Poulsen theorem. This result does not
extend the domain of the two-body contact equivalence to general maps.
