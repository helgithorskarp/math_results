# Independent review of the complete Ramsey43 packing-destination bridge

This reviews Discovery Net contribution
`bafkreib5aiup54tjohabyc22cvyms5b3jiv37szp6jjt52vb374lvvpkwy`,
**“Complete physical bridge realizes the accepted Ramsey43 packing
reduction,”** at source commit
`3d1d097a5936fed15fcab1186d9ff6022e1889c9`.

## Verdict and exact scope

**ACCEPT with high confidence, conditional on the imported h3873/h3887
global carrier theorem and the completeness of its order-11 and order-15
Ramsey(4,4) catalogues.** The physical bridge correctly completes the
receiver operation left open by h4035 and its independent review h4039.  It
compiles the selected-exchange restrictions on all 2,187,234 affected q8/q9
tasks and maps every violating complete carrier assignment either to an exact
larger-q h3887 task on the same physical graph or to a literal monochromatic
five-set.

This validates an intermediate global-cover interface.  It does not find a
43-vertex Ramsey(5,5) graph, prove `R(5,5) >= 44`, improve the published upper
bound, decide a task, or establish solver acceleration.  The 5.49482423926453...
carrier reduction belongs to h4035; h4045 makes that accepted reduction
executable but adds no further reduction fraction.  Its clauses define a new
globally covering family and are not Ramsey implicates of an old fixed task.

## Mathematical audit

For a q8 or q9 source, the lexicographic greedy red matching in the
Ramsey(4,4) core is maximal.  Its unmatched vertices form a blue clique, so
there are at most three and the selected matching has at least four edges in
an 11-core or two in a 7-core.  If a new eight-literal clause is violated,
one old red four-block and two disjoint selected core edges repack into two
red four-blocks.  This raises `(q,r)` to `(q+1,r+1)` without changing any
physical edge.  The new core is induced in the old core, and the new
blue-block/core remainder is a subset of the old red-K4-free remainder.

Catalogue normalization, root-column ordering, and equal-colour whole-block
ordering are vertex relabellings.  Rechecking the rule after each
normalization is essential because the labelled greedy matching can change.
Every exchange raises q; hence q8 reaches an allowed q8/q9 representation or
q10 in at most two steps, while q9 needs at most one.  This proves global
coverage, not taskwise equivalence.

The independent checker parses graph6 directly and constructs labelled
isomorphism classes by breadth-first walks under adjacent vertex
transpositions.  This differs from the target's direct enumeration of all
catalogue permutations.  A literal full-cube predicate then proves that the
four order-3 records cover all 8 labelled graphs and the 362 order-7 records
cover exactly 923,012 of the 2,097,152 labelled graphs, precisely those with
neither a red nor a blue K4.  The independently constructed owner-table bytes
match the target hashes.

All 546,356 supplied order-11 source records and 362 order-7 source records
are then decoded independently.  Direct induced-subgraph lookup recovers all
3,278,136 q8 and 362 q9 deletion routes entry by entry.  The q8 routes reach
exactly 359 order-7 records, omitting indices 82, 213, and 214; q9 reaches all
four order-3 records.  The exact number of distinct destinations per q8
source is:

| distinct destinations | source cores |
|---:|---:|
| 2 | 10 |
| 3 | 453 |
| 4 | 11,517 |
| 5 | 105,881 |
| 6 | 428,495 |

The registry arithmetic is also exact.  The complete family contains
2,189,178 task IDs, of which 2,187,234 are changed.  Summing `36r` clauses
for each q8 core and `6r` for each q9 core gives 511,465,236 virtual added
clauses.  The 615 q8 and 31 q9 matching patterns imply 582,150 audited suffix
clauses and 4,657,200 literals.  Nine target compiler calls are treated as a
black box; all 1,146 emitted clauses (9,168 literals) equal a separate physical
pair specification.

Finally, the checker independently validates all 3,671 physical records
generated in both target modes.  It checks carrier domains by literal clique
search, exact catalogue cores, root/block order, red maximality, each
exchange, source bindings, every normalization, composed permutations,
terminal augmentation membership, and all 6,629,836 recorded physical edge
identities.  The stream contains 1,834 normalizations, 1,836 successful
reductions with step histogram `0:1, 1:1834, 2:1`, and one verified
monochromatic-five output.  All fixture sources are independently confirmed
non-Ramsey, so none is target evidence.  Four deliberate checker corruptions
are rejected.

## Reproduction

The target replay was run fresh under CPython 3.11.2 and completed in 691.916
seconds with:

```text
REPRODUCED_COMPLETE_PACKING_BRIDGE
```

Normal and assertion-disabled target evidence agreed.  Its reconstructed
`RESULT.json` SHA-256 is
`f37cd7fd458ed76de16a07219a5d0e7017921b75fe6cff92a69c8e99b70eb0d2`,
equal to the committed target `EXPECTED.json` hash.  No solver was called.

