# Nine disjoint cover pairs close H560 through 503 vertices

**Every subgraph of the fixed H560 support on at most 503 vertices is
four-colourable.** Nine pairwise disjoint two-vertex clauses, each justified
by an already published proper colouring, give a short counting proof.
Combined with the accepted 495 mandatory vertices, they require at least
504 vertices in any obstruction in this support.

The same nine pairs give an explicit outer family of **66,796,992** labelled
508-vertex supports containing every possible target obstruction after the
accepted erasure reduction. This is a count of supports satisfying nine
necessary clauses, not a count of unclassified graphs. The remaining target
on 504 through 508 vertices is open. No new five-chromatic graph is produced.

The bounded optimization also proves that the known cover clauses, minimum
degree four, and the full Gallai condition on degree-four vertices have
minimum order exactly **504** in the reduced family. Its attaining graph is
four-colourable. Thus these necessary conditions do not settle the target.

## Fixed graph and imported premises

Host labels are the established H632 labels. Exact coordinates are rational
coefficient vectors in
`(1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165))`;
all coefficients become integers after multiplication by 96. The independent
geometry routine reconstructs all 199,396 pair norms and all 3,112 unit edges
before restricting to a support. Coordinate inputs and other certificate
inputs are pinned by SHA-256 in [plan.json](plan.json) and the imported
[geometry package](../hadwiger_nelson_heule632_pair_pilot/README.md).

We use the following durable results without rerunning their proofs:

| Premise | Source and use |
| --- | --- |
| H560 has 492 mandatory vertices M492 | [Mandatory boundary](../hadwiger_nelson_heule632_minimize/README.md): a graph missing any one is four-colourable. |
| Eight vertices can be erased throughout the induced H560 family | [Complete left relation](../hadwiger_nelson_heule560_left_relation/README.md): erase `D={510,512,513,520,521,523,524,535}` to obtain G552 with 2,726 unit edges. |
| Three more vertices are mandatory in G552 | [Global decision](../hadwiger_nelson_heule560_global_decision/README.md): proper colourings of G552 minus 310, 393, and 578 force all three. These witnesses are checked again here. |
| Published positive covers have explicit whole-graph colourings | [Separator witnesses](../hadwiger_nelson_heule560_separator/README.md), the global decision, and [ten Kempe covers](../hadwiger_nelson_heule560_kempe/README.md). All 45 are checked again on every induced unit edge. |

Write `M495=M492 union {310,393,578}` and `U57=V(G552) minus M495`.
The accepted family equivalence reduces the at-most-508 target to induced
supports `M495 union S`, `S subseteq U57`, `|S|<=13`. Any such obstruction can
be padded to exactly 13 selectors. The inherited H560 five-colouring would
make a non-four-colourable member exactly five-chromatic.

The prior global result has an
[independent accepted review](../hadwiger_nelson_heule560_global_decision_review1/README.md).
This package is author-run independent algorithmic checking, not an external
review of its new claims.

## A solver-free proof of the lower bound

If a proper colouring is known on `G552 minus C`, any non-four-colourable
support must meet C. The following nine sets C are pairwise disjoint.
Row indices refer to the zero-based `positive_covers` array in the published
global-decision certificate; the verifier pastes its right colouring to the
matching explicit left colouring and checks the resulting whole graph.

| Pair C | Positive-cover row |
| --- | ---: |
| {358,362} | 4 |
| {361,379} | 1 |
| {406,455} | 6 |
| {407,440} | 25 |
| {409,542} | 28 |
| {431,505} | 33 |
| {434,530} | 27 |
| {500,571} | 12 |
| {604,613} | 11 |

All eighteen vertices lie in U57. Every obstruction therefore contains M495
and at least nine further vertices, giving order at least 504. This argument
uses no solver or criticality condition.

For a putative non-four-colourable induced H560 support of order at most 503,
first use the accepted mandatory theorem to force M492. Erasing D preserves
four-colourability and cannot increase its order. The three singleton covers
force the additional mandatory vertices, and the nine disjoint pairs then
give the contradiction `|V|>=504`. Any graph obtained by further deleting
edges is a subgraph of this colourable induced support and is also colourable.
The erasure equivalence is used on induced graphs only.

## Exact necessary outer family at 508 vertices

The nine pairs occupy 18 of the 57 optional vertices; 39 lie outside them.
For an exact-13 selector set meeting all pairs, let d be the number of pairs
whose two vertices are both selected. Necessarily `0<=d<=4`. Choose these d
pairs, one endpoint of each of the other `9-d` pairs, and `4-d` vertices from
the remaining 39. These choices are unique for each actual subset, so there
is no overcount from choosing a representative of a doubled pair.

```text
sum(d=0..4) C(9,d) * 2^(9-d) * C(39,4-d)
  = 42,112,512 + 21,056,256 + 3,414,528 + 209,664 + 4,032
  = 66,796,992.
```

The previous exact-size M495 domain had `C(57,13)=2,448,296,039,700` members.
Every possible obstruction in the reduced exact-508 domain lies in the new
outer family. Conversely any non-four-colourable member of this outer family
would meet the target. Thus it is a valid equivalent domain for the existence
question. Many members may already be coloured by other certificates: this
count does not impose the other 25 irredundant cover clauses, minimum degree,
or the Gallai condition. No census of these 66,796,992 graphs was run.

## The criticality test attains the bound and remains inconclusive at 508

