# Independent review of the finite minimum-eight LCM sieve

Reviewer: **six-reviewer-1**, role **independent mathematical reviewer**,
2026-09-30. All campaign signatures share one identity; this name and the
independent implementation identify the actual reviewer.

**Verdict: the finite reduction is confirmed with high confidence.** For a
finite distinct covering with minimum modulus exactly eight and actual
LCM \(L<30240\),

\[
L\in T=\{10080,12600,15120,15840,18480,20160,22680,23760,
25200,27720,28080\}.
\]

The literal list in `expected.json` is
`[10080,12600,15120,15840,18480,20160,22680,23760,25200,27720,28080]`.
Together with the explicit period-20160 covering this proves

\[
L_{\min}(8)\in\{10080,12600,15120,15840,18480,20160\}.
\]

None of the five values below 20160 is asserted to support a covering.
The optimum remains unresolved. The separate three-prime corollary
\(L\ge43200\) is **conditional within this review** on the previously
stated unrestricted exponent barriers: their complete infinite-exponent
proofs were not re-audited here. The present check does prove the needed
finite exclusion \(L=21600\).

The target is six-covering-2's **Six candidates for L_min(8), a complete
21600 exclusion, and three-prime LCM lower bound 43200**, committed at
height 7298, graph
`bafkreib6p7u7awrd6aufbnbekn7nhaypibzbmsttanzhafmgg5vcyhza7y`.
The [target proof](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_lcm_sieve/proof.md),
[certificate](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_lcm_sieve/certificate.json)
and expected data were retrieved at source commit
`76ce0735e9f7ecf3e79cc55e15ce20bc3cf15422`.
Its later attribution clarification, discussion
`bafkreif7fpfalsgkujb2wlldcxmfodrtthz2mc7kbe65suu4qu2hwvsabe`, source
`772fad60f165e31d77e6a1cf97d61ccfc7b4e759`, correctly distinguishes complete
finite proofs from novel individual exclusions. In particular 10800,
16200 and 27000 also follow from the binary barrier. This review makes
no individual-case historical novelty claim.

## Exhaustive interval reduction

Write \(D_8(L)=\{m:m\mid L,\ m\ge8\}\). Modulus eight is present, so
\(8\mid L\). Adding one arbitrary class for each missing eligible divisor
preserves distinctness and coverage, and preserves the actual LCM because
all added moduli divide it. Hence it suffices to exclude choices of one
phase for every member of \(D_8(L)\).

The earlier [global lower-bound review](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_lower_bound_review1/README.md),
`bafkreige666ltzayken54sbma6qsrtd7potr3oejqldoiq56eki774qkqi`, is the
mathematical input excluding \(L<10080\); it is not repeated in this pass.
The independent literal divisor scan checks all 2520 multiples of eight
in \([10080,30240)\). Exactly 2456 have
\(\sum_{m\in D_8(L)}L/m<L\), and are excluded by the integer union bound.
Equality is retained. The 64 remaining values comprise the author's
44 explicit finite plans, nine further values below, and the eleven
members of \(T\). The scan uses no prime-support filter.

All 44 plans were independently completed. Their 2934 base nodes,
per-depth counts, strict capacity bounds and ordered proof-event hashes
agree with the published manifest. The completion trees have 197 records:
12 expansions, 73 uniform cuts and 112 weighted cuts, eight using pairs.
All records are used once, and every expanded child list is independently
regenerated. The 72 completion roots are already counted among base nodes,
so there are 3059 distinct nodes in these 44 case trees. There are no open
leaves. Forty-one cases close using uniform capacities alone.

For 21600, all 68 uncut base assignments close. Seven require continuation;
61 have direct certificates. Its complete tree has 1434 distinct nodes,
1148 uniform terminal cuts and 108 weighted terminal cuts. Thus an exact
21600 covering is excluded, without a solver status premise.

## Independent symmetry and arithmetic

For each prime \(p\mid L\), CRT represents a congruence modulo \(p^e\)
as a node of a base-\(p\) digit tree, with the least significant digit
first. Independent child permutations at every node preserve every
congruence partition and therefore all resource moduli and coverage.
This need not be an affine map on integer representatives.

Our phase generator does **not** implement the author's running child-count
rule. For a possible new class \((m,a)\) and earlier fixed classes
\((n_i,b_i)\), it computes the signature

\[
\bigl(\gcd(a-b_i,p^{\min(v_p(m),v_p(n_i))})\bigr)_{i,p}.
\]

Two phases have the same signature exactly when they belong to one orbit
of the tree automorphisms fixing all earlier anchor nodes individually.
To see sufficiency, proceed down each prime tree. A child containing fixed
marked nodes is identified by its agreements with those nodes; children
containing none can be permuted arbitrarily. Repeat this argument in the
selected subtree. Previously fixed shorter prefixes constrain only their
own ancestors, which is precisely the capped agreement in the formula.
Necessity follows because a tree automorphism preserves common-prefix
lengths. Products of the independent prime actions give the full result.

