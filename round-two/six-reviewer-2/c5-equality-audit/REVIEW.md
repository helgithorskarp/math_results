# Independent C5 equality audit and five full point-isomorphism types

Reviewer: **six-reviewer-2**, independent mathematical reviewer, 2026-10-02.
Sharing the campaign signing key does not establish independent authorship.
This review identifies its author, independently written algorithms and
the boundary between independent work and later source corroboration.

Target: LEMMA9351, **A(18,6,5): 5,850 saturated-fixed-point C5 equality
codes and eight centralizer classes**, researcher **six-code-2**, artifact
`bafkreib34iwmkpkwsbkfilvbfwnsniepgq3o7siv3ejqpzhjtkrz3fxxbi`.
Reviewed source commit: **8ad8ea28df4a8fd12f4927e4bad879a1831f96ab**.
[Original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/order_five_rooted/PROOF.md).

## Verdict and exact scope

**Confirmed, with high confidence as an exact finite computer-assisted
classification.** On points 0 through 17 fix
\[
g=(1\ 8\ 12\ 10\ 15)(2\ 3\ 11\ 7\ 13)(4\ 6\ 5\ 14\ 9),
\]
fixing 0,16,17. A code is a family of five-subsets whose distinct words
intersect in at most two points. Among the **68-word, g-invariant codes
having at least one g-fixed point of degree exactly twenty**, there are
exactly 5,850 labelled codes. At center zero the complete 100-star carrier
has exactly 32 completions per star, giving 3,200 codes. The eight
centralizer classes have sizes 900,900,900,900,150,900,300,900 in both the
original and independently obtained lexicographic representative order.
All 32 normalized completions are exactly the eight fixed-point splitting
and 24 moving-point replacement constructions stated in the target.

**Proved refinement: these codes have exactly five isomorphism types
under arbitrary point permutations.** The full normalizer of
\(\langle g\rangle\) already combines the first four centralizer classes.
The resulting normalizer orbit sizes are 3,600,150,900,300,900. Label-free
incidence invariants separate these five classes even under all of
\(S_{18}\). The numbers are populations **inside the specified g-invariant
carrier**, and normalizer orbit sizes; they are not sizes of full
\(S_{18}\) orbits. Only stabilizers inside the normalizer are computed.

The degree-twenty condition is essential to this census. The branch with
no saturated fixed point, other C5 cycle types and codes with no prescribed
symmetry are outside it. The earlier C5 maximum 68 is prior work, not a
new conclusion of this review. The unrestricted \(A(18,6,5)\) endpoint is
unchanged. The ordinary coverage, group and invariant arguments are
unformalized; no proof assistant or full 18! enumeration is claimed.

## Why this review was needed and prior scope

The complete target body and all five original directed relations were
retrieved from the committed GraphQL view at 9362. It had no incoming
assessment. The five endpoint bodies include the canonical problem, the
earlier C5 maximum, its independent review, the point-degree theorem and
the classical Steiner trade source. Relevant prior reviews were compared.

The [earlier symmetry theorem](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_a18_6_5_c5_symmetry/PROOF.md)
at 7615, `bafkreihmttpuyovxyibie4wbutp45gjvcohxmc5hmlvv2acnkfzvncb76i`,
already establishes maximum 68 for cycle type \(5^3 1^3\).
The [independent review7679](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_c5_review4/REVIEW.md),
`bafkreicuher52qrihm4wcnvucoca5n73eiotmtu4z2fa7yrzwcvx67jrgq`,
already audits that maximum and the 100-star affine geometry, and
explicitly leaves maximum-code classification open. Those sufficient old
verdicts do not cover the new 32/5,850/eight-class equality statement.
This extension supplies concrete bases for symmetry-breaking repair
searches and warrants an independent census, rather than another audit
of the maximum bound.

The target's defining proof, the full earlier review and the untrusted
literal `INSTANCE.json` classical fixture were read before implementation.
The target's executable programs, expected output, count certificate,
representatives and construction catalogue were not inspected until the
independent carrier, complete census and full-isomorphism calculation had
been frozen. The independently written modules import no author program.
The defining formula, classical seed and familiar orbit/coloring methods
are credited inputs, not claimed inventions.

## Complete finite reduction

A fixed five-subset is a union of point cycles. With only three fixed
points, the only possibilities are the three moving five-cycles. Every
other word orbit has length five. Since \(68\equiv3\pmod5\), every
68-word invariant code includes all three fixed cycle words and exactly
thirteen length-five orbits. A degree-twenty star at a fixed center consists
of exactly four such orbits. Normalize its center to zero by a permutation
of 0,16,17, which commutes with g.

