# Exact chart exclusion for the third Tammes-15 decagon

Actual author: **six-tammes-2**, role: **researcher**, 2026-09-30.

The prescribed `(6,50,-1)` ten-point coordinate family admits at most
four additional unit packing points throughout CLOSED
`[581/1000,593/1000]`. Its prior lower-strip certificate closes the
remaining range, so this core has no fifteen-point extension throughout
its strict incumbent-improvement domain. Together with the earlier
fourth-core result, **112 of the original 224 reduced systems are
resolved**. The first two cores' 112 full-domain systems remain open.
Global numerical Tammes-15 bounds are unchanged. Independent mathematical
review and formalization are pending.

[PROOF.md](PROOF.md) gives the exact coordinates, complete rational sphere
chart, closed covers, distance bounds and clique implication. Three
graphs on 438/483/612 cells have 43,338/53,111/85,365 edges and no
five-clique. Every retained cell has capacity one. All 963 discarded
cells have strict exact tensor-Bernstein witnesses on their whole
closed parameter/cell domains.

Production requires **CPython >=3.11**, standard library only. No solver,
downloaded data, floating library or private input is needed. From the
repository root:

```sh
python3 -B tammes15_decagon_third_chart_exclusion/check.py | cmp - tammes15_decagon_third_chart_exclusion/EXPECTED.json
python3 -B tammes15_decagon_third_chart_exclusion/check.py --selftest | cmp - tammes15_decagon_third_chart_exclusion/EXPECTED.json
python3 -B -O tammes15_decagon_third_chart_exclusion/check.py --selftest | cmp - tammes15_decagon_third_chart_exclusion/EXPECTED.json
(cd tammes15_decagon_third_chart_exclusion && sha256sum -c SHA256SUMS)
```

Normal verification took 4.62 seconds on CPython 3.11.2; ordinary and
optimized selftests took 5.21/5.53 seconds. They compare every one of
33,792 graphs on five/six vertices with the clique definition and reject
eight malformed/false certificates. Every successful production output
is byte-identical to EXPECTED.json. Exceptions, incomplete runs and
state-budget failures establish no exclusion.

Optional separate audit: **SymPy 1.14.0**, pinned in requirements.txt.
Using a Python environment containing that package:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B tammes15_decagon_third_chart_exclusion/audit_sympy.py
```

It rebuilds all thirty coordinate entries from a direct polynomial
table, verifies ten unit identities, ten core chart-gap identities and
three universal chart/chord identities. Native QQ[t,u,v] substitutions
check all 963 witnesses and 60,669 positive tensor coefficients. A
different complete ordered-triangle/common-neighbor-edge algorithm
checks all three graphs. This audit took 26.56 seconds, peak 55,748 KiB.
It shares the certificate and compatibility-graph arithmetic; it is
additional author validation, not independent mathematical review.
The written geometric implications remain unformalized.

The certificate is 25,960 bytes. Expected output is 3,678 bytes, SHA256
`8ffb51cfff73474fbabfe8e899fd6877ba9bcd7d7cc68970ae25c3de6cf92ab4`.
Certificate SHA256:
`21487607c334f451a23bfaa8321f531c46dd772f64799a40da84574155ec2637`.
All file hashes are in SHA256SUMS. The verified source commit is
recorded separately in the original graph contribution after publication.

The chart proof, polynomial kernel, graph arithmetic and clique code are
reused with attribution from
[the fourth-core certificate](../tammes15_decagon_chart_exclusion/README.md),
source `04bf5ec7dfb2d56e939c23b9f56c3a13ab4db87e`.
The third core's distinct folds and new interval trees are explicit in
this self-contained directory. The full family/isometry identification
is in [the four-core reduction](../tammes15_decagon_extension_reduction/PROOF.md),
source `06a71407ea6a9fbed944d4672cb11e5c21e3432e`.
The prior third-core lower strip is in
[the three-core cap certificate](../tammes15_decagon_remaining_cap_exclusions/PROOF.md),
source `6e7d7b8988873be4af2aedd16506b7bb2b1ff906`.

No keys, credentials, private ledger, raw pilot data, large proof corpus
or external proof input is part of this contribution.
