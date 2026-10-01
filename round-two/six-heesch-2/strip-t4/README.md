# A nineteen-cell strip with exactly three coronas

Agent **six-heesch-2**, role **researcher**. The explicit unmarked polyhex T4
has **Hc=Hh=3**, allowing all Euclidean motions and reflections. There is a
39-copy three-disc patch, and a finite fourth-corona obstruction. This tile
does not meet the finite-five target.

The obstruction combines necessary contact domains of sizes 190,43,29 with
an independently enumerated inventory of 17 root surrounds. None of those
surrounds has a second halo cover in the required 43-contact domain. The
29-contact domain nevertheless has a witness for every pair-centered halo
test: a nonempty fixed point of pair peeling need not extend to coronas.

[proof.md](proof.md) states the exact shape, depth argument, plane-tiling
exclusion and trust boundaries. [lower.json](lower.json) gives every lower
pose; [upper.json](upper.json) contains the short late rejection graphs.
Early exclusions are regenerated rather than supplied as bulky traces.
[stable.json](stable.json) proves the pair fixed point. The
[control15.json](control15.json) patch reproduces the known T3 four-corona
example from the author's census, not new mathematics.

Run with CPython 3.11.2 or compatible Python, assertions enabled, and no
solver package:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 round-two/six-heesch-2/strip-t4/verify.py
```

The reader regenerates 243 first-support and 50 pair exclusions with the
existing cell auditor. A separate lazy checker reconstructs cell incidence
and checks 178 late certificates /387 rejection states. A set-based search
on the first uncovered point independently finds all 17 surrounds. All 29
fixed-point witnesses, both lower controls and four false/malformed controls
are checked. [expected.json](expected.json) records the completed output.
The final fresh run took 20.941 seconds /48,688 KiB on one CPU, within two GiB.
The 45-second and 100,000-search-node guards abort incomplete verification.

Dependencies are the adjacent [geometry](../geometry.py),
[definition checker](../check_geometry.py), [cover](../cover.py),
[cell auditor](../audit.py) and [pair peeling](../pair_peeling.py).
The computation and geometric bridge are unformalized; internal auditing is
not independent peer review. No record or historical-priority claim is made.
