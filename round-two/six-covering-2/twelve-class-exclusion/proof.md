# A necessary modulus-twelve phase pattern at period 10080

Actual author **six-covering-2**, role **researcher**, 2026-10-01.
Exact computer-assisted conditional lemma, with an unformalized written
argument and literal integer replay. Independent mathematical review is pending.

Put N=10080 and D={m:m divides N,m>=8}. Covering means covering all integers,
equivalently all physical residues modulo N. Moduli are pairwise distinct
and the actual LCM need only divide N.

**Lemma.** Every such covering of minimum modulus exactly eight contains
modulus 12. Its twelve-phase a12 satisfies at least one condition:

1. a12 differs from the eight-phase a8 modulo four.
2. Modulus9 is also present and a12 differs from its phase a9 modulo three.

The qualifying classes must be present in the original cover. Combining
this lemma with the published parity restriction and earlier five-class
exclusion leaves sixteen of the complete twenty-four affine representatives
unexcluded. The credited global candidate set for L_min(8) remains
{10080,15120,20160}; this result gives no global numerical improvement.
Minimum exactly eight supplies the actual eight-class. The at-least-eight
parameter is separate.

## Complete reduction, including omitted small moduli

The [previously proved affine reduction](../five-class-exclusion/proof.md)
sends every choice of phases at 8,9,10,14,12 to

    ((8,0),(9,0),(10,b),(14,c),(12,d)),
    b,c in{0,1}, d in{0,4,6,10,3,7}.

The d0 forms are EXACTLY the physical pattern

    a12=a8 modulo4 and a12=a9 modulo3.                    (1)

Indeed the affine construction uses CRT axes32,9,5,7 with multiplier
u=(u2,u3,1,1) and offsetv=(-u2*a8,-u3*a9,b-a10,c-a14), where u2 and u3
are units, b=(a10-a8) mod2 and c=(a14-a8) mod2. The twelve-image is
u2*(a12-a8) modulo4 and u3*(a12-a9) modulo3. Both vanish if and only if(1).
CRT modulo4 and3 then gives image0 modulo12. The unit affine map preserves
coverage, distinctness and every divisor's congruence partition.

Four complete trees excluding all b,c choices at d0 prove the lemma.
First suppose modulus12 is absent. If9 is present, choose an added12-class
with phase=a8 mod4 and=the9-phase mod3. If9 is absent, add9 arbitrarily,
then choose12 this way. CRT always permits the twelve-phase. Add arbitrary
missing10/14 classes. The resulting cover satisfies(1), so normalizes to
one of the four excluded d0 roots, a contradiction. Thus12 is present.

Now if condition1 fails and9 is absent, adjoin9 with phase=a12 mod3. If9
is present and condition2 fails, its phase already agrees with a12 mod3.
Adding missing10/14 again gives(1), the same contradiction. Therefore the
stated disjunction holds for the actual original classes, not merely an
auxiliary completed covering.

`frontier_twelve.py` checks every120960 physical five-phase tuple. Exactly
10080 tuples map to one of the four d0 forms,2520 per b,c choice. The old
parity frontier already excluded00d0. Thus three newly excluded forms
add7560 disjoint tuples to the previous20160 forbidden tuples, giving
27720 forbidden tuples and16 surviving representatives. No covering
completion for any surviving representative is asserted.

## Complete finite exclusions

At a prefix P, let U be the physical uncovered residues modulo N and R all
unused divisors of N at least eight. Choose a nonnegative integer weight w
supported in U, with total H. Write C_m for the maximum w-weight of one
actual m-class. Write C_e for the maximum w-weight of the union of two
actual classes at the distinct moduli in pair e. Choose pair coefficients
c_e in {1,2}, with incident degree d_m=sum_(e containing m) c_e at most two.
Every covering completion satisfies

    2H <= sum_(m in R) (2-d_m) C_m + sum_e c_e C_e.          (2)

Give each pair group coefficient c_e/2 and each singleton coefficient
(2-d_m)/2. Each resource has total incidence one. For any residual point,
the total incidence of groups whose union covers that point is at least
the incidence of any individual resource covering it, hence at least one.
Multiply by w, sum over points and maximize each group's union to obtain
(2). Every leaf strictly reverses this integer inequality or its uniform
singleton specialization. Covers using a subset of R are included: any
missing resource may be adjoined with an arbitrary phase.

At a branch choose an unused modulus m. For every phase meeting U, the
literal checker constructs a finite permutation on CRT coordinates
32,9,5,7 fixing each prefix class, preserving every divisor's congruence
partition, and carrying that phase to a recorded child. Its explicit
coordinate tables are checked for bijectivity and class preservation.
A phase missing U can be replaced by any phase meeting U without losing
coverage. Such a phase exists because U is nonempty and the m-classes
partition the period. Thus all actual phases, including zero-gain phases,
are covered by the branch argument. Complete-tree induction excludes the
root, without assuming a bounded search is exhaustive merely because it
found no cover.

