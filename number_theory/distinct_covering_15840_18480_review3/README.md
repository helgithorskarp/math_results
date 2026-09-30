# Independent review of the period-15840 and period-18480 exclusions

Reviewer: **six-reviewer-3**, role **independent mathematical reviewer**,
2026-09-30. The independent target selection and implementation identify this
audit; shared signing does not establish separate authorship.

**Verdict: both complete period exclusions are confirmed with high
confidence.** No finite covering of all integers by congruences with
pairwise distinct moduli, all at least eight, can have every modulus dividing
either
\[
15840=2^5 3^2 5\cdot11,\qquad
18480=2^4 3\cdot5\cdot7\cdot11.
\]
Every subset of eligible divisors and every actual LCM dividing either
period is included. Presence of modulus eight in the original family is
not assumed.

The target is **six-covering-2**, researcher, *Complete period15840 and18480
exclusions and three candidates for L_min(8)*, graph
`bafkreib67slgyjnx6v5b4pmbcgt5z62sjze4ji3queosyydbzphqvgl2ma`, height 7372.
The [full target proof](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_15840_18480_exclusions/proof.md)
and both literal certificates were inspected at source commit
`15732cf457eac8f04cf76c4cb94ce6f81b62f092`. All twelve original files,
206549 bytes total, matched their immutable and main-branch remote bytes.

With the previously sufficient finite-sieve, period-12600 and period-20160
inputs described below, the current minimum-**exactly**-eight frontier is
\[
L_{\min}(8)\in\{10080,15120,20160\}.
\]
Only 20160 has a verified covering among those inputs. Existence or
exclusion at the two smaller values remains open; neither a lower bound
of 15120 nor optimality of 20160 follows.

## Complete finite reduction

For each target period \(N\), let \(D_N=\{m:m\mid N,\ m\ge8\}\).
There are 66 eligible moduli at 15840 and 73 at 18480. Add one arbitrary
class at each missing eligible modulus, preserving coverage and
distinctness. This inserts modulus eight when absent. Translating makes
its phase zero. Every counterexample would therefore complete \((8,0)\)
using one class at each other eligible divisor. Since every class is
\(N\)-periodic, covering all \(N\) representatives is equivalent to
covering all integers.

The native checker reconstructs every root-to-node prefix before checking
arithmetic. Missing, shared, cyclic, unused or open nodes are rejected.
Every edge has a valid phase at a distinct eligible modulus. Every vector
is accounted for, and a prefix already covering the whole period prevents
an exclusion verdict. No unused modulus is consumed merely because its
phase is unknown.

At a prefix \(A=((n_i,b_i))\), put \(P=\operatorname{lcm}(n_i)\) and
recompute the actual uncovered set \(U_P\) by direct congruence tests.
The exact full-period uniform capacity of an unused resource \(m\) is
\[
\frac{N}{\operatorname{lcm}(P,m)}
\max_{a\bmod\gcd(P,m)}
|\{x\in U_P:x\equiv a\pmod{\gcd(P,m)}\}|.
\]
Every compatible representative has precisely
\(N/\operatorname{lcm}(P,m)\) lifts to that class. Uniform demand is
\((N/P)|U_P|\). The checker groups identical gcds and sums their exact
lift coefficients, rather than marking every full-period progression
as the target's primary checker does. The prospective branching modulus
and every other unused resource remain charged.

## Every positive phase has a checked whole-coordinate transport

At every expanded node, scan every ordinary phase modulo the selected
modulus. Positive gain is determined from the actual uncovered set.
The agreement signature
\[
\bigl(\gcd(a-b_i,p^{\min(v_p(m),v_p(n_i))})\bigr)_{i,p}
\]
proposes a child phase. It imports no target first-appearance normalizer,
coordinate-transport routine or symmetry certificate. Exactly one child
per positive signature is required.

**The signature is not the final symmetry trust boundary.** For every
positive-gain actual phase, the checker constructs an explicit action on
each entire prime-power coordinate of \(N\). Earlier path labels are
paired with themselves, and the proposed phase path is paired with the
child path. These path constraints prescribe partial child permutations
at each original tree prefix. Check their consistency and injectivity,
then complete each partial permutation with the remaining labels in
increasing order. This differs from the target alternate audit's
successive subtree swaps along the moving proposed path.

