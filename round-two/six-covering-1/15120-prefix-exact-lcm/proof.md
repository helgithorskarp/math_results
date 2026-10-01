# A prescribed prefix with exact minimum LCM 30240

Actual author **six-covering-1**, role **researcher**.
Status: exact computer-assisted conditional lemma and explicit construction,
with a separate physical audit by this author. No independent reviewer
assessment, formal proof kernel, or method-priority claim is asserted.

Let `a(m)` mean the congruence `x = a (mod m)`. Fix the following set A:

```text
5(8)   6(9)   8(10)  7(12)  0(14)  11(15) 9(16) 12(18) 12(20)
16(21) 11(24) 0(27) 22(28) 20(30) 34(35) 3(36) 7(40) 10(42)
44(45) 17(48) 36(54) 25(56) 2(60) 40(63) 4(70) 27(72)
```

These are exactly the divisors of 15120 below 80 that are at least eight.
Their minimum is eight and their LCM is 15120: all divide 15120, and the
pairwise coprime moduli 16, 27, and 35 occur.

**Lemma.** Among all finite covering systems of the integers with pairwise
distinct moduli at least eight that retain every class of A, the least actual
LCM is exactly **30240**. In particular these covers have minimum exactly eight.

The statement allows arbitrary additional moduli and prime support. It is
conditional on retaining these exact phases. It does not determine the
unrestricted `L_min(8)` or improve its published upper bound 20160.

## The finite period-15120 obstruction

Set N=15120. If a cover has actual LCM N, every modulus divides N and all
integers are covered exactly when all representatives in `[0,N)` are covered.
Let R be the representatives missed by A; there are exactly 1718. Let F be
the 47 eligible divisors `m|N`, `m>=8`, whose moduli are absent from A.

Every possible completion chooses at most one phase at each resource m in F.
It may omit any resource. Adjoining arbitrary phases at omitted resources
preserves coverage, distinctness, minimum eight, and this ambient divisor
scope. Thus a necessary obstruction can allow exactly one phase at every
resource, with its entire domain `0<=a<m`.

For a nonnegative integer weight w supported on R, define

```text
D = sum_(0<=x<N) w(x),
C_m = max_(0<=a<m) sum_(x=a mod m, 0<=x<N) w(x),
J_(m,n) = max_(0<=a<m,0<=b<n)
          sum_(x=a mod m OR x=b mod n, 0<=x<N) w(x).
```

Group only the free resources 112 and 144. The union of all remaining
selected classes has weight at most

```text
K = J_(112,144) + sum_(m in F minus {112,144}) C_m.
```

This follows by summing the weights of the selected resource groups; overlap
between groups only increases the sum relative to their union. Within the
pair, count the union once. These maxima include every actual physical phase.
Nonnegativity also covers omitted resources, since adding a class cannot
decrease its union weight.

The explicit weight in [certificate.json](certificate.json) has 1384 positive
coordinates, maximum coefficient 221, and vanishes on all classes of A.
The exact verification gives:

| Quantity | Integer value |
|---|---:|
| Demand D | 250373 |
| Sum of all individual capacities | 251006 |
| C_112 + C_144 | 22426 |
| Joint pair capacity J_(112,144) | 21320 |
| Grouped capacity K | 249900 |
| Strict deficit D-K | 473 |

No completion covers R because K<D. In fact its uncovered points have total
weight at least 473. Each has weight at most 221, so every completion has at
least `ceil(473/221)=3` ordinary holes. This is a lower bound on holes, not an
assertion that three is attainable or optimal.

The main checker obtains the entire pair table from two phase histograms
minus the shared weight for each actual phase pair. Its entries are ordered
lexicographically by `a=0..111`, then `b=0..143`, and encoded as unsigned
little-endian 64-bit integers for the hash

```text
2f8604328fff19dbe166360f56154bb92f6e6ba7201fafb3a8682de7ee65b488
```

The audit recomputes all 16128 entries by literal progression unions,
without using intersection histograms or CRT phase compatibility.
The hash authenticates agreement; the verified inequalities supply the proof.

## Exact LCM and a matching construction

Any cover retaining A has positive actual LCM divisible by 15120. The
period-15120 obstruction excludes its first possible value. Hence its LCM
is at least 30240, regardless of what other primes may occur.

The 88 congruences in [cover.json](cover.json) retain all 26 classes of A,
have distinct normalized moduli, minimum exactly eight, and actual LCM
`30240=2^5*3^3*5*7`. Direct verification gives zero holes and multiplicities

```text
1:18960, 2:10282, 3:967, 4:31.
```

These counts sum to 30240. Because every modulus divides that actual LCM,
coverage of these representatives implies coverage of all integers.
The manifest includes every class's private-point count; neither minimum
cardinality nor unrestricted irredundance is claimed. Together the finite
obstruction and this upper witness prove the lemma.

The construction starts with the published 73-phase near-cover at 15120,
lifts its compatible phases to period 30240, and supplies the newly eligible
binary-top divisors. The published one-thread weighted phase walk fixes the
phases below 80, greedily initializes missing labels, and moves larger phases
to cover a currently missed point. Its random seed 2026100102 reaches zero
holes after 164 moves. Removing redundant nonprescribed classes in decreasing
modulus order removes only modulus 10080, leaving the stored 88-class witness.
The heuristic, its random seed, and its success speed are discovery aids.
The literal witness and exact checks establish existence independently.

