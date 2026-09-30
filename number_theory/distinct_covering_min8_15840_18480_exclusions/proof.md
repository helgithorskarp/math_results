# Excluding distinct coverings at periods 15840 and 18480

Actual author: **six-covering-2**, role **researcher**, 2026-09-30.
Status: complete exact computer-assisted proofs, each checked by a separate
algorithm by the same author. No independent review or proof-assistant
formalization of these two new exclusions is claimed. Campaign signatures
share one identity; the name above identifies the actual author.

## Statements and scope

**Proposition.** For each of

\[
N=15840=2^5 3^2 5\cdot11,\qquad N=18480=2^4 3\cdot5\cdot7\cdot11,
\]

there is no finite covering of all integers by congruences with pairwise
distinct moduli, all at least eight, whose moduli all divide N.

This excludes every subset of eligible divisors and all residue choices,
including actual LCM equal to N or any divisor of N. The fixed-period
hypothesis is essential. The minimum-at-least-eight proposition implies
the assigned minimum-exactly-eight instances, with these scopes stated
separately.

**Corollary.** Define L_min(8) using minimum **exactly eight**. Combining
these two exclusions with the independently checked finite sieve, the
author's previous 12600 exclusion and six-covering-1's verified 20160
construction gives

\[
L_{\min}(8)\in\{10080,15120,20160\}.
\]

Only 20160 has a covering witness among these inputs. Neither smaller
value is asserted feasible or excluded. The numerical interval remains
10080 <= L_min(8) <= 20160. The corollary uses the cited prior results;
the two standalone period exclusions do not assume them.

## Complete finite reduction


Set \(D=\{m:m\mid N,\ m\ge8\}\); there are 66 eligible moduli for 15840 and 73 for 18480.
Any hypothesized covering uses a subset of \(D\). Adding one arbitrary
congruence at each missing eligible modulus preserves coverage and
distinctness, and keeps every modulus dividing \(N\). This also inserts
modulus eight when absent. Translating the integers makes its phase zero.
Therefore it suffices to exclude completions of the root \((8,0)\) using
one class for each unused member of \(D\). Coverage is equivalent to
coverage of all \(N\) representatives by periodicity.

At a prefix \(A=((m_i,a_i))\), let

\[
U_A=\{0\le x<N:x\not\equiv a_i\pmod{m_i}\text{ for every }i\},
\qquad B_A=D\setminus\{m_i\}.
\]

Every remaining eligible modulus is charged, including any prospective
branching modulus. Nothing is removed merely because its phase is unknown.

For nonnegative integer weights \(w\) supported in \(U_A\), put
\(H=\sum_x w(x)\). Partition \(B_A\) into singletons and disjoint pairs.
For a group \(G\), define its capacity by the maximum, over **all** phase
choices, of the weight covered by the union of its classes:

\[
C_G(w)=\max_{(b_m\bmod m)_{m\in G}}
\sum_{x\in\bigcup_{m\in G}(b_m\bmod m)}w(x).
\]

Any completion covering \(U_A\) must satisfy
\(H\le\sum_G C_G(w)\), by nonnegativity and the union bound. Consequently
the strict integer inequality \(H>\sum_G C_G(w)\) excludes that prefix.
Uniform cuts use \(w=1_{U_A}\) and singleton groups. Weighted cuts use the
saved integer vector and its stated pairs; every other remaining modulus
is a singleton. Equality is never an exclusion.

The certificate represents weights by explicit Cartesian bit masks on the
CRT axes \(32,9,5,11\) for 15840 and \(16,3,5,7,11\) for 18480,
with a positive integer at each box. The masks are
literal subsets of each axis, not assertions about a generated orbit.
Both decoders check disjointness and support in the actual uncovered set.

## Complete branching and its symmetry

For each prime \(p\mid N\), view its \(p\)-power coordinate as a rooted
digit tree, with the least significant digit first. Independent
permutations of children at every node preserve every congruence partition
modulo \(p^e\). Taking the product over the prime coordinates therefore sends
each congruence to a congruence with the same modulus, and preserves
coverage, distinctness and all resource moduli.

Label the ordered placed nodes canonically by naming children on first
appearance. This is performed on their original coordinate prefixes;
the partial names extend to permutations of every finite tree. Two ordered
prefixes have the same normalized labels exactly when such an automorphism
sends one to the other. For sufficiency, compose the two partial naming
maps, extending unused child names arbitrarily to bijections. For necessity,
the automorphism preserves which earlier paths share a child and the order
of first appearance, recursively at every prefix.

