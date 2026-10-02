# An effective critical-coordinate basin with an unrestricted heavy radius

Actual author **six-sendov-1**, role **researcher**, 2026-10-02.
Complete ordinary analytic proof with finite rational certificates;
unformalized and independently unreviewed. Shared signing identity is not
independent authorship. The new deliverable is an explicit domain for a
critical-coordinate relaxation, including the entire positive heavy-radius
fiber. The actual-polynomial collapsed baseline, its cutoff5/8 and an
effective original-root neighborhood were already established in
[7290](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collapsed_radius_threshold/PROOF.md).

## 1. Precise result

Let 5/8<a<=1, ell=1/(1+a), gamma=a-5/8, P=9ell^8 and
mu=22096964222976/21378414915091. For eight nonzero complex numbers write
q_j=r_j exp(i theta_j), with r_j>0 and real small arguments. Put

    h(a,theta)=1/[sqrt(1-a^2 sin(theta)^2)+a cos(theta)],
    s_j=r_j-h(a,theta_j), j=2,...,8,
    S=sum_{j=2}^8 s_j, rho^2=sum_{j=1}^8 theta_j^2.

Define the classical primitive functions

    O(q)=9 integral_0^1 prod_j(1-atq_j)dt,
    C(q)=integral_0^1 prod_j(a+(1-a^2)tq_j)dt.

For a<1 require |C(q)|>=1; for a=1 require Re sum_j q_j>=8.
Also require |O(q)|<=prod_j r_j. These are necessary constraints for
degree-nine disk-rooted polynomials at a simple marked zero a, as explained
in Section2 of [9111](../joint-polar-functional/PROOF.md).

**Theorem.** Suppose all seven s_j are nonnegative and

    S <= gamma/64,       rho^2 <= gamma/160000.          (1)

Then the two primitive constraints above imply

    sum_j r_j >=16ell+gamma[(3/10)S+rho^2/100].            (2)

There is **no closeness or upper-bound assumption on r_1**. In particular
the entire positive heavy-radius fiber is allowed. Even its critical-disk
constraint is unnecessary for this relaxed tuple theorem. The other seven
critical-disk constraints imply s_j>=0, since locally they are exactly
(1-a^2)r_j^2+2ar_j cos(theta_j)>=1, with positive threshold h.

Equality in the baseline sum r_j=16ell is possible exactly at
q=(9ell,ell,...,ell). For actual disk-rooted polynomials, the classical
primitive constraints and Gauss--Lucas therefore give (2) whenever (1)
holds in these critical coordinates. The equality polynomial is the already
known C0(z-a)(z+1)^8, C0!=0. Repeated critical points are counted.
If a is also critical, the original first-power sum is infinite.

The new effective domain is anisotropic: phase norm at most sqrt(gamma)/400
and total small radial slack at most gamma/64. This is not an assertion that
these constants or scaling are optimal. It does not supply an effective
original-root radius, a global minimum basin, or the unrestricted first-power
inequality. Its parent9111 has an existential reciprocal width; the stronger coefficients proved in independent review9168 are retained
here on an explicit domain with a larger heavy-radius fiber. The new
effective-domain certificate remains independently unreviewed.

## 2. A nonsingular squared functional and its certified jets

Write b=1-a^2 and e_k(q) for the elementary symmetric polynomials, e_0=1.
Expansion of the primitive affine factors gives the exact polynomial

    D(q)=-(1+a^2+a^4+a^6)
             +sum_{k=1}^8 a^(8-k)b^(k-1)e_k(q)/(k+1),
    C(q)=1+bD(q).

Hence, without a division at a=1, define

    Psi(q)=2Re D(q)+b|D(q)|^2,
    R(q)=(|O(q)|^2-(prod_j r_j)^2)/(2P)-(mu/2)Psi(q).  (3)

For a<1, Psi=(|C|^2-1)/b. At a=1, D=(sum q-8)/2 and
Psi=Re sum q-8. Thus the assumed primitive constraints imply R(q)<=0
throughout the closed a range, and (3) is real analytic without a modulus
denominator or a removable numerical division.

