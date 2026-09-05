# The Parts pool colouring dual clears the fixed 509-vertex control

This package replaces the previous three-block quantified selector by
an exact two-block dual: **every selection of at most 134 pool points
has a compatible four-colouring beside fixed L**. Its truth would close
the sealed at-most-508 family; its falsity would expose a candidate
non-four-colourable graph. [PROOF.md](PROOF.md) proves the equivalence,
using the reviewed twenty-class L-interface theorem.

The known non-four-colourable 509 control now finishes in about 4.78 seconds
with the same DepQBF executable that previously returned unknown at
30 seconds. A separate Kissat run produces a fresh independently accepted
DRAT certificate in about 0.87 seconds, with checking taking 0.62 seconds.
This is a representation assessment and reproduction of a known control.
**The full family has not been solved; no new closure, lower bound or
five-chromatic graph is claimed.**

## Reproduce

From a complete repository checkout, Python 3.11 standard library only:

```sh
python3 hadwiger_nelson_parts509_quantified_dual/verify_dual.py
```

Expected: `DUAL FINITE CHECKS VERIFIED`, 52 abstract fixtures, 491
selector assignments and 491 fixed-selection specializations checked
against direct four-colouring enumeration. These include the prior
14 controls and exhaustive three-vertex graph/budget tests. They are
logical fixtures, not asserted plane unit-distance geometries. The
verifier also checks two explicit colourings of the real 508-vertex
deletion control, including the decoded native witness in
[native_witness.json](native_witness.json).

Generate the unsolved full-family formula locally:

```sh
python3 hadwiger_nelson_parts509_quantified_dual/encode_dual.py \
  --case pool508 --out /tmp/parts-dual508.qdimacs
```

Expected: 3852 variables and 74956 clauses, with 303 universal selectors
followed by 3549 existential variables. QDIMACS SHA-256:
`20f03643727208fafbe960bea868e443ea6fb8e0788c5846c8fb93c8ef660e20`.
This hash authenticates the deterministic encoding, not its truth.

With DepQBF 5.01, Kissat 4.0.4 and drat-trim, reproduce the bounded solver
controls and generate/check the fixed 509-vertex proof:

```sh
python3 hadwiger_nelson_parts509_quantified_dual/benchmark.py \
  --depqbf /path/to/depqbf --kissat /path/to/kissat \
  --drat-trim /path/to/drat-trim --work /tmp/parts-dual-controls \
  --real-seconds 30 --proof-seconds 120
```

Use a fresh work directory. Solver versions, executable hashes, instance
hashes and producing-run measurements are in
[benchmark_summary.json](benchmark_summary.json). The command never runs
the full-family instance. Raw formulas, native logs and the generated
binary DRAT stay in the chosen local work directory. The checker reports
`s VERIFIED`; the producing proof had 1098848 bytes and SHA-256
`37434580d223428ed183f1f2dc1ba5b05c3cfeeb9186d05eab55f2405724245f`.
Proof bytes may depend on the exact solver build and invocation; acceptance
by the checker, rather than hash equality alone, is the proof requirement.

## Calibration results

| Control | Dual truth | DepQBF result |
| --- | --- | --- |
| 52 abstract fixtures | 28 true, 24 false | All agreed |
| Fixed original S: 509 vertices | False | False in 4.780 seconds |
| Fixed S minus 397: 508 vertices | True | True in 0.065 seconds |

For fixed S, the SAT-exported CNF has 560 variables and 2944 clauses, SHA-256
`455638bf235c49d8877cf4086cb6d2d1730b71539c3ed6e7e1e71cea50686741`.
The native 508 colouring is checked on 508 vertices and 2427 strict unit
edges. The full native workflow took 10.722 seconds including geometry
generation, with maximum child peak RSS 68740 KiB on the producing Linux
host. A separate post-run decoder check produced the committed positive
witness. This timing excludes authoring and the solver-free finite audit.

The earlier encoding used universal two-bit colourings and existential
monochromatic-edge witnesses. This one uses existential colour indicators
and guarded ordinary colouring clauses after universal selection. The
comparison changes polarity, variable representation and fixed-selection
simplification together; it does not isolate the effect of any one change
or establish full-family scaling.

## Continuation decision and scope

The fixed 509-vertex validation hurdle passed. The subsequent single
600-second full-family pilot returned **unknown** after 600.208 seconds,
with exit code 0 and no candidate or strategy certificate. See
[PILOT.md](PILOT.md) and [pilot_summary.json](pilot_summary.json) for the
exact configuration, limits, hashes and reproduction command.

Decision: **do not automatically extend this unchanged configuration**.
The next useful milestone is to justify and validate an exact reduction
of the selector domain before another family run. Inclusion-minimal
selected sets and their necessary degree conditions are a proposed route,
not an implemented or certified reduction in this package. No job is
active, and the old isolated cut/shrink loop remains paused.

A future false dual answer must yield a selection of at most 134 pool
points and a separately checked non-four-colourability certificate;
an explicit five-colouring is additionally needed for a record claim.
A true dual answer needs a checked QBF certificate or independently
verified complete colouring strategy to establish family closure.
Unknown remains unknown. Any conclusion applies only to the fixed 374-point
L and the specified 303-point pool.

All dependency hashes are checked through [manifest.json](manifest.json)
and the pinned previous encoder manifest. The source uses the earlier
exact geometry and interface evidence; it does not duplicate the
teammate's alternative geometric construction or the parked overlap census.
