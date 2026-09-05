# A certified 574-vertex obstruction inside the sealed Parts pool

The explicit strict unit-distance graph here has **574 vertices, 2707
edges and chromatic number five**. It retains all 374 vertices of the
fixed Parts large component L and selects 200 of the 303 pool points:
110 original S points and 90 Q5 completion points.

Deleting any one of those **200 selected pool vertices** gives a graph
with chromatic number four. Hence every proper subset of this selected
pool is four-colourable beside L. The certificate supplies all 200
deletion colourings, a proper five-colouring and a regenerable full-graph
DRAT refutation of four-colourability.

This establishes minimality only with respect to the selected pool
vertices. Deletions inside L have not been tested, and full vertex
criticality is not claimed. The graph exceeds the 509-vertex benchmark;
it does not improve the record or close the whole 303-point pool.

[PROOF.md](PROOF.md) states the exact graph, encoding and claim scope.
[certificate.json](certificate.json) is a 58411-byte positive certificate.
The final negative certificate uses the ordinary full-graph colouring
CNF, so completeness of the twenty-class L interface is **not** a
verification assumption for this graph.

## Verify the exact graph and positive witnesses

From the repository root with Python 3.11 standard library:

```sh
python3 hadwiger_nelson_parts509_pool_obstruction574/verify.py --cnf /tmp/parts574.cnf
```

The default command reconstructs exact integer coordinates, checks all
unit pairs in the 677-point universe, checks the five-colouring and all
200 deletion colourings, and writes the exact four-colouring CNF.
It explicitly reports that non-four-colourability has not yet been
checked. [expected.json](expected.json) contains deterministic graph and
CNF facts. The CNF has 2296 variables and 11405 clauses, SHA-256:

```text
4eb76b20de1b91381a9491e1debeaac7dcb6b30c0255311376dfdeeba5c73f8d
```

Complete the negative verification with Kissat 4.0.4 and drat-trim:

```sh
/path/to/kissat --time=300 /tmp/parts574.cnf /tmp/parts574.drat
python3 hadwiger_nelson_parts509_pool_obstruction574/verify.py \
  --proof /tmp/parts574.drat --drat-trim /path/to/drat-trim
```

Kissat's expected exit code is 20. Final verifier status:

```text
574-VERTEX GRAPH AND ALL 200 POOL DELETIONS VERIFIED
```

The producing full-graph proof took 5.784 seconds to generate and 3.988
seconds to check. Its 7336948 bytes and SHA-256 are recorded in
[proof_manifest.json](proof_manifest.json), with executable hashes and
limits. The proof is generated locally rather than committed. A different
valid DRAT refutation is accepted; proof-byte equality is not required.

## Bounded discovery

This was one search from the non-four-colourable side, following two
unknown full-family QBF pilots. A vertex-activation SAT encoding permits
assumption-core extraction without a selection-budget counter. The seed
omits original vertex 374, ensuring that it cannot simply return the
original Parts selection. A deterministic deletion pass tries remaining
S vertices before Q5 points, in increasing label order. Each returned
core is provisional until independently certified on the final graph.

The pass completed 263 queries: 200 SAT, 63 UNSAT and no unknown result,
using 54.389 cumulative native solver seconds. Limits were 100000
conflicts per query, 304 queries and 150 cumulative native seconds.
The 200 positive models restrict to the final deletion witnesses.
[search_summary.json](search_summary.json) records measurements and the
separate calibration on 58 fixtures, 1131 selections and 221 small cores.
No colouring-library cut or shrink run was started.

Optional discovery reproduction needs `python-sat==1.8.dev24` with
CaDiCaL 1.9.5, in addition to the standard-library verification tools:

```sh
python3 -m pip install -r hadwiger_nelson_parts509_pool_obstruction574/requirements.txt
python3 hadwiger_nelson_parts509_pool_obstruction574/controls.py
python3 hadwiger_nelson_parts509_pool_obstruction574/search.py --work /tmp/parts574-search
```

Use a fresh work directory. Search emits a provisional core and saved
positive models; it does not itself certify negative verdicts or make
a record claim. Runtime-limited discovery may vary with execution
conditions. The fixed published certificate is independently verifiable
regardless of how discovery behaves on a later system.

## Scope and handoff

This calibrates a different certificate method and supplies an explicit
non-four-colourable seed involving 90 completion points. It proves no
performance advantage over the QBF family tests, which ask a different
question. Both timed-out QBF configurations and the isolated cut/shrink
loop remain paused.

The next useful bounded assessment is an indispensability audit of the
374 retained L vertices in this certified graph. That would be a new
minimization phase; it has not started. No new seed or geometric family
was opened, and no background job remains running.

The exact coordinate sources, reviewed integer geometry reader and
explicit L witness table are pinned in [manifest.json](manifest.json).
Trust includes those parsers and integer arithmetic, the elementary CNF
and restriction arguments, and drat-trim. These are author checks, not
external review or proof-assistant formalization. No novelty priority
is claimed for graph minimization or assumption-core extraction; primary
context is [Parts, Graph minimization](https://arxiv.org/abs/2010.12665)
and the [PySAT solver API](https://pysathq.github.io/docs/html/api/solvers.html).