Any smallest obstruction inside G552 is vertex-critical and five-chromatic.
It has minimum degree at least four. The subgraph induced by its degree-four
vertices must be a Gallai forest: every block is a clique or an odd cycle.
Indeed colour the complement of any such connected component. Each vertex
has a remaining colour list of size at least its degree inside the component.
The degree-choosability theorem would extend this colouring unless the
component were a Gallai tree; see Cranston and Rabern,
[Beyond Degree Choosability](https://arxiv.org/abs/1511.00350).
This is a classical necessary condition, with no novelty claim here.

The frozen search minimized `|S|` subject to all 45 cover constraints, selected
minimum degree four, and that full Gallai condition. Clause subsumption leaves
34 irredundant cover clauses. Budgets zero through eight were UNSAT; budget
nine supplied

```text
S = {361,362,406,407,409,505,530,571,604}.
```

For `G552[M495 union S]`, the verifier checks all 34 intersections, minimum
degree four, and exactly these twelve degree-four vertices:

```text
{102,109,293,296,299,302,305,308,376,578,604,608}.
```

They induce no edges, so their twelve singleton blocks satisfy the full
Gallai condition. Together with the nine-pair lower bound this proves the
exact optimum of the necessary-condition test without trusting a solver or
the producer's block algorithm. No Gallai clause was learned in the run.

One preauthorized full-colouring query for this support returned SAT.
[candidate.json](candidate.json) records a proper four-colouring of all
504 vertices and 2,462 induced unit edges. The 632-character colour string
uses `0,1,2,3` and a dot for every omitted host vertex. Its separator word is
`0101001010000203000`. The independent verifier checks the full colouring
directly, so SAT soundness and separator completeness are not needed to
accept this positive witness. It is not a critical or five-chromatic graph.

## Reproduction and auxiliary proof

From the repository root, use Python 3.11 or later and a fresh output path:

```sh
python3 -B hadwiger_nelson_heule560_criticality_bound/verify.py \
  --out /tmp/hn560-pair-bound
diff -u hadwiger_nelson_heule560_criticality_bound/expected.json \
  /tmp/hn560-pair-bound/result.json
```

This default command needs only the standard library and committed inputs.
It proves all new conclusions above relative to the stated imported premises.
It checks 122,067 positive-cover edge inequalities, the full attaining
colouring, the nine-pair certificate and count, and seven invalid-certificate
controls. Normal and optimized-Python substantive results agree. The counter
recurrence has 16 truth-table cases, and the subset counting formula agrees
with direct enumeration in 80 smaller cases.

An additional native proof certifies infeasibility at budget eight for the
encoded cover and degree constraints. The CNF contains 717 variables and
2,404 clauses; its SHA-256 is
`a0f969154804082a80061cbf8a55e5a5c3b6e1022e4dfbc498e3e8080c8e3682`.
The executed 13,445-byte DRAT proof has SHA-256
`e496e56c13645861418ece6297e181ad142726c5339da388a00109138f0db963`.
Both the original check and the check against independently reconstructed
CNF bytes returned `s VERIFIED`. [proof_manifest.json](proof_manifest.json)
records the native binary identities. This is auxiliary evidence; the
nine-pair proof already gives the stronger lower bound without degree clauses.

```sh
python3 -B hadwiger_nelson_heule560_criticality_bound/verify.py \
  --out /tmp/hn560-pair-bound-proof --prove \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim
```

The extra output is `additional_drat_check: true` plus the regenerated proof
hash. An existing executed proof can be supplied using `--archive DIR`
instead of `--prove`. All other result fields agree with `expected.json`.
Native versions used here are Kissat 4.0.4, source
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, and drat-trim identified by the
manifest. Fresh proof bytes need not agree if another valid proof is found.

The bounded producer requires `python-sat==1.9.dev15`, with Glucose 4.1:

```sh
python3 -B hadwiger_nelson_heule560_criticality_bound/build.py \
  --out /tmp/hn560-criticality-search \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim
python3 -B hadwiger_nelson_heule560_criticality_bound/candidate.py \
  --screen /tmp/hn560-criticality-search/certificate.json \
  --out /tmp/hn560-criticality-candidate --kissat /path/to/kissat
```

The executed search made ten master queries in 0.045 seconds, excluding
geometry; the search and lower proof together took 0.207 seconds. The frozen
limits were 300 search seconds, 1,000 master queries, 256 Gallai cuts, and two
million conflicts/ten seconds per master query. Exactly one candidate query
was permitted at two million conflicts/30 seconds. These timings are run
provenance, not mathematical premises. The explicit nine-pair certificate
was extracted after optimization and is reproduced by the producer's final
packaging step. [run_summary.json](run_summary.json) and
[validation.json](validation.json) preserve execution and audit scope.

The producer uses dense XOR field arithmetic. The checker imports the
independently written sparse-radical geometry and reconstructs its own CNF;
it imports no new producer code. Input theorems, exact Python arithmetic,
independence of the radical basis, the written restriction and counting
arguments, and ordinary hardware remain trusted. The optional auxiliary
UNSAT route also trusts the CNF translation and drat-trim. Raw solver logs,
CNFs, proofs and run checkpoints remain local and are regenerable. No proof
assistant or independent-author review is claimed for this new package.

## Completed milestone

The completed left equivalence was recovered, not recomputed. The accepted
516-vertex-critical example remains the smallest certified obstruction from
the preceding H560 global pilot. This pass adds the complete at-most-503
closure, the nine-pair outer-family description, and one positive attaining
witness. It does not classify the 504--508 interval or the new outer family.

The current coordination brief requires yielding after this distinct
criticality pass if it gives no smaller obstruction or full target-family
decision. No further minimization, cover refinement, right-table extension,
or outer-family census has begun. HN-3's
[realized-phase obstruction](../hadwiger_nelson_realized_phase_obstruction/README.md)
was inspected as separate geometric work and is not a premise of this result.
