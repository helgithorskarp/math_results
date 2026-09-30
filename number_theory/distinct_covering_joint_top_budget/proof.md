# Joint top phases and known periodic footprints

Actual author: **six-covering-2, researcher**, 2026-09-30. These are written
finite covering lemmas with exact author controls. No independent review,
formal proof-assistant certification, historical priority or new numerical
bound for minimum exactly eight is asserted.

The result strengthens our [mixed-weight bound](../distinct_covering_mixed_block_bounds/proof.md),
source46f06c2bd5d2558e1b91082545ad6e57fc2bb4c9, graph7480. The primitive-block
sign mechanism is from **six-covering-3, researcher**,
[source234569d6](../distinct_covering_primitive_block_capacity/proof.md),
graph7420. The exact realization proof adapts that author's equal-label
merging from [source42b081df](../distinct_covering_primitive_partition_realization/proof.md),
graph7464. All needed proof steps are supplied below.

## Parameters and actual top charge

Let N=BC with coprime integers B,C>=2. Put rho=rad(B), T=B/rho, choose b|T,
and write Q=bC. Prescribe classes A={(m,a)} with distinct eligible moduli
dividing N. Let R be distinct unplaced eligible divisors of N, containing
every member of S={Bd:d|C}. A completion may use any subset of R, at most
one phase for each modulus, and covers all residues modulo N together with
A. All top resources must be eligible and unplaced. Eligibility may mean
modulus at least eight. No assumption that the actual completion LCM equals
N is made.

For a nonnegative weight f on Z/N put D_N(f)=sum_x f(x),
Phi_(n,a)(f)=sum_(x=a modn)f(x), and C_n(f)=max_a Phi_(n,a)(f).
Let u>=0 vanish on A. Let v>=0 be Q-periodic; initially it need not vanish
on A. In CRT coordinates write u(alpha,z), alpha modB,z modC, and
v_z(t), t modb. The pair (alpha,z) denotes the ordinary residue satisfying
these two congruences, not alpha*C+z.

A top Bd class has independent coordinates alpha_d modB and r_d modd.
Its unrestricted footprint is

    U_d(alpha_d,r_d)=sum_(z=r_d modd) u(alpha_d,z).

Write h(k)=k for k>=2 and h(0)=h(1)=0. Define its actual useful periodic
charge by grouping primitive-block labels q=alpha_d modT:

    k_q(z)=#{d: alpha_d=q modT and z=r_d modd},
    M((alpha_d,r_d))=sum_d U_d(alpha_d,r_d)
                    +sum_(q modT,z modC) h(k_q(z))*v_z(q modb).

Let J(u,v)=max M over all actual top phases. This is a maximum of the
defined charge, which retains class multiplicity even at coincident points.
It is not union mass or a maximum over phases admitting a covering.

## Exact partition reduction

For q modT and r modd put

    A_d(q,r)=max_(alpha=q modT) U_d(alpha,r).

For each nonempty group G of divisors of C define

    k_G(z)=#{d inG:z=r_d modd},
    J_G=max_(q modT,(r_d modd:d inG))
           [sum_(d inG) A_d(q,r_d)
            +sum_(z modC)h(k_G(z))*v_z(q modb)].

**Joint-top lemma.**

    J(u,v)=max_(set partitions pi of {d:d|C}) sum_(G inpi) J_G.       (1)

For the upper bound, equality of actual q labels induces a partition of
the top resources. Each group's unrestricted footprints are bounded by
A_d at its actual q,r, and its useful periodic charge is exactly the
displayed group charge. Maximizing the groups separately gives the right
side of (1).

Conversely choose an optimizing partition and all its group maximizers.
Merge groups choosing the same q. Each resource independently chooses a
B-coordinate attaining A_d(q,r_d), so its unrestricted charge stays the
same. The useful periodic charge does not decrease: h is superadditive,
h(a+b)>=h(a)+h(b), and v>=0. After merging, group q labels are distinct.
The chosen B-coordinates and cofactor phases are realized by CRT modulo
Bd. They give actual phases with charge at least the partition maximum.
The upper bound prevents a larger value. This proves equality.

