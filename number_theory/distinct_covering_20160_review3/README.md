# Independent review of the minimum-eight period-20160 covering

Reviewer: **six-reviewer-3**, role: **independent mathematical reviewer**.
Date: 2026-09-30. Campaign signatures share one identity; separate authorship
is specified by this name and the independent implementation below.

**Verdict: confirmed with high confidence.** The literal 77 congruences cover
every integer, with pairwise distinct moduli, minimum exactly eight, and actual
LCM 20160. Thus \(L_{\min}(8)\le20160\). The previously reviewed unrestricted
lower bound gives the campaign interval \(10080\le L_{\min}(8)\le20160\).
This review checks the new upper bound; it does not repeat that lower-bound
audit or determine the minimum.

Target: **An explicit 77-class minimum-eight covering with LCM 20160**,
graph `bafkreia2v3b6it3qgjvt6thqjqhtuoqkogzpj7idamrq6wc3vsy2s7btfq`,
height 7286, explicitly authored by **six-covering-1**, researcher.
Verified target-source commit: `1b26a5217c02c00ede618b445dc935a88839391a`.
See the [proof](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_20160/proof.md)
and [certificate](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_20160/cover.json).
The earlier 30240-period review concerns different congruences. No independent
review of this new certificate was present at target selection.

## Exact claim and literal input

Here \(a(m)\) means \(n\equiv a\pmod m\). The complete input is:

```text
1(8) 8(9) 2(10) 7(12) 6(14) 4(15) 5(16) 14(18) 10(20)
15(21) 3(24) 10(28) 16(30) 13(32) 23(35) 11(36) 0(40) 18(42)
29(45) 39(48) 26(56) 28(60) 0(63) 15(64) 28(70) 59(72) 77(80)
12(84) 56(90) 63(96) 9(105) 52(112) 100(120) 84(126) 18(140) 23(144)
125(160) 24(168) 128(180) 111(192) 156(210) 125(224) 173(240) 168(252) 278(280)
95(288) 218(315) 61(320) 108(336) 20(360) 358(420) 61(448) 253(480) 54(504)
100(560) 239(576) 294(630) 669(672) 461(720) 54(840) 541(960) 222(1008) 829(1120)
546(1260) 285(1344) 509(1440) 1500(1680) 1533(2016) 1501(2240) 2406(2520) 221(2880) 1053(3360)
861(4032) 726(5040) 2781(6720) 4893(10080) 6909(20160)
```

The independent [cover.tsv](cover.tsv) was transcribed from the signed graph
table, then compared entry by entry with the remote author's JSON: all 77
rows agree. The checker validates normalization and distinctness and scans
the divisors of 20160. These are exactly its 77 divisors at least eight:
\(20160=2^6\,3^2\,5\,7\) has 84 divisors, and precisely \(1,\ldots,7\) are
below eight. Class \(1(8)\) establishes the exact minimum. Moduli 64 and
315 alone have LCM 20160; every displayed modulus divides that number.
The stated period is therefore the actual LCM.

## Independent CRT and binary-tree proof

The reviewer code imports no author source, expected table or search output.
The author's checks mark ordinary progressions and test ordinary congruence
predicates. This check instead uses the bijection

\[
\mathbb Z/20160\mathbb Z\longrightarrow
\mathbb Z/64\mathbb Z\times\mathbb Z/315\mathbb Z,\qquad
n\longmapsto(n\bmod64,n\bmod315).
\]

Write \(m=2^e d\), with \(d\) odd. Class \(a(m)\) becomes the rectangle
\(x\equiv a\pmod{2^e}\), \(y\equiv a\pmod d\).
For each of the 315 odd fibers \(y\), activate exactly the classes whose
odd condition holds. Their binary conditions are nodes of the depth-six
tree whose paths specify bits from least significant to most significant.
Two nodes have disjoint leaf sets unless one is an ancestor of the other.
Sort by depth and retain a node only if no retained ancestor covers it;
duplicate nodes retain the first label. This gives a disjoint antichain
with the same union as the active classes.

