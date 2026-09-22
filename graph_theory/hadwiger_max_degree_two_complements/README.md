# Hadwiger numbers of complements of maximum-degree-two graphs

This directory gives a self-contained proof and exact computational audit of
the following classification.  If `H` is a nonempty finite simple graph with
maximum degree at most two, `alpha(H)` is its independence number, and
`eta(G)` is the Hadwiger number, then

```text
eta(complement(H)) = floor((|V(H)| + alpha(H))/2),
```

except when `H` is the disjoint union of isolated vertices and exactly one of

```text
C3, C4, P4, P5,
C5 + P2, C5 + P3, C6 + P2, C6 + P3.
```

For those eight families the value is one smaller.  The proof is in
[THEOREM.md](THEOREM.md).  [SOURCES.md](SOURCES.md) records the primary prior
art and the deliberately narrow status claim.  As a corollary, Hadwiger's
conjecture holds throughout this complement class.

## Reproduction

Only Python 3.10 or later and POSIX shell utilities are required.  From the
repository root run

```sh
./graph_theory/hadwiger_max_degree_two_complements/run_checks.sh
```

The checker:

- constructs the canonical independent set and auxiliary forbidden graph;
- verifies every returned branch-set model directly in the complement;
- audits every disjoint union of paths and cycles through order 16;
- independently enumerates all maximum independent sets and residual pairings
  for the eight exceptional cores, confirming that equality is impossible;
- audits the small auxiliary matching obstructions; and
- runs mutation-sensitive unit tests.

The finite audit is a check of the definitions and boundary cases, not the
proof of the universal theorem.  The universal step is the structural
argument in `THEOREM.md`: the auxiliary graph always has maximum degree two,
and Dirac's theorem supplies the required matching beyond the explicitly
audited orders.

`EXPECTED_OUTPUT.json` is the compact expected summary.  `SHA256SUMS` binds
the public source files.
