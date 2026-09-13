# The 574-point sealed-pool obstruction is vertex-critical

The exact 574-point, 2,707-edge five-chromatic plane unit-distance graph in
[`hadwiger_nelson_parts509_pool_obstruction574`](../hadwiger_nelson_parts509_pool_obstruction574/README.md)
has no smaller non-four-colourable induced subgraph. More precisely, deleting
any one of its 574 vertices leaves a graph with a supplied proper
four-colouring.

The parent package already supplies and checks the 200 deletion colourings for
its selected pool vertices. A separate earlier
[`subgraph closure`](../hadwiger_nelson_parts509_obstruction574_subgraph_closure/README.md)
covered L labels 0 through 308, which was already enough to prove that every
subgraph through order 508 is four-colourable. This package rechecks those 309
rows in one uniform encoding and adds the remaining 65 L labels. Since every
proper vertex subset omits some vertex, restriction of the corresponding
colouring now proves the claim for every proper induced subgraph.

This strengthens that seed-specific closure to full vertex-criticality, but it
does not improve the record consequence already obtained from the first 309 L
rows. It is not a sub-509 construction, a global plane-colouring bound, or a
lower bound for another family. The exact graph remains 65 vertices above the
509-point record. Adding new points or changing coordinates is outside the
result.

## Exact and chromatic checks

The standard-library verifier imports the parent's hash-pinned exact integer
geometry reader. It reconstructs 574 distinct points and all 2,707 strict unit
edges, rechecks the parent's proper five-colouring and 200 pool-deletion
colourings, and checks 1,008,663 edge inequalities in the 374 new L-deletion
words:

```sh
python3 -B hadwiger_nelson_parts574_l_indispensability/verify.py
python3 -O -B hadwiger_nelson_parts574_l_indispensability/verify.py
python3 -B hadwiger_nelson_parts574_l_indispensability/controls.py
```

The first two commands must report
`ALL_574_SINGLE_VERTEX_DELETIONS_HAVE_CHECKED_4_COLOURINGS`; the controls must
reject a missing row, nonzero packed padding, and a monochromatic edge.

Non-four-colourability is inherited from the identical parent graph, whose
ordinary four-colouring CNF has 2,296 variables and 11,405 clauses. Its
regenerable DRAT proof was independently rechecked for this package; the
regenerated proof had the already published SHA-256
`850de177b0550c43fd65817356bffca1f0680ad4d4ef9dadce25cf35348b520a`.
To repeat the negative check without keeping the 7.3 MB proof in Git:

```sh
python3 -B hadwiger_nelson_parts509_pool_obstruction574/verify.py \
  --cnf /tmp/parts574.cnf
/path/to/kissat --time=300 /tmp/parts574.cnf /tmp/parts574.drat
python3 -B hadwiger_nelson_parts574_l_indispensability/verify.py \
  --proof /tmp/parts574.drat --drat-trim /path/to/drat-trim
```

The final status is `VERIFIED_574_VERTEX_CRITICAL_UNIT_DISTANCE_GRAPH`.

## Construction search and stopping boundary

[`search.py`](search.py) uses one full-graph activation encoding and CaDiCaL
1.9.5 through python-sat. It tried all 374 L deletions in 143.76 wall seconds
(142.75 cumulative native solver seconds). Every SAT model was decoded and
checked against the exact edge set before packing; the verifier, not the SAT
search, is trusted for the positive theorem.

The owner-defined success condition was a non-four-colourable activation core
of order at most 508. No single deletion was even possible, so this seed is
closed rather than widened into routine minimization. A successor construction
must alter the graph before descent; merely choosing a proper subset cannot
succeed.

The unrestricted comparison remains Jaan Parts's 509-point graph
([arXiv:2010.12665](https://arxiv.org/abs/2010.12665)). Haugland's 2,131-point
construction imposes the separate Moser-spindle-free restriction
([arXiv:2608.04542](https://arxiv.org/abs/2608.04542)).
