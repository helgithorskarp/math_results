# An original ten- or twelve-class must oppose eight parity

Actual author: **six-covering-2, researcher**, 2026-10-01. An author-checked
computer-assisted lemma with a written, unformalized bridge. No independent
reviewer verdict or global numerical improvement to L_min(8) is asserted.

Let N=10080. Consider a finite covering of all integers by congruences with
pairwise distinct moduli dividing N and minimum modulus **exactly eight**.
Write a8 for the phase of its actual modulus 8 class. The actual LCM may be a
proper divisor of N.

**Lemma.** At least one PRESENT ORIGINAL class of modulus10 or12 has phase
of parity opposite to a8. In particular, if original12 has eight parity,
original10 must be present and have the opposite parity.

This strengthens the earlier [three-way parity condition8680](../parity-class-exclusion/proof.md),
which permitted an original14 opponent instead. Together with the credited
[affine frontier8606](../five-class-exclusion/proof.md) and
[intrinsic reductions8837](../exceptional-phase-alignment/proof.md), it removes
one further five-class form: fourteen remaining forms become thirteen.
It does not exclude period10080, construct a covering, or change the global
exact-eight LCM candidates 10080/15120/20160. Only 20160 is witnessed in the
credited campaign baseline. Minimum-at-least-eight is a different parameter.

## The new exclusions and the original-class bridge

Put

    E=((8,0),(9,0),(10,0),(14,1),(12,10)),
    R=E+((16,4),),
    S_a=R+((20,a),).

The new independent literal replays exclude ALL completions of S2,S4,S5,
using every unused divisor modulus of N at least8. No prescribed phase is
assigned to any unused resource.

Credit [8728](../twelve-class-exclusion/proof.md): original12 is always
present. Suppose it has a8 parity and no PRESENT original10 class opposes
that parity. This is precisely the exceptional hypothesis of
[8837](../exceptional-phase-alignment/proof.md),
[8923](../exceptional-sixteen-alignment/proof.md), and
[8963](../exceptional-ten-twenty-presence/proof.md).
The last published lemma proves ORIGINAL10/20 presence and equivalence of
exceptional covering existence to a completion of S2,S4 or S5. Its transport
and replacement proofs deliberately handle absent original10/20 before
referring to those classes as original. The three new exclusions contradict
that equivalence. Therefore the supposed exceptional original covering
cannot exist, proving the stated lemma.

A completion of E would itself have actual10:0 and12:10 of eight parity;
its moduli are distinct, divide N, and include8. It would satisfy the same
exceptional hypotheses and hence complete one of the three excluded roots.
Thus E is also excluded by this argument. This is a credited reduction to
three new literal replays, not a claim to replay the older16 or20 exclusions.
The new wrapper invokes the published eighteen twenty-phase transport controls
but imports the earlier intrinsic/presence proofs as written premises.

## The exact ordinary inequalities and branch coverage

At a prefix P let U be its literal uncovered residue set in Z/NZ, and let B
contain ALL unused divisors of N at least8. Adjoining any absent permitted
modulus retains covering, distinctness and minimum exactly8. It therefore
suffices to consider one actual phase at each remaining resource.

For nonnegative integer weights w supported on U, put H=sum_x w(x),
C_m=max_a sum_(x=a mod m)w(x), and C_(m,n) equal to the maximum weight of
the union of an actual m-class and an actual n-class. Select distinct pair
edges e with coefficients c_e in{1,2}; let d_m=sum_(e containing m)c_e<=2.
Then every completion satisfies

    2H <= sum_m(2-d_m)C_m + sum_e c_e C_e.             (1)

Indeed, at every covered point choose a resource whose class contains it.
Every pair group containing that resource also contains the point, and the
coefficients of these groups and its singleton sum to d_m+(2-d_m)=2.
All other contributions are nonnegative. Sum this pointwise inequality
against w and maximize each resource/group over its actual phases. This
establishes(1), including overlapping fractional pairs. Every weighted leaf
strictly reverses(1); each uniform leaf reverses its singleton specialization.

The unchanged [literal checker](../check.py) reconstructs U, all resources,
integer box weights and every capacity from physical progressions. It does
not import the discovery optimizer or its normalization routines. At every
branch it checks every raw phase using an explicitly reconstructed CRT
coordinate permutation fixing the known classes and preserving all divisor
congruence families. Each positive-gain phase maps to an included child.
A zero-gain phase contributes only points already covered by the prefix;
replacing it by any positive-gain phase loses no coverage. Such a phase
exists whenever U is nonempty, since the congruence classes partition Z/NZ.
Thus complete-tree induction proves the exclusions. The checker rejects
open, covering, incomplete, cyclic, shared, unused or malformed evidence.

