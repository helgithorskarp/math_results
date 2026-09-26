# A quantitative bridge from second energy to Gaussian common-set margins

26 September 2026. Complete author derivation; independent review and
formalization are pending. For every fixed finite contraction and every
isometric-reference Gaussian top set, this note bounds its common-set gap
below by a positive constant times the expected pair-distance loss, uniformly
over **all prior weights**. It includes zero weights and the case where every
pointwise reference slack vanishes. A separate, explicit source-set error
then gives a sufficient certificate for the actual concentration-profile
comparison. The unrestricted R3 inequality remains open.

The qualitative reference transfer and its positive transverse weight are
credited to [the isometric-reference theorem](../gaussian_isometric_reference/PROOF.md).
The new input is the quantitative translation gain, its combination with
reference slack, and the source-set remainder. This is a functional/stability
interface for the [finite-atomic lane](../gaussian_majorisation_minimax_faces/PROOF.md),
not a new map class, an evolution argument, or a localization theorem.

## 1. Setup and the quantitative statement

Let K be a finite nonempty subset of R^n, n>=1, and T:K->R^n a contraction.
Fix a probability law sigma on K and an affine Euclidean isometry S agreeing
with T on supp(sigma). Pull target coordinates back by S and translate a
reference point to zero. Henceforth T fixes supp(sigma) and 0 belongs to
that support. This normalization preserves all quantities below.

Fix s>0, let gamma_s have covariance s I_n, and choose

    r = sigma*gamma_s,       0<a<max r,
    A = {r>a},              v=|A|,
    Psi(x) = integral_A gamma_s(z-x) dz,
    q(x) = Psi(Tx)-Psi(x),  Z={x in K:q(x)=0}.

