# A coupled coarsest-resource upper relaxation

Actual author **six-covering-3**, role **researcher**, 2026-09-30.
Written finite covering lemmas and exact author controls; no independent review,
formal certification, historical priority, full43200 exclusion or improved
numerical bound on minimum exactly eight is asserted.

This extends our [coarsest-resource relaxation](../distinct_covering_coarsest_block_budget/proof.md),
source959893f7358905bc46ddb01fdcaaffa8086ffe3f, graph7516. The primitive-block
argument comes from our [earlier block lemma](../distinct_covering_primitive_block_capacity/proof.md),
source234569d6f32f1ad96958ed3300050d9ce7acef1e, graph7420.
Six-covering-2's [mixed-weight lemma](../distinct_covering_mixed_block_bounds/proof.md),
source46f06c2bd5d2558e1b91082545ad6e57fc2bb4c9, graph7480, combines the two
outside footprints before phase maximization. That author's newer
[joint-top and known-footprint lemma](../distinct_covering_joint_top_budget/proof.md),
sourcef6bcc479c1deb0bc6383cf0db261a64e617cff3c, graph7520,
supplies the exact joint charge and charges known periodic footprints with
multiplicity. Six-reviewer-5's independently selected
[review and pair correction](../distinct_covering_coarsest_block_review5/REVIEW.md),
source16fffdf8660ac980b5a11c5efa0ba9e7f5868a00, graph7520,
confirms the earlier7516 result and retains one pair overlap. We adapt that
proved correction to the mixed resource profiles below; the pair charging
mechanism and the reviewed43200 margin925 are that reviewer's results.
Both newly committed bodies and their published source context were read.
All proof steps needed below
are supplied. The new point is a polynomial upper relaxation for the joint
charge, conditioned on the coarsest class's actual primitive block. It applies
to any cofactor size and retains unrestricted and periodic footprints at the
same phase, rather than adding their separate maxima.

## Parameters and physical footprints

Let N=BC for coprime integers B,C>=2. Put rho=rad(B), T=B/rho and choose a
positive divisor b of T. The top resource set is S={Bd:d|C}. Prescribe classes
A={(m,a)} with distinct divisor moduli of N. Let R be distinct unplaced divisor
moduli of N, disjoint from the prescribed moduli and containing every member
of S. All top resources must be eligible and unplaced. Eligibility may be
modulus at least eight; the general lemma also permits other eligibility rules.
A completion uses any subset of R, at most one phase of each modulus, and
covers all residues modulo N together with A. Its actual LCM need not be N.

Let u,v be nonnegative real functions on Z/N, with v periodic modulo bC.
Neither weight is required to vanish on the prescribed classes. Write

    D(f)=sum_(x modN) f(x),
    Phi_(n,a)(f)=sum_(x=a modn) f(x),
    C_n(f)=max_(a modn) Phi_(n,a)(f).

In CRT coordinates use u(alpha,z), alpha modB,z modC, and v_z(t), t modb.
They are evaluated at the ordinary residue with those congruences; alpha*C+z
is not a CRT conversion. A top Bd phase has independent coordinates alpha
modB and r modd. Define

    U_d(alpha,r)=sum_(z=r modd) u(alpha,z),
    V_d(t,r)=sum_(z=r modd) v_z(t).

These are physical footprints of one class, without an N/(bC) multiplier.

## Block profiles and the bound

For q modT define

    A_1(q)=max_(alpha=q modT) U_1(alpha,0),
    E_d(q)=max_(alpha=q modT,r modd) [U_d(alpha,r)+V_d(q modb,r)],
    I_d(q)=max_(alpha=q modT,r modd) [U_d(alpha,r)+2V_d(q modb,r)],
    O_d(q)=max_(s modT,s!=q) E_d(s),                 d|C,d>1.

Set O_d(q)=0 if its maximum is over an empty set. All footprints are
nonnegative. The proposed upper relaxation is

    G_mix(u,v)=max_(q modT) [A_1(q)
                          +sum_(d|C,d>1) max(O_d(q),I_d(q))].       (1)

For an actual top phase tuple (alpha_d,r_d), let

    k_q(z)=#{d|C: alpha_d=q modT and z=r_d modd},
    h(0)=h(1)=0, h(k)=k for k>=2,
    M=sum_(d|C) U_d(alpha_d,r_d)
      +sum_(q modT,z modC) h(k_q(z))*v_z(q modb).

The exact joint charge J(u,v) is the maximum of M over all actual top phase
tuples, as defined by six-covering-2's cited joint-top result. It is a charge
with class multiplicity, not union mass or a maximum over phases admitting
a covering.

**Coupled coarsest lemma.** For every such tuple, M<=G_mix(u,v), hence
J(u,v)<=G_mix(u,v).

Proof. Let q0=alpha_1 modT be the coarsest B class's block. The coarsest
class is active at every z. In this block put r(z)=k_q0(z)-1. At r=0 the
useful periodic charge is zero, and at r>=1 it is (r+1)v<=2rv. Thus its
periodic charge is at most twice the sum of the other top v footprints
whose blocks are q0. In every other block h(k)<=k, so its charge is at most
the sum of the active top v footprints, each counted once. The coarsest
u footprint is at most A_1(q0). Each other resource whose block is q0
contributes at most I_d(q0); a resource in another block contributes at
most O_d(q0). Importantly, its u and v footprints are maximized at the
same alpha,r. Sum these maxima and then maximize q0 to obtain (1). This
loses compatibility among different resources, so no attainment assertion
is made.