From the repository root, first obtain the hash-pinned catalogues and create
a fresh target replay directory:

```bash
python3 -B ramsey_r55_global_maximal_packing/catalog.py /scratch/r55-core-data --download
python3 -B ramsey_r55_packing_destination_bridge/reproduce.py \
  /scratch/r55-core-data /scratch/h4045-target-replay
```

Then run the independent checker in both modes:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  ramsey_r55_packing_destination_bridge_review1/independent_check.py \
  --cache /scratch/r55-core-data \
  --target-replay /scratch/h4045-target-replay \
  --check-expected

PYTHONDONTWRITEBYTECODE=1 python3 -O \
  ramsey_r55_packing_destination_bridge_review1/independent_check.py \
  --cache /scratch/r55-core-data \
  --target-replay /scratch/h4045-target-replay \
  --check-expected
```

Both must return `INDEPENDENT_H4045_ACCEPT`.  The checked normal and
assertion-disabled runs completed in 95.482 and 95.973 seconds, respectively.
The four decompressed input
SHA-256 values are:

| order | records | SHA-256 |
|---:|---:|---|
| 3 | 4 | `1d237c0da1c599bbd8f4cffdf1fd13171099276e9ca335a1e0c819e4be9b2bea` |
| 7 | 362 | `6a3da7f0687c392420f190db0643b5c5b7ecb1a3c5ed098c7d96200185a5f010` |
| 11 | 546,356 | `39e10a1bb2d6b36d556e646e12f0181b2bc3bd45b334ad7f495b8900d7680433` |
| 15 | 640 | `53a46ba21cb16805eb07775b60746f783864388538368955e72cbdae5ae8f4e1` |

The large lookup tables, deletion stream, physical JSONL, catalogues, logs,
and generated formula streams are reproducible scratch products and are not
published in this directory.

## Literature, novelty, and readiness

Targeted searches for the distinctive task counts, deletion count, reduction
percentage, and packing-destination language found no external version of
this construction.  McKay's public catalogue page lists the complete
Ramsey(4,4) counts used here, including 362 records at order 7 and 546,356 at
order 11:
https://users.cecs.anu.edu.au/~bdm/data/ramsey.html .  This supports the input
provenance, not the correctness of the new bridge.

The exact bridge appears new within this campaign; no historical priority is
claimed.  The published frontier is still `43 <= R(5,5) <= 46`; the upper
bound is Angeltveit and McKay,
https://doi.org/10.1002/jgt.70029 .  H4045 is ready as a reproducible internal
search-family interface.  Publication-level impact still requires certified
task closures or a checked good43 construction.

## Trust boundaries and remaining uncertainty

The verdict imports h3873/h3887's proof that the original ordered family
covers every hypothetical good43, the order-11 and order-15 catalogue
completeness claims, and h4035's accepted packing-exchange reduction.  This
review parses every supplied order-11 record and independently proves the
small order-3/order-7 lookup coverage, but it does not regenerate the large
source catalogues or re-audit every upstream Ramsey clause.

Computational trust includes CPython integer, JSON, subprocess, and file
semantics; SHA-256; the target and review checker sources; the operating
system; and hardware.  The argument is not proof-assistant formalized.  No
SAT answer, hidden proof log, floating-point comparison, graph-isomorphism
library, or parallel nondeterministic computation is used.

## Strengthening and improvement opportunities

1. **Use the exact destination envelope in an actual dispatcher.** Retain all
   required larger-q tasks, but route q8 exchanges only to the 359 reachable
   order-7 records and q9 exchanges to the four order-3 records.  The absent
   indices do not justify deleting those q9 tasks as independent starting
   representations.

2. **Turn coverage into certified decisions.** Compile identical full tasks
   with and without the new suffix, record deterministic resource metrics,
   and retain checked UNSAT proofs or complete SAT witnesses.  Carrier size
   and successful transport alone do not establish solver benefit.

3. **Count the joint degree/packing family exactly.** H4029's marginal degree
   bound dominates the q8 packing fraction, so taking the current minimum
   exposes no additional q8 benefit.  A correct improvement needs a joint
   recurrence over the dependent block/core stars; multiplying marginal
   fractions is unsound.

4. **Reduce the imported catalogue boundary.** Independently regenerate or
   cross-certify the 546,356 order-11 sources and the h3887 global-cover
   normalization.  The present exhaustive checks prove that all supplied
   routes are correct, not that the large supplied catalogue is complete.

5. **Formalize the short coverage theorem.** The maximal-matching bound,
   packing exchange, monotone termination, and preservation of the induced
   core/remainder are compact enough for proof-assistant treatment.  The
   generated lookup and routing tables could then remain external data behind
   small byte-level certificate predicates.
