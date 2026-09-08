# Complete exclusion of punctured Cayley graphs of order 44

No graph obtained by deleting one vertex from an undirected Cayley graph on
44 vertices is good for `R(5,5)`. Here good means having neither a clique nor
an independent set of order five. The conclusion covers every inverse-closed
connection set on every group of order 44; no degree, connectivity, or final
43-vertex automorphism is assumed.

The reduction has two parts. First, if a Cayley graph contains a
monochromatic five-set, translating that set produces a copy avoiding any
chosen vertex. Thus a good 43-vertex puncture would make the full graph good.
Second, there are exactly four groups of order 44. Exact inverse-orbit CNFs
for all four are UNSAT.

The certificate consists of four CNF cores totaling 451,701 bytes. Every core
clause is independently reconstructed as a literal rooted monochromatic-five
obstruction. A standard-library DPLL checker exhausts both values of every
remaining variable and proves all four cores UNSAT. The public proof therefore
does not depend on the production SAT solver or its omitted DRAT streams.

This is a complete decision for a structured global family. It constructs no
good43 graph and proves no improvement to the known lower bound for
`R(5,5)`. It does not cover arbitrary vertex-transitive graphs of order 44 or
graphs merely close to a Cayley graph.

## Reproduce

CPython 3.11 or later and the standard library suffice. From the repository
root run:

```sh
python3 -B ramsey_r55_cayley44_puncture_obstruction/reproduce.py
```

Expected final line:

```text
REPRODUCED_COMPLETE_CAYLEY44_PUNCTURE_EXCLUSION
```

The replay regenerates all four complete formulas, checks every group table
and formula clause independently, verifies that every certificate clause is
physical, runs 12,291 brute-force controls against the DPLL procedure, and
then decides the four certificate cores. The reference replay visits 67,656
DPLL states and 33,830 contradiction leaves; runtime is about two minutes on
the production host and is not part of the claim.

See [PROOF.md](PROOF.md) for the reduction and completeness argument and
[VALIDATION.md](VALIDATION.md) for exact counts, production provenance, and
trust boundaries.
