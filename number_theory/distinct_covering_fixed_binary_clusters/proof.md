# Distinct top points with prescribed top phases

Actual author: **six-covering-2**, role **researcher**, 2026-09-30.
Written lemmas and exact author checks; no historical-priority or independent-review claim.
This is a sharpening of the campaign's existing primitive-block charge and
an extension to fixed top classes, not a new numerical L_min(8) bound.

Let N=BC, B,C>=2 coprime, rho=rad(B), T=B/rho, b|T and Q=bC. Let A
be known distinct classes dividing N and R be possible unused eligible
divisors, disjoint from A's moduli. Assume every top resource
S={Bd:d|C} is either prescribed in A or available in R. A completion can
use any subset of R, at most one phase per modulus. Top classes prescribed
in A retain their phases. This is different from requiring all S unplaced.

Let u>=0 on Z/N vanish on every known class. Let v>=0 be Q-periodic;
it can be positive on any known class, including a known top class.
Write D(f)=sum_(x modN) f(x), Phi_(n,a)(f)=sum_(x=a modn) f(x), and
C_n(f)=max_a Phi_(n,a)(f).

For each actual complete choice of top phases (adjoining unused available
top classes if necessary), let alpha_d modB and a_d modd be its CRT
coordinates. In the block q+Tj (j modrho), at cofactor z, define

    P(q,z)={alpha_d : alpha_d=q modT, z=a_d modd},
    r(q,z)=|P(q,z)|, f(r)=r if r>=2 and0 otherwise.

P is a set of distinct B-coordinate points, not a multiset of resources.
Let A_S be the prescribed top resources. Define

    K_A(u,v)=max over the FREE top phases of
      [sum_(n in S outside A_S) Phi_(n,a_n)(u)
       +sum_(q modT,z modC) f(r(q,z))*v_z(q modb)],

with the phases of A_S fixed exactly. Every completion satisfies

    D(u+v)-sum_((n,a) in A, n outsideS) Phi_(n,a)(v)
      <=sum_(n in R outsideS) C_n(u+v)+K_A(u,v).           (1)

Only known OUTSIDE footprints are subtracted in (1). A prescribed top
class participates in P with its actual point. Subtracting its footprint
on the left without making the same subtraction from K_A is a different
and weaker rearrangement, not the formula above. Known outside costs
have multiplicity; a negative effective demand is allowed.

## Proof

Fix q,z. The periodic weight has a constant value W on this primitive
block because b|T. A class with proper B-part is either inactive at z
or its indicator has a shift by rho/ell in j, for a prime ell dividing
rho: its B-part divides B/ell. This includes prescribed outside classes.

Use the elementary sign lemma from the existing primitive-block proof:
a sum of these proper-period functions which is nonnegative except
possibly at one point j0 has nonnegative total. The product over primes
ell|rho of (I-shift_(rho/ell)) kills each summand, including a constant.
Its subset corners j0+sum_(ell inE)rho/ell are distinct: reduce a
difference modulo a prime in the symmetric difference. Expansion gives
the identity

    sum_j h(j) = 2sum_(E with odd size) h(j0+sum_(ell inE)rho/ell)
                 +sum_(j outside all subset corners) h(j).

Every displayed value is away from j0, so it is nonnegative. This proves
the sign step and credits six-covering-3's mechanism7420.

If r(q,z)<=1, the sum of ALL used outside footprints minus W is
nonnegative away from at most one distinct top point, even if many top
resources coincide there. The sign lemma shows that outside footprints
alone meet the whole block demand. If r(q,z)>=2, ordinary weighted union
counting charges the distinct top points once, yielding r(q,z)*W rather
than the number of active resources times W. Thus

    D(v) <= sum_(known outside) Phi(v)
            +sum_(used unused outside) Phi(v)
            +sum_(q,z) f(r(q,z))*W.

Adjoining an omitted free top class cannot decrease f(r), since f is
nondecreasing, and cannot alter a prescribed phase. Ordinary counting
for u, which vanishes on all known classes, gives

    D(u) <= sum_(used unused outside) Phi(u)
            +sum_(free top) Phi(u).

Combine outside u,v footprints at the SAME actual phase before taking
their individual capacities; add nonnegative capacities of any omitted
outside resources. Maximizing only FREE top phases proves (1).
No actual-LCM equality, irredundancy, numerical solver, integrality of
u/v, or cofactor prime-power assumption is required by the proof.

When no top resource is prescribed, K_A(u,v)<=J(u,v) of the published
joint-top lemma. Pointwise r<=k and f(r)<=k*1_(k>=2), with the same
unrestricted top footprints. Strictness is possible. The input domain of
that published theorem did not permit a top modulus to be prescribed;
the present statement records the fixed-phase restriction explicitly.

For a power-of-two B, rho=2, so the periodic charge is exactly2W when
both binary points have active top classes and0 otherwise. The bound
therefore truncates every larger resource multiplicity on that block.

## Exact small controls and a necessary optimization warning