A depth-\(e\) node contains \(2^{6-e}\) leaves. In **each** of the 315 fibers
the checker proves the exact integer equality

\[
\sum_{\text{retained nodes}}2^{6-e}=64.
\]

This certifies full partitions, rather than inferring coverage from an
aggregate histogram. Their size distribution is:

| Nodes | 1 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Fibers | 95 | 37 | 15 | 28 | 27 | 30 | 44 | 14 | 1 | 20 | 4 |

The totals sum to 315. All labeled partitions are regenerated and checked;
their deterministic SHA-256 is
`166003c57cd90c2b4b3d1a8a92961fba832af8f3466ff34ba75d1aa77a04cdce`.
The hash authenticates outputs; the partition equalities supply the proof.

For multiplicities and irredundancy, traverse each binary tree, carrying
every active ancestor label to its 64 leaves. The inverse CRT map is

\[
n=y+315\bigl(51(x-y)\bmod64\bigr),
\]

since \(315\cdot51\equiv1\pmod{64}\). The code checks every round trip and
that each integer representative appears exactly once. The full ordered
multiplicity-byte hash agrees with the author:
`2a265098f6eb7e0727dbc94b74d17f6b11e6bd3c799f3fe0ca90df07491cc7dc`.
The histogram is \(\{1:13665,2:6176,3:317,4:2\}\), with no holes.
The incidence total 26976 equals \(\sum_m20160/m\).
All 77 private-point counts also agree entry by entry. They are positive,
including the single private representative 14973 for modulus 10080.
Private representatives and their congruence-span gcds are recorded in
[expected.json](expected.json).

Reducing any integer modulo 20160 preserves membership in every class.
Full coverage of this CRT product therefore covers all integers, including
negative ones. No search-completeness premise is needed.

## Strengthening and improvement opportunities

**Proved single-class replacement rigidity.** Keep any 76 classes fixed
and replace the other by any congruence \(b\pmod q\). If the resulting
family covers all integers, has distinct moduli and all moduli at least
eight, then the replacement is the original congruence. The new modulus
and new LCM are not restricted in advance.

Choose a private integer \(n\) of the removed class. Both \(n\) and
\(n+20160\) are uncovered by the retained classes, by periodicity.
The replacement must contain both, so \(q\mid20160\). Every such
\(q\ge8\) already occurs among the retained classes except the removed
modulus \(m\). Distinctness forces \(q=m\), and containing \(n\) forces
\(b\equiv n\equiv a\pmod m\). This argument works for any irredundant
covering using every eligible divisor of its period.

More precisely, for the private representatives \(P_i\) of class \(i\)
in one period, choose \(n_0\in P_i\) and set

\[
g_i=\gcd\bigl(20160,\{n-n_0:n\in P_i\}\bigr).
\]

With the other classes fixed, \(b\pmod q\) preserves coverage **if and
only if** \(q\mid g_i\) and \(b\equiv n_0\pmod q\).
Necessity follows from all private differences and a full-period
difference. Sufficiency follows because only the periodic private set
is left uncovered. The checker computes all these gcds: 62 equal the
original modulus; the other 15 are larger divisors already occupied.
Improving this witness therefore requires changing at least two classes.
This is a local obstruction, with no global optimality or cardinality claim.

**Why halving does not prove period 10080.** Projecting onto
\(\mathbb Z/10080\mathbb Z\) replaces \(m\) by \(\gcd(m,10080)\).
The projection covers but has only 65 distinct moduli: 12 each occur with
two different phases. All collisions are verified in the expected evidence.
None has equal phases, which would make the higher-modulus original class
redundant. The projection is outside the distinct-modulus problem.
It neither constructs nor excludes a distinct covering at 10080.

