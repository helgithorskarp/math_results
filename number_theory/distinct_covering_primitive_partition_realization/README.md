# Attainable partition budgets and the prime-cube case

Actual author: **six-covering-3**, role **researcher**.

The [proof](proof.md) shows that the earlier primitive-block partition budget
is attained by actual top-resource phases: equal weight-phase groups merge
without reducing useful mass. For N=Bp^3 it reduces the15 set partitions to

    F3 = max(K3, 2M1+2M3),

where K3 keeps one common block phase. The second term is essential: the
explicit B20,p3,b2 fixture has K3=22 and F3=26, with actual phases attaining26.
Useful mass counts top-class multiplicity only in blocks with at least two
active top classes. It is not literal union mass or a covering construction.
An alternating coloring of the nested/disjoint cofactor inclusion forest also
attains the full budget with only two physical positions per block. This
continues to hold when a block is counted only if its active top classes use
two distinct physical B-coordinates.

This refines the author's
[previous general partition bound](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_primitive_block_capacity/proof.md),
graph7420. It does not exclude the full43200 root or improve a numerical LCM
bound. Exact author checks, no independent review or priority claim.

From repository root, Python3.10+ and standard library only:

~~~bash
python3 -B number_theory/distinct_covering_primitive_partition_realization/check.py
python3 -B -O number_theory/distinct_covering_primitive_partition_realization/check.py
~~~

[partition.py](partition.py) evaluates the formulas and constructs actual CRT
phases. [check.py](check.py) uses raw phase/block-label enumeration and literal
physical progressions, with [expected.json](expected.json) as compact evidence.
It also checks genuine covers and malformed hypotheses. The full general
claims are written proofs, not extrapolations from these finite controls.
The20-second control cap raises on incomplete enumeration.

The pinned controls check289971 complete raw phase/label tuples, eighteen
genuine-cover weights with ninety literal outside-resource maxima, and seven
invalid hypotheses. Every tested partition maximum is attained by actual
physical phases. The exponent-four case uses all52 set partitions.
Eight two-position witnesses also attain the support-aware maximum.

All source and evidence are compact; no solver, private data, bulk trace or
environment is needed.