Thus, when earlier classes \(A\) are fixed, equal normalizations of
\(A+((m,a),)\) and \(A+((m,b),)\) give an automorphism fixing every class
in \(A\) and sending the proposed phase \(a\) to \(b\). The primary checker
scans **every** phase modulo each branched modulus, and requires a child
with the same normalization for every phase that meets \(U_A\).

Phases disjoint from \(U_A\) need not become children: their class is
already covered by the prefix, and can be replaced by any positive-gain
phase without losing coverage. Since \(U_A\ne\varnothing\) at each
expanded node, at least one such phase exists. This is a justified
dominance step, not a search heuristic.

The alternate checker does not trust the normalization criterion. It uses
capped prime-power agreement signatures only to propose a child. For
every positive-gain actual phase it constructs explicit coordinate
permutations and verifies their whole finite actions: bijectivity,
preservation of every congruence partition, fixing of every placed
coordinate cylinder, and transport to the designated child. This supplies
a separate finite witness for every symmetry reduction used by the tree.

## Complete evidence and independent arithmetic

| Period | Nodes | Expanded | Uniform cuts | Weighted cuts | Paired cuts | Open leaves |
|---:|---:|---:|---:|---:|---:|---:|
| 15840 | 286 | 67 | 91 | 128 | 36 | 0 |
| 18480 | 145 | 47 | 34 | 64 | 23 | 0 |

At 15840, the maximum prefix length is 10; 128 literal
vectors use 3905 boxes, largest weight 2348.
The checks cover 944976 positive point incidences,
all 1171 actual branch phases and all
177313 ordered pair-phase entries. The alternate
replay checks 1089 positive-gain transports, using
530 distinct coordinate permutation witnesses.

At 18480, the maximum prefix length is 9; 64 literal
vectors use 1962 boxes, largest weight 173.
The checks cover 617828 positive point incidences,
all 817 actual branch phases and all
115090 ordered pair-phase entries. The alternate
replay checks 758 positive-gain transports, using
460 distinct coordinate permutation witnesses.

The primary decoder uses inverse CRT and Cartesian products. Its pair
counter evaluates compatible CRT intersections and inclusion-exclusion.
The alternate decoder tests actual remainders against literal axis masks;
its pair counter sums the second progression outside the first using
ordinary remainder predicates. Uniform capacities use full-period
progressions. Neither proof checker imports the discovery LP, orbit
generator, numerical solver or its selected matching.

The two implementations agree on **every** strict cut and every ordered
pair-capacity entry. These are full replays rooted only at (8,0), with no
unprocessed siblings. Common scalar factors were divided out of saved
integer weights when possible; this preserves every strict inequality.
The checkers reject missing, cyclic, shared, unused or open proof nodes,
false cuts, covered or overlapping support, and invalid resource groups.

Period 15840 certificate SHA256:
`ca9b12acac505569435cab36172e9b6a4a6b6d85306b173a52e321fc7db12bbd`.
Ordered node-event SHA256:
`77e11e7087e4e28cea8b738ac6ad3cedd393a56e60cf39bfc1bcf91c41ee1919`.
Ordered pair-table SHA256:
`82e438be87d620ee6bb3e08a69a67b3e31ab4dfc626f183af3aae63288808b26`.

Period 18480 certificate SHA256:
`34b14234d1de52640fb4534e668de79b3847f3054b64e90b2fe5c723c28b942f`.
Ordered node-event SHA256:
`45c05f3a6f37f5a9931a49386d94eae738f3ab2ec398c8a011646d6297bc6b5b`.
Ordered pair-table SHA256:
`15b3624d4e7151c54c1dc708409797b9df2e84c393b0a7e149175a5b482b3ef4`.

Small controls verify 5268 normalization phases by
17931 explicit coordinate checks,
423 entire pair tables with 168282 entries,
all 6 prefixes of a genuine period-12 cover,
and 10 malformed-input rejections for each target.
The controls include prime-eleven examples at 132 and 660. They supplement
the full proofs; they are not the completeness argument.

## Attribution and dependencies

The proof mechanism follows this author's earlier
[12600 certificate](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_12600_exclusion/proof.md),
source `1e5314450d14b6941c07376ed926990707725bab`, graph
`bafkreidipjiqkl2txe4y7bma75falk4slb3eiiesjt66bcfjmqxm3r65a4`, height7332.
That numerical exclusion is also a premise of the three-candidate
corollary, not of either new standalone proposition.
The elementary counting and symmetry methods are not claimed inventions.
The new evidence is the two complete finite exclusions.

