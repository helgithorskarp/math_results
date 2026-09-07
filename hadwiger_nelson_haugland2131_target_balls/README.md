# All target-sized metric balls in Haugland's 2,131-vertex graph are four-colourable

Let G be the exact strict 2,131-vertex, 12,530-edge graph reconstructed from
Haugland's Appendix A, with the labels in the pinned sibling `graph.json`.
For a vertex v and an integer r >= 0, define

```
B_G(v,r) = {u in V(G) : graph distance in the full G from v to u is at most r}.
```

**Exact computer-assisted theorem.** If `|B_G(v,r)| <= 508`, then the induced
graph `G[B_G(v,r)]` is four-colourable. Every vertex- or edge-deleted subgraph
of every such ball is therefore four-colourable as well.

This exhausts a finite candidate-extraction family for the record target; it
finds no smaller five-chromatic graph. It does **not** classify arbitrary
508-vertex subsets of G, balls with more than 508 vertices, Euclidean discs,
or balls in an infinite Cayley graph. Distances are measured in the specified
finite host, not recomputed inside a candidate subgraph.

## Complete candidate census

For each of all 2,131 centres, take its largest admissible radius. The checker
computes full graph distances from every centre independently of the producer.

| Largest radius with ball order at most 508 | Centres |
|---|---:|
| 1 | 7 |
| 2 | 1,452 |
| 3 | 672 |

Including radius zero, there are **7,058** admissible centre-and-radius pairs,
and their vertex sets are all distinct. The 2,131 largest-radius balls are
also distinct. Under set containment they have **746 maximal members**, with
orders between **99 and 507**: 74 have radius two and 672 have radius three.

Every smaller-radius ball is contained in its centre's largest-radius ball.
The verifier checks that each of those 2,131 sets is contained in a certified
member. It also checks that the 746 certified sets form an antichain. Coverage
and the antichain check establish that the certificate contains exactly the
maximal members of the family, not a sample. The vertex limit comes from the
fixed record target; no radius or centre sampling cap is used.

## Compact positive certificates

The graph's exact edge list decomposes into two copies of its first
1,066-vertex induced subgraph Q. Both copies share vertex 0. The second-copy
label map is

```
f(0)=0,   f(v)=v+1065 for 1 <= v < 1066.
```

Each half has 6,264 edges. The only additional edges are
`(303,1368)` and `(435,1500)`, corresponding to the marked vertices 303 and 435
in the two copies. The verifier checks the complete edge-set equality; neither
cross edge is omitted.

`half_colourings.txt` supplies **sixteen distinct proper four-colourings of
all of Q**, each normalized to colour zero at vertex 0. These positive words
are checked directly on all half edges, giving 100,224 edge-colouring checks.
In particular, Q is four-colourable; the new proof does not need the paper's
endpoint-forcing UNSAT computation.

Each of the 746 recipes has seven integers:

```
[centre, radius, left_word, left_swap, right_word, right_swap, permutation]
```

A swap value of zero leaves the corresponding restricted word unchanged.
For a swap colour c in {1,2,3}, take the components induced by colours {0,c}
in the half's selected vertices. Interchange 0 and c on every such component
that does not contain the shared vertex 0. Apply the indicated permutation
of the four colour names to the right half, then join the words. Permutations
are numbered by lexicographic order of the 24 permutations of (0,1,2,3).

Interchanging two colours on whole bichromatic components preserves
properness. When the common vertex is selected, its two colour assignments
must agree. These observations explain the search, but the verifier additionally
checks the reconstructed colouring against **every induced edge in every
certified ball**, including both cross edges when present. This totals
**1,192,772 edge incidences**. It checks all selected vertices receive a
colour from {0,1,2,3}. The proof therefore does not depend on the search
heuristic or a claimed completeness of Kempe switching.

## Reproduce

Python 3.11 or later and the standard library suffice. Keep the pinned sibling
source input at its published relative path. From this directory:

```sh
python3 -B verify.py
python3 -B controls.py
sha256sum -c SHA256SUMS
```

The verifier output matches `expected.json`. The recipe certificate is
**13,867 bytes**, SHA-256

```
36e112636ad74fc21b0e32e0f06b7e1561d67304a0d3128154b56ebbc833d15e
```