**Unproved next opportunities.** Joint changes can bypass the replacement
obstruction. A smaller-period construction needs a new certificate;
an improved lower bound needs complete exclusions with unrestricted
prime support and justified symmetry reduction. These 315 partitions
also give a small representation for formalizing the witness: the CRT
bijection, prefix containment and exhaustive fiber checks must all be
verified in a proof-assistant kernel. None of these steps is claimed here.

## Reproduction and trust boundary

From the repository root, Python 3.11 or later, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B number_theory/distinct_covering_20160_review3/independent_check.py
```

The checker reconstructs every partition, ordered multiplicity, private
count, replacement-span gcd and projection collision, then compares its
own compact expected evidence. `--write` regenerates that evidence;
expected values are outputs, not assumptions in coverage validation.
Checks use explicit exceptions and remain enabled under `python3 -O`.
Normal and optimized runs agree exactly.

The antichain algorithm is compared with literal leaf membership on **all
32768 subsets** of the 15 nodes of the depth-three tree. It rejects 158
controls: four malformed/incorrect families, all 77 one-step phase changes
and all 77 deletions. Phase and deletion rejection must exhibit an uncovered
fiber. Deletion controls bypass the complete-divisor input requirement.

The reviewer replayed the author's progression verifier, separate pointwise
audit and five corrupted-certificate/initializer controls; all passed.
All 13 target files matched their remote published commit bytes.
The discovery search was inspected for role and scope, but not rebuilt
or independently replayed. Its heuristic, seed and failure outcomes are
not proof inputs.

On CPython 3.11.2 the full independent check with controls takes about two
seconds and less than 30 MiB peak child RSS, one process and one CPU thread.
Source and compact evidence are self-contained; there is no reproduction-time
network input, solver, floating arithmetic, private data or omitted corpus.
The trust boundary is exact Python integer execution, the literal input,
and the written CRT, prefix, periodicity and replacement arguments.
There is no proof-assistant formalization.

## Primary literature and publication scope

[Bosma, *Some computational experiments in number theory*](https://www.math.ru.nl/~bosma/pubs/bosmaexp.pdf),
Section 2, printed page 5, lists period 60480 for minimum eight and 20160
for minimum seven. The table does not assert minimality. The reviewer
downloaded and read the primary PDF: this minimum-eight certificate improves
that displayed upper bound by a factor of three. It does not establish
a current historical record.

[Zhang–Zhang](https://arxiv.org/html/2607.19029), Section 7, gives the
minimum-seven 10080 construction and claims its optimality. That exclusion
is not a premise of this review.
[Harrington–Klein–Lowrance–Trifonov](https://arxiv.org/html/2605.18644),
Theorem 1.11, gives minimum eight with period
\(2^8\,3^3\,5^2=172800\); Problem 3 concerns prime support \(\{2,3,5\}\).
This witness uses seven, so restricted three-prime exponent barriers
do not apply to it.

The campaign interval additionally uses lower-bound contribution
`bafkreihbmsoga46xbfhoklyxsfg3utwtcji4wkiszwrpbdffvuucffe3cy` and
[six-reviewer-1's assessment](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_lower_bound_review1/README.md),
graph `bafkreige666ltzayken54sbma6qsrtd7potr3oejqldoiq56eki774qkqi`.
The earlier [30240-period review](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_30240_review1/README.md),
graph `bafkreifayjcjbietnpqhqwhidhi4qk7d2oulny7eio4tkjib76utqv4e2a`,
includes the 82-class refinement used as the researcher's initializer.
It supplies provenance without validating the new period or phases.
None of these earlier constructions is needed for the independent coverage
proof.

A bounded candidate-specific primary-literature search did not locate this
exact minimum-eight period-20160 certificate. Literature priority and
best-known status remain unestablished. The finite construction and replacement
obstruction are ready to cite within scope. Determining \(L_{\min}(8)\)
and preparing a broader publication require further mathematics and a more
exhaustive priority audit.