The merging mechanism is explicitly adapted from six-covering-3's cited
7464 result, whose pure periodic case is reproduced here as J(0,v)=F_C(v).
The new reduction keeps the unrestricted u footprints at the same block
labels and phases as the periodic useful charge. Singleton groups retain
their unrestricted charges; the old special two-term F formula cannot
simply be reused for J.

The subset recurrence fixes the least remaining resource, considers every
group containing it, and recurses on the complement. It enumerates all
unordered partitions. With four resources there are15 nonempty groups and
15 partitions. The theorem applies to any cofactor; the public optimizer
is deliberately limited to cofactors having at most four divisors.

For fixed actual phases, useful v mass is at most all top v footprints.
Bounding each phase separately gives

    J(u,v)<=sum_(n inS) C_n(u+v).                                  (2)

Separately, top u mass is at most sum_S C_n(u) and useful v mass is at most
the earlier partition budget F_C(v), so

    J(u,v)<=sum_(n inS) C_n(u)+F_C(v).                              (3)

The endpoints are J(u,0)=sum_S C_n(u) and J(0,v)=F_C(v). The former is
attained by independent phases; the latter is exactly the group partition
definition because every t modb is represented by q modT.

## Known-footprint covering inequality

**Affine completion lemma.** Every completion satisfies

    D_N(u+v)-sum_((m,a) inA) Phi_(m,a)(v)
        <=sum_(n inR outsideS) C_n(u+v)+J(u,v).                    (4)

The known footprints are summed with multiplicity. In particular, overlap
of known classes can make the left side negative. No union correction,
coefficient truncation or replacement by uncovered demand is valid in (4).
If v also vanishes on A, the left side is simply D_N(u+v), giving a sharper
supported mixed inequality than the earlier separate top charges.

We include the primitive-block argument for completeness. On Z/rho let g
be a sum of functions, each invariant under shift rho/ell for some prime
ell|rho. If g>=0 except possibly at one point, then sum_j g(j)>=0.
Indeed, the commuting operator product_(ell|rho)(I-shift_(rho/ell))
annihilates every summand. Its subset shifts are distinct: modulo a prime
in the symmetric difference, only its own rho/ell term is nonzero. At a
possibly negative j0, expansion of the identity gives

    -g(j0)=sum_(nonempty even subsets E) g(j0+sum_(ell inE)rho/ell)
            -sum_(odd subsets E) g(j0+sum_(ell inE)rho/ell).

All the other values are nonnegative. The even-subset values therefore
compensate any negative value, and the full sum is nonnegative. A constant
function has the required invariance.

Adjoin missing S classes with arbitrary phases, preserving covering and
distinctness. Fix z modC and a primitive B-block q+Tj, j modrho. The weight
v_z is constant on this block. Every known modulus and every used outside
resource has proper B-part m=gcd(n,B)<B, since all full B-part resources
belong to S and are unplaced initially. Choose a prime ell|B with m|B/ell.
Its active class indicator is invariant under j-shift rho/ell, which
changes the B-coordinate by B/ell. Its v footprint has the same invariance.

Include known classes at their fixed phases in the outside footprint sum.
In a block with at most one active top class, subtract the constant demand
v_z from that sum. Covering makes the difference nonnegative except
possibly at the top point. The sign fact shows that known and used outside
footprints alone meet the entire block's v demand. With k>=2 active top
classes, ordinary weighted counting instead charges their k footprints,
of total k*v_z(q modb). Summing gives

    D_N(v)<=sum_A Phi(v)+sum_actual_used_outside Phi(v)
                      +actual_useful_top_v.

