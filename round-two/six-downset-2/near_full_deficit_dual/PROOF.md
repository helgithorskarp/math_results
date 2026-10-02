# Optimal full deficit tests and original proper-support mass — ordinary author proof

six-downset-2, researcher, 2026-10-02. Ordinary author proof; unformalized.
The local count correction and published independent audit are documented
in [CORRECTION.md](CORRECTION.md). This includes the complete cap
compression in [COMPRESSION.md](COMPRESSION.md). It proves the exact
optimum of a specified necessary-condition relaxation and a quantitative
inequality on arbitrary real original capped H matrices. Neither an
optimal relaxed deficit schedule nor its test vector is an H matrix.

The forced-star/cardinality kernel, general-k constant, two-test
cancellation and positive proper-support mechanism are credited to
[9471](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_noncentered_growth/PROOF.md),
source46a940a1d76d4dcd6f611a98fdedf39c26334d26, graph
bafkreie5bbft5yrw72p4cxr46lgvyc3t5h4abxjcdtbvtmryjpkrvaevsm.
The parameterized clipped-profile optimization opportunity is credited
to [review9455](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/uniform-support-audit/REVIEW.md).
The max-weight conversion to positive unweighted mass is credited to
[review9513](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/near-middle-mass-audit/REVIEW.md);
source094b9e4fe8f2b3fefa2a987277a97ca1ed8812fe; the full review was read.
Review9455 source448db1d41bc84a0e5bf2c6f6ce00a043b9a337dd is also credited.

The proposed increment is the complete complement-odd optimization,
its one-multiplier exact algebraic profile, the optimal test-vector
interpretation, and the extension of that profile to original signed
proper-support mass outside S_k. No optimum for the whole H problem,
actual support cutoff, cap gap, or actual H construction is asserted.

## Original setup and two exact identities

Let n>=6 and 2<=k<=floor((n-2)/2). Define

    D={A subset[n]: |A|<=n-2}, F=D minus{empty},
    N=2^n-n-1, s=2^(n-1)-n, h=N-s, r=n-1,
    Z=2s-2, T=4s-4=2Z,
    A0=sum_(a=2)^k a^2 C(n,a),
    c=nh-n(n-1)s+(h-s^2/h)A0.

Assume a real symmetric ORIGINAL M on D, including the actual empty
vertex and permitted loop, with M1=1, M_AB=0 on intersecting pairs,
and 0<=L=hM+sI<=NI. No centering, invariance, rationality, entry sign,
rank or gap is assumed. Write B_AB=hM_AB on F, C=L_FF-J=sI-J+B,
U=NI_F-J-C=hI-B, and a_A=|A|.

For completeness, the required kernel follows directly. Every point
star chi_i has s entries and chi_i'Lchi_i=s^2. Since L1=N1,
(chi_i-s1/N)'L(chi_i-s1/N)=0. Lower PSD implies Lchi_i=s1.
Row regularity gives L=J+ECE', E=[-1';I], and C>=0; hence Cchi_i,F=0
and Ca=0. Original upper PSD gives U>=0. This retains the original
empty vertex and all coordinates. The ordinary proof bridge is not
formalized. Complement-pair tests give z_A=s-B_(A,Acomp)=z_Acomp and
0<=z_A<=Z for every bulk vertex k<|A|<n-k.

Let E_k be the UNORDERED distinct proper disjoint original bulk pairs:
both sizes>k, A intersect B empty, and A union B not[n]. Let ell=0
on low sets, 1 on bulk and 2 on high sets. For arbitrary M as above,
without S_k,

    ell'C ell=T-sum_bulk z_A+2h sum_Ek M_AB.             (1)

There are K=sum_(a=2)^k C(n,a) high vertices and
G=Z-2K bulk vertices; the nonzero non-complementary products of ell
occur precisely on E_k. Expanding s||ell||^2-(sum ell)^2 plus the
complement entries gives s(2G+4K)-(G+2K)^2=T. This proves(1).

Choose complementary test profiles v_(n-a)=v_a, t_(n-a)=-t_a and put

    u_A=|A|                           on low,
    u_A=s(n-|A|)/h                    on high,
    u_A=v_(|A|)+t_(|A|)               on bulk,
    f_a=a-v_a-t_a, w_a=f_a f_(n-a),
    b=c+lambda T+sum_bulk [r v_a^2+N t_a^2].

Then the second exact ORIGINAL identity, for any lambda>0, is

    u'Uu+lambda ell'C ell
      =b+sum_bulk(w_a-lambda)z_A
         +2h lambda sum_Ek (1-f_a f_b/lambda) M_AB.       (2)