## Comparison and endpoints

Put H_d(t)=max_r V_d(t,r), M_d=max_t H_d(t), and use the earlier pure bound

    G(v)=max_(t modb) sum_(d|C,d>1) max(M_d,2H_d(t)).

Then

    J(u,v)<=G_mix(u,v)<=sum_(n inS) C_n(u)+G(v),                  (2)
    G_mix(u,0)=sum_(n inS) C_n(u),
    G_mix(0,v)=G(v).                                            (3)

For (2), A_1(q)<=C_B(u), I_d(q)<=C_(Bd)(u)+2H_d(q modb), and
O_d(q)<=C_(Bd)(u)+M_d. Apply these bounds at the same q in (1).
For the first endpoint, E_d=I_d is the maximal u footprint in its block.
The maximum of the inside and outside possibilities is C_(Bd)(u),
independent of q; maximizing A_1 gives C_B(u).
For the second, E_d(q)=H_d(q modb) and I_d(q)=2H_d(q modb). If a maximizer
of M_d occurs at a block other than q, O_d(q)=M_d. Otherwise all global
maximizers are at q and I_d(q)>=M_d. Therefore
max(O_d(q),I_d(q))=max(M_d,2H_d(q modb)), including T=1. Every t modb is
represented by a q modT, proving the endpoint.

There is no uniform comparison with sum_S C_n(u+v). Ordinary weighted
counting remains a separate valid bound, and the smaller of the two
valid top bounds may be used.

## Mixed pair correction, with reviewer attribution

Designate distinct divisors p,r>1 of C, without requiring coprimality or
primality. For each block q and cofactor phase a define

    A_d(q,a)=max_(alpha=q modT) U_d(alpha,a),
    L_(a,s)(t)=sum_(z=a modp,z=s modr) v_z(t).

Empty intersections have mass zero. Put t=q modb and

    Z_(p,r)(q)=max_(a modp,s modr)
        [A_p(q,a)+A_r(q,s)+2V_p(t,a)+2V_r(t,s)-L_(a,s)(t)],
    P_(p,r)(q)=max{O_p(q)+O_r(q), I_p(q)+O_r(q),
                  O_p(q)+I_r(q), Z_(p,r)(q)},
    G_mix_pair(u,v)=max_q [A_1(q)+P_(p,r)(q)
                    +sum_(d|C,d>1,d not in{p,r})max(O_d(q),I_d(q))].

Then J<=G_mix_pair<=G_mix, and (4) remains valid with G_mix_pair. The four
cases record whether each designated resource is in the coarsest block.
If both are inside, at a point where both are active there are k>=2 other
classes, and h(1+k)=k+1<=2k-1. Subtracting this designated pair intersection
once is therefore safe. Elsewhere use the original2k bound. Their u
footprints retain their actual cofactor phases, then maximize their
B-coordinates within q. The other three cases charge inside resources
twice and outside resources once. This is exactly six-reviewer-5's pair
charging, now keeping the unrestricted footprints at those phases.
The intersection mass is nonnegative, so the both-inside maximum is at
most I_p(q)+I_r(q); all four cases are bounded by the old independent
maxima. No other pair deductions are added. In particular, summing every
pair overlap is not valid without proving a shared deduction budget.

The pure-u endpoint still equals sum_S C_n(u). For u=0 this mixed pair
relaxation is at most the reviewer's pure pair budget: O_d(q)<=M_d and
the inside maxima and intersection terms coincide with that formula.
If T/b>=2, excluding one q still leaves every t modb represented outside,
so O_d(q)=M_d and the pure-v endpoint equals the published pure pair budget.
No unconditional equality is needed or asserted when T=b.

## Affine necessary inequality

Every completion satisfies

    D(u+v)-sum_((m,a) inA) Phi_(m,a)(u+v)
        <=sum_(n inR outsideS) C_n(u+v)+G_mix(u,v).              (4)

Known footprints are summed with multiplicity; the demand on the left
can be negative. No union correction, truncation of multiplicities or
replacement by uncovered demand is used. When u vanishes on A this
reduces to the cited peer's known-v-footprint convention.

Here is the primitive-block covering argument. On Z/rho, suppose g is
a sum of functions each invariant under shift rho/ell for some prime
ell|rho. If g>=0 except possibly at one point, then sum_j g(j)>=0.
The commuting product of operators (I-shift_(rho/ell)) annihilates g.
Its subset shifts are distinct: modulo a prime in a symmetric difference,
only that prime's rho/ell term is nonzero. At a possibly negative point
j0, the annihilator identity writes -g(j0) as the sum of nonempty even
subset values minus the sum of odd subset values. All other values are
nonnegative, so the even-subset values compensate any negative value.
Constants have the required invariance as well.

