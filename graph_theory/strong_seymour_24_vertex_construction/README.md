# A 24-vertex tournament without a strong Seymour vertex

The construction improves the published 36-vertex upper bound to **24**.
It reweights the nine-vertex quotient in Gibbons's earlier constant-nine
construction. Its clusters form three cyclic layers of sizes a,b,c. If b>a and c>2b,
three explicit types of deficient Hall sets exclude every strong Seymour
vertex, for arbitrary tournaments inside the clusters. The choice (1,2,5)
has 24 vertices, with Hall witnesses of sizes 5>4, 8>7, and 10>9.

For transitive clusters, the exact number of strong vertices is

    3 * 1[c <= 2b] + 3 * 1[b <= a].

Thus 24 is the exact minimum **in this three-parameter family**. The
unrestricted minimum is not determined. Combining our upper bound with the
separately accepted graph result through order 15 gives **16 <= m <= 24**.

Read [PROOF.md](PROOF.md) for the self-contained construction and universal
classification, and [SOURCES.md](SOURCES.md) for prior work and claim scope.
The literal [24-by-24 adjacency matrix](tournament24.txt) uses the order
A0,A1,A2,B0,B1,B2,C0,C1,C2, with transitive vertices consecutive inside each
cluster. Entry 1 means that the row vertex beats the column vertex.

## Reproduce

Python 3.11 or later; the proof checks use only the standard library.
Run from this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > /tmp/seymour24-primary.json
diff -u EXPECTED_PRIMARY.json /tmp/seymour24-primary.json
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py > /tmp/seymour24-independent.json
diff -u EXPECTED_INDEPENDENT.json /tmp/seymour24-independent.json
sha256sum -c SHA256SUMS
```

`verify.py` checks the nine Hall rows, their exact primal/dual identities,
the complete symbolic closure table, every vertex of the explicit example,
examples with balanced internal clusters and doubled parameters, and five
negative fixtures. `independent_check.py` imports none of that code. It
exhausts all 110,592 Hall subsets of the literal example, checks maximum
matchings separately, and audits all 216 parameter triples 1<=a,b,c<=6 on
6,804 expanded vertices.

Reference run: CPython 3.11.2; the two checks took about 0.1 and 2.8 seconds,
with peak child RSS about 16 MiB on the research host. Both also pass with
Python optimization enabled (`python3 -O`), with identical outputs.

Literal tournament SHA-256:

    ae2ee4fe49a5945ac1cf0e0b97ba828812cbf4dd00a3e1536eb289e670812fa2

Independent parameter-audit SHA-256:

    8b337c99a3fdfc5fe98d04b037784797061d60eee64eda24dc6a37c225461e30

The symbolic proof is universal; the finite audit is corroboration. The
separate lower-bound SAT computation is not replayed here. These are internal
checks by different methods, not an independent external review.

## Optional discovery replay

With `ortools==9.15.6755` installed, run `python3 search_weights.py` to recover
feasible positive cluster sizes on the published quotient. This script uses
one disjunction of exact Hall inequalities per quotient root and validates
any returned assignment with ordinary integers. The solver's optimality or
infeasibility status is not part of the proof. No third-party package is
needed for the default verification commands.
