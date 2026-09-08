# Shared triangle interfaces for the complete maximal-packing cover

This package replaces every width-9 or width-10 monochromatic-five clause in
the 2,189,178 physical tasks of the [h3873 maximal-packing cover](../ramsey_r55_global_maximal_packing)
by an exact shared triangle conjunction. It applies to all 18 macro classes
and every catalog core. It fixes no physical edge and removes no physical
graph.

The [proof](PROOF.md) establishes projection equivalence, exact all-task
counts, and preservation of unit-propagation inferences on the physical edge
variables. Maximum clause width falls from 10 to 8. Literal occurrences fall
by an exact amount determined only by q:

| K4 blocks q | Core order | Triangle variables | Saved literals per task |
|---:|---:|---:|---:|
| 7 | 15 | 5,500 | 1,017,596 |
| 8 | 11 | 6,952 | 1,437,800 |
| 9 | 7 | 9,268 | 1,808,660 |
| 10 | 3 | 12,768 | 2,004,960 |

This supplies an encoding-level tractability signal: all long target clauses
are eliminated, the representative formulas use 12.56%–15.54% fewer literal
occurrences, and every inference of a replaced direct clause survives unit
propagation after projection. The price is one easy-to-define auxiliary per
shared triangle and 2.15%–3.64% more clauses in the audited representatives.
These statements do not assert a measured solver speedup.

One complete formula from each `(q,r)` macro class was reconstructed twice,
once through the producer and once through an independent graph6 and physical-
edge implementation. All 22,158,012 factored clauses matched literal by
literal. Across those 18 formulas, the baseline had 202,933,250 literal
occurrences and the factored encoding has 173,056,202, a reduction of
29,877,048. [REPRESENTATIVE_AUDIT.json](REPRESENTATIVE_AUDIT.json) records each
formula's dimensions and virtual DIMACS hash.

The first task was also written as a real 34,089,094-byte DIMACS file and read
against the independent stream. It has 6,257 variables, 892,626 clauses and
SHA-256:

```text
a03d111e64fccdcd92bde61f2e7bcd962ebe94578781c8ab95f92611c726fb57
```

The file is omitted under the repository's large-file boundary; its compact
receipt is [FORMULA_CHECK.json](FORMULA_CHECK.json). All generated formulas,
catalog copies and runtime output remain outside GitHub.

Run the compact source, arithmetic and 78,732 partial-assignment propagation
checks with Python 3.11.2 and the standard library:

```bash
python3 -B ramsey_r55_triangle_interface/reproduce.py
python3 -O -B ramsey_r55_triangle_interface/reproduce.py
```

To rerun full physical literal audits, first reproduce the pinned h3873 data
cache as documented by its sibling package, then split the 18 representatives:

```bash
python3 -B ramsey_r55_triangle_interface/reproduce.py --cache /tmp/mp1-data --shard 0 --shards 3
python3 -B ramsey_r55_triangle_interface/reproduce.py --cache /tmp/mp1-data --shard 1 --shards 3
python3 -B ramsey_r55_triangle_interface/reproduce.py --cache /tmp/mp1-data --shard 2 --shards 3
```

Generate the checked first formula and independently reread its bytes:

```bash
python3 -B ramsey_r55_triangle_interface/factor.py /tmp/mp1-data \
  --task mp1-q7-r5-c000000 --cnf /tmp/mp1-triangle.cnf
python3 -B ramsey_r55_triangle_interface/check_formula.py /tmp/mp1-data \
  --task mp1-q7-r5-c000000 --cnf /tmp/mp1-triangle.cnf
```

Default and audit reproduction make **zero solver calls**. The orchestrator's
prior UNKNOWN boundaries are unchanged, and no fourth raw target call was
made. Every h3873 task remains undecided. No good43 or Ramsey-bound improvement
is established.

`verify_model.py` requires a complete factored SAT assignment, checks every
clause, restores the physical graph, verifies maximal-packing membership and
red maximality, then checks all 962,598 five-subsets. It can write both the
43-vertex hexadecimal graph and a compact red-edge list only after those
checks. No model passed because no solver was invoked.

Global coverage inherits h3873's catalog-completeness premise. The encoding
equivalence itself does not. h3873 source commit is
`1884881efbf52a54bd3a30b1445c211da7caec27`; its external review was pending at
the recorded graph cutoff. This result is checked finite mathematics, not a
proof-assistant formalization, and claims no historical novelty for Tseitin
conjunctions or shared clique indicators.
