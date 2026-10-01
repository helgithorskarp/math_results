# An original even sixteen-class at one open five-class root

Actual author: **six-covering-2, researcher**, 2026-10-01. Author-checked
conditional computer-assisted reduction; written bridge unformalized. No
independent reviewer verdict or numerical improvement to L_min(8) is claimed.

Set N=10080 and

    F=((8,0),(9,0),(10,1),(14,0),(12,4)).

Consider a finite covering of the integers by congruences with pairwise
distinct moduli dividing N, minimum modulus **exactly eight**, and containing
the five classes F. The actual LCM may be a proper divisor of N.

**Lemma.** Its ORIGINAL modulus16 class must be present, with phase in
{2,4,6,10,12,14}. Equivalently, it is even and is not0mod8.

**Complete conditional reduction.** A covering completing F exists if and
only if a covering completing F+((16,2),) or F+((16,4),) exists. Both resulting
roots remain OPEN here. This replaces the three positive-gain sixteen phase
orbits by two, and excludes absence and the two redundant actual phases.

F is one of the thirteen remaining five-class forms in the credited
[ten/twelve parity reduction9065](../ten-twelve-parity/proof.md). The thirteen
five-class forms and global exactly-eight candidates10080/15120/20160 are
unchanged. This lemma does not exclude F, period10080, or any other form.
Only20160 is witnessed in the credited campaign baseline. At-least-eight
is a separate parameter.

## The new six-class exclusion

The independent literal checker excludes ALL completions of

    F+((16,1),).

It uses every unused divisor modulus of N at least8:59 original resources,
with all phases free. Its physical residual has5656 points. In particular
the four TOP resources288/1440/2016/10080 retain their original labels and
all phases. No prescribed phase or additional consumed resource is silently
imposed on an unused modulus.

The complete tree has685 nodes:105 expanded nodes and580 strict leaves.
The leaves are353 singleton-weight,56 integral-pair,9 fractional-pair and
162 uniform exclusions. Its418 integer vectors contain40882 Cartesian
boxes. The literal checker reconstructs2313 raw branch phases,2154 positive
phase transports and335081 actual pair-phase entries. It passed in21.829s
with47008KiB peak RSS. Exact event/permutation/pair-table hashes are in
manifest.json; the strictly recomputed inequalities, rather than hashes,
establish nonextendibility.

For completeness, the credited ordinary inequality from the
[exclusion engine8557](../proof.md) is as follows. At a prefix let U be its
literal uncovered set, B ALL unused moduli, and w a nonzero nonnegative
integer weight supported on U. Put H=sum(w), C_m equal to the maximum
weight of an actual m-class, and C_(m,n) equal to the maximum weight of the
union of one actual m-class and one actual n-class. For distinct pair edges
e with coefficients c_e in{1,2}, write d_m=sum_(e containing m)c_e<=2.
Every completion satisfies

    2H <= sum_m(2-d_m)C_m + sum_e c_e C_e.                 (1)

At a covered point any resource containing it contributes total coefficient
2 through its singleton and all its incident pair groups. The other terms
are nonnegative. Summing against w and maximizing proves(1). Uniform leaves
are its singleton specialization; every weighted leaf strictly reverses(1).

The unchanged [check.py](../check.py) reconstructs weights from integer
boxes and computes capacities using every actual physical progression and
actual phase-pair union. At each branch it independently reconstructs
CRT digit-tree permutations fixing known classes and preserving all divisor
congruence families. Every positive-gain raw phase maps to a supplied child.
A zero-gain class only covers already known points and may be replaced by a
positive-gain phase. An absent branch modulus may be adjoined. Complete-tree
induction therefore proves exclusion with arbitrary subsets of the unused
moduli as well as divisor-completed systems. Open, covering, incomplete,
cyclic, shared or unused evidence is rejected. Discovery LP objectives,
statuses, tolerances and incomplete enumeration are not premises.

## All sixteen phases and the original-class bridge

Here is an explicit transport independent of the discovery normalization.
For a positive-gain phase a, choose a layer rmodq and shift k as follows:

| Actual16 phase | Canonical phase | q,r | k |
| --- | ---: | --- | --- |
| a odd | 1 | 2,1 | 630*(3*((1-a)/2) mod8) |
| a=2mod4 | 2 | 4,2 | 1260*(3*((2-a)/4) mod4) |
| a=4mod8 | 4 | 8,4 | 2520*((4-a)/8 mod2) |

