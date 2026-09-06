# Bounded global H560 decision: the 310-absent case closes; the target remains open

Using the complete 60-selector equivalence, one bounded global-family pilot
produced **35 verified four-colouring covers and 80 certified obstruction
supports**. Three covers force the additional vertices **310, 393 and 578**.
In particular, the entire case with 310 absent is four-colourable, so only
the 20-state left interface is needed for a remaining obstruction.

The smallest certified obstruction has **516 vertices**. A compact set of
deletion witnesses also proves that one specified 516-vertex support is
vertex-critical. This is above the 509-vertex baseline. No graph on at most
508 vertices, complete family closure, or complete residual frontier was found.

The terminal decision is **NO GO for extending this same boundary-enumeration
pilot without reassessment**. An explicit family of **194,580** exact-508
supports is outside both the new covers and all ten earlier Kempe covers.
This is a rigorous lower bound on the supports those positive certificates
leave unresolved, not a non-four-colourability claim about them. No subsequent
search, support refinement or geometric construction phase has begun.

## Recovered input and precise family

The [completed left-selector theorem](../hadwiger_nelson_heule560_left_relation/README.md)
was recovered from source commit `4562cbc6d90e7c33ff497752b599e43e7f3c01d6`
and Discovery Net contribution
`bafkreici45gf7ulztnrxhvwxwx4j33tep5fwyzu2if3kwrjyesckmc6fi4`, height 3421.
Its enumeration and proof were **not recomputed**. The saved committed
confirmation, proof manifest and prior audit repaired the missing controller
report. Its new [independent acceptance](../hadwiger_nelson_heule560_left_relation_review1/README.md)
was inspected before this publication.

Use the parent's exact H632 host labels and the H560 partition into M of
size 492 and U of size 68. Erase

```
D = {510,512,513,520,521,523,524,535}.
```

Write G552 for the resulting induced support and V for its 60 optional
vertices, in the increasing order supplied by [certificate.json](certificate.json).
For T contained in V, the graph under study is G552[M union T]. Every
potential at-most-508 obstruction in H560 is equivalent to one with exactly
16 of these selectors. The parent mandatory theorem handles all subsets
missing a vertex of M. Padding handles sizes below 508.

The exact [separator theorem](../hadwiger_nelson_heule560_separator/README.md)
provides a right block with 196 vertices, 806 edges and 19 shared mandatory
vertices Q. Its interior has 59 optional vertices. The remaining selector is
310, in the left block. Let R_B denote all right-boundary words attainable
with right optional set B, allowing arbitrary interior recolouring. Then

```
G552[M union T] is four-colourable iff
  R_(T minus {310}) intersects P72, if 310 is absent;
  R_(T minus {310}) intersects P20, if 310 is present.
```

Here P20 is a subset of P72 of sizes 20 and 72. These are the complete
left relations, not restricted colouring templates. The new computation
never fixes an interior colouring of the right block.

## Positive family facts and the 516-vertex obstruction

The 35 positive rows retain respectively 55, 56, 57, 58 or 59 of the 60
selectors, with multiplicities 1, 6, 7, 18 and 3. Each row supplies an actual
proper right-block colouring and its allowed left-boundary word. The checker
pastes an inherited left witness, then checks the entire selected graph.
Restriction proves four-colourability for every subset of each cover.

The three 59-selector covers omit, individually, 310, 393 and 578.
Consequently every obstruction in G552 contains all three. Erasure equivalence
gives the same necessity in H560. In particular G552 minus {310}, on 551
vertices, is four-colourable, and the equivalent entire H560 family with 310
absent is closed. This disposes of all C(59,16)=109,712,808,959,985 canonical
exact-508 supports in that case, without enumerating them. Some were already
covered by earlier certificates; this count is not a newly covered increment.

Within G552, the mandatory set can now be strengthened to
M union {310,393,578}, of size 495. A remaining target contains at most 13 of
the other 57 optional vertices and uses P20 on the left. Other positive covers
give further necessary selector clauses, not a complete description.

