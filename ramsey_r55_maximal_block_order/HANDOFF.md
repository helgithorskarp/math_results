# Complete ordered tasks for team-r55-1

All tasks remain undecided. The exact joint carrier is below 2^759 and more
than 1,939 times smaller than the h3873 carrier. This is a reduction in
labeled carrier size, not a solver-time estimate. The construction preserves
satisfiability task by task and includes every parent core index.

`bo1-qQ-rR-cCCCCCC` corresponds to `mp1-qQ-rR-cCCCCCC`, with precisely the
parent ranges. `TASKS.json` supplies all 18 macro classes, full core-index
ranges, exact per-task counts and disjoint global intervals. It avoids a dump
of 2,189,178 separate JSON task rows.

The smallest carrier class is q=7,r=7, containing 640 tasks below 2^695 codes
each. A complete instance from that class is included in `FORMULAS.json`.
To generate and audit its triangle form from the pinned checkout:

```bash
python3 -B ramsey_r55_maximal_block_order/ordered.py /tmp/bo1-data --task bo1-q7-r7-c000000 --triangles --cnf /tmp/bo1-first.cnf
python3 -B ramsey_r55_maximal_block_order/check_order.py --cache /tmp/bo1-data --task bo1-q7-r7-c000000 --triangles --cnf /tmp/bo1-first.cnf
```

In Python, with the package on the module path:

```python
import check_order
receipt = check_order.audit_file(
    'bo1-q7-r7-c000000', '/tmp/bo1-data', '/tmp/bo1-first.cnf', triangles=True)
```


The frozen smallest-class triangle example has 6,332 total variables, 756
physical edge variables, 905,265 clauses and 35,194,411 bytes. Its SHA-256 is
`899f8492e9806bc87ed71296a9aca8d52b63f3cfaa4eaa0e1bf17b0ac945664a`.
The 75 new prefix variables account for 455 ordering clauses; maximum width
remains eight. See FORMULAS.json for the other complete instances.

Omit `--triangles` to produce the direct physical encoding. The physical
variable map, fixed core and all parent clauses are retained. Triangle
variables, when used, keep the h3881 numbering. Prefix variables are appended
strictly after the selected base encoding. Variable 1 remains forced true.
Each adjacent same-color nonroot block comparison uses 15 prefix variables
and 91 clauses. Comparing the whole unsigned 16-bit matrix, rather than only
one column, is required by this interface's exact count.

`carrier.Carrier(name,cache)` exposes `unrank(index)`, `rank(graph)` and
`normalize(parent_graph)`. The latter returns the complete physical graph,
its new code, and a new-label-to-old-label permutation; it preserves all
fixed core labels and checks maximality preservation. It requires parent
carrier membership and does not claim that a returned graph is a target.
Tied root matrices remain allowed and are counted exactly.

`carrier.locate(global_index)` and `carrier.global_index(name,local)` transport
codes through the complete registry. Codes can violate maximality and the
remaining five-set clauses even when their pair/star/root conditions hold.

For a SAT claim, use the exact full-model decoder:

```bash
python3 -B ramsey_r55_maximal_block_order/ordered.py /tmp/bo1-data --task bo1-q7-r7-c000000 --triangles --sat /tmp/bo1-first.model
```

It requires an exact SATISFIABLE status, a complete nonconflicting assignment
including every auxiliary, all clauses satisfied, ordered carrier membership,
and an independent literal physical43 check of every five-subset. UNKNOWN,
partial models, a carrier, or a transport certificate cannot establish the
target. A future UNSAT requires a checked complete proof for the exact CNF.
Because the normalization preserves each task, an UNSAT decision of its
ordered formula would decide that parent task; no such decision exists here.

The accompanying shared snapshot pins all four source packages and the four
catalogs. Keep fresh formulas and solver receipts outside the snapshot.
Its manifest, source commit, graph reference and receiving replay are recorded
in the separate immutable delivery receipt. No physical solver call is part
of this milestone; the choice and gate for a physical decision remain yours.
