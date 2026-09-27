# Logarithmic noise suffices for every convex polynomial test

Author theorem with exact arithmetic controls, 27 September 2026.
Independent mathematical review is pending. Full Gaussian majorisation in
dimension three remains open. The theorem signs a whole polynomial cone
uniformly over all bounded laws and contractions; it is not a new local cell.

## 1. A uniform signed theorem

Let mu be a probability law supported in B(a,R) in R3, T be 1-Lipschitz,
and s>0. Write

    C=(2 pi s)^(-3/2), f=mu*gamma_s, g=(T#mu)*gamma_s,
    H(u)=integral(g-Cu)_+ - integral(f-Cu)_+, 0<=u<=1,
    epsilon=R^2/s,
    d=E[|X-X'|^2-|TX-TX'|^2]/s.

All spatial integrals are over R3. Favorable sign is H>=0. Both endpoint
values of H are zero. Repeated atoms, zero-weight labels and diffuse laws
are allowed; neither a covariance condition nor a positive loss floor is
assumed. R=0 is trivial. If d=0, the accepted loss-modulus result gives H=0.

**Theorem.** Let k>=12 be an integer and suppose epsilon<=1/(8k). Put

    n_k=2^(k-4)-1, r=2^(-2k), I=[r,1/4].                 (1)

For every real polynomial p of degree at most n_k, nonnegative on [0,1],
let M=max_I p. Then

    integral_0^1 p(u) H(u)du >= d M 2^(-4k-6).           (2)

In particular every polynomial energy U with U(0)=0, degree at most

                         2^(k-4)+1,                    (3)

and convex on [0,C] satisfies integral U(f)<=integral U(g). This inequality
is strict for d>0 and non-affine U. For n>=0 a convenient equivalent rule
for curvature degree n (energy degree n+2) is

    k=max(12,4+ceil(log2(n+1))),   s>=8k R^2.             (4)

Thus the sufficient variance is O(R^2 log(n+2)), not the exponentially
growing sufficient variance in the earlier finite-Hankel estimate. The
constants here are deliberately conservative; in particular this does not
improve the earlier degree-four variance cutoff. Examples of the new rule:

| s/R^2 at least | every convex energy through degree |
| ---: | ---: |
| 96 | 257 |
| 128 | 4097 |
| 256 | 268435457 |

At any fixed finite s/R^2 the degree bound is finite. Passing to all convex
energies at that fixed variance is not justified. No full hinge sign,
unrestricted quartic theorem, or Kneser--Poulsen consequence is asserted.

To see the energy normalization, put V(t)=U(Ct)/C and p=V''. Equal masses
cancel the affine part of V; layer cake gives exactly

    integral[U(g)-U(f)] = integral_0^1 p(u)H(u)du.        (5)

Nonzero p>=0 has M>0, since a polynomial vanishing on I is identically
zero. This proves the strict consequence once (2) is established.

## 2. Three Gaussian estimates, with their review boundaries

We use the accepted high-noise window and the accepted loss-dependent
modulus, with their exact source pins in INPUTS.json. The quantitative
interior estimate was already present as Theorem B of the high-noise
source, but its first review explicitly did not accept that separate
theorem. We therefore include the short derivation needed here rather
than label that interior bound independently accepted.

For every k in the theorem set

    a=2^(2-5k), r=2^(-2k), b=1/4, L=b-r.                (6)

The needed estimates are

    H(u)>=0                  on [a,1],
    H(u)>=d u/1024           on [r,b],
    |H(u)|<=16 d sqrt(u)     on [0,1].                  (7)

**Signed outer interval.** The accepted window signs H for
u>=exp(-L_epsilon), where

    L_epsilon=(4-5epsilon)^2/[32epsilon(1-epsilon)]
             >=1/(2epsilon)-3/4 >=4k-3/4.

Since exp(3/4)<=17/8<4 and exp(4)>32, exp(-L_epsilon)<a.
The high-threshold region of (7) follows, including u=1. Notice a<r<b.

**Interior lower bound.** Scale s to one. With
Z_t=(sqrt(1-t)X,sqrt(t)TX), let Q(z)=E exp(-|z-Z_t|^2/2),
V=-log Q, and

    h(z)=E[Delta(X,X') exp(-|z-Z_t|^2/2-|z-Z'_t|^2/2)]/Q(z)^2.

The accepted coarea analysis gives kappa I<=D^2V<=I, kappa=1-epsilon,
the unique mode z_*, and 0<=v_*=V(z_*)<=epsilon/2. On a ray z_*+v theta,
write w=V(z), P=V_v and J=h v^5/P. Its elementary bounds are

    kappa v<=P<=v, V_vv<=1,
    (log h)_v>=-4 sqrt(epsilon),
    h(z_*+v theta)>=d exp(-5epsilon-4 sqrt(epsilon)v).

The last inequality follows by removing the common Gaussian factor:
the numerator is at least d exp(-2|z|sqrt(epsilon)-epsilon), the squared
one-point denominator at most exp(2|z|sqrt(epsilon)), and
|z|<=sqrt(epsilon)+v. It does not replace d by a posterior loss.

Let ell=-log u with log4<=ell<=2k log2. Use epsilon<=1/(8k)<=1/96,
log2<3/4, kappa>=95/96. Then

    q=4 sqrt(2epsilon ell/kappa) <=5/2,
    beta=5-1/kappa >=379/95,  beta-q>1,
    5epsilon+q<3,  ell-epsilon/2>1.                     (8)

For w<=ell, v<=sqrt(2ell/kappa). Thus

    d(log J)/dv >=-4sqrt(epsilon)+beta/v >=1/v,
    dJ/dw >= h v^4/P^2 >=(d/27)v^2
            >=(2d/27)(w-v_*).

We used e<3. Integrating over S5, whose area is pi^3, gives
A_t'(w)>=(2pi^3d/27)(w-v_*) above the mode. Below it A_t'=0.
The accepted normalized coarea/Abel identity is

    H(exp(-ell))=exp(-ell)/(32pi^3 sqrt(pi))
        integral_0^1 integral_0^ell A_t'(w)/sqrt(ell-w) dw dt.

Since integral_0^W v/sqrt(W-v)dv=4W^(3/2)/3, this proves

    H(u)>=d u (ell-epsilon/2)^(3/2)/(324sqrt(pi))
          >d u/648 >=d u/1024.                         (9)

Here sqrt(pi)<2. The mode extension has no boundary atom, as established
in the accepted coarea dependency. The same written proof applies to
arbitrary bounded laws, without finite-atom approximation.

**Loss-dependent tail.** The accepted modulus gives
|H(u)-H(0)|<=d K_epsilon sqrt(u), where, with c=4sqrt(2epsilon/kappa),

    K_epsilon=(4+sqrt(2pi))/(16sqrt(pi)kappa^3)
       exp(5epsilon+c^2/2)(c+2)^2[4+c(c+2)].

For epsilon<=1/96, exact bounds are

    c<=3/5, kappa^(-3)<=9/8, 5epsilon+c^2/2<1/4,
    exp(1/4)<4/3,
    (4+sqrt(2pi))/(16sqrt(pi))<1/4.

The last uses 3<pi<22/7, sqrt(pi)>5/3 and sqrt(2pi)<8/3.
Therefore

    K_epsilon < (1/4)(9/8)(4/3)(169/25)(139/25)
              =70473/5000 <16.                         (10)

All three estimates in (7) are now available with the same factor d.
An absolute defect bound without d would not give the uniform theorem
near isometries.

The elementary logarithm and exponential inequalities used here can be
checked without numerical constants: the series
log2=2 sum_(j>=0) 1/[(2j+1)3^(2j+1)] puts log2 strictly between 2/3
and 3/4. The exponential series gives e<3, exp(1/4)<4/3, and
exp(1/2)<2. The outer-cutoff exponential comparisons are included in the
exact checker as a positive partial sum and a geometric tail bound.

## 3. A whole-cone polynomial certificate

The remaining step is a finite-dimensional polynomial inequality, not
sampling of Gaussian hinges or of polynomial roots. Let P_j denote the
Legendre polynomial with P_j(1)=1. On I=[r,b], write

    t(u)=(2u-r-b)/L,
    K_n(u,v)=L^(-1) sum_(j=0)^n (2j+1)P_j(t(u))P_j(t(v)).

Orthogonality gives, for every polynomial p of degree at most n,

    p(u)=integral_I K_n(u,v)p(v)dv.                     (11)

For u,v in I, |P_j(t)|<=1; hence, for p>=0 on I,

    M<=((n+1)^2/L) integral_I p.                        (12)

For u in [0,a], |t(u)|<=1+2r/L. The classical Laplace integral for
Legendre polynomials gives, for x>=1,

    |P_j(x)|<=exp(j arcosh x),
    arcosh(1+z)<=sqrt(2z).

These facts can also be verified from the elementary integral
P_j(x)=pi^(-1) integral_0^pi (x+sqrt(x^2-1)cos theta)^j dtheta.
It gives |P_j|<=1 on [-1,1] using the imaginary square root there;
the polynomial identity is justified by expanding even cosine powers.
Thus for u in [0,a], v in I,

    |K_n(u,v)|<=((n+1)^2/L) exp(2n sqrt(r/L)).

Our degree restriction and L>=1/8 give

    (n+1)^2 r<=1/256, (n+1)^2 r/L<=1/32,
    2n sqrt(r/L)<1/2, exp(1/2)<2.

Consequently (11), with p>=0 on I, gives the uniform extrapolation bound

    0<=p(u)<= (1/(16r)) integral_I p,   0<=u<=a.         (13)

Global nonnegativity of p is needed when discarding the other signed
thresholds. It is not enough that p be nonnegative only on I.

Let J=integral_I p. Using (7), dropping the other nonnegative contributions,
and using (13) in the only possibly adverse tail, we obtain

    integral_0^1 pH
      >= (d r/1024) J - (2d/(3r)) a^(3/2) J.            (14)

This pays for the entire open interval (0,a), not just an endpoint.
For k>=12,

    a^(3/2)/r^2 <=2^(3-3k),
    (2/3)2^(3-3k)<1/2048.                              (15)

The first bound follows already from sqrt(a)<=2^(1-2k). Thus (14) is
at least d r J/2048. Finally (12) gives

    J>=L M/(n+1)^2 >=32r M.

Together these inequalities prove (2). The constants in (8), (10),
(12)--(15) have exact rational controls in verify.py. The infinite k range
in (15) follows by multiplying its upper bound by 1/8 when k increases;
it is not inferred from a finite list of successful k values.

## 4. Exact Taylor moments and the R3 certification spine

This section supplies a uniform signed finite moment functional, not an
additional Gaussian sign assumption. Let n>=0, k as in the theorem, and
p(u)=sum_(r=0)^n c_r u^r, p>=0 on [0,1], M=max_I p.
The accepted R3 loss-proportional moment result gives

    a_r=integral_0^1 u^r H(u)du,
    L_(r+2)=E[P_Q(z_Y)-P_Q(z_X)]/[(r+2)^(5/2)(r+1)],
    |a_r-L_(r+2)|<=d e_r,
    e_r=[((r+2)epsilon/2)^Q]/[4(r+2)^2 Q!],              (16)

where P_Q(z)=sum_(j=0)^Q (-z)^j/j! and
z=(sum |X_i|^2-|sum X_i|^2/(r+2))/2 after scaling by sqrt(s).
The rational e_r slightly weakens the accepted power 5/2 to 2.
The full signed remainder, rather than only its absolute version, is
retained by the accompanying finite producer.

For a uniform coefficient bound, expand p on I in shifted Chebyshev
polynomials. Its constant coefficient is at most M in absolute value,
and all others at most 2M by cosine orthogonality. Since L>=1/8,
t(u)=alpha u-beta has |alpha|<=16 and |beta|<=3. The recurrence for
Chebyshev polynomials bounds their monomial coefficient l1 norms by 64^j:
the induction uses 38/64+1/64^2<1. Hence

    sum |c_r| <=2(n+1)64^n M.                            (17)

The ordinary Taylor factorial bound gives

    |sum c_r a_r - sum c_r L_(r+2)|
      <=d M (n+1)64^n/8 * [((n+2)epsilon/2)^Q/Q!].       (18)

One sufficient integer choice, with no positive lower bound on d, is

                         Q=8n+4k+24.                   (19)

Indeed Q>=3(n+2)epsilon and Q!>=(Q/e)^Q, e<3, make the factorial term
at most 2^(-Q). Also n+1<=2^n for n>=0, including n=0. Thus (18) is at
most d M 2^(-n-4k-27), and in particular at most d M 2^(-4k-8).
Combining with (2) proves the actual finite-functional sign

    sum_(r=0)^n c_r L_(r+2) >=3 d M 2^(-4k-8).           (20)

R3's paired cubature preserves d and both marginal moment lists through
degree 2Q on at most 2 binom(2Q+3,3)-1 original pairs, so it preserves
every L in (20) exactly. Equations (19)--(20) therefore give a whole
signed polynomial cone on that compressed moment representation.
They do not require rational rounding of real cubature sites or weights.
For rational finite data the L values are explicitly algebraic, with
rational coefficients times 1/sqrt(r+2), and can be enclosed outward.

The supplied moments.py computes them from the two marginal generating
functions

    E exp(t.X+v|X|^2),  weighted degree |alpha|+2j<=2Q.

Multiplying this truncated series produces moments of sums of iid replicas;
expanding (sum |X_i|^2-|sum X_i|^2/m)^j then gives the scatter moments.
The producer does not enumerate N^m label tuples. Its state count is O(Q^4),
but its naive exact convolutions and large integers can still be expensive.
The large Q in (19) is a sufficient mathematical budget, not a claim of
practical high-degree replay. Tighter certified remainder bounds may use a
smaller Q. The finite controls below do so and check every remaining error.

## 5. What is checked, and what remains mathematical

The standard-library checker validates the dyadic schedules and all rational
constant comparisons; reconstructs Legendre orthogonality and the exact
reproducing identity independently on finite polynomial spaces; and verifies
the Chebyshev coefficient norm recurrence. Actual Gaussian controls compare
the marginal generating-function producer with definition-level replica
enumeration, including full paired rank six and loss tending to zero by
vanishing weights. Directed radical intervals and the R3 remainder give
outward bounds for a curvature with a negative monomial coefficient.
The controls are calibration, not a claim of new positive configurations.

This is a compressed universal certificate: its conclusion concerns every
nonnegative polynomial in the stated finite-dimensional cone and every
admissible law, not a finite geometry mesh. The written proof supplies
Gaussian coarea/Abel analysis, Legendre identities and all infinite-parameter
quantifiers. Finite tests do not formalize those bridges, establish historical
priority, or independently accept this new theorem.

The accepted global defect bound and R3/R8 approximation frontier remain
the unrestricted context. R8's Jackson reconstruction is compatible with
the signed moment data but is not a premise here and has no independent
acceptance asserted. At fixed variance, polynomials beyond (3), the remaining
low-threshold hinge signs, and the full dimension-three theorem remain open.