At N=36,B=4,C=9,b=2, put v(x)=1_(x=0 mod18). With u=0 and all top
resources free, complete phase enumeration gives K=2 versus J=3.
With u(x)=1_(x=0 mod36), the maxima are4 and6. These are budgets, not
covers or exclusions. With (4,0) prescribed, v positive on it, and
u(x)=1_(x=18 mod36), the fixed-phase maxima are4 for the distinct-point
charge and5 for the multiplicity comparator.

The old set-partition formula cannot simply replace k by r and remain
EXACT. At N=60,B=4,C=15,b=2, v(x)=1_(x=0 mod30), u=0, the true
distinct-point maximum is2. An independent sum of two pair-group maxima
is4: both groups choose q=0 and the same two points. Merging them loses
the duplicated charge. Resource multiplicity was superadditive under
equal-label merging in the old proof; distinct-point cardinality is not.
Independent group sums remain upper relaxations, not exact realizations.
A future exact optimizer must keep distinct primitive-block labels, for
example by a subset dynamic program over actual labels, as well as the
within-label B-coordinate choices. No large-cofactor optimizer is supplied.

The control code uses a capped exhaustive actual-phase product.
The universal argument is the written proof. A separate literal-residue
checker verifies actual charges on genuine period36 covers with fixed
top phases, positive known weights and negative effective demands. Its
limits do not become exclusions. The assigned15120 application would
use B16,C945,b8 and the already prescribed16 class, but optimizing that16-resource cofactor remains unimplemented. The cluster
relaxation below supplies a strict practical same-vector certificate.

Dependencies: six-covering-3 primitive sign/block proof7420, source
234569d6f32f1ad96958ed3300050d9ce7acef1e; six-covering-2 joint-top proof
committed7520, sourcef6bcc479c1deb0bc6383cf0db261a64e617cff3c; related
six-reviewer-5 coarsest pair-overlap refinement7520/source
16fffdf8660ac980b5a11c5efa0ba9e7f5868a00. That review does not review this
lemma. No numerical bound or independent review is asserted.

## A tractable fixed-binary cluster upper relaxation

Suppose B is a power of two, and A contains exactly ONE top resource,
the coarsest B-class at alpha0. Set q0=alpha0 modT and
alpha1=alpha0+T modB. All other top resources are eligible and unplaced.
Let U_d(alpha,r)=sum_(z=r modd) u(alpha,z), V_d(t,r)=sum_(z=r modd)v_z(t).
For d|C,d>1 set

    L_d=max_(alpha modB,alpha !=q0 modT,r modd)
          [U_d(alpha,r)+V_d(alpha modb,r)],
    H_d=max_(r modd)[U_d(alpha1,r)+2V_d(q0 modb,r)].

Use L_d=0 if the outside phase set is empty; this permits harmless
omission in the upper relaxation. Choose a small cluster P of distinct
divisors d>1 of C. For G subset P define

    U_G=max_(r_d modd for d inG)
          [sum_(d inG)U_d(alpha1,r_d)
           +2sum_(z in UNION of the G cosets) v_z(q0 modb)],
    U_empty=0,
    H_P=max_(G subsetP)[U_G+sum_(d inP outsideG)L_d],
    K_cluster=H_P+sum_(d|C,d>1,d outsideP)max(L_d,H_d).

Then K_A(u,v)<=K_cluster, so (1) is valid with this upper budget.
The union is counted once, with coefficient two. For a pair this retains
twice its weighted intersection as a deduction from two inside charges;
larger clusters account for their entire union and avoid unsafe independent
subtraction of many overlapping pairs. This adapts the reviewer5 cluster
observation to a fixed binary coarsest class; it is not the reviewed G formula.

Proof: at q0 the known B-class covers the alpha0 point for every z. A free
top class there with the same point contributes zero u (u vanishes on the
known class) and cannot increase the periodic point set. Moving it to
alpha1 with its same cofactor phase can only increase the objective. The
periodic charge at q0 is therefore bounded by twice the weighted union of
the inside free cosets. Every other block q has no prescribed top class;
its distinct-point periodic charge is at most the sum of actual free
periodic footprints. These outside mixed footprints are bounded by L_d.
Within q0, keep the exact union for whichever cluster members are inside,
and charge noncluster cosets individually. Nonnegative union counting
justifies this allocation. Maximizing the cluster's inside subset gives
H_P, and bounding each other resource by max(L_d,H_d) proves the result.

This formula needs only product_(d inP)(1+d) phase evaluations for the
chosen cluster, plus individual physical maxima. At15120 choose
B16,C945,b8, known16=4 and clusterP={3,5,7}: just192 cluster evaluations.
This is a complete upper-relaxation computation, not a full16-resource
optimizer. A strict physical integer cut would still need exact support,
all outside resources, known-outside costs and alternate literal checks.
Other prescribed full-B resources violate this particular corollary's
hypotheses. Their general fixed-phase K_A case remains a separate problem.


## Complete conditional period15120 application

The known classes are

    [(8,0),(9,0),(10,1),(14,1),(12,6),(16,4),(15,2),
     (18,5),(20,16),(21,4),(24,1)].

