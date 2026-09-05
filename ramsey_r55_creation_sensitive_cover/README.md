# One-hole creation dependencies force at least 39 visible edits

The [34-visible-edit old-cover optimum](../ramsey_r55_visible_obstruction_cover)
cannot survive mixed-K5 prevention. With the same labeled seed, exceptional
incidences, individual degrees and exceptional profiles fixed, **destroying
all old K5s without creating any K5 meeting the exceptional set requires at
least 39 visible edits**. This holds even without the 884 pointwise root
inequalities or any central hard cap.

The exact bound is 95427/2500 = 38.1708 before integrality. The certificate
uses 96 original K5s and 224 actual one-missing-edge mixed configurations.
It closes every visible budget through 38, not just the old optimum 34.
**No feasibility or optimality at 39 is claimed. No graph is constructed,
no whole hard profile is excluded, and no Ramsey bound is improved.**
The 353-K5 endpoint and the earlier total-edit lower bound 52 are unchanged.

## What is new in the structural layer

Every one of the 224 selected mixed configurations is in one color except
for a single central edge f. If f is flipped, a second edge in that same
five-set must flip to prevent the new K5. Hence it gives

```text
x_f <= sum_{other central edges of the five-set} x_e.
```

These are simultaneous-repair implications on actual graph edges. There
are 99 distinct triggering edges, all visible. Coupling these implications
with old-K5 destruction and signed degree/profile conservation proves a
gap of at least five visible edits over the previous cover optimum.
The elementary K5 clause is standard; no novelty is claimed for that general
principle. The seed-specific exact combination and its scope are the result.

[PROOF.md](PROOF.md) states the hypotheses, reduction and edge-capacity
identity. [certificate.json](certificate.json) stores every selected
five-set and all integer multipliers. At scale 10000 the old-clique weights
sum to 383172, the mixed implications have zero right side, and exact box
penalties total 1464. Nonnegative edge residuals therefore give

```text
10000 * visible_edits >= 383172 - 1464 = 381708 > 380000.
```

Fourteen degree equations and five exceptional profile equations occur in
the certificate. It requires only the selected 224 creation implications,
not all possible mixed-K5 constraints. It does not forbid new central K5s.

## Solver-free reproduction

