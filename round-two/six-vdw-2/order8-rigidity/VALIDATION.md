# Validation record

Agent **six-vdw-2**, role **researcher**, 2026-10-01. The record describes
same-author independent encoding and proof-checking implementations;
independent peer review is a separate process.

The complete fresh source regeneration returned
`EXACT_ORDER8_PUNCTURED_FIELD_EXCLUSION` in **70.073 seconds**, with
76020 KiB peak child RSS and 60976 KiB parent RSS. Python 3.11.2,
GCC 12.2.0, `python-sat==1.8.dev24`, `six==1.17.0` and CaDiCaL195
were used. Every stage ran serially with the native thread environment
set to one. The measured solver cases stayed below the specified
50000-conflict and 30-second external budgets.

The unchanged-source `--resume` run also passed, in **51.003 seconds**.
It verified checkpoint hashes, reused complete proposal/conversion
stages, and reran the mathematical audits, seventeen exact proof replays
in both Python modes, corruption controls, and incomplete-solver control.

The first packaged harness attempt stopped on comparison of Python
integer dictionary keys with JSON string dictionary keys. The final
harness normalizes through JSON before comparing. A separate proof-result
comparison ignores the CLI's extra elapsed-time field while comparing
every mathematical result field. The final full run passed; no failed
harness or interrupted run is counted as an exclusion.

## Definition-level coverage

The generator's discrete-log/spacing-one/scaling constraints agree with
the auditor's independent Euler-quotient enumeration of **all 380072
ordered field pairs (a,d), d!=0**. The auditor removes exactly 4312
zero-containing APs and retains 375760. Complete clause-multiset equality
is checked for every one of the seventeen case CNFs, in normal and
optimized Python. There are 23177 distinct field supports, with ranks
4:77, 5:231, 6:4543 and 7:18326.

The explicit AP `(a,d)=(3,34)` gives support `{0,1,2,8,18}`. All 77
scaled ordered APs are checked from field arithmetic. Exhaustive small
odd cycles of lengths 3,5,7,9,11 check 2728 words, 2718 nonconstant
normalizations, and 25488 independent window/maximum-run equivalences.
These controls supplement the universal coverage argument in PROOF.md;
they are not a substitute for it.

## Seventeen exact refutations

Each case has 77 variables and `46510+L` initial clauses. The strict
checker accepts only positive-RUP additions with a checked empty clause.
All cases passed normal and `python -O` replay. The unchanged reused
checker hash, all CNF hashes, reference proof hashes and per-case counts
are in expected.json. All reference proof bytes matched the fresh run.

| Longest run L | Solver conflicts | Checked additions | Propagation hints |
| --- | ---: | ---: | ---: |
| 2 | 15731 | 17947 | 279401 |
| 3 | 34352 | 34688 | 525741 |
| 4 | 15574 | 18585 | 260198 |
| 5 | 6215 | 8106 | 110885 |
| 6 | 2539 | 3969 | 50950 |
| 7 | 1614 | 2602 | 32509 |
| 8 | 1109 | 1825 | 21881 |
| 9 | 354 | 508 | 9729 |
| 10 | 111 | 109 | 3324 |
| 11 | 49 | 43 | 1230 |
| 12 | 33 | 32 | 937 |
| 13 | 10 | 9 | 281 |
| 14 | 3 | 2 | 75 |
| 15 | 1 | 1 | 33 |
| 16 | 1 | 1 | 27 |
| 17 | 1 | 1 | 17 |
| 18 | 1 | 1 | 24 |
| **Total** | | **88429** | **1297242** |

The pinned converter is the official drat-trim source at Git commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, SHA256
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`.
Neither its `s VERIFIED` nor the solver's UNSAT response is a premise
of the lemma: the independent RUP induction establishes each refutation.

## Rejection and incomplete controls

All 256 subsets of the eight nonempty nontautological clauses on two
variables are classified by exhaustive truth assignments. The checker
accepts a RUP refutation for each of the 161 UNSAT formulas and rejects
a forged empty-clause proof for each of the 95 SAT formulas.

Ten deliberately corrupted production inputs are rejected: unknown
propagation hint, unsupported negative RAT hint, out-of-domain literal,
missing terminator, absent empty conclusion, unknown deletion, omitted
normalization boundary, reversed boundary color, replaced field-AP
clause, and omitted cyclic-window clause. These controls pass both normal
and optimized Python. CNF-corruption rejection uses the complete
definition-level auditor rather than assuming a corrupted formula must
be satisfiable.

The one-conflict L=3 control returns **UNKNOWN**, with no proof trace.
It contributes no exclusion. Only a complete audited seventeen-case
cover and seventeen verified empty-clause conclusions establish the
order-eight theorem. Generated trace corpora and binaries are scratch
outputs and are excluded from publication.
