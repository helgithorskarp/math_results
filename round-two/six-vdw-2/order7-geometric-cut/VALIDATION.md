# Validation record

Agent **six-vdw-2**, role **researcher**, 2026-10-01. Independent model
implementations and exact proof checking are by the same author; new
independent peer review is not claimed.

Complete fresh source regeneration returned
`EXACT_ORDER7_GEOMETRIC_AND_SIGN_PHASE_CUTS`, with
`family_exclusion=false`, in **148.844 seconds**. Peak child RSS was
83644 KiB; parent RSS 67476 KiB. Python 3.11.2, GCC 12.2.0,
`python-sat==1.8.dev24`, `six==1.17.0` and CaDiCaL195 were used.
All jobs ran serially, native threads one, within the standing one-CPU
and 2 GiB scope. No solver cap or resource limit was increased.

The unchanged-source `--resume` run also passed, in **157.689 seconds**.
It validates stored hashes, reuses complete proposal/conversion stages,
and reruns both exact mathematical audits, all 29 proof replays in both
Python modes, and all controls. Runtime variation reflects the shared
scope; resume success does not depend on a faster wall-clock time.

## Exact audits and coverage

The logarithm/spacing-one/scaling generator agrees with the independent
Euler-map/all-(a,d) auditor for all 31 run models, including the five
open models. Every one of the 380072 ordered field pairs is covered;
4312 zero-containing APs are removed and 375760 retained. The complete
support set has 26488 entries, ranks 5:88,6:5280,7:21120.
The `(418,2)` AP witness and all 88 actual scaled APs are checked.

The independent signed auditor explicitly forms H-cosets and their
negatives by multiplication, without generator or Euler-auditor import.
It reconstructs the three full signed clause sets from all field APs.
Two phase-zero QR positive controls satisfy all reconstructed field
clauses. Tiny signed words exhaustively check 1404 normalization
instances, covering color exchange and the exceptional-pair rotation.

Run-normalization controls check 4092 words of cycle lengths 2 through
11, including 10 alternating words, 4062 nonconstant nonalternating
normalizations, and 36868 window/maximum-run equivalences. The universal
coverage arguments in PROOF.md justify the actual 88/44-dimensional
reductions; these small controls supplement the proofs.

## Complete positive-RUP traces

The 26 run traces for L=7..32 total 108427 checked additions and 1576701
propagation hints. The three signed traces add 15246 additions and
173812 hints. **All 29 traces**, totaling **123673 additions and 1750513
hints**, passed normal and optimized Python replay. Every reference CNF
and proof hash matches the fresh run; per-case data are in expected.json.

| Signed profile | Phase weight K | Variables | Clauses | Conflicts | RUP additions | Hints |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| All opposed | 44 | 44 | 21121 | 9360 | 9738 | 115090 |
| One opposed pair | 1 | 44 | 29509 | 1625 | 2356 | 25702 |
| One agreed pair | 43 | 44 | 24595 | 2377 | 3152 | 33020 |

The hardest completed run model, L=7, used 40556 conflicts. These
complete proposals stayed within the 50000-conflict budget and external
30-second timeout. Converter limits are 25 seconds internal and 30
seconds external. The pinned official drat-trim source SHA is
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`
at commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
Only independent replay of the exact audited CNF is a proof premise;
the solver/converter success messages alone prove nothing.

## Rejection controls and open cases

All 256 subsets of the eight nonempty nontautological two-variable
clauses are classified by exhaustive truth assignments. The checker
accepts 161 valid UNSAT refutations and rejects 95 forged SAT proofs.

Ten run/proof production corruptions are rejected: unknown propagation
hint, unsupported negative RAT hint, out-of-domain literal, missing
terminator, absent empty conclusion, unknown deletion, omitted boundary,
reversed boundary color, replaced field clause and omitted cyclic window.
Four signed encoding corruptions are also rejected: reversed field
literal, omitted field clause, reversed color-normalization unit, and
a CNF paired with the wrong phase profile. These checks pass normal/-O.

An L=7 one-conflict control returns UNKNOWN without a trace. Initial
L=2..6 probes also return UNKNOWN at the recorded budget (50000 or
50001 accumulated conflicts under the solver's budget API). Those
five records in expected.json establish no exclusion. The default
reproduction does not propose proofs for them. An interrupted,
incomplete or budget-limited computation never counts as a refutation.

The new proof leaves the entire H7 classification unresolved and the
previous nonquadratic stabilizer bound seven unchanged. The stronger
nonquadratic phase band imports the explicitly cited order>=11 theorem
only to classify phase weight zero. Generated CNFs, proof traces and
binaries are scratch artifacts and are not published.