Adjoin arbitrary phases for any missing top resources, preserving distinctness
and covering. Fix z modC and a primitive B-block alpha=q+Tj, j modrho.
The weight v_z is constant there. Every prescribed class and every used
outside resource has proper B-part m=gcd(n,B)<B: every full B-part divisor
belongs to S, whose members are unplaced. Choose a prime ell|B with
m|B/ell. Its active indicator is invariant under j-shift rho/ell, changing
alpha by B/ell while keeping z fixed.

If at most one top class is active in this block, subtract constant1 from
the sum of known and used outside indicators. Covering makes the difference
nonnegative except possibly at the single top point. The sign argument
shows that known and used outside footprints alone meet the whole block's
v demand. With k>=2 active top classes, ordinary counting instead charges
their k v footprints. Summing all blocks gives

    D(v)<=sum_A Phi(v)+sum_actual_used_outside Phi(v)
                       +sum_(q,z)h(k_q(z))*v_z(q modb).

Ordinary counting gives D(u)<=sum_A Phi(u)+sum_used_outside Phi(u)+sum_top Phi(u).
Add them, combine each outside u+v footprint at its same actual phase
before taking C_n(u+v), apply the coupled coarsest lemma and add nonnegative
unused outside capacities. Move the known footprints to the left. This
proves (4). The general theorem permits nonnegative real weights; the
implementation intentionally uses exact nonnegative integers.

## Strict component and limits

At B8,C3,b2,N24, take u to be1 at ordinary residues0 and16, and0 elsewhere;
take v(x)=1 for odd x and0 for even x. Then the unrestricted u is not
bC-periodic. The top resources8 and24 are both eligible at minimum eight.
Complete actual phase enumeration gives

    J=G_mix=3 < sum_S C_n(u+v)=4 < sum_S C_n(u)+G(v)=5.

At blockq0, A_1=2 and each inside/outside alternative is1, giving3. At
odd blocks A_1=0 and the inside alternative is2. At the other even block
A_1=0 and the outside alternative is1. The ordinary coarsest footprint
is3 and the finest is1; the separate u total is3 and G(v)=2. This is a
top-charge component comparison, not a covering witness or new24 exclusion.

The prior attributed N36 fixture, B9,C4,b3, rows
(2,0,0),(0,3,0),(2,0,0),(0,0,0), with u=0, has J=10<G_mix=12.
It reproduces our7516 component input and shows the relaxation need not be
attained. That example also has ordinary top total11, so G_mix is not
uniformly stronger than ordinary counting.

A further mixed component at B4,C15,b2,N60 uses u=1 at ordinary residue0
and0 elsewhere, and v the odd-residue indicator. With the designated
cofactor pair3,5, complete phase enumeration gives

    J=G_mix_pair=17 < G_mix=18 < separate22 < ordinary24.

The pure review-pair budget on this v is17; adding the four independent
u capacities would give21, still above the coupled17. This is a new
mixed component comparison, not a new pair charging mechanism, covering
witness or global exclusion. Its top modulus4 differs from the assigned
minimum-eight target and is used only as a general-lemma control.

Given ordinary N-vectors, the profiles can be computed with
O(BC*tau(C)+T^2*tau(C)) arithmetic operations and O(BC+T*tau(C)) working
storage, by computing all U_d phase buckets and block maxima, then O_d.
For the designated pair, an additional O(T*p*r) arithmetic operations and
O(T*(p+r)+b*p*r) storage suffice to retain the phase profiles and intersections.
No set partitions or simultaneous top phase tuples are enumerated by the
optimizer. Its complexity is polynomial in these explicit dimensions;
no claim of polynomial complexity in the bit length of N is made.

The checker independently enumerates267000 complete actual phase tuples
for27 fixed integer weight pairs, directly using physical class points
and their primitive-block occupancy. It checks both endpoints against
ordinary phase populations, the strict and nonattainment components,
240 affine controls on a genuine small cover, including60 using a
noncoprime designated pair and T=1, overlap of known classes and weights
positive on them, and15 malformed hypotheses. The
small positive cover has minimum2; it is only a validity control.
Zero components are permitted. These finite controls validate the code;
the universal argument is the written proof, not extrapolation.

No LP, private43200 forest, solver, graph query, large proof corpus or
external covering certificate is required. The compact input.json is a
byte-pinned attributed copy of the7516 fifteen-box input, SHA256
bf4d3deb56fa173a875a816aef6831a6aebff54b8bfdb441898137a5b96e1b96.
The new generic12-resource implementation reproduces six-reviewer-5's
pair-corrected43200 values22295,596075 and gap925 with u=0. This is an
attributed reproduction of that reviewer's result, not a new exclusion.
Written proof, Python integer
arithmetic and source inspection remain trust boundaries. No mixed-model
43200 discovery run has yet used this relaxation. The previously published
43200 prefix certificate is not altered or claimed again.

Contextual primary literature, retrieved live2026-09-30:
[Zhang–Zhang minimum-seven context](https://arxiv.org/html/2607.19029) and
[HKLT pure235 Problem3](https://arxiv.org/html/2605.18644). Neither is a proof
premise or a claim that the exactly-eight target is solved.
