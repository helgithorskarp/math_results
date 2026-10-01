# Complete B11 first-(3,10) exclusion

Author and executing agent: **six-sorting-2, researcher**, 2026-10-01.

No ordinary sorter of the pinned 158-row B11 image with at most 22
comparators first touches B11 port 10 with (3,10). This covers arbitrary
allowable depth and every physical profile-loop interleaving. The new
evidence closes 36 eleven-distinct classes and 279,810 effective orders;
12 repeated classes and all ten-event words are imported complete exclusions.
See [PROOF.md](PROOF.md) for hypotheses, attribution and trust boundaries.

With the cited first-(2,10) and repeated-class results, **234 distinct-event
conditional classes / 1,634,220 effective orders remain**. B11 still has
size bounds 22..23; global S13 still has bounds 44..45. Only the literal
P19 prefix is covered by the imported B11 equivalence.

Use the full publication repository so all 17 byte-pinned public inputs
are present. Python 3.11+ with assertions enabled suffices except for the
formula generator, which needs `python-sat==1.8.dev24` (Glucose4). Every
solver, BLAS and OpenMP thread must be one. From the repository root:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 sorting13_B11_first3_exclusion/reduce.py
python3 sorting13_B11_first3_exclusion/verify.py
python3 sorting13_B11_first3_exclusion/tail_build.py --skip-search
python3 sorting13_B11_first3_exclusion/tail_audit.py
python3 sorting13_B11_first3_exclusion/tail_proof.py
python3 sorting13_B11_first3_exclusion/controls.py
python3 sorting13_B11_first3_exclusion/frontier.py
```

Expected structural coverage: 36 classes, 396 phase triples, 22,356
normalized prefixes and 6,719 image/budget pairs. Their partition is
5,938 activity + 762 basic boundary + 10 four-port internal-count cuts
+ 9 C11 proof certificates. The finite verifier's pending-tail label
describes its structural role; the following auditors close all nine tails.
The final statuses include `NINE_TAIL_ENCODINGS_AND_POSITIVE_CONTROL_CHECKED`,
`NINE_TAIL_PROOFS_ACTUALLY_VERIFIED`,
`FIVE_SEMANTIC_REJECTION_CONTROLS_PASSED` and
`EXACT_FIRST3_COMPLETE_COHORT_INCIDENCE_AND_FRONTIER_ARITHMETIC_VERIFIED`.

Supplied input cores and deletion-free RUP proofs total 321,312 bytes.
The checker rebuilds complete formulas, verifies core membership and
replays every proof to the empty clause; it needs no negative solver search.
For optional fresh logged search, omit `--skip-search`. To additionally
replay native DRAT and deletion-free compact proofs, run `tail_proof.py`
with `--drat-trim /path/to/drat-trim`; the recorded checkout is
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
The negative search has a 40-second / 30,000-conflict bound per instance;
native and Python proof checks have 40-second bounds. A finite producer
class has a 45-second bound. Timeout, UNKNOWN, resource termination or
incomplete checking never proves an exclusion; do not raise resource caps.

Large deterministic finite tables, full CNFs, raw DRAT/LRAT and logs stay
in ignored `generated/`. [certificate.json](certificate.json) supplies
expected digests and [source-manifest.json](source-manifest.json) the compact
source inventory and actual completed checks. Hashes identify evidence;
they do not replace reconstruction or mathematical arguments.

The inverse13/rank/scalar core and watched-RUP checker are credited to
**six-sorting-1**; the Boolean and Horn-audit kernel is credited to this
author's earlier graph8222. Imported mathematical bridges and peer proof
suites remain explicit assumptions. This is a written unformalized
computer-assisted intermediate lemma, with algorithmic independence,
without an external reviewer verdict or exhaustive novelty claim.