The minimum is exactly8. All remaining eligible divisors of15120 can be
used in any subset with arbitrary phases. The only prescribed full-binary
resource is16. Use B16,C945,b8, Q7560, q0=4, alpha1=12 and clusterP={3,5,7}.
The52 literal CRT boxes in [input.json](input.json) define w>=0. Set
u=w and v(x mod7560)=w(x)+w(x+7560). The boxes are disjoint and have axes
(16,27,5,7); the checker decodes them in two separate ways. No discovery
solver, orbit declaration, graph or private frontier is a proof input.

All known classes have u-weight zero. The periodic component is zero
on every known PROPER-binary class and has weight93771 on the known
16-class. It therefore violates the old all-top-unplaced hypothesis and
is not a supported-weight instance of that earlier theorem.

Exact physical totals:

| Quantity | Value |
| --- | ---: |
| Demand D(u+v), known-outside costs zero | 2999745 |
| Outside capacity, all47 unused proper-binary resources | 2577600 |
| Cluster top upper budget | 395838 |
| Total / strict gap | 2973438 / 26307 |
| No-cluster fixed-binary top upper budget | 396468 |
| No-cluster total / strict gap | 2974068 / 25677 |
| Ordinary residual demand, same vector masked off all known classes | 2905974 |
| Ordinary residual capacity, all62 unused resources | 2946125 |

The cluster adds630 units of saving; it is not necessary for strictness
of this particular vector. The fixed-top binary bound is essential to
this SAME-VECTOR comparison with ordinary counting. The input ALSO
contains a different ordinary vector with demand99003, capacity98995
and strict gap8. Thus this application does not establish a stronger
optimized bound, a newly necessary proof mechanism for this prefix,
a full15120 exclusion or any new numerical L_min(8) bound.

[check.py](check.py) recomputes every actual outside/resource phase,
evaluates all192 selected-cluster phase cases, and independently verifies
the bound using ordinary progressions and literal unions. It also checks
the alternative ordinary certificate, all61668 declared small actual-top
phase tuples,764 genuine-cover weight cases,194 cluster cover cases,
positive known-top weights, negative effective demands and explicit
invalid/incomplete-input rejections. Small controls have lower minimum
moduli and are not target constructions. One ambient60 control has actual
LCM12; actualLCM equality is not a premise of the covering inequalities.

Reproduce from repository root with Python3.10+ and the standard library:

    python3 -B number_theory/distinct_covering_fixed_binary_clusters/check.py
    python3 -B -O number_theory/distinct_covering_fixed_binary_clusters/check.py

Both commands must match [expected.json](expected.json). The written
proof supplies universal validity; finite controls check the implementation.
Trust boundaries are the unformalized CRT/sign/union arguments, ordinary
Python arbitrary-precision integers, and the compact literal input.
No proof assistant, independent review or historical priority is claimed.
The campaign's1973-node eight-class15120 subtree and other private partial
frontiers are not included or assumed. Global candidates remain
10080,15120,20160, with only20160 witnessed among these inputs.

## Primary and campaign source context

[Zhang--Zhang](https://arxiv.org/html/2607.19029) provides the
minimum-seven/successive-filtering context; [HKLT Problem3](https://arxiv.org/html/2605.18644)
is the separate pure235 target. Both were retrieved live2026-09-30.
Neither is a proof premise or a solution of unrestricted exact minimum8.
No exhaustive historical-priority search is claimed.

The local sign argument credits six-covering-3's
[primitive-block proof](../distinct_covering_primitive_block_capacity/proof.md),
source234569d6f32f1ad96958ed3300050d9ce7acef1e, graph7420. The earlier
[joint-top/known-footprint proof](../distinct_covering_joint_top_budget/proof.md)
is six-covering-2's sourcef6bcc479c1deb0bc6383cf0db261a64e617cff3c, committed7520;
the present distinct-point charge and fixed top phases refine that scope.
The union cluster allocation acknowledges the independently selected
six-reviewer-5 [coarsest pair review](../distinct_covering_coarsest_block_review5/REVIEW.md),
source16fffdf8660ac980b5a11c5efa0ba9e7f5868a00, graph7520. This is a binary
fixed-coarsest formula, not a reproduction or review of the general G formula.
The actual-resource framework is six-covering-2's
[weighted residual proof](../distinct_covering_residual_weight_duals/proof.md),
sourceb9d39eb740a866e07237be1c78b834d1ab6ea718, graph7174.


The final source refresh also read six-covering-3's
[coupled coarsest proof](../distinct_covering_coupled_coarsest_budget/proof.md),
sourcee31259c8420004b5521b823e03050ddd58a8dbdf. Its mixed inside/outside
phase profiles and designated-pair refinement are attributed to that author,
with the pair mechanism credited there to reviewer5. It permits positive
known u/v footprints but still requires EVERY top resource unplaced.
Here the binary coarsest class is prescribed and its actual phase is fixed.
Its opposite binary coordinate and the cluster's entire union provide the
specific upper relaxation above. No general-profile or reviewer-pair
priority is claimed here. That source was read before this publication.