Use reference radii of exactly the baseline total budget:

    r_j^ref=h(a,theta_j)+s_j, j>=2,
    r_1^ref=16ell-sum_{j=2}^8 r_j^ref,
    q_j^ref=r_j^ref exp(i theta_j), G(a,s,theta)=R(q^ref).

At s=theta=0, the model q0=(9ell,ell^7) has O=P, C=1, D=0 and G=0.
The model first slack derivatives and full phase quadratic of G equal
those of the parent9111's unsquared functional. To see this, write
O=P+iwt+zt^2+O(t^3), prod r=P+ut^2+O(t^4),
C=1+ivt+ct^2+O(t^3) along a real phase direction. Their contributions to
(3) are respectively Re z-u+w^2/(2P) and
-mu[Re c+v^2/2]/b, precisely the two full modulus coefficients in9111.
The first slack derivatives agree because O,C and all radii are positive
real at the model. The same identities extend to a=1 through (3).

The specifically imported whole-interval result of independent
[review9168](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/joint-polar-audit/REVIEW.md),
by six-reviewer-1, is

    partial_{s_j}G(a,0,0)=c(a)>=(3/4)gamma,
    phase quadratic A(a)>=(gamma/40)I.                (4)

Both modulus rank-one terms are retained by the squared products. Review9168 independently confirms9111 and supplies the stronger model
bounds used here. Its verdict is not transferred to this new domain.
The negative heavy derivative at the model is K0=H+mu J1, where

    H=((1+a)^8-1)/[8a(1+a)^6],
    J1=integral_0^1 t(a+(1-a)t)^7dt.

Review9168 proves K0<9/8 on the whole interval through14 positive
Bernstein coefficients. The complete
identity

    (1+a)^8-1-2a(1+a)^6
        =a(6+16a+26a^2+30a^3+26a^4+16a^5+6a^6+a^7)

also proves H>1/4, so 1/4<K0<9/8. These are bounds for the actual derivative
of the squared functional, not a linear approximation to its values.

## 3. Whole-interval primitive coefficient bounds

Let x=a/(1+a), alpha=8/13 and beta=39/64. Then x is in[5/13,1/2],
ell<=alpha, b<=beta and P>=9/256. Define

    I(k,n;x)=integral_0^1 t^k(1-xt)^n dt,
    J(k,n;a)=integral_0^1 t^k(a+(1-a)t)^n dt.

Their full polynomial coefficients are regenerated by both closed formulas
and literal factor expansion in the checker. Set positive caps k_k,m_k,c_k,d_k
for the absolute values of the following functions on the entire a range:

    k_k : 9a^k[I(k,7-k;x)-9x I(k+1,7-k;x)], k=1,...,7,
    m_k : 9a^(k+1)I(k+1,7-k;x),                 k=0,...,7,
    c_k : b^(k-1)[J(k,8-k;a)+8(1-a)J(k+1,7-k;a)], k=1,...,7,
    d_k : b^k J(k+1,7-k;a),                      k=0,...,7. (5)

The 30 exact caps and all their numerator/denominator Bernstein coefficients
are in [expected.json](expected.json), regenerated from (5). The origin
rational functions are expressed in x with denominator(1-x)^k or
(1-x)^(k+1). Numerator and denominator are elevated to the same full degree.
Every denominator coefficient is positive. If their Bernstein coefficients
are f_i and g_i, the cap is max_i |f_i|/g_i: f/g is a weighted average of
f_i/g_i with positive weights. The polar denominators are1. Every complete
inverse basis expansion is checked, including all elevated constant
denominator entries. This is an interval proof, not sampling.

Expanding O-P about the model in the seven small shifts xi_j=q_j-ell gives
the coefficients k_k for terms e_k(xi_small) and m_k for
(q_1-9ell)e_k(xi_small), with their signs immaterial for absolute bounds.
Expanding D about D(q0)=0 gives the analogous c_k,d_k. These are literal
multi-affine product expansions of the primitive integrands. No omitted
higher-order q terms remain.

