# Focused four-hub P22/T4 exclusion

Actual author **six-code-3, researcher**. [PROOF.md](PROOF.md) establishes
the conditional implication: a71-word packing on18 points with pairwise
intersection at most two, four unsaturated hubs and P22 has T<=3. Thus
no word contains all four hubs. Independent review of this new result is
pending; its ordinary bridges are unformalized.

From the repository root, using standard-library Python3.12:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python round-two/six-code-3/four_hub_p22_hhh_cut/reproduce.py --work /tmp/p22-t4-normal
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python -O round-two/six-code-3/four_hub_p22_hhh_cut/reproduce.py --work /tmp/p22-t4-optimized
```

Both directories must be fresh. Each invocation uses one serial child at
a time. Fixed guards are218960 physical marks/30s,100000 states/10s for
the split census,500000 states/20s for the coefficient census and typed
partition check, and60s per child. A guard or failed stage is incomplete,
never mathematical absence. Source files are copied, not entry symlinks.

Six complete outputs are checked: two full physical screens, two focused
T4 censuses, and two typed support classifications. The census covers all
ten branches/37 vectors, retaining both ownership modes for T4. Only two
vectors survive the prior necessary tests; disjoint positive-support
sets exclude both. Complete mathematical SHA256:
`f4a1bfafd5df3c7ae7b164a4b9f25a8ee05597850e447b035a6de5f55d389fa4`.
Generated complete records and logs stay in the requested work directory.

The three baseline files are unchanged credited compiler/fixture/type
inputs. Source filenames and diagnostic PRIVATE/pass16 fields preserve
origin labels from the author's earlier pipeline, not an independent
review status. The supplied automorphism groups and old numeric census
functions in the baseline compiler are unused. The new focused drivers
call the compiler and reconstruct every needed row/type independently.

Only compact source, fixtures, hashes and validation summaries are
published. Neither the private39422-vector wider exploration nor its
incomplete producer prefixes are required. The theorem's explicit
premises and open T0..3/global profile scope are given in PROOF.md.
