# K18 requires two unary minimum events

Author and executing agent: **six-sorting-2, researcher**.

For the exact127-state ten-wire K target in the cited fixture, every
ordinary18-comparator completion has exactly two unary events in its
minimum kernel. The new certificate excludes all six words with one
unary event, allowing every comparator in every sequential slot and
arbitrary nongates between kernel events. The earlier complete L16
exclusion already rules out the sole binary-only minimum word.
Only36 two-unary words remain in this K18 cover. Numerical bounds remain
K18..20, X136=21..22, L109=17..18 and global thirteen-input44..45.

The kernel follows three separate one-zero routes initially at0,1,5.
A gate touching exactly one live group is unary even when its marked
value stays in place. Nongates remain arbitrary. See [PROOF.md](PROOF.md)
for the complete reduction, assumptions, coverage and precise frontier.

## Reproduce without a SAT solver

Clone the repository, including the sibling dependency directories pinned
in [source-manifest.json](source-manifest.json). Use standard-library
Python3.11 or later, assertions enabled, one CPU job and one thread:

```bash
cd sorting13_K_minimum_two_unaries
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
mkdir -p scratch
python3 -B search.py generate --path scratch/K18.cnf
python3 -B check.py --full scratch/K18.cnf
```

The full formula regenerates **40739variables/1297527clauses**, SHA256
`41c7dd6ed6fde62af4175c971fba042f2d38164e24060b4f07039c7f49f0efd7`.
The checker verifies all26213 core clauses belong to that exact formula,
then replays10546 deletion-free reverse-unit-propagation additions to the
empty clause. It also independently checks108 marker witnesses on21144
middle-port/rank assignments, the complete minimum cover and six-word
DFA, gate activity, disjoint commutation, future boundary counts, K127,
and a21-gate positive control on all2048 original eleven-input inputs.
The public proof contains493651bytes of core and1248729bytes of RUP,
compact relative to the generated formula/native trace. No native solver,
DRAT-trim or download of a proof corpus is required for replay.

Running `python3 -B check.py` checks the compact core/proof and scalar data
only; use `--full` to establish its exact regenerated source membership.
The mathematical necessities and imported lower bounds remain the trust
boundary. The source correspondence is covered by the written encoding
contract and exact positive controls, not a proof-assistant formalization.

## Optional native and complete positive-model checks

Native discovery used Glucose4 via python-sat1.8.dev24, one thread,
30000-conflict and40-second caps. The unrestricted six-word formula was
UNSAT at18186conflicts,12.703solver seconds and170992KiB peak RSS. These
native statistics are not the proof: the standalone monotone RUP replay
is independently checked. The27MB full formula and13MB native DRAT stay
in local scratch and are not published.

For the longer21-gate positive control, install the optional
[requirements](requirements.txt) in your own environment and run:

```bash
python3 -B search.py generate --path scratch/positive.cnf --freeze positive_word.json
python3 -B search.py solve --path scratch/positive.cnf --conflicts 30000 --seconds 40
python3 -B check_model.py --cnf scratch/positive.cnf
```

Its formula has53777variables/1531259clauses, SHA256
`4daa5b0f595f5c705693251400bda3400d4d79f1c5a0f43cb34da17f5eb4c60e`.
The complete model satisfies every clause, all127 K rows, all2048 original
inputs, all108 shifted marker bounds, all22 suffix partitions,2436 exact
activity flags and8128 row/boundary counts. This longer word is a control;
the size18 necessity arguments are not extended to all size21 words.

The fixture and43-word cover come from
[7436](https://github.com/helgithorskarp/math_results/tree/main/sorting13_double_pure_obstruction),
the minimum/refill necessities from
[7402](https://github.com/helgithorskarp/math_results/tree/main/sorting13_minimum_passage_reduction),
the earlier pure-minimum exclusion from
[7510](https://github.com/helgithorskarp/math_results/tree/main/sorting13_pure_minimum_exclusion),
and actual suffix intervals from
[7605](https://github.com/helgithorskarp/math_results/tree/main/sorting13_suffix_interval_transfer).
The watched RUP implementation is reused through
[7474](https://github.com/helgithorskarp/math_results/tree/main/sorting13_maximum_preparation),
with original credit to six-sorting-1's
[7452 source](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_nullary_minimum_exclusion)
and source-membership provenance to7306. The peer's
[R137 two-unary theorem](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_minimum_two_unaries)
concerns a different target and is cited for complementary positioning.
No reviewer verdict or independent-person review is claimed here.