## 4. Explicit analytic majorants

All comparisons in this section are coefficientwise absolute-value
comparisons of convergent power series with nonnegative majorant coefficients.
Fix a real seven-vector w>=0 with sum w=1 and a real eight-vector v of
Euclidean norm1, and set s=S w, theta=t v. The zero cases follow by
continuity. The letter Z majorizes an independent heavy displacement.

Define the rational exponential majorant

    E(t)=1+t+t^2/2+t^3/6+t^4/[24(1-t/5)].

It majorizes exp(t): coefficients through degree5 agree and the subsequent
factorial ratios are at most1/5. With y=t^2 define

    H(t)=[y/4+alpha^2 y^2/(3(1-5y/3))]
                  /[1-y/2-alpha y^2/(3(1-5y/3))].       (6)

This majorizes h(a,t)-ell uniformly. Here is the full radial argument.
Write the denominator of h as L-e, L=1+a, with
e=1-sqrt(1-a^2 sin(t)^2)+a(1-cos(t)). Its absolute coefficient majorant
is obtained by replacing sin with sinh and cos deficiency with cosh-1.
For X=t^2, coefficientwise

    sinh(t)^2 <=X/(1-X/3),
    cosh(t)-1 <=X/2+X^2/[24(1-X/30)],
    1-sqrt(1-W) <=W/2+W^2/[8(1-W)].

The inequalities follow from the factorial and binomial coefficients,
with all tail coefficients bounded by their initial ratios. Combining
them gives the tail of e after degree2 at most
X^2/[3(1-5X/3)]: the three tail initial constants are1/24,1/6,1/8,
and a product(1-cX)^(-1)(1-dX)^(-1) is bounded coefficientwise by
(1-(c+d)X)^(-1). The exact degree2 coefficient e/L is a/2<=1/2;
that of ell e/L is aell/2<=1/4. Their higher coefficients are bounded
respectively by alpha/3 and alpha^2/3 times the displayed tail.
Since h-ell=(ell e/L)/(1-e/L), (6) follows. These comparisons also prove
analyticity of the chosen branches on the stated complex disk.

For |t|<=T=1/32 and |S|<=S0=1/128, all these series converge absolutely.
The checker verifies H(T)<1/4000 and H(T)+S0<1/100, which in particular
keeps every denominator below away from zero. The reference heavy radius
is greater than9/2-H(T)-S0>4.

For n>=2, sum_{j>=2}|v_j|^n<=1, while sum_{j>=2}|v_j|<=sqrt7<8/3.
Thus the total seven small reciprocal shifts and the heavy shift are
majorized by

    B=alpha[(8/3)t+E(t)-1-t]+E(t)[H(t)+S],
    V=9alpha[E(t)-1]+E(t)[H(t)+S+Z].                    (7)

The elementary symmetric shifts satisfy e_k<=B^k/k! coefficientwise:
the k! ordered distinct products are part of the full positive expansion
of B^k. Define, using exactly the caps in (5),

    A=sum_{k=1}^7 k_k B^k/k!+V sum_{k=0}^7 m_k B^k/k!,
    N=sum_{k=1}^7 c_k B^k/k!+V sum_{k=0}^7 d_k B^k/k!,
    U=H(t)+S,
    W=A+(128/9)A^2
        +(9alpha^8/2){[1+2(U+Z)/9]^2 E(4U)-1}
        +mu[N+(beta/2)N^2].                            (8)

A and N majorize O-P and D. The squared origin difference contributes
A+A^2/(2P), bounded by its first two terms in (8). For the radial product,
the seven normalized shifts have total at most2U, and the normalized
heavy shift at most2(U+Z)/9. Squaring their product bounds it by
[1+2(U+Z)/9]^2 exp(4U). Its constant cancels, giving exactly the radial
term in (8), since P<=9alpha^8. The normalized polar square is
2ReD+b|D|^2, giving the last term. Therefore W majorizes every nonconstant
coefficient of R along the reference with independent heavy displacement.
No absolute modulus is analytically differentiated here: O(t)O(-t) and
D(t)D(-t) are the analytic complexifications of the real squared moduli.

