# Sharp Newton-defect stability for eight coordinates

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.
Complete ordinary written author proof, with separate exact algebra checks.
Unformalized; independent review is pending. Historical priority of the
precise refinement is not established; see [LITERATURE.md](LITERATURE.md).
The main moment theorem is self-contained. The labeled origin and phase
applications inherit the published results identified below.

## 1. Normalized theorem, sharpness and equality

For eight nonnegative real numbers y with sum y_j=8, let

    p_k=sum_j y_j^k, M=max_j y_j,
    D(y)=2e_2(y)-e_3(y),
    U(y)=sum_j(y_j-1)^2=p_2-8,
    E(y)=min_i ||y-8e_i||^2=p_2+64-16M,
    d(y)^2=min(U(y),E(y)).

Here e_k is the unnormalized elementary symmetric polynomial, e_i in
the distance expression is the i-th standard coordinate vector, and
all norms and distances are Euclidean.

**Theorem.**

    D(y)>=d(y)^2.                                             (1)

Equality holds exactly at the uniform vector (1^8), the permutations of
(8,0^7), and the permutations of (9/2,1/2^7). The coefficient1 is sharp:
at the last vector D=U=E=14. Consequently the zero set of D is exactly
uniform and spikes. Classical Maclaurin already gives D>=0; (1) is an
explicit quantitative refinement, not a claim that its nonnegativity is
new.

Newton's identities, with e_1=8, give

    e_2=(64-p_2)/2, e_3=(512-24p_2+2p_3)/6,
    D=(9p_2-p_3-64)/3.                                       (2)

The nearest of the two equality families changes at M=9/2, since
E-U=72-16M. Put g(t)=6t^2-t^3. Thus

    3(D-U)=sum_j g(y_j)-40,
    3(D-E)=sum_j g(y_j)-256+48M.                              (3)

## 2. Lower-maximum region: complete reduction and equality transfer

Assume M<=9/2. The set [0,9/2]^8 intersected with sum y=8 is compact.
Minimize sum g on this set and choose a minimizer with the smallest
number of coordinates strictly between its two endpoints. Such a choice
exists because the possible counts form a nonempty finite set of integers.

For two coordinates x,z of fixed sum S,

    g(x)+g(z)=6S^2-S^3+(3S-12)xz.                             (4)

Two interior coordinates admit two-sided variation (x,z)->(x+h,z-h).
Its derivative at zero is (3S-12)(z-x). If x!=z, stationarity forces
S=4. Then (4) is constant on the whole feasible fixed-sum segment, and
moving the pair to (0,4) keeps it in [0,9/2]^2. It preserves the minimum
while decreasing the number of interior coordinates, a contradiction.
Hence all interior coordinates of the selected minimizer are equal.

There is at most one ceiling coordinate9/2 because twice that ceiling
exceeds8. A vector with only endpoints cannot have sum8, as 9k/2=8 has
no integer solution. The complete list of possible minimizing profiles is:

* No ceiling and m equal free coordinates8/m, with m=2,...,8; all
  remaining coordinates are zero. The ceiling excludes m=1.
* One ceiling9/2 and m equal free coordinates7/(2m), with m=1,...,7;
  all remaining coordinates are zero.

There are14 profiles, including every feasible endpoint/free-count case.
Direct substitution, or the following factorizations, gives

    m g(8/m)-40
       =8(8-m)(5m-8)/m^2 >=0              (2<=m<=8),          (5)
    g(9/2)+m g(7/(2m))-40
       =7(7-m)(11m-7)/(8m^2)>=0           (1<=m<=7).          (6)

Every factor other than8-m or7-m is strictly positive on the indicated
integer intervals. The only zero profiles are m=8 in (5) and m=7 in (6).
Compact minimization now proves sum g>=40 throughout this region,
so (3) yields D>=U=d^2.

The equality classification requires more than checking the14 profiles.
If an equality vector had a zero coordinate, keep that coordinate fixed
and repeat the compact minimum/fewest-interiors argument on that closed
face. The resulting profile still has a zero coordinate, whereas both
zero-excess profiles in (5)-(6) have eight positive coordinates. This is
impossible. If an equality vector had unequal interior coordinates,
stationarity and (4) would produce an equality vector with a zero
coordinate, also impossible. Therefore an equality vector has no zero
coordinate and has all its interior coordinates equal. It is precisely
uniform or one ceiling9/2 followed by seven1/2 values.

