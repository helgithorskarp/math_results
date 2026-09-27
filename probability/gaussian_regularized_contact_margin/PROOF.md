# A Gaussian-tail completion of the small-loss contact margin

27 September 2026. Complete author proof, pending independent review.
The essential bounded-input dependency is R3's independently accepted
[effective mean-loss theorem](../gaussian_effective_mean_loss/PROOF.md),
accepted at graph6432. That review does not cover the new transfer proved
here. The unrestricted dimension-three question remains open.

## 1. Actual regularized inputs and the conclusion

Write gamma_s=N(0,s I_3), C=(2pi)^(-3/2), omega=4pi/3, and
L_f(v)=sup_(|E|=v) integral_E f. Fix integers L>=1 and b>=20. Let U be
ANY centered random vector supported in B(0,L), let Z be an independent
standard normal in R3, and suppose

    2^-b <= beta <= 2^-20,
    X=U+sqrt(beta)Z,
    F:R3->R3 globally 1-Lipschitz,
    f=law(X)*gamma_1,      g=(F#law(X))*gamma_1,
    Delta=|X-X'|^2-|F(X)-F(X')|^2 >= 0,
    d=E Delta,            M=2^20(L^2+b+1).                 (1)

Primes denote independent copies of the complete input. No finite-support
or minimum-prior assumption is imposed on U. F is applied to X, not merely
to the centers U. All moments used below are finite by Lipschitz growth.

**Theorem.** If 0<d<=2^-M, then simultaneously for every 0<v<=omega L^3,

    L_g(v)-L_f(v) >= (C/8) v d^(513/512) > 0.             (2)

At d=0, F is a Euclidean isometry and all profiles agree. In particular,
any nontrivial profile contact in the range of (1)--(2) has d>2^-M.
Global order at other volumes is not a premise of (2).

For the exact auxiliary family rho=nu*gamma_epsilon at output heat time
s>0, apply (1) to (X-E U)/sqrt(s). It is enough that

    |U-E U| <= L sqrt(s),
    2^-b <= epsilon/s <= 2^-20,
    d=E[|X-X'|^2-|F(X)-F(X')|^2]/s <= 2^-M.

The conclusion is (2) with C replaced by C_s=(2pi s)^(-3/2) and
0<v<=omega L^3 s^(3/2). The centered/scaled endpoint map remains globally
nonexpansive. A c-Lipschitz map with c<1 has d>0, since the input has
positive covariance, so it cannot give a contact in this range.

The result removes the unverified core/tail premise left in Section 6 of
the accepted [near-isometry contact theorem](../gaussian_contact_near_isometries/PROOF.md)
for this explicit smoothing/loss regime. It also permits arbitrarily large
displacements in remote Gaussian tails. It does not establish the sign at
general loss, arbitrary epsilon/s, or all volumes for one fixed positive d.

## 2. The credited bounded-input estimate

We use the bounded-volume version of R3's theorem. A centered source law
supported in B(0,R), with covariance at least kappa I_3, has a contracted
image of mean pair loss d_0. For volumes at most omega L^3 put

    tau=exp(-(L+R)^2/2),    w=exp(-(L+3R)^2/2),
    K0=2R^2/kappa,        A=96R^3/kappa+6R,
    K1=16R/kappa,         K2=2R/tau^2,
    c0=w^2 min(tau/4,1/16),    delta=c0/(4K1).             (3)

Let d_* be the minimum of the seven numbers

    kappa^2/(4R^2K0),
    delta^2/(2K0),
    kappa delta^2/(8R^2K0),
    w^4 kappa^2 delta^2/(144R^4K0),
    2 kappa delta/R,
    c0 delta^4/(8 A^2 K0^2),
    c0^2 delta^4/(64 K2^2 K0^3).                          (4)

If 0<d_0<=d_*, the conditional source/target profiles satisfy

    L_g0(v)-L_f0(v) >= (C c0/2) v d_0.                  (5)

The substitution B=L+2R in that theorem is valid: every source top set
of volume v<=omega L^3 has threshold at least C tau and is contained
in B(0,L+2R). Testing on the actual source set gives (5). Separate
centering/Procrustes alignment of the conditional target leaves its
profile and pair losses unchanged. Formulae (3)--(5) are credited input,
not a new first-variation or rare-displacement proof.

## 3. Truncate the independent Gaussian increment

Choose the unique integer m with

    2^(-m-1) < d <= 2^-m;       m>=M.

Set E={|Z|<=4sqrt(m)}, p=Pr(E^c), and let X_0 have the conditional law
of X given E. The cutoff is on the independent Gaussian increment, not
on U+sqrt(beta)Z. Thus U keeps its law and is still independent of the
radially truncated Z. In particular E X_0=0.

The elementary chi-square moment identities give

    E exp(|Z|^2/4)=2^(3/2)<3,
    E[|Z|^2 exp(|Z|^2/4)]=3*2^(5/2)<17.

Since e>2, exponential Markov bounds imply

    p <= 3*2^(-4m),
    G:=E[|Z|^2 1_(E^c)] <= 17*2^(-4m).                 (6)

Rotational symmetry yields

    Cov(X_0)=Cov(U)+beta (3-G)/[3(1-p)] I_3
             >= (beta/2) I_3.                          (7)

For m>=1, the displayed bound on G is below 3/2. We can therefore use

    R=max(1,L+4sqrt(beta m)),   kappa=beta/2             (8)

in the bounded theorem. The maximum is harmless since L>=1. The core
still uses the SAME map F; conditioning has not substituted a different
endpoint image or optimized set.

