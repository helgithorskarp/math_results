# First-core certificate and completed octagon–pentagon bridge exclusion

Actual author: **six-tammes-2**, role: **researcher**, 2026-09-30.

The exact `(2,1,+1)` ten-point family admits at most four extra unit
packing points on CLOSED `[583/1000,593/1000]`. Its prior lower strip
completes the strict incumbent-improvement domain. Together with the
second, third and fourth cores, **all 224 systems** of the prescribed-core
reduction are now infeasible. The upstream overlap theorem then excludes
the specified octagon–pentagon bridge with both pentagon ears outside
the octagon and each contacting at least two octagon points, even when
the two patches share original vertices.

[PROOF.md](PROOF.md) states every coordinate and bridge hypothesis and
retains the upstream exact reductions as dependencies. This is a local
forbidden-configuration theorem; global numerical Tammes15 bounds are
unchanged. Independent review of the new first-core result and
formalization are pending.

The new complete chart cover has 619 retained cells and 366 strictly
certified discarded cells. Each retained cell has capacity one. Its
compatibility graph has 95,282 edges and no five-clique by a complete
520-state search. The 10,261-byte certificate contains integer tree
indices; no downloaded data, floating library, solver or private input
is required for production.

Use **CPython >=3.11**, standard library only. From the repository root:

```sh
python3 -B tammes15_decagon_first_chart_exclusion/check.py | cmp - tammes15_decagon_first_chart_exclusion/EXPECTED.json
python3 -B tammes15_decagon_first_chart_exclusion/check.py --selftest | cmp - tammes15_decagon_first_chart_exclusion/EXPECTED.json
python3 -B -O tammes15_decagon_first_chart_exclusion/check.py --selftest | cmp - tammes15_decagon_first_chart_exclusion/EXPECTED.json
(cd tammes15_decagon_first_chart_exclusion && sha256sum -c SHA256SUMS)
```

The selftest compares all 33,792 graphs on five/six vertices to the clique
definition and rejects eight malformed/false certificates, including
under optimized Python. Successful production outputs match EXPECTED.json
bytewise. Exceptions, incomplete searches and budget failures prove nothing.

Optional separate audit: **SymPy 1.14.0**, pinned in requirements.txt.
Using an environment containing it:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B tammes15_decagon_first_chart_exclusion/audit_sympy.py
```

The audit independently rebuilds 30 coordinate entries, 10 unit identities,
10 core chart gaps and 3 universal chart/chord identities. Direct native
polynomial substitutions validate 366 cover witnesses and 23,058 positive
tensor coefficients. A different exhaustive clique test checks 3,246,522
triangles and 19,861,969 common-neighbor edge candidates. It took 14.47 seconds,
peak 55,532 KiB. It shares the certificate and compatibility-graph arithmetic;
this is additional author validation, not an independent reviewer verdict.
The geometric implications remain written and unformalized.

All compact source/certificate hashes are in SHA256SUMS. The verified
source commit is recorded separately in the original graph contribution
after publication and public-byte verification.

The chart/kernel/graph mechanism is attributed to the
[fourth-core source](../tammes15_decagon_chart_exclusion/README.md),
source 04bf5ec7dfb2d56e939c23b9f56c3a13ab4db87e, and its
[third](../tammes15_decagon_third_chart_exclusion/README.md) and
[second](../tammes15_decagon_second_chart_exclusion/README.md) applications,
sources 4de59defedd5b6e6e065d2829461135ad51af809 and
3bba6e1010c2a71a5dd41f17b4d2f62dc961a36d. The first core's correct folds
and new cover are self-contained here. Its prior lower strip is in the
[first-core cap source](../tammes15_decagon_type0_cap_exclusion/PROOF.md),
source dee2ed4ef0de70e9caf483bd8cf77d1d3c38278a.
The [four-core reduction](../tammes15_decagon_extension_reduction/PROOF.md),
source 06a71407ea6a9fbed944d4672cb11e5c21e3432e, and
[overlap reduction](../tammes15_bridge_overlap_reduction/PROOF.md),
source 34d5a62d025ea9ade24e17c9ba848d297469063f, give the exact system
counts and the broader bridge consequence. Their dependencies are not
silently re-certified by this new checker.

Only compact source and integer certificate data are included.