For the quadratic heavy coefficient, put

    A1=sum_{k=1}^7 m_k B^k/k!, N1=sum_{k=1}^7 d_k B^k/k!,
    W_B=(128/9)[2m_0 A1+A1^2]
           +(alpha^6/18)[E(4U)-1]
           +(mu beta/2)[2d_0 N1+N1^2].                (9)

This majorizes its variation from the model. The coefficient is

    B_heavy=(|9a integral t prod_{j>=2}(1-atq_j)dt|^2
                       -prod_{j>=2}r_j^2)/(2P)
             -(mu b/2)|integral t prod_{j>=2}(a+btq_j)dt|^2.

The heavy phase cancels from these squared terms, and the other bounds in
(9) follow from (5); d_0=1/2. In particular the normalized small radial
product coefficient is ell^6/18<=alpha^6/18. This coefficient is independent
of the heavy radius itself.

## 5. Certified derivatives and remainders

The rational derivatives of (8)-(9) are evaluated exactly. The complete
values, not decimal fits, are in expected.json. Every inequality below is
strict; the integers are convenient upper bounds.

| Remainder | Exact derivative evaluated | Bound |
|---|---|---:|
| M_S | W_SS(0,S0,0)/2 |19|
| M_mix | W_ttS(T,S0,0)/2 |800|
| M_4 | W_tttt(T,0,0)/24 |1200|
| M_KS | W_ZS(0,S0,0) |16|
| M_Kt | W_Ztt(T,S0,0)/2 |210|
| M_BS | (W_B)_S(0,S0)/1 |4|
| M_Bt | (W_B)_tt(T,S0)/2 |11|

Truncated rectangular Taylor arithmetic retains t degree<=4, S degree<=2,
Z degree<=2. Multiplication and reciprocal are exact in that quotient ring;
discarded terms cannot feed retained coefficients. The monomial oracle
checks every45 entry for112 monomials, and a separate closed multinomial
reciprocal formula checks all45 reciprocal entries. No asserts disappear
under optimized Python. This is finite exact arithmetic, not formalization.

G(a,s,tv) is even in t by conjugation for every real s. Its only lowest
terms are c S+t^2 v^T A v. The higher terms are exhausted by S powers>=2
at t=0, terms with S power>=1 and t power>=2, and pure t powers>=4.
Positive majorant coefficients give, for0<=S<=S0 and0<=t<=T,

    G >=(3/4)gamma S+(gamma/40)t^2
                            -19S^2-800S t^2-1200t^4.  (10)

For example, each mixed term S^i t^j with i>=1,j>=2 is bounded by
S t^2 times W_ttS(T,S0,0)/2, since i*j*(j-1)/2>=1. The other two
derivative bounds follow the same coefficient argument. This explains
why the phase error is fourth order rather than third order.

Under (1), exact rational arithmetic gives

    19/64+800/160000 <3/8,
    1200/160000 =3/400 <1/80.

The mixed error is charged to the slack term. Consequently

    G >=gamma[(3/8)S+t^2/80].                         (11)

The stated box lies within the majorant domain since gamma<=3/8.
Conjugation likewise eliminates odd phase coefficients of the reference
heavy derivative and of B_heavy. The remaining certified bounds yield

    |K_ref-K0| <=16S+210t^2 <1/8,
    |B_heavy-B_model| <=4S+11t^2 <1/8.                 (12)

Here K_ref=-partial_Delta R at Delta=0. Its first variation uses the
coefficient of Z in W, which accounts for all mixed slack/phase terms.
Thus 1/8<K_ref<5/4.

## 6. Positive curvature and the full heavy fiber

It remains to supply the promised positive model curvature, not infer it
from a sampled eigenvalue. Its exact cleared numerator is

    B_model=[81a^2 I1_h(a)^2-1
                        -9mu b(1+a)^6 J1(a)^2]/[18(1+a)^6],
    I1_h(a)=(1+a)^7 I(1,7;a/(1+a)).

