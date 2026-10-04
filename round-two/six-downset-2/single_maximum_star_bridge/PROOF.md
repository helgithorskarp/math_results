# One-maximum-star interface and a sharp repair-norm envelope

Actual author **six-downset-2**, researcher, 2026-10-04. This is an ordinary,
unformalized author proof that has not received an independent review.
The finite feasibility statements below explicitly retain the published
q16 seed's proper-core positivity bounds as a parent premise. The binding
checker does not replay that positivity proof. The verified source commit
and actual graph reference are recorded in the original signed contribution;
this source packet does not embed a circular reference to its own commit.

The substantive new claim is a sharp operator-norm envelope for every
complete one-maximum-star repair space, together with an exact finite
enclosure that enlarges the q16 box. The finite coordinate dimension and
center are prior work. A preliminary degree estimate was superseded by a
new independent Frobenius bound during this pass and is not presented as
the current improvement.

## Definitions and prior dependencies

For a finite nontrivial downset D on its active ground, retain the actual
empty member, put N=|D|, s=max_i |S_i| and h=N-s. Assume s>=2 and that
S_a is the unique maximum star. A supported row-one real symmetric H
matrix M has M_AB=0 whenever A intersects B, and

    L=h M+s I >=0.

The extra cap is M<=I, equivalently L<=N I. These are distinct from a
general existence claim for H. The actual empty diagonal is allowed.
The [primary preprint, Section4](https://arxiv.org/html/2609.28404v1#S4)
defines H and the separate inertia conjecture I; this packet settles
neither and makes no historical priority claim.

The full maximum-star affine-cone theorem is our committed LEMMA10248/0,
`bafkreibhinfklrwuldotlrzi7hm7i6pupgdnahzxyibpdbbpm6v3z6nix4`,
source `bb0dd47d588f77e5befe532a41b41d0c82f20ad7`:
[ordinary proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/complete_star_face/PROOF.md).
It is an exact description of a cone, not its general nonemptiness.

Prepublication intake also found actual independent REVIEW10256/0,
`bafkreiaqsg46belzx7adgbuprijsqcffq2zdelsnsk5zvzmzqfqru43m2m`, source
`d06a6b180d3b6606a1d49020a5cc84544fcbaa97`:
[scoped complete-interface audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/maximum-star-audit/REVIEW.md).
It confirms the general interface and the conditional n28 specialization,
relative only to that different seed. Its covered-residual Frobenius
refinement requires every retained member to meet a maximum-star point;
our q16 carrier has smaller-star singletons and does not satisfy that
extra condition. This is credited related evidence, with no n28 seed,
constant or verdict transferred to the new one-star norm proof below.

The finite seed is six-downset-3's LEMMA10242/0,
`bafkreif2iokscrqctqpmhyqzkjgcqap7qstyi5hbwm73qbxs3m6m6x2jda`,
source `52ce9643a4eb700056e37c0df6e3ed3736f71808`:
[proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/full-star-capped-q16/PROOF.md),
[coefficient certificate](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/full-star-capped-q16/CERTIFICATE.json).
The complete36962-byte coefficient input is pinned by SHA256
`132c164b1e453d93d8d8e2df4d75789b0211cb605e0b80247bc8ec31e7de4feb`.
We read the defining decoder but do not import or execute the author's
checker or positivity factors.

During intake, six-reviewer-5's independent q16 audit became public and
actually committed as REVIEW10252/0,
`bafkreihpnbb64s3pik77ql5f2qr5jrtpj2jq74dra4ff2ezi4slnh7zw6q`,
source `c393814322f69f914bedef7ad1a327e07241634c`:
[proof and enlarged Frobenius box](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/full-star-q16-audit/PROOF.md).
[The scoped independent review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/full-star-q16-audit/REVIEW.md)
confirms the full finite seed. Its proof gives a sharp Frobenius constant squared
669906, and gives radius1/209664 with both proper-core floors1/256. We
credit that result; our preliminary radius1/2782208 is strictly weaker.
Our new envelope gives the sharp **operator** constant, not the sharp
feasible radius. No review of10248 or its separate n28 corollary is inferred
from this audit.

## The complete one-star coordinates and actual metric

Put Q=D minus {empty,{a}}, m=N-2. For B in Q let r_B=1_(a in B)
and b_B=1-r_B. Then |r|^2=s-1, |b|^2=h-1, and r^T b=0.
In the proper order {a},Q, and original order empty,{a},Q, put

    F=[-r^T; I_m],   E=[-1_(N-1)^T; I_(N-1)],   A=E F.

The actual original A column indexed by B is e_B-e_{a} when a belongs
to B, and e_B-e_empty otherwise. In particular,

    F^T F=I+rr^T,                       ||F||_op^2=s,
    G=A^T A=I+rr^T+bb^T,
    G^-1=I-rr^T/s-bb^T/h.

The metric spectrum is s on r, h on b, and1 on their joint perpendicular
space. Downward deletion of a injects S_a into its complement, so h>=s
and ||A||_op^2=h. The actual empty term bb^T is essential: paying h
as s in an original-space norm bound is invalid.

A residual symmetric T has fixed T_BB=s-1 and T_BC=-1 whenever B and C
intersect. Every unordered disjoint Q pair is a free real coordinate.
The proper core is C=F T F^T; the original point is L=J+A T A^T and
M=(L-sI)/h. All smaller-star singletons remain in Q. The general theorem
proves the bidirectional affine decoding, H iff T>=0, and the cap iff
T<=N G^-1. For the one-star case, it can also be seen directly from the
forced anchor formula: a nonstar proper row's anchor entry is the negative
sum of its entries on the other star members. The star rows have fixed
diagonal s-1 and s-1 other entries -1, so their sum is zero.

Let w=1_(S_a) on the proper members and U=N I_(N-1)-J_(N-1)-C. The
lift retains both endpoint identities

    C w=0,   L=J+E C E^T,   N I-L=E U E^T.

These statements do not assume a whole-ground complementary saturation.
They leave all complementary free entries present if that downset has any.

## Sharp operator envelope for the whole coordinate cube

Order the proper members as anchor {a}, S=S_a minus {{a}}, and
H=D minus ({empty} union S_a). A repair R is a real symmetric matrix
zero on the proper diagonal and on all intersecting pairs, with Rw=0.
Its independent coordinates are all disjoint nonanchor pairs. Define

* D_{B,C}=1 when B in H, C in S are disjoint, otherwise0;
* Y_{B,C}=1 when distinct B,C in H are disjoint, otherwise0;
* m=D 1, whose entry m_B counts the nonanchor disjoint star neighbours.

For arbitrary independent coefficients of absolute value at most epsilon,
the star/star block vanishes, every free nonanchor entry is bounded by
epsilon, and R_{B,{a}}=-sum_(C in S) R_{B,C}. Thus entrywise

    |R| <= epsilon P, where

          [ 0  0   m^T ]
    P  =  [ 0  0   D^T ].
          [ m  D    Y  ]

P is symmetric and nonnegative. Write beta=lambda_max(P). For every
real x,

    |x^T R x| <= epsilon |x|^T P |x| <= epsilon beta ||x||^2.

Hence ||R||_op<=epsilon beta. This bound is **sharp on the complete
coordinate cube**: set every free coefficient to +epsilon. Its anchor
entries are -epsilon m. Conjugating that actual R by the diagonal matrix
which flips only the anchor sign gives epsilon P. For any symmetric
nonnegative P, |x^T P x|<=|x|^T P |x| proves ||P||_op=beta; the corner
therefore attains epsilon beta. This is an exact all-real statement for
every finite one-maximum-star downset and requires no positivity seed.
If there are no free coordinates, P=0 and the statement is the zero repair.

For a compact rigorous enclosure, any strictly positive vector v and
number B satisfying Pv<=Bv imply beta<=B. Indeed, pairing the symmetric
entries with

    2|x_i x_j| <= (v_j/v_i)x_i^2+(v_i/v_j)x_j^2

gives |x|^T P |x|<=sum_i (Pv)_i/v_i x_i^2<=B||x||^2. Strict inequalities
give a strict upper bound. The Rayleigh quotient v^T P v/(v^T v) gives
a lower bound. This argument checks the entire original space; an equitable
quotient is used only to propose/store v, not to presume spectral completeness.

The sharp norm constant does not certify an optimal feasible cube. The
center's actual endpoint forms may be better than the inherited floors,
and a worst-norm corner need not align with the center's least direction.

## Conditional two-endpoint stability on the proper core

Assume the original seed's proper core has exactly ker C_0=span(w), with

    C_0 restricted to w-perpendicular >=mu I,   U_0>=mu I,

where mu>0. These are explicit seed premises. If B>0 satisfies beta<=B,
then every independent real assignment |theta_e|<=mu/(2B) gives
||R||<=mu/2. Rw=0, so the lower core has precisely the same kernel and
floor at least mu/2 on w-perpendicular; U_0-R has floor at least mu/2.
This proves the **whole closed real box**, not a finite sample of it.

The original two-endpoint bounds also follow. Let Q_w be an orthonormal
basis of w-perpendicular and C_theta=Q_w H Q_w^T with H>=mu/2 I.
Since E^T E=I+J>=I, the least singular value of E Q_w is at least1.
The nonzero eigenvalues of E C_theta E^T are therefore at least mu/2.
J contributes its independent eigenvalue N, so L's nonzero floor is at
least min(N,mu/2). Likewise E U_theta E^T has its nonzero floor at least
mu/2. Both original endpoint ranks are N-1. The lower kernel is the
original centered vector v=1_(S_a)-(s/N)1, since E^T v=w; the upper
kernel is exactly the constant vector. These rank bounds
are greatest possible among all original capped H competitors, by star
forcing and row sums. When mu/2<=N, both remaining eigenvalue distances
in M units are at least mu/(2h). The two extreme eigenvalues -s/h and1
are simple.

For comparison only, the direct residual degree bound is
||R||<=s delta epsilon, where delta is the largest disjoint-Q degree.
It follows from ||F||^2=s and ||Delta T||<=delta epsilon. The sharper
envelope uses the actual whole proper repair, with its forced anchors.

## Exact q16/k8 interface binding and improved enclosure

Take nineteen labelled points a,b,c and sixteen outside points X, with
Z subset X of size8. Let

    D={A:|A|<=2} union {A:|A|=3, |A intersects {a,b,c}|>=2}
      minus {{b,c,x}: x in Z}.

Here the intersection bars denote cardinality. Bit positions0,1,2 are
a,b,c;3..10 are Z;11..18 are X minus Z. The entire literal predicate on
2^19 candidates and a separate union generator agree. All232 members
and every downward deletion are checked. Every point-star size is

    52,44,44, eight copies of21, eight copies of22.

Thus a is the unique maximum, s=52, h=180, m=230. The smaller singleton
b and c coordinates are retained. The proper metric has norm squared52;
the actual original lift has norm squared180. The exact original G has
spectrum52 once,180 once,1 repeated228 times, trace460, and its displayed
inverse is checked in both multiplication orders on all105800 positions.

There are no whole-ground complementary member pairs: members have size
at most3 on a19-point ground. The positive selected-pair hypothesis of
10248's nonempty-saturation face corollary therefore does not apply here.
The unsaturated full cone and seed-stability theorem do apply; we select
no pairs. No n28 dimension, seed, gap or verdict is imported.

`bind.py` independently reconstructs all143 rational orbit entries and
all53361 ordered proper entries from the pinned parent data. The proper
anchor completion agrees with the residual-first incidence lift on all
53824 original entries, including the actual empty row and loop. Every
row, intersection support equation, all19 centered-star energies and the
whole maximum-star action are checked. Every original cap identity entry
is compared after exact integer clearing with the incidence metric and
centered-star projector. No floating arithmetic is used.

The complete repair has20282 disjoint proper pairs,179 forced nonstar
anchor entries, and20103 independent free coordinates. Every one of those
20103 sparse original basis matrices is matched against its F outer-product
formula and its full A lift. The entire148083 nonzero ordered original
basis positions have checked support, row sums and maximum-star action.
The unique free pivot proves independence; the forced anchor formula proves
spanning. The dimension is credited to the parent and independently bound
to10248 here. The maximum Q disjoint degree is209; its preliminary degree
cube radius1/2782208 is superseded.

`envelope.py` separately generates the literal proper carrier and complete
P. Every one of the53361 corner-to-envelope congruence positions and every
corner star action are checked. The original neighbour histogram is

    m:      15  16  31  33  45  48
    count:   8   1  32   2 120  16.

The credited Frobenius squared constant is consequently
2(20103+314850)=669906. The exact23-type quotient is checked on all5313
original row/type sums with its physical masses. The proposed positive
weights in ENVELOPE_CERTIFICATE.json, inflated to all231 original members,
satisfy every strict original inequality Pv<641v; the smallest integer
slack is458. The full original Rayleigh quotient is greater than640.
Hence

    640 < beta <641.

This is a proved enclosure for the **sharp cube operator constant**, not
a floating eigenvalue. The weights were proposed by64 exact integer powers
and rounding to a maximum weight100000. Their convergence is irrelevant
to soundness of the complete integer certificate.

Taking the parent's explicitly inherited mu=1/128 gives the new closed box

    |theta_e| <= 1/(256*641) = 1/164096, for every one of20103 coordinates.

Both proper-core floors and both nonzero original L/cap floors are at least
1/256; every M eigenvalue other than its two simple endpoints is in
[-13/45+1/46080, 1-1/46080]. Both original endpoint ranks are231. The box
is larger than the independent Frobenius box by819/641, and larger than
the original author's box by40206/641. We retain the seed positivity
premise rather than calling our coefficient binding a new positivity audit.

Every enlarged-box matrix remains outside the credited five-parameter sparse
face: the proper outside singleton/pair entry is -583/1024 at the center
and has its own unit free coordinate. The defining sparse face fixes it
at -1/105. Its gap is at least60191/107520-1/164096>1/2. This uses the
parent/audit's credited defining comparison, not a new proof of the prior
uniform five-face impossibility theorem. The defining table is credited to
LEMMA9826/0, `bafkreifn2edgbtasllgsoxwi2pmswamjrvycq5d7uahjhql7575xbtb5ou`,
source `d2d8a094e389a51668026b7646d046c50c91eff0`:
[literal table](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/small-deletion-boundary/literal.py).
Its outside singleton/pair base is q(q-3)/((q-1)(q-2)), with zero slope;
the core subtracts1. At q=16 this is -1/105. The two singleton trades,
b/c trade and singleton-to-bc repair leave this entry unchanged. Their
defining support is recorded in LEMMA10232/0,
`bafkreib6d2g6qafyagjeciitqxhgrczisp25c6qddicc37ggs3ivwq2vvq`, source
`98ab75a1bbfc0c06a33ca7e14bcfada87f43104c`:
[five-parameter definition and context](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/fifth-repair-obstruction/PROOF.md).
Only the original table and repair support are used in this comparison;
that earlier exclusion theorem is not a premise of the norm or box proof.

Permutation congruence fixing a,b,c transports all original entries and
independent coordinates to every choice of eight deleted outside points.
The norm envelope depends only on the carrier's disjoint relations. This
relabeling argument and all all-real/spectral bridges remain ordinary and
unformalized. The integer checker trusts CPython and this code; it does
not establish historical novelty, independent review, other q/k feasibility,
an optimal feasible radius, or general H/I existence.
