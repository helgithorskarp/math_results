# Original twelve differs from original eight modulo four at period 10080

Actual author **six-covering-2**, role **researcher**, 2026-10-02.
Exact computer-assisted lemma with an ordinary, unformalized phase bridge.
No independent reviewer verdict, formalization or historical priority is claimed.

Let N=10080. Consider a finite covering of all integers by congruences with
pairwise distinct moduli dividing N and minimum modulus **exactly eight**.
Its actual least common multiple may properly divide N. Write a8 for the
phase of its original modulus-8 class. The credited [original12 lemma](../twelve-class-exclusion/proof.md)
ensures that original modulus12 is present; write its phase a12.

**Lemma.** a12 is different from a8 modulo four.

The new complete finite exclusion is

    G=((8,0),(9,0),(10,1),(14,1),(12,4)).

At this FIVE-class root every one of the60 unused ORIGINAL divisor moduli
is free, including every phase of288/1440/2016/10080. No16,20,28,32 or other
descendant is already consumed at the root. The result removes one of the
[twelve previously remaining forms](../aligned-twelve-fourteen-presence/proof.md),
leaving eleven. It does not exclude period10080 or improve the global numerical
L_min(8) candidates10080/15120/20160, of which20160 is the credited witness.
Minimum-at-least-eight remains a separate parameter.

## Original-class and explicit affine bridge

Suppose a12 agrees with a8 modulo four. The credited [8728 lemma](../twelve-class-exclusion/proof.md)
gives ORIGINAL9 presence and a12-a9 nonzero modulo three. The credited
[9065 lemma](../ten-twelve-parity/proof.md) gives ORIGINAL10 presence and
a10-a8 odd. The credited [9239 lemma](../aligned-twelve-fourteen-presence/proof.md)
gives ORIGINAL14 presence and a14-a8 odd. Those conclusions refer to the
initial cover; their published absence-class bridges are credited premises.
The new argument does not silently adjoin these classes and then call them
original. In particular it imports no private original16 or20 restriction.

Use CRT coordinates32,9,5,7 and choose multiplier and offset

    u=(1,u3,1,1),  u3=(a12-a9)^(-1)mod3 in{1,2},
    v=(-a8,-u3*a9,1-a10,1-a14).

The9-coordinate multiplier is a unit modulo9, and every coordinate multiplier
is a unit. The resulting multiplier is a unit moduloN. The phases at8 and9
become0. At10 the image is odd and1mod5, hence phase1. At14 it is odd and1mod7,
hence phase1. At12 it is0mod4 and1mod3, hence phase4. Thus the transformed
cover extends G. The affine map permutes the full period, preserves each
original divisor's entire class family and preserves covering/distinctness.
The complete G exclusion below contradicts that cover, proving the lemma.
This leaves no aligned original12 case; no converse or covering sufficiency
is asserted.

## Complete literal G exclusion

At a prefix A let U be its literal uncovered residues moduloN. Keep EVERY
unused divisor modulus at least8 as an original resource. For nonnegative
integer weights w on U, put H=sum w and

    C_m=max_a sum_(x=a mod m)w(x).

For a distinct original-resource pair e=(m,n), C_e is the maximum weight of
the ACTUAL union of one m-class and one n-class. Let c_e be1 or2, with incident
degrees d_m=sum_(e containing m)c_e<=2. Every completion obeys

    2H <= sum_m(2-d_m)C_m + sum_e c_e C_e.           (1)

At any covered point choose one covering resource. Its singleton/pair groups
have total coefficient2; the other groups contribute nonnegatively. Weight
and sum these point inequalities, then maximize each group. Every weighted
leaf strictly reverses(1). Uniform leaves use its singleton specialization.
Unused original moduli may be adjoined with arbitrary phases, so omitted
resources do not evade the necessary inequality.

At each branch, the [unchanged literal checker](../check.py) checks EVERY raw
phase. Explicit CRT digit-tree bijections carry positive-gain phases to recorded
children, fixing all known classes and preserving EVERY original congruence
family. The checker verifies the complete physical permutation and incidences.
A zero-gain phase or an omitted branch resource can be replaced by a positive-
gain phase without losing a proposed cover; such a phase exists for nonempty U.
Complete branch coverage and all strict leaves then prove exclusion by finite
induction. No solver status, timeout or incomplete enumeration is a premise.

The full author replay checked2756nodes,380branch expansions,2376strict leaves:
1571singleton,207integral-pair,8fractional-pair,590uniform. Its1786integer
vectors occupy165931disjoint positive boxes. It checks8530raw branch phases,
7986positive transports and1270367actual selected pair-phase entries.
Runtime76.896866seconds,peak82832KiB. It recomputes physical progressions,
capacities, actual unions, integer box decompositions and branch transports.
It imports no floating-point solver, discovery normalizer or CRT intersection
formula. Incomplete, covering, shared, cyclic, unused or malformed evidence
is rejected.

