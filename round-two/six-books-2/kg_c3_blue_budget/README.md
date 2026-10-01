# Cyclic KG(7,2) blue-deletion budget

six-books-2, researcher; ordinary R(B4,B7),2026-10-01.

[PROOF.md](PROOF.md) gives a standalone construction theorem: after one/two
original KG blue edge orbits are promoted, blue B7 avoidance permits at most
three/five original red orbit deletions. The action is(012)(345) on the ground
set, with one added fixed vertex of red degree nine. Both blue-only budgets
are attained. The sharp controls have red B4s and are not Ramsey witnesses.

Using explicitly credited earlier degree/edge results, any ordinary22 witness
of C3 cycle type3^7 1 must therefore promote at least three KG blue orbits and
recolor at least30/33 of its original210 edge colors at102/99 red edges.
Three-or-more promotions and the unrestricted Ramsey gap remain open.

## Fresh reproduction

Python3.11+, g++ with C++17, no third-party packages, solver, network download,
proof corpus or previously generated checkpoint is required. From repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 round-two/six-books-2/kg_c3_blue_budget/reproduce.py \
  --work scratch/kg-c3-blue-budget
```

Choose an empty --work directory. The runner compiles the independent program,
regenerates all producer/native records, checks complete coverage and entrywise
pool/pair equality, and compares the entire result with the pre-existing frozen
expected.json. It runs exact controls normally and with python -O. All jobs are
serial, all thread variables are one, and every mathematical case phase has a
30-second budget. Timings are separate from deterministic evidence. No timeout
or incomplete phase means mathematical absence.

The independent program tests **139502 four-subsets and128917750 six-subsets**
over **1225 and20825 labeled cases**. It uses neither the producer's symmetry
quotient nor its pair/clique pruning. The producer needs only3/973 critical
cliques; a different maximal-clique algorithm independently rebuilds those covers.
All source, frozen evidence and control inputs are compact; the generated records
and executable stay local. This is same-author algorithm independence, not
external peer review or a proof-assistant theorem.

To resume complete case phases explicitly:

```sh
python3 round-two/six-books-2/kg_c3_blue_budget/reproduce.py \
  --work scratch/kg-c3-blue-budget --resume
```

Source hashes must be unchanged. All cached records are checked again against
the complete independent census and frozen evidence. A killed/incomplete phase
without its final boundary metadata is rejected; preserve it and use a fresh
directory rather than interpreting the prefix as a proof. No resource escalation
is needed. --generate-expected is only the initial fixture-generation operation;
it cannot replace an existing fixture and does not report fixture agreement.

Files: model.py defines the ground construction and checked centralizer;
prove.py builds the finite certificate; independent.cpp covers every labeled raw
subset; check.py verifies transport, clique completeness, literal pages and
damages; reproduce.py runs serial bounded phases. expected.json freezes the
full deterministic result; primary21.rows is the known21-vertex control, whose
source/hash/normalization and primary references are given in PROOF.md.
