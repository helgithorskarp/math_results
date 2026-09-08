# Closed direct four-path integration gate for R(5,5)

The direct block carrier obtained from h3931's four forced P5/complement-P5
copies fails its declared reduction test. One macro has a certified lower
bound exceeding twelve times the entire h3887 carrier, even after every
permitted internal and equal-type block relabeling. This closes this
representation choice; it does not invalidate h3931 or exclude a good43.

Read [PROOF.md](PROOF.md) for the complete target cover, precise carrier and
group action, integer proof, dependencies and limits. [GATE.json](GATE.json)
preserves the gate declared before computation. [CERTIFICATE.json](CERTIFICATE.json)
contains every forbidden event and all exact comparison integers.

From the repository root, using CPython 3.11 or later, standard library only:

```sh
python3 -B ramsey_r55_four_path_integration_gate/reproduce.py
```

Expected status: `REPRODUCED_DIRECT_INTEGRATION_GATE_FAILURE`.
The replay runs the producer and separate physical-graph checker in normal
and assertion-disabled modes, compares compact evidence, tests malformed
certificates, and verifies the source manifest. It downloads nothing and
imports no upstream implementation. Catalog counts and completeness are
explicit upstream premises; this replay does not independently establish
catalog completeness or the h3931 theorem.

Optionally audit the already-frozen, decompressed upstream 11-vertex catalog:

```sh
python3 -B ramsey_r55_four_path_integration_gate/check.py \
  ramsey_r55_four_path_integration_gate/CERTIFICATE.json --catalog11 /path/to/r44_11.g6
```

The 6,556,272-byte catalog is not republished. Its public origin, digest and
upstream source pins appear in [DEPENDENCIES.json](DEPENDENCIES.json).
The optional audit checks integrity and 546,356 distinct literal core words;
upstream mathematical validation remains imported.

No target solver was run. No physical packing task was decided and no
good43 was constructed. Carrier size gives no solver-runtime conclusion.
This package is a reproducible failed integration gate, not a new survivor
handoff or a universal obstruction to using the accepted h3931 theorem.