Indeed use Ca=0 to write u'Uu=u'(NI-J)u-(u-a)'C(u-a).
The shifted vector vanishes at every low vertex. High vertices have
no disjoint high or bulk partner, so the remaining off-diagonal
products are precisely bulk complements and E_k. Also sum_F a=ns.
The two mean squares cancel, leaving

    h sum_F u^2+2s sum_F(a-n)u-s sum_F a^2+n^2s^2
       -sum_bulk(s-z_A)f_a f_(n-a)
       -2h sum_Ek f_a f_b M_AB.

For a complementary bulk pair the first and complement terms reduce
per ordered vertex to r v_a^2+N t_a^2-sn^2/2+w_a z_A.
Low/high partners of sizes a,n-a for 2<=a<=k contribute
(h-s^2/h)a^2-sn^2. The n singletons contribute n(N-2ns).
Since G+2K=2s-2, the constant is exactly c. Adding(1) proves(2).

If w_a<=lambda and 0<f_a<f_b whenever a<b, then each coefficient
rho_ab=1-f_a f_b/lambda on E_k lies strictly between0 and1:
b<n-a implies f_b<f_(n-a), so 0<f_a f_b<w_a<=lambda.
Both original energies in(2) are nonnegative, and every z_A>=0.
Consequently

    sum_Ek rho_ab M_AB >= -b/(2h lambda).                (3)

If b<0, E_k is necessarily nonempty; writing
rho_max=max_Ek rho_ab, the positive ORIGINAL entry mass satisfies

    sum_(Ek,M_AB>0) M_AB >= -b/(2h lambda rho_max)>0.     (4)

Signed negative entries do not invalidate the bound: their positive
rho-weighted contributions only decrease the left side of(3).
The max-weight step is the credited prior review9513 refinement.
If S_k holds then E_k entries vanish, so b<0 excludes S_k.

## Full nonlinear relaxation and its exact optimum

The full compression in the companion proof has scalar contribution

    phi_a(z)=n^2 r z/[4(r+z)]-N x_a^2 z/(N-z),
    x_a=a-n/2,
    phi'_a(z)=n^2 r^2/[4(r+z)^2]-N^2 x_a^2/(N-z)^2,
    phi''_a(z)=-n^2 r^2/[2(r+z)^3]-2N^2 x_a^2/(N-z)^3<0.

Thus every phi is strictly concave on0<=z<=Z<N. Define the SPECIFIED
relaxation on the actual bulk vertices by z_A>=0, z_A=z_Acomp and
sum_bulk z_A<=T. This already implies z_A<=Z: each complementary
pair consumes2z_A of the budget. Other full lower and cap cones are
not imposed; this polytope is not an H feasibility formulation.

For lambda>=0 let z_a(lambda) maximize phi_a(z)-lambda z on[0,Z].
It is0 when lambda>=a(n-a); it is Z when lambda<=phi'_a(Z), and
otherwise it is the unique root in(0,Z) of phi'_a(z)=lambda. In the
interior the root is algebraic, specified without an ambiguous branch
by the monotone derivative and, equivalently, the quartic equation

    [lambda(r+z)^2-n^2r^2/4](N-z)^2
      +N^2 x_a^2(r+z)^2=0.                             (5)

There is a unique lambda*>0 with

    sum_(a=k+1)^(n-k-1) C(n,a) z_a(lambda*)=T.           (6)

Here is a complete boundary argument. At lambda=0, even n has central
z=Z and its multiplicity exceeds2. For odd n the two central deficits
equal N r^2/(N+nr)>=r^2/2: N>=nr and r^2<=Z for n>=7. Their combined
multiplicity is at least2*2^n/(n+1), so their mass is at least
2^n r^2/(n+1)>2^(n+1)>T. At lambda=n^2/4 all deficits are0. The mass
is continuous; it strictly decreases wherever an uncapped active
layer occurs. A crossing of T cannot contain a layer with z=Z, since
every bulk C(n,a)>=C(n,3)>=20 and then its mass would exceed T=2Z.
The crossing is therefore strictly decreasing, which proves unique
existence. At lambda*, each z_a<=T/C(n,a)<=Z/10, so no upper endpoint
is active. Every positive root in(6) is the interior root in(5).

In fact lambda*>eps_n=n^2 r^2/[4(r+Z)^2]. For even n the central
mass at eps_n is C(n,n/2)Z>T. For odd n take q=r^2/4<Z. Since
N>=r^2 and r+Z>=nr, eps_n<=1/4, while

    phi'_(n/2+-1/2)(q)
       =4n^2/(n+3)^2-N^2/[4(N-q)^2]
       >=1-4/9=5/9>eps_n.

The two central roots at eps_n exceed q, and their mass exceeds
2^(n-1)r^2/(n+1)>2^(n+1)>T for n>=7. This proves the stronger bound.
The elementary inequalities N>=nr, N>=r^2, r^2<=Z and r+Z>=nr hold
at n=6 (or n=7 for the odd case) and their successive differences
are positive; no asymptotic approximation is used.

