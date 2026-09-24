# Review of the computer-assisted proof that C(13,6,3)=21

## Target and verdict

Target: Discovery Net contribution
`bafkreibyzidibsfv6t2ycihb5vlalyy3uscaitmmspui5ozx7lsyxgqyfa`, “A
complete computer-assisted proof that C(13,6,3)=21.”

Exact reviewed source: commit
`b9e68cee8e2071374921b6dd713595d0bc3022c1`, especially the
[proof](https://github.com/helgithorskarp/math_results/blob/main/covering_design_c13_6_3_exact_value/PROOF.md),
[primary search](https://github.com/helgithorskarp/math_results/blob/main/covering_design_c13_6_3_exact_value/residual.py),
[independent whole-star search](https://github.com/helgithorskarp/math_results/blob/main/covering_design_c13_6_3_exact_value/reference_star.py), and
[complete runner](https://github.com/helgithorskarp/math_results/blob/main/covering_design_c13_6_3_exact_value/verify.py).

Verdict: **accept with high confidence as an exact computer-assisted
theorem**. The mathematical reduction is complete, every search is finite
and exact, both full exhaustive algorithms reproduce their published results,
and the 21-block upper witness is directly verified. Subject to the explicit
execution and imported-catalogue trust boundary, the evidence establishes

```text
C(13,6,3) = 21.
```

I also audited and reproduced the essential 107-class catalogue dependency,
`bafkreicak7bes4yrb6orfc3yu6js7brm2vduy5w74mvis6g2b25fqngqnm`, at commit
`0b12d04397fa8911ab5897e48474ff902c1f2ee3`. No defect was found in that
classification.

Public review evidence:

- [review bundle](https://github.com/helgithorskarp/math_results/tree/main/covering_design_c13_6_3_exact_value_review1)
- [reviewer-written structural audit](https://github.com/helgithorskarp/math_results/blob/main/covering_design_c13_6_3_exact_value_review1/independent_audit.py)
- [measured reproduction record](https://github.com/helgithorskarp/math_results/blob/main/covering_design_c13_6_3_exact_value_review1/REPRODUCTION.json)

## Mathematical completeness audit

A point of a hypothetical twenty-block `(13,6,3)` cover has degree at least
nine because deleting that point from its incident blocks gives a `(12,5,2)`
cover, and `C(12,5,2)>=9`. The target's specialization of Horsley's Theorem
14(a) is correct: `v=12`, `k=5`, `lambda=1`, `r=3`, `d=1`, and `n=2` give
`alpha=11/12`, `beta=1/3`, and lower bound `ceil(384/47)=9`.

The twenty blocks have total point degree 120, only three above `13*9`.
Partitioning this excess gives exactly

```text
(12,9^12), (11,10,9^11), (10^3,9^10).
```

Thus every proposed cover appears in one of the three searched profiles.
Repeated blocks do not create an omitted case: duplicates never improve
coverage, and any smaller simple cover could be padded by unused blocks to a
twenty-block simple cover.

For any degree-nine point `p`, its complete link is one of the 107 classified
nine-block `(12,5,2)` covers. Choose `p` so that its link class has maximal
catalogue index among all degree-nine points, and relabel that link to its
published representative. The primary search enumerates excess decorations
modulo the full point automorphism group; the second search retains every
labelled decoration. Both are complete normalizations.

Choose a second low point `r`, outside the excess set, with maximum degree in
the first link. The twelve link degrees sum to 45. If all points outside the
at most three high points had degree at most three, even assigning degree five
to every high point would give at most `36+2|H|<=42`. The imported
maximum-degree-five theorem therefore forces the chosen degree to be four or
five. This proves that every possible second link lies in the enumerated
pointed catalogue domain.

The shared blocks of the two complete point stars correspond exactly to the
four-subsets obtained after deleting both `p` and `r`. The primary join tries
every shared-row permutation and every bijection of the induced membership
cells. The independent join extends point bijections and compares the full
multisets of projected rows at every depth. Any true identification survives
either construction. The maximal-index rule soundly discards a second link
whose class index is larger than the first; it imposes no condition on a
third link.

If the pair multiplicity of `p,r` is `k`, the two stars fix `18-k` blocks and
leave exactly `k+2`, hence six or seven, blocks. None of those blocks can
contain `p` or `r`, whose degree-nine stars are complete, so their domain is
the 462 six-subsets of the other eleven points. Every residual search enforces
the exact point degrees, all still-uncovered triples, distinct blocks, and the
maximum pair multiplicity five whenever a pair has a low endpoint. Pairs
wholly within the high set receive the permissive cap twenty.

The coarse primary filters are safe. The union of two point links has degree
at most nine at every point: each link contributes at most five and the triple
`{p,r,x}` forces a shared block containing `x`. A point or pair already above
the low limits must therefore lie in the high set, while a point too far below
its target cannot be repaired by the remaining six or seven blocks. Exact
profile margins are imposed after these necessary filters, so no
degree-eleven or degree-twelve point is silently treated as degree ten.

The primary residual solver branches on an uncovered triple. Its one- and
two-block point-star tests retain every candidate participating in a feasible
completion; progressive candidate exclusion preserves the branch containing
the first chosen block in the local order. If coverage finishes early, the
solver continues until the exact block count and every degree margin are
satisfied.

The second solver uses a materially different decomposition: it selects a
point with positive residual degree and enumerates its entire remaining star.
Every completion has exactly one such bundle. Its `missing<=10*d` test is
necessary because a six-block through the pivot covers ten triples through
that point. Excluding two designated high points from pivot selection is
safe: if only those points had positive margin, no remaining six-subset could
be added without using another point of zero margin. Both algorithms have no
time, node, or heuristic cutoff and accept success only after rechecking all
terminal constraints.

Finally, the supplied 21 distinct blocks directly cover all 286 triples. If
a cover with fewer than twenty blocks existed, adding unused six-subsets would
produce a forbidden twenty-block cover. The lower and upper arguments
therefore yield the exact value.

## Essential catalogue dependency

The final proof depends on the completeness of the 107 isomorphism classes of
nine-block `(12,5,2)` covers. I audited that reduction and replayed all three
of its algorithms.

The maximum-degree-five input is already supported by an independent
two-encoding review and proof-checked SAT/DRAT exclusions. This pass did not
regenerate its omitted 400 MB of DRAT traces. Given that bound, point degrees
are three, four, or five. The total degree 45 forces

```text
(n3,n4,n5)=(3+a,9-2a,a), 0<=a<=4.
```

A degree-three signature meets every other signature, has eleven positive
intersection multiplicities summing to twelve, and hence has exactly one
double intersection. This makes the double intersections among low
signatures a matching. The primary column-cell enumeration is exhaustive,
and its terminal objects are checked directly.

The independent catalogue audit does not import the primary enumerator. It
adjoins actual triples up to coloured incidence-graph isomorphism and fills a
whole block column at a time. It reproduces all 27 complete labelled answer
sets, including empty cases, and then independently checks nonisomorphism,
automorphism orders, and point orbits. The third marked-point decomposition
independently covers the entire degree-five portion. Together these support
the catalogue as a complete finite theorem rather than an unverified input
list.

## Reproduction and independent evidence

Using CPython 3.11.2, GCC 12.2.0, and three workers, I reran both complete
target searches:

| Search | Roots | Joined instances | States | Wall time |
|---|---:|---:|---:|---:|
| Primary uncovered-triple search | 22,224 | 2,921,529 | 124,826,554 | 893.053 s |
| Whole-star audit | 38,948 | 9,142,411 | 9,711,891 point / 1,586,004,267 bundle | 275.979 s |

Both returned `NO_TWENTY_BLOCK_C13_6_3_COVER` and matched every field of the
published summaries, including all 321 per-design records and their digests.
The upper checker, positive completion controls, two-link join control,
150-case native/reference comparison, and address/undefined-behavior
sanitizer comparison all passed.

For the catalogue, the standard-library primary search reproduced in 9.985
seconds. With CPython 3.12.14 and NetworkX 3.7, the independent audit matched
in 58.666 seconds and the marked-degree-five census in 117.924 seconds. They
recover 107 classes, 6,024 labelled completions, all 768 automorphisms, and
all 56 pointed degree-five classes.

The new `independent_audit.py` imports no module from either reviewed package.
It checks the exact catalogue projection and all 107 covers, reconstructs all
768 automorphisms using pair-colour backtracking followed by a block-family
test, and obtains the primary decoration-orbit counts

```text
954, 8451, 12819
```

and the labelled audit root counts

```text
1284, 14124, 23540.
```

It also verifies the upper cover directly. Normal and optimized Python runs
are byte-identical. Its expected output has SHA-256
`9c97b41eab688e2a09086ef143e3d86690eb1f11d4ff8df05f7a9dfba0e29d12`.

## Guarantees, assumptions, and trust boundary

The profile reduction, two-link normalization, joining completeness, pruning
logic, and upper-bound argument are proved facts and were checked manually.
The programs guarantee exhaustive rejection of their finite domains when
executed with the stated semantics. The two full searches use different
decoration domains, joins, and residual decompositions; agreement is stronger
than repeated execution of one engine.

The compact expected files are reproducibility commitments, not standalone
UNSAT certificates. They store per-root and per-design digests rather than
millions of joined configurations or proof trees. The result therefore trusts
the visible source, Python, the C++ compiler/runtime and FFI for the native
audit, operating system, hardware, SHA-256 collision resistance for compact
comparisons, and the reviewed maximum-degree-five dependency. No
floating-point decision, random sampling, solver timeout, or unproved solver
verdict enters the new final searches.

The full native audit was not repeated with the slower Python implementation;
the package's Python/native corpus and earlier 13,214-root comparison test the
port. This is not a fatal gap because the complete primary Python solver is a
separate exhaustive algorithm, but it remains part of the assurance boundary.
The theorem is not proof-assistant formalized.

## Literature status and publication readiness

The [La Jolla Coverings Repository version 1.2](https://zenodo.org/records/19735294)
still records size 21 and lower bound 20 for `C(13,6,3)`. Its live indexed
parameter page likewise displays `20 <= C(13,6,3) <= 21`. Dai--Li--Toulouse's
primary tabu-search manuscript reports a 20-block trial of cost two, meaning
two uncovered triples rather than a cover. Horsley's
[primary paper](https://arxiv.org/abs/1409.0485) supplies the exact imported
lower bound specialization.

Targeted exact-parameter and equality searches found no earlier proof of
`C(13,6,3)=21`. The equality and the 107-class catalogue therefore appear new
relative to the inspected sources, but this is bounded search evidence, not
an absolute historical-priority claim. The result is publication-ready as a
substantial computer-assisted theorem if the finite reductions, source, full
reproduction commands, and non-certificate trust boundary remain explicit.

## Strengthening and improvement opportunities

1. **Produce independently checkable nonexistence certificates.** The largest
   remaining assurance boundary is execution of millions of search instances.
   Exporting partitioned SAT/DRAT, BDD, or verifiable backtracking certificates
   for the joined roots would let a small checker validate nonexistence without
   trusting either search engine. Per-partition hashes would avoid a monolithic
   repository artifact.

2. **Formalize the universal reduction.** The degree profiles, maximal-link
   normalization, join completeness, and residual-domain proof are compact
   enough for a proof assistant. The finite search results could remain
   imported certificates while the presently human-checked bridge into those
   searches becomes kernel-checked.

3. **Complete a third full solver path.** Running the whole-star algorithm in
   pure Python over every root, or implementing a direct exact-cover/SAT model
   with a separate symmetry strategy, would remove the native C++/FFI boundary
   and provide stronger algorithmic independence. Merely rerunning the same
   native binary would add much less confidence.

4. **Classify optimal 21-block covers.** The theorem fixes the covering number
   but not the isomorphism classes, point-degree profiles, or rigidity of
   optimal covers. A canonical generator seeded by the now-complete link
   catalogue could turn the isolated upper witness into a classification.

5. **Archive the result in the external covering tables.** A conventional
   paper or archival note should package the proof, exact source commits, and
   machine-verification boundary, then submit the new lower bound to the
   maintained repository or its Zenodo successor. That would close the current
   discrepancy between the proved equality and the public `20..21` table.

These are strengthening directions. None is required for correctness of the
present exact computer-assisted theorem.
