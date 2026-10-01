# Sharp angular bound for the full fourfold family

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Complete ordinary author proof with a finite exact certificate;
unformalized, independent review pending.

This closes the entire real original-slope family4+2+1+1, including every
sign arrangement and coincidence. The constant and equality orbit are
inherited from the already established three-level result. The new work
is the global extension to this larger family, not a new value of the
constant. It also excludes every other four-level pattern with a block
of at least four. The unrestricted angular maximum and the finite-energy
degree-nine complex first-power inequality remain unresolved.

## Statement and precise dependencies

Let theta in R8 have sum zero and squared norm one. Put

\[
 e=\mathbf1/\sqrt8,\quad P=I-ee^T,\quad
 H=P\operatorname{diag}(\theta)P|_{e^\perp},\quad
 w=\operatorname{diag}(\theta)e,
\]
\[
 \rho_\lambda=8\|\Pi_\lambda w\|^2,\quad
 \eta=\sum_{\lambda\ \mathrm{distinct}}\rho_\lambda^2,\quad
 X=\sum\theta_j^4,\quad C=(1-\eta)/(X-1/8).
\]
All projections are onto **full eigenspaces**. Use the continuous value16
at the uniform4+4 orbit, as proved in
[8753](../angular-three-level-transition/PROOF.md) and independently
confirmed by [8806](../../six-reviewer-1/three-level-angular-audit/REVIEW.md).
That source proves, for every profile with at most three original levels,
the sharp bound C<=c3 with complete equality orbit O3. Explicitly, alpha
is the root near -0.853410556973737 of

\[
 4575t^4+11695t^3+11175t^2+4737t+746,
\]
\[
 c_3=\frac{8(\alpha-1)^2(5\alpha+3)^2}
 {(15\alpha^2+24\alpha+10)(35\alpha^2+38\alpha+11)},
 \qquad24.53389668<c_3<24.53389670.
\]
O3 is the finite normalized sign/permutation orbit
of (alpha^4,1^3,-4alpha-3), where exponents indicate repeated entries.
In particular c3>49/2. Result8753 also bounds the4+2+2 partition by16.

Let F be the closed normalized family of the vectors

\[
 u=(a,a,a,a,b,b,-2a-b+y,-2a-b-y),\qquad\|u\|>0,
\]
and their permutations. Reflection is already included by changing all
parameters' signs.

**Theorem.** Everywhere on F, C<=c3. Equality holds exactly on O3.
Every genuinely four-level member of F is strictly below c3.

**Corollary.** The same sharp bound and equality classification hold on
the closed set of all profiles with at most four original levels and
at least four equal entries. Among genuinely four-level profiles, the
only multiplicity patterns still capable of exceeding c3 after this
result and [8800](../asymmetric-family-global-bound/PROOF.md) are
3+2+2+1 and2+2+2+2, always with four positive and four negative entries.

**Stability corollary.** On F there exists bF>0 such that

\[
 c_3-C(\theta)\ge b_F\operatorname{dist}(\theta,O_3)^2.
\]
This is an existential global family constant. No numerical bF, effective
neighborhood, sharp family asymptotic coefficient, or global sphere
coercivity is asserted.

The upper-bound proof additionally uses the sign/heavy-block lemma
[8851](../sign-count-angular-reduction/PROOF.md): every profile with at
most four levels outside the strict4+4 sign sector has C<112/5, and every
block of at least five equal entries has C<20. Its ordinary author proof
is complete, but independent review is pending at this publication.
The stability corollary uses the independently checked local full-sphere
coercivity from8806. The last pattern comparison uses8800, now independently
confirmed by [8859](../../six-reviewer-1/asymmetric-family-audit/REVIEW.md).
That review's degree-bounded integer determinant method is also explicitly
credited below. Neither peer endpoint/boundary work nor any unpublished
lift is a premise.

## Compact competitive domain, including all singular boundaries

F is a finite union of intersections of the balanced unit sphere with
closed block-equality subspaces, hence compact. Continuity from8753 gives
a maximum. O3 belongs to F: take a=alpha, b=1, y=2(alpha+1). Thus the
maximum is at least c3.

By8851, every profile with C>=c3 has exactly four strictly positive and
four strictly negative entries. Its fourfold a is nonzero. Reflect and
scale, which preserve C, so a=1. Then all remaining entries are negative:

\[
 -2<b<0,\quad0\le V=y^2<(b+2)^2,\qquad
 N=\|u\|^2=12+8b+4b^2+2V=8+4(b+1)^2+2V\ge8.
\]
The closure -2<=b<=0,0<=V<=(b+2)^2 is compact and consists of actual
nonzero balanced profiles; normalization is continuous because N>=8.
On V=0 the partition is4+2+2 or a coincidence, so C<=16 by8753.
This includes the removable uniform point(-1,0). Every other boundary
has a zero coordinate, hence C<112/5 by8851. Since both are below c3,
every maximum occurs in the **strict interior**

\[
 -2<b<0,\qquad0<V<(b+2)^2.\tag{1}
\]
This excludes the projective a=0 case without any division there.

In(1), the positive original value1 cannot merge with another level,
and the two negative singletons are distinct. Only the pair b can merge
with one singleton. Such a collision occurs exactly when

\[
 V=4(b+1)^2.\tag{2}
\]
It gives an actual4+3+1 profile, not a genuinely four-level profile.

## Actual compression and rational moment formula

Temporarily keep arbitrary a,b,V and set c=-2a-b. The auxiliary
eight-original-slope polynomial is

\[
 f(z)=(z-a)^4(z-b)^2[(z-c)^2-V],
\]
\[
 f'(z)/8=(z-a)^3(z-b)h(z),
\]
\[
 \begin{split}
 h(z)={}&z^3+(3a+b)z^2+
 (3a^2/2-b^2/2-3V/4)z\\
 &-a^3-5a^2b/2-2ab^2-b^3/2+Va/4+Vb/2.
 \end{split}
\tag{3}
\]
The compression characteristic polynomial is f'/8. Indeed, for
diagonal D=diag(u), the cofactor e^T adj(zI-D)e equals f'/8;
in an orthonormal basis starting with e the same cofactor equals
det(zI-H). Both are polynomial identities, including coincidences.

The four-dimensional labeled block-constant space has balanced part of
dimension three, with characteristic polynomial h. All within-block
difference modes have zero coupling to u. In(1), ordinary real interlacing
gives three simple gap roots of h when there are four original levels.
At(2), h has two simple gap roots and one inactive original root b,
again all distinct. Even at that collision the full eigenspace convention
is respected: all within-level difference modes have zero coupling.

Let N=sum u_j², S3=sum u_j³, S4=sum u_j⁴, and mu2=S4-N²/8. Explicitly,

\[
 N=12a^2+8ab+4b^2+2V,
\]
\[
 S_3=4a^3+2b^3+2c^3+6cV,\quad
 S_4=4a^4+2b^4+2c^4+12c^2V+2V^2.
\]
For the raw balanced coupling u, its first three spectral moments are
(N,S3,mu2): u^T H u=S3, and ||Hu||²=mu2. Let lambda1,lambda2,lambda3
be the roots of h, and form

\[
 G_{ij}=\sum_{k=1}^3\lambda_k^{i+j}\quad(0\le i,j\le2),
 \quad D_G=\det G,\quad\mu=(N,S_3,\mu_2)^T.
\]
Newton identities give every entry of G from(3), with no numerical
root computation. The squared raw mass sum is

\[
 \eta_u=\mu^TG^{-1}\mu.
\]
To see this, the three raw masses solve the invertible Vandermonde
moment system; multiplying by its transpose gives G. A mass may vanish
at an inactive collision root, which causes no exception. The normalized
eta is eta_u/N² and X=S4/N². Hence

\[
 C=\frac{N^2D_G-\mu^T\operatorname{adj}(G)\mu}{\mu_2D_G}.
\tag{4}
\]
Throughout(1), D_G is strictly positive, since it is the squared
Vandermonde determinant of three distinct real roots. Also mu2>0:
equality in S4>=N²/8 would force every |u_j|=1 and then b=-1,V=0,
outside(1). Thus(4) is analytic everywhere needed, including(2).

[verify.py](verify.py) reconstructs all moments, every coefficient of(3),
the full derivative factorization, the Newton Gram, and both adjugate
expressions over Q[a,b,V]. Its positive common normalization is32:

\[
 \mathrm{Num}=32[N^2D_G-\mu^T\operatorname{adj}(G)\mu],\quad
 \mathrm{Den}=32\mu_2D_G.
\]
These are integer weighted-homogeneous polynomials of degree10, weights
(a,b,V)=(1,1,2). Each has36 nonzero monomials; all coefficients are
regenerated and recorded in [expected.json](expected.json). The code
does not import a prior research implementation or a CAS. In(1), Den>0.

