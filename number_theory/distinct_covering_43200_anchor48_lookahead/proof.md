# Two conditional period-43200 exclusions by modulus-48 lookahead

Actual author **six-covering-3**, role **researcher**, 2026-09-30.
Written proof and exact author checks; no independent review or priority claim.

No finite covering by congruences with pairwise distinct moduli, all at
least 8 and dividing 43200, contains either of the following two lists:

    moduli:   8, 9,10,12,15,16,18,20,24,25,30,36,40,45
    residues: 0, 0, 5,10, 1, 4, 3,17, 2, 1,13, 6,27,33
    residues: 0, 0, 5,10, 1, 4, 3,17, 2, 1,13, 6,27,38

Each row specifies one class for every modulus. Actual LCM may be any
divisor of 43200; the prescribed modulus-8 class ensures minimum exactly 8.
This excludes two fixed prefixes, not all coverings at this ambient period.
No numerical global or pure-{2,3,5} minimum-LCM bound changes.

The reusable step is a finite missing-modulus completion split. The
capacity inequality is the existing binary distinct-point/union mechanism
of six-covering-2, applied at period 3600. No new general capacity theorem
or optimized dominance is claimed.

## Missing-modulus completion

Let eligible moduli be a fixed finite set, and let a prescribed prefix
leave an eligible modulus d unplaced. Existence of a distinct covering
completion is equivalent to existence of a completion after adjoining
some class a modulo d, for one of all d raw phases a=0,...,d-1.
Indeed, an existing d-class supplies its phase. If no d-class exists,
adjoin any one: coverage and distinctness are preserved. A covering
containing an extended prefix is already a completion of the original
prefix. This uses no quotient or restriction on the other phases.

Take d=48. It divides 43200, is eligible, and occurs in neither prefix.
Thus excluding every one of its 48 phases excludes the stated parent.
The completion can increase actual LCM within the divisors of 43200;
it does not preserve a previously smaller actual LCM. The minimum stays
exactly 8 because the modulus-8 class is already prescribed.

## Binary upper budget used for each child

Set N=43200=64*675, B=64, C=675, T=32, b=16, Q=3600.
Every top modulus in S={Bd:d divides C} is eligible and unplaced,
even after adjoining 48. There are 12 such moduli. All other eligible
moduli have proper binary part dividing T. Each known class also has
proper binary part. Every chosen nonnegative integer weight w is
Q-periodic, hence bC-periodic, and vanishes on all 15 known classes.

At fixed odd coordinate z modulo C, a primitive binary block has the
two binary points q and q+T. They have equal weight W_z(q modulo b).
An outside congruence has the same indicator at both points. If top
classes cover fewer than two distinct points, outside classes must cover
both; otherwise charge the block's mass twice to those distinct points.
This yields full demand at most outside footprints plus the two-point
charge from top classes.

Adjoin any omitted top resources and fix the B-class. In its T-block,
any other top class on the same binary point is redundant with the
B-class and can be moved to the opposite point, preserving its odd
phase. A class modulo Bd can be shifted by Td because d is odd. The
charge in that block is at most twice the union of the other inside
cofactor classes. In other blocks it is at most the sum of their
individual footprints. Distinctness permits only one phase per modulus.

Write

    H_d(t) = max_(a modulo d) sum_(z=a modulo d) W_z(t),
    M_d = max_t H_d(t),                         d divides C, d>1.

Designate P={3,5}. For each t retain all inside/outside choices for these
two resources, using -1 for outside and a=0,...,d-1 for inside. Let

    F(t) = max_(s in {-1,0,1,2}, r in {-1,0,1,2,3,4})
           [2*mass of the union of the selected inside cofactor classes
            + sum of M_d for the designated outside resources],
    G = max_t [F(t) + sum_(d divides C,d>1,d not in P) max(M_d,2H_d(t))].

The common t is the label of the B-class's block. Non-designated inside
resources cost at most 2H_d(t); outside ones cost at most M_d. All
inside/outside choices and cofactor phases are enumerated, so G is an
upper relaxation without a simultaneous-attainment premise. For each
eligible unused outside modulus n put

    C_n(w) = max_(a modulo n) sum_(x=a modulo n) w(x).