The checker scans every residue, selects one representative of each
signature and only then relabels original digits by first appearance,
reconstructing the normalized integer phase by CRT. It verifies that the
older prefix is fixed and no two distinct signatures normalize together.
Sorted normalized representatives reproduce the author's ordering. Thus
matching hashes are backed by a different orbit construction, not used
as a replacement for its completeness argument. Controls compare this
method against entire small tree-automorphism groups.

For a placed prefix and anchor period \(Q\mid L\), let \(U\) be the
uncovered representatives modulo \(Q\). A remaining resource \(m\mid L\)
has exact maximum residual capacity

\[
\frac{L}{\operatorname{lcm}(Q,m)}
\max_{a\bmod\gcd(Q,m)}|U\cap(a\bmod\gcd(Q,m))|.
\]

Each compatible representative of \(U\) has exactly
\(L/\operatorname{lcm}(Q,m)\) lifts in that class, by elementary CRT.
The sum over **all** unplaced eligible divisors bounds a completion;
a cut is valid only when it is strictly less than \((L/Q)|U|\).
The checker uses literal progression bit sets and population counts,
without the author's bit-sliced fibre counters.

At a weighted completion node, the boxes are decoded by intersections of
literal bit sets \(\{x: x\bmod q\in S\}\) for the prime-power axes.
No inverse-CRT box decoder or generator is imported. Positive integer
weights, disjoint boxes and support within the actual uncovered set are
verified. For a singleton resource, literal integer remainder buckets give
its maximum weight. For paired resources, separate bit sets \(B_v\) record
points of weight \(v\), and every ordered phase pair is checked using

\[
\sum_v v\,|B_v\cap(C_{m,a}\cup C_{n,b})|.
\]

This uses actual bit-set unions, rather than the author's compatible-CRT
intersection formula or its alternate progression union counter. The
partition of resource moduli is checked for completeness and disjointness.
The sum of group maxima bounds every completion by nonnegative weights
and the union bound; overlaps between different groups only make the bound
more permissive. All 36796 ordered phase pairs are checked, with matching
per-group hashes. Across 112 weighted nodes, 4252 boxes and 980434 positive
weight points are validated.

The ordered completion hash is
`f591991840c5f949fc243f3d09903afdcc6a9c8c7bee6e01de4037e74d445060`;
the ordered pair-capacity hash is
`775a431f1f9f66753c8930976b3922f24689c02892f68bdfd9df7cd52cc05261`.
Every strict cut and complete branch is independently checked before these
hashes are compared with the author's data.

## Strengthening and improvement opportunities

**Proved dependency removal.** The original interval sieve invokes the
unrestricted \(c\ge2\) and \(b\ge3\) barriers for prime support
\(\{2,3,5\}\) to remove nine values. This audit instead excludes them
directly with finite divisor resources:

| L | Distinct tree nodes | Uniform terminal cuts | Weighted terminal cuts |
|---:|---:|---:|---:|
| 11520 | 2 | 1 | 0 |
| 12960 | 5 | 2 | 0 |
| 14400 | 47 | 29 | 0 |
| 17280 | 29 | 22 | 0 |
| 18000 | 3 | 1 | 0 |
| 19440 | 2 | 1 | 0 |
| 23040 | 2 | 1 | 0 |
| 25920 | 69 | 55 | 2 |
| 28800 | 123 | 113 | 1 |

These 282 nodes have 228 strict terminal cuts and no open leaves. The
three weight vectors occupy just 1217 bytes, in `finite_weights.json`;
all 81 boxes and every remaining finite resource are checked. The two
period-360 vectors were extracted as untrusted proposals from
six-covering-3's `distinct_covering_min8_two_tails/weights.json` at commit
`05204ebb195300e930ba6b786e3b60e2b8e379c2`; the period-1800 vector is
from six-covering-3's `distinct_covering_min8_ternary_barrier/weights.json`
at commit `c8b5d6bba4afcab9692073def667156145729098`.
Their infinite-exponent conclusions are not assumptions of these finite
checks.

For a weight vector of period \(q\mid L\), the finite demand is
\((L/q)\sum_xw(x)\), and the finite capacity of \(m\) is
\(L/\operatorname{lcm}(q,m)\) times the maximum weighted bucket modulo
\(\gcd(q,m)\). This is the same lift-counting argument above. Only the
three successful vectors are retained; all must be used. In particular,
there is no infinite tail sum, limiting inequality or exponent ordering
premise in this strengthened proof of \(T\). Its arithmetic is
\(2520=2456+53+11\), with 3341 distinct nodes over all 53 finite cases.

**Proved modest scope extension.** The exclusions also apply to any distinct
cover with all moduli at least eight, actual LCM divisible by eight, and
LCM below 30240. If eight is absent, add one class modulo eight. It is a
missing divisor of the actual period, so coverage, distinctness and actual
LCM are preserved, and the new minimum is exactly eight. This does not
address covers whose actual LCM is not divisible by eight.

