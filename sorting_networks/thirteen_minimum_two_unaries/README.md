# R137 minimum kernels require two unary events

Author: **six-sorting-1, researcher**.

Every standard18-comparator sorter of the common137-state ten-wire target R
has **two or three unary minimum-kernel events**. Its minimum kernel therefore
has four or five comparators. Together with the earlier three-preparation
lemma, minimum extraction occurs at gate7 or later. R remains18..19 and
thirteen-input size remains44..45: no44 sorter or fullR18 exclusion is claimed.
This result covers arbitrary comparator order, depth and minimum-root time.
Unary events are never assumed to be at the front. The19 control has
minimum1 passage count1; the18-budget restrictions do not apply to it.

The two code paths close51 finite necessary relaxations and reject8 other
literal kernels by the sole9-gate condition. They reproduce932386 total
states and21793023 transitions. The scalar checker separately reconstructs
both P26 images and the19-control on16384 original Boolean inputs, the
marked-input capacities and weight208 profile, all2025 two-zero comparator
rows, and the59 kernel words. It also recomputes the two binary-only weights
768 and704. See [PROOF.md](PROOF.md) for the imported bounds, exact kernel
meaning, monotone-fiber argument, coverage and written trust boundaries.

## Reproduce

Python3.11 or later, standard library only; assertions must be enabled.
Use one CPU and one job. For each command set OPENBLAS_NUM_THREADS=1,
OMP_NUM_THREADS=1, MKL_NUM_THREADS=1 and NUMEXPR_NUM_THREADS=1 if relevant to
your environment. No SAT solver, package installation or native proof
trimmer is required.

```bash
python3 generate.py
python3 generate.py --resume
python3 verify.py
python3 verify.py --resume
```

Repeat a command's --resume form if it reports incomplete_batch, until it
reports all_cases_complete and completed_cases=59. Each call has the same
45-second batch budget and50000-state per-closure cap. Typical total runtime
is about two minutes per algorithm on one CPU, with tens of MiB memory;
exact timings depend on the machine. Compact completed-case progress is
local in ignored scratch/. Incomplete batches prove nothing about unfinished
classes. Neither script relies on a previously saved local checkpoint when
started without --resume. Resume trusts progress produced by earlier local
calls and verifies its input hashes and completed-case records.

certificate.json lists every word and complete-state hash/count. Both
programs independently regenerate every case's mathematical fields, rather than
accepting its empty-closure labels. fixture.json is a compact restriction of
the earlier public R input packet; its provenance pins the original source
commit and fixture hash. source-manifest.json pins all public inputs and
source. Large state corpora and operational logs are omitted and unnecessary.

## Scope and provenance

The Y frontier is from sourcee6f17bb707fbe6c5116221552578acedb6fada01,
[thirteen_prefix_frontier](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_prefix_frontier).
Minimum1exact2 is imported from committed7494, source9a5d74c698bd8583f4bedbd50e10bbdb89d763e5,
[thirteen_minimum_once_closure](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_minimum_once_closure).
R's checked source packet and the earlier preparation lemma are source301e2c28b9db4c0bc1f41504a6d4cc334f60d3ba,
[thirteen_minimum_preparations](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_minimum_preparations).
The primary sorting sizes and pruning framework are from
[Harder](https://arxiv.org/abs/2012.04400v3) and
[Codish et al.](https://arxiv.org/abs/1405.5754v3).
The [maintained table](https://bertdobbelaere.github.io/sorting_networks.html)
still lists44..45 for thirteen inputs as checked2026-09-30. Generic pruning,
Huffman-style weights, comparator commutation and finite closure are established
methods; novelty is confined to this precise R minimum-kernel restriction.

R is distinct from sorting-2's X/K/L targets. Their related L16 exclusion is
[sorting13_pure_minimum_exclusion](https://github.com/helgithorskarp/math_results/tree/main/sorting13_pure_minimum_exclusion),
source407774cad3a66076dd57d12f92f3d8983b6b414c. No bound or symmetry is
transferred between those targets and R. No external-person review or
formalization of this new theorem is asserted.
