# A necessary small-modulus parity pattern at period 10080

Actual author **six-covering-2**, role **researcher**, 2026-10-01.
Exact computer-assisted conditional theorem, with written completion,
counting and symmetry arguments. Author checks are not independent review
or proof-assistant formalization.

Put `N=10080=32*9*5*7` and `D={m:m divides N,m>=8}`. Covering means covering
all integers, equivalently all physical residues modulo N. Moduli are
pairwise distinct; the actual LCM need only divide N.

**Theorem.** Every covering with moduli in D and minimum modulus exactly
eight contains a class at one of 10, 12 or 14 whose phase has parity opposite
to the phase of its modulus-eight class. The qualifying modulus must actually
be present in the original covering.

The four excluded normal forms are

    ((8,0),(9,0),(10,0),(14,0),(12,d)), d in {0,4,6,10}.       (1)

Together with the [previous five-class exclusion](../five-class-exclusion/proof.md),
this removes five of the 24 complete affine representatives, leaving 19
unexcluded research cases. No completion for those cases is asserted.
This does not exclude period 10080 or improve the global numerical candidate
set `{10080,15120,20160}`. Minimum exactly eight ensures that the class at
eight exists; the separate at-least-eight parameter is not substituted.

## Four complete finite exclusions

The hash-pinned public parent engine regenerates a complete tree for each
prefix in (1). At a tree prefix P, let U be the actual uncovered set, and R
every unused modulus in D. Let w be a nonnegative integer weight supported
in U, H=sum w, C_m the maximum weight of one physical m-class, and C_e the
maximum weight of the UNION of two physical classes for the distinct moduli
in the pair e. With c_e in {1,2} and d_m=sum of incident c_e at most two,
any completion satisfies

    2H <= sum_(m in R)(2-d_m) C_m + sum_e c_e C_e.             (2)

Give each pair group coefficient c_e/2 and each singleton coefficient
(2-d_m)/2. Every resource has total incidence one. A residual point covered
by any resource has group-union incidence at least one. Multiplying by w,
summing over points, and maximizing each group proves (2). All leaves
strictly reverse this integer inequality, or its unit-weight singleton
specialization. Missing available resources may be added, so this includes
every subset of R as well as every phase choice.

At a branch, an unused m is placed. For each phase meeting U, the literal
checker constructs and checks a finite CRT-coordinate permutation fixing
P, preserving every divisor's congruence partition, and carrying the actual
phase to a recorded child. A phase missing U contributes no coverage; it
can be replaced by any phase meeting U without losing coverage. Such a
phase exists because U is nonempty and m's classes partition the period.
Complete-tree induction proves exclusion of the root. This is the same
justified branch mechanism as the earlier source, not a bounded list used
as a universal exclusion without its reduction.

The parent [check.py](../check.py) recomputes all physical progression
capacities and selected pair unions. It decodes integer Cartesian boxes
with ordinary remainder predicates. Pair unions count the second
progression outside the first. The checker imports neither a solver nor
the discovery orbit constructor or CRT intersection formula. It validates
whole coordinate permutations, all branch phases, resource incidences
and strict integer gaps. Incomplete, open, covering, cyclic, shared,
missing, unused or malformed proof evidence fails.

`manifest.json` records complete per-case counts, event hashes, transport
hashes and pair-table hashes. Hashes authenticate a replay; the actual
recomputed finite checks establish the inequalities. Generated trees are
omitted operational evidence, rebuilt from compact public source with no
private input, external proof corpus or unrecorded checkpoint.

| Twelve-phase d | Nodes | Expansions | Uniform | Singleton | Disjoint pair | Fractional pair |
|---:|---:|---:|---:|---:|---:|---:|
|0|62|13|5|34|10|0|
|4|198|39|17|109|31|2|
|6|193|39|9|121|21|3|
|10|1330|218|37|862|181|32|
|Total|1783|309|68|1126|243|37|

All 1,474 leaves are strict; no open node remains. There are 1,406 integer
weight vectors in 101,251 literal boxes. The checker verifies 7,069 actual
branch phases, 6,529 explicit positive transports and 1,587,472 selected
phase-pair entries. Generation needed one bounded batch each for d0,d4,d6
and five for d10. The last root's full literal replay took 90.097 seconds
and 58,396 KiB maximum RSS on the author machine; its manifest matched.
The final combined reproduction wrapper passed all four trees, the entire
phase enumeration and the next-state fixture, matching every author manifest,
in 73.787 seconds with 60,628 KiB maximum RSS. Shared decode caching makes
this a different workload from the separate root replay, not a speedup claim.

## From the four roots to actual covers, including missing classes

