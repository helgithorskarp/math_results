# The phase-42 covering prefix is excluded through moduli 100 and 108

Actual author **six-covering-3**, role **researcher**, 2026-10-01.
Written proof and exact author checks; independent review and formalization
are pending. The result is an explicit conditional certificate applying
credited CRT symmetries and the binary union bound. No priority for those
general methods is asserted.

Let N=43200. Prescribe these twenty congruences, pairing the moduli and
phases in the two rows:

    8,9,10,12,15,16,18,20,24,25,30,36,40,45,48,50,75,54,60,72
    0,0, 5,10, 1, 4, 3,17, 2, 3,11,30,27,19,14,33,13,33,29,42

**Conditional exclusion.** No finite distinct covering with moduli at
least 8 dividing N contains all twenty prescribed classes. Every unused
eligible divisor is allowed any phase and may be omitted, at most once.
The prescribed modulus 8 makes the minimum exactly 8. The actual LCM may
divide N; it is not required to equal N. This conditional exclusion does
not exclude the whole period or improve a global bound on L_min(8).

## Complete two-stage reduction

The prescribed moduli have LCM Q=10800. A hypothetical completion can
adjoin one arbitrary class at a missing modulus 100, since 100 divides Q.
This preserves coverage, distinctness, the minimum and its original
actual LCM. The same statement applies to missing modulus 108 after
prescribing a 100 class, since 108 also divides Q.

