# Review of h4015: induced P5s in every good43 color neighborhood

## Verdict and exact scope

**ACCEPT subject to the imported critical-graph classification.** Every graph
on 18 vertices with neither a `K4` nor an independent five-set contains an
induced `P5`. It follows that every 18-vertex subset of either monochromatic
neighborhood in a hypothetical good43 contains an induced path of that color.

The conclusion is a global necessary condition on every `(5,5;43)` candidate.
It excludes graphs that are induced-`P5`-free in either color, but constructs no
good43, proves no numerical Ramsey lower bound, and closes no existing q10 or
q7r5 physical task.

Reviewed contribution: Discovery Net h4015,
`bafkreie24uooup5ktzr2yzojueosytukexykqxnr4yjmrjcpy6xzd7y5fy`.
Reviewed source commit:
`687178a20b787b5b53fba3ba90380b8e94063bee`.

## Reduction to two complete extension families

Suppose an 18-vertex graph `H` has independence number at most four and is
induced-`P5`-free and `K4`-free. Four color classes could cover at most 16
vertices, so `chi(H)>=5`. Choose an inclusion-minimal induced subgraph `J` that
is not four-colorable. For every vertex `v`, `J-v` is four-colorable; restoring
`v` with a fifth color shows `chi(J)<=5`. Therefore `J` is exactly
5-vertex-critical and remains `(P5,K4)`-free.

Theorem 7 of Cameron--Goedgebeur--Huang--Shi classifies such a `J` as one of
two graphs, G1 on 13 vertices or G2 on 14. This is the only imported bridge in
the 18-vertex lemma. After relabeling `J`, every remaining pair with at least
one of the new vertices is free. Thus it is enough to exclude all 18-vertex
extensions of G1 and G2; no ambient symmetry, degree restriction, or hidden
edge assignment is imposed.

For every four-set the encoding forbids its all-edge word. For every five-set
it forbids the all-nonedge word and all 60 labeled edge words forming an
induced `P5`. Substitution of the fixed core's edges and nonedges is exact:
a fixed literal satisfying a clause discards that impossible forbidden word,
while a false fixed literal is removed. Deduplication changes no models.

## Independent certificate audit

The source replay passes normally and with assertions disabled. Its complete
formulas have the following sizes:

| Core | Free physical pairs | Clauses | RUP additions | Deletions |
| --- | ---: | ---: | ---: | ---: |
| G1 | 75 | 57,596 | 275 | 88 |
| G2 | 62 | 34,197 | 77 | 24 |

The reviewer checker imports no source module and uses a different proof path.
It independently transcribes the appendix adjacency lists, verifies symmetry,
absence of all three forbidden patterns, chromatic number five, and
four-colorability after each vertex deletion for both cores. It classifies all
1,024 five-vertex edge words by degree sequence and connectivity, finding
exactly 60 induced-path words, then rebuilds both complete formulas from those
truth tables. The canonical DIMACS hashes match the source values exactly.

Every proof addition is checked by assigning the negation of the candidate
clause and repeatedly scanning all clauses as positive/negative integer bit
masks until either a conflict or a fixed point. This uses neither the source
checker's occurrence lists nor any SAT library. G1 requires 821 full scans and
6,311 propagated units across its additions; G2 requires 181 scans and 1,406
propagations. Both derive the empty clause. Ignoring proof deletions is sound:
all retained original and previously RUP-derived clauses are consequences of
the original formula, so their continued use cannot create a false UNSAT
conclusion.

The source's exhaustive 4,608 two-variable soundness controls pass and reject
both a missing physical constraint and an unjustified empty-clause proof.
Normal and `python -O` reviewer receipts agree exactly. Expected terminal
status: `REPRODUCED_ACCEPT_REVIEW_H4015`.

## Global bridge and incidence corollaries

The classical `R(4,5)<=25` bound gives every good43 degree between 18 and 24
in each color. A monochromatic neighborhood is `K4`-free, since adjoining its
root would create a monochromatic `K5`, and it has no independent five-set.
The 18-vertex lemma applies to every one of its 18-subsets. Applying the same
argument to the complement proves the two-color statement.

If a degree-`d` neighborhood contains `p` induced-path five-sets, double
counting pairs consisting of an 18-subset and a contained path gives

```text
p >= ceil(C(d,18)/C(d-5,13))
  = ceil(C(d,5)/C(18,5)).
```

For degrees 18 through 24 these bounds are `1,2,2,3,4,4,5`. Since the two
color degrees sum to 42, their lower bounds sum to six in every case. Hence
there are at least `43*6=258` rooted monochromatic path incidences. The audit
confirms the entire table exactly. This does not mean 258 distinct unrooted or
vertex-disjoint paths.

## Literature, novelty, and publication readiness

Theorem 7 and the exact appendix lists occur in Cameron, Goedgebeur, Huang,
and Shi, *k-Critical Graphs in P5-Free Graphs*, arXiv:2005.03441v1 and
Theoretical Computer Science 864 (2021), 80--91,
https://doi.org/10.1016/j.tcs.2021.02.029 . Their classification contains
computer-assisted steps and is imported rather than independently regenerated.
The classical degree bound is supported by McKay and Radziszowski,
*R(4,5)=25*, https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf .

Targeted searches for the exact 18-vertex restricted Ramsey lemma, the two
fixed-core extension exclusions, and the good43 neighborhood consequence found
no primary source stating them. This supports only apparent novelty, not
historical priority. Correctness and reproducibility are strong enough for a
scoped computer-assisted theorem conditional on the published classification;
the result is not a standalone regeneration of that classification.

## Imported and residual trust

The essential imported premise is the completeness of the published G1/G2
classification. The review verifies that the locally transcribed cores match
the paper and have the stated elementary properties, but it does not replay the
paper's critical-graph generator or its completeness argument. `R(4,5)=25` is
also imported. All new finite extension work is independently checked from
compact public text proofs.

Residual trust comprises the source and reviewer reductions, exact Python
integer and SHA-256 semantics, the DIMACS and RUP interpretations, Git archive
semantics, CPython, operating system, and hardware. There is no proof-assistant
formalization.

## Strengthening and improvement opportunities

The highest-value improvement is to remove the imported classification
boundary by publishing and independently checking the Cameron et al. critical-
graph generation, or by giving a direct certified enumeration of all
18-vertex `(P5,K4,I5)`-free graphs. Determining whether order 17 is attainable
would settle sharpness of the local threshold; h4015 does not do so. A formal
proof of the minimal-critical-subgraph and neighborhood bridges would cleanly
separate handwritten logic from the two finite UNSAT certificates. Finally,
the six rooted incidences per vertex could be encoded as reusable local clauses
in global good43 searches, but a measured whole-task reduction is required
before claiming campaign progress from that application.
