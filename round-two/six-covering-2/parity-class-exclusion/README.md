# Small-modulus parity restriction for period 10080

Actual author **six-covering-2**, **researcher**, 2026-10-01.

Every distinct covering with minimum modulus exactly eight and all moduli
dividing 10080 contains a class at 10, 12 or 14 of parity opposite to its
eight-class. Four complete exact trees exclude the common-parity pattern.
Combining these with the previously committed five-class exclusion leaves
19 of the complete 24 affine normal forms unexcluded. The global candidates
`{10080,15120,20160}` are unchanged.

Read [proof.md](proof.md). [frontier.py](frontier.py) checks all 120,960
physical phase tuples and lists the nineteen remaining representatives.
The compact [manifest.json](manifest.json) records all exact author-run
counts and hashes. Large generated trees are intentionally omitted and
regenerate from the unchanged public parent source; no private data is needed.

## Generate and exactly replay

From the repository root, use Python 3.12 with the pinned parent discovery
requirements (author versions: Python 3.12.14, NumPy 2.4.6, SciPy 1.17.1):

```sh
python3.12 -m venv /tmp/covering-parity-env
/tmp/covering-parity-env/bin/python -m pip install -r round-two/six-covering-2/requirements-discovery.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  /tmp/covering-parity-env/bin/python -B round-two/six-covering-2/parity-class-exclusion/reproduce.py --generate
```

Each root gets up to eight resumable voluntary batches of 180 seconds and
700 new nodes. This is a reproducibility allowance, not a mathematical
bound. Every LP has the existing two-second limit. Generation is sequential
and all numerical threads are one. The wrapper reports no theorem if any
root remains incomplete; rerunning resumes the generated files. Numerical
statuses or resource interruptions are never nonexistence certificates.

Once trees exist, Python 3.10+ standard library suffices for exact replay
(author replay: CPython 3.11.2). For example:

```sh
python3 -B round-two/six-covering-2/parity-class-exclusion/reproduce.py \
  --generated PATH_TO_TREES --require-manifest
python3 -O -B round-two/six-covering-2/parity-class-exclusion/frontier.py
```

`PATH_TO_TREES` contains `tree-normal-0-0-0.json`, `tree-normal-0-0-4.json`,
`tree-normal-0-0-6.json` and `tree-normal-0-0-10.json`. `--require-manifest`
also requires the exact author-run manifest. A different numerical proposal
may yield a different valid tree; omitting that option still checks every
strict integer leaf and every literal branch transport, and reports whether
the author manifest matched. Event hashes alone are not proofs.

The output must report four excluded forms, 15,120 newly forbidden phase
tuples, five combined excluded forms, 20,160 combined forbidden tuples,
and nineteen remaining forms. The author trees have 1,783 nodes, 309
expansions, 7,069 actual branch phases, 6,529 positive transports and
1,587,472 selected pair entries; all 1,474 leaves are strict.
The last two combined claims additionally use
the old theorem at graph height 8606; this wrapper checks the new four trees.
The older proof has its own [reproduction wrapper](../five-class-exclusion/reproduce.py).

[application-next.json](application-next.json) is the next unexcluded root
`8:0,9:0,10:0,14:1,12:0`. It supplies an exact physical residual bitset and
every unused eligible modulus, with all four primitive top resources free.
The wrapper recomputes every residual bit and the complete resource list.
This is a handoff state, not a covering or an exclusion certificate.

The proof is unformalized written mathematics plus exact Python execution,
checked by its author. Independent mathematical review is pending.
`SHA256SUMS` authenticates this directory's compact source, and the manifest
pins every parent source dependency. No solver is imported by the checker.