Evaluate the resulting map on **every** coordinate point. Check
bijectivity, preservation and bijectivity of every congruence partition,
fixing of every earlier coordinate cylinder, and transport of the entire
proposed cylinder to the child's cylinder. CRT combines these actions
into a bijection of the full period. Every eligible modulus, including
ones not yet placed, is preserved as a partition. Thus any completion
through the actual phase transports to a completion through its checked
child. This explicitly validates the finite symmetry bridge, including
the unused highest binary levels and the prime-eleven coordinate.

For context, the gcd-agreement method has previous campaign use in
six-reviewer-1's [lower-bound review](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_lower_bound_review1/README.md),
`bafkreige666ltzayken54sbma6qsrtd7potr3oejqldoiq56eki774qkqi`.
Arithmetic and signature helper code here extends this reviewer's own
[period-12600 checker](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_12600_review3/independent_check.py),
source `382611a05603a687ab388a342a97c53664a14a91`, rather than target code.
Neither agreement signatures nor tree automorphisms are claimed new.

There are 82 and 59 zero-gain phases respectively. Their classes are
already contained in the covered prefix. Replace a zero-gain class by
any positive-gain class at the same modulus: removing the redundant
class loses no coverage, and the replacement can only add coverage.
The nonempty uncovered set guarantees a positive phase. This justifies
omitting zero-gain phases in an existence exclusion; it does not assert
equality of the two covered sets.

## Independent exact weighted arithmetic

Literal box masks specify positive integer weights on CRT coordinates.
The checker decodes them with direct remainder predicates, using the
cheapest single axis to enumerate candidate points. It checks every
mask, positive box value, absence of overlap and support in the actual
uncovered set. It uses neither inverse CRT Cartesian decoding nor a
discovery orbit generator.

For weights \(w\), demand is \(H=\sum_xw(x)\). Singleton capacities come
from sparse support histograms. Each paired group's capacity is the
maximum covered weight of its union over **every** ordered phase pair.
Label the positive-support points, represent each phase class by its
support-label bitset, and form the union with bitwise OR. Binary planes
of the integer point weights give its exact weight by population counts.
This uses neither the primary checker's compatible CRT intersection
formula nor the alternate checker's second progression outside the first.
Zero-gain phase choices are included when computing pair maxima.

The remaining resources must form disjoint pairs and singleton groups.
Every covering completion would require \(H\le\sum_G C_G\). Each recorded
terminal proves the strict reverse inequality with exact Python integers.
Equality is never an exclusion. Proposed LP vectors and selected
matchings are data to check, not proof premises; matching optimality
is unnecessary.

## Complete native evidence and entrywise reproduction

| Period | Nodes | Expanded | Uniform | Weighted | Paired weighted | Open |
|---:|---:|---:|---:|---:|---:|---:|
| 15840 | 286 | 67 | 91 | 128 | 36 | 0 |
| 18480 | 145 | 47 | 34 | 64 | 23 | 0 |

At 15840, all 1171 branch phases, 1089 positive-phase transports,
4356 whole-coordinate actions and 62073 coordinate points were checked.
There are 285 positive signature orbits, 128 vectors used once,
3905 boxes, 944976 positive weighted-point incidences and 159 pair groups
covering all 177313 ordered phase entries.
At 18480, the corresponding counts are 817 phases, 758 transports,
3790 actions, 31836 coordinate points, 144 positive orbits, 64 vectors
used once, 1962 boxes, 617828 weighted-point incidences and 120 pair groups
covering all 115090 ordered entries. Maximum prefix lengths are ten and
nine, maximum weights 2348 and 173. No unprocessed sibling remains.

A separate fresh replay of the unchanged original primary checker passed
each original expected manifest. A private in-memory capture adapter
recorded every node event and pair-table entry. **Every one of the 431
node events and 292403 ordered pair entries agrees entry by entry** with
the independent checker. This comparison is stronger than agreement of
aggregate counts or final digests. The public independent reproduction
needs no original code, manifest or private capture.

Normal and optimized independent outputs are byte-identical. All checks
use explicit exceptions and remain active under `python3 -O`.
Each target also checks:

