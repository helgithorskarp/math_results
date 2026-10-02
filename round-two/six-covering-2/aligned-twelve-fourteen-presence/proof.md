# Aligned twelve forces an original fourteen opponent at period 10080

Actual author **six-covering-2**, role **researcher**, 2026-10-02.
An exact computer-assisted lemma with a written, unformalized class bridge.
No independent reviewer verdict or formalization is claimed.

Let N=10080. Consider a finite covering of all integers by congruences with
pairwise distinct moduli dividing N and minimum modulus **exactly eight**.
The actual least common multiple may properly divide N. Write a8 for the
phase of its original modulus-8 class. The credited [twelve-class lemma](../twelve-class-exclusion/proof.md)
ensures that an original modulus-12 class is present; write its phase a12.

**Lemma.** If a12 agrees with a8 modulo four, then modulus 14 is present in
the ORIGINAL cover, and its phase has parity opposite to a8.

Together with the credited lemmas, the aligned case therefore requires all
three ORIGINAL classes 9, 10 and 14: a12 differs from a9 modulo three, and
both a10 and a14 have parity opposite to a8. The 9/10 conclusions are credited;
the 14 presence and parity restriction are new here.

The new finite exclusion is the complete five-class form

    F=((8,0),(9,0),(10,1),(14,0),(12,4)).

Every remaining original divisor modulus is permitted at F: all 60 resources,
with no hidden consumption of 16, 20, 28 or any TOP resource. This removes
one of the [thirteen previously remaining forms](../ten-twelve-parity/proof.md),
leaving twelve. The global L_min(8) candidates 10080/15120/20160 and the credited
20160 witness remain unchanged. This is not an exclusion of period 10080.
Minimum-at-least-eight is a separate parameter.

## Original-class bridge, including absent fourteen

Assume a12=a8 modulo four. The published [8728 lemma](../twelve-class-exclusion/proof.md)
implies that ORIGINAL9 is present and a12-a9 is nonzero modulo three. The
published [9065 lemma](../ten-twelve-parity/proof.md) implies that ORIGINAL10
is present and a10-a8 is odd, since original12 has eight parity.

Suppose there is no PRESENT original14 class whose parity opposes a8. If14
is present, its phase a14 has a8 parity. If14 is absent, adjoin a class of
modulus14 with that parity. Adjoining this distinct unused divisor retains
covering, minimum exactly 8 and divisibility of every modulus by N. It is an
auxiliary class only in this case; we do not call it original in the initial
cover. In either case the resulting covering has five actual classes satisfying

    a10-a8 odd, a14-a8 even,
    a12-a8=0mod4, a12-a9 nonzero mod3.                 (1)

Here is an explicit unit affine normalization of (1). On CRT coordinates
32,9,5,7, choose multiplier

    u=(1,u3,1,1), with u3=(a12-a9)^(-1)mod3 in{1,2},

and offset

    v=(-a8,-u3*a9,1-a10,-a14).

The 9-coordinate multiplier is a unit modulo9, so the CRT multiplier is a
unit modulo N. The transformed phases at 8 and9 are0. At10, parity is odd
and the residue modulo5 is1, giving phase1. At14, parity is even and the
residue modulo7 is0, giving phase0. At12, the residue modulo4 is0 and the
residue modulo3 is1, giving phase4. Hence the transformed covering extends F.
The affine map permutes integers modulo N and preserves each divisor's whole
congruence partition, coverage and distinctness. The complete F exclusion below
contradicts this cover. Therefore original14 must already be present and oppose
a8 parity. This handles omission before asserting original-class presence.

## Exact complete F certificate

At a prefix A let U be its literal uncovered residues in Z/NZ, and B contain
EVERY unused divisor modulus of N at least8. For nonnegative integer weights
w supported on U, put H=sum w and C_m=max_a sum_(x=a mod m)w(x). For a distinct
pair e=(m,n), let C_e be the maximum weight of the actual union of one m-class
and one n-class. Select pair coefficients c_e in{1,2}, with incident degrees
d_m=sum_(e containing m)c_e<=2. Every completion satisfies

    2H <= sum_m (2-d_m) C_m + sum_e c_e C_e.          (2)

At each covered point choose one resource covering it. Its singleton/pair
groups contribute total coefficient2; every other group contributes a
nonnegative amount. Sum against w and maximize each group to obtain (2).
Every weighted leaf strictly reverses (2); uniform leaves use its singleton
specialization. Covers omitting resources are included by adjoining arbitrary
phases at those distinct unused moduli.

At every branch the [unchanged literal checker](../check.py) checks EVERY raw
phase. Each positive-gain phase is carried to a recorded child by an explicit
CRT digit-tree bijection fixing all known classes and preserving every original
divisor-congruence family. A zero-gain phase, or omission of the branch modulus,
may be replaced by a positive-gain phase without losing a proposed cover.
Such a phase exists because U is nonempty and the classes partition the period.
The checker verifies complete branch coverage and each strict leaf, giving a
finite induction excluding F. No incomplete enumeration or solver status is
a nonexistence premise.

