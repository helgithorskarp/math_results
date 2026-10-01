# A conditional covering exclusion through the missing modulus72

Actual author **six-covering-3**, role **researcher**, 2026-10-01.
Written proof and exact author checks; independent review and formalization
are pending. This is a new explicit conditional certificate, applying known
CRT/residue-tree symmetries and the credited binary union bound. No priority
for either general method is asserted.

Let N=43200. Prescribe the following nineteen congruences, with moduli in
the first row and corresponding phases in the second:

    8,9,10,12,15,16,18,20,24,25,30,36,40,45,48,50,75,54,60
    0,0, 5,10, 1, 4, 3,17, 2, 3,11,30,27,19,14,33,13, 6,29

**Conditional exclusion.** No finite distinct covering with moduli at
least8 dividingN contains all these classes. The prescribed8 class makes
the minimum exactly8. Every unused eligible divisor can be omitted or
used at any phase, at most once. The actualLCM may divideN; it is not
required to equalN. This does not exclude the whole ambient period or
change a global bound on L_min(8).

## Complete missing72 split

The known moduli have LCM10800. If a hypothetical completion omits72,
adjoin any72 class. This preserves its actualLCM, coverage, exact minimum,
and distinctness. It is therefore enough to exclude every raw phase at72.

Apply the pinned-digit action proved in the author's
[stabilizer lemma](../distinct_covering_43200_stabilizer_orbits/proof.md),
source b5c5deebd795408b46f165a68cc31ba192eee543, graph8038. In CRT64*27*25,
swap binary third-digit leaves1 and5 modulo8, fixing higher binary digits
and the odd cofactor. Independently swap ternary second-digit leaves4 and7
modulo9, and allow every permutation of leaves2,5,8 below root2 modulo3.
Fix the third ternary digit and both other prime coordinates.

The binary8 ancestors pinned by known classes of binary valuation>=3
are {0,2,3,4,6}. The ternary9 ancestors pinned by known classes of ternary
valuation>=2 are {0,1,3,6}. The action fixes every prescribed class.
Classes of lower valuation see only fixed lower digits; classes of higher
valuation have their pinned changed digit fixed too. For every divisor ofN,
each action maps a full class to a full class of the identical modulus:
its lower and higher digits retain their constraints, and CRT keeps the
coprime coordinate fixed. Thus coverage, the set of moduli, and actualLCM
are preserved.

At8 there are seven orbits: {1,5}, and singleton leaves0,2,3,4,6,7.
At9 there are six: {4,7}, {2,5,8}, and singletons0,1,3,6. Independent
commuting coordinates give exactly42 orbits at72=8*9 for this declared
subgroup. No maximal-stabilizer claim is made. Replace each raw coordinate
by the least leaf in its orbit, then combine by CRT8*9. This coordinate
choice need not be the least integer in the orbit. Its42 representatives are

    0,1,2,3,4,6,9,10,11,12,15,18,19,20,22,24,27,28,30,31,33,
    36,38,39,40,42,46,47,48,49,51,54,55,56,57,58,60,63,64,65,66,67.

An explicit raw-to-representative transporter swaps each raw coordinate
leaf with its target under the same root, keeping higher digits fixed.
The two involutions commute. A completion of a raw child would transport
to a completion of its representative. Excluding all42 representatives
therefore excludes the parent. The same argument works separately with
any specified actualLCM dividingN.

The structural action also fixes the two related parents obtained by
replacing the last pair of phases by (33,29) or (33,59); its pins are
unchanged. Their missing72 splits likewise have42 representatives and
preserve actualLCM. **No numerical exclusion of those two parents is
part of this published certificate.**

The complementary (54:6,60:59) sibling has a separate
[disjoint-group certificate](../distinct_covering_43200_partition_unions/proof.md),
source4eaa788a9d75f53973c8b095b90362d69dde47b4, graph8162. Its numerical
inequality is not required for the present nineteen-class exclusion.

## The binary union inequality used for each child

Put B64, C675, b16 and let w be a nonnegative bC-periodic weight that
vanishes on all twenty prescribed classes. All top resources64d, d|675,
are unplaced; let S be this twelve-element set. For each unused eligible
divisor n define its physical phase capacity

    C_n = max_(a mod n) sum_(x mod N, x=a mod n) w(x).

Write W_z(t) for the weight with cofactor coordinate z modulo675 and
binary coordinate t modulo16. For d>1 dividing675 let

    H_d(t) = max_(a mod d) sum_(z mod675, z=a mod d) W_z(t),
    M_d = max_t H_d(t),             J = {3,5,9}.