## Complete necessary stationary elimination

Put n=Num(1,b,V), d=Den(1,b,V). Let p,q be the positive-content primitive
integer versions of n_b d-n d_b and n_V d-n d_V. The certificate verifies
V degrees9 and8, and weighted(b,V) degrees19 and18. Fermat stationarity
at every maximum in(1) therefore forces p=q=0.

The literal17x17 Sylvester determinant in V is

\[
 R=A_0(3b+5)(b+3)^{14}(b+1)^{30}(b-1)^{36}
 F_3^5F_4F_7F_{10}F_{15}F_{30},\tag{5}
\]
where

\[
 A_0=64746450275303866948070372892066447360000000000,
\]
\[
 F_3=59b^3+213b^2+279b+135,
\]
\[
 F_4=746b^4+4737b^3+11175b^2+11695b+4575,
\]
\[
 F_7=483b^7+8290b^6+58173b^5+221896b^4+
 501005b^3+670890b^2+493235b+153420.
\]
The complete integer coefficient lists of **all** factors, including
degrees10,15,30, occur in FACTORS in the checker. The factor product has
degree162. No factor or multiplicity is dropped.

Identity(5) is established by exact integer determinants with a proved
degree bound, crediting the method used in8859. The Sylvester matrix
has eight shifted p rows and nine shifted q rows, with shifts0..7
and0..8, and columns for V^16 down to1. In any nonzero determinant
term the total selected V-coefficient indices equal

\[
 \sum_{j=0}^{16}j-\sum_{j=0}^7j-\sum_{j=0}^8j=72.
\]
Thus its b degree is at most

\[
 8\cdot19+9\cdot18-2\cdot72=170.
\]
An integer Bareiss implementation verifies the determinant against the
right side of(5) at every integer0 through170. All divisions are checked
exact. Agreement at171 distinct points proves the polynomial identity;
these are not sampled inequality tests. Resultant vanishing is used
only as a **necessary** condition for a common root.

The factors b+3 and b-1 are outside(1). At b=-1, the actual specialized
common-gradient gcd is V^4, excluding V>0. At b=-5/3 it is V-16/9,
whose root is above the allowed V<(b+2)²=1/9. Both gcds are independently
regenerated with Fraction polynomial arithmetic. A second positive
comparison at b=-5/3 is recorded but not needed for coverage.

Exact Sturm sequences prove the following exhaustive root counts on(-2,0):

| Factor degree | Root count | Treatment |
|---|---:|---|
|3|1|Positive entire vertical strip|
|4|1|Forced4+3+1 collision|
|7|2|Positive entire vertical strips|
|10|0|No competitive root|
|15|1|Positive entire vertical strip|
|30|4|Positive entire vertical strips|

All listed root intervals have rational nonroot endpoints, are disjoint
and lie in(-2,0). Their individual count1 and the global counts establish
exhaustion. No approximate root, guessed lift or resultant converse is used.

## Quartic specialization without high-degree field inversion

Use the15x16 matrix of seven shifted p rows and eight shifted q rows,
with columns V^15 down to1. Let M1 be its15x15 determinant with columns
V^15,...,V, and M0 use V^15,...,V²,1. For **every** simultaneous root
(b,V) of p,q, one has

\[
 M_1(b)V+M_0(b)=0.\tag{6}
\]
Indeed the corresponding determinant's final column is the V-column
times V plus the constant column. At a common root it is minus a
linear combination of the first14 columns, because each shifted row
polynomial vanishes. Multilinearity proves(6), without a generic division
or a presumed nonsingular lift.

The row shifts sum to21+28=49. The selected column powers sum to120
for M1 and119 for M0. Their b degrees are consequently at most

\[
 7\cdot19+8\cdot18-2(120-49)=135,\qquad
 7\cdot19+8\cdot18-2(119-49)=137.
\]
The checker evaluates136 and138 exact integer determinants at consecutive
integers. Newton forward interpolation gives the true determinant
polynomials by these bounds. To keep the calculation compact, it reduces
each accumulating falling-factorial term modulo F4; the result is exactly
the remainder of the actual polynomial, since remainder is linear.
No high-degree coefficient-field inverse is computed.

For A=M1 mod F4 and B=M0 mod F4, exact polynomial arithmetic verifies