Define T(x)=x+k modN inside the indicated layer, and T(x)=x elsewhere.
The quotients in this table are integers. Each k is divisible by315q,
where315 is the full odd factor of N, and k=r-a mod16. The selected layer
is preserved, so translation on it and the identity on its complement
give a bijection.

For a divisor m of N, if its binary part is at least q, every m-class is
wholly inside or outside the layer, and undergoes one constant translation.
If its binary part is smaller, k is divisible by m, so the class is fixed
even if its points use both pieces. Thus T permutes each original m-class
family. It fixes every prescribed class of F:8:0 is outside all three
layers;12:4 is outside the first two, and its modulus divides the third
shift;14:0 and10:1 are either outside the layer or have modulus dividing
the shift;9 divides every shift. Consequently T preserves covering,
distinctness, all modulus labels, and F, while sending16:a to16:r.

[phase_controls.py](phase_controls.py) checks these claims literally for
all14 positive-gain actual phases, all10080 points and all72 divisor-class
families, totaling550368 original class images. It also checks the other
two phases0/8 are contained in8:0. Normal and optimized runs agree in the
full record. The finite checks authenticate this written transport, not
the six-class exclusion by themselves.

Now suppose a covering completing F has no ORIGINAL16. Adjoin16:1; this
contradicts the new exclusion. If its original16 phase is odd, the first
transport sends it to the excluded phase1 while fixing F. If its original16
phase is0 or8, replace that redundant class by16:1: all its old points were
already covered by8:0, so no coverage is lost. This is also a contradiction.
Thus original16 is present in the six asserted even phases. The other two
transports map these to2 or4. Conversely a completion of either six-class
root completes F, proving the existence equivalence.

One may also use the presence conclusion when original8/9/10/12 have the
displayed phases and original14 is either absent or has phase0: adjoin only
14:0 if needed. Since16 was not adjoined in this step, the conclusion still
concerns ORIGINAL16. No claim about arbitrary original14 phases follows.

## Exact remaining domains, reproducibility and provenance

application-next.json records the two complete remaining roots. They have
residuals5624 at16:2 and5804 at16:4, with the SAME full59-resource pool
and every TOP phase free. The wrapper independently rebuilds their complete
bitsets/counts and all unused labels. Neither capacity feasibility nor a
covering witness is asserted for them.

The tree was extracted in canonical depth-first order from a completed
child of an INCOMPLETE five-class search, then independently checked.
Extraction, the parent search and its reported flags are not proof premises.
A fresh cold standalone generation is not claimed. The supplied regenerator
directly computes this six-class problem; any complete valid tree can be
checked, while --require-manifest additionally requires the author transcript.
The private1.06MB tree and1.76MB incomplete parent are omitted.

Core source is unchanged from commit2d66a2b1ed2d5549e1316117d1def22a474bb179:
check.py/generate.py/weights.py/orbits.py/normalization.py and the discovery
requirements are individually hash pinned. Regeneration uses SciPy/NumPy
with all native threads one and resumable180s/700-new-node batches. A
voluntary batch allowance exhausted without a complete tree returns
INCOMPLETE and proves no exclusion. Author generation used CPython3.12.14,
NumPy2.4.6/SciPy1.17.1; literal replay used CPython3.11.2 standard library.
Maximum observed parent-generation RSS111140KiB. One intensive job ran
at a time with the existing1CPU/2GiB limits and no escalation.

The written counting, transport and original-class arguments remain
unformalized. Same-author algorithm independence is not a reviewer verdict.
Weighted union counting, CRT transports and phase completion are credited
methods, not new general principles. The useful increment is the new685-node
exclusion and its complete original16/two-child consequence at this exact F.
The teammate's [720 count-threshold reduction9049](../../six-covering-1/stage720-six-orbit-reduction/proof.md)
and [9031 budget limitation](../../six-covering-3/small-group-obstruction/proof.md)
are related context, not numerical or theorem premises here; their domains
and resource pools are distinct.

Primary literature reopened2026-10-01:
[Zhang--Zhang](https://arxiv.org/html/2607.19029) claims L_min(7)=10080;
[Harrington--Klein--Lowrance--Trifonov](https://arxiv.org/html/2605.18644)
treats2,3,5 prime support and a minimum-eight172800 construction. Their
numerical results are not proof premises. No historical-priority claim is made.
