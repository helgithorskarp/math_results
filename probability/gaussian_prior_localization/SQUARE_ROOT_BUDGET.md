# A smaller moment degree from superlevel geometry and total mass

Complete author proof; independent mathematical review is pending. The full
R3 Gaussian-majorisation problem remains open. This reduces the required
largest moment power on the existing unrestricted finite frontier from
65536 k^8 to **2048 k^5-1**, without changing its configurations or rational
denominators. It proves no unknown beta sign.

The ingredients are elementary superlevel geometry, unit probability mass,
and the classical genuine Bernstein--Durrmeyer operator. Weighted positive
approximation is established mathematics; see the references and attribution
in [SOURCES.md](SOURCES.md). The new campaign application is the explicit
radius-dependent bound and its effective composition with the existing
localization. No optimal degree or historical priority is claimed.

## 1. A modulus in the square root of the threshold

Let f=mu*gamma_s and g=nu*gamma_s be Gaussian convolutions of probability
laws on R3, at the SAME variance s>0. Their supports fit, after separate
translations, in balls of radius R. A map between the laws is not needed
in this section. Put

    C=(2 pi s)^(-3/2), r=R/sqrt(s),
    H(u)=integral(g-Cu)_+ - integral(f-Cu)_+,  0<=u<=1,
    B_r=(sqrt(10)/3) r^(3/2)+15/4.                         (1)

Both endpoint values H(0)=H(1)=0 are exact. The first uses equal unit mass;
the second uses the Gaussian density bound f,g<=C.

**Lemma 1.** For all u,v in [0,1],

    |H(v)-H(u)| <= 2 B_r |sqrt(v)-sqrt(u)|.                (2)

This holds at collisions, zero-weight faces, critical density levels,
and for diffuse or singular mixing laws.

**Proof.** Write V_f(a)=volume{x:f(x)>a}, and similarly for g. The
support-ball inclusion used in R8's [uniform frontier](../gaussian_majorisation_open_stability/UNIFORM_FRONTIER.md)
gives, for 0<u<=1,

    C V_f(Cu), C V_g(Cu)
       <= [sqrt(2/pi)/3] [r+sqrt(2 log(1/u))]^3.           (3)

Independently, probability mass one gives u C V_f(Cu)<=1 and the same
for g. The two nonnegative volumes are bounded by the SAME upper bound,
so their difference costs one copy, not the sum of two copies. Layer cake
shows that H is absolutely continuous, with almost-everywhere bound

    |H'(u)| <= min{1/u, [sqrt(2/pi)/3]
                              [r+sqrt(2 log(1/u))]^3}.     (4)

This statement requires no smoothness of level surfaces. Layer cake and
integrability of the superlevel volumes also apply at the endpoint zero.

Put t=log(1/u). Since pi>3, sqrt(2/pi)/3<5/18. The identity

    4(a^3+b^3)-(a+b)^3=3(a-b)^2(a+b)>=0

and min(A,B+D)<=min(A,B)+D imply

    sqrt(u)|H'(u)|
      <= min{exp(t/2), (10/9) r^3 exp(-t/2)}
                       +(10/9)(2t)^(3/2)exp(-t/2)
      <= (sqrt(10)/3)r^(3/2)+15/4.                        (5)

For the first term use min(A,B)<=sqrt(AB). For the second, the maximum
of (2t)^(3/2)exp(-t/2) on t>=0 is (6/e)^(3/2), at t=3.
The elementary e>8/3 makes (10/9)(6/e)^(3/2)<15/4.
Integrating B_r/sqrt(u) proves (2), including u=0. QED.

The unit-mass bound is what changes the radius dependence from order r^3
in the unweighted derivative to order r^(3/2) in (5). No lower atom weight,
positive threshold cutoff, contraction strictness or signed tail is used.

## 2. The same beta row with a classical positive kernel

Use the existing normalized moment/beta definitions from the
[global criterion](../gaussian_majorisation_global_criterion/PROOF.md):

    b_(N,j)=E H(Beta(j+1,N-j+1)),   0<=j<=N,
    D_N=max(0,-min_j b_(N,j)),
    Delta=max_(0<=u<=1)(-H(u))_+.

**Lemma 2.** For every integer N>=0,

    0<=Delta-D_N <= 2 B_r sqrt(2/(N+3)).                  (6)

**Proof.** Put n=N+2. Take J~Bin(n,u). If J=0 set V=0; if J=n set V=1;
otherwise take V conditional on J to have law Beta(J,n-J). This is the
classical genuine Bernstein--Durrmeyer kernel, not a new operator. Its
conditional first and second moments, valid also at J=0,n, are

    E(V|J)=J/n,
    E(V^2|J)=J(J+1)/(n(n+1)).

Hence

    E V=u,    E(V-u)^2=2u(1-u)/(n+1).                     (7)

For u>0, the identity for a difference of square roots gives

    E(sqrt(V)-sqrt(u))^2
      = E[(V-u)^2/(sqrt(V)+sqrt(u))^2]
      <= E(V-u)^2/u <= 2/(n+1).                          (8)

At u=0 the kernel has V=0, so (8) holds without division. Equations
(2), (8), and Cauchy--Schwarz give

    |E H(V)-H(u)| <= 2 B_r sqrt(2/(N+3)).

