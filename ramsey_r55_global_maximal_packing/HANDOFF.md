# Physical task interface for team-r55-1

All tasks are undecided. This package runs no target solver. The exact
identities and disjoint carrier intervals of every task are given compactly
by `TASKS.json` and the constructor in `family.py`.

A task ID is `mp1-qQ-rR-cCCCCCC`, with q in 7..10, r in 5..q, and a
zero-based six-digit core index in the relevant pinned catalog. All indices
in each half-open range are included. A single core's failure cannot exclude
its macro class. No old UNKNOWN or UNSAT transfers automatically to this
new labeling family.

The least carrier class is q=7,r=5: 640 tasks, each below 2^704 codes.
This is an exact carrier-size ordering, not an empirical solver ranking.
For example, generate the first complete task and independently check it:

```bash
python3 -B ramsey_r55_global_maximal_packing/family.py /tmp/mp1-data --task mp1-q7-r5-c000000 --cnf /tmp/mp1-first.cnf
python3 -B ramsey_r55_global_maximal_packing/audit.py --cache /tmp/mp1-data --task mp1-q7-r5-c000000 --cnf /tmp/mp1-first.cnf
```

Its formula has 757 DIMACS variables, 756 physical edge variables, and
873,566 clauses including 1,216 whole-union red-maximality clauses. Consult
`FORMULA_AUDIT.json` for the frozen hash and byte size. Variable 1 is forced
true. The other variables are all non-fixed unordered physical edges in
lexicographic order. The fixed core and four-clique edges are restored by
the decoder.

Within Python, `Task(name, cache).unrank(code)` produces a carrier graph;
`.rank(graph)` checks and recovers its unique local code. `locate(index)`
and `global_index(name,local)` map to and from the complete registry's
integer intervals. `--code` deliberately labels its output as a carrier,
not a target. The carrier can fail global closure or remaining five-sets.

A complete SAT model can be submitted to the physical target decoder:

```bash
python3 -B ramsey_r55_global_maximal_packing/family.py /tmp/mp1-data --task mp1-q7-r5-c000000 --sat /tmp/mp1-first.model
```

This requires exactly `s SATISFIABLE`, a complete nonconflicting assignment
including the true constant, matching pair/star/root/fixed conditions and
red maximality, and zero monochromatic fives in a literal physical43 check.
UNKNOWN, UNSAT, partial assignments, or a carrier graph are never accepted
as target certificates. A future UNSAT claim requires an independently
checked complete proof for the exact CNF; no such proof is supplied here.

`transport(graph, permutation, task)` checks a supplied new-label-to-old-label
43-vertex isomorphism certificate, carrier membership and red maximality.
It does not search the complete catalog for an isomorphism and does not
certify the input graph as a target. Catalog normalization is justified by
the coverage proof and imported catalog completeness.

For a shared immutable snapshot, keep future solver inputs, outputs and
decision manifests outside it. Its public source commit, manifest digest,
Discovery Net reference and receiving-directory replay are recorded in the
separate shared delivery receipt. This source handoff remains content-stable.
