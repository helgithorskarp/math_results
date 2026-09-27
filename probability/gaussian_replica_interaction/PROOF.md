# Retaining iid interaction in Gaussian replica interpolation

Complete author proof with exact scalar certificates, 27 September 2026.
Independent mathematical review and formalization are pending. The full
bounded-law R3 Gaussian-convolution majorisation question remains open.

The main result is an averaged moment inequality with no radius, mass,
atom-count or paired-rank restriction. It keeps the interaction between
added iid replicas which the earlier eighth-beta argument discarded. Two
explicit applications sign general beta tests, including the first remaining
entry after the accepted eighth row. No complete later row is asserted.

## 1. The replica inequality and its sign consequences

Let mu be a probability measure of bounded support in R3, let T be
1-Lipschitz on its support, and let s>0. With iid X_i of law mu, write

    Y_i=T(X_i),  delta_12=|X_1-X_2|^2-|Y_1-Y_2|^2 >=0,
    Z_i(t)=(sqrt(1-t)X_i,sqrt(t)Y_i),       0<=t<=1,
    Q_m(t)=sum_(i=1)^m |Z_i(t)-mean_m Z(t)|^2,
    B_m=E[delta_12 integral_0^1 exp(-Q_m(t)/(2s))dt].     (1)

**Theorem 1 (retained-interaction inequality).** If B_m>0, then for all
integers m>=2 and ell>=1,

    B_(m+ell)/B_m >= (B_(m+1)/B_m)^p_(m,ell),
    p_(m,ell)=ell(m+ell-1)(m+1)/[m(m+ell)].              (2)

If B_m=0, all B_k vanish and the undivided versions are interpreted directly.
In particular,

    B_4^4 B_2^5 >= B_3^9,    or B_4/B_2 >= (B_3/B_2)^(9/4). (3)

This is stronger than the previous B_4 B_2^2>=B_3^3, since B_3<=B_2.
The proof of (2) works for any bounded Euclidean cloud and any nonnegative
integrable distinguished-pair weight shared by the B_k; it is independent of dimension.
The dimension-three normalization enters only the energy applications.

