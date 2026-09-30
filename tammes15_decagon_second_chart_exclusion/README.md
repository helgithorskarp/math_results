# Exact chart exclusion for the second Tammes-15 decagon

Actual author: **six-tammes-2**, role: **researcher**, 2026-09-30.

The prescribed `(3,1,+1)` ten-point coordinate family admits at most
four additional unit packing points on CLOSED `[29/50,593/1000]`.
Its prior lower-strip certificate completes its strict incumbent-improvement
domain. Combined with the third- and fourth-core exclusions, **168 of
224** systems in the prescribed-core reduction are resolved. The first
core's 56 systems remain open above `583/1000`. Global numerical
Tammes-15 bounds are unchanged; independent review and formalization
are pending.

[PROOF.md](PROOF.md) supplies the exact coordinates, complete sphere
chart, closed cover, distance bounds and clique implication. The cover
has 150 retained cells and 178 strictly certified discarded cells.
Each retained cell has capacity one. Its compatibility graph has
5,124 edges and no five-clique, proved by a complete 37-state search.

Production requires **CPython >=3.11**, standard library only. No solver,
floating library, download or private input is needed. From the repository
root:

```sh
python3 -B tammes15_decagon_second_chart_exclusion/check.py | cmp - tammes15_decagon_second_chart_exclusion/EXPECTED.json
python3 -B tammes15_decagon_second_chart_exclusion/check.py --selftest | cmp - tammes15_decagon_second_chart_exclusion/EXPECTED.json
python3 -B -O tammes15_decagon_second_chart_exclusion/check.py --selftest | cmp - tammes15_decagon_second_chart_exclusion/EXPECTED.json
(cd tammes15_decagon_second_chart_exclusion && sha256sum -c SHA256SUMS)
```

The selftest compares all 33,792 graphs on five/six vertices against the
clique definition and rejects eight false or malformed certificates.
Every successful production output must match EXPECTED.json bytewise.
Exceptions, incomplete enumeration and state-budget failures prove nothing.

Optional separate audit: **SymPy1.14.0**, pinned in requirements.txt.
Using an environment containing that package:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B tammes15_decagon_second_chart_exclusion/audit_sympy.py
```

This rebuilds 30 coordinate entries, ten unit identities, ten core chart
inequalities and three universal chart/chord identities. Native polynomial
substitution validates 178 discarded witnesses and 11,214 positive
tensor-Bernstein coefficients. A different exhaustive clique algorithm
checks 42,348 triangles and 60,607 common-neighbor edge candidates.
It shares the certificate and compatibility-graph arithmetic and is
additional author validation, not an independent reviewer verdict.
Written geometric implications remain unformalized.

The certificate is **2,511 bytes**. File hashes are in SHA256SUMS.
The verified source commit is recorded separately in the original graph
contribution after source publication and public-byte verification.

The kernel, chart proof, graph arithmetic and clique mechanism are reused
with attribution from the
[fourth-core certificate](../tammes15_decagon_chart_exclusion/README.md),
source `04bf5ec7dfb2d56e939c23b9f56c3a13ab4db87e`, and
[third-core application](../tammes15_decagon_third_chart_exclusion/README.md),
source `4de59defedd5b6e6e065d2829461135ad51af809`.
The distinct second-core folds and new cover are self-contained here.
Its family identification is in the
[four-core reduction](../tammes15_decagon_extension_reduction/PROOF.md),
source `06a71407ea6a9fbed944d4672cb11e5c21e3432e`; its prior lower
strip is in the
[three-core cap certificate](../tammes15_decagon_remaining_cap_exclusions/PROOF.md),
source `6e7d7b8988873be4af2aedd16506b7bb2b1ff906`.

Only compact source and integer certificate data are included.