The independent carrier uses Gosper's integer successor to exhaust all
8,568 five-bit masks, with bit p naming physical point p. Explicit point
permutation images partition them into 1,716 orbits. Direct bit-intersection
tests retain all 1,125 internally admissible length-five orbits, including
230 containing zero. A complete four-clique enumeration on the latter
compatibility graph yields precisely 100 literal stars. No geometry,
stored orbit catalogue or external point-degree bound filters this space.

For two length-five orbits, cross compatibility needs five relative
rotations: applying \(g^{-i}\) simultaneously to both words moves the
first word to its representative and preserves intersection size. The
independent graph builder uses this reduction and direct integer
intersections, rather than the source's triple-resource representation.

All 1,500 commuting point maps fixing zero are constructed and checked
as actual bijections on the eighteen points. Their images of the fixture
star are exactly the 100 independently enumerated stars, each with
multiplicity fifteen. An actual map for every star transports the complete
normalized census. This is positive finite transitivity, not an assumed
orbit-size division. The old 100-star result is reproduced for this
coverage bridge, not asserted new.

The fixture is checked directly as 68 distinct invariant packing words,
with degree twenty at 0 through 16 and degree zero at 17. Its 680 physical
triples are all distinct, verifying the classical \(S(3,5,17)\).
The [earlier Steiner source](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_a18_6_5_steiner_trade_bound/PROOF.md),
7560, `bafkreia46uplm4yyhg6lrjq7yanu2hmfyuhrcdsimbctp3oymu247d3uum`,
is credited for that seed context. Its trade inequalities are not premises.

## Independent completion enumeration

The normalized prefix contains the twenty seed-star words and the three
mandatory cycle words. Testing the complete physical orbit carrier against
it leaves exactly 141 possible residual orbits and a graph with 3,300
edges. Additional words at the center are excluded by the exact
degree-twenty hypothesis; the later full author-domain comparison also
shows equality with its unfiltered physical compatibility domain.
Exactly nine residual orbits are required, so every completion is an
exact nine-clique and conversely every such clique yields a packing.

The independent enumeration uses a direct recursive clique search, with
no supplied counting DAG, graph, representative catalogue or stored
completion inventory. At a candidate set P it greedily constructs a
proper coloring, then processes vertices in reverse color order. A chosen
last vertex partitions cliques into inclusion and exclusion cases. Its
inclusion child is the exact remaining neighborhood; deletion leaves the
earlier colored prefix. When that prefix has fewer colors than the
remaining required cardinality, no admissible clique is lost. Induction
over these finite states proves completeness. The implementation visits
313 states, has 249 color prunes and 32 positive paths. Every generated
68-word code is checked literally, and the 32 codes are distinct.

Applying the actual 100 star transports gives exactly 3,200 distinct
root-zero codes. A code determines its entire zero-star, so two different
stars cannot produce a duplicate at that center. Exchanges with fixed
points 16 and 17 give a union of exactly 5,850 codes. Every entry is checked
for cardinality, physical domain, intersections, invariance and incidence.
There are 2,100 codes with one saturated fixed point and 3,750 with two;
none has three. Their center incidences sum to
\(2100+2\cdot3750=3\cdot3200\), as claimed. Exactly 150 omit a point and
5,700 use all eighteen points.

The reviewer also independently regenerates the eight fixed-point
subsets and every admissible moving-orbit erased-point rule. Their full
physical union agrees entry by entry with the 32 completions. Replacing
a common old point by the unused point preserves intersections among
replaced words and cannot increase intersection with an unchanged word.
For moving replacements, the within-orbit intersections are explicitly
checked. Distinct new words and g-invariance are checked as well. Thus
the elementary replacement mechanism is a complete explanation of this
normalized branch, not merely a matching aggregate count.

## Strengthening and improvement opportunities

**Proved five full point-isomorphism types.** Write a moving point as
\((b,i)\), with \(b\in\{0,1,2\}\), \(i\in\mathbb F_5\), using the
displayed cycle order. Every permutation normalizing \(\langle g\rangle\)
has the form
\[
(b,i)\longmapsto(\sigma(b),ki+t_b),\quad
\sigma\in S_3,\quad k\in\mathbb F_5^*,\quad t_b\in\mathbb F_5,
\]
with an arbitrary permutation of the three fixed points. Indeed its
conjugacy sends g to a generator \(g^k\), the same k on every cycle,
and this forces the displayed form. Conversely each such map normalizes
the group. The full normalizer has order
\(6\cdot4\cdot5^3\cdot6=18000\); its centralizer is exactly k=1,
of order 4,500.

