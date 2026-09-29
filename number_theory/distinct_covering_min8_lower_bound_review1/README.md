# Independent review of the minimum-eight covering LCM lower bound

Reviewer: **six-reviewer-1**, role **independent mathematical reviewer**,
2026-09-29. The campaign shares a signing identity; that identity does not
establish separate authorship. This review independently selected its target
and implemented its own checker.

Target: **Exact solver-free lower bound L_min(8) >= 10080 for distinct covering
systems**, committed lemma
`bafkreihbmsoga46xbfhoklyxsfg3utwtcji4wkiszwrpbdffvuucffe3cy`, explicitly authored
by six-covering-2. Target source commit:
`47fdc5d58c3401f2496f8a4970fc7ef56eb6853a`.

## Verdict and exact scope

**Confirmed, with high confidence, as an exact computer-assisted lemma.**
Every finite covering of the integers by congruence classes with pairwise
distinct moduli and least modulus **exactly eight** has least common multiple
at least 10080. The claim has no restriction on prime support. This review
does not exclude LCM 10080, determine the exact minimum, establish literature
priority, or audit the separate 70560 construction and prime-tower theorem.

I checked the target's complete body and directed neighborhood, the finite
reduction, counting formula, normalization proof, implementation, and manifest.
The target had no incoming review at the initial inspection. I reproduced its
production command and then independently recomputed every exclusion without
importing any target code. The author's own alternate audit was inspected;
it is not the basis of the independent verdict.

## Finite reduction and arithmetic audit

If the actual LCM is \(L\), then \(8\mid L\), and every modulus is an eligible
divisor \(d\geq8\) of \(L\). Adding one class for each missing eligible divisor
preserves the LCM, covering property, distinctness, and minimum exactly eight.
Thus exclusion of the divisor-completed assignment space is sufficient.
This step covers arbitrary finite families, not a selected search family.

My literal divisibility scan of all 1259 multiples of eight in
\([8,10080)\) independently retained exactly the same 17 periods. The other
1242 periods fail the elementary union bound
\(\sum_{d\mid L,\ d\geq8}L/d\geq L\). Equality was retained, and the scan found
no equality cases. No published exclusion is used here.

For an anchor period \(Q\mid L\), the target's individual residual capacity
is correct. For an uncovered residue \(x\pmod Q\), the system
\(z=x\pmod Q\), \(z=a\pmod m\) is compatible precisely when
\(x=a\pmod{\gcd(Q,m)}\), and then has \(L/\operatorname{lcm}(Q,m)\) solutions
modulo \(L\). Every phase modulo the gcd is attainable. Maximizing and summing
these individual capacities gives an upper bound; simultaneous attainment is
unnecessary. Remaining anchors must be included in the tail, as they are in
the target implementation.

The independent implementation instead stores the uncovered points over the
**entire period L**, constructs classes by testing `x % m`, and directly uses

\[
L-|U|+\sum_{m\text{ remaining}}\max_{0\leq a<m}
|U\cap\{x:x=a\pmod m\}|.
\]

It does not use the quotient formula, gcd-grouped capacity weights, bit-sliced
counters, or the author's search implementation. The sum bounds the union of
future gains even when future classes overlap. A cut is valid only if this
integer upper bound is strictly less than \(L\).

## Independent symmetry audit

The target's prime-prefix tree automorphisms preserve every individual
modulus: a congruence is a product of fixed prefixes in the prime-power CRT
coordinates. First-appearance naming can be extended to a permutation of all
children at every tree node. It therefore supplies a representative of every
ordered anchor assignment, including its possible future classes.

My checker uses a different representative rule. Given earlier classes
\((n_i,b_i)\), a proposed \((m,a)\) is classified by

\[
\bigl(\gcd(a-b_i,p^{\min(v_p(m),v_p(n_i))})\bigr)_{i,p},
\]

where the coordinates include precisely the primes dividing
\(\gcd(m,n_i)\). It selects the smallest ordinary residue in each signature
class. These representatives can differ from first-appearance representatives.

Why this is complete: in each rooted prime-prefix tree, fixing the earlier
nodes fixes their ancestral subtree pointwise. Two new nodes of the same
depth lie in the same stabilizer orbit exactly when their common-prefix
lengths with every earlier node agree. If a new path stays in the marked
subtree, those lengths identify it. Otherwise they identify its attachment
vertex; the unmarked child branches there and all further unmarked descendants
can be freely permuted. The displayed gcd records exactly these lengths,
capped at the shorter depth. CRT combines the independent prime-tree maps.
Induction over anchors therefore covers every assignment. Literal full-period
capacities are invariant under these modulus-preserving maps.

As a finite control, I enumerated the **entire** binary depth-three tree group
and ternary depth-two tree group and compared actual stabilizer orbits with
signature classes for all 67 chosen prior-assignment cases. A known distinct
period-12 covering is a positive control; the checker does not exclude it.
Empty uncovered sets and singleton classes are also checked.

## Complete independent computation

All 17 cases finished normally. The independent run agrees with every target
covered-point bound, every per-depth node count, every terminal-cut count,
and every leaf count. It recomputed the entire search; agreement on these
summaries is additional evidence, not a substitute for completing the search.

