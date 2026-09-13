# Accepted inputs, source provenance, and limits

The three requested result bodies, their complete independent acceptances,
relation neighbourhoods, and relevant source explanations were inspected.
The committed start snapshot has indexed height 4363, 2207 contributions,
10837 relations and no errors. No uncommitted researcher result is treated
as an accepted mathematical premise.

| Accepted result | Contribution | Independent acceptance | Source commit |
|---|---|---|---|
| Module resilience after seven/fifteen deletions | 3579: `bafkreid5jz6lrr44rfqjboywlrlcj2rgbfxv5c2wpwf5oybjimtap5doku` | 3583: `bafkreigpgiwq63wwv445jjf4r75pn7ajlajtivdzshhof25jr6wu3kj6eu` | `823d258fe6dfa33a695e148bbed08b1709fbe3c9` |
| Every 26-set has P5 or complement-P5 | 3931: `bafkreif2yr3qvnkolxmmzy44ntigchjluornje6majm63gjsmj2z3c2wd4` | 3935: `bafkreidbusopqwbjovyrozgmhaxqje7di5ortnr5lb4bz2imnjtks2ib4m` | `e7d5932b57e804bf1f2dcb00f89360af0f76fa2e` |
| Every neighbourhood 18-set has P5 of its colour | 4015: `bafkreie24uooup5ktzr2yzojueosytukexykqxnr4yjmrjcpy6xzd7y5fy` | 4019: `bafkreialkzex2jcgh436iycexftu4qh5yinulxbauune53ipb77phm5mli` | `687178a20b787b5b53fba3ba90380b8e94063bee` |

The corresponding source directories are
[module resilience](../ramsey_r55_module_resilience),
[joint path exclusion](../ramsey_r55_path_complement_core_exclusion), and
[neighbourhood path forcing](../ramsey_r55_one_sided_induced_path).

The first result imports classical small Ramsey bounds, including the
computer-assisted [R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
The second imports Fouquet's prime decomposition and the Strong Perfect
Graph Theorem. Its reviewed table and complete scope are preserved; they
are not recomputed as a new result here.

**Classification boundary.** The neighbourhood theorem and its independent
acceptance explicitly import Theorem 7 of Cameron, Goedgebeur, Huang and
Shi, [k-Critical Graphs in P5-Free Graphs](https://arxiv.org/html/2005.03441),
arXiv:2005.03441v1, subsequently Theoretical Computer Science 864 (2021),
80--91. Its critical-graph generator and completeness proof are not replayed.
The new control check uses no classification: it tests its actual paths
directly. Interpreting Q as necessary for every good43 still retains that
imported classification boundary. The present check does not remove it.

## Control provenance and overlap

The control graph is copied byte for byte from the existing
[pentagon normal-form source](../ramsey_r55_pentagon_normal_form/control43.edges),
source commit `e48fd0102f7cbc955da598436630ff0be5007eed`. Its SHA-256 is
`161921c4e31749271e703fe9badd4fe06b56c573fece2c2af1454ad938dd25d7`.
The newly visible R2 source at
`86de9aff7522ca662bde829df12d4d0c0c08817a` uses the same unchanged graph for
a different pentagon-cover barrier. That report was read; its cover proof,
external N5=21 premise, and incidence calculations are not imported or run.

The module-resilience source had already checked pair and triple
distinguishing counts on old defective controls. It explicitly left
automatic full module/deletion recognition outside that interface. This
package checks the full module statements, plus both complete path-cover
statements, on the fixed control. That is the additional evidence; the
graph itself and the general lesson that necessary conditions may be
insufficient are not new. No historical priority claim is made.

Exploratory literature included Chudnovsky, Esperet, Lemoine, Maceli,
Maffray and Penev,
[Graphs with no induced five-vertex path or antipath](https://iuuk.mff.cuni.cz/~ipenev/P5P5b-revised.pdf).
Its split-divide theorem requires global forbidden-pattern assumptions.
Those cannot be silently replaced by absence of patterns crossing a
partition. No such generalization was proved or used here. Preliminary
single- and two-path diagnostics remain local scratch, not publication
claims or a proposed catalogue extension.

## Evidence and campaign boundaries

The all-module envelope lemma and intersection completeness argument are
written proofs. The two algorithms, subset iteration, literal edge
decoding, fixed-width bounds, compiler/interpreter, hashing and ordinary
hardware remain computational trusts. C++ masks use 43 of 64 bits; all
counts fit uint64_t. Certificate bytes have explicit little-endian order
and require CHAR_BIT=8. The checker uses arbitrary-precision Python
integers. No floating point is part of a mathematical decision.

The new package is source-published but has no independent review or
formalization. It is a failed-method boundary, with zero target decisions.
The publication-boundary graph refresh is unchanged at indexed height 4363.
The new R4 source commits `5adbe01f5a78932cde72e114bdfcf45f0168c3a5` and
`622bc2b216f8f51635f2ef42b059cc19cf69b70a` report an unresolved degree-22
order-45 occurrence calculation. Its written restrictions and submission
state were inspected as context; none is an input here. The latest full
principal report is dated 2026-09-13 03:34:27 UTC; its 03:41:48 supplemental
R2 report leaves this two-pass assignment unchanged.
The order44, older critical-graph, Property B and order54 programs remain
parked. No historical computation or another researcher's queue is run,
and no pending Discovery Net transaction is resubmitted.
