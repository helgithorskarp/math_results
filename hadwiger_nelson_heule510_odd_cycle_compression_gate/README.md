# Heule510 has no degree-four odd cycle to compress

The complete strict unit graph on the fixed Heule510 coordinates has exactly
eight degree-four vertices, and they form an independent set. Consequently
the proposed replacement of a degree-four odd-cycle component by a unit
triangle has no input component in this source. The construction stops before
any new points or colouring queries are generated.

This is a small, exact source-selection stop. It supplies no capped physical
graph, new chromatic obstruction, global lower bound, or record improvement.
The data are not claimed to be previously unknown.

## Why this component would have carried the obstruction

The proposed surgery concerned one induced cycle C whose vertices all have
degree four in a five-chromatic physical parent G. Keep H=G-C fixed. Every
vertex of C then has two neighbours in H. For any proper four-colouring of H,
its available colour list at that vertex has size at least two.

A cycle with lists of size at least two is not list-colourable precisely when
it is odd and all lists are the same two-element set. Here is the elementary
argument. If adjacent lists differ, orient the cyclic order so that a colour
of the first list is absent from the last list. Use that colour first and
colour the remaining vertices greedily along the path. The final vertex
automatically differs from the first. If all lists agree, an even cycle uses
two colours, any cycle uses three, and an odd cycle cannot use only two.

Thus every proper four-colouring of H would give the same two available
colours at all cycle vertices. A physical unit triangle, each of whose
vertices was constrained by retained neighbours to these same lists for
**every** host colouring, would reproduce the obstruction. Existence of such
points is an additional geometric obligation, not a conclusion of the list
lemma. Exact complete edges, a proper five-colouring and ordinary non-four
evidence would still be required on the resulting whole support.

For the selected 510-point parent, deleting a cycle of odd length k>=5 and
adding three points would cost at most 510-k+3<=508 points. This accounting is
conditional only. The required cycle does not exist, so no physical triangle
placement, list-relation census, or capped composition was attempted.

## Exact source and result

The input is `aligned_H` in the sibling
[`aligned_510.json`](../hadwiger_nelson_parts509_heule_union_minimum/aligned_510.json).
Labels below are its zero-based row numbers. That file was introduced at
commit `d7340f5ba7f7b7e03b14b586364ef545df414e96`; its byte hash is

```text
84456269b4acb9fa911164f7148eb227e5f30835f03d8cb5d46d6f9602fd8e5b
```

Coordinates use the rational basis
`1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165`, with the positive radicals.
The checker verifies an exact common scale of 288, coefficientwise distinctness
of all 510 points, and all 129,795 unordered distances. It reconstructs 2,504
unit edges. The degree-four labels are exactly

```text
139,144,316,319,322,325,328,331
```

Their eight components are singletons. Their neighbour lists and the full
degree histogram are in [expected.json](expected.json). The ordered complete
edge-list hash, in the serialization specified by the checker, is

```text
4976a7b233b74690bd04068762d29f195f0868a5a72cc5439033df2b3484b493
```

## Reproduction and boundary

From a full repository checkout, with Python 3.11 or newer:

```sh
python3 -B hadwiger_nelson_heule510_odd_cycle_compression_gate/verify.py
```

The final status is `NO_DEGREE_FOUR_ODD_CYCLE_IN_FIXED_HEULE510`.
Every distance is compared in two exact arithmetic representations: dense
subset-mask multiplication and sparse squarefree-radicand multiplication using
gcd reduction. The new checker also agrees entrywise on the full edge list
with the initial selector using the existing catalogue arithmetic. These are
author checks, not independent peer review. No SAT solver, floating-point
comparison, assertion-dependent check, or large external proof is needed.

The source's known five-chromaticity motivates the construction but is not a
premise of this degree calculation; its proof was not replayed here. The list
lemma is standard elementary mathematics, not a novelty claim. Prior Parts509
degree-four signature work already concerns a different independent set of
six low-degree vertices; this pass neither reclassifies those relations nor
extends that programme.

Retire this fixed source for the declared cycle compression. This result does
not exclude other surgeries on Heule510, edge-deleted parents, higher-degree
components, or different parents. Those are not follow-up branches of this
gate. It also does not reopen the separate H510 smaller-image programme.

For record context, [Parts's paper](https://arxiv.org/abs/2010.12665) gives 509
vertices and 2,442 edges, and [Haugland v4](https://arxiv.org/html/2608.04542v4)
still names 509 as current; both were checked on 2026-09-15.