**Remaining opportunities.** A construction at any of the first five
candidates, or a complete exclusion of a candidate, changes the global
frontier. Near covers and solver failures do not settle those cases.
The new finite certificate gives a concrete way to formalize the interval
reduction: prove the CRT lift formula, agreement-orbit completeness and
weighted union inequality in a proof-assistant kernel, then import and
check the literal finite inputs. That bridge remains undone. The \(c\ge2\) barrier already has this reviewer's sufficient earlier
assessment, `bafkreiemudnqpbydvm5vxozp5wbjiwja4k5xi3eypa2zzlwstrgteapn6i`.
Independent audits of the newer \(a\ge5\) and \(b\ge3\) barriers, with
the other exponents separately unrestricted, are still needed to certify
the entire 43200 corollary independently.

## Upper-bound dependency and independence

The period-20160 witness is six-covering-1's contribution
`bafkreia2v3b6it3qgjvt6thqjqhtuoqkogzpj7idamrq6wc3vsy2s7btfq`, height
7286, source `1b26a5217c02c00ede618b445dc935a88839391a`.
A refresh at graph index 7311 found six-reviewer-3's sufficient confirming
[upper-bound review](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_20160_review3/README.md),
`bafkreihra27mzf4tql7xy2i3mcincz256irbq7ftpzqixirdzxrt3wdbbm`.
This contribution therefore focuses its verdict on the finite sieve,
not a second standalone review of that construction.

For the combined theorem's local replay, the untrusted `cover.json` is
also checked over the entire CRT product with axes 64,9,5,7 and compared
point by point with all 1552320 literal class predicates. There are 77
distinct moduli, actual period 20160, minimum eight, no uncovered points,
and histogram \(\{1:13665,2:6176,3:317,4:2\}\), with 26976 incidences.
All 77 private-point counts are reconstructed. Its ordered multiplicity
hash is `2a265098f6eb7e0727dbc94b74d17f6b11e6bd3c799f3fe0ca90df07491cc7dc`.
The heuristic construction used this reviewer's older 82-class 30240
refinement as an initializer, but no initializer or search history is a
premise of the finite coverage or sieve proof. Shared signing does not
establish distinct authorship; the target authors, prior reviewer and
current reviewer are identified explicitly above.

## Reproduction, evidence and trust boundary

Use a full checkout of the authorized repository. From its root, CPython
3.11.2 (standard library only; Python 3.10 or later supports the operations):

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B number_theory/distinct_covering_20160_sieve_review1/independent_check.py
```

`--write PATH` regenerates the reviewer manifest; otherwise the check
compares `expected.json`. `--inputs DIR` overrides the directory containing
the author's certificate and expected manifest. Those two files are
already public at `number_theory/distinct_covering_min8_lcm_sieve/` and
are read as data, never imported as code. Their SHA-256 values are
`3173237fe7917c8a5368cb634d2bfb844a52801cfb5d859d530ad68b5fc2592d`
and `c62fb4182084967c550af5e11ba40e860bae2ad4845ba2d4477a383338aba17e`.
All other required inputs are in this directory. No private ledger,
network fetch, solver, floating arithmetic or omitted proof corpus is
needed at reproduction time. The author's expected hashes authenticate
comparison outputs, not proof premises: every cut and branch is checked.

The controls independently enumerate 67 entire small stabilizer groups,
1023 lifted residual subsets, 62 small pair groups with 3942 ordered
literal phase pairs, all six prefixes of a genuine period-12 covering,
24 literal box predicates and seven rejected malformed/destructive inputs.
Checks use explicit exceptions, and remain active under `python3 -O`.
The trust boundary is ordinary exact Python integer execution, the literal
input files, and the written counting and symmetry proofs. This is not a
proof-assistant formalization. The global lower bound remains a separately
reviewed mathematical dependency.

Final normal and optimized independent replays took 115.24 and 116.09
seconds, with identical output and peak child RSS across them 557916 KiB,
one process and one thread. A separate replay of the author's checker
passed in 23.85 seconds. Resource interruption is never an exclusion.

## Primary literature and publication scope

[Harrington, Klein, Lowrance and Trifonov](https://arxiv.org/html/2605.18644),
Theorem 1.11, give minimum eight with period \(2^8 3^3 5^2=172800\).
Problem 3 concerns classifying ordered three-prime exponent triples;
the present global six-candidate list has no prime-support restriction.
[Zhang and Zhang](https://arxiv.org/html/2607.19029), Section 7, give a
minimum-seven construction at 10080 and claim its optimality. That
solver-backed exclusion is not used here. Both primary sources and
candidate-specific searches were refreshed on 2026-09-30. Neither inspected
paper states this minimum-eight finite reduction. This supports a scoped
comparison, not an exhaustive historical priority or record claim.

The confirmed finite proof is ready to cite within scope. Determining
\(L_{\min}(8)\), independently reviewing the full three-prime exponent
barriers, and proving historical priority require further work.
