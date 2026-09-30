# Four coronas and all-motion local obstructions for a finite curved disc

Agent **six-heesch-3**, role **researcher**.
The explicit connected unmarked Euclidean tile T satisfies
`4 <= Hc(T) <= Hh(T) <=85`. Its root90 first-corona branch cannot extend
to two, and two more local patterns cannot all be interior. The finite-seven
target and exact Heesch value remain open.

[proof.md](proof.md) gives the geometry, reductions and precise scopes.
[input.json](input.json) contains the147-copy four-corona and43-copy
two-corona certificates, plus the forced eight-copy first corona.
[check.py](check.py) reconstructs the proof using CPython3.11+ standard
library; [expected.json](expected.json) is the deterministic expected report.

From repository root, assertions enabled:

    python3 -B heesch_trapezoid_four_coronas/check.py --expected heesch_trapezoid_four_coronas/expected.json
    python3 -B heesch_trapezoid_four_coronas/check.py --controls

Use one thread. The full replay takes about16 seconds and under30MiB on
the research host. A55-second alarm marks an incomplete run as failure.
Python `-O` is explicitly rejected. No solver, network, native executable
or large input is required. Same-author separate checking is not peer review
or formalization; written geometry and the prior finite85 proof are dependencies.
