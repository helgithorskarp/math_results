# Compact K4 expansion interface for every ordered good43 task

Every prescribed monochromatic four-clique in the complete h3887 packing
family must touch at least 19 of its 39 outside vertices in its own color.
This is an unconditional consequence of the h3897 separator-through-18
classification: its outside same-color neighborhood is a separator whenever
it has size at most 18, and it would leave the four-clique and at least 21
other vertices on opposite sides.

For one fixed four-clique, the rule is the conjunction of
`binom(39,21) = 62,359,143,990` minimal physical cut clauses, each of width
84. This package gives an exactly equivalent definitional encoding with
648 auxiliary variables and 2,572 clauses per block, of maximum width five.
It therefore adds 4,536--6,480 variables and 18,004--25,720 clauses to the
q=7--10 ordered tasks. The interface covers every one of h3887's 2,189,178
tasks without changing task identifiers, block order, core labels, physical
edge variables, or physical model sets.

The added counter is propagation-complete at its natural boundary. If a
partial assignment makes 21 outside vertices anticomplete to a block in the
block's color, unit propagation finds a conflict. If it makes exactly 20
vertices anticomplete, unit propagation requires every remaining outside
vertex to have at least one block-color contact. This is a concrete new
decision mechanism rather than another carrier count or raw solver call.

The smallest ordered triangle formula `bo1-q7-r7-c000000` was freshly
generated and independently read literal by literal. It has 10,868 variables,
923,269 clauses, maximum width eight, 35,503,067 bytes, and SHA-256
`755dbcd5677bbc57a0865637dbce19fa72084c4846b3996b8697bf1485070178`.
The bulk CNF is omitted. No SAT solver was run, no task was decided, and no
good43 or Ramsey-number improvement is claimed.

## Reproduction

CPython 3.11.2 and its standard library suffice for the compact replay:

```sh
python3 -B ramsey_r55_k4_expansion_interface/reproduce.py
```

Expected status: `REPRODUCED_K4_EXPANSION_INTERFACE`. This checks both pinned
dependencies, the source manifest, all 18 `(q,r)` suffixes through a separate
literal reconstruction, every local truth table, 7,172 exhaustive small
counter assignments, and boundary propagation controls under normal and `-O`
Python.

To reproduce the full audited example, first obtain the four pinned McKay
Ramsey(4,4) files through the h3873 downloader, then use a fresh CNF path:

```sh
python3 -B ramsey_r55_global_maximal_packing/catalog.py /tmp/k4e-data --download
python3 -B ramsey_r55_k4_expansion_interface/reproduce.py \
  --cache /tmp/k4e-data --cnf /tmp/k4e-q7r7.cnf --generate
```

The replay generates no solver output. `augment.py --sat MODEL` accepts only
a complete satisfying augmented assignment and passes its physical part to
h3887's exact model and five-set verifier. [PROOF.md](PROOF.md) proves the
structural reduction and encoding, [HANDOFF.md](HANDOFF.md) specifies the
search interface, and [VALIDATION.md](VALIDATION.md) records exact evidence
and trust boundaries.