The residual framework is attributed to
[six-covering-3's prime-tower work](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_prime_tower),
graph `bafkreiadl5p7tzrjxfj5dzkkfp5om2fhr5fztv4k6all56vzq4cjta5eqa`,
height7102. Weighted discovery uses this author's
[lossless residual quotient](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_residual_weight_duals),
source `b9d39eb740a866e07237be1c78b834d1ab6ea718`, graph
`bafkreidokkxgmeixbjd3k2ibu5j2cdbk3eavhiggfwq5437hz4ryikbhm4`, height7174,
and [joint capacities](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_joint_capacity),
source `d1c0f5712486644eb3963d074c81743bfc9e4bec`, graph
`bafkreiagxm3vjb7tkvojo5yx636uifqq66lbiyt6vqb4r6z3f7rn4u6wpq`, height7228.
The self-contained proofs here do not import their older exclusion cases.

The complete finite sieve is from this author's
[original reduction](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_lcm_sieve/proof.md),
source `76ce0735e9f7ecf3e79cc55e15ce20bc3cf15422`, graph
`bafkreib6p7u7awrd6aufbnbekn7nhaypibzbmsttanzhafmgg5vcyhza7y`, height7298;
attribution clarification `772fad60f165e31d77e6a1cf97d61ccfc7b4e759`.
[six-reviewer-1's finite independent check](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_20160_sieve_review1/README.md),
source `145ce6649b0ffa66005fc8dc6727ea003b869d3b`, graph
`bafkreieflxf6j6pls76ozup56vkc3r7x2lshaiyxjyzfj7cejmwmayba3i`, height7318,
removes all infinite-exponent-barrier premises from the finite candidate
list. Only that finite theorem is needed here; its separate support-235
corollary and exponent barriers are not dependencies of the new corollary.
The finite version includes the global lower bound and literal verification
of [six-covering-1's 20160 cover](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_20160/proof.md),
source `1b26a5217c02c00ede618b445dc935a88839391a`, graph
`bafkreia2v3b6it3qgjvt6thqjqhtuoqkogzpj7idamrq6wc3vsy2s7btfq`, height7286.
These older reviews do not review the new 15840 or 18480 proofs.
A freshly published [independent12600 review by six-reviewer-3](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_12600_review3/README.md),
source `382611a05603a687ab388a342a97c53664a14a91`, confirms the earlier12600
proposition and supplies an outside-modulus density consequence. It is
additional evidence for that prior input, not a review of these two new proofs.

The complementary [51-class retention result](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_incumbent_stability/proof.md)
by six-covering-1, source `02083700154e18c62e9eef87a4789491993530b0`, graph
`bafkreic7lbbx3rf6nihyuqoa5vp5gahnoj4d2wchs4p4obdiubcgy73qjm`, height7344,
is a local optimum for a specified core. It does not exclude unrestricted
10080 or15120 and is context rather than a premise here.

Primary literature refreshed2026-09-30:
[Zhang-Zhang](https://arxiv.org/html/2607.19029) gives a minimum-seven
cover at10080 and claims its optimum; that minimum-seven claim is unused.
[Harrington-Klein-Lowrance-Trifonov](https://arxiv.org/html/2605.18644),
Problem3, concerns support{2,3,5}; both periods here additionally use11.
The [Simpson-Zeilberger1991 prime-replacement theorem](https://sites.math.rutgers.edu/~zeilberg/mamarimY/Zeilberger_y1991_p59.pdf)
is classical. It is not claimed as a new method or used as a premise here.
The inspected primary papers and current graph/source context did not
contain these two finite exclusions. No exhaustive historical-priority
claim is made.

## Reproduction and trust boundary

Run the commands in [README.md](README.md), Python3.10+ and standard
library only. CPython3.11.2 was used. The two ordinary-integer replays
are the proof checks; discovery's floating LP outputs only proposed
weights and branch order. No solver status, timeout, incomplete branch,
absence of a witness or killed process is an exclusion.

Discovery used one-thread NumPy2.4.6, SciPy1.17.1 and HiGHS1.12.0, with
two-second LP limits and bounded resumable jobs. Pair proposals used an
exact small maximum-saving matching among the first12 unused resources,
allowing up to6 disjoint pairs. This selects proposals only: the proof
rechecks their full literal capacities and assumes no matching optimality.
The unchanged process scope is1CPU/2GiB/128tasks; no resource setting was
raised. All proof checks run sequentially.

The complete replay inputs are the source, small manifests and two literal
certificates of109040 and48904bytes. Private frontiers, discovery logs,
LP environments and ledgers are omitted. The trust boundary is exact
ordinary Python execution, the literal evidence, and the written
periodicity, nonnegative-union and congruence-symmetry arguments. These
are not formal-kernel proofs or independent peer reviews.
