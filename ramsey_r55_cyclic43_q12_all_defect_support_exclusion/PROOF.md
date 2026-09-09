# Proof certificate

## Theorem

Let `G_0,...,G_237` be the 238 red-blue colourings in the pinned
`complete_additional_objective_12_rotation_representatives` list.  For each
`i`, let `D_i` be the set of monochromatic copies of `K5` in `G_i`, and let

```text
S_i = union { E(Q) : Q in D_i }.
```

Every source has exactly twelve defects.  No colouring that agrees with
`G_i` on `E(K_43) \ S_i` is free of both red and blue `K5`s.

## Ramsey clauses after fixing the complement of the support

Give each edge `e` in `S_i` a Boolean variable `x_e`, with red equal to one.
For a five-set `Q`:

- if every fixed edge of `Q` is red, avoiding a red `K5` gives
  `OR_{e in E(Q) intersect S_i} not x_e`;
- if every fixed edge of `Q` is blue, avoiding a blue `K5` gives
  `OR_{e in E(Q) intersect S_i} x_e`.

All other five-set constraints are already satisfied by fixed edges of both
colours.  Neither displayed clause is empty: an all-fixed monochromatic
five-set would be a source defect, so all ten of its edges would belong to
`S_i`.

These clauses are exact for the subcube.  More importantly for certificate
checking, each displayed clause is individually a valid physical consequence
of the absence of monochromatic `K5`s.

## Exhaustive generation

`classify_up.cpp` reconstructs the cyclic seed and each indexed toggle set.
It scans all `binom(43,5) = 962598` five-sets to find the twelve defects and
their exact union support.  It then scans every five-set again, builds the
reduced clauses above, and performs ordinary unit propagation.  For each
assignment it records the witnessing five-set, the forced physical edge, and
its forced colour.  It records the final five-set whose clause is false.

All 238 traces end in conflict.  There are 18,077 proof rows in total,
including exactly 238 terminal conflicts.  Individual cores contain 57 to 91
physical clauses.  Support sizes have the exact distribution

```text
60^13 66^20 72^15 77^5 78^57 81^3 82^7 83^21
84^63 88^2 89^4 90^22 91^2 95^2 97^2.
```

## Independent verification

`verify.py` does not repeat the generator's exhaustive five-subset scan to
find defects.  It builds red and blue adjacency bitsets and recursively lists
all five-cliques in each colour.  Their union reconstructs `S_i` and checks
the defect counts and every census row.

For every proof row, the verifier reconstructs the ten physical edges of its
five-set and derives all applicable reduced Ramsey clauses directly from
`G_i` and `S_i`.  An assignment row is accepted only if a derived clause has
exactly one unassigned edge, all assigned literals are false, and the declared
colour is the unique satisfying value.  The last row is accepted only if a
derived clause is completely false.  Hence each trace is a self-contained
unit-propagation refutation from physical Ramsey clauses.

The release and sanitized C++ executions generate identical evidence.
Normal and optimized Python executions independently accept all 238 traces.
Altered support counts, altered physical witnesses, and missing final
conflicts are rejected.

## Trust boundary

The finite claim depends on C++/Python integer and file semantics, inspection
of the two short implementations, and the SHA-256-pinned 238-source input.
It does not depend on SAT-solver soundness.  Completeness beyond that inherited
source list is not claimed.