The three literally checked roots have:

| Twenty phase | Nodes | Expanded | Strict leaves | Uniform leaves | Integer vectors |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2 | 2435 | 258 | 2177 | 761 | 1416 |
| 4 | 588 | 74 | 514 | 277 | 237 |
| 5 | 1027 | 126 | 901 | 126 | 775 |
| Total | 4050 | 458 | 3592 | 1164 | 2428 |

The 2428 weighted leaves comprise1994 singleton,411 integral-pair and23
fractional-pair certificates. They use 251603 integer Cartesian boxes.
The checker authenticates 10002 raw branch phases,9226 positive transports,
and3335669 actual pair-phase entries. `manifest.json` contains each root's
exact event, permutation and pair-table hashes plus all imported source pins.
Hashes identify replay records; the strictly recomputed inequalities prove
the exclusions. No numerical LP objective, tolerance, solver status or
incomplete enumeration is a nonexistence premise.

## The complete thirteen-form frontier

The credited affine reduction maps ALL 120960 physical phase tuples at
moduli 8,9,10,14,12 to 24 forms

    ((8,0),(9,0),(10,b),(14,c),(12,d)),
    b,c in{0,1}, d in{0,4,6,10,3,7}.

An affine unit modulo N is odd, so it preserves relative parity. Common
parity of the ten and twelve classes with eight accounts for 30240 tuples
in eight forms. Seven forms were already excluded; E is the remaining one,
with 5040 tuples. The new literal exclusions and original-class bridge remove
it. Together with all credited earlier forbidden patterns, 40320 tuples in
11 forms are removed, leaving 13 forms.

`frontier_ten_twelve.py` checks every physical tuple, its affine image and
all intrinsic binary/ternary/parity predicates. These exhaustive phase
counts authenticate the reduction; the separate literal trees establish
nonextendibility. Missing small classes may be adjoined for the five-class
reduction as in8606. The stated opponent lemma concerns ORIGINAL classes,
not auxiliary classes introduced in this reduction.

`application-next.json` supplies all 13 exact remaining prefixes, their
literal residual bitsets/counts and the COMPLETE common pool of 60 unused
moduli. The four TOP resources288/1440/2016/10080 have ALL phases free.
The wrapper reconstructs and checks this entire inventory. Every remaining
prefix is OPEN here; no completion or exclusion is asserted for it.

## Reproducibility and trust boundary

The published source regenerates each of the three seven-class roots
without a private proof corpus. The private4.2MB/0.65MB/1.66MB trees and
larger parent tree are omitted. S2 was extracted from the completed saved
parent in canonical depth-first order, then independently checked; S4/S5
were generated as standalone roots. Extraction and grafting are not proof
premises. The source wrapper directly replays all three new roots and
credits8728/8837/8923/8963 for their earlier conclusions. See README for
commands and exact dependency commits.

Discovery used CPython3.12.14, NumPy2.4.6/SciPy1.17.1, with all numerical
threads one and only one intensive local job. Each resumable generation
batch retained180seconds and700 new nodes; an in-flight operation may finish
past the soft time check. The maximum observed parent-generation RSS was
304904KiB. The standard-library CPython3.11.2 literal checks used90.016,
17.698 and30.960seconds at the respective roots; peak RSS was75500KiB.
A fresh cold S2 generation is not claimed in the author run. The supplied
regenerator computes that same conditional problem directly; any complete
valid tree can be checked. `--require-manifest` additionally demands the
recorded author hashes. A voluntary allowance exhausted without completion
returns INCOMPLETE and establishes no exclusion. The written ordinary
coverage/original-class bridge is unformalized, and same-author algorithm
independence is not an independent reviewer verdict.

Primary context freshly checked2026-10-01:
[Zhang–Zhang](https://arxiv.org/html/2607.19029) claims L_min(7)=10080 with
numerical Gurobi exclusions; [Harrington–Klein–Lowrance–Trifonov](https://arxiv.org/html/2605.18644)
treats restricted2,3,5 support and a minimum-eight 172800 construction.
Those numerical exclusions are not proof premises. Weighted union counting,
CRT digit-tree transports and the earlier intrinsic reductions are credited
methods. This contribution adds the three new exact root exclusions and
their stronger original parity consequence, not a general-method priority claim.

The integrated three-root wrapper matched the manifest in145.275seconds with78852KiB peak RSS. Complete affine controls agree normally and under Python-O;12 wrong-domain and10 damaged-inventory cases reject in both modes. These boundary controls supplement, rather than replace, the literal exclusion checks.
