# Radius-three deletion rigidity of the order-28 Folkman witness

Let `G` be the 28-vertex, `K4`-free, 7-chromatic Cayley graph in the
[companion construction](../chromatic_folkman_n7q4_order28/).  This directory
establishes the following finite structural statement.

> **Theorem.** Delete any vertex `v` of `G`, and let `H=G-v`.  If `J` is a
> `K4`-free graph on `V(H)` with at most three inherited edges absent,
> `|E(H) \ E(J)| <= 3`, then `J` is six-colourable.  Edges outside `E(H)` may
> be added without restriction.

Thus this particular order-28 witness cannot be converted to an order-27
`K4`-free, 7-chromatic graph by deleting a vertex, deleting at most three
additional inherited edges, and then adding arbitrary edges.

## Reduction and certificate

The Cayley graph is vertex-transitive, so it suffices to delete its identity.
The verifier reconstructs the graph and checks this reduction explicitly.
The remaining graph `H` has 27 vertices and 156 edges.

The file `colourings.txt` contains 42 partitions of those vertices into six
classes.  Introduce one Boolean edge variable for each of the 351 vertex
pairs.  The deterministic generator makes a CNF with:

- 17,550 clauses, one for each four-set, excluding a `K4`;
- 1,086 clauses and 468 auxiliary variables forming a forward sequential
  counter for at most three absent inherited edges; and
- 42 positive clauses saying that a counterexample must break every listed
  partition with a monochromatic edge.

The result has 819 variables and 18,678 clauses.  Its SHA-256 digest is

```text
ec2fa762b02b8c385948e533cf9608fb5a290c7e2191cc701b23b38a41d5f421
```

CaDiCaL reports `UNSAT`.  `drat-trim` independently verified the textual DRAT
trace using 2,426 input clauses and 23,935 core lemmas (all RUP, no RAT), with
3,448,010 resolution steps.  Exact hashes and counts are in
`solver_record.txt`.  The 23.3 MB generated trace is deliberately omitted;
the byte-canonical formula generator is retained.

If a graph `J` in the theorem were not six-colourable, it would break all 42
partitions, satisfy every `K4` clause, and satisfy the deletion counter.  Its
edge variables, together with a suitable counter assignment, would therefore
satisfy the refuted formula, a contradiction.

## Solver-independent radius-two gate

The first six partitions admit a short exhaustive audit independent of the
SAT generator.  For each of the `C(156,2)=12,090` nominated pairs of inherited
edges, `radius2_audit.py` deletes the pair and considers every edge whose
individual addition remains `K4`-free.  Deleted edges may be added back, so
this represents every graph missing zero, one, or two inherited edges.

The audit recursively enumerates all feasible subsets and retains every
inclusion-maximal completion.  Any individually rejected edge already forms
a `K4` with the fixed subgraph and can never occur in a feasible completion;
any nonmaximal feasible graph is a subgraph of a maximal one.  There are
30,211 raw maximal completions and 4,416 distinct labelled ones.  In order,
the six fixed partitions colour 3,163, 948, 234, 59, 9, and 3 previously
uncovered completions.  None remains.  This proves the radius-two subcase and
provides a transparent structural seed for the radius-three certificate.

## Reproduce

Python 3.8 or later is sufficient for the two source checks; there are no
third-party Python dependencies.

```bash
python3 verify.py
python3 radius2_audit.py
python3 verify.py --write-cnf build/radius3.cnf
sha256sum build/radius3.cnf
```

To regenerate and independently check a proof with CaDiCaL and `drat-trim`:

```bash
cadical --no-binary build/radius3.cnf build/radius3.drat
drat-trim build/radius3.cnf build/radius3.drat
```

CaDiCaL conventionally exits with status 20 after proving UNSAT.  A newly
generated proof need not have the recorded byte hash, but it must verify
against the formula with the displayed hash.

## Scope

This is a local rigidity theorem about one explicit graph.  It does **not**
prove the lower bound `n(7,4) >= 28`, classify all 27-vertex `K4`-free graphs,
or exclude modifications that remove four or more inherited edges.  The
radius-three theorem depends on the stated SAT/DRAT trust boundary; only the
radius-two subcase has the separate solver-independent exhaustive audit.