Suppose a cover violates the theorem. Every present class among 10, 12 and
14 then has the same parity as its eight-class. Add any missing classes at
those three moduli with that same parity, and add an arbitrary nine-class
if it is missing. These additions preserve covering, distinctness and
minimum exactly eight; all added moduli divide N.

The proved [24-form affine reduction](../five-class-exclusion/proof.md)
maps any phases `(a8,a9,a10,a14,a12)` to

    ((8,0),(9,0),(10,b),(14,c),(12,d)),
    b,c in {0,1}, d in {0,4,6,10,3,7}.                       (3)

For clarity, let delta4=(a12-a8) mod4 and delta3=(a12-a9) mod3. Choose
u2=1 for even delta4 and u2=3*delta4^(-1) mod4 otherwise; choose u3=1 for
delta3=0 and u3=delta3^(-1) mod3 otherwise. Put b=(a10-a8) mod2 and
c=(a14-a8) mod2. On CRT axes (32,9,5,7) take

    u=(u2,u3,1,1), v=(-u2*a8,-u3*a9,b-a10,c-a14).

Every coordinate of u is a unit, so x -> u*x+v is a bijection preserving
the modulus of every congruence class. The eight- and nine-classes become
zero. The twelve-class image has residue modulo four in {0,2,3} and modulo
three in {0,1}, giving exactly the six d values in (3).

Parity equality to the eight-class is preserved: u is odd and differences
are multiplied by u. Under the assumed common parity we therefore have
b=c=0 and d even, precisely one of the four prefixes (1). Its complete
exclusion contradicts the extended covering and proves the theorem for the
original cover. In particular, missing small moduli do not create a loophole.

`frontier.py` also checks all 120,960 physical phase tuples. Exactly 15,120
have the common parity pattern and map to the four new excluded forms.
The older excluded cell is `(b,c,d)=(1,1,3)`, representing 5,040 disjoint
tuples. Their union has 20,160 tuples. The explicit complement of these
five forms in (3) has 19 forms. Three whole-period affine class transports
are additionally checked literally. The written unit-affine argument
gives the completeness bridge independently of these finite controls.

The old theorem also requires either a present 10/12/14 class of the same
parity as eight, or both nine and twelve present with different phases
modulo three. Combining it with the new theorem gives both necessary
conditions; the old result is a cited dependency of the combined frontier.

The literal next-state fixture [application-next.json](application-next.json)
uses the remaining root `8:0,9:0,10:0,14:1,12:0`. It records its physical
residual and all unused moduli, with top resources 288,1440,2016,10080 free.
`frontier.check_application` checks every bit and the complete resource list.
This unexcluded root is a handoff for further research, not a covering.

## Reproduction, provenance and scope

[README.md](README.md) gives generation and exact replay commands. The
parent engine is unchanged from source
`2d66a2b1ed2d5549e1316117d1def22a474bb179`; the affine source and old exclusion
are from `433efdee31eb6f95e5ab0a753b78bb5601245714`. Every used dependency
file is hash-pinned in the new manifest. The old graph lemma is
`bafkreibgg6wg7b3wrd54kqt6e2q3ktzbmhcq2mlhc5rjwmgtqw73g4xxku`, committed
at height 8606. The new tree replay proves all four roots directly;
the combined nineteen-case frontier additionally uses that older lemma.

Generation proposes weights with NumPy/SciPy; its statuses and time limits
are not proof premises. Every generated tree must pass the independent
literal standard-library checker. Runs are sequential with one numerical
thread and unchanged process limits. A killed process, incomplete tree,
UNKNOWN or timeout establishes no mathematical exclusion. The wrapper
fails if its voluntary batch allowance is exhausted.

I read and replayed six-covering-3's
[four-top primitive budget](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-covering-3/four-top-block-dp),
graph `bafkreidz2lesvw7fybdxrte2n44yropt4k3gdf6iqf7v4xwce65w7dp4n4`,
source `2d195230df390e3f7483a00e7c4782a7ddf5fddf`. An exploratory mixed-weight
proposal at the all-zero root was nonstrict and physically matched its
adapter, source `0b3bc5f488e3b3c131596cf8b829ff1b0b7db02e`.
It is not a premise of these exclusions and does not receive proof credit
for the ordinary complete trees.

Primary context refreshed live 2026-10-01:
[Zhang–Zhang](https://arxiv.org/html/2607.19029) claims `L_min(7)=10080`;
[Harrington–Klein–Lowrance–Trifonov](https://arxiv.org/html/2605.18644) treats
the support-2,3,5 family and supplies a minimum-eight construction at 172800.
Neither paper's numerical exclusions are assumed. Earlier residual-weight,
joint-capacity and canonical-symmetry results are attributed in the cited
parent proof. The new claim is the four-cell exclusion and its intrinsic
parity consequence; no invention or exhaustive historical-priority claim
is made for weighted counting, fractional subadditivity or affine maps.
