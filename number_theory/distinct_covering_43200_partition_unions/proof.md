# A conditional period-43200 exclusion using disjoint union groups

Actual author **six-covering-3**, role **researcher**, 2026-10-01.
Written proof and exact author checks; independent review is pending.

There is no finite covering by congruences with pairwise distinct moduli,
all at least eight and dividing 43200, containing these nineteen classes:

    moduli:   8,9,10,12,15,16,18,20,24,25,30,36,40,45,48,50,75,54,60
    residues: 0,0, 5,10, 1, 4, 3,17, 2, 3,11,30,27,19,14,33,13, 6,59

The minimum is **exactly eight** because the modulus-eight class occurs.
The actual least common multiple need only divide the ambient period
43200. All other eligible moduli have arbitrary phases and may be omitted.
This is a conditional exclusion, without a whole-period exclusion or a
new global minimum-LCM bound. It differs from the seventeen-class parent
in the [previous ternary certificate](../distinct_covering_43200_anchor54_child/proof.md).

## The necessary binary charge

Write N=43200=64*675, B=64, C=675, T=32 and b=16. All twelve top
resources S={Bd:d divides C} remain unplaced. All other divisors of N
have binary part dividing T. Let w be a nonnegative Q=10800=bC-periodic
weight vanishing on the prescribed classes.

Use ordinary CRT coordinates (alpha modulo B,z modulo C). In a
primitive block with alpha=q or q+T, the two points have equal weight
W_z(t), where t=q modulo b. Every non-top class has the same indicator
at both points. If the top classes cover at most one distinct point,
the non-top classes in a covering must cover both points; charge the
full block demand to their footprints. If the top classes cover both
points, charge at most their full mass 2W_z(t) to the top classes.
Ordinary nonnegative footprint counting therefore gives

    D_N(w) <= sum_(unused non-top n) C_n(w) + K,

where C_n(w) is the largest actual phase mass of modulus n, and K is
an upper bound for this distinct-point top charge. Known footprints
have weight zero.

Adjoin any omitted top resource, including B, if necessary. This
preserves coverage, distinctness and divisibility by N; an original
smaller actual LCM may increase. Fix the primitive block q0 of the
B-class. At that block the B-class covers one point for every z. A
Bd-class on that same binary point is redundant there; shifting it
by Td preserves its odd phase and moves it to the opposite point.
The B-class continues to cover all its previous points. Thus this
replacement cannot decrease the top charge or destroy coverage.

At q0 the top charge is bounded by twice the weighted union of the
OTHER inside cofactor cosets. At every other primitive block it is
bounded by the sum of the active top footprints. Define, for d>1
dividing C,

    H_d(t)=max_(a modulo d) sum_(z=a modulo d) W_z(t),
    M_d=max_t H_d(t).

An individual Bd-resource can be charged at most 2H_d(t) inside q0,
or M_d outside. The label t of the coarsest class is shared by all
inside terms. This is the pure periodic specialization of
[six-covering-2's fixed-binary cluster proof](../distinct_covering_fixed_binary_clusters/proof.md),
source `7fdc72707e47e4a230ef50b9c8fef55124599f51`, graph7633. The
[coarsest budget](../distinct_covering_coarsest_block_budget/proof.md), graph7685,
and [primitive-block proof](../distinct_covering_primitive_block_capacity/proof.md),
graph7420, are earlier campaign context. The binary argument above is
self-contained; no solver outcome or general sign lemma is omitted.

## Several disjoint union groups

Choose pairwise disjoint groups of cofactor resources

    P1={3,5,9,15}, P2={25,27}, P3={45,75}.

For each group Pj and label t, maximize over all choices s_d in
{-1,0,...,d-1}, where -1 means outside q0:

    F_j(t)=max_s [2*mass(UNION of the cosets z=s_d modulo d with s_d>=0)
                  +sum_(d in Pj with s_d=-1) M_d].

The necessary top upper budget is

    G_P=max_t [F_1(t)+F_2(t)+F_3(t)
               +sum_(d|C,d>1,d outside the groups) max(M_d,2H_d(t))].

Indeed, the union of ALL inside cosets has mass at most the sum of
the three group-union masses and the remaining individual masses.
Each outside resource occurs exactly once because the groups are
disjoint. Bound its footprint by M_d. Each group's actual assignment
is bounded by F_j(t), retaining the SAME actual coarsest label t.
Maximizing that label proves the displayed bound and hence

    D_N(w) <= sum_(unused non-top n) C_n(w) + G_P.                 (1)

The group maxima need not be simultaneously attainable: this is an
upper relaxation. Merging two groups cannot increase the same-vector
budget, since the mass of their combined union is at most the sum
of their union masses, with unchanged outside costs. In particular,
adding union groups in place of individual resources cannot worsen
the single-group bound. This is a direct regrouping of the existing
binary union argument, without a method-priority or exact-optimizer
claim. Independent pair deductions with overlapping resources would
require a different argument and are not used here.

## The compact certificate

[input.json](input.json) has **87 literal Cartesian boxes** on the
ordinary-remainder axes (16,27,25), with positive integer weights.
Each box specifies three bit masks and one weight. Within the vector
the boxes are disjoint; omitted points have weight zero. The input
is **2617 bytes** and contains no solver solution or private frontier.

[check.py](check.py) decodes those ordinary remainders directly, checks
every prescribed class, and repeats the Q-vector four times to reach N.
It counts EVERY actual phase of all 59 remaining resources. At each
label t, it evaluates every group assignment on physical points
x=t+T modulo B using literal union membership. All arithmetic uses
Python arbitrary-precision integers. No numerical library, production
budget, CRT interpolation, graph, ledger or private file is imported.

The exact physical totals are:

| Quantity | Value |
| --- | ---: |
| Demand D_N(w) | 39998116 |
| Non-top capacity | 36733316 |
| Grouped top budget G_P | 3264488 |
| Total capacity | 39997804 |
| Strict gap | **312** |
| Ordinary capacity, same vector | 40332004 |
| Only P1 retained as a union, same vector | 40009046 |

Thus (1) is strictly violated. The single-group comparator exceeds
the demand by 10930; the additional groups are necessary for strictness
of THIS vector. No assertion is made that the comparator admits no
different strict vector or that a floating optimum supplies such a proof.

The checker counts 156864 actual phase buckets and respectively
61440,11648,55936 union cases for the three groups:129024 in total.
[expected.json](expected.json) pins the full weight hash, actual phase
values hash, every group-case hash and the exact physical result.
Those values come from the separately completed physical audit; the
single-group comparison was also recomputed by ordinary progressions
before running the public checker. No private audit is a reader's premise.

From the repository root with Python3.10+ and the standard library:

    python3 -B number_theory/distinct_covering_43200_partition_unions/check.py --controls
    python3 -B -O number_theory/distinct_covering_43200_partition_unions/check.py --controls

Both commands must match expected.json and reject eleven malformed
controls, including wrong scope, repeated resources, overlapping boxes,
nonpositive weights and weight on a prescribed class. The full union
loop keeps a20-second cap; an incomplete run proves nothing.
[SHA256SUMS](SHA256SUMS) pins source and compact evidence.

Trust boundaries are the written two-point/grouping proof, unformalized
standard-library Python, and the compact integer input. These are author
checks, without an independent reviewer verdict. The private phase-60
forcing tables and broader fourteen-anchor composition are outside this
public certificate. No covering construction or minimum-modulus record
is claimed. [Zhang--Zhang](https://arxiv.org/html/2607.19029) and
[HKLT Problem3](https://arxiv.org/html/2605.18644), checked live2026-10-01,
provide primary context, rather than numerical proof premises.
