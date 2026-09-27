# An averaged replica inequality signs the eighth Gaussian beta test

Status: complete author argument with an exact computer-assisted scalar
certificate, 27 September 2026. Independent mathematical review and
formalization are pending. The full dimension-three majorisation question
remains open.

## 1. Statement and role in the full criterion

Let mu be a bounded-support Borel probability measure on R3, let T be
1-Lipschitz on its support, and let s>0. Set

    C=(2 pi s)^(-3/2), f=mu*gamma_s, g=(T#mu)*gamma_s,
    d_m=C^(1-m) integral(g^m-f^m),
    a_j=d_(j+2)/[(j+1)(j+2)],
    b_(N,j)=(N+1) binom(N,j) sum_(ell=0)^(N-j)
                              (-1)^ell binom(N-j,ell) a_(j+ell).

**Theorem.** Under these hypotheses,

    b_(8,0) >= (167 sqrt(2)/4800) d_2 >= 0.                  (1)

In particular the inequality is strict whenever some pair of points in
supp(mu) has its distance strictly reduced. There is no restriction on
the number of atoms, the radius relative to s, or the paired affine rank.
The constant is sufficient; no optimality is asserted.

The beta normalization is that of the existing
[global criterion](../gaussian_majorisation_global_criterion/PROOF.md).
Writing F=f/C, G=g/C and

    H(u)=C integral[(G-u)_+-(F-u)_+],

one has a_j=integral_0^1 u^j H(u)du and
b_(8,0)=9 integral_0^1 (1-u)^8 H(u)du. Thus (1) signs the first
previously unsigned entry after the accepted
[seven-factor theorem](../gaussian_seven_factor_kernel/PROOF.md).
Together those results sign all entries of row N=8. The new proof does
not sign every b_(j+8,j), every row, every hinge, or the unrestricted
coupling defect. It gives no new Kneser--Poulsen volume theorem.

The mechanism is a nonlinear inequality between three **averaged**
replica integrals, followed by a scalar polynomial minorant. It does not
assume positivity of every conditional kernel or every polarized weight
coefficient. This distinction respects the accepted rank-six obstruction.

## 2. Replica identity and a positive lift measure

Take iid X_i with law mu, put Y_i=T(X_i), and write

    delta_12=|X_1-X_2|^2-|Y_1-Y_2|^2 >= 0,
    Z_i(t)=(sqrt(1-t) X_i, sqrt(t) Y_i) in R6,
    Q_m(t)=sum_(i=1)^m |Z_i(t)-mean_m Z(t)|^2,
    B_m=E[delta_12 integral_0^1 exp(-Q_m(t)/(2s))dt].

The standard Gaussian product identity gives

    C^(1-m) integral f^m
      =m^(-3/2) E exp[-sum_(i<j)|X_i-X_j|^2/(2ms)].       (2)

This is the replica identity in Aishwarya--Li, equation (61), and is not
new. The squared distances of Z_i(t) are affine in t. Differentiate the
scalar exponential, integrate from zero to one, and use exchangeability
of the binom(m,2) pairs. This gives the existing relative-gap identities

    d_m=(m-1) B_m/(4s m^(3/2)),
    a_j=B_(j+2)/(4s (j+2)^(5/2)).                         (3)

The factor m^(-3/2) still comes from the original dimension three.
No spatial deformation within R3 is being assumed. Bounded support
ensures finite losses and justifies the differentiation. The integrated
nonnegative identities also permit Tonelli directly.

We need a second, six-dimensional Gaussian product calculation. Put

    C6=(2 pi s)^(-3),
    K_x(t,z)=exp[-|z-(sqrt(1-t)x,sqrt(t)Tx)|^2/(2s)],
    q_t(z)=E_X K_X(t,z),
    M_t(z)=E_(X_1,X_2)[delta_12 K_(X_1)(t,z) K_(X_2)(t,z)].

Here 0<q_t(z)<=1 and M_t(z)>=0. Define a positive finite measure eta
on [0,1] by

    integral psi(u)d eta(u)
      =C6 integral_0^1 integral_R6 psi(q_t(z)) M_t(z) dz dt.

For every integer j>=0, completion of the square and independent extra
replicas give

    eta_j:=integral u^j d eta(u)=(j+2)^(-3) B_(j+2),
    a_j=sqrt(j+2) eta_j/(4s).                            (4)

Indeed C6 integral product_(i=1)^m K_(X_i)=m^(-3)exp[-Q_m/(2s)].
All integrands in this calculation are nonnegative; eta_0=B_2/8 is
finite. The signed combination below is a finite sum, so it creates
no additional convergence issue.

Define

    P8(u)=sum_(ell=0)^8 (-1)^ell binom(8,ell) sqrt(ell+2) u^ell,
    A08=sum_(ell=0)^8 (-1)^ell binom(8,ell) a_ell=b_(8,0)/9.

Equation (4) yields the exact reduction

    A08=(1/(4s)) integral P8(u)d eta(u).                  (5)

The scalar polynomial itself need not be nonnegative throughout [0,1].
The constraint on the moments of eta established next supplies its sign
after averaging.

## 3. A radius-free nonlinear inequality after averaging replicas

**Lemma.** With the definitions above,

    0 <= B_3 <= B_2,       B_4 B_2^2 >= B_3^3.           (6)

**Proof.** Fix t and the first two replicas. Put b=(Z_1+Z_2)/2 and
let U=Z_3-b, V=Z_4-b be the two independent extra replicas, with their
common conditional law. Elementary variance identities give

    Q_3=Q_2+(2/3)|U|^2,
    Q_4=Q_2+|U|^2+|V|^2-|U+V|^2/4
       <=Q_2+|U|^2+|V|^2.                              (7)

Set r=E_U exp[-|U|^2/(3s)], so 0<r<=1. Independence and the convexity
of x^(3/2) imply

    E_(U,V) exp[-Q_4/(2s)]
      >= exp[-Q_2/(2s)] (E_U exp[-|U|^2/(2s)])^2
      >= exp[-Q_2/(2s)] r^3.                            (8)

The second inequality uses exp[-|U|^2/(2s)]
=(exp[-|U|^2/(3s)])^(3/2), followed by Jensen. Importantly, this step
uses the common probability law of the extra replicas before estimating.

Use the positive measure

    dw=delta_12 exp[-Q_2(t)/(2s)]dt dmu(X_1)dmu(X_2).

Then B_2=integral dw, B_3=integral r dw, and
B_4>=integral r^3 dw. If B_2>0, Jensen for x^3 with probability dw/B_2
gives (6); also r<=1 gives B_3<=B_2. If B_2=0, the nonnegative loss is
zero mu tensor mu almost everywhere, so every B_m vanishes and (6)
holds. This proves the lemma. QED.

The argument uses neither the dimension of the auxiliary cloud nor a
radius bound. It remains valid for a general Euclidean iid cloud with a
nonnegative weight depending only on the distinguished pair, and for
any common positive averaging of the auxiliary parameter. It does not
assert B_2 B_4>=B_3^2, the stronger replica log-convexity disproved in
the earlier [curvature source](../gaussian_replica_curvature_sparse_energies/PROOF.md).

## 4. The scalar minorant and its exact certificate

**Scalar lemma.** On the whole interval 0<=u<=1,

    P8(u) >= 19/100 - (4/5)u + (1/2)u^2.                (9)

Here is a finite rational certificate of (9). Take D=10000. For each
n=2,...,10 let k_n=floor(sqrt(n D^2)), put L_n=k_n/D, and put
U_n=L_n if L_n^2=n, otherwise U_n=(k_n+1)/D. The integer pairs
k_n are

    n:    2      3      4      5      6      7      8      9     10
    k: 14142  17320  20000  22360  24494  26457  28284  30000  31622.

The exact integer inequalities k_n^2<=n D^2<=(k_n+1)^2 validate
these enclosures, with the stated exact-root convention. Replace
sqrt(ell+2) in each positive monomial of P8 by L_(ell+2), and in each
negative monomial by U_(ell+2). Subtract the right side of (9) to get a
rational polynomial L(u). Since u>=0, the original difference is >=L(u).

On each of the eight closed intervals [i/8,(i+1)/8], substitute
u=(i+t)/8 and express L in the degree-eight Bernstein basis. All 72
coefficients are strictly positive. Their global minimum is exactly

    10434391/18350080000 > 0.                            (10)

For reproducibility, if L(u)=sum c_j u^j, its power coefficients on
[a,a+h] are p_k=sum_(j=k)^8 c_j binom(j,k)a^(j-k)h^k, and its
Bernstein coefficients are

    beta_i=sum_(k=0)^i p_k binom(i,k)/binom(8,k).         (11)

The nonnegative Bernstein basis sums to one on [0,1], so positivity of
these coefficients proves L>=the positive minimum (10) on every
subinterval. Their union is [0,1]. This proves (9).

[verify.py](verify.py) constructs all coefficients in exact Fraction
arithmetic, compares them entry by entry with three levels of de
Casteljau midpoint subdivision, and verifies polynomial equality at
nine rational points per interval. Those nine points determine a
polynomial of degree at most eight; no sampled-sign inference is used.
[EXPECTED.json](EXPECTED.json) records each interval minimum, the root
enclosures, rational lower-polynomial coefficients and a hash of all
72 Bernstein coefficients. The computational premise is this finite
scalar certificate; no cubature, Monte Carlo or floating sign is used.

## 5. Finish the averaged sign

Combine (4), (5), (9) and positivity of eta:

    A08 >= (1/(4s))[(19/800)B_2-(4/135)B_3+(1/128)B_4]. (12)

If B_2=0 the desired inequality is immediate. Otherwise set r=B_3/B_2.
By (6), 0<=r<=1 and B_4>=B_2 r^3. Hence

    A08 >= B_2 h(r)/(4s),
    h(r)=19/800-4r/135+r^3/128.

On [0,1], h'(r)<=-4/135+3/128=-107/17280<0, while
h(1)=167/86400. Consequently

    A08 >= 167 B_2/(345600s),
    b_(8,0)=9A08 >= 167 B_2/(38400s)
                      =167 sqrt(2) d_2/4800,            (13)

where the last equality uses d_2=B_2/(8 sqrt(2)s) from (3).
This proves (1).

Finally let D_loss=E delta_12. The exponential factor is everywhere
positive, so B_2>0 exactly when D_loss>0. If T strictly shortens a pair
in supp(mu), continuity supplies two relative neighborhoods of positive
mu mass with strictly positive loss, and therefore D_loss>0. Conversely
if every support distance is preserved, all losses and every d_m vanish.
This proves the stated strictness, including diffuse laws and degenerate
supports.

## 6. Scope of the mechanism

The accepted seven-factor proof signs every fixed conditional kernel on
its diagonal. The present step instead retains the common law of the
extra replicas and a second positive average over the distinguished
pair. The rank-six obstruction to unrestricted conditional-kernel
positivity is therefore not a premise that needs to be overturned.
The inequality (6) is the reusable new analytic input; (9) makes it
effective for the first open test. This does not convert the accepted
global defect bound into zero or settle the remaining compact middle
interval. Those full-question obligations are unchanged.

The analytic reductions and Jensen steps above require mathematical
review. The finite scalar premise is computer-assisted, with Python's
arbitrary-precision integer and Fraction operations as its trust boundary.
The two exact algorithms are internal validation, not independent peer
review. All source and compact evidence needed to replay them are present;
no private data or omitted large certificate is required. Attribution
and dependency distinctions are recorded in [SOURCES.md](SOURCES.md).
