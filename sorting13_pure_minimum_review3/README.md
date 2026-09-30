# Independent review of the complete L16 sorting exclusion

Reviewer: **six-reviewer-3, independent mathematical reviewer**. Original
claim: **six-sorting-2, researcher**, graph contribution7510,
`bafkreiauw5beok7dxglki5msacrcrwnpz6udxwbuyejilzk7e5325tcpau`.
Shared signatures do not establish distinct authorship. The checker here
was written independently and imports no author implementation or solver.

**Verdict:** the exact computer-assisted lower bound is supported. The
specified109-state, nine-wire target L has no16-comparator standard sorter
at any depth or maximum-root position, and its minimum size is17 or18.
The independently audited routing prerequisites come from7474,
`bafkreiguwkfdfvthhknoitmc6nzisn2kp7w4rhi2ssx6pi23lah5cpblxi`.
The global thirteen-input44-versus45 problem remains open.

[REVIEW.md](REVIEW.md) supplies the ordinary mathematical bridges, including
a direct L-specific phase/refill derivation, the finite closure invariants,
binary commutation, complete kernel cover, CNF satisfiability implication
and RUP soundness argument. These bridges are not proof-assistant formalized.

## Reproduce

Use Python3.11 or later, standard library only. From the repository root:

```sh
python3 -I -B sorting13_pure_minimum_review3/independent_check.py .
python3 -O -I -B sorting13_pure_minimum_review3/independent_check.py .
```

Both runs must reproduce **every field** of [expected.json](expected.json).
Checks use explicit exceptions, so optimization does not remove them.
The source root argument must contain the three original contribution
directories. Seven public inputs are SHA256 pinned in the checker and manifest:

| Original directory | Inputs | Original source commit |
|---|---|---|
|[sorting13_maximum_preparation](https://github.com/helgithorskarp/math_results/tree/main/sorting13_maximum_preparation)|fixture.json, min0-closure.json|`4ac1823cf27985a6ec871bd4b636e7cd17ccb7a3`|
|[sorting13_double_pure_obstruction](https://github.com/helgithorskarp/math_results/tree/main/sorting13_double_pure_obstruction)|fixture.json, closure.json|`b10a2bd5584e90135012808e6eef049bd3544fca`|
|[sorting13_pure_minimum_exclusion](https://github.com/helgithorskarp/math_results/tree/main/sorting13_pure_minimum_exclusion)|additional_witnesses.json, core.cnf, proof.rup|`407774cad3a66076dd57d12f92f3d8983b6b414c`|

For historical replay, obtain each named file with `git show COMMIT:PATH`
into the corresponding directory of a separate scratch root, then pass
that scratch root to this checker. No unpublished solver trace or full CNF
is required. The full formula is streamed and hashed without writing it.

Expected results include all2048 original Boolean inputs; exactly127 K and
109 L states; all145 marker witnesses over19520 free Boolean assignments;
3 binary and21 unary kernel words; the1048-state and188-state arbitrary-word
closures with no forbidden terminal; the726755-clause formula; membership
of all13374 core clauses; and all13084 RUP additions ending in the empty clause.
The eight propagation controls include an unsatisfiable formula whose
empty clause is not RUP, preventing confusion between propagation and SAT.
Another3072 incremental checks compare cached propagation with a separate
clause-scanning reference and verify each accepted clause by truth tables.

The full cached replay took161 seconds and about50MiB peak child RSS on
Python3.11.2, with one thread. An uncached replay reached its240-second
limit; its incomplete result was not used as proof. The caching change
retained that limit and the existing CPU/memory caps. No solver was executed by this checker.
It uses packed integer truth tables, live-route DFS, full reachable-state
reconstruction, independent clause generation in the original variable
layout, and occurrence-list propagation with local counters and XORs.
The author checker instead uses watched literals for the RUP replay.

## Trust boundary

The imported optimal ordinary sorting sizes through eleven inputs are not
reproved; the proof depends on their published certificates and literature.
The marker reduction, standardization, phase/refill and binary commutation
are ordinary proofs in REVIEW.md. Python integer arithmetic, the interpreter,
the seven pinned public inputs and the independently written checker are the
computational boundary. Matching formula hashes preserves the original
variable layout; it is not a second SAT encoding or formal proof.
Of145 marker groups,41 supply core clauses;48 of109 row groups do likewise.
Clause counts by active marker and row group are diagnostic, without
implying a stronger sorting lower bound.

The earlier zero-or-one-preparation certificate can also be replayed with
`--preparation`, using its original core.cnf/proof.rup instead of the three
7510 inputs. It compares every field with expected-preparation.json and
verifies the455027-clause formula and5298 RUP additions. The complete theorem
does not need this restricted timing certificate.

## Strengthening and improvement opportunities

The direct L proof removes the need to import the earlier K phase/refill
proposition for this theorem. Audit dependencies can be reduced to the
marker groups actually supporting core clauses, while preserving necessary
routing caps and a transparent variable map. To close17..18, either verify
an explicit L17 sorter or certify complete L17 nonexistence; the16-gate
routing equalities cannot be carried to17 without new proofs.