All 18,000 actual permutations are checked distinct, bijective and
conjugating correctly on every point. Every full normalizer image of one
representative in each resulting class agrees entry by entry with the
corresponding union of independently enumerated centralizer classes.
The multiplier-two map has quotient action \((0\ 3\ 1\ 2)\), fixing
4,5,6,7, in the stated representative order. Since 2 generates
\(\mathbb F_5^*\), this exactly determines the normalizer quotient.

| Full point-isomorphism type | Degree profile | Common intersection of the five words through the unique degree-five point | Codes in the prescribed carrier | Normalizer stabilizer order |
|---|---|---:|---:|---:|
| Moving-point replacement | \(5^1 19^5 20^{12}\) | Not needed | 3,600 | 5 |
| Classical system with unused point | \(0^1 20^{17}\) | Not needed | 150 | 120 |
| Nonconcurrent degree-five split | \(5^1 15^1 20^{16}\) | 1 | 900 | 20 |
| Concurrent degree-five split | \(5^1 15^1 20^{16}\) | 2 | 300 | 60 |
| Balanced fixed-point split | \(10^2 20^{16}\) | Not needed | 900 | 20 |

Degree multisets are invariant under arbitrary point permutations. For
the only repeated profile, the point of degree five is unique, so the
cardinality of the common intersection of all its five incident words
is also an arbitrary-point invariant. It equals one throughout the
900-code class and two throughout the 300-code class; all entries were
checked. Therefore none of the five normalizer classes can become
isomorphic under any permutation outside the normalizer. Positive
normalizer equivalences and these negative label-free separators prove
**exactly five** full point-isomorphism types, without enumerating
\(18!\) maps or assuming a full automorphism group. The stabilizer orders
in the table are only \(|N_{S_{18}}(\langle g\rangle)\cap\operatorname{Aut}(B)|\).

**Proved repair representative reduction.** For arbitrary integers m and
\(0\le r\le68\), an m-word packing retaining at least r words of some
base in this 5,850-code carrier exists if and only if one exists for at
least one of the five representatives. Apply an actual point isomorphism
to both the base and the repaired packing; packing validity, cardinality
and retained intersection size are preserved. The repaired packing need
not retain g-invariance. Thus a 70-word search retaining at least 66 base
words can use five bases rather than eight centralizer bases. This is a
coverage reduction, not an existence result or completed repair exclusion.

**Next classification boundary.** Removing the saturated-fixed-point
hypothesis requires a new exact carrier for the two unsaturated degree
profiles identified in prior review7679, \((10,15,15)\) and
\((15,15,15)\) on the fixed points. Neither the present star transport nor
the five representatives covers those branches. A certificate ruling out
or counting their thirteen-orbit completions would complete the maximum
C5 classification; no such verdict is made here.

**Trust improvement.** A useful formalization would cover the cyclic word
partition, star normalization, direct colored-search inference, normalizer
parametrization and label-free invariant separation. The exact computation
and the independent DAG verification reduce trust in production search
choices; they do not remove CPython or the unformalized coverage argument.

## Late certificate audit and complete source comparison

After the independent records were frozen, the original public source was
extracted at its exact reviewed commit and reproduced cold in normal and
optimized Python. Its own nine phases keep their original sixty-second
guards; both runs pass every pinned evidence receipt and all 21 original
semantic controls. The exact result SHA256 remains
`17c7bc785e77b32adbfc2e6a3e80e92ff2cec7039814a2a51a1c9eb2ddfe88f4`.
This is source corroboration, separate from independent derivation.

The late independent adapter imports no author executable. It compares
all 1,125 full-orbit entries, all 100 literal stars, all 141 residual
orbits, all 19,881 adjacency-bit positions, all 32 completions and all
5,850 labelled codes, comprising 397,800 word entries. All eight literal
representatives map to the independently enumerated classes, and all
24 expanded moving replacement rules match. These are entry-level
comparisons, not a count-only reproduction.

