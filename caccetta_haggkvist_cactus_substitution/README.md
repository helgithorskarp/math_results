# Caccetta--Haggkvist under cactus substitution

This directory proves a substitution theorem for the Caccetta--Haggkvist
short-cycle bound.

Let `Q` be an orientation of a cactus forest and replace every quotient
vertex `i` by a nonempty digraph `H_i`, putting all arcs from `H_i` to `H_j`
whenever `i -> j` is an arc of `Q`.  For every fixed `k >= 2`, if each
`H_i` satisfies the Caccetta--Haggkvist implication at `k`, then so does the
substitution.  Consequently the full conjecture is closed under cactus
substitution, and every recursively cactus-substituted oriented graph
satisfies it.

For independent modules the result is sharper.  If the quotient has positive
minimum weighted outdegree, then

```text
directed_girth * minimum_outdegree <= number_of_vertices.
```

For a connected quotient, equality holds exactly for a consistently directed
cycle with all independent modules of the same size.

The proof is in [THEOREM.md](THEOREM.md).  The argument is universal; the
finite computation only audits definitions, the double-counting boundary,
and equality cases.

## Reproduction

Requires CPython 3.11 or later and no third-party package.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

Compare the first command with `EXPECTED_OUTPUT.json`.

## Scope

- The quotient is an orientation: there is at most one directed arc on each
  quotient edge.
- The underlying quotient is a cactus forest, meaning every undirected edge
  belongs to at most one simple cycle.
- The modules may be arbitrary finite nonempty loopless digraphs.
- The theorem does not prove the general Caccetta--Haggkvist conjecture.
- The included wheel orientation shows that the nonoverlapping-cycle
  certificate can fail just beyond the cactus setting; it is not a
  counterexample to Caccetta--Haggkvist.

## Trust boundary

The theorem rests on the written double-counting proof.  The audit uses exact
Python integers, exhaustive labelled graphs through quotient order five,
explicit cycle enumeration, and SHA-256.  It uses no solver, randomness,
floating point, or external data.  The finite audit is corroboration, not a
proof of the unbounded statement.
