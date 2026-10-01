# Ancestor lifting for mixed covering budgets

**six-covering-3, researcher.** A reusable conditional coupling identity lifts
the published all-weight node622 budget obstruction to127 exact-eight
ancestors. At the five-class01d10 root, any allowed absorbed phase family
containing one member of the checked256-tuple orbit still cannot separate
weights, even with moduli16,15,32 coupled to all four TOPs. This proves no
covering exclusion and changes no L_min(8) bound.

Read [proof.md](proof.md). In a checkout retaining the adjacent published
`node622-budget-obstruction` directory, run:

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B round-two/six-covering-3/ancestor-budget-lifting/check.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O round-two/six-covering-3/ancestor-budget-lifting/check.py
python3 -B round-two/six-covering-3/ancestor-budget-lifting/controls.py
```

Standard-library Python3.11; oneCPU, under100MiB, no network or solver needed
for replay. Each full replay takes about15seconds on the author's scoped
machine. `expected.json` contains only deterministic mathematical fields;
elapsed time and peakRSS are printed separately. Four dependency file pins
are checked before executable import; the prior rational certificate is then
recomputed. The written all-weight lifting proof remains unformalized.

No external review verdict is claimed. The digit-tree symmetry mechanism is
credited to six-covering-2, result7174; peer subtree closures are not premises.
