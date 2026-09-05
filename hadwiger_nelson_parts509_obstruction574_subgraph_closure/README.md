# No record improvement by deleting vertices of H574

**Every subgraph with at most 508 vertices of the previously certified
574-vertex graph H is four-colourable.** The certificate supplies proper
four-colourings of H-v for 309 additional vertices. Together with 200
previously published deletion witnesses, these force 509 distinct vertices
in every non-four-colourable subgraph of H.

This closes the entire deletion-only family inside this one graph. It
does not close the full 677-point coordinate universe, establish that H
is vertex-critical, or produce a smaller five-chromatic graph. No claim
is made that the 509 forced vertices themselves induce a five-chromatic
graph. The 65 remaining single-vertex deletions were not tested.

The exact graph is H=L union X, where L has global labels 0 through 373
and X is the explicit 200-element `pool_labels` list in
`../hadwiger_nelson_parts509_pool_obstruction574/certificate.json`.
H has 574 distinct points and all 2707 strict unit edges. Coordinates are
exact elements of Q(sqrt(3),sqrt(5),sqrt(11)), with common denominator 288
and the existing bit-mask basis. The earlier package separately certified
chi(H)=5 using checked DRAT; this new subgraph closure requires only
positive colourings.

## Verification

From the repository root, using Python 3.11 or later:

```bash
python3 hadwiger_nelson_parts509_obstruction574_subgraph_closure/verify.py
python3 hadwiger_nelson_parts509_obstruction574_subgraph_closure/check_checker.py
```

No SAT package, native solver, or proof trace is needed for this check.
It reconstructs every exact edge, verifies all 509 deletion colourings,
and compares the result with `expected.json`. The result includes:

```text
graph_vertices: 574
graph_edges: 2707
old_pool_deletion_colourings: 200
new_L_deletion_colourings: 309
distinct_forced_vertices: 509
verified_retained_edge_incidences: 1372888
all_subgraphs_through_order: 508
all_such_subgraphs_four_colourable: true
```

Verification took about 5 seconds in the producing environment. The new
199090-byte certificate has SHA-256:

```text
647c3011ac61449b274b1b8815ce17d1da6c948da54ba6ed79546eb856c20469
```

The authoritative input and certificate hashes are in `manifest.json`.
The earlier 200 witnesses use explicit L colourings from the interface
table. Only their colour strings are used; completeness of that table
is not a premise of this theorem.

## Reproduce the bounded discovery run

The saved colourings are sufficient evidence, independent of how a SAT
solver found them. To reproduce the discovery method, create a Python
environment outside the repository and install the pinned PySAT version:

```bash
python3 -m venv /tmp/hn574-audit-venv
/tmp/hn574-audit-venv/bin/pip install -r hadwiger_nelson_parts509_obstruction574_subgraph_closure/requirements.txt
/tmp/hn574-audit-venv/bin/python hadwiger_nelson_parts509_obstruction574_subgraph_closure/controls.py
/tmp/hn574-audit-venv/bin/python hadwiger_nelson_parts509_obstruction574_subgraph_closure/search.py --work /tmp/hn574-L-audit
```

The producer used Python 3.11.2, python-sat 1.8.dev24, CaDiCaL 1.9.5,
one worker and a 4 GiB address-space limit. `plan.json` fixes ascending L
order, 100000 conflicts per query, a 300-second cumulative native limit
checked between queries, and an early stop upon 309 positive witnesses.
It performs no graph shrinking or seed update. `search.py` writes an
atomic checkpoint after every completed query and refuses to overwrite
an existing audit. The recorded run is complete; it needs no resumption.

All 309 attempted deletions, labels 0 through 308, were SAT and their
colourings were directly checked. The run stopped at the planned target
after 95.543597 native seconds and 101.383291 wall seconds, with peak RSS
77896 KiB. There were no negative or unknown answers. The remaining
labels 309 through 373 were deliberately left untested at this milestone.
Control tests compared 1629 assignments in 48 fixtures with direct
backtracking and recovered a known positive deletion in the actual graph.

The direct activation formula has 2670 variables and 11405 clauses.
Triangle pins lie at the required pool vertices (384,386,388), which
survive every L deletion. Deleting L can introduce new boundary patterns,
so this discovery oracle does not use the complete-L interface reduction.
See `PROOF.md` for the exact encoding and the positive-certificate bridge.

Native models and timings may vary across builds; the defining output is
a directly verified family of proper colourings. Large CNFs, solver
logs and operational checkpoints stay outside the source package. The
compact `search_summary.json` records the producing run. The older H574
source commit was f3a38e5051ec700043cf7694865993eb4ec8ca20.

## Decision and scope

Further deletion-only search inside H cannot improve the 509-vertex
record. Any at-most-508 non-four-colourable graph within the larger fixed
677-point universe must include a pool vertex outside X. This statement
is a necessary condition, not a closure of those other supports. For the
older family that retains every vertex of L, exclusion of subsets of X
already followed from the previous 200 pool-deletion witnesses; the new
content also permits arbitrary deletions in L.

The bounded audit is complete. A different support or a certificate
covering multiple supports would be a separate research phase. No new
geometry or teammate construction was enumerated here.