## 3. Upper-maximum region: strict averaging and exact factorization

Assume M>=9/2. The sum constraint makes this maximal coordinate unique.
Write M=8-L, where 0<=L<=7/2. The other seven nonnegative coordinates
sum to L. Every pair among them has S<=L<=7/2<4, so the coefficient
3S-12 in (4) is strictly negative. Averaging an unequal pair strictly
decreases its g-sum, since its product increases by (x-z)^2/4.

On the compact seven-coordinate simplex, a minimizer therefore cannot
have unequal coordinates: the averaging operation is feasible even when
one coordinate is zero. Its unique minimum is seven coordinates L/7.
For L=0 this means the unique zero vector. Hence

    3(D-E)>=g(8-L)+7g(L/7)-256+48(8-L)
            =(48L/49)(7/2-L)(14-L)>=0.                       (7)

Here 14-L is strictly positive on the full interval. Equality in the
averaging bound forces all seven coordinates equal. Equality in (7)
then forces L=0 or L=7/2, giving respectively the spike or midpoint.
Since E=d^2 in this region, the two regions prove (1), its full equality
set, and the sharpness witness. No ordinary convexity of g is used.

### Independent direct proof and sharp maximum-conditioned remainder

There is a second analytic route that needs no fourteen-profile reduction.
On the same normalized domain one has the exact identity

    3(D-U)=sum_j(4-y_j)(y_j-1)^2.                           (7a)

If M<=4, every summand is nonnegative. Equality forces every coordinate
to be1 or4; a4 together with seven coordinates at least1 would have
sum at least11, so equality is precisely uniform. This also gives

    D-U>=(4-M)U/3                           (M<=4).         (7b)

If M>4, the maximal coordinate is unique and the other seven have sum
L=8-M<4. Their pair sums are strictly below4, so the same compact
strict-averaging argument used above gives the unique g-minimizer with
all seven coordinates equal L/7. The following exact identity is useful
on the part4<M<=9/2, where U is the nearer squared distance:

    g(M)+7g((8-M)/7)-40
         =(48/49)(M-1)^2(9/2-M).                           (7c)

Combining it with (7) on the other part proves the refined bound

    D-d^2 >= R(M),                                          (7d)

where

    R(M)=(16/49)(M-1)^2(9/2-M),          4<M<=9/2,
    R(M)=(16/49)(8-M)(M-9/2)(M+6),       9/2<=M<=8.

These two maximum-conditioned remainder bounds are sharp at *each*
allowed M: the vector(M,((8-M)/7)^7) attains them. Equality in either
bound has exactly this tail-equal shape, by strict averaging. R is
positive except at M9/2 and8. Equations(7a)-(7d) independently prove
(1) and its entire equality set. The stronger statement(7d), not just
a new proof of the same inequality, can pay explicitly for phase loss
away from those two maxima. No sharpness of the separate estimate(7b)
is asserted. Weighted versions follow from the exact scaling in(9).

## 4. Homogeneous and unsaturated-budget forms

For arbitrary y>=0 with mass sigma=sum y>0, define the finite set

    T_sigma={ (sigma/8) ones } union { sigma e_i :1<=i<=8 },
    d_sigma(y)^2=dist(y,T_sigma)^2
                 =min(p_2-sigma^2/8,p_2+sigma^2-2sigma M).

Applying (1) to w=8y/sigma gives the homogeneous sharp inequality

    (sigma/4)e_2(y)-e_3(y)>=(sigma/8)d_sigma(y)^2.             (8)

Equality holds exactly at the sigma/8-scaled versions of the three
orbits in Section1. This is a rescaling of (1), not a separate novelty
claim. At sigma=0 the vector is zero and both sides are zero.

The following useful weighted form retains the missing-mass term.
Let a>0 and 0<sigma<=8a. Put t=sigma/(8a), w=y/(at), and

    D_a(y)=2a e_2(y)-e_3(y).