The 80 negative supports use 24 through 33 optional vertices. Their complete
size census appears in [expected.json](expected.json). Each is five-chromatic:
the combined checked refutation below proves the lower bound, and the
inherited five-colouring is checked on every retained edge.

For negative row 52 (zero-based), the optional set is

```
310 358 361 362 393 406 407 409 416 431 434 454
498 500 539 569 578 586 596 609 610 612 613 615
```

Together with M it defines the specified 516-vertex graph. All 24 optional
single deletions have new proper witnesses. Deletion of any of the 492
vertices of M is four-colourable by restricting the accepted parent deletion
witness. Therefore every vertex deletion is four-colourable, proving
vertex-criticality. This says nothing about edge-criticality or minimum order
among all graphs in the family. Public minimality evidence is retained for
this one core only; the other 79 negative rows are asserted to be obstruction
supports, with no public minimality claim.

## Exact encoding and negative certificate

The oracle has 916 variables and 6,017 clauses. Give every right vertex four
one-hot colour variables, including omitted optional vertices, and introduce
all 60 selectors. For each right edge and colour, guard the unequal-colour
clause by the negative selectors of its optional endpoints. An absent vertex
can receive any colour, with all its edge constraints disabled.

Introduce one gate for each of the 72 boundary words and require at least
one gate. A gate implies its 19 boundary colours. For every word outside P20,
add `not selector[310] OR not gate[word]`. There are no further boundary pins,
palette restrictions or interior templates.

A model chooses an allowed word and a proper colouring of the selected
right graph. The imported left equivalence supplies a matching left
colouring, which glues to a proper full-graph colouring. Conversely a proper
full-graph colouring can be globally relabelled to its normalized boundary
word, extended arbitrarily to absent vertices and encoded by setting that
word's gate. This proves both directions of the oracle equivalence.

To certify all 80 negative supports at once, append a case gate for each
negative mask. Require at least one case; each case implies inclusion of
all selectors in its mask. No exclusion of other selectors is needed. A
model restricts to a colouring of one alleged obstruction. Conversely a
colouring of any alleged obstruction extends to a model with exactly its
mask selected and its case gate true. Thus UNSAT proves all 80 negative
assertions. Multiple gates need no separate exclusivity constraint.

The combined CNF has **996 variables and 8,226 clauses**:

| Artifact | SHA-256 |
| --- | --- |
| Oracle CNF | `4682363b5c0afd715b028e2214191f2710260a5c74c29cf89934ad538df6465e` |
| Combined negative CNF | `bde148aa4dc1d8e1ce8a378f2168a79f19fe84d028cb4b9fd8a9cf49649ef832` |
| Executed DRAT | `16ff41fc5a85e41b42f6950b54f871dd08912850c06f1f0a1dd79846737a2581` |

The proof has 1,596,382 bytes and remains local. Kissat returned UNSAT;
drat-trim returned exit 0 and the exact line `s VERIFIED`. The independently
constructed CNF matched byte for byte and the proof checked against it too.
The public verifier can regenerate the proof. There is no fresh direct
516-vertex colouring CNF: its lower bound uses this checked right-block
encoding and the explicitly imported left theorem.

## Bounded execution and the residual decision

[plan.json](plan.json) was frozen before the new native queries. A MARCO-style
master represents as-yet unclassified selector masks. A positive cover P
excludes its downward cone by the clause `OR_{v outside P} selector[v]`.
A negative mask N excludes its upward cone by
`OR_{v in N} not selector[v]`. The oracle greedily grows positive masks and
shrinks negative masks in increasing host-label order. Positive master phases
prefer larger masks. The initial empty/full answers are controls of this
new right encoding, not a rerun of the left classification.

The limits were 128 completed boundary rows, 12,000 oracle queries and 300
search seconds. Individual queries had a 200,000-conflict/10-second limit.
The current grow/shrink unit was allowed to finish at the time boundary.
The run finished 115 rows and 4,249 oracle queries in 301.91 search seconds;
the terminal check and combined proof brought the total to 306.24 seconds,
excluding input geometry. It stopped at the frozen search-time condition.
No query was UNKNOWN. The maximum row count was not reached.