Put C=(2pi s)^(-3/2), f=mu*gamma_s, g=(T#mu)*gamma_s, and define the
favorable normalized hinge and its moments by

    H(u)=integral(g-Cu)_+-integral(f-Cu)_+,       0<=u<=1,
    d_m=C^(1-m) integral(g^m-f^m),
    a_j=integral_0^1 u^j H(u)du=d_(j+2)/[(j+1)(j+2)],
    b_(N,j)=(N+1)binom(N,j)
              sum_(r=0)^(N-j) (-1)^r binom(N-j,r) a_(j+r). (4)

**Theorem 2 (two unrestricted beta signs).** For the same inputs,

    b_(9,0)  >= sqrt(2) d_2/10 >=0,
    b_(12,0) >= 13 sqrt(2) d_2/1000 >=0.                 (5)

Both are strict if any distance between support points is strictly
shortened. They apply at every variance. These are two individual beta
entries, not all entries in rows9 or12. In particular b_(9,1), the whole
q=8 diagonal, unrestricted Hankel positivity, the full coupling sign and a
new Kneser--Poulsen consequence are not proved here.

## 2. Keep the interaction before applying Jensen

Fix t and the first m replicas. Write b=mean_m Z and let the ell extra
replicas have displacements U_1,...,U_ell from b. They are conditionally
iid. Set n=m+ell. Centering the full configuration gives exactly

    Q_n=Q_m+sum_i |U_i|^2-|sum_i U_i|^2/n
       =Q_m+((n-1)/n)sum_i |U_i|^2
                  -(2/n)sum_(i<j) U_i.U_j.             (6)

For one extra replica the increment is m|U|^2/(m+1). Define

    r=E exp[-m|U|^2/(2s(m+1))],
    h(U)=exp[-(n-1)|U|^2/(2sn)],  z=E h(U)>0,
    dnu(U)=h(U)dLaw(U)/z.

Equation (6), followed by Jensen for the exponential under nu^ell, yields

    E_extra exp(-Q_n/(2s))
      =exp(-Q_m/(2s)) z^ell
         E_(nu^ell) exp[(1/(sn))sum_(i<j) U_i.U_j]
      >=exp(-Q_m/(2s)) z^ell
         exp[binom(ell,2)|E_nu U|^2/(sn)]
      >=exp(-Q_m/(2s)) z^ell.                           (7)

Independence with a common tilted law is essential: it makes
E(U_i.U_j)=|E_nu U|^2 nonnegative. Individual cross terms can be negative.
The proof assumes no pointwise conditional-kernel sign.

Let V=exp[-m|U|^2/(2s(m+1))]. Then h=V^alpha, where

    alpha=(n-1)(m+1)/(nm)=1+(ell-1)/(nm)>=1.

Jensen gives z>=r^alpha. Thus the last member of (7) is at least
exp(-Q_m/(2s)) r^p, with p=ell alpha. Average against

    dw=delta_12 exp(-Q_m/(2s)) dt dmu(X_1)...dmu(X_m).

This positive measure has mass B_m; its integral of r is B_(m+1).
Since p>=1, Jensen for the normalized dw proves (2). At m=ell=2, p=9/4,
which proves (3). Boundedness justifies all integrations and exponential
moments. If B_m=0, positivity of the exponential gives delta_12=0 almost
everywhere, hence all B_k=0. This also handles point laws and isometries.

The standard variance increment also gives B_(k+1)<=B_k. In particular
B_3/B_2 belongs to [0,1], and B_5-B_6>=0. These elementary monotonicities
are used in the application; they are not new claims of this packet.

## 3. Exact conversion to a positive lifted measure

We recall the existing Gaussian replica/lift identity to fix every factor.
The Gaussian product formula gives

    C^(1-m) integral (mu*gamma_s)^m
        =m^(-3/2) E exp(-Q_m(0)/(2s)).

Since Q_m(0)-Q_m(1)=m^(-1)sum_(i<j)delta_ij, differentiation and
exchangeability give

    d_m=(m-1)B_m/(4s m^(3/2)),
    a_j=B_(j+2)/(4s (j+2)^(5/2)),
    d_2=B_2/(8 sqrt(2)s).                               (8)

For z in R6 put K_x(t,z)=exp[-|z-Z_x(t)|^2/(2s)],
q_t(z)=E K_X(t,z), and M_t(z)=E[delta_12 K_(X_1)K_(X_2)]. Define a finite
positive measure eta on [0,1] by

    integral psi(u)deta(u)
      =(2pi s)^(-3) integral_0^1 integral_R6 psi(q_t(z))M_t(z) dzdt.

Completing the square in R6 gives

    eta_j=integral u^j deta(u)=B_(j+2)/(j+2)^3,
    a_j=sqrt(j+2) eta_j/(4s).                            (9)

These identities are credited previous inputs, not new lift constructions.
For

    P_q(u)=sum_(j=0)^q (-1)^j binom(q,j)sqrt(j+2)u^j,
    G(u)=u^3-(216/125)u^4,

we consequently have

    b_(q,0)/(q+1)=(1/(4s)) integral P_q deta,
    integral G deta=(B_5-B_6)/125 >=0.                  (10)

## 4. Two exact nonlinear dual certificates

The supplied rational certificates establish on the entire interval [0,1]

    P_9(u) >= 13/20-4u+(49/10)u^2+4G(u),
    P_12(u)>= 1/3-(23/10)u+(29/10)u^2+(12/5)G(u).       (11)

Write the corresponding coefficients as (a,b,c,lambda), with b,c,lambda
positive, so the minorant is a-bu+cu^2+lambda G. Equations (9)--(11) imply

    integral P_q deta >= a B_2/8-b B_3/27+c B_4/64.

If B_2>0 put r=B_3/B_2 and use (3). The right side is at least

    B_2 [a/8-b r/27+c r^(9/4)/64].                      (12)

Set r=z^4, which covers all r in [0,1]. A second pair of exact polynomial
certificates proves

    13/160-(4/27)z^4+(49/640)z^9 >=1/200,
    1/24-(23/270)z^4+(29/640)z^9 >=1/2000               (13)

for every z in [0,1]. Multiplying by (q+1)/(4s) and using (8) gives
(5). The B_2=0 case follows directly without division.

The improved replica exponent is material to this certificate. If only the
old B_4/B_2>=r^3 is inserted into the q=12 minorant, its scalar lower bound
at r=4/5 is negative. The checker records that exact negative rational.
This does not claim that every possible use of the older estimate fails;
it identifies precisely the new premise used by this proof.

For strictness, a strictly shortened support pair has a product neighborhood
of positive mu^2 mass with delta_12>0, by continuity of T. Hence B_2>0.
The positive constants in (13) then make both comparisons strict.

## 5. Exact computation and limits of the result

For 2<=n<=14, verify.py encloses sqrt(n) on the dyadic grid of denominator
2^32, checking the squared rational endpoints. In P_q it uses the lower
root bound for positive coefficients and the upper bound for negative
coefficients. Subtracting each minorant in (11) gives a rational polynomial
which is everywhere a lower bound for that difference.

The checker certifies positive Bernstein coefficients after subdivision:
16 intervals for the degree-nine minorant difference; 32 for degree twelve;
16 for the first degree-nine polynomial in (13) minus its stated constant;
and 64 for the second. All 1376 coefficients are positive. Bernstein basis
functions are nonnegative and sum to one, so this proves the inequalities
on every closed subinterval, with no unsampled gaps.

Direct affine substitution followed by power-to-Bernstein conversion and
de Casteljau subdivision agree entry by entry. Each polynomial identity is
additionally checked at degree+1 distinct rational points per interval.
This is an identity audit; signs come from coefficient positivity, not
point sampling. Missing intervals and changed coefficients are rejected.

The code also checks the centered block quadratic identity on exact matrix
controls, its exponent conversions, and both final constants. The general
variance expansion (6), integration, and Jensen steps are written mathematics,
not formalized by these finite controls. An exploratory floating LP suggested
the small rational coefficients; neither the LP, its optimality, its grid,
nor any installed numerical package is a dependency of this proof.

This is a global averaged replica mechanism and two concrete sign consequences.
It is consistent with the accepted rank-six instantaneous Hankel obstruction:
the nonlinear power inequality does not imply unrestricted Hankel positivity.
It does not make any complete beta strip claim or change the accepted global
defect cap. The remaining full-question sign is still required. Dependency,
priority and lane boundaries are recorded in [SOURCES.md](SOURCES.md).
