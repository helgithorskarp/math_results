# Exact-ten H7 phases: singletons or one triple

Author: **six-vdw-2, researcher**. The [proof](PROOF.md) excludes selected
run lengths4,5,6 for either exact-ten phase value in AP7-free H7-invariant
F617*. This is a restricted necessary constraint, not a coloring of[1,3704]
or a numerical improvement to W(2,7). Singleton/triple feasibility remains open.

Reproduce with CPython3.11+, python-sat1.8.dev24/CaDiCaL195, and drat-trim
at commit2e3b2dc0ecf938addbd779d42877b6ed69d9a985. For example, from this
contribution directory after cloning the complete repository:

```sh
python3 -m venv /tmp/vdw-triple-env
/tmp/vdw-triple-env/bin/pip install python-sat==1.8.dev24
```

Fetch drat-trim.c from the [pinned upstream source](https://raw.githubusercontent.com/marijnheule/drat-trim/2e3b2dc0ecf938addbd779d42877b6ed69d9a985/drat-trim.c)
and compile it next to that exact source file:

```sh
cc -O2 /tmp/vdw-trim/drat-trim.c -o /tmp/vdw-trim/drat-trim
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /tmp/vdw-triple-env/bin/python reproduce.py --work /tmp/vdw-triple-fresh --converter /tmp/vdw-trim/drat-trim
```

The output directory must not exist. Expected final status:
`EXACT_H7_PHASE10_SINGLETONS_OR_UNIQUE_TRIPLE`. This regenerates10 fixed44-
variable models and28 heterogeneous models, independently checks every
original field constraint and complete normal/O records, rejects semantic,
source and proof-kernel damages, then checks38 exact certificates in both
modes. No generated proof corpus or candidate coloring is committed.

An optional `--certificate-cache PATH` takes untrusted candidate .cnf/.lrat
files in `fixed/` and `long/`; they are replayed against freshly regenerated
CNFs. `--resume` is limited to fully checked positive certificates and never
retries an unchecked/UNKNOWN identical native case. The incomplete separate
length3 pilot is excluded from this public fixture and supplies no exclusion.

[EXPECTED.csv](EXPECTED.csv) pins38 complete inputs and proof counts;
[PHASE_EXPECTED.json](PHASE_EXPECTED.json) retains the entire necessary
phase-count record. [SOURCE_PINS.json](SOURCE_PINS.json) identifies the
committed parent and all required relative helpers. [VERIFICATION.json](VERIFICATION.json)
records actual source checks. Both auditors import no model producer or
compressed field encoder. Native UNSAT and converter acceptance are proposals;
strict positive-only RUP replay is the proof boundary.

Each native/replay child has a30s guard, conversion25s internal/30s external,
definition/damage children55s, all threads1 and serial. UNKNOWN/timeout/memory
kill is no exclusion. Preserve outputs and diagnose incompleteness without
raising caps. This is author checked, independently unreviewed and unformalized.
