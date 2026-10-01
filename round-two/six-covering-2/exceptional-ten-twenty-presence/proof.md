# Original ten and twenty classes in the exceptional minimum-eight case

Actual author: **six-covering-2, researcher**, 2026-10-01. An exact
computer-assisted conditional lemma with a written, unformalized bridge.
Author validation is described below; no independent reviewer verdict is
asserted. This establishes no global period10080 exclusion or numerical
improvement to L_min(8).

Let N=10080. A covering has pairwise distinct moduli dividing N and minimum
modulus **exactly eight**, with actual eight-phase a8. Its actual LCM may
divide N; equality is unnecessary. By the credited
[modulus-twelve result](../twelve-class-exclusion/proof.md), modulus12 is
present. Suppose its actual phase a12 has a8 parity, and no PRESENT modulus10
class has parity opposite a8. These are the exceptional hypotheses of
[8837](../exceptional-phase-alignment/proof.md).

**Lemma.** Both modulus10 and modulus20 are PRESENT in the ORIGINAL covering.
Their actual phases satisfy

    a10-a8 is even,
    a20-a8 is odd  if and only if  a20-a10=0mod5.          (1)

The credited [sixteen-alignment lemma8923](../exceptional-sixteen-alignment/proof.md)
already forces original16 with a16-a8=4mod8. After the credited affine
normalization, existence of an exceptional covering is therefore equivalent
to existence of a completion of one of these THREE roots:

    ((8,0),(9,0),(10,0),(14,1),(12,10),(16,4),(20,2)),
    ((8,0),(9,0),(10,0),(14,1),(12,10),(16,4),(20,4)),
    ((8,0),(9,0),(10,0),(14,1),(12,10),(16,4),(20,5)).      (2)

All three roots are unexcluded here; no completion is asserted. The sole new
full ordinary exclusion is

    S=((8,0),(9,0),(10,0),(14,1),(12,10),(16,4),(20,1)).    (3)

In particular this lemma does NOT remove the exceptional five-class form.
The complete five-class frontier remains14 forms, and the global exactly-eight
LCM candidates remain10080/15120/20160, with only20160 witnessed.
Minimum-at-least-eight is a different parameter.

## Transport of the twenty phases

Write R for the six-class prefix of(3). The CRT coordinates are32,9,5,7.
For an odd20-phase a nonzero modulo5, send its binary residue modulo4 to1
as follows: keep all even32-coordinates fixed, and if a=3mod4 toggle the
second binary digit on every odd32-coordinate. This is a rooted-tree
permutation, preserving every binary congruence partition. In the5-coordinate
swap a mod5 with1 while keeping0 fixed. Keep the9 and7 coordinates fixed.

The product permutation fixes each class of R: its four prescribed even
binary classes are fixed pointwise in that coordinate;14:1 needs only the
unchanged odd binary residue;10:0 also needs the fixed5-coordinate0.
It maps the whole20:a class to20:1 and preserves every divisor-class family.
Thus exclusion of(3) excludes all E+16:4+20:a with a odd and a!=0mod5.

For even a nonzero modulo5, keep the binary coordinate fixed and swap its
5-coordinate with that of2 if a=2mod4, or4 if a=0mod4. This sends the class
to20:2 or20:4. Odd phases0mod5 similarly map to20:5 by the binary toggle.
The remaining phases0 and10 are contained in10:0. The complete positive
phase partition has sizes8/4/4/2 at representatives1/2/4/5.

`phase_controls.py` constructs all18 product permutations. It checks their
physical bijectivity, preservation of all72 divisor partitions, fixing each
class of R and transport of the entire twenty-class, with181440 point checks
and1296 divisor-family checks. It also verifies every twenty-to-ten
containment. These controls authenticate the finite transport argument;
the separate complete tree proves the exclusion of(3).

## Original presence, including the missing-ten case

First exclude an exceptional covering with original20 ABSENT. Adjoin10 with
eight parity if needed. By8837 and8923, normalize to R; adjoining20:1 would
then give a completion of the excluded root(3). Every addition uses a
previously absent divisor modulus and preserves covering and minimum exactly8.

