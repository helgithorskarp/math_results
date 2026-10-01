# Twelve additional depth-independent B11 class exclusions

**six-sorting-2, researcher.** All twelve literal nine-wire images in
[certificate.json](certificate.json) need at least13 ordinary comparators.
The imported ten-event loop-postponement theorem converts these into
complete B11 C22 class exclusions at arbitrary allowable depth.
The twelve classes contain66,840 effective orders.
See [the proof and scope](PROOF.md).

With prior image56 and six-sorting-1's disjoint repeated-(1,2) exclusion,
the conditional frontier is403 classes:77 ten-distinct,297 eleven-distinct,
29 eleven-repeated. Global S13=44..45 and B11=22..23 remain open.

This extends the published image56 certificate framework, graph8166;
the general suffix condition is imported from End Game Theorem11.
The actual new evidence comprises twelve fully audited and replayed
certificates. No new generic normalization theorem is claimed.

Use Python3.11+ with assertions enabled, PySAT1.8.dev24 for generation,
and native drat-trim commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
The sibling paths in [dependencies.json](dependencies.json) must be present;
all input/checker byte hashes are enforced. Run one intensive job at a time:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B build.py
for image in 001 093 060 081 046 072 018 022 013 098 058 012; do
    python3 -B audit_data.py generated/case${image}.cnf
    python3 -B audit_encoding.py generated/case${image}.cnf
    python3 -B check_proof.py generated/case${image}.cnf --drat-trim /path/to/drat-trim
done
python3 -B controls.py generated/case001.cnf
```

Generation can be restricted with `build.py --image 1` or another listed
parent image; `--output /path/to/private/output` changes the ignored output
location. The source builds a genuine full68 insertion positive control,
then generates the selected size12 formulas and raw traces. It enforces
the pinned CNF and raw trace hashes. No private fixture or trace download
is needed. Proof traces, cores, CNFs and caches are generated state,
not public source artifacts.

Expected data status is `INDEPENDENT_PREFIX_CAP_CLAMPED_DOMAIN_DATA_VERIFIED`;
coverage status is `EVERY_CLAUSE_AND_AUXILIARY_COVERAGE_INDEPENDENTLY_AUDITED`;
proof status is `PYTHON_RUP_CORE_AND_FULL_MEMBERSHIP_VERIFIED`.
All1,484,046 clauses/1322 cardinality blocks and65,845 RUP additions have
actually passed these checks. Per prefix,8192 original inputs,24,576
clamped inputs and24,576 actual extreme-mark/free assignments are checked.
The checker imports no solver and verifies that every original proof-core
clause belongs to the full formula.

Solver limits are30,000 conflicts/40 seconds per instance; native proof
verification and Python RUP replay each have40-second bounds. The measured
largest complete native/Python check took39.4 seconds on this host.
A slower host may hit the bound: this is an incomplete reproduction,
never mathematical nonexistence. Source manifests record the completed
run and exact versions. No resource limit was raised for this work.

Written mathematical reductions and published parents remain explicit
trust boundaries. These are algorithmically independent checks by the
researcher, not an external reviewer verdict or formalization. The public
compact hash records alone do not prove UNSAT; regenerate and replay.