These are instances of the usual divisor-completion principle, described
in Section 2 of [Zhang and Zhang](https://arxiv.org/html/2607.19029).
Their minimum-7 computational exclusions are not premises here.

For the first split, write N=1728*25 and fix the cofactor coordinate.
Independently permute second-digit quinary leaves under each fixed root
modulo 5, fixing leaves {3,8,13} modulo 25. These are precisely the
quinary leaves prescribed by the 25,50,75 classes; each other known
modulus has quinary valuation at most 1. Every prescribed full class is
therefore fixed. Every divisor partition of N is permuted: its quinary
component is 1,5 or 25, and the coprime coordinate is fixed. A full class
maps to a full class at the same modulus. Thus these bijections preserve
coverage, distinctness, the modulus set and actual LCM.

There are eight quinary leaf orbits: three pinned singletons, {18,23},
and the five leaves below each of the other four roots. The binary
residue modulo 4 is fixed, giving 32 orbits at 100=4*25. Normalize each
unpinned leaf to the least unpinned leaf under its root, then combine
with the binary residue by CRT. The representatives are

    0,1,2,3,4,8,13,18,25,26,27,28,29,33,38,43,
    50,51,52,53,54,58,63,68,75,76,77,78,79,83,88,93.

This coordinate choice need not give the least integer in its orbit.
The transport swaps the raw leaf with the target under their common
root. Thirty representatives have strict weight certificates below.
The remaining raw phases {23,43,73,93} normalize to representatives
43 and 93, each of which is excluded by a complete missing-108 split.

For that second split, write N=1600*27 and fix the cofactor coordinate.
At the second ternary digit fix nodes {0,1,3,6} modulo 9 and permute the
remaining siblings {4,7} and {2,5,8}, keeping the third digit fixed.
Independently permute third-digit leaves below every node modulo 9,
fixing leaf 6 modulo 27. Every prescribed class with a factor 9 has
its second-digit node pinned; the only full 27 leaf is 6, prescribed
by 54:33. A class with ternary valuation at most 1 sees a fixed root.
The 100 class is fixed since 100 divides the cofactor 1600. Every one
of the twenty-one prescribed classes is fixed at either 100 phase
43 or 93. Every divisor partition is preserved as in the first split.

The seven ternary leaf orbits are

    {0,9,18}, {1,10,19}, {3,12,21}, {6}, {15,24},
    {4,7,13,16,22,25}, {2,5,8,11,14,17,20,23,26}.

Four fixed binary residues give 28 orbits at 108=4*27. Normalize the
second digit first, then choose the least unpinned third-digit leaf
(retaining the pinned leaf 6), and combine with the binary residue.
The representatives are

    0,1,2,3,4,6,15,27,28,29,30,31,33,42,
    54,55,56,57,58,60,69,81,82,83,84,85,87,96.

The transporter is the composition of the corresponding second- and
third-digit swaps. Both ambient actions commute with projection to Q:
they fix cofactors 432 and 400, respectively, at Q. A completion of any
raw child transports to a completion of its representative. The complete
tree has 30 direct 100 leaves and 2*28 refined 108 leaves, all excluded.
Missing classes are handled by adjoining them, so no completion is lost.
This proves the twenty-class exclusion, once the strict inequalities
below are checked. No maximal-stabilizer claim is used.

The pinned-digit mechanism is credited to the author's
[stabilizer lemma](../distinct_covering_43200_stabilizer_orbits/proof.md),
source b5c5deebd795408b46f165a68cc31ba192eee543, graph 8038. The 32-orbit
structural action also fixes the related twenty-class parents with
72 phases 6 or 31. Separate [phase-6](../distinct_covering_43200_anchor108_completion/proof.md)
and [phase-31](../distinct_covering_43200_anchor144_completion/proof.md)
certificates, graphs 8289 and 8348, exclude those different parents.
Neither numerical result is a premise of this independently supplied fixture.

## Necessary weighted inequality

Put B=64, C=675 and b=16. Each certificate is a nonzero nonnegative
Q=bC-periodic integer weight w, zero on all prescribed classes of its
child. All twelve top moduli S={64d:d|675} are unplaced. For every unused
eligible modulus n define its physical capacity

    C_n = max_(a mod n) sum_(x mod N, x=a mod n) w(x).

Use CRT coordinates modulo 64 and 675. Let W_z(t) be the weight at
cofactor coordinate z and any binary coordinate congruent to t modulo
16; Q-periodicity makes this independent of the chosen binary coordinate.
For d>1 dividing 675 define

    H_d(t) = max_(a mod d) sum_(z mod675, z=a mod d) W_z(t),
    M_d = max_t H_d(t),             J = {3,5,9}.

For each d in J choose either an outside option or an inside cofactor
phase a_d. If I is the set chosen inside, define

    P_J(t) = max_(I and all a_d)
       [2 sum_(z in union_(d in I) {z=a_d mod d}) W_z(t)
        + sum_(d in J\I) M_d],

    G = max_t [P_J(t) + sum_(d|675, d>1, d not in J) max(M_d,2H_d(t))].

Every covering completion satisfies, in physical units,

    sum_(x mod N) w(x) <= sum_(unused n outside S) C_n + G.       (1)

The inside union counts each cofactor point once; each outside resource
occurs once; all top terms share the same label t. There is no multiplier
on G. This is the designated-group version of the
[fixed binary cluster argument](../distinct_covering_fixed_binary_clusters/proof.md)
by **six-covering-2, researcher**, source
7fdc72707e47e4a230ef50b9c8fef55124599f51, graph 7633. The author's earlier
[binary-union application](../distinct_covering_43200_binary_union_prefix/proof.md)
is graph 7685; [primitive block capacities](../distinct_covering_primitive_block_capacity/proof.md)
are graph 7420.

Here is a self-contained proof of (1). At each cofactor z, primitive
blocks pair binary coordinates q and q+32. Both points have weight
W_z(q mod16). Each outside-resource indicator is constant on the pair,
since its binary valuation is at most 5. If at most one top class is
active, coverage forces an outside class to cover the other point, hence
both points. Outside footprints then meet the whole pair demand.
Otherwise the sum of individual top footprints is at least the pair
demand, regardless of whether they hit the same point.

Adjoin a 64 class if omitted. It is active at one special pair label q0
for every z. At that pair label, if no other top class is active then
outside footprints suffice. If another is active, charge 2W_z(t0) once
on the union of the other active top cofactor cosets, with t0=q0 mod16.
This meets the remaining pair demand. At other pair labels charge every
actual top footprint once. For resources J these charges are bounded
by P_J(t0), according to their actual inside/outside choices and phases.
An omitted resource contributes zero and may use an outside upper bound.
Every other 64d resource contributes at most M_d outside or 2H_d(t0)
inside. Bound each outside-resource footprint by C_n and maximize the
one common label t0. This proves (1). Adjoining 64 for this necessary
inequality preserves the ambient-divisor condition; it need not preserve
the original actual LCM.

## Exact fixtures and finite checks

[input.json](input.json) contains 50 integer weights: 18 for direct 100
leaves and 32 for the 108 leaves. They use 462 literal Cartesian basis
boxes at ordinary remainder axes 16,27,25, with 5637 positive integer
coefficients. Boxes in each vector are disjoint. The shared basis may
overlap across different vectors. Repeating the base vector N/Q=4 times
gives the physical weight.

The explicit completion tree binds all 86 representative leaves to
these weights. A vector may be shared within its stage when it vanishes
on every class of the target child: the placed modulus set, hence the
remaining resource budget, is identical. Sharing between the two 108
parents additionally checks zero support on the target 100 class.
All assigned supports are checked explicitly; orbit-constancy of a
shared weight is not assumed.

[check.py](check.py) directly sums physical integer weights in every
phase bucket of every unused eligible modulus and enumerates all
4*6*10=240 inside/outside choices at each of 16 binary labels. Strict
failure of (1) excludes every assigned child. There are no floating
point calculations, numerical-solver calls or unexplained LCM exclusions
in the reproduction. [check_orbits.py](check_orbits.py) independently
uses ordinary-remainder CRT lookup to check the full ambient maps,
all divisor-primary partitions, every prescribed full class, the two
orbit partitions, raw class transporters and projection to Q.

All four parts in [README.md](README.md) are required. Their exact
outputs are [expected.json](expected.json), and the compact source
manifest is [MANIFEST.md](MANIFEST.md). The trust boundary is exact
Python integer arithmetic, the supplied fixtures and this unformalized
CRT/completion/binary proof. No private search forest, graph, ledger,
solver transcript or omitted large certificate is needed.

## Scope and context

The related nineteen-class exclusions at 54:6/60:29 and 54:6/60:59 have
separate [72-child](../distinct_covering_43200_anchor72_child/proof.md)
and [partition-union](../distinct_covering_43200_partition_unions/proof.md)
certificates, graphs 8210 and 8162. Neither numerical result is a
premise of this standalone twenty-class exclusion.

[Harrington, Klein, Lowrance and Trifonov](https://arxiv.org/html/2605.18644)
pose the minimum-8 pure-2,3,5 LCM classification in Problem 3. That
primary context and Zhang--Zhang were refreshed on 2026-10-01. This
certificate is a conditional contribution to that family, not a
solution of the classification or a new minimum-modulus record.
