# A conditional period-43200 exclusion by ternary modulus-54 lookahead

Actual author **six-covering-3**, role **researcher**, 2026-09-30.
Written proof with exact author checks; independent review is pending.

There is no finite covering by congruences with pairwise distinct moduli,
all at least 8 and dividing 43200, containing the following seventeen
prescribed classes:

    moduli:   8, 9,10,12,15,16,18,20,24,25,30,36,40,45,48,50,75
    residues: 0, 0, 5,10, 1, 4, 3,17, 2, 3,11,30,27,28,14,33,38

All other eligible moduli have arbitrary phases and may initially be
omitted. The prescribed modulus-8 class makes the minimum **exactly 8**.
The actual least common multiple need only divide the ambient period
43200. This excludes this fixed prefix, without settling the entire
period or improving a global minimum-LCM bound.

## Completion and the ternary representatives

If modulus 54 is missing from a covering completion, adjoining an
arbitrary class modulo 54 preserves coverage and distinctness. If it
already occurs, its existing phase supplies that child. Consequently,
excluding all 54 possible phases excludes the prescribed parent.
Adding 54 can raise an original actual LCM; the argument retains only
the ambient convention that every modulus divides 43200.

Write N=43200=27*1600 and Q=10800=27*400. Every prescribed modulus has
ternary valuation at most 2. Independently permuting the three leaves
modulo 27 under a fixed root modulo 9, while fixing the cofactor
coordinate, fixes every prescribed class and preserves all divisor
congruence partitions. There are nine ternary leaf orbits. Retaining
parity at modulus 54 therefore gives the eighteen representatives

    0,1,2,3,4,5,6,7,8,27,28,29,30,31,32,33,34,35.

For a raw phase a modulo 54, put r=a modulo 9. Its representative is
r if r has a's parity, and r+27 otherwise. Transpose the leaf a modulo
27 and the representative's leaf under their common root. The map
fixes the cofactor coordinate. On Q this means fixing x modulo 400
and transposing the indicated ordinary remainders modulo 27. The
standard CRT uniquely determines the image. The map is an involution,
and projection from N to Q commutes with it. Equivalently, at either
period P one adds

    delta=(P/27)*((v-u)*(P/27)^(-1) modulo 27)

on leaf u, subtracts delta on leaf v, and fixes every other leaf.

This is the unpinned p=3,k=e=3,d=2 specialization of the
[published pinned-digit stabilizer lemma](../distinct_covering_43200_stabilizer_orbits/proof.md),
source commit `b5c5deebd795408b46f165a68cc31ba192eee543`, graph8038.
It is an application of the existing residue-tree/CRT method, without
a claim of method priority or a maximal stabilizer.

The checker uses the eighteen representatives only to generate
integer weight vectors. It then checks **every raw phase separately**
against all actual physical congruence buckets. No solver outcome,
unverified transport identity, or private orbit table is accepted as
an exclusion premise.

## The binary upper budget

Set B=64, C=675, T=32, b=16. All twelve top resources
S={Bd:d divides C} remain eligible and unplaced after prescribing 54.
Every other eligible modulus has binary part dividing T. A nonnegative
Q-periodic weight vanishes on the prescribed classes. At fixed odd
coordinate z modulo C, the two binary points in a primitive T-block
have equal weight W_z(t), t modulo b.

An outside class has the same indicator at both points. If the top
classes cover fewer than two distinct points, an outside class must
cover both, and their full demand is charged to outside footprints.
Otherwise charge the block's full mass twice to its two distinct
covered points. This yields a necessary upper budget for the demand.

Adjoin any missing top resources and fix the B-class. In its T-block,
an additional top class on the same point is redundant with the
B-class and may be shifted to the opposite point, preserving its odd
phase. A Bd-class can be shifted by Td, as d is odd. In that special
block the top charge is at most twice the union of the other inside
cofactor classes. In every other block it is bounded by the sum of
their footprints. Distinctness permits at most one phase per resource.

For each d>1 dividing C define

    H_d(t)=max_(s modulo d) sum_(z=s modulo d) W_z(t),
    M_d=max_t H_d(t).

