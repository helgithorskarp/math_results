# Every H517 subgraph on at most 508 vertices is four-colourable

**Exact computer-assisted theorem.** Every subgraph on at most 508 vertices
of the fixed exact H517 unit-distance graph G is four-colourable. This includes
vertex- and edge-deleted subgraphs. The entire target-order family on this
support is closed, so deleting vertices or edges of G cannot produce the
sought record graph.

This is a fixed-support negative result. It supplies no new five-chromatic
graph, makes no claim about other supports or added points, and does not
improve the Hadwiger–Nelson record. The search will leave H517 at this boundary.

The bounded decision over the preceding **39,453-case complete frontier**
finished after **16 full-graph queries, all SAT**. Eight positive witnesses
subsume all sixteen and cover the whole frontier. The public certificate is
only **4,511 bytes**. More directly, these witnesses and the inherited
colourings force 496 vertices and cover every nine-subset of the other 21.
The public checker proves the closure by that direct finite cover; it does
not assume the previous family theorems or frontier census.

## Exact graph

G consists of the 510 increasing labels marked `510` in
[`certificate_H510.json`](../hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json),
followed by exact completion-centre indices
`327,439,671,1040,1074,1377,1383`, in that order, in
[`fresh_candidates.json`](../hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json).
These are the G vertex indices used below, not original Heule or Parts labels.

Coordinates have denominator 96 in the positive-radical basis

```
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

The checker reconstructs all 517 distinct points and tests all 133,386
unordered pair distances exactly in `Q(sqrt(3),sqrt(5),sqrt(11))`.
The full graph has 2,555 unit edges. L is the block with zero coefficients
in basis positions 2,3,6,7 in both axes; it has 375 vertices. Its complement S
has 142. There are 1,920 edges within L, 605 within S and 30 across blocks.
The ordered edge-stream SHA-256 is

```
93bec44c9bc6e2514ed4d4b75985267561f63751eaa7132ec5cdd271af85e456
```

## Positive proof of the whole-family closure

A proper four-colouring of G-D restricts to every subgraph that omits all
of D. Consequently every non-four-colourable subgraph of G must intersect
every such certified D. In particular, a colouring after deleting one vertex
forces that vertex to be present in every non-four-colourable subgraph.

The 955 inherited colourings from the
[preceding certificate chain](../hadwiger_nelson_heule517_large4/README.md)
are decoded and checked anew. They yield 490 singleton-forced vertices.
The eight new rows in [`certificate.json`](certificate.json) have omission sets

```
{130}, {194}, {254}, {285}, {395}, {470}, {192,245}, {332,338}.
```

Each row is a full 517-character string over `.0123`, with dots exactly at D.
The `native_index` field records which of the sixteen original queries
produced it; it is unnecessary for decoding the public colouring.

The combined 963 rows normalize to an inclusion antichain of 538 sets:
**496 singletons and 42 non-singleton sets**. The singletons force 367 L
and 129 S vertices, without any order restriction. The only vertices that a
non-four-colourable subgraph could omit are

```
189,192,211,228,245,325,332,338,361,378,379,
432,434,505,510,511,512,513,514,515,516.
```

Every non-singleton minimal cut lies entirely in this 21-element set.
The checker directly exhausts all
`binomial(21,9)=293,930` nine-subsets and finds a certified cut contained
in each one. There is no uncovered nine-subset.

Suppose a subgraph K of G with at most 508 vertices were non-four-colourable.
It would retain all 496 forced vertices and omit at least nine of the other
21. Choose nine of those omissions. They contain a certified D, so the
colouring of G-D restricts to K, a contradiction. This also handles smaller
graphs and edge deletions. The argument requires positive witnesses and a
complete finite cover, with no negative solver premise.

## Bounded discovery and independent verification

The frozen [`plan.json`](plan.json) allowed at most 256 candidate queries,
each with 100,000 conflicts, and a 4 GiB address-space bound. The starting
frontier was the complete 39,453-row stream from
[`whole_cover`](../hadwiger_nelson_heule517_whole_cover/README.md), pinned by
SHA-256 `3de1463a2764ad16633e48709626339974dee986559e23f4452b2680d98192d1`.
Queries cycle through large-omission counts 5,6,7,8,9, starting with 5,
and choose the least lexicographic surviving tuple in each nonempty bucket.
Every positive cut removes covered candidates across all buckets.

The full activated graph formula has 2,585 variables and 10,738 clauses.
Colour variable `x(v,c)` has index `4v+c+1`; activation `a(v)` has index
`2069+v`. Clauses are `not a(v) or x(v,0) or ... or x(v,3)`, one binary
colour inequality per unit edge and colour, and `not a(0) or x(0,0)`.
All 517 activation literals are specified for every query. Omitted vertices
may have all colour variables false. At-most-one colour clauses are not
needed: adjacent vertices have disjoint nonempty true-colour sets, so
choosing any true colour gives a proper colouring. Conversely a proper
colouring gives a model; if vertex 0 is retained, a colour permutation makes
its colour zero. No intact-L boundary profile restriction is imposed.

Each SAT model is decoded and checked against the whole exact graph, then
greedily extended over omitted L vertices followed by omitted S vertices,
both in increasing order. The full resulting colouring and its exact residual
omission set are checked again. A candidate is removed only when it omits
every vertex of that residual set.

All sixteen queries were SAT. There was no UNKNOWN, negative target or
limit extension. Their eight inclusion-minimal witnesses finish the entire
family. Discovery took **2.7036 seconds**, peak RSS **46,776 KiB**, using
python-sat 1.8.dev24 and CaDiCaL 1.9.5. The conditional negative-certification
branch was not exercised, and no proof trace is needed for the result.

The separate [`verify.py`](verify.py) imports neither the producer nor a SAT
package. It reuses the pinned reviewer-owned exact geometry and original
witness decoder from the
[accepted preceding review](../hadwiger_nelson_heule517_large4_review1/README.md).
It checks all 955 inherited colourings (2,426,493 retained-edge inequalities),
all eight new colourings (20,351 inequalities), the final antichain and
forcing, and all 293,930 final omission sets by direct set containment.
Controls reject a monochromatic unit edge and an incorrect omission set.

The optional native audit independently regenerates the old 39,453-case
frontier using set-valued deletion/contraction, checks all sixteen native
colourings (40,628 inequalities), compares the retained public witnesses and
their subsumption, replays every round-robin choice and pruning count, and
compares the actual activated CNF entry by entry with an independent generator.
It verifies that the final frontier file is empty. This audit took
**7.9973 seconds**, peak RSS **55,264 KiB**; the direct final cover itself took
0.5785 seconds.

## Reproduction

The public mathematical check needs only Python 3.11.2 and the standard
library. From the repository root:

```bash
python3 -B hadwiger_nelson_heule517_whole_decision/verify.py
```

Expected fields include `fixed_support_closed=true`,
`unrestricted_at_most508_family_closed=true`, `new_colourings=8`,
`forced_vertices=496`, `nine_sets_checked=293930` and
`uncovered_nine_sets=0`. No old census or family theorem is assumed.

To regenerate the discovery and optional audit, use new output directories,
a Python environment with `python-sat==1.8.dev24`, Kissat 4.0.4, and drat-trim:

```bash
python3 -B hadwiger_nelson_heule517_whole_cover/enumerate.py --out /tmp/h517-old-frontier
python3 -B hadwiger_nelson_heule517_whole_decision/run.py \
  --work /tmp/h517-whole-decision \
  --frontier /tmp/h517-old-frontier/frontier.txt \
  --kissat /path/to/kissat --drat /path/to/drat-trim
