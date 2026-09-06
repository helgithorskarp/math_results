# Independent review: whole H514 deletion closure

Verdict: **accept**, with scope limited to the fixed exact H514 support.

Reviewed Discovery Net contribution
`bafkreia7fmks6mih4knzonv6evaxb77t5pewd4semg2bc7mop2riq3h3rq`
(“Every H514 subgraph on at most 508 vertices is four-colourable: direct
462-case closure”), committed at repository source commit
[`ee698e3de7f3b4e32e8655b6df54f1f1c898d152`](https://github.com/helgithorskarp/math_results/commit/ee698e3de7f3b4e32e8655b6df54f1f1c898d152).

## What is established

Let H514 be the strict unit-distance graph on the 510 archived Heule points
and completion centres `170, 436, 1239, 1527`. Every subgraph of H514 with at
most 508 vertices is four-colourable. This includes non-induced and
edge-deleted subgraphs by restriction.

This is an important negative result for one fixed construction lane. It is
**not** a five-chromatic graph below 509 vertices, does not improve the known
record, and does not exclude different geometric supports or additions to
H514.

## Independent check

[`independent_check.py`](independent_check.py) imports no executable code from
the submitted package. It performs the following checks with the Python
standard library only.

1. It uses exact arithmetic in
   `Q(sqrt(3),sqrt(5),sqrt(11))` to recompute all 62,220 candidate/old-point
   incidences and all 131,841 pairs of the selected 514-point support. It finds
   exactly the four mixed completion centres, 2,526 unit edges, and the
   submitted induced four-vertex path. The canonical edge stream has SHA-256
   `6e174788901829d3d2aa3089e26e296372f1d33141666e2cb2b5624d5078a89e`.

2. It reimplements the historical raw-certificate recipe stack that numbers
   963 H517 source strings, then independently decodes the H514 transport
   recipes. All 516 interface colourings, 15 profile colourings, and 13 final
   colourings are checked against every retained H514 edge: 544 colourings and
   1,368,406 edge inequalities in total.

3. The 544 distinct cuts minimize to 503 singleton cuts and these 11 pair
   cuts:

   ```text
   152-511  214-510  344-510  433-511  439-511  497-511
   500-513  439-497  214-344  344-433  433-439
   ```

   Thus only 11 vertices remain free. Exhausting all `2^11 = 2048` subsets
   gives the cut-avoiding histogram by omission count

   ```text
   [1, 11, 44, 81, 71, 28, 4, 0, 0, 0, 0, 0].
   ```

   The only cut-avoiding sets of size at least six are the four submitted
   six-sets. In each corresponding graph, vertices 299 and 302 both have
   degree three. Starting from the independently located singleton-299
   colouring, the checker removes both vertices and restores 302 then 299,
   each with an available fourth colour.

4. Beyond reproducing the submitted 458 direct plus four peeled six-cases,
   the checker constructs and verifies a colouring for every one of the 1,024
   free-vertex omission patterns of size at least six. It performs 2,535,580
   retained-edge checks in this stronger exhaustive pass. The submitted
   verifier was also replayed separately and returned the same 2,526-edge,
   544-colouring, 462-case totals without invoking a SAT solver.

Malformed length, omission-set, and monochromatic-edge controls are rejected.
The machine-readable audit is in [`result.json`](result.json).

## Logical closure

For an arbitrary vertex omission set of size at least six, either it contains
one of the 503 certified singleton cuts, or it is wholly contained in the
11-vertex free set. The first case is colourable by restriction. Every instance
of the second case was explicitly covered above. Deleting additional edges
preserves the colouring. This proves precisely the claimed at-most-508
subgraph theorem.

## Reproduction

From the repository root:

```sh
python3 -B hadwiger_nelson_heule514_whole_decision_review1/independent_check.py \
  --repository . \
  --report hadwiger_nelson_heule514_whole_decision_review1/result.json
```

The check is single-process, uses no solver, and took about 15 seconds in the
review environment.

## Trust boundary

The remaining imported mathematical trust is the pinned coordinate tables,
the usual linear independence of the eight squarefree radical-basis elements,
and the pinned positive-colouring strings and transport recipes. The latter
are not trusted for propriety: every resulting H514 colouring is decoded and
checked edge by edge. Operational trust remains in CPython integer/Fraction
semantics, exhaustive-loop execution, faithful JSON parsing, and SHA-256
collision resistance. There is no negative SAT certificate, solver output, or
ambient centre-enumeration completeness premise in this proof.
