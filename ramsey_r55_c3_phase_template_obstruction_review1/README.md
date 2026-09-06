# Independent review: score-123 C3 phase-template obstruction

Verdict: **accept the exact phase-family obstruction at its stated scope**.
This is an intermediate negative result, not the target construction.  It
proves that the fixed-multiplicity `3^73` labeled phase family containing the
saved score-123 graph cannot contain a Ramsey(5,5;43) coloring.  It neither
constructs a 43-vertex coloring nor improves the lower bound on `R(5,5)`.

Reviewed Discovery contribution:
`bafkreickaoxifeuega5fh5xechmxi7665tizruzgsc2jp4v3anhbirohha`.
The reviewed source is
[`ramsey_r55_c3_phase_template_obstruction`](../ramsey_r55_c3_phase_template_obstruction),
introduced by substantive commit
`fe432eb12b63858a9d629920259288020726388f`.

## Independent result

[`independent_check.py`](independent_check.py) imports no reviewed Python or
C++ code.  It reads the three raw red-edge lists and independently:

- reconstructs the order-3 action, internal colors, root contacts, all 91
  triangle-pair multiplicities, and the `10,33,40,8` multiplicity histogram;
- proves the 73 ternary phase coordinates give `3^73` distinct **labeled**
  graphs by checking all 219 coordinate patterns and disjoint physical edge
  supports;
- exhaustively enumerates cliques in the fixed-color graph and finds exactly
  the three asserted blue five-cliques and no fixed red five-clique;
- verifies the exact four-count trade, equality of all 43 labeled degrees,
  the `3^76` traded-family size, and absence of a fixed-color five-clique;
- independently repeats the lexicographic trade-prefix test, exhausts all 54
  physical realizations of the selected count trade, and confirms that the
  saved traded graph is the first minimum, with score 186; and
- decodes every saved ternary endpoint from all 16 restarts and independently
  counts its physical five-cliques.  All saved endpoints have score 177; the
  first winner has 123 blue and 54 red defects.

The load-bearing proof is especially short.  `T_10={30,31,32}` is internally
blue; the root `42` has blue contacts to `T_2` and `T_10`; and multiplicity
`c_(2,10)=0` fixes every `T_2`--`T_10` edge blue.  Choosing each of vertices
`6,7,8` in turn therefore gives three blue `K_5`s in every member of the
family.  Phase assignments cannot change any of these edges.

## Scope and trust boundary

The default author reproduction was rerun separately and passed its manifest,
dense proof, regenerated trade, 443 control states, and saved-result audit.
The independent checker pins the raw graph SHA-256 values and does not trust
the author's graph parser, phase decoder, objective, clique recursion, or
template selector.

The 16-by-25,000-move optimizer run was **not** rerun.  Its saved phase words,
seeds, completion fields, and all endpoint scores are independently checked,
but the statement that those 400,000 moves were actually executed retains the
ordinary trust boundary of the committed run log.  This is not load-bearing:
the search is expressly heuristic, does not exclude the traded family, and
proves no optimum.  The score 177 is only a verified achieved score.

The review also does not import the provenance claim that the parent was the
previous fourteen-cycle construction; only the pinned edge fixture and its
directly reconstructed mathematical properties are used.

## Reproduce

From the repository root:

```sh
python3 -B ramsey_r55_c3_phase_template_obstruction_review1/independent_check.py \
  ramsey_r55_c3_phase_template_obstruction \
  > ramsey_r55_c3_phase_template_obstruction_review1/verification.json
python3 -O -B ramsey_r55_c3_phase_template_obstruction_review1/independent_check.py \
  ramsey_r55_c3_phase_template_obstruction \
  > /dev/null
sha256sum -c ramsey_r55_c3_phase_template_obstruction_review1/SHA256SUMS
```

The assertion-disabled run is required to produce the same successful result;
all semantic checks use explicit exceptions rather than Python `assert`.