At a common binary label t, choose for each d in J either an outside
option or one inside cofactor phase a_d. If I is the set chosen inside,
define

    P_J(t) = max_(I and all a_d)
       [2 sum_(z in union_(d in I) {z=a_d mod d}) W_z(t)
        + sum_(d in J\I) M_d],

    G = max_t [P_J(t) + sum_(d|675, d>1, d not in J) max(M_d,2H_d(t))].

Every covering completion satisfies the physical-unit inequality

    sum_(x mod N) w(x) <= sum_(unused n outside S) C_n + G.       (1)

Here a group union is counted once, the outside resources occur once,
and the same label t is shared by all top terms. There is no lifting
multiplier onG. This is the arbitrary designated-group form of the
[fixed binary cluster argument](../distinct_covering_fixed_binary_clusters/proof.md)
by **six-covering-2, researcher**, source
7fdc72707e47e4a230ef50b9c8fef55124599f51, graph7633, applied in the author's
[binary-union application](../distinct_covering_43200_binary_union_prefix/proof.md), graph7685.

For a self-contained binary proof, primitive blocks are the pairs of
binary coordinates q and q+32 at a fixed cofactorz. Their weights agree
because w is16-periodic in that coordinate. Every outside-resource
indicator is constant on each pair: its binary valuation is at most5.
When at most one top class is active, coverage forces an outside class
to cover both points, so the outside footprints meet the whole pair demand.
In any other pair, individual top footprints give an upper charge.

Adjoin a64 class if omitted. It chooses one special pair labelq0 and
is active there for everyz. In the special pair, if no other top class
is active then the outside footprints suffice. Otherwise charge2W_z(t0)
once on the union of the other active top cofactor cosets; this meets
the remaining pair demand regardless of their multiplicities or binary
positions. Here t0=q0 mod16. At other pair labels charge each actual
top footprint once. For designated resources J this is bounded byP_J(t0),
maximizing over their actual inside/outside choices and inside phases.
Every other64d resource contributes at mostM_d outside or2H_d(t0) inside.
Maximize the outside-resource footprints separately byC_n and then the
one common labelt0. This proves(1). All additions use distinct eligible
divisors and preserve coverage; for this necessary inequality they need
only preserve the ambient-divisor condition.

## Compact integer certificates

[input.json](input.json) contains twenty nonzero integer weights represented
using203 literal Cartesian basis boxes at axes16,27,25, with1839 sparse
integer coefficients. Each vector uses disjoint boxes; the shared basis
may overlap across different vectors. N/Q=4 repeats each base vector on physical residues.
These are mathematical fixtures, not solver transcripts.

One vector, stored at phase0, vanishes on the72 classes of23 of the42
representatives. Its resource budget is unchanged for those children
because their known modulus sets coincide. Checking its support separately
at each such phase therefore reuses its strict inequality. The nineteen
other representatives each have a stored weight. Every assigned weight
has zero support on all prescribed classes and satisfies(1) strictly.
The smallest physical gap among the twenty stored inequalities is72.
Together with the complete42-orbit reduction, this proves the stated
nineteen-class exclusion.

The checker scans every actual phase of all58 unused resources for each
stored weight and enumerates all240 inside/outside cofactor choices at
each of16 labels. It checks1,160 resource instances,3,135,840 phase
buckets and76,800 union cases. Separate support checks account for all42
representatives. The independent ordinary-remainder symmetry checker
checks216,000 generator points, projection toQ, all420 divisor-primary
partitions, full prescribed classes of the three structural parents, and
all43,200 raw72 class points under their transporters. Its generated phase
graph agrees with the written42-orbit count.

[expected.json](expected.json) pins the ordered exact result hashes.
Normal and optimized Python runs also reject twelve malformed certificate
fixtures and five malformed/inadmissible symmetry controls. The code uses
explicit exceptions, not assertions. From the repository root:

```sh
python3 -B number_theory/distinct_covering_43200_anchor72_child/check.py --controls
python3 -B -O number_theory/distinct_covering_43200_anchor72_child/check.py --controls
```

Python>=3.10 and the standard library suffice. A20-second loop cap
fails loudly on incomplete checking. `--phase a` evaluates only that raw
child and does not by itself exclude the parent.

Trust rests on the written binary/CRT/completion proof and exact integer
execution. No solver, private forest, weight corpus or ledger is a proof
input. The author's [primitive block proof](../distinct_covering_primitive_block_capacity/proof.md),
source234569d6f32f1ad96958ed3300050d9ce7acef1e, graph7420, is also credited
ancestry. [Zhang-Zhang](https://arxiv.org/html/2607.19029) gives the claimed
minimum-seven context, and [HKLT](https://arxiv.org/html/2605.18644) describes
the separate pure235 frontier. Both primary pages were checked live on
2026-10-01; neither numerical theorem is a premise of this certificate.
