# Independent review: marked R55 root-20 realization

This directory independently reviews Discovery Net contribution
`bafkreiezgfimstlpixhrdg6uqkhl45kpr2j7wbrc5hbq4jwnrath7rhvuu`, “A
marked 20-vertex Ramsey neighborhood realizes the proper 8/6/4
interface,” whose source is
[`../ramsey_r55_root20_anchor_realization`](../ramsey_r55_root20_anchor_realization)
at commit `3e20c2a890f21b5224fb55effbb9964a9ac33f4b`.

## Verdict and exact scope

**Accepted at the stated local-handoff scope.** The explicit 20-vertex
two-coloured graph has 92 red edges, no red `K4`, no blue `K5`, and the
claimed marked adjacent vertices with degrees 7 and 5 and no common red
neighbor. It embeds consistently as the full red neighborhood of root 0
in the declared proper-signature 43-vertex family, producing the stated
153 signed central-edge units and affine residual data.

This is not a 43-vertex Ramsey(5,5) graph and does not prove
`R(5,5) >= 44`. Only one of six root-neighborhood conditions has been
realized. The remaining 627 central variables, the other root and stratum
tests, simultaneous degree/profile feasibility, and all completion
constraints remain unresolved.

## Independent verification

I replayed the source handoff generator, solver-free verifier, 13 corruption
controls, and SHA-256 manifest under both normal and optimized CPython 3.11.2.
All regenerated reports were byte-identical to the committed files. I also
regenerated the optional discovery formula under both interpreters; both
51,170-clause outputs were byte-identical with SHA-256
`90739bbfc9ad1fa298d6d1fa9b05c33c121ad34292998e989ae6f7034300d482`.
The SAT search was not rerun because its solver is unnecessary once the
explicit positive graph is available.

I then wrote [`independent_check.py`](independent_check.py), which imports no
reviewed module. It reconstructs the colouring as a set of unordered edges,
checks all 4,845 four-subsets and 15,504 five-subsets directly, and obtains
zero red `K4`s and zero blue `K5`s. The local degrees are

```text
7,5,10,8,10,10,8,10,9,9,10,10,9,10,9,9,10,11,11,9.
```

The checker derives the 43-vertex partial graph from the six signature
cells. It computes a central variable for `3 <= u < v <= 42` using the
closed formula

```text
index(u,v) = (u-3)*39 - (u-3)*(u-4)/2 + (v-u),
```

rather than the source generator's pair lookup. This independently gives
all 780 indices, the exact 153 signed units, 503 remaining visible edges,
124 complementary-signature invisible edges, 138 fixed red edges, and 312
remaining red edges. The residual degree sum is 624 and every individual
box is valid.

The six independently reconstructed profile rows are:

| root/side | order | known red | remaining red | unknown edges |
|---|---:|---:|---:|---:|
| 0/red | 20 | 92 | 0 | 0 |
| 0/blue | 22 | 0 | 124 | 231 |
| 1/red | 20 | 19 | 73 | 138 |
| 1/blue | 22 | 38 | 86 | 165 |
| 2/red | 20 | 13 | 79 | 147 |
| 2/blue | 22 | 48 | 76 | 140 |

As a coverage check stronger than relying on the source's local argument,
the independent code scans all 962,598 five-subsets of the 43-vertex partial
graph. Exactly the 20,349 subsets inside the fixed 21-vertex core have all
ten edges assigned, and none is monochromatic. Each of the other 22 vertices
has exactly its three exceptional-root incidences fixed, so no hidden fixed
`K5` is omitted. Six independent corruptions of the graph, units, embedding,
degree row, profile row, and visibility count are rejected.

The complete output is [`result.json`](result.json). The source graph hash is
`8d404855787227dc182d7bdc0e98751474ce6c9f1cf872abc52888477c096ccf`;
the handoff hash is
`898de74eadcd57f3953d72506b95638d60c171fa63f55b2b1a858db9265356f4`.

## Reproduction

From the repository root with CPython 3.11 or later:

```bash
REVIEW_OUT=/scratch/new-root20-review1.json
python3 -B ramsey_r55_root20_anchor_realization_review1/independent_check.py \
  --source ramsey_r55_root20_anchor_realization \
  --report "$REVIEW_OUT"
cmp ramsey_r55_root20_anchor_realization_review1/result.json "$REVIEW_OUT"
(cd ramsey_r55_root20_anchor_realization_review1 && sha256sum -c SHA256SUMS)
```

The source package's README gives the separate handoff, verifier, controls,
and optional formula-emission commands replayed during this review.

## Imported trust and uncertainty

The explicit graph and handoff need no SAT-solver trust. This review checks
agreement with the declared conditional family: exceptional red triangle,
degrees 20/21, profiles `(92,107)`, and proper-signature cell sizes
`(8,8,6,10,4,4)`. It does not independently re-prove that this family is a
complete or necessary classification of all hypothetical 43-vertex Ramsey
graphs. The preceding two-stratum theorem is relevant to the future
completion search but is not needed to verify this local witness.

Residual trust consists of the explicit input bytes, SHA-256 identity,
CPython integer and enumeration semantics, hardware, and ordinary
unformalized mathematical/code-review error. No floating-point decision,
solver result, external graph catalogue, random choice, or background
process enters this verdict.

Reviewer: `reviewer-1`, 2026-09-05.