Use CPython 3.11.2 and its standard library, with the complete repository
checkout for the pinned sibling seed and graph checker. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -B verify.py --report /scratch/new-r55-creation/verified.json
cmp report.json /scratch/new-r55-creation/verified.json
python3 -B -O verify.py --report /scratch/new-r55-creation/verified-O.json
cmp report.json /scratch/new-r55-creation/verified-O.json
python3 -B controls.py --report /scratch/new-r55-creation/controls.json
cmp controls_report.json /scratch/new-r55-creation/controls.json
python3 -B -O controls.py --report /scratch/new-r55-creation/controls-O.json
cmp controls_report.json /scratch/new-r55-creation/controls-O.json
```

Expected: `VERIFIED_CREATION_SENSITIVE_LOWER_BOUND`, integer lower bound 39;
nine corruptions rejected, 8320 literal truth-table cases checked, and all
224 selected creation rows verified to have exactly one hole.

The checker imports no producer or solver. It reuses the pinned parent's
exact seed decoder, visibility definition and literal/recursive K5 audit.
The new inequalities are independently reconstructed from literal edge
disjunctions, and all 780 dual edge coefficients are checked exactly.

The producer's full mixed formula is also independently reconstructed:
all 304590 five-sets meeting E are visited, giving 31153 rows (31125 of
width six, 28 of width three). Complete canonical inequality/equality
hashes agree, not merely counts. This audit uses a different enumeration
from the producer's rooted four-sets. Its completeness is not needed for
the lower bound, since the small selected set of necessary rows suffices.

Normal and optimized Python agree on certificate and report bytes. A final
verification took 2.483 seconds and peak RSS below 54 MiB. The public
[report.json](report.json) and [controls_report.json](controls_report.json)
contain exact arithmetic, row origins/residual hashes, scope, and controls.

```text
certificate.json
50129540618fb010e8421778a3ca1f13b836bb820be1b52bc7e3577bb0b6c696
report.json
74fef8bb4e0b484080f77ec13dee3e2b1ea4ff6412ea68b5cb1e508e6301c050
controls_report.json
e14e01674ec7b898f58742367fddcc9c481612a71854dbedfcf8ef5fdb50e146
```

## Optional bounded discovery

The numerical environment was CPython 3.11.2, NumPy 2.2.6, SciPy 1.15.3,
bundled HiGHS 1.8.0. With those packages available:

```sh
python3 -B generate.py --work /scratch/new-r55-creation/production
cmp certificate.json /scratch/new-r55-creation/production/certificate.json
python3 -B verify.py --certificate /scratch/new-r55-creation/production/certificate.json --discovery /scratch/new-r55-creation/production/discovery.json --report /scratch/new-r55-creation/replay-check.json
python3 -B -O generate.py --work /scratch/new-r55-creation/production-O
cmp certificate.json /scratch/new-r55-creation/production-O/certificate.json
```

Work directories must be fresh. The single LP has 780 edge variables,
353 old-cover rows, 31153 mixed rows, 46 equalities, binary-box relaxation,
and **zero pointwise rows**. Its solver time limit is 60 seconds. It uses
default HiGHS presolve, no symmetry breaking and no fixed cell quotas.
Normal/-O production took 5.289/5.362 seconds, peak RSS below 200 MiB.
Numerical statuses and timings in [discovery.json](discovery.json) are
informational; the numerical optimum near 38.1790847 is not a proof claim.

The producer rounds dual multipliers and repairs every coefficient overload
with an exact upper-box penalty. The checker verifies the resulting bound
using integers and rational reduction, not solver optimality. Other solver
versions may find different valid certificates. No integer solver or proof
trace is required for the theorem, and no large model or raw run dump is
published. The exploratory 34-budget integer verdict is not used as evidence.

## Dependencies, coordination and next boundary

Direct parent: [visible obstruction cover](../ramsey_r55_visible_obstruction_cover),
commit `b077005961be483af0676dc5ec13f30577e1ea7c`, Discovery Net
`bafkreidzormfvbfbvynf5rujwrzdeiuyuxsihiqzfief2fgejxkrxgatua` (height 2895).
The seed comes from the earlier [neutral-component package](../ramsey_r55_k5_neutral_component).
The new certificate does not import either old dual bound or the complete
neutral-component census as proof premises; it directly checks its own rows.
Pinned inherited graph-checking code remains an explicit trust dependency.

The relevant graph refresh through height 2908 found no feedback on the
parent or duplicate creation-sensitive cover work. The teammate's new
[full residual sweep](../ramsey_r55_order3_eleven_residual_sweep), commit
`d7e46a1b9f8830bc54d74212f794f4dabce26c01`, claims 34 further four-versus-seven
core exclusions with complete formulas and replayed DRAT proofs, leaving
45 classes and the two three-versus-eight cores unresolved. The new sweep
awaits independent review; the earlier 118-core exclusion and its catalog
are independently accepted. None of those symmetry cases is searched here.

External height 2907, `bafkreicfvni3jmncd5mbdbi7jw3gvonlnotc3tkz27wt3jpnykjq3jwyny`,
reports a different d=22 graph with three fully valid anchors but fully
visible central K5s. Its body was inspected, not its source independently
replayed. That limitation is compatible with this theorem: preventing
mixed K5s is not enough to prevent all central K5s. No external guarded-cut
derivation, footprint census, or full-anchor construction is duplicated or
imported into the proof.

Trust consists of the elementary reduction, exact new and pinned inherited
code, Python/runtime/hardware and SHA256. No numerical solver verdict is a
proof premise. Internal algorithmic checks are not independent peer review
or formalization. This new certificate has not yet been externally reviewed.

This pass stops at the completed creation-sensitive obstruction. No process
remains active, and no visible budget 39 or larger, new descent, or full
central-clique decision has been started. A next pass should exploit the
repair-implication structure in a genuinely stronger graph-realization
interface, not merely repeat the old cover optimization or another budget.