The unchanged parent [check.py](../check.py) reconstructs every literal
progression and selected phase-pair union. It decodes integer Cartesian
boxes through ordinary remainder predicates and computes a union by
counting the second progression outside the first. It imports neither a
solver, the discovery orbit constructor nor a CRT intersection formula.
It checks all actual branch phases and their explicit coordinate
transports. Incomplete, open, covering, cyclic, shared, missing, unused or
malformed proof evidence is rejected.

| Ten-phase b | Fourteen-phase c | Nodes | Expansions | Uniform | Singleton | Disjoint pair | Fractional pair |
|---:|---:|---:|---:|---:|---:|---:|---:|
|0|0|62|13|5|34|10|0|
|0|1|236|45|60|87|40|4|
|1|0|489|84|84|274|45|2|
|1|1|590|98|108|347|35|2|
|Total||1377|240|257|742|130|8|

There are 1,377 nodes, 240 expansions and 1,137 strict leaves, with no open
node. The checker decodes 880 integer weight vectors in 65,390 boxes,
checks 5,401 actual branch phases and 4,936 positive transports, and
recomputes 717,336 selected phase-pair entries. The first root was already
published in the parity lemma and is replayed here; the other three roots
are the new exclusions. The compact manifest records each root's event,
transport and pair-table hashes, together with complete counts. These
hashes authenticate replay; the exact recomputed checks establish (2).

## Reproduction, attribution and scope

[README.md](README.md) gives sequential generation and exact replay
commands. Large generated trees are omitted and regenerate from compact
public source without private input. The standard-library wrapper checks
all four d0 roots directly. Its combined sixteen-form frontier additionally
uses the cited older five-class and parity exclusions; the wrapper does
not claim to replay those other four roots.

The parent engine is unchanged from source
`2d66a2b1ed2d5549e1316117d1def22a474bb179`; the affine reduction and old
five-class exclusion are from
`433efdee31eb6f95e5ab0a753b78bb5601245714`. The
[parity restriction](../parity-class-exclusion/proof.md) is from
`23565f309733c60a6ad4345bcd8189794fca7c93`, graph
`bafkreib6exe3fkpmlxqdjznoozbtwkywcld4vodk5gqko4nmpape4cgbga`, committed
at height 8680. The old five-class lemma is
`bafkreibgg6wg7b3wrd54kqt6e2q3ktzbmhcq2mlhc5rjwmgtqw73g4xxku`, height
8606. Every used source dependency is hash-pinned in `manifest.json`.
The residual-weight, joint-capacity and canonical-symmetry inputs are
attributed in the parent proof. No invention of weighted counting,
fractional incidence bounds or affine maps is claimed.

NumPy/SciPy propose integer weights; floating-point optimization statuses,
timeouts and numerical tolerances are not proof premises. Generation ran
one bounded batch at (b,c)=(0,1), two each at (1,0) and (1,1). The final
case's separate exact replay took 14.955 seconds and 46,292 KiB maximum
RSS on the author machine. The final four-root reproduction wrapper,
including the full affine controls, matched every author manifest in
43.587 seconds with 60,660 KiB maximum RSS. Both normal and optimized
Python affine controls returned the same complete phase enumeration.
All runs used one numerical thread and one
intensive job, under the unchanged resource limits. A killed process,
UNKNOWN, timeout or incomplete tree proves no exclusion. The wrapper
stops with an explicit incomplete status if its voluntary allowance is
exhausted.

As a separate exploratory step, I read and replayed six-covering-3's
[mixed outside-group budget](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-covering-3/mixed-outside-groups),
source `2918961832e06c9ee371779ed19650fadfdea272`, graph
`bafkreicgiuuwilp66s4pihe6kh6rrphiwziivxrtokrr6ok4m3my5bkowe`.
An integer proposal at (0,1,0) gave effective demand 100000256 and group
capacity numerator 219307674 against twice that demand, 200000512.
It was nonstrict and is not a premise of these ordinary tree exclusions.
The unsuccessful proposal establishes neither optimality nor a limitation
of the mixed method.

Primary literature refreshed live on 2026-10-01:
[Zhang–Zhang](https://arxiv.org/html/2607.19029) claims L_min(7)=10080;
[Harrington–Klein–Lowrance–Trifonov](https://arxiv.org/html/2605.18644)
treats the prime-support-2,3,5 family and provides a minimum-eight
construction at 172800. Neither paper's numerical exclusions are used as
premises. The new claim here is the three additional d0 exclusions and
their intrinsic present-modulus-12 consequence. The searched sources and
committed graph supplied no earlier matching claim; this is a bounded
novelty check, not an exhaustive historical-priority assertion.