The author literal replay has 2625 nodes, 375 branch expansions and 2250 strict
leaves: 1270 singleton, 208 integral-pair, 19 fractional-pair and 753 uniform.
There are 1497 weight vectors in 155438 disjoint positive integer boxes,
7797 raw branch phases, 7363 positive transports and 1169803 actual selected
phase-pair entries. It ran in118.083936 seconds with78120 KiB peak child RSS.
The literal verifier imports neither the floating-point solver, the discovery
normalizer nor a CRT intersection formula. It recomputes physical progressions,
every capacity, all phase-pair unions, decoded integer boxes and transports.
Open, covering, incomplete, cyclic, shared, missing, unused or malformed proof
evidence is rejected.

[manifest.json](manifest.json) records exact counts and event/transport/pair-table
hashes. Hashes identify the record; the strictly recomputed inequalities prove
the exclusion. The 4029549-byte generated tree is omitted. Its author SHA256 is
514a558bfff7eda588f2cf3521a9b42003524a7fab6b59ef3af50a03306b2c66.
The author used seven resumable bounded batches at this five-class root, each
180 seconds/700 new nodes, with one numerical thread. The final batch used
167.878 seconds/128544 KiB. A fresh cold uninterrupted regeneration is not
claimed; the public source regenerates the same root from no private input.
If a finite voluntary allowance exhausts, it returns INCOMPLETE and proves
nothing. Any complete valid certificate proves the conditional exclusion;
--require-manifest additionally requires the author's exact replay record.

## Complete twelve-form frontier and attribution

The credited [8606 affine reduction](../five-class-exclusion/proof.md) sends
all 120960 physical phase tuples at 8,9,10,14,12 to24 forms. The prior9065
frontier removes11 forms/40320 tuples. The new F form represents exactly 5040
additional tuples satisfying (1), giving12 removed forms/45360 tuples and
12 remaining forms. [frontier_fourteen.py](frontier_fourteen.py) checks every
physical tuple and, independently of the credited affine constructor, verifies
the explicit CRT map above on all 5040 new tuples. It also checks that the
four forms corresponding to a12=a8 mod4 and a14=a8 mod2 are all removed.
Those four forms represent15120 tuples; only the F cell is newly excluded here.
Phase enumeration alone is not the finite exclusion proof.

[application-next.json](application-next.json) gives all twelve remaining
prefixes, exact literal residual bitsets/counts and the complete common pool
of60 UNUSED original moduli. All phases of288/1440/2016/10080 remain free.
The wrapper reconstructs every inventory field. Missing small moduli may be
adjoined for this auxiliary five-class frontier; the original14 lemma instead
uses the explicit absent-class contradiction above. Every remaining form is
unexcluded here; no completion or whole-period classification is asserted.

| Credited input | Scope used | Source commit | Graph artifact |
| --- | --- | --- | --- |
| Literal tree criterion8557 | Exact counting/branch verifier; different-prefix numerical theorem not imported | 2d66a2b1ed2d5549e1316117d1def22a474bb179 | bafkreih3y7ovbsfsqmxizyrcdho5ynff3hqzstw5kpocuoyvezqku3neaq |
| Affine reduction8606 | Complete five-class normalization | 433efdee31eb6f95e5ab0a753b78bb5601245714 | bafkreibgg6wg7b3wrd54kqt6e2q3ktzbmhcq2mlhc5rjwmgtqw73g4xxku |
| Original12 lemma8728 | Original12/9 presence and ternary condition | b1d33a7c2b7ab8091d58508033107e0f88e61c80 | bafkreibbmkj4sx4jy5gfc2nnsa4bsapfezivsa6l6ty4pokny6wsr55mci |
| Ten/twelve lemma9065 | Original10 presence/parity and credited13-form frontier | 22ee1456490508063668c2cc6514d4c1ef9d2849 | bafkreiai5yxijdvvwy4wnzmtsi4jsoapztlrtyxq5a3nwdw2qo7f6ptplu |

The prior [9117 sixteen restriction](../first-root-sixteen-presence/proof.md)
left F's canonical16:2/4 children open, source 28b11892997c765d098c6badb96f1ea867ffb342,
graph bafkreiddsmc6ahaqxmqvdohwvsrq22gan35ahdtpp4p3gk23teyv2k6j6e.
The present full-F exclusion strengthens that conclusion; its numerical proof
is replayed directly and does not assume the earlier phase bridge. All imported
source/proof dependencies are hash-pinned. The earlier intrinsic theorems are
credited written premises, not claims to recheck their other numerical roots.

Primary context, freshly checked2026-10-02:
[Zhang–Zhang](https://arxiv.org/html/2607.19029) claims L_min(7)=10080 with final
numerical exclusions; [HKLT](https://arxiv.org/html/2605.18644) treats the
restricted2/3/5-support minimum-eight frontier. Neither supplies a numerical
proof premise here. Weighted union counting, affine normalization and CRT
digit-tree maps are credited methods; no historical-priority claim is made.
The new content is the complete F exclusion and original14 consequence.

The final publication-directory wrapper matched the full author manifest in
77.561 seconds with79564KiB peak child RSS. Complete phase controls agree
normally and under Python-O, including all5040 separately constructed CRT
maps. Twelve wrong domains and eight damaged remaining-resource inventories
reject in both modes. These checks supplement the literal proof; domain-only
positive controls and controls-only mode do not accept a proof certificate.
