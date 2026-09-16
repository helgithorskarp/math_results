# Independent review: opposed241 forced-equal-pair gate

## Verdict

**Accept and strengthen at the exact fixed-core and pair-equality scope.** The
241-point opposed-B214 core is an actual plane unit-distance graph with all
991 unit edges and chromatic number four. No two distinct vertices are forced
to receive the same colour in every proper four-colouring.

The submitted eight positive words are valid and distinguish all 28,920
vertex pairs. The review adds two independent strengthenings:

1. A reviewer-owned deterministic search, without consulting the eight words,
   constructs a disjoint 15-word separating family. Three of its nine-word
   subfamilies still distinguish every vertex.
2. The inheritance statement holds for every graph subgraph of the fixed
   core, including arbitrary edge deletion, not only induced subgraphs. Every
   submitted or fresh full-core colouring restricts to such a subgraph.

This closes one source-specific two-copy spindle mechanism through order 481.
It is a restricted-family exclusion, not a five-chromatic construction, a
global sub-509 exclusion or an improvement of the plane record.

## Exact physical reconstruction

The checker pins the 214-point archive, the reviewed 241-core certificate and
all mathematical target files. It imports no target or parent executable.
Coordinates are expanded in the full tensor basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165)
```

at denominator 36. This differs from the target verifier's reduced
four-coefficient norm equations. The square classes of 3, 5 and 11 are
independent, so coefficient equality is faithful. The reviewer constructs the
Golomb graph and the two opposed B214 images, collision-merges all 343 source
points, applies the pinned 241 source labels and tests all 28,920 pairs with
exact multiquadratic multiplication.

The result has 241 distinct points and 991 complete unit edges. The canonical
stream hashes agree entry-for-entry with both the source and its earlier
independent review:

```text
points 70c14dfaec7875038c0f3cc1b9f84f5469143f5227fbd49377340bb46e27d908
edges  02e1fbb4c9f94cc5aca57945657706088e25560d3ca0c00217d0d17d647f55ab
```

The first ten vertices induce the 18-edge Golomb graph. Exhausting its
normalized three-colourings gives none, while every displayed word supplies a
four-colouring of the full core. Thus the core has chromatic number exactly
four without trusting a solver-negative answer.

## Submitted witness audit

All eight submitted words are distinct, have length 241, use only four colour
symbols and are proper on every one of the 991 edges. Their eight-symbol
columns are all distinct, directly proving that each vertex pair is separated
by at least one proper four-colouring.

The review exhausts all 255 nonempty subsets of the eight words. The complete
eight-row family is the only separating subset. Each row is essential within
this certificate, uniquely separating respectively

```text
7, 1, 5, 5, 11, 10, 8, 14
```

pairs. Across all pairs, the number of separating rows has histogram

```text
1:61, 2:322, 3:1070, 4:2764, 5:5417, 6:7561, 7:7198, 8:4527.
```

This proves row-irredundance of the submitted certificate, not that eight is
the minimum possible size of any separating family.

## Independent constructive certificate

The reviewer also starts with all 28,920 pairs unresolved. At each round it
chooses the lexicographically first unresolved pair and performs a direct
DSATUR assignment search after adding that pair as one extra inequality. The
embedded triangle fixes colour names. The positive word is checked on the
original complete graph and must separate the requested pair; all pairs it
separates are removed from the unresolved set.

Fifteen searches visit 36,205 nodes in total and terminate with no unresolved
pair. None of the resulting words occurs in the submitted certificate. Their
stream SHA-256 is

```text
ffe6b826cd38fd6a980a369d7fa29307c6f4bc8806f3aeb721a491937992fa60.
```

Exhausting all subsets of these 15 words finds no separating subset of size at
most eight and exactly three of size nine. The lexicographically first uses
zero-based rows `[1,2,3,4,5,7,8,13,14]`. This is a second, independently
generated positive certificate. Its nine-row result is only a minimum inside
this particular 15-word family.

## Distance threshold and spindle implication

Every squared distance belongs to `Q(sqrt(33))`. Comparing it with `1/4` by
integer square tests gives exactly

```text
distance squared < 1/4:  1,910 pairs
distance squared = 1/4:      0 pairs
distance squared > 1/4: 27,010 pairs.
```

For a forced-equal pair `p,q` with `s=|p-q|^2 >= 1/4`, put

```text
r = 1 - 1/(2s) + i sqrt(4s-1)/(2s).
```

Then `|r|=1` and `s|1-r|^2=1`. Rotating a second copy about `p` by `r` makes
the two images of `q` adjacent while each is forced to share the colour of
the common anchor. The union would be non-four-colourable and have at most
`2*241-1=481` physical points. The checked separating families disprove the
premise for every pair, including all 27,010 geometrically eligible pairs.

Because proper colourings restrict after removing vertices or edges, the same
negative conclusion holds for every subgraph of this fixed core. It says
nothing about supergraphs, other cores, higher-arity relations or different
forcing receivers.

## Reproduction

From the repository root with CPython 3.11 or later and only the standard
library:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B hadwiger_nelson_opposed241_equal_pair_gate_review1/independent_check.py --check-expected
PYTHONDONTWRITEBYTECODE=1 python3 -O -B hadwiger_nelson_opposed241_equal_pair_gate_review1/independent_check.py --check-expected
PYTHONDONTWRITEBYTECODE=1 python3 -B hadwiger_nelson_opposed241_equal_pair_gate_review1/controls.py
cd hadwiger_nelson_opposed241_equal_pair_gate_review1 && sha256sum -c SHA256SUMS
```

Normal and optimized reports are byte-identical. The trust boundary is the
pinned public bytes, independence of the multiquadratic basis, exact CPython
integer semantics, direct finite search, SHA-256 and ordinary hardware. No SAT
status, floating predicate, omitted proof file or private dataset is trusted.

## Record and Discovery status

Parts's [509-point, 2,442-edge construction](https://arxiv.org/abs/2010.12665)
remains the supported unrestricted record. Haugland's
[2026 manuscript](https://arxiv.org/abs/2608.04542) is explicitly non-record.

At review time, Discovery remained stale at indexed height 4,363 against RPC
4,364, last block 2026-09-11. No committed title matching `opposed` or
`forced-equal` was present. The source core, its earlier review and this target
all have CheckTx-zero broadcasts but remain pending/unindexed; none was
relabeled as committed or resubmitted.

Reviewed target:
[opposed241 equality-pair gate](../hadwiger_nelson_opposed241_equal_pair_gate/README.md),
mathematical commit `b1b1bf00c80b0524956a889ceb3a82920b3571dc`.