The sixteen half words occupy 17,072 bytes, SHA-256

```
dad9913f90d489f110f713a209da3f6632c309a9f4c155ae33b5fe44bd54d3be
```

Regenerate the recipes and, optionally, the positive half words:

```sh
python3 -B generate.py --out /tmp/haugland-target-balls
cmp certificate.json /tmp/haugland-target-balls/certificate.json
python3 -B discover_words.py --out /tmp/haugland-target-words
cmp half_colourings.txt /tmp/haugland-target-words/half_colourings.txt
```

Word discovery uses the pinned standard-library cyclotomic arithmetic in the
[strict-edge package](../hadwiger_nelson_haugland2131_strict_edges/README.md).
It reconstructs Q, labels each edge by one of 42 antipodal direction classes,
and imposes the cycle-parity relations on direction labels in F2. A spanning
tree gives 42 binary direction variables with relation rank 30. Two linear
functionals on the resulting 12-dimensional binary space assign two colour
bits, and every direction is required to receive a nonzero pair. The search
finds 42 direction-invariant words modulo permutations fixing colour zero;
it retains the sixteen used by the ball certificate. No assertion that these
are all proper four-colourings of Q is made or needed. The verifier imports
neither the discovery code nor its arithmetic.

Recipe generation took about three seconds in the recorded CPython 3.11.2
run. It uses truncated breadth-first layers, descending-size containment
pruning, and searches the supplied words and swaps. The independent verifier
runs full breadth-first searches, proves coverage and maximality directly,
and decodes swaps by enumerating all bichromatic components. It imports no
producer code and checks all final colour inequalities. Normal and optimized
Python runs agree byte for byte for word discovery, recipe generation,
verification and controls.

Controls compare the producer's ball extraction against Floyd-Warshall
exhaustively on all 1,099 labelled simple graphs of orders one through five,
for every applicable vertex limit: 5,405 graph-and-limit cases, including
disconnected graphs. Thirteen malformed inputs are rejected across word,
edge-decomposition, radius, coverage, palette and gluing checks. These are
author-run controls, not external peer review or proof-assistant formalization.

## Exact geometry, prior work and limitations

The [independent strict-edge census](../hadwiger_nelson_haugland2131_strict_edges/README.md)
establishes the host's exact coordinates and all 12,530 unit edges. Its graph
edge stream `u v\n` has SHA-256

```
980bdb02e133be0e4257bab1a204f2942f554e59822136fab632f45494a6c113
```

The coordinate construction uses Q(zeta_84,sqrt(5)); the original path
transcription and edge list are in the
[reconstruction package](../hadwiger_nelson_haugland2131_exact_reproduction/README.md).
The new checker pins the complete input bytes and this edge hash. Unit-distance
realizability and strict-edge completeness are inherited from that exact
geometry theorem, whose standard-library checker was replayed during this
pass. To replay it from the repository root:

```sh
python3 -B hadwiger_nelson_haugland2131_strict_edges/independent_check.py \
  hadwiger_nelson_haugland2131_exact_reproduction/graph.json \
  hadwiger_nelson_haugland2131_strict_edges/certificate.json
```

[Haugland's paper](https://arxiv.org/html/2608.04542v4) supplies the construction
and its reported five-chromatic lower bound. The earlier independent repository
reproduction left that lower-bound SAT proof pending. This positive ball-family
exclusion neither relies on nor completes it. No new record, general lower
bound for the plane, or novelty of graph-ball extraction is claimed.

The broader question whether **every** subgraph of G through order 508 is
four-colourable remains open in this pass. Preliminary one-hot, binary and
phase-seeded SAT probes on much larger halves or one-vertex deletions were all
UNKNOWN within their declared conflict budgets. They supplied no negative
certificate. Exact direction-based colourings were then used for the complete
ball-family gate. Failure of the preliminary simultaneous-separation procedure
is not asserted to exclude any graph.

The completed Parts/H632 maps, Parts planar-realization classification, E477
attachments and the teammate's
[mixed Moser/L10 sum support](../hadwiger_nelson_mixed_moser_l10_sums/README.md)
were not resumed. The present finite ball family is now closed. Further work
must use supports not covered by these balls or a different mechanism; this
certificate does not authorize a radius, budget or cap-extension ladder.