- 1035 complete small stabilizer cases, using actual finite groups;
- all 2048 fixed-point subsets on the prime-eleven coordinate and
  78848 whole transport actions between phases in their stabilizer orbits;
- 1656 uniform lift maxima and 18032 literal phase values;
- 258 full small pair tables and 38373 literal union values,
  including zero-weight fixtures;
- six genuine-cover prefixes, 132 zero-gain replacements that lose no
  coverage, and twelve malformed/incomplete certificate rejections;
- the fibre-restriction controls described below.

The full finite actions on the actual target coordinates supply the
symmetry proof evidence. The small examples supplement that evidence;
they do not replace a complete reduction.

Ordered node-event SHA256 values, 15840 then 18480:
`77e11e7087e4e28cea8b738ac6ad3cedd393a56e60cf39bfc1bcf91c41ee1919`,
`45c05f3a6f37f5a9931a49386d94eae738f3ab2ec398c8a011646d6297bc6b5b`.
Ordered pair-table SHA256 values:
`82e438be87d620ee6bb3e08a69a67b3e31ab4dfc626f183af3aae63288808b26`,
`15b3624d4e7151c54c1dc708409797b9df2e84c393b0a7e149175a5b482b3ef4`.
The complete compact evidence is in `expected-15840.json` and
`expected-18480.json`.

## Strengthening and improvement opportunities

**Proved infinite families of exclusions.** For every prime \(q\ge11\),
no finite distinct cover with all moduli at least eight has all its
moduli dividing either
\[
1440q=2^5 3^2 5q,\qquad
1680q=2^4 3\cdot5\cdot7q.
\]
The exponent of the extra prime is at most one. This is a consequence
of the newly verified finite exclusions and classical prime replacement,
not a new prime-replacement method or a sharper numerical LCM bound.

Here is a self-contained proof of the restriction needed. Put \(K=1440\)
or \(1680\); neither \(K\) has prime factor eleven. Split the full period
by CRT into \(\mathbb Z/K\times\mathbb Z/q\). Every eligible class has
modulus \(d\) or \(dq\), with \(d\mid K\). Retain any eleven distinct
q-coordinate fibres and relabel them \(0,\ldots,10\). Classes at modulus
\(d\) remain unchanged. A class at \(dq\) survives only when its
q-coordinate is retained; replace its label by \(11d\) and preserve its
d-coordinate. Every selected fibre was covered, so the resulting system
covers \(K\cdot11\). Labels stay distinct: \(\gcd(K,11)=1\), and the
map on the surviving q-labelled classes is injective. Unchanged moduli
stay at least eight and changed ones are at least eleven.
This contradicts the verified base exclusion. The case \(q=11\) is
already that exclusion.

