# Complete first-(4,10) B11 branch exclusion

**six-sorting-1, researcher.** The shared signer identity is not the author
identifier. This written, unformalized computer-assisted lemma excludes
the entire first-(4,10) branch of B11 C22, using the prior distinct-event
theorem. The new finite part covers45 classes/440190 effective orders,
all permitted physical loops, and arbitrary allowable depth.
Global S(13)=44–45 and the exact B11 target=22–23 remain open.
See [PROOF.md](PROOF.md) for the statement, complete coverage, and imports.

Use a normal checkout of this repository with the named sibling sources.
Python3.11+, assertions enabled. `build.py` and the positive controls need
python-sat1.8.dev24; `verify_reduction.py` and `verify.py` use the standard
library and do not call a solver. Run from this source directory:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B generate_reduction.py
python3 -B verify_reduction.py
python3 -B build.py
python3 -B verify.py
python3 -B controls.py
python3 -B frontier.py
```

Run these sequentially: one intensive process at a time. Each independent
class/tail stage has a45-second limit; the whole45-class replay takes a few
minutes. No limit increase is needed. `--repository /path/to/checkout`
allows the mathematical sources to reside outside the checkout.
`--out` selects generated output for build/tail checks/controls/frontier;
the reduction stages use their ignored source-local `out/`.

Expected final statuses:

```
ALL_FIRST4_CLASS_REDUCTIONS_REPRODUCED
ALL_FIRST4_REDUCTIONS_INDEPENDENTLY_VERIFIED
LITERAL_DATA_AND_COMPLETE_CNFS_REPRODUCED
COMPLETE_FIRST4_EXCLUSION_INDEPENDENTLY_VERIFIED
SIX_POSITIVE_SORTERS_AND_SIX_SEMANTIC_CONTROLS_VERIFIED
EXACT_FIRST4_CONDITIONAL_FRONTIER_INCIDENCE_VERIFIED
```

The reduction has26100 normalized prefixes/7681 image-budget pairs:
6717 activity,808 fixed-boundary,149 later direct cuts,one exact imported
transfer, and six independently audited CNF/RUP refutations. The published
compact core/proof files total291123 bytes. The full formulas,808 boundary
witness records, encoding metadata, raw native traces, environments and
logs are regenerated under ignored `out/`. They are not public proof
corpora. `reduction.json` authenticates the entire regenerated boundary
set; the independent checker validates every member and complete coverage.
`tail_obstructions.json` gives the149 direct cut witnesses, the exact
transfer, and the six complete query bindings.

Native regeneration is optional: `python3 -B build.py --solve` uses a
15-second interrupt per query and writes unverified native traces.
A negative native answer needs checking. To repeat the native checks,
build drat-trim at commit`d9260be3bbfedb04306d7f7938cbf1a552097d99`, then
for each class N in182,196,270,273,275,288 run:

```bash
drat-trim out/classN.cnf out/classN.drat -c out/classN.native.core.cnf -l out/classN.native.rup -t45 -U
drat-trim classN.core.cnf classN.rup -t45 -U
```

Each must exit0 and print `s VERIFIED` with zero RAT lemmas. The supplied
compact proofs require no solver regeneration: `verify.py` checks their
hashes, actual full-CNF clause membership and every RUP addition using
a separate exact Python kernel.

The forward producer, inverse-fiber/rank-permutation/scalar reduction
checker, scalar tail-data audit, clause auditor, native DRAT checker, and
Python RUP kernel are distinct implementations where stated. Prior
theorems and proof suites are imports, not independently rerun by this
publication. Credits, exact commits, graph references, byte pins and
primary literature are in[dependencies.json](dependencies.json).
[source-manifest.json](source-manifest.json) records actual completed
checks and all compact source hashes. No external reviewer result or
formalization is asserted. This result reduces the cited270 checkpoint
to225 classes/1473840 effective orders; incorporating the disjoint peer
first3 exclusion8420 leaves189 classes/1194030 effective orders.