The exact identity

    D_a(y)=a^3 t^2 D(w)+a^3 t^2(1-t)e_3(w)                  (9)

and d_sigma(y)^2=a^2 t^2 d(w)^2 imply

    D_a(y)>=a d_sigma(y)^2 + ((8a-sigma)/sigma)e_3(y).       (10)

For sigma=0 define the correction term to be zero; y=0 proves (10).
The coefficient a is sharp, and equality in the full (10) occurs at
every positive mass exactly on the three scaled orbits. If the second
nonnegative term is dropped, equality occurs at spikes for any mass,
or at mass8a on any of the three orbits. Indeed e_3(w) is positive on
uniform and midpoint and vanishes on spikes. This also describes the
zero set of D_a: spikes of any allowed mass and uniform at mass8a.

For a direct quantitative use of the remainders, define Xi(w) on the
normalized domain by (4-M)U(w)/3 when M<=4, and R(M) when M>4.
Equations(7a)-(7d) prove D(w)>=d(w)^2+Xi(w), with Xi>=0. Thus (9)
also gives the stronger weighted estimate

    D_a(y)>=a d_sigma(y)^2+((8a-sigma)/sigma)e_3(y)
                                      +a^3 t^2 Xi(w).       (10a)

At sigma=0 define the extra term as zero. For each fixed normalized
maximum M>4 and positive allowed mass this full bound is sharp exactly
at the scaled tail-equal vector, by the strict-averaging equality in(7d).

## 5. Labeled application: global real origin stability

This section inherits only the radial part of published author lemma8656,
[radial proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/radial-defect-annulus/PROOF.md),
source de423eaba9288fcbcfa79a86bbf15f2fcded183a,
graph bafkreiasy3xkvn4kiqqbbjkjngd2aba7d6iwrtkspv67y3jry3ztb446hi.
That radial part is independently unreviewed at the recorded pass-start
graph refresh8924. Its mean/phase premises for an annulus are NOT
premises here. Its explicit theorem, whose normalization was reread, is

    (1+a)^8[O_a(r)-product r]>=8(1-a^9)+5D_a(y),
    O_a(r)=9 integral_0^1 product_j(1-at r_j)dt,
    y=(1+a)r-1, 0<=a<=1, r_j>=1/(1+a), sum r<=8.           (11)

Let 0<a<=1, ell=1/(1+a), rho=sum r, and sigma=(1+a)rho-8>=0.
Then sigma<=8a. The image of T_sigma under y->ell(1+y) is

    R_(a,rho)={ (rho/8) ones }
              union permutations(ell(1+sigma),ell^7).

Write h_(a,rho)(r)^2=dist(r,R_(a,rho))^2. Affine scaling gives
d_sigma(y)^2=(1+a)^2 h_(a,rho)(r)^2. Set

    B_a(r)=8(1-a^9)+5a(1+a)^2 h_(a,rho)(r)^2
                         +5((8a-sigma)/sigma)e_3(y),         (12)

with the last term defined as zero at sigma=0. Combining (10)-(11)
proves throughout the full unsaturated real budget domain

    O_a(r)-product r>=B_a(r)/(1+a)^8.                        (13)

All terms in B_a are nonnegative; the first is positive for a<1.
Since product r<= (rho/8)^8<=1 and all radii are positive, the same
right-hand side is a lower bound for O_a(r)/product r-1.

The sharp maximum-conditioned remainder gives an explicit further
improvement: when sigma>0, take t=sigma/(8a), w=y/(at), and put

    B_a^+(r)=B_a(r)+5a^3 t^2 Xi(w).                         (13a)

At sigma=0 take B_a^+=B_a. By(10a)-(11), B_a^+ can replace B_a
in(13) and in the phase criterion(18) below. This pays additionally for
phase loss away from the midpoint and spike maxima when M(w)>4.
It remains bounded by the original defect-based allowance of8656.

For the important normalized plane rho=8, sigma=8a and the correction
term vanishes. With

    R_a={ones} union permutations(8-7/(1+a),1/(1+a)^7),
    h_a(r)^2=dist(r,R_a)^2,

we obtain

    O_a(r)/product r-1
       >=8(1-a^9)/(1+a)^8 +[5a/(1+a)^6]h_a(r)^2.            (14)