Next suppose ORIGINAL10 is absent. Original20 must now be present. If its
phase has parity opposite8, adjoin an eight-parity10 whose5-coordinate
DIFFERS from that of20. The credited normalization sends this to R with an
odd20-phase nonzero modulo5, excluded by the transport above. If20 instead
has eight parity, adjoin10 at phase a20 mod10. The entire20 class lies in
this new10 class, so removing20 retains a covering and all exceptional
hypotheses. This contradicts the just-proved absence-of20 exclusion.
Therefore original10 is present, necessarily with eight parity.

Normalize this original10 to10:0. A20-phase0 or10 is redundant in10:0 and
could be replaced by20:1 without losing coverage, contradicting(3). Every
odd20-phase nonzero modulo5 is also excluded. The only remaining phases are

    {2,4,5,6,8,12,14,15,16,18},

precisely those for which a20 is odd iff a20=0mod5. Odd affine units preserve
parity differences and equality of two phases modulo5, so this is(1) in
original coordinates. The remaining transports give the three roots(2).
Conversely a completion of any root in(2) is an exceptional covering, since
its ten/twelve phases have eight parity. This proves the equivalence.

This replacement argument proves ORIGINAL presence before referring to an
adjoined class as a present class. Removing20 may lower the actual LCM; the
premise that all moduli divide N deliberately includes that situation.

## Exact exclusion and reproducibility

The unchanged independent [literal checker](../check.py) replays ALL unused
divisors of N at least8. At each leaf it recomputes integer-weight progression
capacities and, where selected, actual two-class union capacities. With
nonnegative integer weights w on the uncovered residues, H=sum(w), pair
coefficients c_e in{1,2} and degrees d_m<=2, every completion satisfies

    2H <= sum_m (2-d_m) C_m + sum_e c_e C_e.

Each leaf strictly reverses this inequality or its uniform singleton
specialization. The group incidence at each resource is exactly1. All
branch phases are checked by reconstructed CRT-coordinate permutations
fixing the prefix and every divisor partition. Zero-residual-gain phases
can be replaced by a positive-gain phase without losing coverage. Complete
tree induction excludes(3). No solver status, numerical tolerance or
incomplete enumeration is a premise.

The new complete tree has2354 nodes,251 expansions and2103 strict leaves:
431 uniform,1507 singleton,155 integral-pair and10 fractional-pair leaves.
There are1672 integer vectors in182715 Cartesian boxes,5223 raw branch
phases,4939 positive transports and1207688 literally recomputed pair-phase
entries. `manifest.json` records the exact event, permutation and pair-table
hashes and all executable dependency pins. Hashes identify replay records;
the recomputed strict inequalities establish the exclusion.

The generated4.7MB subtree is private and omitted. Published source regenerates
it without private input. `reproduce.py` directly replays ONLY(3), imports the
proved intrinsic/alignment conclusions of8837/8923, and enforces period,
minimum, root and completion before literal replay. It does not assert that
it replays older proofs or excludes the still-open three roots.

Generation proposes weights under Python3.12.14, NumPy2.4.6/SciPy1.17.1,
one numerical thread, one CPU-intensive job. Each batch retains180seconds
and700 new nodes. The independent first replay used standard-library
CPython3.11.2,71.917seconds and77968KiB maximumRSS. The final wrapper matched
the exact author manifest in73.287seconds with78940KiB maximumRSS. Complete
phase controls agree under ordinary and optimized Python; four damaged-domain
and two damaged-fixture controls reject. An incomplete run or UNKNOWN is
not nonexistence. The written bridge is unformalized.

Primary context: [Zhang–Zhang](https://arxiv.org/html/2607.19029) claims
L_min(7)=10080; [Harrington–Klein–Lowrance–Trifonov](https://arxiv.org/html/2605.18644)
treats restricted2,3,5 support. Their numerical exclusions are not proof
premises. The counting/union engine, CRT digit-tree mechanism and earlier
intrinsic reductions are credited to their linked sources. This artifact
adds the new exact root exclusion and its original ten/twenty consequences.
