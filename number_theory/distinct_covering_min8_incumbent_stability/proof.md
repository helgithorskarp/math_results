# Exact minimum LCM 20160 when 51 of 53 designated classes are retained

Author: **six-covering-1**, role **researcher**, 2026-09-30.
Status: complete exact computer-assisted local lemma and matching explicit
construction; separate audit by this author, with no external review of
this new lemma claimed.

## Statement and explicit family

Here a(m) denotes the congruence x congruent to a modulo m. Let F consist
of these 53 normalized classes:

```text
1(8) 8(9) 2(10) 7(12) 6(14) 4(15) 5(16) 14(18) 10(20)
15(21) 3(24) 10(28) 16(30) 23(35) 11(36) 0(40) 18(42) 29(45)
39(48) 26(56) 28(60) 0(63) 28(70) 59(72) 77(80) 12(84) 56(90)
9(105) 52(112) 100(120) 84(126) 18(140) 23(144) 24(168) 128(180) 156(210)
173(240) 168(252) 278(280) 218(315) 108(336) 20(360) 358(420) 54(504) 100(560)
294(630) 461(720) 54(840) 222(1008) 546(1260) 1500(1680) 2406(2520) 726(5040)
```

Their moduli are precisely the 53 divisors of B=5040=2^4*3^2*5*7 that are
at least eight. Retention means the same modulus **and** the same phase.
Changing a phase or omitting its modulus ceases to retain that member.

**Lemma.** A finite covering of all integers by congruences with pairwise
distinct moduli, all at least eight, that retains at least 51 members of F
has actual LCM at least 20160.

**Sharpness.** The [previous 77-class covering](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_20160/proof.md)
retains all 53, has minimum **exactly eight**, and actual LCM 20160.
The identical certificate is included as `upper_cover.json` and verified
by both implementations here. Thus the least LCM in the retained-class
family is exactly 20160, for either the all-moduli-at-least-eight family
or its minimum-exactly-eight subfamily. These two definitions are stated
separately; the assigned global parameter L_min(8) uses exactly eight.

An improved covering of actual LCM below 20160 must change or omit at
least three of the displayed classes. This applies to this literal core;
the unrestricted optimum remains unresolved. No existence claim is made
for any smaller period, or for repairs that change three classes.

## Complete reduction of every smaller actual LCM

The three disjoint pairs of moduli

    (16,315), (144,35), (80,63)

are in F, and each pair has LCM5040. Omitting at most two members leaves
at least one entire pair. Every retained 51-class subset therefore has
actual LCM5040: all its moduli divide5040, and the surviving pair forces it.
The hypothetical cover's actual LCM is consequently a positive multiple
of5040. Below20160 the complete possibilities are5040,10080,15120, with
no restriction on the primes or size of any proposed replacement modulus
besides what that actual LCM itself forces.

A cover whose moduli divide5040 also covers every representative modulo
10080 and uses eligible divisors of10080. Excluding the fixed-prefix family
at10080 therefore excludes5040 as well. It suffices to exclude10080 and
15120, with all unused eligible divisors available at arbitrary phases.

If at least51 classes are retained, choose any51 of them as a fixed prefix.
There are exactly binomial(53,2)=1378 such prefixes, specified by the two
members of F not fixed. Those two resources are available whether the
hypothetical covering retained, changed or omitted them. For target period
L, charge **every** divisor m of L with m>=8 except the 51 actually fixed
moduli. There are14 such resources at10080 and22 at15120. A missing modulus
can be inserted at an arbitrary phase, preserving coverage and distinctness;
an already present resource receives its actual phase. Every chosen modulus
must divide the actual LCM, so no resource is omitted by this reduction.

## Exact finite capacity inequality

For a fixed prefix A, define its uncovered base set U_A in {0,...,5039}.
Its full uncovered set modulo L is the L/5040 copies of U_A. Let w be any
nonnegative integer function on the base supported in U_A, and lift it by
periodicity. Its full demand is

    D = (L/5040) * sum(w).

For any remaining modulus m, put g=gcd(5040,m). CRT proves that a class
at phase a modulo m contains exactly L/lcm(5040,m) representatives above
each base point r congruent to a modulo g, and none above other base points.
Thus its **exact** maximum phase weight is

    C_m = (L/lcm(5040,m)) * max_a sum(w(r) for r congruent to a modulo g).

Every normalized g-phase is induced by an m-phase, so this is an equality,
not a phase-sampling approximation. If a completion covers the residual set,
nonnegativity and the union bound imply D<=sum(C_m), charging each remaining
modulus once. The strict integer reverse inequality excludes the prefix.

Uniform w=1 on U_A closes most cases. Otherwise `weights.json` supplies
the explicit positive integer base coordinates. The checker verifies their
support and all phases of every remaining modulus, and requires strictness.
No group pairs, phase normalization, floating tolerance or search tree is
needed for this lemma.

## Complete evidence and matching upper

| Target period | All fixed prefixes | Strict uniform cuts | Strict weighted cuts | Minimum uniform gap | Minimum weighted gap |
|---:|---:|---:|---:|---:|---:|
|10080|1378|1360|18|2|236|
|15120|1378|1312|66|8|356|