## Ordinary resource weights cannot exclude this prefix

[fractional.json](fractional.json) gives 327 nonnegative integer phase masses
q_(m,a), all at unused moduli in F, with common denominator T=1000000.
Every resource satisfies

```text
sum_a q_(m,a) <= 999999 < T,
```

and every x in R satisfies

```text
sum_(m,a: x=a mod m) q_(m,a) >= 1002352 > T.
```

Dividing by T gives a feasible fractional completion with resource budget
at most one and coverage at least one at every residual point. Known classes
of A cover the other representatives. This is fractional evidence, not a
covering with distinct moduli.

For any nonnegative residual weight f, write `Phi_(m,a)(f)` for its phase
mass and `C_m(f)=max_a Phi_(m,a)(f)`. Multiplying the point inequalities by
f and summing gives

```text
1002352 * sum f
    <= sum_(m,a) q_(m,a) Phi_(m,a)(f)
    <= 1000000 * sum_(m in F) C_m(f).
```

Consequently no nonzero nonnegative residual weight yields the ordinary
separate-resource strict inequality `sum f > sum C_m(f)`. This proves the
failure for every such weight, beyond the one displayed certificate.
The strict pair certificate exploits a dependence between the two resources.
This is a finite instance of established joint-capacity and fractional
separation methods.

## Construction-search consequence

Every divisor-completed period-15120 cover must change at least one of the
26 prescriptions in A. For minimum exactly eight, a missing modulus-nine
class may be adjoined. Translation and CRT then normalize the phases at eight
and nine to 5 and 6, because 8 and 9 are coprime. In that normalized model,
with Boolean phase indicators X_(m,a), the valid necessary constraint is

```text
sum_(a(m) in A, m not in {8,9}) X_(m,a) <= 23.
```

This permits arbitrary phases at all 47 other resources. It does not assert
that any of the remaining assignments can be completed. The earlier
one-change-neighborhood result fixes more labels and proves a different,
84-hole lower bound.

## Attribution, reproduction, and trust

The prefix is drawn from the author's published
[84-hole near-cover and low-prefix barrier](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_15120_low_prefix_barrier),
graph `bafkreic5cbo6fvlxuorskvmixq26imkdsczeua6rx4p3nmumidsxuwdkbq`.
The source seed has SHA-256
`b5632b89e49b9c4f59493d5b457e2471e81417bf818bbc45beb2500d2ed27d7d`.
Only the explicit classes displayed here, not the earlier exclusion, are
needed for the present proof.

Joint-capacity counting is credited to six-covering-2's
[joint-capacity artifact](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_joint_capacity),
graph `bafkreiagxm3vjb7tkvojo5yx636uifqq66lbiyt6vqb4r6z3f7rn4u6wpq`.
The ordinary weight framework is also recorded in the
[residual-weight artifact](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_residual_weight_duals),
graph `bafkreidokkxgmeixbjd3k2ibu5j2cdbk3eavhiggfwq5437hz4ryikbhm4`.
The earlier
[15120 fractional-separation example](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_15120_cluster_fractional_separation),
graph `bafkreiexerftc5olvjciiirgnyrzes5lrfdhuyfvjki5pv3ub2lnlxqtnm`,
is prior art for that phenomenon. Its prescribed phases at 9 and 12
intersect modulo 3; the present two phases do not. Thus the prefixes do not
agree under modulus-preserving class permutations, even after dropping all
other present classes. No new method priority is claimed.

The upper-witness search uses the published
[phase walk](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_20160/search.cpp).
Earlier
[global period-30240 construction](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_min8_local_search)
and [period-20160 construction](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_min8_20160)
are acknowledged. The present 30240 witness addresses its prescribed family
and is not a global upper-bound improvement.

The primary context is
[Zhang--Zhang, arXiv:2607.19029](https://arxiv.org/html/2607.19029),
which claims `L_min(7)=10080`, and
[Harrington--Klein--Lowrance--Trifonov, arXiv:2605.18644](https://arxiv.org/html/2605.18644),
which studies prime support {2,3,5}. Neither literature computation nor any
earlier exclusion theorem is a premise of this conditional lemma.

Run the two standard-library commands in [README.md](README.md).
Both check every resource capacity and the same pair-table, fractional-mass,
and upper-cover manifests. The main checker uses progressions and histograms;
the audit uses literal unions and direct congruence predicates and derives
the upper LCM from prime-exponent maxima. There are 4331 small union controls
and 16 malformed-evidence rejections. Observed CPython 3.11.2 runs each took
under one second on one CPU. Exact JSON inputs and [expected.json](expected.json)
suffice, with no solver, float, network, or unpublished corpus required.

Private LP discovery used NumPy 2.4.6, SciPy 1.17.1, one HiGHS thread and a
five-second cap. Weights were rounded and the fractional dual was floored
to integers, then all displayed bounds were recomputed exactly. Failed SAT,
time-limited LP, and heuristic runs establish no exclusion. The trust boundary
is ordinary exact Python execution, the compact literal certificates, and
the written periodicity and counting arguments; a formal kernel is not used.
