# Exact four-hub P21 endpoint obstruction

six-code-3, researcher. Conditional author-checked theorem: every
71-word A(18,6,5) packing with exactly four unsaturated points has
their total pair replication at least21. The full profile
(18,19,19,19,20^14) is covered. Unit endpoint capacity and equality
rigidity exclude all15 P20 branches, using imported saturated radius
and precise local three-point premises. Independent mathematical
review is pending; ordinary bridges are unformalized.

Read [PROOF.md](PROOF.md) and [DEPENDENCIES.json](DEPENDENCIES.json).
CPython3.11+ and its standard library suffice. From the repository
root run sequentially, choosing fresh scratch directories:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 round-two/six-code-3/four_hub_p21_endpoint_cut/reproduce.py \
  --work scratch/four-hub-p21-normal
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -O round-two/six-code-3/four_hub_p21_endpoint_cut/reproduce.py \
  --work scratch/four-hub-p21-optimized
```

Both whole RESULT.json files should be identical, SHA256
e131837e15f8d7679e5602a8a1d8501d0b5fe5ca21344cbd666e029618cdfa6c.
Two different star/population algorithms reconstruct every426 marked
record,60 types and47 populations. An additional adjacency-subset
checker verifies all18 physical cut records using334912 unit graphs
and direct crossing-pair tests;16 physical/scope controls pass.
Complete cold runs take about3 seconds and under23MiB child peak RSS.

The count vectors and small graph controls are not physical code
realizations. Exact calculations complement the ordinary proof and
do not formalize it. No unrestricted upper70, whole profile exclusion,
threshold sharpness, priority, or new construction is asserted.
Expected data and all18 cut records were frozen before their distinct
checks. Fixed guards are never increased; incomplete work proves no
absence. Generated full records remain in the requested scratch directory.

Public source directory:
https://github.com/helgithorskarp/math_results/tree/main/round-two/six-code-3/four_hub_p21_endpoint_cut
