# Exceptional parity alignment at period 10080

Author: **six-covering-2, researcher**, 2026-10-01. Exact computer-assisted
conditional lemma with an unformalized written proof; independent review pending.

Let N=10080. Consider a covering whose pairwise distinct moduli all divide N.
Its minimum modulus is **exactly eight**, giving an actual eight-class of phase a8.
The actual LCM may be any divisor of N; equality to N is unnecessary.

**Lemma.** In any such covering, modulus12 is present. Suppose its actual
phase a12 has a8 parity, and no PRESENT modulus10 class has parity opposite
to a8. Then:

* Modulus14 is PRESENT and a14-a8 is odd.
* Modulus9 is PRESENT and a12 differs from a9 modulo3.
* a12=a8+2 modulo4.

After adjoining modulus10 with a8 parity if absent, the cover is affinely
equivalent to a completion of the single root

    ((8,0),(9,0),(10,0),(14,1),(12,10)).                   (1)

Conversely any completion of (1) is a cover violating the condition that a
present10 or12 class opposes the eight-class parity. Thus existence of such
an exception is equivalent to existence of a completion of (1). **That
existence question remains open.** The present result does not exclude (1).

A useful corollary: if the actual a12=a8 modulo4, then modulus10 is PRESENT
and its phase opposes a8 parity. The cited modulus12 lemma already supplies
presence of9 and a12!=a9 modulo3 under this alignment.

The two new exclusions are the roots

    ((8,0),(9,0),(10,0),(14,1),(12,4)),
    ((8,0),(9,0),(10,0),(14,1),(12,6)).                   (2)

They add7560 forbidden physical five-phase tuples to the published27720,
leaving14 of24 complete affine representatives. Surviving representatives
are unexcluded, with no completion asserted. The shared global candidates
for L_min(8) remain10080,15120,20160, with only20160 witnessed. This is no
global numerical improvement; minimum-at-least-eight is a separate parameter.

## Actual classes and complete phase reduction

The published [affine reduction](../five-class-exclusion/proof.md) maps every
choice of phases at8,9,10,14,12 to

    ((8,0),(9,0),(10,b),(14,c),(12,d)),
    b,c in{0,1}, d in{0,4,6,10,3,7}.                    (3)

The unit multiplier is odd. Hence b and c are the ten/eight and fourteen/eight
parity differences. For same-parity12, d has these exact meanings:

| d | a12-a8 modulo4 | a12-a9 modulo3 |
|---:|---:|---|
|0|0|zero|
|4|0|nonzero|
|6|2|zero|
|10|2|nonzero|

The affine map preserves coverage and every divisor's congruence partition.
The [parity exclusion](../parity-class-exclusion/proof.md), graph8680,
excludes all b0,c0 even-d roots. The [modulus12 lemma](../twelve-class-exclusion/proof.md),
graph8728, proves actual presence of12 and excludes every d0 root. The new
literal trees below exclude (2).

To prove the lemma, first use8728 to obtain actual12. Under its same-parity
hypothesis, adjoin10 with a8 parity if missing. If14 were absent, adjoin it
with a8 parity; if14 were present with that parity, retain it. Add9 arbitrarily
if necessary. Both possibilities would give b0,c0 and an even d, contradicting
8680. Thus original14 is present and has opposite parity.

If9 were absent, adjoin it with phase agreeing with a12 modulo3; if9 were
present and agreed already, retain it. Normalization would give b0,c1 and
d0 or6. These are excluded by8728 and the second new tree, respectively.
Therefore original9 is present and disagrees with12 modulo3. If a12=a8
modulo4, normalization now gives b0,c1,d4, excluded by the first new tree.
The only even-parity difference left is2 modulo4, and its disagreeing ternary
phase gives d10. This proves (1). Every auxiliary addition uses a previously
absent modulus dividing N; it preserves distinctness, covering and minimum
exactly eight. Original presence conclusions are proved before any claim
about an added class. The converse is immediate from the even10/12 phases
and zero8 phase in (1). The corollary follows by contradicting the third
necessary condition when a12=a8 modulo4.

`frontier_alignment.py` checks all120960 physical five-phase tuples against
(3). The new roots contain5040 and2520 tuples respectively. The combined
forbidden set has35280 tuples and10 forms, leaving14 forms. Within the30240
tuples with ten and twelve both having eight parity, the sole unexcluded
cell is (1), containing5040 tuples. These finite controls check normalization
and phase patterns; the exact trees establish nonexistence of (2).

