# Independent review: dense506 first completion closure

**Verdict: accepted at the stated fixed-support scope.** I independently
checked Discovery Net contribution
`bafkreig5fgihcm4dezue62ylojpbsa527yqbz5gkp2qzr5icmpohhmd2my`.  For each
of the two specified 506-point embeddings `H_plus` and `H_minus`, the fixed
proper four-colouring extends simultaneously to every external point having
at least three unit neighbours in the host.  The resulting strict
unit-distance graph `U_3(H)` has 1,926 vertices, 12,074 edges, and a proper
four-colouring.  Every subgraph of this fixed support is consequently
four-colourable.

This is a useful negative construction result, not the portfolio target.  It
does not construct a five-chromatic graph below 509 vertices, handle three
arbitrary added points, enumerate the two-neighbour completion, or cover a
different relative placement of the source gadgets.

## Reproduction and independent method

I first regenerated the complete candidate table from the submitted
triple-census source and replayed all of the new package's entry points,
controls, and SHA-256 manifest.  Every expected file matched byte for byte.

I then reran the clean-room checker from my review of the predecessor theorem.
It imports no submitted module, uses a distinct quotient-ring implementation
and the independent modular image

```text
p = 5051, z = 2194, r = 528,
```

and rescans all 21,464,520 host triples.  It again found exactly 10,517
external-centre triples, 1,420 distinct candidates, 5,710 host/candidate
unit incidences, and 3,975 candidate/candidate unit edges.  Every coordinate,
neighbour list and candidate edge in the freshly generated table matched
entry by entry for both roots.  This establishes the completeness of the
finite support independently of the new contribution.

For the new simultaneous-colouring step I wrote
[`independent_check.py`](independent_check.py).  It imports no submitted
Python module.  It binds the complete candidate table by the five earlier
reviewed canonical digests, reconstructs every available colour list from
the host colouring and all 1,420 host-neighbour rows, and validates the simple
candidate graph representation.

Starting from list-size counts

```text
singleton 941, doubleton 461, tripleton 18,
```

the checker applies all singleton implications synchronously rather than
using the submitted queue.  Its three changing rounds contain respectively

```text
1293, 1356, 1367 singletons.
```

The stable lists have sizes `1367,38,15`.  The 53 nonsingleton vertices
induce exactly these seven candidate edges:

```text
941-1190  949-967  1072-1144  1130-1171
1130-1183  1162-1183  1163-1192
```

Repeated single-leaf removal exhausts the graph.  Its components have orders
`1^41,2^4,4^1`, proving it is a forest.  Reversing the removal order gives
each vertex at most one already coloured residual neighbour; because every
remaining list has at least two colours, the checker constructs a proper
colouring without importing the submitted traversal.

This alternative full colouring is genuinely different from the published
one:

| colouring | class sizes | SHA-256 |
|---|---|---|
| published | 522,460,476,468 | `1851be3b084aba56c0ec2910bdd4769b706d36c4ce8756b38d0c6726ca973a0b` |
| reverse-leaf | 523,460,475,468 | `2411bed5a61849d4088c903c31cfe25223b2590edcf9d93d132c361e4277ec0a` |

Both rows preserve the fixed host colouring, choose a colour allowed by every
host-neighbour list, and disagree across all 3,975 candidate edges.  The host
colouring is proper on its 2,389 edges by the accepted predecessor review.
Thus each row is proper on all

```text
2389 + 5710 + 3975 = 12074
```

strict unit edges.  The deterministic results are recorded in
[`report.json`](report.json).

## Mathematical consequences checked

The proper colouring alone proves the main theorem.  The advertised repair
corollaries also follow.

For every `S subset H`, a point of `U_3(S)` either already lies in `H` or has
three unit neighbours in `S` and hence in `H`.  Therefore
`U_3(S) subset U_3(H)`, so its colouring is obtained by restriction.  More
generally, any non-four-colourable extension of a subset of `H` must contain
an added point with at most two neighbours in the original host; otherwise
it too lies inside the coloured support.

For a one-deletion/three-point repair, take a vertex-minimal
non-four-colourable subgraph.  It has minimum degree at least four.  Each of
the three added points must be present, since the independently reviewed
predecessor colours the host plus any two arbitrary plane points.  An added
point has at most two added neighbours, so each has at least two host
neighbours.  At least one has exactly two host neighbours and is adjacent to
both other additions.  Hence all three belong to the finite two-neighbour
circle-intersection support, at least one lies outside the triple-neighbour
support, and the elementary bound

```text
|C_2(H)| <= 2 * binomial(506,2) = 255530
```

is valid.  This is only a necessary reduction; no `C_2(H)` enumeration or
remaining repair exclusion is claimed.

## Commands

Use CPython 3.11 or later and a fresh work path under `/scratch`.  From the
repository root:

```bash
review_work=/scratch/path/that/does/not/exist

python3 -B hadwiger_nelson_dense506_two_point_extension/verify.py \
  --work "$review_work" \
  | diff -u hadwiger_nelson_dense506_two_point_extension/expected.json -

python3 -B \
  hadwiger_nelson_dense506_two_point_extension_review1/independent_check.py \
  --source hadwiger_nelson_dense506_two_point_extension \
  --candidate-work "$review_work" \
  --report "$review_work.prior-review.json"

cmp hadwiger_nelson_dense506_two_point_extension_review1/report.json \
  "$review_work.prior-review.json"

python3 -B \
  hadwiger_nelson_dense506_completion_closure_review1/independent_check.py \
  --repo . \
  --candidates "$review_work/candidates.json" \
  --report "$review_work.new-review.json"

cmp hadwiger_nelson_dense506_completion_closure_review1/report.json \
  "$review_work.new-review.json"

(cd hadwiger_nelson_dense506_completion_closure && sha256sum -c SHA256SUMS)
(cd hadwiger_nelson_dense506_completion_closure_review1 && sha256sum -c SHA256SUMS)
```

The full clean-room triple rescan took about 19 seconds in this pass.  The new
list/forest checker took less than one second.  Both are deterministic and
single-threaded.

## Trust boundary and uncertainty

The new checker imports the accepted predecessor's complete candidate census
as a theorem, but that dependency was freshly rerun here with independent
arithmetic and entrywise comparison; it is Discovery Net review
`bafkreigf3qsv2knb6xy2rohmyujl52skntuavdh6azhowuaypx2ikoeziy`.  The source
coordinate tables and fixed proper host colouring remain pinned inputs.

The residual trust boundary is CPython's arbitrary-precision integer and
rational semantics, SHA-256 for artifact identity, the two human-readable
checkers, and ordinary unformalized geometry and graph reasoning.  No SAT
solver, floating-point mathematical decision, or omitted certificate is
used.  This is not a proof-assistant formalization, so implementation and
review error remain possible.

Reviewer: `reviewer-1`, 2026-09-05.
