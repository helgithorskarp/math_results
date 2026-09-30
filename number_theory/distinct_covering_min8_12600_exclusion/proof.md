# Excluding every minimum-at-least-eight covering of period 12600

Actual author: **six-covering-2**, role **researcher**, 2026-09-30. All
campaign signatures share one identity; the author name identifies this
work. Status: exact computer-assisted proof with a complete alternate
check by the same author. No external reviewer verdict or proof-assistant
formalization of this new result is claimed.

## Statements and scope

**Proposition.** There is no finite covering of the integers by congruences
with pairwise distinct moduli, all at least eight, whose moduli all divide
\(N=12600=2^3 3^2 5^2 7\).

This includes actual LCM 12600 and any smaller actual LCM dividing 12600.
It is stronger in its minimum hypothesis than the exact-eight instance
needed for the assigned problem. Its period restriction is essential.

**Consequence.** Define \(L_{\min}(8)\) using minimum exactly eight. The
previous finite sieve and explicit period-20160 cover imply
\(L_{\min}(8)\in\{10080,12600,15120,15840,18480,20160\}\).
Removing 12600 gives

\[
L_{\min}(8)\in\{10080,15120,15840,18480,20160\}.
\]

Only 20160 has a covering witness in these inputs. We do not infer
\(L_{\min}(8)\ge15120\), or existence at any smaller retained value.

## Complete finite reduction

Set \(D=\{m:m\mid N,\ m\ge8\}\); there are exactly 65 eligible moduli.
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
CRT axes \((8,9,25,7)\), with a positive integer at each box. The masks are
literal subsets of each axis, not assertions about a generated orbit.
Both decoders check disjointness and support in the actual uncovered set.

## Complete branching and its symmetry

For each prime \(p\mid N\), view its \(p\)-power coordinate as a rooted
digit tree, with the least significant digit first. Independent
permutations of children at every node preserve every congruence partition
modulo \(p^e\). Taking the product over the four primes therefore sends
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

## Evidence and arithmetic independence

The complete certificate has 1159 nodes, maximum prefix length 12:

| Node kind | Count |
|---|---:|
| Expanded | 202 |
| Strict uniform cut | 430 |
| Strict weighted cut | 527 |
| Pending or covering leaf | 0 |

There are 957 terminal cuts and 1158 tree edges. The weighted nodes use 527
vectors, 23628 literal boxes, maximum point weight 2607; 112 nodes use
paired resources. All 3071089 positive weighted points across nodes are
checked. All 4155 actual branch phases are scanned; the alternate replay
checks 3890 positive-gain transports with 1807 distinct coordinate witnesses.
All 457720 ordered pair-phase tuples are checked.

The primary decoder uses CRT inversion and Cartesian products; its pair
counter uses the compatible CRT intersection and inclusion-exclusion.
The alternate decoder uses literal predicates \(x\bmod q\in S\); its
pair counter sums the actual second progression outside the first, using
ordinary integer remainders. Uniform capacities also come from actual
full-period progressions. Neither replay imports LP matrices, point-orbit
generators or solver decisions.

Both full implementations agree on every recorded strict cut and every
ordered pair-capacity entry. Ordered node-event SHA-256:
`bb548b7e79b06f9e0102fb9361824c54ca52ff18c5fd7f756158f2508ca8ab57`.
Ordered pair-table SHA-256:
`1950cf07a76f7c664431fb43d66a1378b6d2b7263bf5c266c93e71969e9f82e6`.
Certificate SHA-256:
`332bccfc80087837a8f9b370d4b45c7e8726eb63f75a3b523b7135760e7cf8e0`.
The checker rejects missing, repeated, cyclic, shared and unused proof
nodes, open nodes, false cuts, malformed weights and invalid resource pairs.

Small controls check 3832 normalization phases by 12492 full coordinate
transport checks; 258 complete pair tables with 38373 phase tuples; all six
prefixes of a genuine period-12 cover; and ten malformed inputs, including
covered weight support and repeated resources. These controls complement
the full root replays and are not used as completeness evidence alone.

## Attribution, primary sources and dependencies

The residual counting framework is developed in
[six-covering-3's prime-tower work](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_prime_tower).
Weighted discovery uses this author's earlier
[lossless residual LP quotient](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_residual_weight_duals),
graph `bafkreidokkxgmeixbjd3k2ibu5j2cdbk3eavhiggfwq5437hz4ryikbhm4`,
and [joint resource capacities](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_joint_capacity),
graph `bafkreiagxm3vjb7tkvojo5yx636uifqq66lbiyt6vqb4r6z3f7rn4u6wpq`.
The standalone proposition does not assume their earlier exclusion instances.

The five-candidate consequence starts from this author's
[earlier finite sieve](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_lcm_sieve/proof.md),
graph `bafkreib6p7u7awrd6aufbnbekn7nhaypibzbmsttanzhafmgg5vcyhza7y`,
height 7298. Its original mathematical source is
`76ce0735e9f7ecf3e79cc55e15ce20bc3cf15422`; the attribution clarification is
`772fad60f165e31d77e6a1cf97d61ccfc7b4e759`.
[six-reviewer-1's independently checked finite version](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_20160_sieve_review1/README.md),
graph `bafkreieflxf6j6pls76ozup56vkc3r7x2lshaiyxjyzfj7cejmwmayba3i`,
height 7318, source `145ce6649b0ffa66005fc8dc6727ea003b869d3b`, removes the
infinite-exponent-barrier premises from that finite reduction. That finite
version supplies the previously proved candidate list here. It includes
the separately reviewed global lower bound and literal verification of
[six-covering-1's upper-20160 witness](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_20160/proof.md),
graph `bafkreia2v3b6it3qgjvt6thqjqhtuoqkogzpj7idamrq6wc3vsy2s7btfq`,
source `1b26a5217c02c00ede618b445dc935a88839391a`.
The prior review does **not** review this new 12600 proof.

[Zhang and Zhang](https://arxiv.org/html/2607.19029) give a minimum-seven
construction at 10080 and claim its optimality. It is context, not a
solver-backed premise of this proof. [HKLT](https://arxiv.org/html/2605.18644),
Problem 3, concerns minimum-eight coverings on prime support \(\{2,3,5\}\);
12600 additionally has prime seven. Current primary sources, campaign
checkpoints, repository commits and graph were refreshed on 2026-09-30.
No 12600 minimum-eight exclusion was found in the inspected primary sources
or earlier campaign claims; no exhaustive historical priority is asserted.

## Reproduction and trust boundary

Run the three commands in [README.md](README.md). CPython 3.11.2 was used;
Python 3.10+ and the standard library suffice. Initial full exact replays
took 62.84 seconds and 55.16 seconds; alternate peak RSS was 100736 KiB.
All execution used one process and one numerical thread within the unchanged
CPU1/2GiB/128-task scope. Source entry points are also checked before publication.

Discovery used NumPy 2.4.6, SciPy 1.17.1 and HiGHS 1.12.0, one thread and
two-second LP limits. Floating solutions proposed weights and branching
order; integer reconstruction and literal capacities alone justified cuts.
Incomplete states were preserved until every branch closed. Solver status,
timeout, absence of a witness and memory limits supplied no exclusion.

The exact source, small manifests and 582605-byte literal certificate are
complete replay inputs. Private databases and discovery logs are unnecessary
and omitted. The trust boundary is exact Python integer execution, the
literal certificate, and the written union, periodicity and symmetry
arguments. It is not a formal-kernel proof or an external review.
