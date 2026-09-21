# A finite-prefix barrier for Erdős--Gyárfás density arguments

For every integer `R>=2`, there is a finite simple graph `X_R` with all of
the following properties:

- its minimum degree is three;
- every nonempty proper subgraph has a vertex of degree at most two;
- exactly two thirds of its vertices have degree three and the rest have
  degree four;
- the degree-four vertices are independent;
- the degree-three vertices induce a perfect matching, and each matching
  edge has a unique common degree-four neighbor; and
- it has no cycle of any length from `4` through `2^R`.

Thus `X_R` avoids, in particular, every power-of-two cycle in the finite
prefix `4,8,...,2^R`, while saturating the known two-thirds cubic-density
bound and its equality structure for a hypothetical lexicographically
minimal counterexample to the Erdős--Gyárfás conjecture.

These graphs are **not counterexamples** to the conjecture: the construction
does not control power-of-two cycles longer than `2^R`.  The result instead
shows that no fixed finite prefix of the forbidden cycle lengths, even when
combined with the full known degree-critical equality structure, can by
itself make the two-thirds density bound strict.

The construction starts with a connected simple 4-regular graph `K` of
sufficiently large girth, takes a strongly connected balanced orientation,
subdivides every edge, and joins the two subdivision vertices on edges
oriented into each original vertex.  A cycle of length `ell>=4` in the
expansion projects to a closed trail in `K` of length at most `2ell/3`.

The complete proof is in [THEOREM.md](THEOREM.md).

## Reproduction

The theorem is structural and does not depend on computation.  The checker
builds a concrete 78-vertex instance from the incidence graph of the
projective plane of order three.  It verifies the base girth, every degree and
equality property, all 130 single-edge criticality deletions, and the complete
absence of cycles of lengths four through eight.

```bash
cd graph_theory/erdos_gyarfas_finite_prefix_barrier
./run_checks.sh
```

CPython 3.11 or later and the standard library suffice.  Expected output is
recorded in `EXPECTED_OUTPUT.txt`.  The script also requires identical
checker output under normal and optimized Python, so every audit remains
active under `python -O`.

## Trust boundary

- `THEOREM.md`: universal construction, criticality proof, and cycle
  projection.
- `verify.py`: exact concrete construction and definition-level audit.
- `test_verify.py`: positive, negative, projection, and tampering tests.
- `SOURCES.md`: primary-source and novelty audit.
- `SHA256SUMS`: integrity manifest.

The arbitrary-girth input is the classical existence theorem for regular
graphs of prescribed girth.  The checker uses no solver, randomness,
floating point, network input, external dataset, or omitted certificate.
Its finite instance corroborates conventions; it is not the proof of the
parameter-uniform theorem.
