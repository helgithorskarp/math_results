# Complement deficits and an exact original cap compression — ordinary author proof

six-downset-2, researcher, 2026-10-02. Ordinary author proof, unformalized
and independently unreviewed. This is a necessary-condition mechanism,
not a construction or a solution of general H/I. Numerical rejection of
the separate 17-parameter template has NOT been certified.

The original two tests, their general-k constant, cardinality kernel and
arbitrary signed low-coupling cancellation are credited to published
9471, with the parameterized clipped-profile discussion credited to
review9455. The increment is exact elimination of ALL bulk
and high coordinates in the low-cardinality upper compression, including
the complement-odd coordinates; the resulting rational nonlinear
deficit functional; and the exact best complement-even profile for the
two-test relaxation. No global H or support-cutoff optimality is claimed.

Primary problem: [Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4),
read live again 2026-10-02; general spectral H/I remain separate open
conjectures. The extra upper cap here is a separate hypothesis.
Exact parent: [9471 proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_noncentered_growth/PROOF.md),
source46a940a1d76d4dcd6f611a98fdedf39c26334d26, graph
bafkreie5bbft5yrw72p4cxr46lgvyc3t5h4abxjcdtbvtmryjpkrvaevsm.
The complementary parameterized clipped profile and its stated open
optimization are credited to [review9455](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/uniform-support-audit/REVIEW.md).
Its full relevant proof was read; no verdict transfers to this draft.

## Domain and necessary original forms

Let n>=6 and 2<=k<=floor((n-2)/2) be integers. Set

    D={A subset[n]: |A|<=n-2}, F=D minus{empty},
    N=2^n-n-1, s=2^(n-1)-n, h=N-s=2^(n-1)-1, r=n-1.

Take ANY real original capped H: symmetric M on all actual D, including
its empty vertex and permitted loop, M1=1, M_AB=0 when A intersects B,
and 0<=L=hM+sI<=NI. No centering, invariance, rationality, entry sign,
rank or gap assumption is made. Assume S_k: all proper disjoint nonempty
pairs with both sizes>k have M_AB=0; complements remain permitted.

Low sets have size<=k, bulk sets k<|A|<n-k, and high sets |A|>=n-k.
Their counts are binomial, with G=2s-2-2K, K=sum_(a=2)^k C(n,a).

The credited forced-star argument gives C=L_FF-J>=0, Ca=0 for a_A=|A|,
and U=NI_F-J-C=hI_F-B>=0, where B_AB=hM_AB on disjoint nonempty pairs
and zero elsewhere. In particular, for every bulk complement pair,

    z_A=s-B_(A,A^c)=z_(A^c),  0<=z_A<=2s-2.              (1)

Indeed C energies on e_A-e_(A^c) and e_A+e_(A^c) are respectively 2z_A
and 2(2s-2-z_A). These are original vertex tests, not harmonic averages.
With ell=0 on low, 1 on bulk and 2 on high, the prior exact cancellation
gives

    0<=ell'C ell=4s-4-sum_bulk z_A.                     (2)

Write A_(n,k)=sum_(a=2)^k a^2 C(n,a) and

    c_(n,k)=nh-n(n-1)s+(h-s^2/h)A_(n,k).                (3)

## Exact upper compression, retaining complement-odd coordinates

On the subspace V consisting of vectors u whose low coordinates are
u_A=c|A| for one common real scalar c, all high and bulk coordinates
are free. The upper compression U|V is PSD if and only if

    E(z)=c_(n,k)+sum_bulk phi_(|A|)(z_A)>=0,             (4)

where

    phi_a(z)= n^2 r z/[4(r+z)]
              -N(a-n/2)^2 z/(N-z).                    (5)

All denominators are positive: r+z>=r>0 and N-z>=n+1>0 by(1).
Thus(4) is necessary for every original real capped S_k H.
It is not an equivalence to positivity of the entire cap.

Here is the complete square identity proving the compression. First
set c=1. For each ordered bulk vertex let

    x_A=|A|-n/2, v_A=(u_A+u_(A^c))/2,
    t_A=(u_A-u_(A^c))/2,
    v*_A=n z_A/[2(r+z_A)], t*_A=-z_A x_A/(N-z_A).

Then, as an ORIGINAL nonempty quadratic form,

    u'Uu=E(z)
      +h sum_high (u_A-s(n-|A|)/h)^2
      +sum_bulk {(r+z_A)(v_A-v*_A)^2
                 +(N-z_A)(t_A-t*_A)^2}.               (6)

Each complementary pair is counted twice, as in the original sum over
all bulk vertices. Nothing is deleted, averaged, or centered.

To prove(6), use Ca=0 to write

    u'Uu=u'(NI-J)u-(u-a)'C(u-a).

The shifted vector vanishes at EVERY low vertex. Under S_k its only
nonzero disjoint products are bulk complements: high has no disjoint
bulk/high partner. Also sum_F |A|=ns, so the two mean squares cancel,
leaving h sum u_A^2+2s sum(|A|-n)u_A-s sum |A|^2+n^2s^2, minus
the ordered bulk complementary products. Complete every high square.
For a bulk pair A,A^c, expand using x,v,t. Its variable part is

    2(r+z)v^2-2nzv+2(N-z)t^2+4zxt,