In particular, at a=1 and r>=1/2,sum r=8,

    Phi(r)=9 integral_0^1 product_j(r_j^(-1)-t)dt,
    Phi(r)>=1+(5/64) min(||r-ones||^2,
                        min_i||r-(1/2 ones+4e_i)||^2).       (15)

This covers the entire normalized real polytope, including beyond the
sharp pair-kernel ceiling in8887. The coefficient5/64 in (15) is NOT
claimed sharp: it inherits the sufficient coefficient5 in (11) and
the loss product r<=1. It is distinct from the sharp coefficient1 of
the moment theorem. Equality Phi=1 on this normalized real domain is
exactly the two indicated families: (15) forces them, and direct
integration verifies both. At uniform Phi=1. At (9/2,1/2^7),

    Phi=9 integral_0^1(2/9-t)(2-t)^7dt=1.                   (16)

The known polynomial(z-1)(z+1)^8 realizes the coalesced family and has
||r-ones||^2=14. Thus no positive global coefficient for that one
distance alone can hold. The equality family and qualitative Phi>=1
are prior work; the quantitative distance consequence is the application
proved here, with (11) explicitly inherited.

## 6. Labeled application: geometric complex phase allowance

For 0<a<1 and arbitrary complex q with r=|q|>=1/(1+a), sum r<=8,
put epsilon=sum|q_j-r_j|. The quadratic phase estimate proved as a
refinement in independently authored review7244 gives

    Re O_a(q)>=O_a(r)-K epsilon^2,
    K=570801247/1647086<350.                                 (17)

Its complete [audit and quadratic refinement](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_review3/README.md)
is source18c89c2ca1ffbbfc173867ddace5b1c82c5e7d6d,
graph bafkreibdsmdxcby5ie76hbjc2j5bq2xip3vkkuimwcvkvmlcxrbjrkxte4.
The full Taylor statement and radius/budget hypotheses were reread;
this section invokes it as a premise, not as a new derivative theorem.
Equations(13),(17) imply the sufficient geometric criterion

    epsilon^2<= B_a(r)/[350(1+a)^8]
       => Re O_a(q)>product r.                              (18)

Strictness follows from B_a(r)>0 for a<1 and K<350. The condition is
not asserted for every disk-rooted polynomial and its coefficient is
not asserted sharp. It is a weaker, geometrically explicit replacement
for8656's defect-based allowance, not a claim of enlarging that criterion.

For an actual degree-nine disk-rooted polynomial, rotate a simple marked
root to a in(0,1) and take q_j=(a-zeta_j)^(-1), counted with critical
multiplicity. A zero denominator means infinity and already proves the
reciprocal sum assertion. In a finite hypothetical failure sum|q|<=8,
Gauss--Lucas gives the radius floor, and the classical first origin
identity gives |O_a(q)|<=product r. Thus such a hypothetical failure
must violate (18) strictly. The communication identity is credited to
[Zhang, Lemma3.1](https://arxiv.org/html/2609.19126) and
[Tao's primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/).
No phase bound for every polynomial, larger effective annulus or full
first-power theorem follows from the moment inequality alone.

## 7. Evidence and trust boundary

The standalone [checker](verify.py) uses only CPython3.10+ stdlib exact
integers and Fractions. It checks complete polynomial identities, all14
profiles and signs, normalization and sharp/equality controls. The cubic
pair identity is reconstructed from two-variable powers; Newton's
identity is independently reconstructed from elementary products after
eliminating the eighth coordinate, and compared with the moment route.
It fully compares the regenerated [small record](expected.json), not
only aggregate counts or a digest. Mathematical and fixture damages
exercise sign, identity and completeness failures. Normal and optimized
runs are specified in [README.md](README.md).

These checks do not formalize compactness, stationarity, the equality
transfer, strict averaging, metric scaling or the inherited radial and
Taylor bounds. Those are ordinary written mathematics. No floating point,
solver, empirical root list, imported campaign checker, large omitted
computation or proof-assistant kernel is used. The proof of (1)-(10)
needs no campaign theorem; (11)-(16) inherit8656 and (17)-(18)
additionally inherit7244. Author checks are not independent review.
