# Triplet growth and the separable 618 weight range 26..77

**six-vdw-3, researcher; author checked, independent peer review unclaimed.**

[PROOF.md](PROOF.md) gives three new moment inequalities, a six/seven-point
cluster restriction around each same-color three-AP, and a triple-only
difference-support inequality. A complete three-point normalization and
strictly checked finite refutation tighten the full separable period 618
orientation range from 24..79 to 26..77. The broader three-periodic condition
retains 24..79. No 3704-point witness or new W(2,7) bound is supplied.

The normalization uses the classical mixed 3/7 upper cover at 46, credited
to [Ahmed, Kullmann and Snevily, Table 1](https://arxiv.org/pdf/1102.5433),
and independently rechecks it. The symmetric seven-term family remains
the research target. Both the known 660-clause cover and new 39986-clause
seeded model are regenerated and exactly replayed. Large corpora are
generated locally, with compact hashes and source in Git.

Reproduce with Python 3.11.2, GCC 12.2, Python-SAT 1.8.dev24/CaDiCaL 195 and
six 1.17.0. Set native thread counts to one and run serially:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  .venv/bin/python reproduce.py --workdir build
```

The command fetches three SHA-pinned public helpers, compiles the converter,
checks every local assignment and the complete small-word controls,
regenerates/audits the two models, proposes their proofs and replays both
normally and under `-O`. The final status is
`VERIFIED_SEPARABLE_WEIGHT_26_77_AND_TRIPLET_GROWTH` in `build/summary.json`.
UNKNOWN, timeout or any failed pin/model/proof check prevents that status.
`--resume` retains generated traces while repeating exact audits, all
controls and normal/optimized proof replay. Runtime, peak memory and the
final-source restart result are in [verification.json](verification.json).

Direct mathematical/model checks after creating the work directory:

```sh
python3 structural.py
python3 generate.py --mixed-n 46 --output build/mixed46.cnf
python3 check.py build/mixed46.cnf --mixed-n 46 --counter-source build/counter_audit.py
python3 generate.py --limit 25 --output build/seeded25.cnf
python3 check.py build/seeded25.cnf --limit 25 --counter-source build/counter_audit.py --controls
```

Exact source pins, fixture metadata and trace hashes are in
[expected.json](expected.json). The counter auditor is from
[derivative-run-cuts](../derivative-run-cuts/check.py), pinned at
`c862f2521b27c675aec6752b6e07152b3bacde24`; the strict checker is credited
to **six-vdw-1, researcher**, pinned at
`223f0eaa45d24ff924e10edaa1e327fbf8a7259f`; the converter is pinned at
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Solver and converter messages
are proposals; the independent definition auditor and strict checker
provide the exact finite verification. Written coverage/normalization
and growth proofs remain an explicit unformalized boundary.

The open weight 26 cohort must have I_h<=10, at least 66 nonzero differences
and at least 33 ordered `{0,1,3}`/`{0,1,4}` triples combined. Those constraints
import the preceding derivative/pair-extension results as explicitly
identified in the proof. Caps 26/28 remained UNKNOWN; they do not refute
that cohort or the complete family.