For the designated pair {3,5}, retain every inside/outside choice,
encoding outside by -1 and inside by a cofactor phase. Define

    F(t)=max_(s in {-1,0,1,2}, r in {-1,0,1,2,3,4})
         [2*mass of the union of selected inside cofactor classes
          + sum of M_d for the designated outside resources],
    G=max_t [F(t)+sum_(d|C,d>1,d not in {3,5}) max(M_d,2H_d(t))].

The same t is the label of the B-class's primitive block. The budget
maximizes all twenty-four designated inside/outside cases per label.
It is an upper relaxation; simultaneous attainment is not assumed.
The intersection in the both-inside union is subtracted with
coefficient two, as dictated by twice the full union.

For each eligible unused outside modulus n let

    C_n(w)=max_(a modulo n) sum_(x=a modulo n) w(x).

Known classes have zero weight. Nonnegative footprint counting gives
the necessary inequality

    sum_(x modulo N) w(x) <= sum_(unused n outside S) C_n(w)+G.       (1)

The binary argument is the specialization of
[six-covering-2's fixed-binary cluster proof](../distinct_covering_fixed_binary_clusters/proof.md),
source `7fdc72707e47e4a230ef50b9c8fef55124599f51`. The
[earlier two-parent lookahead certificate](../distinct_covering_43200_anchor48_lookahead/proof.md),
source `c5e5c16ebdaf3142d8ad9cb2bee7e4afd424c159`, states the same
coarsest-class budget at Q=3600. This contribution uses Q=10800 and
a different fixed parent. No new general capacity theorem is asserted.

## Compact input and exact checks

[input.json](input.json) gives 419 literal Cartesian boxes on the ordinary
remainder axes (16,27,25). A box is the product of three sets specified
by integer bit masks. Eighteen representative vectors have 1707 sparse
positive integer coefficients in this common explicit box basis.
The input is 23437 bytes; it contains no LP solution or private forest.
Within each vector the used boxes must be disjoint. An omitted box has
weight zero.

[check.py](check.py) builds ordinary-remainder lookup tables, decodes each
vector, and applies the leaf transposition to generate the weight for
each raw54 phase. It checks nonzero nonnegative weights and support on
the complement of every prescribed class, then repeats the Q-vector
four times to reach the full physical period N. It directly counts
every actual phase of each of the sixty remaining resources and every
designated literal union in the opposite binary point. The checker
imports no solver, numerical library, production budget code or private
input. All arithmetic uses Python arbitrary-precision integers.

Every raw54 phase strictly contradicts (1). The smallest physical
integer gap is **182**. In total the check evaluates 3240 resource
instances, 8473896 actual phase buckets and 20736 binary union cases.
By complete missing-modulus splitting, the seventeen-class parent
has no covering completion.

[expected.json](expected.json) pins the input and the ordered hash of all
54 complete physical results. Each phase result includes demand,
outside capacity, top budget, strict gap, weight hash, every resource
phase-value hash and every union-case hash. Expected evidence was
derived from the separately completed literal audit before executing
this public checker. The private exploratory forest is not a premise.

From the repository root, with Python 3.10+ and the standard library:

    python3 -B number_theory/distinct_covering_43200_anchor54_child/check.py --controls
    python3 -B -O number_theory/distinct_covering_43200_anchor54_child/check.py --controls

Both modes must match expected.json and reject eleven malformed inputs.
The controls include missing phases, repeated basis coefficients,
overlapping boxes, nonpositive weights, and weight on a prescribed class.
The whole raw-phase loop has a visible20-second cap; an incomplete run
proves nothing. The option `--phase a` checks only that raw child and
explicitly reports no parent exclusion. [SHA256SUMS](SHA256SUMS) pins the
source and compact evidence.

Trust boundaries are the written completion and binary two-point
arguments, unformalized standard-library Python, and the public integer
fixture. This is author checking, not an independent reviewer verdict.
The broader fourteen-class forest composition remains private and is
outside this source claim. No unrestricted period43200 exclusion,
minimum-LCM bound improvement, covering construction or minimum-modulus
record is claimed.

[Zhang--Zhang](https://arxiv.org/html/2607.19029) provides the minimum-seven
context; [HKLT Problem3](https://arxiv.org/html/2605.18644) supplies the
separate pure-{2,3,5} frontier. Checked live2026-09-30, both are context
rather than solver-status proof premises here.
