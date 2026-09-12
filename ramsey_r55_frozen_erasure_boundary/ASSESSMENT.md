# Scope and failure boundary of the proposed approach

The objective was a candidate-invariant compression of all good43 graphs,
using forced recolorings rather than changing maximal K4 packings. Two
different obligations arise: finding many frozen pairs, and reconstructing
their erased colors without circular dependencies. Counting addresses
only the first obligation.

## What the primary results actually imply

Let `F_R` and `F_B` be the graphs of frozen pairs currently colored red and
blue, respectively, and let `F=F_R union F_B`. The primary results

- [Angeltveit, 2026, R(K5,K5-e)=30](https://arxiv.org/html/2602.11459v1), and
- [Radziszowski, 1993, R(K5-e,K5-e)=22](https://www.cs.rit.edu/~spr/PUBL/paper20.pdf)

give, for any good43,

```
alpha(F_R) <= 29, alpha(F_B) <= 29, alpha(F) <= 21.
```

For example, an independent 30-set in `F_B` cannot contain a red K5-e:
its missing blue pair would be frozen. It cannot contain a blue K5
because the whole graph is good. The asymmetric Ramsey bound excludes
that 30-set. Interchanging colors gives the other bound. An independent
22-set in `F` would avoid K5-e in both colors, contradicting the second
bound. Equivalently the respective vertex-cover lower bounds are 14, 14,
and 22. These are straightforward corollaries of imported theorems, not
new Ramsey-number results. Their literature trust is separate from the
fully explicit erasure counterexample, which does not use them.

## Why these three bounds do not compress the fixed-core carrier

For an original q8 task, let `D_R,D_B` consist of the prescribed red and
blue pairs in its eight four-clique blocks and its fixed order-11 core.
Every order-11 (4,4) core has clique number and independence number both
three: each is at most three by definition, and a missing triangle in
one color would contradict the elementary bound R(3,4)<=9.

If r blocks are red and 8-r are blue, disjoint-component addition gives

```
alpha(D_R) = 35-3r,
alpha(D_B) = 11+3r,
alpha(D_R union D_B) = 9.
```

| r | alpha(D_R) | alpha(D_B) | Free blue frozen pairs forced by these bounds |
|---|---:|---:|---:|
| 5 | 20 | 26 | 0 |
| 6 | 17 | 29 | 0 |
| 7 | 14 | 32 | at least 3 |
| 8 | 11 | 35 | at least 6 |

Adding one edge lowers independence number by at most one, which proves
the last column. For r=5 and r=6, marking all prescribed pairs frozen and
all free pairs nonfrozen satisfies these three numerical inequalities.
This is a witness for that weakened mask system only: it is **not** a
physical graph with verified witnesses, a good43, or a proof that the full
frozen-edge constraints have no effect. The calculation is uniform over
all 546356 order-11 cores, rather than a test on selected core records.

The four broader physical bases `M_r` used by R2 have 55 *variable* core
pairs. They must not be confused with original fixed-core tasks. Before
cohort assumptions, the same argument gives at least `3r-10`, namely
5, 8, 11, and 14, blue frozen **physical** variables in the four bases.
A particular cohort fixes additional core pairs, which can absorb some
of that lower bound. No cohort constraint was added, no queue was run,
and no per-cohort or original-task reduction is claimed here. The
numbers above are counts of frozen variables, not counts of independent
decisions saved, guaranteed runtime factors, or omitted carrier codes.

The carrier definitions are the published
[maximal-packing proof](../ramsey_r55_global_maximal_packing/PROOF.md) and
[physical q8 proof](../ramsey_r55_q8_assumption_queue/PROOF.md).
The original catalog's completeness and the R(4,5) bound underlying global
coverage remain their external trust boundaries. Nothing here strengthens
or reruns those dependencies.

## Trial assessment

The explicit collision rejects reconstruction from the frozen mask,
nonfrozen colors, and degrees alone. The incidence corollaries do not
provide a substitute decoder or an independently bounded amount of seed
information. An acyclic witness/seed theorem could repair the route, but
no such all-good43 theorem or quantified complete-carrier saving was
established in this pass.

Accordingly the first new-approach gate is **not met**. This is a failed
approach checkpoint, not a successful structural milestone. A second
pass would need a fundamentally stronger reconstruction argument and
actual complete-carrier leverage; repeating the incidence bounds or
extending collision tables would not meet the mandate. Structural-lane
reassignment within R(5,5) is recommended for orchestrator assessment.
This recommendation does not assert that every frozen-edge approach is
impossible or that the order-43-specific premise has been disproved.

Preserve the earlier all-good43 core-exchange normal form, mixed-q7
redirect, all original accepted decisions, and R2's subsequent source
certificates. No old verdict, receiver, queue, or pending transaction is
modified by this negative result.
