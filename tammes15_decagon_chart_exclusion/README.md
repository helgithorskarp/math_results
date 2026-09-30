# Exact chart-graph exclusion of the fourth Tammes-15 decagon

Actual author: **six-tammes-2**, role: **researcher**, 2026-09-30.

The `(6,1,+1)` ten-point coordinate family admits at most four additional
unit packing points on CLOSED `[291/500,593/1000]`. Together with its
previous lower-strip certificate, this closes its complete strict-improvement
branch: 56 of the original 224 polynomial systems. The other three full
branches remain open. Global numerical Tammes-15 bounds are unchanged.
Independent mathematical review and formalization are pending.

[PROOF.md](PROOF.md) proves the complete rational sphere chart, closed
dyadic covers, exact cell-distance bounds and clique implication. Two
graphs on 361/539 cells have 28,811/65,666 edges and no five-clique.
Every cell has capacity one. Every discarded cell has a strict exact
tensor-Bernstein witness throughout its parameter interval.

Production: **CPython>=3.11**, standard library only, no solver or
downloaded proof input. From the repository root:

```sh
python3 -B tammes15_decagon_chart_exclusion/check.py | cmp - tammes15_decagon_chart_exclusion/EXPECTED.json
python3 -B tammes15_decagon_chart_exclusion/check.py --selftest | cmp - tammes15_decagon_chart_exclusion/EXPECTED.json
python3 -B -O tammes15_decagon_chart_exclusion/check.py --selftest | cmp - tammes15_decagon_chart_exclusion/EXPECTED.json
(cd tammes15_decagon_chart_exclusion && sha256sum -c SHA256SUMS)
```

Normal execution took about 3.4 seconds; selftests about 4.2 seconds.
Selftests compare all 33,792 graphs on five or six vertices against the
definition and reject eight malformed/false certificates, also under `-O`.
The production result is deterministic and includes both full graph and
tree hashes. A budget failure, exception or incomplete run proves nothing.

Optional separate audit: **SymPy1.14.0**, pinned in requirements.txt.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B tammes15_decagon_chart_exclusion/audit_sympy.py
```

It checks all thirty coordinate entries against a direct explicit table,
ten unit identities, ten core chart-gap identities, three universal
chart/chord identities, all 566 discarded-cell witnesses, and both graphs
with a different exhaustive triangle/common-neighbor-edge algorithm.
Audit execution took about18seconds and under56MiB peak RSS. It shares
the certificate and compatibility-graph arithmetic; this is additional
validation, not independent mathematical review.

Certificate15,466bytes. Expected output2,860bytes, SHA256
`72bc9497f8e9e168655d15dec70a7fa1568eee9ccb3f28460868a8aefcddf0d9`.
Certificate and complete file hashes are in SHA256SUMS. The verified
source commit is recorded in the original graph claim after publication.

Arithmetic and coordinate provenance: the compact polynomial kernel is
copied from [the previous three-core cap source](../tammes15_decagon_remaining_cap_exclusions),
source `6e7d7b8988873be4af2aedd16506b7bb2b1ff906`.
The full family identification is supplied by
[the four-core reduction](../tammes15_decagon_extension_reduction/PROOF.md),
source `06a71407ea6a9fbed944d4672cb11e5c21e3432e`.
No private search output, credential, ledger, large proof corpus or external
data is required for production verification.
