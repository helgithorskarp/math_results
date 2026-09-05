# All overlaps of the mixed gadget at (7+i sqrt(15))/8

Every overlapping placement of
`B292 union (u V214+h)`, with `u=(7+i sqrt(15))/8` and
`B292=A159 union ((5+i sqrt(11))/6)A159`, is four-colourable.
All **62,488 translations** and all choices of source anchors are covered;
each graph has 505 vertices. Disjoint translations and other angles remain
outside this result. No five-chromatic graph or record improvement is found.

The [proof](PROOF.md) reduces strict cross edges to 66 exact difference
pairs, supplied in [contacts.tsv](contacts.tsv). There are at most six
new edges per placement. The inherited eight/seven-row colouring library
misses 82 cases. Two new colourings of each source cover every case.
The added positive certificate is 1,016 bytes.

An independent audit scans all **76,590,448** source-difference pairs by
modular Euclidean distance, then checks survivors with generic exact
radical arithmetic. It matches every contact pair, projected edge list,
and selected colouring. Two explicit 505-vertex former residuals also
receive full strict-distance checks on 254,520 point pairs in total.

## Reproduce

Use a full repository checkout and CPython 3.11.2 (standard library only).
From this directory, choose fresh output paths:

```sh
python3 census.py > /tmp/spindle-overlap-census.json
cmp expected.json /tmp/spindle-overlap-census.json
python3 audit.py > /tmp/spindle-overlap-audit.json
cmp expected_audit.json /tmp/spindle-overlap-audit.json
python3 controls.py > /tmp/spindle-overlap-controls.json
cmp expected_controls.json /tmp/spindle-overlap-controls.json
sha256sum -c SHA256SUMS
```

The census proves coverage using the explicit positive rows and finite
reduction. The audit provides a different exhaustive geometric computation;
it does not use the slope partition. All three commands fail on mismatched
certificates or failed checks. No solver, external service, numerical
precision choice, or large omitted certificate is needed for replay.

The source arrays and earlier colouring rows are reused from pinned sibling
packages. The producer imports exact integer source assembly; the audit
rebuilds it via the prior generic radical implementation. `SHA256SUMS`
includes all transitive source and data dependencies. Each complete
placement is assigned the lexicographically first source-row/permutation
triple that works; `expected.json` records its full stream hash and the
usage counts of selected triples.

The final serial replay took 1.156 seconds for the census, 20.440 seconds
for the independent audit, and 4.280 seconds for the full-geometry controls.
Maximum child peak RSS across the workflow was 37,644 KiB.

## Optional discovery reproduction

This is not required to check the theorem. With CPython 3.11.2 and
`python-sat==1.8.dev24` installed, use a new directory:

```sh
python3 discover.py --out /tmp/spindle-overlap-discovery
cmp new_B.txt /tmp/spindle-overlap-discovery/new_B.txt
cmp new_V.txt /tmp/spindle-overlap-discovery/new_V.txt
```

The generator checks placements in decreasing new-edge count, then anchor
order, and calls CaDiCaL195 only when the current library fails. It has a
20-query cap and a 200,000-conflict limit per query. The producing and
repeated runs each needed two satisfiable queries, at `(119,169)` and
`(79,167)`, and produced byte-identical positive rows. Timing fields vary.
`solver_provenance.json` records the producing versions, bounded settings,
CNF array hashes, and measured queries. A non-SAT answer would be saved
as an unresolved candidate and would not establish a negative result.

The [proof](PROOF.md) states the encoding and exact trust boundary. These
are author cross-checks; external mathematical review remains pending.
