# A forward posterior transport bound and its global direction obstruction

26 September 2026. Complete author derivation; independent review and
formalization are pending. The full three-dimensional Gaussian-majorisation
question remains open.

We investigated a coupling from an actual source top set into a target
selector of the same volume. Gibbs' inequality gives a legitimate signed
lower bound, including a nonnegative information term. The theorem below
shows that **optimizing over every coupling of this type still cannot give
a global certificate**. Its optimized exponent is uniformly negative at
large volumes whenever the target has a strictly larger concentration at
even one smaller volume. A two-atom collapse, already known to satisfy full
majorisation, is a bounded three-dimensional control.

This closes the specified direction of coupling, not law-dependent endpoint
couplings in general. In particular, the information term cannot be silently
used to close the team's contact inequality or compact zero-defect criterion.

## 1. The proposed coupling and the exact identity

Let mu be a probability law in R^n with finite second moment, n>=1, and let
T be 1-Lipschitz. All bounded inputs and the regularized inputs in the
[contact reduction](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md)
satisfy these assumptions. Fix s>0 and write

    gamma_s(z)=(2 pi s)^(-n/2) exp(-|z|^2/(2s)),
    f=mu*gamma_s,                  g=(T#mu)*gamma_s,
    C_u(v)=sup_(|E|=v) integral_E u.

For 0<v<infinity, let A be the source top set of volume v and put M=C_f(v).
Thus A={f>a_f(v)}, where a_f(v)>0. Gaussian mixtures are positive, analytic,
vanish at infinity and have null positive level sets. Their top sets are
bounded and unique up to null sets at every finite positive volume. These
facts do not require a regular level or a smooth boundary.

A feasible coupling pi(dz,dy) has first marginal 1_A(z) dz and second
marginal nu(dy)=theta(y)dy, with 0<=theta<=1. Its mass is v. We require
integral |y|^2 dnu<infinity. Write

    pi(dz,dy)=1_A(z)dz K(dy|z)=nu(dy)L(dz|y).             (1)

Here K and L are probability kernels on their respective marginal supports.
The kernel may depend on the entire prior, the map, the variance and v.
There is no finite-rank, deterministic, affine or prior-independent
restriction. The identity coupling y=z shows that the feasible set is
nonempty.

Define probabilities and finite reference measures by

    P(dx,dz)=mu(dx)1_A(z)gamma_s(z-x)dz/M,
    Q(dx,dy)=mu(dx) integral gamma_s(z-x)pi(dz,dy)/M,
    b(dx,dz)=mu(dx)1_A(z)dz,
    c(dx,dy)=mu(dx)nu(dy).                                (2)

Both b and c have mass v; P and Q have mass one. Their densities relative
to these bases are

    p(x,z)=gamma_s(z-x)/M,
    q(x,y)=integral p(x,z)L(dz|y).                        (3)

For a probability R absolutely continuous with respect to a finite measure
d, put Ent_d(R)=integral log(dR/dd)dR. Let

    I_pi=Ent_b(P)-Ent_c(Q),
    E_X=E_P |Z-X|^2,          E_T=E_Q |Y-TX|^2,
    beta(pi)=(E_X-E_T)/(2s)+I_pi.                         (4)

All these quantities are finite. In particular, p is bounded above,
Ent_b(P)=-n log(2 pi s)/2-E_X/(2s)-log M, and conditional Jensen in (3)
gives

    -log v <= Ent_c(Q) <= Ent_b(P),       I_pi>=0.        (5)

The lower bound is relative-entropy nonnegativity after normalizing c/v.
The selected X-law has finite second moment, T has at most linear growth,
and Q_Y(dy)<=((2 pi s)^(-n/2)/M)nu(dy), proving the asserted cost finiteness.

Put

    J_nu=integral theta(y)g(y)dy,
    R_nu(dx,dy)=mu(dx)gamma_s(y-Tx)nu(dy)/J_nu.           (6)

Then 0<J_nu<=C_g(v), R_nu is a probability, and the exact identity is

    log(J_nu/M)=beta(pi)+D(Q||R_nu).                      (7)

Consequently

    C_g(v) >= M exp(beta(pi)).                           (8)

To verify (7), insert (3) and (6) into relative entropy:

    D(Q||R_nu)=Ent_c(Q)+n log(2 pi s)/2+E_T/(2s)+log J_nu.

Subtract the displayed expression for Ent_b(P). This gives (7), with the
plus sign on I_pi in (4). No variational approximation is made. Inequality
J_nu<=C_g(v) is the ordinary threshold comparison for a selector with
0<=theta<=1 and integral theta=v. Thus the complete remainder in (8) is

    log(C_g(v)/M)-beta(pi)
      =D(Q||R_nu)+log(C_g(v)/J_nu)>=0.                   (9)

The entropy and data-processing facts here are classical; their use is not
a novelty claim. The question tested below is whether the exponent in (8)
can always be made nonnegative for a contraction.

## 2. The genuine positive terms do not supply the missing sign

The source posterior at z is

    mu_z(dx)=gamma_s(z-x)mu(dx)/f(z).

Let m(z)=E_mu_z X, n(z)=E_mu_z TX, and

    delta(z)=tr Cov_mu_z(X)-tr Cov_mu_z(TX)
       = (1/2) integral [|x-x'|^2-|Tx-Tx'|^2]dmu_z(x)dmu_z(x')>=0.

With respect to the probability f(z)pi(dz,dy)/M define

    D_A=E delta(z),
    L_pi=E[|y-n(z)|^2-|z-m(z)|^2].

Conditional variance decomposition gives exactly

    beta(pi)=(D_A-L_pi)/(2s)+I_pi.                        (10)

Thus both posterior pair-distance loss and erased information enter with
the favorable sign. If L_pi<=D_A+2s I_pi, (8) proves the desired comparison
at this volume. This is a sufficient inequality, not an equivalence with
majorisation. The next theorem rules out its proposed universal use.

The information term is not merely formal. Put c_s=(2 pi s)^(-n/2).
Since t log t-t^2/(2B) is convex on [0,B], with B=c_s/M, (3) gives

    I_pi >= (1/(4 c_s M)) integral mu(dx)nu(dy)L(dz|y)L(dz'|y)
                       [gamma_s(z-x)-gamma_s(z'-x)]^2.   (11)

This follows by applying conditional Jensen and writing the variance as
half the expected squared independent difference. Nevertheless, even the
full I_pi, rather than this lower bound, is insufficient globally.

## 3. A uniform obstruction over all feasible couplings

Fix 0<w<v and abbreviate

    G=C_g(v),       a=a_g(v),       b=a_g(w)>a,
    d=C_g(w)/G-C_f(w)/M,
    c=b/(b-a)>1.

**Theorem.** If d>0, every feasible coupling (1) satisfies

    beta(pi) <= log(G/M)-min{d/(2c), d^2/2}.              (12)

No global order between f and g is assumed. The right side is independent
of pi, so the same bound holds for the supremum over all feasible kernels,
including limits or kernels with arbitrarily complicated support.

### Proof

First the output observation cannot be more concentrated than the selected
source. For every measurable E with |E|=w,

    Q_Y(E)=(1/M) integral_A f(z)K(E|z)dz <= C_f(w)/M.    (13)

Indeed 0<=K(E|z)<=1, and its integral over A is nu(E)<=w. The maximizing
source selector of this mass is the volume-w source top set, contained
in A since w<v. This is the precise information-direction constraint.

Let B_v={g>a}, B_w={g>b}, and ell=G-J_nu>=0. Equal total selector volumes
give

    ell=integral (1_(B_v)-theta)(g-a).

Its integrand is nonnegative both inside and outside B_v. Since B_w is
contained in B_v and g/(g-a)<=b/(b-a)=c on B_w,

    integral_(B_w)(1-theta)g <= c ell.                   (14)

If ell>=Gd/(2c), then J_nu/G<=1-d/(2c). By (7),

    beta(pi)<=log(J_nu/M)<=log(G/M)-d/(2c).              (15)

Here d<1, so the logarithm comparison has a positive argument.

Otherwise ell<Gd/(2c). Equations (6) and (14), using J_nu<=G, imply

    (R_nu)_Y(B_w)
      >=[C_g(w)-c ell]/J_nu
      >= C_g(w)/G-d/2
      = C_f(w)/M+d/2.                                   (16)

Together with (13), this gives a probability difference at least d/2 on
the event {Y in B_w}. Coarse-grain Q and R_nu to that event. The log-sum
inequality gives their binary relative entropy as a lower bound for
D(Q||R_nu). For Bernoulli probabilities p,q, this entropy is at least
2(p-q)^2: its second derivative in p is 1/[p(1-p)]>=4, and its value
and first derivative vanish at p=q. Continuity handles endpoints. Thus

    D(Q||R_nu)>=d^2/2.

Using (7) and J_nu<=G proves (12) in the second case as well. This proves
the theorem. In particular the positive information term was retained
throughout; setting it to zero is not responsible for the obstruction.

## 4. Failure of the architecture on known positive comparisons

Suppose C_g(w)>C_f(w) at one fixed w>0. As v tends to infinity,

    M -> 1,     G -> 1,     a_g(v) -> 0,
    d -> d_infinity:=C_g(w)-C_f(w)>0,     c -> 1.

Since 0<d_infinity<1, (12) gives the uniform bound

    limsup_(v->infinity) sup_(feasible pi at volume v) beta(pi)
                                <= -d_infinity^2/2 < 0. (17)

Hence no optimization of this forward construction can certify every
volume for such a pair. This is a statement about the whole coupling
architecture, not a selected numerical kernel or a failure to optimize it.

For a bounded R3 control take mu=(delta_e+delta_(-e))/2, e nonzero, and
T(e)=T(-e)=0, extended by the constant map. Then g=gamma_s. Convexity
applied pointwise to the two translates proves every convex internal-energy
comparison, so full majorisation is already true at every s>0.

Yet max f<gamma_s(0)=max g: each Gaussian translate is at most gamma_s(0),
and distinct centers cannot both attain that value at one point; f attains
its maximum. Since C_u(w)/w tends to max u as w decreases to zero, some
fixed w has C_g(w)>C_f(w). Formula (17) applies. Thus the proposed universal
nonnegative exponent is false even in this elementary positive example.

As an equality check, if T agrees with an isometry S on supp(mu), choose
pi supported on y=Sz. Then nu=1_(S A)dy, information is preserved,
I_pi=0, E_T=E_X and beta=0. Since C_g=C_f, (9) also shows that zero is
the optimized exponent. The normalization is exact on all isometry faces.

## 5. Ordered contacts and the concrete remaining obligation

At an ordered contact C_g(v)=C_f(v), suppose there is a smaller volume w
with C_g(w)>C_f(w). Then d>0, and (12) says

    sup_pi beta(pi) <= -min{d/(2c),d^2/2}<0.             (18)

This includes critical contact levels; all arguments used top sets and
integrals, not normal derivatives. The regularized strict-contraction
test class in the contact reduction has a strict peak comparison, which
provides such a smaller w if a contact exists. That strict-peak input is
credited to the contact source; (12) itself does not depend on it.

Thus favorable posterior pair loss and data-processing information alone
do not yield the R1 contact sign through this construction. The blocker is
(13): the transported selected source is constrained to be less
concentrated than the source, while a successful target at contact can
retain a strictly larger concentration on smaller sets.

The concrete obligation for a revised endpoint mechanism is to avoid (13).
One direction to investigate is mixing target observations toward source
observations, as ordinary majorisation allows, with a law-dependent
recoupling of latent labels. This is an unproved route, not an asserted
construction. A spatial channel that must intertwine every labeled
Gaussian would impose additional restrictions; it must not be substituted
for the required law-dependent coupling.

For the R3--R8 compact frontier, this excludes attempting to make (10)
nonnegative over every variance/volume/weight instance by finite optimization
or stronger enclosures of I_pi. The bound (12) already optimizes over all
such spatial couplings. It leaves the existing compact moment criterion,
fixed-atom reduction, reference-margin theorem and geometric classes intact.
It says nothing against a correctly oriented density-value coupling.

No full Gaussian counterexample, new positive family, stability improvement,
Kneser--Poulsen consequence or contact-flux inequality is established here.
There is no computational premise, omitted certificate or new quadrature.
The proof uses elementary Gaussian identities, conditional Jensen, threshold
selection and binary relative entropy; attribution is in [SOURCES.md](SOURCES.md).