The interior terms of E H(V) are positive multiples of EXACTLY b_(N,J-1).
The remaining two terms are the exact zeros H(0),H(1). Thus E H(V)>=-D_N.
Taking the supremum of the negative part of H proves the upper bound in
(6). Every beta average is at least -Delta, proving the lower bound. QED.

This is a new error estimate for the existing D_N. There are no new test
functions, no square-root density moments, and no changed beta normalization.
The square root is used only to bound the kernel's approximation error.
The endpoint terms must be retained in the kernel proof even though their
hinge values are zero; simply deleting them would lose mass and (7).

## 3. Explicit degree on the existing compact and rational frontiers

Use the compact class K^c_k and integer A_k from
[CUBATURE_FRONTIER.md](CUBATURE_FRONTIER.md). Its endpoint radii are <=2k,
variance is one, and its attained defect E_k obeys

    0<=D-E_k<11/(4k).

Since k>=1 and 80<81, (1) gives

    B_(2k)=(sqrt(80)/3)k^(3/2)+15/4
              <(27/4)k^(3/2).

Choose

    N_k=2048 k^5-3,       largest moment power=N_k+2
                                             =2048 k^5-1. (9)

For every configuration in K^c_k, (6) now yields

    0<=Delta-D_(N_k)<27/(64k).                            (10)

Let B_k be the maximum of D_(N_k) on K^c_k. Its existence follows from
the prior compactness argument and continuous finite replica sums. Then

    0<=D-B_k<203/(64k).                                  (11)

Now use the SAME finite rational family R^c_k as in the cubature interface:
at most A_k labels, L=256k^3, W=4kA_k, integer radii <=3kL, anchor zero,
nonnegative integer masses summing W, and integer squared pair losses
>=256k^2 for distinct labels. Let F_k be the greatest negative beta
magnitude over that family at the NEW row (9). Then

    0<=D-F_k <11/(4k)+27/(64k)+161/(256k)
              =973/(256k).                               (12)

The geometric rounding estimate from [RATIONAL_INTERFACE.md](RATIONAL_INTERFACE.md)
and the updated [paired producer](paired_cubature.py) applies to EVERY beta
row. Apply (10) at compact radius 2k FIRST and transfer that row to the
rounded radius-3k instance. Applying the radius-2k constant directly to
the radius-3k rational family would be incorrect. Conversely every rational
datum is a genuine contraction and its negative beta magnitude is <=D.
These observations prove both inequalities in (12). No monotonicity of F_k
in k is asserted or needed.

For any 0<epsilon<=1, take k=ceil(8/epsilon). A rigorous uniform bound

    b_(N_k,j)>=-epsilon/2  for EVERY rational input and index

implies D<1997 epsilon/2048<epsilon. Similarly a violation of size delta>0
has a rational beta witness below -delta/2 whenever k>=8/delta. Neither a
uniform sign certificate nor a negative witness is supplied here.

The new largest power is less than the previous one divided by 32k^3.
Configuration counts, coordinate denominators, mass denominators, atom
budgets and non-point pair-loss floors are unchanged. The existing bound
eta<=zeta/[(N+1)3^N] on individual normalized moment errors uses the new
N_k; no huge power 3^N needs to be printed to state this requirement.
Replica moment evaluation can still have A_k^(N_k+2) terms. The reduction
is substantial but does not make exhaustive certification practical.

The separately reviewed sign strip N-j<=6 can omit those indices from a
sign search. It is optional context, not a premise of (1)--(12). All other
required signs remain open. The separate accepted D<=7/50 bound is not
numerically improved by (12) without a better bound on F_k. There is no new
Kneser--Poulsen consequence or assertion of full majorisation.

## 4. Compact exact evidence and trust

[weighted_degree.py](weighted_degree.py) implements the new degree and
consumer budgets using the existing rational configuration schema. It
checks the genuine kernel directly from its finite binomial/beta definition.
For integer beta parameters E sqrt(V) is rational, so whole-interval
polynomial controls of (8) require no floating quadrature. They are finite
controls, not an extrapolation to the all-N theorem. The proof above is the
all-parameter justification.

From this directory run with standard-library Python 3.11+:

    python3 -B weighted_degree.py --check
    python3 -B -O weighted_degree.py --check
    sha256sum -c SHA256SUMS

[WEIGHTED_EXPECTED.json](WEIGHTED_EXPECTED.json) is compact expected output;
[WEIGHTED_INPUTS.json](WEIGHTED_INPUTS.json) pins the reused source. Neither
the code nor its toy scalar controls compute a Gaussian beta sign, a
Gaussian integral, or a parameter cover. Superlevel geometry, layer cake,
the calculus maximum in (5), and the credited localization/rounding/moment
arguments remain written, unformalized mathematics. The exact controls are
author checks; independent review of this supplement is pending.

Validated with CPython 3.11.2, normally and under optimization. The output
status is SQUARE_ROOT_DEGREE_BUDGET_CONTROLS_PASS, with record SHA256
`715c3e59f4aae5c20340a62386c4392d2cd0ec50f5be50f592ad69fa16b4fd87`.
The controls comprise 231 kernel checks, 561 product-versus-integral beta
square-root checks, and whole-threshold-interval certificates at all 33
degrees N=0,...,32. Twelve deliberate kernel/input failures are rejected;
a separately damaged expected record is also rejected under optimization.