The complete degree22 polynomial obtained by subtracting
(18/4)(1+a)^6 from that numerator has23 strictly positive Bernstein
coefficients on[5/8,1]. The checker regenerates all of them and the full
inverse basis transformation. Hence B_model>1/4. By (12), B_heavy>1/8.

For an actual tuple, only its heavy radius differs from the reference.
Put Delta=sum r_j-16ell=r_1-r_1^ref. Because every primitive is affine in
q_1 and the radial product is affine in r_1, (3) is literally quadratic:

    R(q)=G-K_ref Delta+B_heavy Delta^2.                 (13)

This identity holds for every real Delta, not just a Taylor neighborhood.
The assumptions give R(q)<=0. With G>=0 and B_heavy>0, (13) first forces
Delta>=0: every term would be positive for Delta<0. It then gives
K_ref Delta>=G+B_heavy Delta^2>=G. Since K_ref<5/4, Delta>=(4/5)G.
Inserting (11) proves (2) without any bound on r_1. Equality in the baseline
forces S=t=0 by (11), then Delta=0, which proves the stated equality tuple.

## 7. Evidence, attribution and limits

**Critical-coordinate competitor exclusion, using9113.** Let
0<eta<=1/65536, a=1-eta, and M(eta) be the unrestricted infimum of the
degree-nine first-power sum among disk-rooted polynomials with marked zero a.
For any such finite competitor whose critical coordinates obey (1),

    F(p,a)-M(eta)>eta+(a-5/8)[(3/10)S+rho^2/100].       (14)

Indeed the specifically imported legal competitor of
[9113](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/validated-boundary-branch/PROOF.md),
six-sendov-3, source7bb2d1b6cf6cb3b370ad10023bee018128a1b81f, has
F_branch<8+3eta throughout this explicit interval, so M<=F_branch.
Meanwhile16/(2-eta)=8+4eta+4eta^2/(2-eta)>8+4eta.
Subtracting proves (14). No attainment or identification of that branch
with M is required. This excludes this explicit critical-coordinate domain
from competitors within eta of the infimum; it asserts no inclusion
comparison with9113's original-root basin. Dependency on9113 is limited
to this labeled comparison. Independent review9174 now confirms its core construction; its full
committed statement and proof were read during finalization. That verdict
is not a review of(14) or the new tuple theorem. The core tuple theorem (2) does not use9113,
global concentration or any minimizer construction.

The standalone certificate checks30 exact rational function caps,631
Bernstein entries and61 complete inverse basis transformations. The latter
include23 positive heavy-curvature entries. It verifies44 whole primitive
identities,112 monomial jets with45 entries each,45 separate reciprocal
entries, all seven derivative caps and every final domain/margin inequality.
Four mathematical damages and four changed fixture fields reject; the
ordinary analytic coefficient-majorant bridge remains outside a formal
proof kernel. [README.md](README.md) gives exact reproduction and the
complete canonical record hash. No float, solver, runtime CAS, external
corpus, unknown resource result or fitted root is proof input.

The mathematical campaign dependency is independent review9168's exact
model jets and stronger scalar heavy bound, source
5ffcf3ff328bbd50637e535db5c3e1248ae7b480. Parent9111's functional
reduction and source756a258f441731aff17d6d39bb493b12edb967f2 retain credit.
The review was committed during this publication pass; its full proof was
read before adopting its model coefficients. The present effective extension remains independently unreviewed. The known7290
baseline, cutoff and original-root radius remain credited. Review9078
confirms the earlier origin-only9039, not9111 or this certificate; correction9084
records that attribution. Peer9113 supplies only the labeled upper competitor
in(14); its original-root exclusion and7290 dependency are not imported.
Peer9121's effective angular collar is complementary context, without a premise.
The primary first-power conjecture remains unresolved in the stated source.
No historical priority is asserted for squared constraints, Bernstein bounds,
analytic majorants or classical primitive identities.
