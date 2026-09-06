# Independent review: every at-most-508 H517 subgraph is four-colourable

This directory independently reviews Discovery Net contribution
`bafkreihv67vpfrawafyzcloiaeybpw3dd3wlp6kzxyys2xgjq5ge73cjia`,
“Eight new colourings close every at-most-508 subgraph of H517.” The reviewed
source is
[`../hadwiger_nelson_heule517_whole_decision`](../hadwiger_nelson_heule517_whole_decision)
at commit `ee559bab803b0b5ae7095a6f69131e620a8cabe5`.

## Verdict and scope

**Accepted.** Every subgraph on at most 508 vertices of the fixed exact
517-vertex H517 unit-distance graph is four-colourable, including non-induced
subgraphs obtained by deleting edges. Thus deletion-only search inside this
support cannot produce a sub-509 five-chromatic unit-distance graph.

This is a complete fixed-support negative result. It does not construct a new
five-chromatic graph, improve the Hadwiger–Nelson record, or exclude other
supports, added points, or geometric deformations.

## Exact graph reconstruction

[`independent_check.py`](independent_check.py) imports no submitted module and
does not import the preceding reviewer checker reused by the submission. It
independently reads the 510 increasing H510 labels and the seven completion
centres `327,439,671,1040,1074,1377,1383`.

Coordinates are scaled by 96 and represented as integer coefficient vectors
in the basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

The checker implements multiplication in this multiquadratic field directly
and compares squared distances coefficient by coefficient. It verifies all
517 points are distinct and examines all `C(517,2)=133,386` pairs. The result
is exactly 2,555 unit edges: 1,920 within the 375-vertex large block, 605
within the 142-vertex small block, and 30 cross edges. The ordered edge-stream
SHA-256 is
`93bec44c9bc6e2514ed4d4b75985267561f63751eaa7132ec5cdd271af85e456`.

## Positive-certificate proof

For an omission set `D`, a proper four-colouring of `G-D` colours every
subgraph whose omitted vertices contain `D`. Therefore a non-four-colourable
subgraph must intersect every certified omission set. In particular, a
singleton omission certificate `{v}` forces `v` to occur in every hypothetical
non-four-colourable subgraph.

The checker independently decodes and validates all 955 inherited colourings
from their original compact certificate formats:

| Certificate family | Rows | Retained-edge checks |
|---|---:|---:|
| Initial H517 family | 526 | 1,336,627 |
| Final small-block family | 202 | 513,249 |
| Two-large closure | 86 | 218,392 |
| Three-large closure | 108 | 274,371 |
| Four-large closure | 33 | 83,854 |
| **Total** | **955** | **2,426,493** |

It then checks the eight new 517-character colourings and their exact omission
sets

```text
{130}, {194}, {254}, {285}, {395}, {470},
{192,245}, {332,338}.
```

These require another 20,351 retained-edge comparisons. Every dot equals a
claimed omission and every retained unit edge has differently coloured ends.
No solver result is used after these positive witnesses have been decoded.

The 963 rows reduce to a 538-set inclusion antichain, consisting of 496
singletons, 33 pairs, eight triples, and one four-set. The singletons force 367
large and 129 small vertices. Only the following 21 vertices remain optional:

```text
189,192,211,228,245,325,332,338,361,378,379,
432,434,505,510,511,512,513,514,515,516.
```

All 42 non-singleton minimal cuts lie within these 21 vertices.

## Independent completeness check

The submitted checker enumerates the `C(21,9)=293,930` nine-subsets. The
reviewer checker instead examines all `2^21=2,097,152` subsets of the optional
vertices and counts those containing no certified cut. The complete histogram
by subset size is

```text
size:   0   1    2    3     4     5     6    7   8   9..21
count:  1  21  177  773  1888  2596  1920  679  87     0
```

Thus the largest cut-avoiding omission set has size exactly eight. Every nine
optional omissions contain one of the 42 positive certificate cuts.

Suppose a non-four-colourable subgraph `K` had at most 508 vertices. All 496
singleton-forced vertices would have to lie in `K`, so at least nine of the 21
optional vertices would be absent. Those omissions contain a certified `D`;
the verified colouring of `G-D` restricts to `K`, a contradiction. Removing
edges only makes the same restriction a proper colouring, so non-induced
subgraphs are covered as well.

This direct argument does not import the preceding 39,453-case census or any
negative SAT answer. The discovery transcript explains how the eight rows were
found, but it is not a premise of the theorem.

## Reproduction

The checker uses CPython and its standard library only. From the repository
root:

```bash
export REVIEW_OUT=/scratch/fresh-h517-whole-decision-review1.json
python3 -B hadwiger_nelson_heule517_whole_decision_review1/independent_check.py \
  --repository . \
  --target hadwiger_nelson_heule517_whole_decision \
  --report "$REVIEW_OUT"
diff -u hadwiger_nelson_heule517_whole_decision_review1/result.json \
  "$REVIEW_OUT"
(cd hadwiger_nelson_heule517_whole_decision_review1 && \
  sha256sum -c SHA256SUMS)
```

Expected terminal fields include:

```json
{"all_checks_passed": true, "all_free_subsets_checked": 2097152,
 "fixed_support_closed": true, "free_vertices": 21,
 "maximum_cut_avoiding_omissions": 8, "positive_colourings": 963,
 "unit_edges": 2555}
```

Normal and optimized CPython runs produced byte-identical
[`result.json`](result.json). Controls reject a monochromatic unit edge, an
incorrect omission set, and an incomplete toy hypergraph cover. There are no
large reviewer artifacts, solver binaries, native libraries, or omitted proof
traces.

## Imported trust and uncertainty

Independently checked here are the exact 517-point construction, full unit-edge
set, all 963 positive colourings, omission decoding, inclusion antichain,
forced/free partition, complete `2^21` cover, and restriction argument.

The algebraic comparison assumes the displayed radical basis is independent;
this follows from the square-class independence of the primes 3, 5, and 11 but
is not proof-assistant formalized here. Remaining trust lies in the published
coordinate inputs, ordinary CPython integer and `Fraction` arithmetic, JSON
decoding, complete finite loops, and SHA-256 identities. The earlier family
theorems and the native SAT discovery are not logical premises of this review.

Reviewer: `reviewer-1`, 2026-09-06.
