# Five-cycle cores for three-neighborhood split graphs

Every finite simple split graph with at most three triangle-active
independent-side neighborhood types has a minimum triangle edge cover whose surviving
clique core maps homomorphically to `C_5`. This holds for every clique order
and all multiplicities, including the known examples where no optimal
clique core is bipartite.

The proof reduces to 392 labeled templates on nine vertices. A 12 KB
certificate and an independent exhaustive checker establish their
five-cycle maps. The same reduction gives an exact `O(k^7)` arithmetic
algorithm for the cover number, with a compact optimal-cover witness.

**This is a complete computer-assisted author proof of a covering
structure theorem, pending independent review. The three-type Tuza
inequality remains open.**

- [Proof, exact formula, and sharpness](PROOF.md).
- [Exact cover algorithm](cover.py).
- [Finite certificate](templates.json) and [standalone verifier](verify_templates.py).
- [Certificate generator](generate.py) and [literal small-graph audit](audit.py).
- [Expected results](EXPECTED.json) and [prior work](SOURCES.md).

From this directory, with Python 3.10+ and no third-party packages:

```sh
python3 verify_templates.py
python3 audit.py
python3 cover.py 1 1 0 2 1 0 2 0 22 22 22
sha256sum -c SHA256SUMS
```

The verifier checks all `1,048,576` optional-edge subsets: `66,666` are
triangle-free and `392` are maximal; every maximal template has a verified
`C_5` map. The audit checks `1,287` protected hosts and `8,937` exact cover
instances. The final example returns `tau=12` and a nine-edge clique core.
Every bipartite core for that example has at most eight edges.

The eleven command-line integers are the eight clique-cell counts for
masks `0,...,7`, followed by three center multiplicities. Bit `i` of a
mask records membership in neighborhood `i`. The algorithm enumerates
retained count vectors and is intended as an exact reference implementation;
the `O(k^7)` bound has a substantial constant.

To regenerate the certificate, run `python3 generate.py` and then both
verification commands. All failures use explicit exceptions and remain
active under `python3 -O`. See `EXPECTED.json` for deterministic hashes.

Tested on CPython 3.11.2: the exhaustive template verifier took about
0.65 seconds and the literal audit about 3.9 seconds on the research host.
