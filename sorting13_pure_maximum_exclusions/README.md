# Certified exclusions of three pure maximum kernels

**six-sorting-2 (researcher)** proves that three nine-wire Boolean targets with81/82/80 states each require at least15 comparators, with no restriction on parallel depth. The targets arise from the binary-only maximum kernels of a conditional127-state ten-wire target K. Therefore every18-comparator sorter of K, if one exists, has at least one unary maximum-kernel gate.

This advances a conditional route inside the136-state X/10 frontier. It does not prove K needs19, X needs22, or thirteen inputs need45. Unary-containing kernels and other X branches remain open. See [PROOF.md](PROOF.md) for the closed-subset reduction, complete binary-kernel classification, pruning witnesses, route bridge and certificate semantics.

The principal lower bounds now also have an **elementary proof independent of SAT**: two mixed witnesses force a unique gate on the final wire and at most two moving-threshold passages, while a terminal-reset argument requires three. The simpler proof was motivated by [six-reviewer-2's independent Y2 review](../sorting_networks/thirteen_endpoint_review2), source `8b85203e6c3b3c248ae011ac12379d6384a519c7`. That review concerns the complementary researcher's result, not this theorem. The RUP certificates provide a separate corroborating proof.

| Target | States | Checked size interval | Full CNF variables / clauses | Core clauses | RUP additions |
|---|---:|---:|---:|---:|---:|
| J0 |81|15..19|13,909 /291,098|2,202|611|
| J1 |82|15..19|14,000 /293,358|2,738|1,034|
| J2 |80|15..20|13,779 /288,742|2,531|853|

The encoding uses14 sequential comparator slots, all36 comparator types, and every Boolean row. It imposes exact execution, selected independently audited pruning bounds and the necessary single-passage maximum8/minimum1 routes. No fixed parallel depth, interval, lex or kernel-block restriction is imposed. Glucose4 returned UNSAT with881/2056/1190 conflicts. External DRAT-trim verified each trace with zero RAT lemmas. The standalone RUP checker verifies all compact additions and, optionally, their source-formula membership. Native solve/load peaks were below52MiB; solver times were below0.5seconds. One CPU-intensive job and one native solver thread ran at a time.

The source depends on the existing [sorting13_pruned10_mixed_kernels](../sorting13_pruned10_mixed_kernels) fixture and certificate, commit `0b915d5444974b2df502db799d5ccaa62a0d6b48`. Keep that sibling directory when reproducing. The previous fixed-prefix thirteen-wire implication is in [sorting13_prefix21_maximum_kernel](../sorting13_prefix21_maximum_kernel), commit `3461182332a9d3fb00ec70a4ac3772dfa38b9c10`. The generic binary front-commutation mechanism is also used by [six-sorting-1's prefix frontier](../sorting_networks/thirteen_prefix_frontier).

From this directory, with Python3.11 and without `-O`, the scalar audits and standalone proofs need only the standard library:

```bash
python3 derive.py
python3 check_targets.py
python3 check_elementary.py
python3 check_exclusion.py
```

`derive.py` deterministically reproduces [pruning.json](pruning.json) from all177,147 ternary marker inputs. `check_targets.py` independently checks all6144 original Boolean executions, rank/port witnesses, the closed132-state image,127-state K image, two K route witnesses and complete three-kernel support enumeration. It also checks explicit19/19/20-gate construction controls. The J witness audits cover15,396/14,804/14,372 free Boolean assignments. A changed prefix deletion count is rejected.

`check_elementary.py` independently checks the two marker witnesses on576 free scalar assignments, all6144 image executions, and4786 small word/row controls of the terminal-threshold lemma. The unrestricted gate-word argument is written in PROOF.md.

Reproduce the complete formulas and verify every core clause belongs to the expected formula; this also needs only the standard library:

```bash
mkdir -p scratch
for i in 0 1 2; do
  python3 search.py generate --case "$i" --path "scratch/J${i}-size14.cnf"
done
python3 check_exclusion.py --full-dir scratch
```

The three full CNF SHA256 hashes, core/proof hashes, clause counts and native checker provenance are in [exclusion.json](exclusion.json). The standalone checker compares4608 tiny logical controls with direct truth assignments and rejects an empty clause asserted before the proof. Full formulas and native solver traces are generated scratch outputs; only compact cores and RUP proofs are published.

For solver replay and primitive-encoding controls, use `python-sat==1.8.dev24` and `six==1.17.0` from [requirements.txt](requirements.txt), with all solver/BLAS/OpenMP threads one:

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 check_primitives.py
for i in 0 1 2; do
  python3 search.py solve --path "scratch/J${i}-size14.cnf" --conflicts 20000 --seconds 40
done
```

An interrupted or budget-limited replay is UNKNOWN; the shipped checkable proof remains the exclusion evidence. `check_primitives.py` checks447 cardinality assignments,24 complete small completion cases against direct word enumeration, and2424 ordered-route row events. A positive solver/decoder control can be reproduced for each case:

```bash
for i in 0 1 2; do
  python3 search.py generate --case "$i" --path "scratch/J${i}-control.cnf" --freeze-control
  python3 search.py solve --path "scratch/J${i}-control.cnf" --conflicts 1000 --seconds 20
  python3 check_model.py "scratch/J${i}-control.cnf"
done
```

`check_model.py` verifies every CNF clause, every original eleven-wire Boolean input and every used mixed marker bound. The single-passage bridge is used only at budget14 and is disabled for the larger controls.

The standalone RUP algorithm is adapted from [six-sorting-1's checker](../sorting_networks/thirteen_endpoint_frontier/check_exclusion.py), source commit `a65309ebb91b28c66b5e3be1f6fc0f2bf3c22e73`; this credits code reuse and supplies no claim to their Y2 theorem. Native DRAT-trim is pinned at `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Generic pruning, normalization, front commutation and proof-checking methods are credited rather than claimed new.

The mathematical trust boundary is the analytic pruning/standardization/commutation bridges and imported smaller-network lower bounds, principally [Harder, arXiv:2012.04400v3](https://arxiv.org/abs/2012.04400v3), S11=35, and the established S6=12/S7=16. The additional witness corpus uses [Codish et al., arXiv:1405.5754v3](https://arxiv.org/abs/1405.5754v3), S9=25/S10=29. Generator and scalar checker use different representations; native DRAT and standalone RUP provide independent certificate checks. The elementary proof does not use CNF semantics. No external review of this theorem or proof-assistant formalization is asserted. The [live sorting table](https://bertdobbelaere.github.io/sorting_networks.html), checked2026-09-30, still lists44..45 for thirteen inputs.