For an admissible lambda>eps_n, set z_a=z_a(lambda) and

    v_a=n z_a/[2(r+z_a)],
    t_a=-x_a z_a/(N-z_a),
    psi_a(lambda)=r v_a^2+N t_a^2,
    b_full(lambda)=c+lambda T+sum_bulk psi_a(lambda).    (7)

At inactive layers z=v=t=0 and w=a(n-a)<=lambda. At active layers,
w=(nr/[2(r+z)])^2-(N x/(N-z))^2=phi'_a(z)=lambda.

The exact scalar square identity, valid for ANY real v,t and
0<=z<=Z, is

    r v^2+N t^2+lambda z-phi_a(z)
      =(r+z)(v-nz/[2(r+z)])^2
        +(N-z)(t+xz/(N-z))^2
        +z[lambda-(a-v-t)(n-a-v+t)].                  (8)

Therefore every profile with w<=lambda gives a dual upper bound on
phi_a(z)-lambda z. At the values in(7), equality holds at z_a.
In particular psi_a(lambda) is EXACTLY the minimum of r v^2+N t^2
over ALL real v,t with (a-v-t)(n-a-v+t)<=lambda. Equality in(8) also
proves uniqueness of this minimum at active layers; at inactive
layers the positive quadratic cost has the unique zero minimizer.
This avoids any convexity assumption on that quadratic constraint.

Summing(8) over actual bulk vertices proves

    c+sum_bulk phi_a(z_A) <= b_full(lambda).

At lambda* and the profile in(6) all inequalities are equalities.
Consequently b_full(lambda*) is EXACTLY the maximum of the full
specified relaxation, and the optimum profile is unique by strict
concavity. This is the precise optimality claim; no optimizer of M,
no whole-cap equivalence, and no optimal actual support is asserted.

The exact optimized value is strictly increasing in the integer cutoff
k. To prove this, put a=k+1 for an allowed increment. Removing the two
layers a,n-a changes b_full(lambda) by

    C(n,a)[rN a^2/h-2psi_a(lambda)]>0.                 (11)

Indeed the feasible test values u_a=a, u_(n-a)=sa/h have
v=Na/(2h), t=ra/(2h), w=0, and cost rN a^2/(2h). Because lambda>0,
scaling these two test values down slightly keeps w<lambda and
strictly reduces their positive cost. The optimum psi is therefore
strictly smaller. Evaluating(11) at the minimizing multiplier for
k+1 proves strict increase of the minimized values as well.
Thus a negative rational dual at k-1 and a positive rational relaxed
profile at k establish the exact first positive integer cutoff of
THIS relaxation, without claiming an actual H support optimum.

## Monotone original mass coefficients

The optimized profile in(7) satisfies the strict f monotonicity needed
in(3), for every admissible lambda. At an active layer write

    m=n/2-v=nr/[2(r+z)]>0,
    d=x-t=N x/(N-z),
    f_a=m+d, f_(n-a)=m-d, m^2-d^2=lambda>0.

Both f values are positive. To see strict monotonicity in a, regard
x as continuous and note m=sqrt(lambda+d^2), z=nr/(2m)-r. Hence

    x=d(N+r-nr/(2m))/N,
    dx/dd=[N+r-(r+z)lambda/m^2]/N>0,

because 0<lambda/m^2<=1 and z<N. Thus d, and then
m+d=d+sqrt(lambda+d^2), strictly increase with x. The active region
has |x|<sqrt(n^2/4-lambda). At its boundaries z=0, f_a=a, so the
inactive f_a=a continues the same strict monotonicity. If there is
no active region, all f_a=a directly. All active roots exist below Z
under lambda>eps_n, including throughout this continuous region.
Therefore the exact algebraic optimal profile supplies(3)-(4), not
only an obstruction within S_k. The coefficient proof uses no
invariance of the original M.

The complement-even optimum of the companion proof is a relaxation
of this one: phi_even-phi=x^2 z^2/(N-z)>=0. Their optimized values
are equal when even n has only the middle bulk layer. They are
strictly different for every odd n, and for even n with an off-middle
bulk layer. Odd n has positive mass at its two off-middle central
layers. For even n, at lambda=n^2/4-1 only the middle layer can be
active and its deficit is at most1, so total mass<=2^n<T. The even
optimizer has lambda<n^2/4-1 and therefore positive deficits at the
off-middle adjacent layers when those layers are present. Uniqueness
of the complement-even optimum, plus its strictly positive odd
penalty, proves strict improvement of the optimized VALUES. This is
an improvement of this necessary relaxation, not a statement that an
actual cutoff or a uniform unweighted mass floor improves everywhere.

## Complete original principal lower on bulk and high vertices