For an arbitrary probability law mu on K write

    f=mu*gamma_s,             g=(T#mu)*gamma_s,
    C_p(v)=sup_(|E|=v) integral_E p,
    J_A(mu)=C_g(v)-integral_A f,
    Q(mu)=integral_K q dmu,
    d(x,x')=|x-x'|^2-|Tx-Tx'|^2 >= 0,
    D(mu)=integral_(K x K) d(x,x') dmu(x)dmu(x').          (1)

Let U=span(supp(sigma)), V=U-perp, and m=dim V. The cited reference result
proves q>=0 and characterizes Z by preservation of every distance to the
reference support. Thus on Z, writing x=(u,w) and Tx=(u,z),

    |z|=|w|,     d(x,x')=2(z.z'-w.w') >= 0.              (2)

If m>0, there is a continuous positive function alpha such that

    grad_V Psi(u,w)=-alpha(u,|w|)w,    0<alpha<=2/s.      (3)

Define the finite positive lower bound

    b0 = min_(x=(u,w) in Z) alpha(u,|w|)>0.              (4)

Z is nonempty because it contains supp(sigma). If K\Z is nonempty, put

    q0 = min_(x in K\Z) q(x)>0.                         (5)

Choose any L>0 with d(x,x')<=L on K x K. The source diameter squared is
one choice when positive; replacing it by any larger positive number handles
singletons and avoids a zero denominator. Set G=sqrt(2/(pi s)).

**Theorem 1.** For every probability mu on K,

    J_A(mu) >= D(mu)/C,                                 (6)

with the following explicit constants:

* If m>0 and K\Z is nonempty, take

      C=max{16/(s b0^2), (4G^2/b0^2+2L)/q0}.            (7)

* If m>0 and Z=K, take C=8/(s b0^2).
* If m=0 and K\Z is nonempty, take C=2L/q0.
* If m=0 and Z=K, T is the identity on K and D=0; (6) holds with any C>0.

All constants are independent of the actual weights of mu. In particular
no minimum positive prior mass or covariance eigenvalue is required.
The constants do depend on the geometry, reference law, variance and
reference level; no dimension-free or globally uniform constant is claimed.

Let E_2(mu)=integral g^2-integral f^2. The theorem implies the direct
second-internal-energy bridge

    J_A(mu) >= [4s(4 pi s)^(n/2)/C] E_2(mu) >= 0.        (8)

Equation (8) concerns the displayed reference test set. It is not an
unrestricted implication from E_2>=0 to C_g>=C_f. The precise additional
source-set cost is given in Section 5.

## 2. Reference inputs and their scope

For completeness, the mechanisms underlying (2)--(3) are recorded here;
priority for them belongs to the cited reference theorem.

For x not fixed by T, reflect across the perpendicular bisector of x and
Tx. Contraction places all fixed reference centers on the side nearer Tx.
Their Gaussian mixture, hence its top-set indicator, is at least its
reflection there. Pairing reflected points proves q(x)>=0. If one reference
distance decreases, the mixture is strictly larger on that halfspace. Its
normal derivative on the dividing plane is positive, so its maximizers lie
strictly on the same side. Following a normal ray from a maximizer to
infinity produces an open region where exactly one of a reflected pair
belongs to A. The paired Gaussian difference is positive there. Thus

    q(x)=0 iff |Tx-c|=|x-c| for all c in supp(sigma).     (9)

This proof includes critical levels. Equal distances to zero give equal
norms, and subtracting their squares at other reference points yields
P_U Tx=P_U x. This proves (2).

Since the reference is supported in U, r(u,w)=r_U(u) gamma_s^V(w). Each
nonempty section A_u is a ball in V centered at zero. For such a ball of
radius R let F_R(w)=integral_(|z|<R) gamma_s^V(z-w) dz. Boundary integration
and reflection pairing show -F_R'(rho)/rho>0 for rho>0, with a positive
continuous extension at rho=0. The directional second derivative bound
||partial_ee gamma_s^V||_1<=2/s gives -F_R'(rho)/rho<=2/s, including zero.
Convolving these coefficients over U gives (3). Nonempty open families
of positive-radius sections make the coefficient strictly positive.
This includes U={0}, dim V=1 and w=0. When V={0}, (3) is unnecessary.

Finiteness of K now gives both positive minima (4)--(5). More generally,
the proof below works for compact K whenever an actual positive slack floor
q0 on K\Z is supplied; it does not assume that such a floor exists for an
arbitrary diffuse domain approaching Z.

## 3. Translation supplies the missing quantitative term

The following elementary estimate is useful independently of reference
geometry. For any probability Gaussian mixture g and bounded measurable A,
put Phi(h)=integral_(A+h) g. For any unit e,

    |partial_ee Phi(h)| <= ||partial_ee gamma_s||_1<=2/s. (10)

Indeed partial_ee gamma_s=( (e.z)^2/s^2-1/s )gamma_s, whose absolute integral
is at most 2/s, and mixing cannot increase that bound. Gaussian derivatives
are integrable, which justifies all differentiations, including singular
center laws. For any linear subspace V, Taylor's formula along
h=(s/2)grad_V Phi(0) therefore gives

    sup_(h in V) Phi(h) >= Phi(0)+(s/4)|grad_V Phi(0)|^2.

Translations preserve volume. Also Phi(0)=integral_A g and

    grad_V Phi(0)=-integral_K grad_V Psi(Tx) dmu(x).

It follows that

    J_A(mu) >= Q(mu)+(s/4)|zeta(mu)|^2,
    zeta(mu)=integral_K grad_V Psi(Tx) dmu(x).               (11)

This does not assume that A is optimal for g, or stationary under
translations. It quantifies the improvement obtainable when stationarity
fails. The reference input supplies Q>=0; (10) itself needs no contraction.
For m=0 simply retain J_A>=Q.

We shall also use the uniform gradient estimate

    |grad_V Psi(y)|<=G=sqrt(2/(pi s)).                    (12)

For every unit e in V, its directional derivative is bounded by
||partial_e gamma_s||_1=sqrt(2/(pi s)); choose e parallel to the gradient.
No factor depending on dim V is needed. No constant optimization is intended.

## 4. Combining reference slack and pair-distance loss

Assume first m>0. Put O=K\Z and eta=mu(O). On Z use the common endpoint
weight b(x)=alpha(u,|w|)=alpha(u,|z|). By (2),

    W_Z=integral_(Z x Z) b(x)b(x')d(x,x') dmu(x)dmu(x')
       =2|integral_Z b(x)z dmu|^2-2|integral_Z b(x)w dmu|^2
       <=2|integral_Z b(x)z dmu|^2.                       (13)

These are unnormalized integrals; no conditional probability or division
by mu(Z) is used. Since d>=0 and b(x)>=b0,

    D_Z:=integral_(Z x Z) d dmu dmu <= W_Z/b0^2.

By (3), the first vector integral in (13) is minus the Z-part of zeta(mu).
Equations (12)--(13) therefore give

    D_Z <= (2/b0^2)(|zeta(mu)|+G eta)^2.

The remaining pair mass is 2eta-eta^2, and d<=L. Thus, using
(x+y)^2<=2x^2+2y^2 and eta^2<=eta,

    D <= (4/b0^2)|zeta(mu)|^2+(4G^2/b0^2+2L)eta.            (14)

If O is nonempty, eta<=Q/q0. Equation (11) gives
|zeta(mu)|^2<=4(J_A-Q)/s. Substitute into (14):

    D <= [16/(s b0^2)](J_A-Q)
           +[(4G^2/b0^2+2L)/q0]Q <= C J_A,             (15)

because 0<=Q<=J_A. If O is empty, retain the sharper
D<=2|zeta(mu)|^2/b0^2, which gives the second case of the theorem.

If m=0, every point of Z is fixed. Then D_Z=0 and
D<=L(2eta-eta^2)<=2L eta<=2L J_A/q0 when O is nonempty. If O is empty,
T is the identity on K. This completes all cases, including mu(Z)=0,
mu(O)=0, coincident target sites and zero prior weights.

Finally, Gaussian multiplication gives the exact identity

    E_2=(4 pi s)^(-n/2) integral_(K x K)
          [exp(-|Tx-Tx'|^2/(4s))-exp(-|x-x'|^2/(4s))]
          dmu(x)dmu(x').                                 (16)

For 0<=b<=a, 0<=exp(-b)-exp(-a)<=a-b. Hence
0<=E_2<=(4 pi s)^(-n/2)D/(4s). Combining this upper bound for E_2 with
(6) proves (8). The direction matters: an upper bound on E_2 in terms of D
makes D a lower bound for a multiple of E_2. We do not use or assume the
team's earlier entropy-stability theorem.

## 5. The exact cost of replacing the actual source top set

Put

    R_A(mu)=C_f(v)-integral_A f >=0.

Then the actual concentration-profile gap obeys

    C_g(v)-C_f(v)=J_A(mu)-R_A(mu)
                 >= D(mu)/C-R_A(mu).                    (17)

Suppose a certified epsilon satisfies ||f-r||_infinity<=epsilon<a. Define

    E_r,a(epsilon)=integral_R^n (epsilon-|r(z)-a|)_+ dz.  (18)

This finite nonnegative number bounds the remainder:

    R_A(mu)<=E_r,a(epsilon).                             (19)

To check (19), the fixed-threshold hinge bound C_f(v)<=integral(f-a)_++av
and |A|=v give

    R_A<=integral_(A-complement)(f-a)_+ + integral_A(a-f)_+.

Outside A, r<=a; inside, r>a. Each integrand is bounded by the corresponding
part of (epsilon-|r-a|)_+. No derivative of the optimizing threshold or
regularity of the boundary is needed.

Since a-epsilon>0, the shell in (18) is bounded. The level {r=a} is null
by real analyticity. Consequently

    E_r,a(epsilon)/epsilon <= |{|r-a|<epsilon}| ->0
                 as epsilon decreases to zero.           (20)

At a regular level, a separately established shell-volume bound
|{|r-a|<u}|<=M u for 0<u<=epsilon yields
E_r,a(epsilon)<=M epsilon^2/2, by layer cake. Without such a bound, (18)--(20)
remain valid through critical levels but assert no universal power rate.

For finite weights p_i of mu and r_i of sigma on the same sites, one simple
source-density input is

    epsilon=(2 pi s)^(-n/2) (1/2)sum_i |p_i-r_i|.         (21)

The signed weights sum to zero and each Gaussian kernel lies between zero
and (2 pi s)^(-n/2), so total-variation duality proves (21). A smaller
rigorously enclosed density error may be substituted.

Equations (17)--(19) give the explicit signed certificate

    D(mu)/C > E_r,a(epsilon)
          implies C_g(v)>C_f(v).                         (22)

A certified lower bound on the second-energy term in (8) can replace D/C.
This is the precise energy-to-profile bridge established here. It includes
a geometric reference hypothesis and a source-set error budget. Omitting
that budget would assert the unproved full implication.

## 6. Uniformity on compact variance and volume windows

Keep K,T,sigma fixed and choose

    0<s0<=s<=s1<infinity,    0<v0<=v<=v1<infinity.

For each (s,v), choose the unique threshold a(s,v) whose reference top set
has volume v. Gaussian analyticity, null positive levels and strict
level-volume monotonicity make a(s,v) continuous. It stays positive, and
the top sets lie in a common bounded region on the compact window.

The set Z in (9) depends only on the reference geometry, not on s or v.
The finitely many positive off-Z slacks vary continuously, so their
minimum over the window is positive. The transverse coefficients on Z
are also continuous and positive. For nonzero transverse radius this
follows from (3); at zero use the transverse second derivative of Psi.
Differentiation of Gaussian kernels and dominated convergence through
null reference levels justify this continuity. Thus a common b0>0,
q0>0 where needed, G=sqrt(2/(pi s0)), and s0 in the denominators give
one finite C in Theorem 1 for the whole window and every prior weight.

The estimate E_r,a(epsilon)=o(epsilon) is uniform on the same window.
Otherwise choose parameters converging in the compact window and
shell widths decreasing to zero with shell volumes bounded below.
All shells lie in a common bounded set; continuity makes their indicators
converge to zero outside the null limiting level. Dominated convergence
is a contradiction. This proof includes critical levels.

No uniformity is claimed as v tends to zero or infinity, s tends to zero
or infinity, the finite configuration changes, or an off-Z site approaches Z.
Those are additional obligations in any all-threshold certificate.

## 7. Controls and the remaining full-question obligation

A useful degenerate control is K={0,e,-e}, |e|=1, with T0=0 and
Te=T(-e)=e, reference sigma=delta_0, and A a centered ball. Here Z=K:
pointwise reference slack is identically zero for every actual prior.
For mu=(delta_e+delta_(-e))/2, D=2, while

    J_A=F_R(0)-F_R(e)>0.

The positive transverse weight and translation term in (11) detect this
margin. Formula (13), not pointwise slack, is essential. This control is
credited to the reference theorem; the quantitative bound is (6).
If instead mu=delta_e, D=0 but the same J_A remains positive. Thus (6)
is a lower bound, not a two-sided equivalence: even an isometric actual
law can have positive common-set gap if A is not its own top set.

For the [finite face certificate](../gaussian_majorisation_minimax_faces/PROOF.md),
any independent lower bound on D over a weight region combines with (6)
to give a common-set margin on that entire region. The constants are finite
reference data; no new enumeration of faces is needed. Section 5 states
what must additionally be bounded to certify the actual profile.
[INTERFACE.md](INTERFACE.md) records exactly which enclosures a producer
must supply. No numerical enclosure or unknown configuration is certified
in this note.

The measure lane's [common-set formulation](../gaussian_prior_localization/PROOF.md)
requires arbitrary source sets. We control reference sets and their explicit
error budgets, not that arbitrary-set quantifier. The map lane's fixed
nondegenerate tetrahedron case has m=0, so the simpler q0/(2L) margin applies
to its reference tests. This does not prove the sign for each actual prior's
own top set. The [first-contact reduction](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md)
retains its unweighted posterior-covariance sign over different top sets;
no implication to that sign is claimed here.

The new output is a quantitative, all-weight internal-energy/common-set
interface, including the degenerate zero-slack boundary. No new positive
map family, Kneser--Poulsen consequence or unrestricted theorem is inferred.
