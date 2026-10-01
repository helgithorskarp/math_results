# A three-stage conditional covering exclusion at period 43200

Actual author **six-covering-3**, role **researcher**, 2026-10-01.
Written proof and exact author checks; independent review and formalization
are pending. This certificate applies credited CRT actions and the fixed
binary union inequality. No priority for those general methods is claimed.

Let N=43200. Pair these twenty moduli and phases:

    8,9,10,12,15,16,18,20,24,25,30,36,40,45,48,50,75,54,60,72
    0,0, 5,10, 1, 4, 3,17, 2, 3,11,30,27,19,14,33,13,33,29,31

**Conditional exclusion.** No finite covering of all integers by classes
with pairwise distinct moduli at least8 dividing N contains all twenty
prescriptions. Every other eligible modulus can have an arbitrary phase
or be omitted, at most once. The prescribed8 class makes the minimum
exactly8. The actualLCM need only divide N, rather than equal N. This
theorem does not exclude unrestricted period43200 or improve L_min(8).

## Complete three-stage reduction

The prescribed moduli have LCM Q=10800. If a completion omits a class
at100,108 or144, adjoin any one at that modulus before its corresponding
split. Each divides Q, so this preserves covering, distinctness, minimum8,
and the completion's original actualLCM. At every stage the subsequent
action preserves all prescriptions and permutes full congruence classes
at each eligible modulus; therefore it preserves existence of a completion.
This divisor-completion principle is standard, also described in Section2
of [Zhang and Zhang](https://arxiv.org/html/2607.19029). Their numerical
minimum7 exclusions are not premises here.

For100, fix the cofactor coordinate in N=1728*25. Permute second-digit
quinary leaves under each fixed root modulo5 while fixing leaves3,8,13
modulo25. The25,50,75 prescriptions fix precisely those leaves; other
prescribed moduli have quinary valuation at most1. Every prescribed full
class is fixed. For each divisor of N, its quinary partition is1,5 or25,
and the other primary coordinates are fixed. Thus every divisor partition
is permuted. The eight quinary leaf orbits, together with the fixed binary
residue modulo4, give32 orbits at100. The target leaf is the least unpinned
leaf under its root, or the pinned leaf itself. Ordinary CRT combines it
with the binary residue. This need not be the least integer in its orbit.

The31 representatives other than93 have strict integer weight certificates.
The only raw100 phases normalizing to93 are73 and93. The maps fix the
cofactor1728, hence fix every108 and144 class as well. It suffices to
handle100:93 before proceeding to108.

For108, fix the cofactor coordinate in N=1600*27. At the second ternary
digit fix nodes0,1,3,4,6 modulo9 and freely permute the siblings2,5,8.
At the third digit, independently permute the three leaves below every
node modulo9, fixing leaf6 modulo27. These pins are exactly those needed
by the21 prescriptions, including72:31. In particular, exchanging4 and7
would move that72 class and is forbidden. The100 class is fixed since100
divides1600. The eight ternary leaf orbits are

    {0,9,18}, {1,10,19}, {3,12,21}, {4,13,22},
    {6}, {15,24}, {7,16,25}, {2,5,8,11,14,17,20,23,26}.

Together with the four fixed binary residues these give32 orbits at108.
Normalize the second digit, then the third digit, and combine by CRT.
The31 representatives other than6 have strict certificates;6 is a singleton
orbit. Hence it remains to handle the22 prescriptions including100:93
and108:6.

For144=16*9 use commuting binary and ternary actions. The binary8 pins
are0,2,3,4,6,7; binary16 pins are4,14. Swap the unpinned8 siblings1 and5,
preserving upper bits. Independently swap r and r+8 at16 for
r=0,1,2,3,5,7. The binary16 leaf orbits are

    {0,8}, {1,5,9,13}, {2,10}, {3,11}, {4}, {6}, {7,15}, {12}, {14}.

At ternary9 swap any two of2,5,8 while preserving the upper ternary digit.
The ternary9 orbits are{0},{1},{2,5,8},{3},{4},{6},{7}. Lift binary maps
to64 leaves by preserving higher bits; lift ternary maps to27 leaves by
preserving the upper digit; fix the quinary25 coordinate. The stated pins
fix every22-class prescription. Each map permutes primary partitions
at every divisor of N, and CRT then gives a bijection on every full
congruence partition. The product has9*7=63 orbits at144, all excluded
by the supplied weights. No maximal-stabilizer claim is needed.

All three actions commute with projection to Q. Their actual maps,
prescribed classes, divisor partitions, orbit partitions, and every
raw-class transporter are checked by independent ordinary-remainder CRT
lookups. The two first actions have32 orbits each, and the last has63.
The explicit completion tree has31+31+63=125 representative leaves,
all excluded. Omitted moduli are handled by adjoining them, so no
completion is lost. This proves the twenty-class theorem once the
necessary inequalities below are checked.

The pinned-digit mechanism is credited to the author's
[stabilizer lemma](../distinct_covering_43200_stabilizer_orbits/proof.md),
source b5c5deebd795408b46f165a68cc31ba192eee543, graph8038. The new
binary/ternary144 action is specific to this22-class parent. The earlier
[100/108 certificate](../distinct_covering_43200_anchor108_completion/proof.md)
excludes the different72:6 parent; that numerical result is not a premise.

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

## Compact exact fixtures and trust boundary

[input.json](input.json) stores61 integer vectors:19 at100,18 at108 and
24 at144. Their689 literal Cartesian basis boxes use ordinary remainder
axes16,27,25 and7724 positive integer coefficients. Within each vector
the boxes are disjoint; boxes belonging to different vectors may overlap.
Repeat the base Q-vector four times to get its physical N-vector.

The completion tree assigns every125 representative leaves to a stored
vector. Sharing within a stage requires zero weight on all prescriptions
of the assigned child. Its placed modulus set, and hence its resource
budget, is unchanged. The checker checks every assigned support directly;
no orbit-constancy assumption is made about a shared vector.

[check.py](check.py) directly sums every actual phase bucket of every
unused eligible modulus, then enumerates all240 inside/outside options
at each of16 binary labels. Its positive integer gaps contradict(1).
There are57,56,55 actual unused resources at the three stages respectively.
The three [action checkers](check_orbits144.py) separately check the full
ambient generators and raw-class transports. No floating arithmetic,
solver optimum, unpublished forest or omitted proof corpus is an input.

All six parts in [README.md](README.md) are required. Their deterministic
outputs are [expected.json](expected.json); [MANIFEST.md](MANIFEST.md)
gives source provenance. The trust boundary is ordinary Python integer
arithmetic, the explicit fixture, and this unformalized CRT/completion/
binary-union proof. A failed or incomplete bounded run certifies nothing.

## Family context and scope

The related19-class54:6/60:29 and54:6/60:59 exclusions are separate
[72-child](../distinct_covering_43200_anchor72_child/proof.md) and
[partition-union](../distinct_covering_43200_partition_unions/proof.md)
results, graphs8210 and8162. They are not numerical premises here.

[Harrington, Klein, Lowrance and Trifonov](https://arxiv.org/html/2605.18644)
pose the minimum8 pure2,3,5 LCM classification in Problem3. This and
Zhang--Zhang were refreshed live2026-10-01. The present branch-local
exclusion does not resolve that classification, exclude a whole period,
prove a new global L_min(8) bound, or give a new minimum-modulus record.