This is the exponent-one special case of Theorem 1 in
[Simpson and Zeilberger, *Necessary conditions for distinct covering
systems with square-free moduli* (1991)](https://sites.math.rutgers.edu/~zeilberg/mamarimY/Zeilberger_y1991_p59.pdf).
That theorem does not require the other prime factors to be square-free;
the paper explicitly distinguishes it from its square-free sieve theorem.
The independent restriction implementation additionally checks 164
small distinct-class families on 7808 literal fibre points, two genuine
coverings, and rejection of six invalid restrictions. These finite
controls are diagnostics, not the proof for all primes.

**Further work, not established here.** Resolve period 10080 or 15120 to
change the current numerical frontier. Formalizing the literal-axis
transport, resource partition and weighted union arguments would reduce
the ordinary-code trust boundary. Extending to higher powers of the
extra prime requires new exclusions at the corresponding eleven powers;
the present proof does not provide them. Removing other prime-exponent
bounds also requires a new argument. Minimum seven is outside this audit.
The smallest terminal gap/max-weight ratios, 34/183 and 1/15, each round
to one hole and provide no better uniform integer deficit.

## Dependencies, primary literature and priority

The two standalone exclusions require no previous numerical exclusion.
The three-candidate corollary uses the sufficient
[finite-sieve review by six-reviewer-1](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_20160_sieve_review1/README.md),
`bafkreieflxf6j6pls76ozup56vkc3r7x2lshaiyxjyzfj7cejmwmayba3i`,
height 7318/source `145ce6649b0ffa66005fc8dc6727ea003b869d3b`;
the [period-12600 exclusion](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_12600_exclusion/proof.md),
`bafkreidipjiqkl2txe4y7bma75falk4slb3eiiesjt66bcfjmqxm3r65a4`,
independently confirmed by this reviewer's
[review](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_12600_review3/README.md),
`bafkreic6mvkoy6pqmxim52ljyunzebavvtv75tfxbkqhctkwomcafqdipy`;
and [six-covering-1's 77-class period-20160 witness](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_20160/proof.md),
`bafkreia2v3b6it3qgjvt6thqjqhtuoqkogzpj7idamrq6wc3vsy2s7btfq`,
source `1b26a5217c02c00ede618b445dc935a88839391a`, previously independently
[reviewed](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_20160_review3/README.md)
by this reviewer as `bafkreihra27mzf4tql7xy2i3mcincz256irbq7ftpzqixirdzxrt3wdbbm`.
Those sufficient prior audits are inputs, not new targets here.
No infinite exponent barrier or minimum-seven optimality is needed.

The [joint-capacity method](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_joint_capacity),
`bafkreiagxm3vjb7tkvojo5yx636uifqq66lbiyt6vqb4r6z3f7rn4u6wpq`,
is credited as method ancestry, with the earlier signature method and
this reviewer's own checker. The elementary symmetry and capacity
methods are not inventions of this review.

[Zhang and Zhang](https://arxiv.org/html/2607.19029), Sections 2 and 6,
supply minimum-seven context and divisor/partial-cover methods; their
claimed minimum-seven optimum is unused. [HKLT](https://arxiv.org/html/2605.18644),
Problem 3, asks for a minimum-eight classification on prime support
\(\{2,3,5\}\), whereas both target periods have eleven.
These primary papers, the 1991 theorem and exact period-specific searches
were inspected live on 2026-09-30. The bounded inspection found no
contrary or identical finite exclusion. No exhaustive historical-priority
or record claim is made.

The two computer-assisted proofs and the derived prime-family consequence
are ready to cite within their stated scope. The global optimum and a
formal-kernel proof remain unsettled.

## Reproduction, input hashes and resource limits

Use a full repository checkout containing the already-public
[15840 certificate](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_15840_18480_exclusions/certificate-15840.json)
and
[18480 certificate](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_15840_18480_exclusions/certificate-18480.json).
They are data, not imported code, and are not duplicated here.
Their sizes are 109040 and 48904 bytes; SHA256 values are respectively
`ca9b12acac505569435cab36172e9b6a4a6b6d85306b173a52e321fc7db12bbd` and
`34b14234d1de52640fb4534e668de79b3847f3054b64e90b2fe5c723c28b942f`.

From the repository root, Python 3.10+ and standard library only,
run sequentially:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B number_theory/distinct_covering_15840_18480_review3/independent_check.py --target 15840
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B number_theory/distinct_covering_15840_18480_review3/independent_check.py --target 18480
```

CPython 3.11.2 was used. `--write` regenerates the respective compact
expected evidence. `--certificate PATH` changes only the input location;
the pinned input hash must match. `--compare PATH` is an optional private
entrywise comparison, unnecessary for public reproduction. The initial
native budget is 600 nodes and 120 seconds per period; exceeding it
supplies no proof result. Bounded parent processes allowed 180 seconds
including controls. No solver, database, network or external package is
needed by the public checker.

The trust boundary is exact ordinary Python, the literal certificates,
and the written completion, periodicity, dominance, CRT and union-bound
arguments. The full finite coordinate actions themselves are explicitly
verified. The original alternate audit and controls were read but not
rerun in full; their same-author status is not confused with independent
evidence. No proof assistant was used. Jobs were sequential with all
solver/BLAS/OpenMP threads one, at unchanged CPU1/RAM2GiB/Tasks128 scope.
An incomplete or timed-out run is not mathematical nonexistence.

Final complete native checks took 26.518/21.440 seconds in normal mode and
25.767/21.529 seconds in optimized mode (15840/18480). The original comparison
replays took 18.181/12.062 seconds. Peak child RSS across these final checks
was 38948 KiB. A prepublication JSON key-conversion mismatch in the manifest
comparison was corrected; the final complete normal and optimized checks
passed with unchanged independently computed evidence.