Nonnegative footprint counting therefore gives the necessary condition

    sum_(x modulo N) w(x) <= sum_(unused n outside S) C_n(w) + G.       (1)

Known classes contribute zero. Missing unused moduli can still be
charged as extra nonnegative resources. For P={3,5}, both-inside charge
is twice the full union, so the intersection is subtracted with
coefficient two. It is not an arbitrary-multiplicity pair correction.

This argument is the specialization of
[six-covering-2's fixed-binary cluster proof](../distinct_covering_fixed_binary_clusters/proof.md),
source `7fdc72707e47e4a230ef50b9c8fef55124599f51`. The
[earlier conditional binary-union certificate](../distinct_covering_43200_binary_union_prefix/proof.md),
source `d0c2b6b515594067537e5035a7f42d13a4dc9690`, gives the same
coarsest-class argument at Q=720 for a different prefix. The
[primitive-block framework](../distinct_covering_primitive_block_capacity/proof.md),
source `234569d6f32f1ad96958ed3300050d9ce7acef1e`, is by six-covering-3.

## Compact input and complete exact evaluation

[input.json](input.json) specifies the two parents and eight nonuniform
integer weight vectors. For each parent, phases 14,23,38,47 modulo 48
use these vectors. A box consists of masks on axes (16,9,25) and a
positive integer value. The physical weight at x equals that value
when all three masks contain x modulo their respective axes; the boxes
are disjoint. No declared orbit or solver status is a proof input.

For every other phase, w is simply the indicator of points modulo Q
outside all 15 prescribed classes, lifted periodically to N. Thus the
other 88 vectors are generated from the public classes, rather than
stored in a proof corpus. All weights satisfy the required support.

After prescribing 48, exactly 63 eligible moduli remain unused: 12 top
and 51 outside. [check.py](check.py) evaluates every actual phase of
each resource over all N residues and every literal designated union
at the opposite binary point. There is no CRT inversion or solver.

| Parent phase modulo 45 | Raw phases modulo 48 checked | Smallest physical strict gap |
| --- | ---: | ---: |
| 33 | 48 | 144 |
| 38 | 48 | 92 |

For each parent the check evaluates 3024 actual resources, 7540944
actual phase buckets, and 18432 union cases. Every child strictly
contradicts (1). The missing-modulus completion lemma consequently
excludes each original fourteen-class parent.

[expected.json](expected.json) pins the input bytes and an ordered hash
of all 48 complete phase results for each parent. Each hashed result
includes the demand, outside capacity, top budget, strict gap, weight
hash, every resource phase-value hash and every union-case hash. This
evidence was assembled from the completed separate literal audits
before running the public checker. A private audit that reached its
time cap after 45 phases was resumed on the remaining three; the public
source now checks all phases directly, without that cached audit.

Reproduce with Python 3.10+ and the standard library, from repository root:

    python3 -B number_theory/distinct_covering_43200_anchor48_lookahead/check.py --parent 33 --controls
    python3 -B -O number_theory/distinct_covering_43200_anchor48_lookahead/check.py --parent 38 --controls

The summaries must match expected.json. Seven malformed variants reject,
including overlapping boxes and positive weight on a known class.
`--phase a` checks a single child and explicitly claims no parent
exclusion. A whole-parent run stops at the existing 20-second cap with
an error if incomplete; such a run supplies no parent exclusion.
[SHA256SUMS](SHA256SUMS) pins the five source/proof/evidence files.

Trust boundaries are the written completion and binary two-point
arguments, unformalized standard-library Python, arbitrary-precision
integer arithmetic, and the compact public input. The private forest,
LP runs and ledger are not dependencies of this certificate. No
independent reviewer verdict or historical-priority determination is
asserted.

[Zhang--Zhang](https://arxiv.org/html/2607.19029) supplies the
minimum-seven context; [HKLT Problem 3](https://arxiv.org/html/2605.18644)
is the separate pure-{2,3,5} target. Retrieved live 2026-09-30, they
are context rather than premises of these conditional cuts.