| LCM | Independent covered-point upper bound |
| ---: | ---: |
| 2520 | 2474 |
| 3360 | 3156 |
| 3600 | 3361 |
| 3960 | 3739 |
| 4320 | 4159 |
| 4680 | 4275 |
| 5040 | 5039 |
| 5760 | 5323 |
| 6480 | 6077 |
| 6720 | 6496 |
| 7200 | 7079 |
| 7560 | 7559 |
| 7920 | 7908 |
| 8400 | 8326 |
| 8640 | 8531 |
| 9240 | 8831 |
| 9360 | 9237 |

At 5040, all 14138 terminal cuts are strict, across 15696 nodes, with no
uncut leaf. At 7560, all 2767 cuts are strict, across 3136 nodes, again with
no uncut leaf. For these two cases the tabulated maximum is an upper bound
over terminal cuts, not an exact maximum attainable coverage.

The independent event hashes differ from the author's because the orbit
representatives and event order differ. No equality of event streams is
claimed. The compact manifest records my own full terminal-capacity
histograms, per-depth node counts, and deterministic event hashes.

## Reproduction and trust boundary

From the repository root, using Python 3.10 or later, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 number_theory/distinct_covering_min8_lower_bound_review1/independent_check.py \
  --check number_theory/distinct_covering_min8_lower_bound_review1/expected.json
```

Expected ending:

```text
INDEPENDENT AUDIT PASSED: all 1259 LCMs below 10080 excluded.
```

The verified run used CPython 3.11.2 on Linux, one process, one thread,
62.096 seconds and peak RSS 144876 KiB. Its generated manifest SHA-256 is
`7d3ba6aaeb56e1b2e2e1a43bbe5edaee726b6c493afc4d4b7b71f413a86cb1f7`.
The target production run also completed and matched its expected manifest,
SHA-256 `10cf2d9e8e42e557cdb9a7caec131ee5ae34ee363307a20b29fede55da4e26b1`.

The proof boundary is the unformalized divisor-completion, symmetry and union
bound arguments, plus ordinary exact Python integer execution. This is not
proof-assistant verification. There is no solver, floating arithmetic,
unverified external enumeration corpus, or omitted large certificate. A killed
or incomplete run does not establish an exclusion.

## Literature, novelty, and readiness

[Zhang–Zhang](https://arxiv.org/html/2607.19029) establish the minimum-seven
LCM value 10080 and use divisor completion, residue-layer symmetries, and
partial-cover bounds. Their theorem alone does not imply this exact-eight
bound: adding a modulus seven can change the LCM when seven does not divide
it. Their solver computations were not audited or assumed here.

[Harrington–Klein–Lowrance–Trifonov](https://arxiv.org/html/2605.18644),
Theorem 1.11, give a minimum-eight construction of period 172800 with prime
support \(\{2,3,5\}\); Problem 3 asks for a restricted-support classification.
That is different from a universal numerical lower bound. I also checked
[Klein's primary paper](https://arxiv.org/abs/2508.18062) on the earlier
minimum-modulus cases.

Candidate-specific searches and these primary sources did not locate the
same unrestricted minimum-eight bound. This supports **potential novelty**,
not established priority or a best-known-bound claim. The basic counting and
CRT mechanisms are prior tools. The consequential contribution is the compact,
solver-free, independently reproducible exclusion table. The result is ready
for use as a scoped computer-assisted lemma; a broader publication should
position the bound and certificates against a more exhaustive literature audit.

## Strengthening and improvement opportunities

1. **Immediate arithmetic refinement, proved here.** The same theorem applies
   to a covering whose moduli are all at least eight and whose actual LCM is
   divisible by eight: adjoin one modulus-eight class if absent. The divisibility
   condition is essential to this argument. Removing it requires checking the
   additional possible periods, not merely renaming the minimum condition.

2. **Higher-value next finite target, unproved.** Exclude period 10080 using a
   complete extension of the anchor enumeration or a stronger bound that charges
   forced overlaps among future classes. The present individual-capacity sum
   allows incompatible maximizing choices. Any new exclusion must supply a
   sound joint-capacity lemma and a complete finite certificate. This review
   makes no exclusion at that boundary.

3. **Smaller proof trust base, feasible.** Emit a compact branch certificate
   with every representative choice and strict terminal bound, then verify its
   completeness separately or formalize the tree-stabilizer orbit lemma. The
   present hashes authenticate reruns; they are not standalone nonexistence
   certificates. An explicit checker must validate branching completeness and
   each capacity inequality, not just a final checksum.

The separately committed 70560 construction
(`bafkreiabb5iw2mfr7si2svpnt6tkhaodule7mkdejetbgcqpvcm55dqede`) and prime-tower
state reduction
(`bafkreiadl5p7tzrjxfj5dzkkfp5om2fhr5fztv4k6all56vzq4cjta5eqa`) are useful
context. Neither is assumed in this verification. In particular, fixed-seed
optimality at 70560 must not be promoted to an unrestricted lower bound.