Ordinary counting for u, whose known footprints are zero, gives
D_N(u)<=sum_actual_used_outside Phi(u)+sum_top Phi(u).
Add these inequalities and combine the u,v footprints of each outside
resource at its same actual phase before maximizing. Bound the actual top
sum by J(u,v), add nonnegative unused outside capacities, and move known v
footprints to the left. This proves (4).

For a Q-periodic v, n|N and g=gcd(Q,n), CRT gives the exact known footprint

    Phi_(n,a)(v)=(N/lcm(Q,n))*sum_(x modQ,x=a modg)v(x).             (5)

When gcd(Q,n)=1 this equals D_N(v)/n. A prescribed coprime modulus therefore
costs its fixed density rather than forcing v to zero. At N15120,B560,C27,
b8,Q216 a prescribed35-class costs exactly D_N(v)/35. Requiring v to vanish
on that class would force v=0, as six-covering-3 warned in the 7464 source.
This bridge is not a numerical exclusion or a covering witness.

## Relation to the newer coarsest-resource relaxation

The prepublication refresh read **six-covering-3's**
[shared-label bound](../distinct_covering_coarsest_block_budget/proof.md),
source959893f7358905bc46ddb01fdcaaffa8086ffe3f, graph7516. That result proves
F_C(v)<=G_C(v), where G_C is a faster upper relaxation for arbitrary-size
cofactors. Thus (3),(4) also give the useful corollary

    D_N(u+v)-sum_A Phi(v)
       <=sum_(R outsideS) C_n(u+v)+sum_S C_n(u)+G_C(v).             (6)

This credits and extends its application to periodic weights positive on
known classes; the G formula and its previously published conditional
43200 certificate are not new claims here. Computing G can be preferable
when exact J is too expensive. No uniform comparison between J(u,v) and
G(v) alone is asserted when u is nonzero.

The checker reproduces that author's N36 component fixture, with B9,C4,b3
and cofactor rows (2,0,0),(0,3,0),(2,0,0),(0,0,0). It finds
J(0,v)=F_4(v)=10<G_4(v)=12<2*sum_(d>1) M_d=14.
This attributed comparison is not a covering or exclusion.

## Exact scope and controls

The standard-library checker compares (1) with every actual top-phase tuple
for seven specified weight pairs:206532 tuples. It checks42 supported or
affine weights against small genuine coverings, including fixed known
footprints with overlap, and3 further affine controls using
six-covering-1's [published20160 covering](../distinct_covering_min8_20160/cover.json),
source1b26a5217c02c00ede618b445dc935a88839391a, graph7286, independently
reviewed at7302. The copied fixture's exact bytes are pinned and attributed.
For those external controls B2240,C9,b16,Q144 and the first15 known classes
include modulus35. Periodic weights remain positive everywhere and their
known35 charge is exactly one thirty-fifth of periodic demand. This is a
reproduction of that covering input, not a new construction.

At N10080,B288,b48,C35 and N15120,B432,b72,C35 prescribe0 mod8, take u as
point1 and v as1 away from0 mod8. J=28, while the earlier separate top budget
is29. The full capacities become11572 and17802, respectively:24 below the
ordinary capacities11596 and17826. Demands8821 and13231 are still smaller
than these capacities. Neither period nor root is excluded by these
illustrations. Ten malformed hypotheses/components reject explicitly.

All controls use exact integers and explicit exceptions, including under
-O. No solver, private frontier or graph query is a verification premise.
Universal validity is the written proof, not extrapolation from the controls.
The exact joint optimizer is exponential; arbitrary cofactor optimization
and any full-period exclusion are outside this artifact.

The assigned exactly-eight target comes from the confirmed campaign brief.
[Zhang–Zhang](https://arxiv.org/html/2607.19029) gives the minimum-seven
context. [HKLT Problem3](https://arxiv.org/html/2605.18644) concerns the
separate pure235 support frontier. Both primary pages were retrieved live
on2026-09-30 and are contextual rather than premises of these lemmas.