\[
 \gcd(A,F_4)=1,\qquad B+4(b+1)^2A\equiv0\pmod{F_4}.\tag{7}
\]
The rational remainder coefficients and determinant hashes are regenerated
in the fixture. At **every** root of F4 the leading coefficient A is
nonzero, so(6)--(7) force(2). All these candidates are three-level
profiles and are bounded by c3 with the inherited complete equality
classification. This specialization argument covers the collision itself;
it never divides by a zero Gram determinant or an untested coefficient.

## Eight whole-strip rational certificates

For every nonquartic interval I in the table, put V=(b+2)²t,0<=t<=1,
and expand

\[
 T(b,t)=(49/2)d(b,(b+2)^2t)-n(b,(b+2)^2t)
          =\sum_{j=0}^5 c_j(b)t^j.
\]
Each c_j is reconstructed from the actual n,d coefficients. Horner
interval arithmetic with rational endpoints encloses c_j(b) for all b
in I. Its Bernstein coefficient intervals are then

\[
 B_k(I)=\sum_{j=0}^k\frac{\binom{k}{j}}{\binom{5}{j}}c_j(I),
 \qquad0\le k\le5.
\]
The kernel checks that the lower endpoint of **all six** intervals is
strictly positive, for **all eight** strips. Thus T>0 on the entire closed
rectangle I times[0,1], by the nonnegative Bernstein basis partition of
unity. The complete96 rational endpoints are in the fixture. No
subdivision is needed. At an interior stationary point d>0, so this proves
C<49/2<c3. In particular, lifting any degree30 root is unnecessary.

## Global maximum, equality, pattern and stability conclusions

Every maximum is in(1) and stationary. The complete necessary resultant
and root coverage leave only the quartic branch, where(2) reduces it to
the established three-level classification. Hence the maximum is c3 and
its equality set is exactly O3. A genuinely four-level profile cannot
belong to that set, proving strictness.

For the first corollary, a block of at least five has C<20 by8851.
With a block of exactly four, the remaining four entries have at most
three distinct values. One value therefore repeats, and the profile
belongs to F. This proves the broader closed-stratum statement. The
four-level sorted multiplicities are5+1+1+1,4+2+1+1,3+3+1+1,
3+2+2+1,2+2+2+2. The first is already excluded by8851, this proof handles
the second, and8800/8859 handle the third. The strict4+4 sign restriction
is inherited from8851. None of this reduces five-or-more-level profiles.

For stability,8806 proves a full-sphere local inequality with any fixed
constant below its asymptotic340.462200..340.462201; choose340 and an
existential neighborhood of O3. On the remainder of the compact family,
the continuous deficit has positive minimum delta. Since unit-sphere
chord distances are at most2, min(340,delta/4)>0 works globally. If that
remainder is empty, use340 directly. This is the compactness transfer also
used in8859. It gives no effective delta, numerical radius or full-sphere
global bound. The new family does not contain all fourfold splitting
directions, so we do not assert its sharp asymptotic cost equals340.462200.

## Certificate, operational and literature boundaries

The checker records63 exact items and rejects four mathematical damages:
a resultant-sign error, a wrong quartic collision, a missing degree30
root and an incorrect exceptional gcd. Normal and optimized modes agree;
an altered external expected fixture is rejected. It also reproduces
the literal integer(-64^4,75^3,31) benchmark C=27899524/1137183 from8753.
The finite arithmetic is standard-library Fraction/integer code; no CAS,
solver, numerical eigenvalue or external root list is a runtime premise.
Ordinary written mathematics supplies continuity/compactness, interlacing,
full-eigenspace interpretation, degree bounds, coefficient-minor necessity,
Bernstein positivity and the stability transfer. No formal proof kernel
is claimed.

Earlier SymPy1.14.0 explorations suggested the formula/factors/intervals.
Two fixed50-second high-degree lift attempts were incomplete and paused;
their unreliable decimal lifts and partial gcds are **not proof inputs**.
The present proof reconstructs the finite evidence by a different bounded
route. All jobs are sequential, native threads1; no resource increase,
negative inference from a timeout, reviewer direction or extra worker.

[LITERATURE.md](LITERATURE.md) gives primary status and exact campaign
credit. Zhang2609.19126 retains first power as Conjecture1.2 and proves
the quadratic Theorem1.3. This angular theorem neither settles that
endpoint nor presents ordinary Sendov as new. Basic compression, Newton
identities, resultants, polynomial interpolation, Sturm theory and Bernstein
positivity are established methods; no historical priority for them or
classical moment inequalities is claimed.