[manifest.json](manifest.json) fixes the full replay counts and event/transport/
pair-table hashes. Hashes identify evidence; the recomputed strict inequalities
prove the exclusion. The4292030-byte generated tree is omitted, with authorSHA256
b578363c8067d74b9a6a17c6905504c14fcd654c0696f386694bad50df407dee.
The author resumed this root across eight bounded batches, each180seconds/
700new nodes, numerical threads1. The final batch used35.650161seconds/
129188KiB. A fresh cold standalone regeneration is not claimed. The supplied
source regenerates this same root from no private input; exhausting a finite
voluntary allowance returns INCOMPLETE and proves nothing. Any complete valid
tree proves the exclusion; --require-manifest additionally requests the exact
author replay record, which can differ with a numerical discovery environment.

## Eleven-form frontier and credited inputs

The credited [8606 reduction](../five-class-exclusion/proof.md) normalizes
all120960physical tuples at8,9,10,14,12 to24forms. The credited9239 frontier
removes12forms/45360tuples. G represents5040additional tuples, yielding
13removed forms/50400tuples and11remaining forms. [frontier_nonalignment.py](frontier_nonalignment.py)
checks every tuple and independently checks the explicit unit map above on
every new G tuple. It verifies that all eight forms where a12=a8mod4 are
removed; they represent30240tuples, of which only the G cell is newly removed
here. Phase enumeration itself does not prove the exclusion.

[application-next.json](application-next.json) lists all eleven remaining
prefixes, exact literal residual bitsets/counts and the common pool of60free
original moduli. All TOP phases remain free. The wrapper reconstructs every
field, and controls-only mode explicitly accepts no exclusion certificate.
Missing small moduli may be adjoined for this auxiliary five-class frontier;
the intrinsic lemma uses the credited ORIGINAL-class conclusions above.
Every listed remaining form is unexcluded here, with no completion assertion.

|Credited input|Scope used|Source commit|Graph artifact|
|---|---|---|---|
|8557|Literal counting/branch criterion; different-prefix numerical result not imported|2d66a2b1ed2d5549e1316117d1def22a474bb179|bafkreih3y7ovbsfsqmxizyrcdho5ynff3hqzstw5kpocuoyvezqku3neaq|
|8606|Complete five-class affine normalization|433efdee31eb6f95e5ab0a753b78bb5601245714|bafkreibgg6wg7b3wrd54kqt6e2q3ktzbmhcq2mlhc5rjwmgtqw73g4xxku|
|8728|Original12/9 presence and ternary phase condition|b1d33a7c2b7ab8091d58508033107e0f88e61c80|bafkreibbmkj4sx4jy5gfc2nnsa4bsapfezivsa6l6ty4pokny6wsr55mci|
|9065|Original10 presence/parity and prior frontier|22ee1456490508063668c2cc6514d4c1ef9d2849|bafkreiai5yxijdvvwy4wnzmtsi4jsoapztlrtyxq5a3nwdw2qo7f6ptplu|
|9239|Original14 presence/parity under alignment and prior12-form frontier|e93fe222da1f175eeac96d1f2c24cdefdcfcf8e0|bafkreig5gmgx7gvsnmjd7yckowqo44zqvuu2lnkyg7zvtuiyvt75egx7v4|

Imported source/proof dependencies are hash-pinned. Earlier intrinsic theorems
are credited written premises; their other numerical roots are not claimed
to have been freshly replayed here. Private G16/20 child refinements are
subsumed by the complete root and are not independent proof premises.

Complementary [9309 support predicates](../../six-covering-3/cardinality-cores/proof.md),
source829191175ec16f2001b48caa53f539d9a155238f, concern a separate free-tail
necessary cut. Their full graph proof/relations and written source were read;
their numerical fixtures or fifteen-table are not imported into this exclusion.
The [9287 tail construction/bound](../../six-covering-1/four-coset-tail-overlap/proof.md),
source106223e6ce40150aa987e64dce7e2725df9e65d4, concerns separate15120 work;
its numerical claims are context only, without local replay or import.

Primary context reopened2026-10-02:
[Zhang--Zhang](https://arxiv.org/html/2607.19029) claims L_min(7)=10080 with
final numerical exclusions; [HKLT](https://arxiv.org/html/2605.18644) treats
the restricted2/3/5-support minimum-eight frontier. Neither is a proof premise.
Weighted union counting, affine normalization and CRT digit-tree maps are
credited methods. New content here is the full G exclusion and its original12
nonalignment consequence, with no global numerical improvement.

The final publication-directory wrapper matched the exact full author
manifest in83.039793seconds,peak83968KiB. Complete normal/O phase controls
agree, including all5040independently constructed unit maps. Twelve wrong
domains and eight damaged resource inventories reject in both modes.
No controls-only or domain-only check accepts an exclusion certificate.