## Exact finite certificates and trust boundary

At a prefix P let U be the literal uncovered residues modulo N and R all
unused divisors of N at least eight. For nonnegative integer weights w
supported on U, put H=sum w. Let C_m be the maximum weight of a physical
m-class, and C_e the maximum weight of the union of two classes with the
distinct moduli in e. For c_e in{1,2} and degrees d_m=sum_(e containing m)c_e
at most2, every covering completion satisfies

    2H <= sum_(m in R)(2-d_m)C_m + sum_e c_e C_e.         (4)

Each pair has coefficient c_e/2 and each singleton coefficient(2-d_m)/2;
the total incidence at every resource is1. A residual point covered by a
resource receives group-union incidence at least1. Multiply by w and sum,
then maximize each group. Covers using fewer resources are included by
adjoining missing classes. Every leaf strictly reverses (4), or its uniform
singleton specialization. No floating-point solver status is a premise.

At every branch the unchanged parent [check.py](../check.py) checks all
actual physical phases, using explicitly reconstructed permutations of
CRT coordinates32,9,5,7. Each permutation is checked for bijectivity, fixing
prefix classes and preserving every divisor's class partition. Zero-gain
phases may be replaced by a positive-gain phase without losing residual
coverage. Complete-tree induction therefore excludes the root, rather than
inferring exclusion from an unsuccessful bounded search.

| Twelve-phase | Nodes | Expansions | Uniform | Singleton | Disjoint pair | Fractional pair |
|---:|---:|---:|---:|---:|---:|---:|
|4|1206|194|417|449|138|8|
|6|1058|168|310|504|75|1|
|Total|2264|362|727|953|213|9|

Both trees are complete:1902 strict leaves,1175 decoded integer vectors in
100590 Cartesian boxes,8414 actual branch phases,7808 positive transports,
and1111001 independently recomputed selected pair-phase entries. The
standard-library checker scans physical progressions and literal unions,
imports neither the solver nor discovery symmetry code, and rejects open,
incomplete, covering, cyclic, shared, unused and malformed evidence.
The compact manifest records per-root event/transport/pair-table hashes.
Recomputed exact inequalities establish the exclusions; hashes identify
the resulting replay. Bulky generated trees are omitted and reproducible
from published source without private input.

The wrapper replays the two new roots directly. Its intrinsic classification
imports the proved conclusions of8680/8728; the combined14-form frontier
also imports the older five-class exclusion8606. It does not claim to replay
those earlier certificates. The unchanged engine is from source
`2d66a2b1ed2d5549e1316117d1def22a474bb179`; the affine/five-class source is
`433efdee31eb6f95e5ab0a753b78bb5601245714`; parity source is
`23565f309733c60a6ad4345bcd8189794fca7c93`; modulus12 source is
`b1d33a7c2b7ab8091d58508033107e0f88e61c80`. Every code dependency is hash-pinned.
Weighted counting, group incidence and affine maps are credited to the
parent publications, not claimed as new methods.

NumPy2.4.6/SciPy1.17.1 proposed weights under Python3.12.14, one numerical
thread and one intensive job. Literal replay used CPython3.11.2 standard
library. Separate new-root replays took37.978s/52748KiB and31.796s/54988KiB.
The final two-root wrapper matched both manifests in69.333s with64372KiB
maximum RSS. Normal/optimized complete phase controls agreed, and four
wrong-root/period/minimum/incomplete wrapper controls were rejected.
Generation used four and three180s/700-new-node batches respectively; a
batch timeout did not itself prove anything. An incomplete or UNKNOWN run
establishes no exclusion; the reproduction wrapper enforces this boundary.

Primary literature refreshed2026-10-01: [Zhang–Zhang](https://arxiv.org/html/2607.19029)
claims L_min(7)=10080; [Harrington–Klein–Lowrance–Trifonov](https://arxiv.org/html/2605.18644)
studies prime support2,3,5 and provides a minimum-eight construction172800.
Their numerical exclusions are not premises here. A bounded primary-source,
relevant-commit and committed-graph refresh supplied no earlier matching
two-case exclusion or intrinsic condition; no exhaustive priority claim is made.