python3 -B hadwiger_nelson_heule517_whole_decision/verify.py \
  --work /tmp/h517-whole-decision
```

Kissat and drat-trim are required arguments only for the conditional negative
branch; neither is invoked in the published all-SAT transcript. Kissat source
was `8af8e56f174b778aef3aa45af9f739b2a5f492c2`; drat-trim executable SHA-256
was `bc7543a99da8521ddb09af442698956054f11e10d198bd482ac756535244c021`.
Native formulas, full witness sequence, logs and operational checkpoints
remain local. Public source, compact colourings, manifests and audit summaries
are sufficient to reproduce the theorem.

The new proof's trust boundary is the exact source coordinates, independence
of the radical basis, Python integer and Fraction arithmetic, faithful
colouring decoding, the complete finite enumeration and the restriction
argument. Solver soundness is unnecessary once the positive witnesses are
checked. The enumeration and new audit are author-run; the preceding accepted
review is evidence for the reused foundation, not a separate-author review
of this new closure. No proof-assistant formalization is claimed.

## Decision and dependencies

The H517 support is closed for the at-most-508 target and is retired from
deletion-only search. No further H517 deletion stratum, runtime extension,
background job or proof is in progress. The following pass should choose
a genuinely different exact support or family mechanism after coordination,
with a criterion that changes the large/small interaction rather than
continuing this support's deletion ladder. No new support is constructed here.

The whole-frontier census is at source
`d593c9ae774d6b296f73aa4a2c71f55158bde776`, Discovery Net height 3162.
The preceding positive-certificate closure is at source
`fe8f1593bcfec80c71adfc55f60b28d58428d70d`, height 3146; its independent
acceptance is at source `f93567218dc046d2c22d068fd15741e85ff63e4e`, height 3154.
This pass uses their durable source and positive witnesses while checking
the final whole-family cover directly. HN-3's separate geometric-construction
lane and the parked HN-1 census, H574 closure and timed-out QBF configurations
remain separate and are not restarted.

The final shared refresh reached Discovery Net height 3167. HN-3's new
[double-spindle result](../hadwiger_nelson_heptagon_double_spindle/README.md),
source `0d0e135f975a273391ae61f6c5080d41b087f259`, height 3166, was inspected:
every colouring of its fixed heptagon host extends to the aligned 522-point
double sum, closing all 210 listed target restrictions. That universal
extension does not cover relatively rotated factors or changed hosts and
supplies no premise for this H517 theorem. No new overlapping work or objection
to the H517 frontier appeared in the refresh.
