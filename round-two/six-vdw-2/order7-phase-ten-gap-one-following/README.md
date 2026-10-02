# Exact-ten gap-one following selection

Author: six-vdw-2, researcher. See [PROOF.md](PROOF.md): in H7-invariant AP7-free F617* colorings, either phase value occurring exactlyTEN has this rule at every run start: selected0,1/background2 implies selected3 and selected4 OR5. Whole exact-ten/H7 and interval3704 remain open.

Use Python3.11.2 with python-sat1.8.dev24/six1.17.0/CaDiCaL195 and the pinned drat-trim. From this directory, with generated data outsideGit:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /path/to/solver-venv/bin/python reproduce.py --work /path/to/fresh-work --converter /path/to/drat-trim
/path/to/solver-venv/bin/python guards.py --work /path/to/fresh-work --output /path/to/fresh-damage-work
```

Expected EXACT_H7_PHASE10_GAP_ONE_FOLLOWING,12 checked cases. Canonical strict totals254042 additions/888183 deletions/4364943 hints per mode. To replay already available proofs as untrusted candidates add `--certificate-cache /path/to/cache`, with head/<stem>.cnf and head/<stem>.lrat. Fresh model generation and BOTH definition audits precede every strict replay. No large corpora are uploaded. UNKNOWN/timeout gives no exclusion; do not retry identical bounded failures or raise shared caps.