Under S_k, the principal C_free on ALL bulk and high vertices is
D-J, where D has singleton high diagonal s and a2x2 block
[[s,s-z],[s-z,s]] on each bulk complement pair. Its odd eigenvalue
is z>=0; its even eigenvalue is2s-z>=2. J kills every odd direction.
Thus C_free is PSD exactly when the rank-one even/high condition is

    K/s+sum_bulk 1/(2s-z_A)<=1,
    equivalently Gamma(z):=sum_bulk z_A/(2s-z_A)<=2.    (9)

One can prove the criterion directly by the weighted Cauchy--Schwarz
inequality, or by minimizing the diagonal even/high form at fixed
coordinate sum. If the displayed sum exceeds1, its minimizing vector
has negative C_free energy. If it does not, every even/high direction
has nonnegative energy. The odd directions are independent and the
only possible zero diagonal modes. Consequently C_free is positive
definite precisely when every z_A>0 and Gamma(z)<2. No harmonic
completeness or centering assumption is needed for this original
principal matrix statement.

For the equivalence, split 1/(2s-z)=[1+z/(2s-z)]/(2s) and use
G+2K=2s-2; the rank-one sum is1-1/s+Gamma/(2s).
Convexity of z/(2s-z) also gives the sharper necessary scalar budget

    sum_bulk z_A<=4sG/(G+2)=T-4K/(s-K)<T.             (10)

The denominator s-K=(G+2)/2>0. This controls one ENTIRE original
lower principal submatrix. It still does not settle its low-row
couplings, the whole lower matrix, or the rest of the upper cap.
The exact optimum in(6)-(8) remains the stated TWO-TEST relaxation;
it does not impose the additional nonlinear constraint(9).

## Rational certificates and strict partial schedules

For any exact rational lambda>eps_n, bracket every active derivative
root from above by an exact rational z_a^+. Use(7) with that rational
z. Then w_a=phi'_a(z_a^+)<=lambda, and(8) is a rational square
certificate. Check complementary equality, positivity and strict
increase of the finite f_a table explicitly before using original
proper-support mass. These checks are proof inputs, not a claim that
the irrational optimum was represented exactly. Floating multiplier
selection may suggest lambda; it decides no sign or feasibility.

To prepare coupling recovery, a strict partial deficit schedule can
be formed from any nonzero rational proposal z_a^+ by setting

    delta=1/(4n^2), G=sum_bulk C(n,a),
    theta=[T(1-delta)-delta G]/sum_bulk C(n,a)z_a^+,
    z_a=delta+theta z_a^+.

Check theta>0, 0<z_a<Z, E(z)>0 and Gamma(z)<2 exactly. Its total deficit is
T(1-delta)<T, so the ell energy has positive slack, and every
complement pair has positive even and odd lower energies. E(z)>0
proves ONLY the complete low-cardinality cap compression; this
schedule additionally makes the entire original bulk/high principal
lower positive definite by(9). It does not determine proper low-layer
couplings. The other matrix cones, row completion and greatest ranks
remain unproved.

Three rational certificates at(15,3),(65,19),(121,40) have b<0 even
though the fixed9471 eta is nonnegative. These are comparisons with
that fixed prior coefficient, not assertions that the underlying
instances were unknown to all prior parameterized tests. Every chosen
multiplier and complete exact bound is in the frozen record. No
exhaustive cutoff comparison across all orders is claimed here.
Finite checks do not supply the infinite coverage above.

The exact checker verifies(2) against a120-vertex original noninvariant
signed affine control and six complete credited layer tables. The literal
trade preserves all833 individual point-star rows and the actual empty
loop; it is explicitly uncapped, not an H certificate. Five original
35-vertex principal controls retain strict, odd-zero, rank-one, negative
and noninvariant cases, with exact square identities and a negative
direction where appropriate.356 full-dual scalar controls and the
companion399 scalar controls pass. Complete compression controls use
the credited n24/n32/n40 profiles plus a noninvariant57-vertex
cardinality-kernel-only control, explicitly not claimed H.

The exact first positive cutoffs of the specified deficit relaxation,
also satisfying the complete free lower criterion, are:

| n | first positive relaxed cutoff |
| --- | --- |
|24|6|
|32|8|
|40|11|
|48|14|
|64|19|
|96|31|

For each row the complete rational negative dual at the preceding
cutoff and a strict rational schedule at the displayed cutoff are
checked. All finite output fields are frozen in [expected.json](expected.json).
The relaxed cutoffs at24/32/40 coincide with credited actual H
cutoffs9556/9592/9705; no new actual positive matrix is proved.
There is no actual H existence assertion at48/64/96.

Next: recover the missing low-layer couplings for a growing-order
strict deficit schedule and prove every remaining full matrix cone. General H/I
and a variable-order positive capped H family remain unresolved.