Loss retention needs more than a small discarded probability. Let
d_0=E[Delta | E and E'] and
T=E[Delta 1_(E^c union E'^c)]. Then

    d=(1-p)^2 d_0+T,     T>=0.

As Delta<=|X-X'|^2 and E X=0, the union bound gives

    T <= 2 E[|X|^2 1_(E^c)]+2p E|X|^2
       <= (4L^2+6beta)p+2beta G
       <= (12L^2+52)2^(-4m)
       <= 2^(-3m).                                      (9)

For the last step, use L^2<=m and 64m<=2^m for m>=16. The centered
cross term vanishes because U is independent of the radial event E.
Equation (9), the loss bin, and (6) imply

    d/2 <= d_0 <= 2d.                                   (10)

In particular all the loss cannot escape into the discarded tail. This
is an essential part of the argument; truncation at a fixed radius would
not justify (10).

## 4. The cutoff survives the growing core

Put q=m/8192. The assumed m>=2^20(L^2+b+1) gives

    L^2<=q/128,     b+1<=q/128,     q>=2816.

The bound beta<=2^-20 gives

    R<=L+sqrt(m)/256<=5sqrt(m)/1024<sqrt(m).

For m>=2^20, sqrt(m)<=2^(m/8192)=2^q. One elementary proof splits
m into intervals [2^j,2^(j+1)), j>=20, and uses
(j+1)/2<=2^(j-13), proved by induction from j=20.

The two Gaussian weights in (3) obey

    (L+R)^2/2 <= 4L^2+m/65536,
    (L+3R)^2/2 <= 16L^2+9m/65536.

Using e<4 and the preceding bound on L^2, it follows that

    tau >= 2^(-q),       w >= 2^(-4q),
    R <= 2^q,           kappa >= 2^(-q).                (11)

For example the two upper bounds on their negative base-two exponents
are 8L^2+m/32768<=5q/16 and
32L^2+9m/32768<=5q/2, respectively. The covariance bound follows from
kappa>=2^(-b-1).

Applying (11) in (3), with R>=1 and kappa<=1, gives

    K0,K1,K2 <= 2^(4q),     A<=2^(8q),
    c0 >= 2^(-16q),        delta>=2^(-32q).              (12)

Here min(tau/4,1/16)>=tau/16. Additive constants in the exponents
are absorbed since q>=8. Substitution into the seven entries of (4)
gives the following lower bounds, in the same order:

    2^(-9q), 2^(-69q), 2^(-72q), 2^(-91q),
    2^(-34q), 2^(-169q), 2^(-181q).                     (13)

For clarity, before absorbing constants the negative exponents are
8q+2, 68q+1, 71q+3, 90q+8, 34q-1, 168q+3 and 180q+6.
These are universal affine inequalities on q>=8, not a sampled schedule.
In particular

    d_* >= 2^(-256q)=2^(-m/32).

By (10), d_0<=2d<=2^(1-m)<=2^(-m/32). The bounded theorem therefore
applies to the actual conditional law at every permitted volume.

## 5. Restore the Gaussian tail, preserving the volume factor

For each of the source and target, the full output density is a mixture
(1-p)u_0+p u_1 of variance-one Gaussian convolutions. Both components
lie between zero and C pointwise. Therefore

    ||u-u_0||_infinity <= p C,
    |L_u(v)-L_u0(v)| <= p C v.                           (14)

This is stronger for small volumes than an absolute mass-error bound.
Combining (5), (10), (12) and (14) gives

    L_g(v)-L_f(v) >= C v (c0 d/4-2p).

The Gaussian tail is now smaller than the loss-dependent margin:

    2p <= 6*2^(-4m) <= 2^(-m-16q-4) < c0 d/8.          (15)

Indeed 3m-16q>=7, while 6<8; the last strict comparison follows from
the lower endpoint of the loss bin and c0>=2^(-16q). It follows that

    L_g(v)-L_f(v) >= (C/8)v c0 d
                   >= (C/8)v d^(1+1/512),

because 16q=m/512 and d<=2^-m. This proves (2), uniformly down to
arbitrarily small positive volume.

If d=0, the nonnegative pair loss vanishes almost surely. The input law
has full support, and F is continuous, so all pair distances in R3 are
preserved. A distance-preserving map R3->R3 is an affine Euclidean
isometry. This proves the equality statement separately, without taking
a logarithm of zero.

## 6. Contact consequence and limits

The [ordered-contact reduction](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md)
uses precisely an input nu*gamma_epsilon and applies a global c<1 map
after smoothing. For every such contact satisfying epsilon/s<=2^-20,
choose integers b,L as in Section 1 that also cover its source-center
radius and its contact volume. Its normalized loss MUST satisfy

    d > 2^(-2^20(L^2+b+1)).                              (16)

Otherwise the actual concentration profiles are strictly separated, so
there is no contact at which to realize an adverse Brownian flux. This
excludes a genuine portion of the contact problem; it is not a statement
about only first-hit event probabilities or a relaxed martingale law.

No argument here forces an arbitrary selected contact to have this small
smoothing ratio or sufficiently small loss. The volume bound is not
uniform as v grows to infinity. The numerical cutoff is deliberately
very small and does not imply a feasible exhaustive cover. There is no
new all-threshold, all-variance, or KP theorem. R3's bounded theorem and
the accepted R1/R8 ingredients retain their own exact scopes and review
status. Ordinary Gaussian tail truncation is not claimed as a novel
probabilistic tool; its role here is to close the loss-relative error
and covariance budgets for the actual auxiliary family.

The universal proof is written mathematics. The companion checker
verifies its affine exponent certificates and finite algebraic controls,
including a control where all loss lies in a small tail. It does not
compute a Gaussian profile, construct a contact, independently review
the bounded-input theorem, or formally verify the analytic proof.
