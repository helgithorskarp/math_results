# Type-2 total colourings from sparse regular complements

This directory proves a parameter-uniform exact total-colouring theorem.
Let `H` be a `K_4`-free `r`-regular graph of even order `N`, with no perfect
matching, and put `G = complement(H)`.  If either

```text
r <= 4
```

or

```text
N > 4r + 2,
```

then

```text
chi''(G) = Delta(G) + 2 = N - r + 1.
```

Thus `G` is forced to be Type 2.  The lower bound is a direct parity count:
in a `(Delta+1)`-total-colouring of an even-order regular graph, every vertex
colour class is even.  Here such a class is a clique of `H`, so `K_4`-freeness
forces every nonempty class to be an edge.  The classes would therefore form
a perfect matching of `H`, contrary to hypothesis.  The matching upper bound
comes from the established Total Colouring Conjecture for `Delta >= N-5`, or
from Chew's dense-graph theorem.

An explicit infinite family starts with three copies of the prism
`C_m square K_2`, subdivides one rung in each copy, and joins the three new
subdivision vertices to one central vertex.  For every `m>=4` this gives a
connected cubic triangle-free graph `H_m` with no perfect matching.  Hence

```text
|V(H_m)| = 6m+4,
chi''(complement(H_m)) = 6m+2.
```

The nonexistence of a Type-1 colouring is universal and is proved in
[`THEOREM.md`](THEOREM.md).  [`verify.py`](verify.py) is a definition-level
audit of the explicit family, not a substitute for that proof.  Reproduce it
with standard-library Python 3.11 or later:

```sh
./run_checks.sh
```

See [`SOURCES.md`](SOURCES.md) for the classical conformability input, the
dense total-colouring theorems, the exact prior-art boundary at complement
degree two, and the bounded novelty search.