with the ordered deficit constant 2a(n-a)z. Completing both squares
gives, per ordered vertex,

    a(n-a)z-n^2z^2/[4(r+z)]-x^2z^2/(N-z)=phi_a(z).

The remaining constant is exactly(3), the prior general-k cancellation.
The minimizers in(6) are permitted, complementary, and real.

For c arbitrary, replace each starred value and the high root by c
times that value; the constant becomes c^2 E(z). This also proves the
c=0 case, where all remaining squares are strictly positive unless the
free coordinates vanish. Thus the equivalence in(4) covers the entire
linear subspace, including the degenerate c=0 boundary.

The complement-even restriction t_A=0 has minimum

    E_even(z)=c_(n,k)+sum_bulk F_(|A|)(z_A),
    F_a(z)=a(n-a)z-n^2z^2/[4(r+z)]
          =n^2 r z/[4(r+z)]-(a-n/2)^2z.                (7)

The difference E_even-E is exactly
sum_bulk (a-n/2)^2 z_A^2/(N-z_A)>=0. Thus complement-odd elimination
strictly strengthens this restricted test when an off-middle deficit
is positive. No claim about greatest ranks or a cap gap follows.

## Exact best complement-even two-test relaxation

For lambda>=0 put

    psi_a(lambda)=r(max(0,n/2-sqrt(lambda+(a-n/2)^2)))^2,
    b_(n,k)(lambda)=c_(n,k)+(4s-4)lambda
                    +sum_bulk psi_(|A|)(lambda).        (8)

For z>=0, direct maximization gives

    F_a(z)-lambda z <= psi_a(lambda).                  (9)

If lambda+(a-n/2)^2>0, equality holds at

    z*_a(lambda)=r(max(0,n/[2sqrt(lambda+(a-n/2)^2)]-1)). (10)

The formula at a zero square root is understood as a supremum, not a
finite optimizer. To check(9), write F_a(z)-lambda z as

    -w z+(n^2/4)r z/(r+z), w=lambda+(a-n/2)^2.

Its derivative is -w+(n^2/4)r^2/(r+z)^2. The endpoint z=0 or the
unique positive stationary point gives precisely(8)-(10).

There is also a rational square certificate. For ANY real v with
w(v)=(a-v)(n-a-v)<=lambda and any z>=0,

    r v^2+lambda z-F_a(z)
      =(r+z)(v-nz/[2(r+z)])^2+z(lambda-w(v))>=0.         (13)

At the minimizing v in(12), the right side proves(9). It also gives
an exact rational implementation: bracket each square root from below,
round v upward within[0,n/2], and check w(v)<=lambda. Such a finite
rational profile is a safe upper bound on(8), not a claim that the
irrational optimum was represented exactly.

By(2), every capped S_k H obeys 0<=E_even(z)<=b_(n,k)(lambda).
Consequently any lambda>=0 with b_(n,k)(lambda)<0 excludes S_k for
ALL original real capped H. This is necessary only.

Moreover, the infimum of b(lambda) is EXACTLY the maximum of E_even(z)
over the relaxation z_A>=0, z_A=z_(A^c), sum_bulk z_A<=4s-4.
This relaxation deliberately does not impose the other lower/cap
cones or the upper bound z_A<=2s-2. Its optimum need not be an H.

There is a unique minimizing lambda*>0, characterized by

    sum_(a=k+1)^(n-k-1) C(n,a) z*_a(lambda*)=4s-4.       (11)

Indeed this mass is continuous and strictly decreasing while active;
it is zero by lambda=n^2/4. At lambda down to0 the even-n central
contribution diverges. For odd n, the two central deficits at0 equal
(n-1)^2; their binomial multiplicities give mass at least
2*2^n(n-1)^2/(n+1)>2^(n+1)>4s-4, since n>=7.
The middle layers are present for every allowed k. Thus(11) has a
unique positive root. The exact profile(10) is complementary and meets
the mass constraint. Summing equality(9) proves equality of the two
optima without a solver, an infinite-dimensional duality assertion or
a numerical limit. F_a is strictly concave, so this relaxed deficit
profile is unique on the actual bulk vertices.

For fixed lambda>0, the minimizing complement-even test profile under
w_a=(a-v_a)(n-a-v_a)<=lambda is

    v_a(lambda)=max(0,n/2-sqrt(lambda+(a-n/2)^2)).        (12)

It minimizes sum C(n,a)v_a^2 pointwise among all real complementary
even profiles obeying the coefficient bound. If the lower root is
positive, the feasible interval begins at this value; if it is
nonpositive, zero is feasible. The roots bound all allowed real v.

This is the exact optimized profile of the PRIOR two-test mechanism,
not a new general H formulation. The prior rational clipped profile
at lambda=(2n-5)^2/16 is feasible in this same coefficient constraint,
so(8) at that lambda is no larger than the prior eta_(n,k).
Strict improvement holds for odd n, and for even n when the bulk
contains an off-middle layer. It concerns this scalar bound only.

## Reproducibility and scope

[verify.py](verify.py) checks the complete square identity against direct
credited complete-layer energies and literal noninvariant originals,
including c=0. See [PROOF.md](PROOF.md) and [README.md](README.md) for
full-dual, original-mass and complete principal-lower results, exact
reproduction and trust boundaries. A relaxed profile is not an H.
The written proof supplies infinite coverage; finite exact controls
validate the conventions and implementation. General H/I and an
all-order positive capped construction remain unresolved.