Every prefix closes. There are84 supplied weight vectors with25201 positive
base coordinates, largest weight458. The 260847-byte certificate includes
all integer demands and capacities for its weighted cases. Any absent,
repeated, unused, unsupported or nonstrict record invalidates the proof.
All uniform capacities are regenerated from the53 listed input classes.

The matching upper certificate has77 distinct classes, minimum exactly8,
actual LCM20160 forced by moduli64 and315, and retains F. Literal coverage
has histogram {1:13665,2:6176,3:317,4:2}, with no holes. Every integer has
the same congruence memberships as its representative modulo20160, proving
coverage of all integers. Its multiplicity bytes have SHA256
`2a265098f6eb7e0727dbc94b74d17f6b11e6bd3c799f3fe0ca90df07491cc7dc`.

The lower exclusions and this upper prove the stated exact minimum within
the retained-class family. They do not change the unrestricted upper20160
or establish unrestricted optimality.

## Verification and trust boundary

Run the three commands in [README.md](README.md), Python>=3.10, stdlib only.
`check.py` regenerates all1378 prefixes for each period, marks the base by
arithmetic progressions, and uses the exact CRT capacity expression above.
`audit.py` imports no checker code: it computes prefix membership by actual
congruence predicates in the full target period, counts every singleton
phase histogram literally, and sums each weighted progression at every
normalized phase. It independently derives LCMs by prime factorization.
Both agree on **every** resource maximum in all2756 cases and the ordered
event digest `4c649f32e6215563ddb89e322fa3a142a001143a6ad3faf6daa674ebbffd9644`.

Production3.986s/20112KiB RSS; alternate13.956s/19684KiB; controls5.176s/27780KiB,
CPython3.11.2. The controls check the full positive proof and reject nine
invalid inputs, including missing resources, covered support, an absent
weight case and a genuinely nonstrict inequality. Proof checks were
sequential, one process and one numerical thread, within the standing
1CPU/2GiB scope. The trust boundary is ordinary exact Python integer
execution and the written periodicity, CRT, retention and union arguments;
there is no proof-assistant kernel or independent review of the new lemma.

Discovery used one-thread NumPy2.4.6/SciPy1.17.1/HiGHS with two-second LP
limits. Some full-period proposals timed out and remained inconclusive.
Averaging weights over translations by5040 preserves demand and cannot
increase convex maximum phase capacities. This permits a smaller periodic
model under the **same** limit; all resulting vectors were then checked
with integers. This discovery optimization is not a proof premise. Source
and compact certificate contain all replay inputs; private logs and scratch
searches are unnecessary.

Weight certificate SHA256: `2ce2ea354a4f98259d13bd672c86513e1ca2e1ff89c249243a9383248ea58535`.
Core SHA256: `1f1c4d618084124f4ca4566fe7bc2357ec1ce56525d8766d890ac1a05bdd8d9f`.

## Attribution and the unresolved global frontier

The core and matching construction were first published by this researcher
at source `1b26a5217c02c00ede618b445dc935a88839391a`, graph
`bafkreia2v3b6it3qgjvt6thqjqhtuoqkogzpj7idamrq6wc3vsy2s7btfq` (7286).
[six-reviewer-3's independent review](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_20160_review3/README.md),
source `f530984a9a66eaef8389aa4a2ba80638b3ab5008`, graph
`bafkreihra27mzf4tql7xy2i3mcincz256irbq7ftpzqixirdzxrt3wdbbm` (7302),
confirms that upper and proves single-class replacement rigidity. It does
not review this new51-retention result. The new result allows arbitrary
replacement phases and unused moduli while imposing this precise core.

Weighted residual capacities and lossless averaging are attributed to
[six-covering-2's residual-weight work](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_residual_weight_duals),
source `b9d39eb740a866e07237be1c78b834d1ab6ea718`, graph
`bafkreidokkxgmeixbjd3k2ibu5j2cdbk3eavhiggfwq5437hz4ryikbhm4` (7174).
The counting methods are not claimed inventions; the contribution is the
new complete exact local optimum and its explicit checked core.

Current campaign inputs give L_min(8) in{10080,15120,15840,18480,20160}:
[six-covering-2's finite sieve](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_lcm_sieve/proof.md)
(graph7298), its attribution clarification source
`772fad60f165e31d77e6a1cf97d61ccfc7b4e759`, and its new
[12600 exclusion](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_12600_exclusion/proof.md),
source `1e5314450d14b6941c07376ed926990707725bab` (7332), together with the
20160 upper. That global list is context and is not a premise of this
self-contained retained-class proof. Minimum-at-least-eight and
minimum-exactly-eight conclusions remain separately identified.

Primary context refreshed2026-09-30: [Zhang-Zhang](https://arxiv.org/html/2607.19029)
provides the minimum-seven10080 seed and claims its optimum; that optimum
is not used. [Harrington-Klein-Lowrance-Trifonov](https://arxiv.org/html/2605.18644)
leaves a minimum-eight prime-support2,3,5 classification frontier, while this
incumbent uses prime7. Bounded literature, repository and graph inspections
found no earlier claim for this specified53-class core; no exhaustive
historical-priority or record assertion is made.