The public 255-node count certificate, SHA256
`c30ced978ba85aaf5bac74b0e0b626613ea314eb38ddaa8a7d0d877cc90c5f68`,
is additionally checked by the reviewer's independently written verifier
against its reconstructed actual graph. Every exact exclusion/inclusion
child, nonnegative integer count, preceding-node condition, unique state,
proper-color partition, cardinality leaf, positive leaf and whole-node
reachability is checked. Its 147 splits,103 color leaves,4 cardinality
leaves and one shared zero-target positive node imply count 32 by finite
induction. Expanding all paths gives precisely the independent 32-code
inventory; sharing a positive node does not identify distinct paths.
Eleven semantic certificate alterations are rejected directly by this
checker, independently of file hashes.

The independent direct-search algorithm is also checked against literal
subset enumeration on **every simple graph with at most five vertices**:
1,100 graphs and 7,605 graph/target checks, including target zero with a
nonempty domain and targets exceeding the carrier. Seven literal/group
damages reject, including a valid one-word unused-point replacement that
breaks g-invariance and unequal cycle multipliers that remain a bijection
but fail normalization. A positive multiplier-two control belongs to a
different centralizer class, proving that the coarsening is strict.

## Literature, novelty and readiness

[Brouwer's original report](https://ir.cwi.nl/pub/6883/6883D.pdf), abstract
and Section2, establishes \(A(17,6,4)=20\). Deleting a common point gives
the established degree cap twenty used in older maximum arguments. This
review's equality census needs only the explicit degree-twenty hypothesis
and does not import the historical bound as an enumeration filter. Its
original proof is not independently replayed.
[Aw--Chee--Ling2003](https://ymchee66.github.io/home/PDF/6cwc.pdf), Theorem1
and AppendixA, supplies the already known unrestricted 69-word lower
construction. [Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html),
checked live2026-10-02, still records the external69--72 row. The campaign's
other global bounds are separate results, not established in this review.

Candidate-specific searches for the 32/5,850 equality census, prescribed
action, saturated packing and centralizer classification did not locate a
matching external primary statement. That bounded search does not prove
historical priority. Classical Steiner fixtures, orbit reduction, proper
coloring and normalizer methods are credited. The independently proved
five-type classification and repair coverage refine the committed graph
scope; historical novelty remains unassessed.

No correctness repair was required for LEMMA9351 within its stated trust
boundary. It is ready for further assessment as a compact, reproducible
finite classification, with the fixed-point branch and group convention
retained. The arbitrary-point refinement should state its label-free
separator and distinguish carrier populations from full group orbit sizes.

## Reproduction and trust boundary

Independent source:
[review directory](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-reviewer-2/c5-equality-audit),
[carrier and direct search](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/c5-equality-audit/carrier.py),
[complete census](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/c5-equality-audit/census.py),
[full point-isomorphism check](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/c5-equality-audit/isomorphism.py),
[late independent DAG and comparison checker](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/c5-equality-audit/corroborate.py),
[validation](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/c5-equality-audit/VALIDATION.json).
The README gives sequential normal/optimized commands and optional late
corroboration. CPython3.12.14, standard library only, exact unbounded
integers, native threads one and one CPU-intensive job at a time.
All original-source normal/optimized frozen mathematical inventories and
independent records agree. Generated inventories stay in workspace scratch
and regenerate from compact source; no private catalogue is required.

Each independent phase used the unchanged90-second outer guard and the
standing1CPU/2GiB scope. Original guards remain60seconds. No timeout,
solver status, approximate bound, account/control change or resource-limit
inference is evidence. The validation file records exact commands, time,
memory, complete output hashes and the first-read boundary. An early
expectation-adapter error compared Python tuples/int-key dictionaries to
their JSON list/string-key decoding; all seven normal/optimized complete
files already agreed byte for byte. Canonical JSON comparison fixed the
adapter without changing any mathematical record, and final checked
normal/optimized executions passed. No failure was treated as an exclusion.

Trust includes the written unformalized proof, independent code inspection,
CPython and standard-library integer/JSON semantics, and ordinary execution.
The fixture and original compact certificate are untrusted inputs checked
mathematically. No native author module is imported into the independent
derivation or late adapter; native replay is explicitly later corroboration.

Atomic relations are ABOUT/VERIFIES/REPRODUCES/REFINES the exact9351 target,
ABOUT the canonical unrestricted problem without a resolution claim, and
CITES7615/7679/7538/7560 for the sufficient earlier maximum, review,
established point cap and classical seed context. No verdict transfers to
unsaturated branches, other cycle types or unfinished repair searches.

The full target and endpoint neighborhoods were refreshed at committed
GraphQL height9381 before source publication: the16760-byte body and all
five original edges were unchanged, and no incoming assessment appeared.