The terminal master enumerated 4,097 unclassified exact-16 masks and stopped
at its cap; this was not an exhaustive frontier. Of these, 3,998 also avoid
all ten accepted [one-pair Kempe covers](../hadwiger_nelson_heule560_kempe/README.md).
Eight of those ten covers are subsumed by the new positive covers. The full
terminal mask dump is local and is an operational observation, not required
for the following small, independently checked lower-bound certificate.

Put

```
F = {310,361,362,393,406,407,409,434,500,505,578,604}.
```

The [residual certificate](residual.json) verifies that F is not contained
in any of the 35 new or ten older positive covers. Thus every 16-selector
superset of F is outside every such positive downward cone. There are

```
C(60-12,16-12) = C(48,4) = 194,580
```

distinct such supports. Every negative mask has size at least 24, so none
of these 16-selector supports contains one. This proves that the two-sided
certificate leaves at least this many exact-508 supports unclassified.
It does not assert that these graphs are uncolourable, that this is the whole
residual family, or that no additional certificate can colour them.

The pilot supplies useful exact cuts and above-target obstructions but no
compact **complete** residual frontier. The campaign therefore checkpoints
and yields for reassessment, without extending the run or starting another
deletion/refinement ladder. HN-3's independently accepted paired-circle
four-clause work was inspected as separate geometric context and is not a
premise or a duplicated workstream here.

## Reproduce and trust boundary

From the repository root, with Python 3.11 or later, Kissat and drat-trim:

```sh
python3 -B hadwiger_nelson_heule560_global_decision/verify.py \
  --prove --out /tmp/hn560-global-check \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim
```

Expected: `negative_proof_verified: true`, 35 positive covers, 80 negative
supports, 24 single-deletion witnesses, eight rejected mutations,
`smallest_negative_support_vertices: 516`, forced selectors [310,393,578],
and `certified_unclassified_exact508_support_lower_bound: 194580`.
An existing raw archive can instead be checked with `--archive /path/to/run`.
`--structure-only` does not establish the negative assertions.

The public certificate is 25,474 bytes. The raw search certificate, terminal
masks, proof and logs stay outside Git. [compact.py](compact.py) retains all
positive and negative cones while selecting deletion evidence for just the
smallest core; omitted deletion witnesses are not premises of public claims.
To repeat the bounded exploratory protocol, use python-sat 1.9.dev15 / Glucose
4.1 and run:

```sh
python3 -B hadwiger_nelson_heule560_global_decision/build.py \
  --out /tmp/hn560-global-search \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim
python3 -B hadwiger_nelson_heule560_global_decision/compact.py \
  --input /tmp/hn560-global-search/certificate.json \
  --output /tmp/hn560-global-compact.json
```

The time-limited search frontier can vary across machines. The published
certificate, CNF and verification target are fixed independently of that
variation; reproducing their claims requires no search replay or unpublished
input. [run_summary.json](run_summary.json), [validation.json](validation.json)
and [proof_manifest.json](proof_manifest.json) record execution and identities.

The independent verifier imports no producer code from this contribution.
It reconstructs all 199,396 host norms using sparse-radicand arithmetic;
the producer uses ordered coefficient convolution. It checks 42,205 right
edge inequalities, 155,469 pasted full-graph inequalities, 204,629 inherited
five-colouring inequalities and 27,346 older-cover inequalities. It compares
both CNF constructions exactly. Normal and optimized-Python structural
reports agree. This is author-run algorithmic checking, not an external
review or proof-assistant formalization of the new result.

Trust remains in pinned exact coordinate inputs, radical-basis independence,
Python integer/rational semantics, the accepted M492 theorem, the complete
72-state separator and left-selector equivalence, the written encoding and
gluing arguments, and the DRAT checking kernel. Source publication alone
does not discharge these dependencies.
