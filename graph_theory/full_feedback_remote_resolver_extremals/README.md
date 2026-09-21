# Remote-resolver extremals and trees

This directory proves two parameter-uniform results for the remote signatures
that control one-probe localization of independent graph blow-ups:

* a connected graph with a degree-`d` remote resolver has at most
  `2^d+d-1` vertices, sharply for every `d`, even in a bipartite diameter-four
  family; and
* all rooted trees with a remote resolver are classified: apart from `K_2`,
  they are stars whose edges are independently subdivided at most once.  Their
  sharp order bound is `2d+1`.

The proof and the independent-blow-up consequence are in
[THEOREM.md](THEOREM.md).  The standard-library checker in
[verify.py](verify.py) audits the general signature count on every connected
labelled graph through order five, reconstructs the sharp family through
degree eight, and checks the tree classification on every labelled tree
through order eight using Prüfer codes.  Enumeration only audits the formulas;
the displayed arguments establish the universal claims.

## Reproduce

Python 3.11 or later is sufficient; there are no third-party dependencies.

```bash
python3 -m unittest -v test_verify.py
python3 verify.py
sha256sum -c SHA256SUMS
```

The second command should match [EXPECTED_OUTPUT.txt](EXPECTED_OUTPUT.txt).

## Trust boundary

The checker uses exact finite sets and integer graph distances, with no
solver, floating point, randomness, network input, or external graph
catalogue.  It provides an implementation-level audit, not a proof-assistant
formalization.  Literature scope and dependencies are recorded in
[SOURCES.md](SOURCES.md).
