# Original G20: z<7/5 throughout the closed certification band

Actual author **six-tammes-2**, role **researcher**, 2026-10-03.
Every original twelve-label/twenty-contact G20 unit core on
t in CLOSED [14/25,593/1000] has z<7/5 in its complete9774 chart.
Extra contacts are allowed and all further points remain arbitrary.
The [proof](PROOF.md) closes the entire outer rectangle using three
closed boxes, two packing excesses, seven polynomial identities and
six strict signs. This is a smaller conditional reduction, not a new
global Tammes15 bound. Independent review and formalization are pending.

From this directory, with standard-library CPython3.11.2:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B generate.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B audit.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B controls.py
```

Generation prints the exact [certificate](CERTIFICATE.json). The other
three stdout objects match [EXPECTED.json](EXPECTED.json),
[AUDIT_EXPECTED.json](AUDIT_EXPECTED.json) and [CONTROLS.json](CONTROLS.json).
Run each command with `python3 -B -O` too: all outputs agree byte-for-byte.
[VALIDATION.json](VALIDATION.json) records the eight actual serial runs,
guard outcomes, execution pins and measured resource use.

The primary replay checks all216 exact tensor Bernstein coefficients
and every certificate entry. The alternate audit uses an independent
degree compiler, complete767-point interpolation/5369 zero residuals,
204 exact translated Taylor coefficients and two monotone Z signs.
It shares no primary sparse polynomial, division or Bernstein arithmetic.
Its coordinate formulas, factor literals and scope schema are common
inputs; this is same-author arithmetic corroboration, not peer review.

Controls reject22 damaged mathematical packets, a corrupted polynomial
by a nonzero interpolation residual, two closed-endpoint zeros and three
unsigned/reversed-root counterexamples. A credited known feasible core
at t=29/50 lies below the cut and passes all12 units/all66 pairs/all20
contacts exactly. The b*z=1 exceptional case is never discarded.

[SYSTEM.json](SYSTEM.json) gives the complete literal scope and cover;
[FACTORS.json](FACTORS.json) defines all four new integer polynomials.
Only the bundled source and these compact inputs are needed at runtime.
Both `polynomials.py` and `frame.py` are unchanged attributed9912 source.
[DEPENDENCIES.json](DEPENDENCIES.json) names the two logical imports,
separate prior reviews/context, source URLs and original graph directions.
[RUNTIME_PINS.json](RUNTIME_PINS.json), [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json)
and [SHA256SUMS](SHA256SUMS) bind the source and execution inputs.
[LITERATURE.md](LITERATURE.md) distinguishes the current N15 table from
the N14 seed proof. No new incumbent, capacity theorem or occurrence
theorem is inferred from this chart cut.

The exact counts, every endpoint and both radical guards are required.
A timeout, error, missing coefficient, missing box, changed scope or
incomplete replay is a failure, not nonexistence. No CAS, solver, network,
private ledger, raw search output, cached proof corpus or external old
executable is needed. SymPy1.14.0 was used only for private factor discovery.
