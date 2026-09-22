# A sharp Erdős--Hajnal exponent for perfect-or-pentagon modular graphs

Call a graph **pentagon-perfect modular** if it can be built recursively by
substitution, starting from one-vertex graphs, with every outer graph either
perfect or isomorphic to `C_5`.  Equivalently, every prime quotient in its
modular decomposition is perfect or `C_5`.

This directory proves that every nonempty graph `G` in this hereditary class
satisfies

```text
alpha(G) * omega(G) >= |V(G)|^(log_5 4),
```

and hence

```text
max(alpha(G), omega(G)) >= |V(G)|^(log_5 2).
```

Both exponents and the leading constant one are sharp.  The `k`-fold
lexicographic power of `C_5` has order `5^k` and both clique and independence
number `2^k`.

The proof is structural.  Its only exceptional local calculation is a weighted
inequality for substitution through `C_5`.  The relevant two fractional
stable-set polytopes each have exactly twelve vertices: the eleven incidence
vectors of stable sets and the all-half vector.  [`verify.py`](verify.py)
enumerates these vertices with exact rational Gaussian elimination and audits
all 144 vertex pairs.  It also checks the sharp-family recurrence.  The code
does not prove the imported perfect-graph polytope theorem or replace the
universal induction in [`THEOREM.md`](THEOREM.md).

Run with standard-library Python 3.11 or later:

```sh
./run_checks.sh
```

See [`SOURCES.md`](SOURCES.md) for the precise distinction from the classical
substitution theorem for forbidden patterns and from the theorem for
`C_5`-free host graphs.
