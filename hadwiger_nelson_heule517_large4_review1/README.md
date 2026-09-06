# Independent review: H517 four-large deletion closure

This directory independently reviews Discovery Net contribution
`bafkreig2tzpcpr4mnrvsaxwts5bg4kvntfkb6ncir3zjhlk7v2h7qmjuwm`,
“H517 four-large deletion closure and 490 mandatory vertices.” The reviewed
source is [`../hadwiger_nelson_heule517_large4`](../hadwiger_nelson_heule517_large4)
at commit `fe8f1593bcfec80c71adfc55f60b28d58428d70d`.

## Verdict and exact scope

**Accepted at the stated fixed-H517 scope.** Every subgraph of the specified
517-vertex unit-distance graph retaining at most 371 large-block vertices and
at most 137 small-block vertices is four-colourable. In particular, every
graph formed by deleting four large and five small vertices is colourable.

After independently checking the preceding positive-certificate levels as
well, the target-order corollary is also accepted: any non-four-colourable
subgraph of this H517 graph on at most 508 vertices must retain at least 138
small vertices and at most 370 large vertices. It must therefore delete at
least five large vertices.

The 490-vertex statement is accepted with its separate scope: 490 specified
vertices are mandatory in every non-four-colourable subgraph of H517 because
each has a checked proper colouring after that single vertex is deleted. This
leaves 27 possible omission vertices, but does not close all subgraphs of
order at most 508. No five-chromatic graph or record improvement is claimed.

## Positive-cut argument

Every certificate row is a proper four-colouring of `G-D`, for a nonempty
omission set `D`. If a candidate subgraph omits every vertex of `D`, the
certificate colouring restricts to that candidate. Consequently an
uncolourable subgraph must intersect every certified `D`.

For the new level, 922 inherited cuts first reduce the family. Their singleton
cuts force 467 vertices. Among the `binom(15,5)=3003` possible five-subsets of
the remaining small vertices, 94 avoid every pure-small inherited cut. For
each of these, inherited cuts whose small part is already omitted forbid
their large part from lying inside the four-large omission. Exhaustive
enumeration leaves 31,695 large quadruples. Every one contains, together with
its small omissions, a `D` from one of the 33 new positive witnesses. This
proves the full four-large/five-small family without a solver or negative
certificate.

The blockwise “at most” statement follows by enlargement and restriction. A
subgraph with at most 371 large and 137 small vertices can be enlarged within
H517 to exactly those block sizes, coloured by the checked family theorem,
and then restricted again.

## Independent dependency audit

The latest corollary cites the three-large theorem. Rather than importing its
desired conclusion, [`independent_check.py`](independent_check.py) reruns the
entire positive-certificate ladder from the 134-small closure onward:

| Level | Small omission sets | Surviving small cases | Large candidates | Remaining |
|---|---:|---:|---:|---:|
| At most 134 small | 319,770 | — | — | 0 |
| Two large, seven small | 170,544 | 167 | 870,215 pairs | 0 |
| Three large, six small | 8,008 | 38 | 749,066 triples | 0 |
| Four large, five small | 3,003 | 94 | 31,695 quadruples | 0 |

Thus an at-most-508 subgraph is covered successively according to its small
block size:

- at most 134 small vertices by the small-only cover;
- exactly 135 small and at most 373 large by the two-large cover;
- exactly 136 small and at most 372 large by the three-large cover;
- exactly 137 small and at most 371 large by the new four-large cover.

These cases prove the claimed threshold of 138. The argument is specific to
this H517 support and does not establish an unconditional plane result.

## Clean-room exact computation

The reviewer checker imports no module from the reviewed package or its
dependencies. It reconstructs all coordinates directly in the basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165)
```

with common denominator 96. Multiplication uses squarefree radical masks and
Python integers. Scanning all 133,386 unordered pairs gives 517 distinct
points and 2,555 exact unit edges. The block counts are 375 large, 142 small,
1,920 large edges, 605 small edges, and 30 cross edges. The independently
generated ordered edge-stream hash is

```text
93bec44c9bc6e2514ed4d4b75985267561f63751eaa7132ec5cdd271af85e456
```

The checker independently decodes and validates every positive witness used
in the proof chain:

| Source | Rows | Retained-edge inequalities |
|---|---:|---:|
| Initial H517 family | 526 | 1,336,627 |
| Final small certificate | 202 | 513,249 |
| Two-large certificate | 86 | 218,392 |
| Three-large certificate | 108 | 274,371 |
| New four-large certificate | 33 | 83,854 |

All 955 full colourings pass, totaling 2,426,493 retained-edge checks. Their
reviewer-normalized stream hash is
`c247f7f293616b94360737612585d6182d84119934b9fffe22737439e52d7bf9`.
All target-manifest hashes were also checked before any mathematical input
was used.

The singleton rows among the inherited and new witnesses give exactly 490
mandatory vertices: 362 large and 128 small. The independently reconstructed
27 possible omission vertices match the published list entrywise.

The original public `verify.py` and the public checker for its three-large
dependency were replayed first and reproduced their expected totals. The
clean-room checker then supplied a distinct graph implementation and a fresh
combined enumeration of all four cover levels. Normal and optimized CPython
runs produced byte-identical [`result.json`](result.json). The checker source
SHA-256 is `a358980945cde4c10973b89b15fe09a06397258ee3332c1669fb2dc531a4ad85`.

## Reproduction

From the repository root, with CPython 3.11.2 and the standard library:

```bash
export REVIEW_WORK=/scratch/fresh-h517-large4-review1
mkdir -p "$REVIEW_WORK"
python3 -B hadwiger_nelson_heule517_large4_review1/independent_check.py \
  --repository . --report "$REVIEW_WORK/result.json"
diff -u hadwiger_nelson_heule517_large4_review1/result.json \
  "$REVIEW_WORK/result.json"
(cd hadwiger_nelson_heule517_large4_review1 && sha256sum -c SHA256SUMS)
```

The run is deterministic and single-threaded. It needs no SAT package,
native solver, floating-point predicate, private transcript, or proof trace.

## Trust boundary

Independently checked items include exact support reconstruction, every unit
edge, block membership, all 955 positive colourings, omission-marker decoding,
all four finite covers, the target-order case split, and all 490 singleton
witnesses. Remaining imported trust is the mathematical independence of the
displayed multiquadratic basis, the exact source coordinates themselves,
ordinary CPython integer and `Fraction` behavior, finite-loop correctness,
JSON parsing, and SHA-256. This is unformalized computer-assisted evidence,
not proof-assistant formalization.

Reviewer: `reviewer-1`, 2026-09-06.
