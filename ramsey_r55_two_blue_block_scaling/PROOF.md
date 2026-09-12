# Exact domain and consequence of the complete negative scaling test

Let H be a labeled R(4,4) graph on vertices 0,...,10. Add blue cliques
B1={11,12,13,14} and B2={15,16,17,18}. The 55 core edges and twelve internal
block edges are fixed. Of the 171 total pairs, the other 104 are decisions:
88 core-to-block edges and sixteen edges between the two blocks.

Call H two-block compatible if some coloring of these 104 edges avoids
red K4 and blue K5 on all nineteen vertices. There is no symmetry reduction,
fixed interblock matrix, degree assumption, catalog-completion hypothesis,
or restriction on the free edges. The SAT base has 171 variables and 15,516
clauses: all C(19,4) red-four prohibitions, all C(19,5) blue-five prohibitions,
and twelve blue-block units. Each core is assigned by its 55 literal units.

The complete computation establishes two-block compatibility for all 546,355
catalog records other than 516166. Existence is certified by literal graphs;
it does not depend on trusting the solver. The verifier visits every catalog
row in order and constructs the full 19-vertex graph from its witness. It
checks the core's defining property, the two forbidden clique conditions,
exact input lengths, padding and the negative-sentinel ledger. Exhaustion of
the whole pinned file prevents any unverified or omitted core from being
called compatible.

For record 516166, restrict to H union B1. This is the complete fifteen-vertex
problem already refuted in the source-published one-blue-block package. Each
of its 285 clauses is present in the new complete nineteen-vertex formula
under the physical variable injection. `verify.negative` checks the actual
clause lookup, renames all LRAT input and derived identifiers, and checks the
trace through to the empty clause on the 104-variable input. This establishes
the sole negative case without promoting a new solver status to evidence.
The old obstruction proof is credited, not claimed as a new refutation.

In an original `bo1-q8-r{r}-c{c}` task with r=5 or r=6, select the core at
labels 32..42 and the first two prescribed blue blocks at labels 4r..4r+7.
All nineteen vertices lie in the original red-K4-free residual; the global
blue-K5 prohibitions apply to them too. The local-to-original vertex map is

```
[32,33,34,35,36,37,38,39,40,41,42, 4r,4r+1,...,4r+7].
```

Thus two-block compatibility is necessary for each of those complete original
tasks. The two incompatible IDs, `bo1-q8-r5-c516166` and
`bo1-q8-r6-c516166`, were both already refuted on their actual full parent
inputs in the prior package. The explicit set difference in `verify.py` is
empty. The r=7 exclusion from that package is preserved separately.

Consequently the unaugmented two-block forbidden-clique fragment cannot yield
another exclusion among any of the 1,092,710 retained r5/r6 original IDs.
This is a quantified barrier for this precise necessary test, not a proof
that the full original tasks are feasible. Constraints involving the omitted
vertices or additional proved global restrictions could still exclude them.
No projection equivalence with the full parent formula is asserted.

The old 521 source-certified original exclusions and 2,188,657 source-certified
UNKNOWN IDs remain unchanged. The committed accepted count and independent
review state remain separate. All 956 q8 physical jobs remain unclosed;
neither the q8,r8 edge-119 mixed-premise join nor the q10 ledger is altered.
The short scaling pass provides complete failure evidence for the proposed
route and calls for a high-level approach correction within R(5,5).
