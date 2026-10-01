# Validation record

Actual agent: **six-reviewer-3**, independent mathematical reviewer,2026-10-01.
Runtime: Python3.11.2, standard library only. All native-thread environment
variables set to1; CPU-intensive jobs run sequentially, each with a180-second
operational timeout. Every recorded replay completed successfully. No solver,
CAS, floating-point proof decision or resource escalation.

## Final independent replay

| Mode | Exit code | Wall seconds | Peak child KiB |
| --- | --- | --- | --- |
| normal | 0 | 79.203 | 28828 |
| optimized | 0 | 76.924 | 30316 |

Both modes return `ok:true`, with28 original cases,30 superseded quadratic
corroboration pairs,33 linear cases and11 rejected controls. Original literal
matrix orders are11/42/163; the linear source additionally supplies11/137.
Three rank-five tables and five exact trade spectra match. Every repaired
linear-range closed endpoint and the new quantitative upper gap are checked.
All reported author rank/radius fields and linear moment/corner/gap fields
are compared before receipt compaction. The actual independent code uses
full rational affine solves and integer Bareiss; no author imports.

Expected receipt SHA256:
`98e6dca1cd4057a072630c75dbae105c6afc1fc78b6139eb441f041c0bc6b64a`.

## Separate source-pinned author reproduction

The quadratic package is pinned to912163895633d4cc34d1ee515fd230e31442ba4e;
the linear package to8b110533913a22fd2d52955e3e20770fbc369cf8. Each command is
`python3 -B verify.py --check RESULTS.json` in a separate copy of that source
package; add `-O` for optimized mode. These author replays are validation of
comparison inputs, not the independently written checker.

| Package/mode | Exit code | Wall seconds | Recorded child maximum KiB |
| --- | --- | --- | --- |
| quadratic normal | 0 | 19.378 | 27708 |
| linear-normal | 0 | 35.471 | 29236 |
| linear-optimized | 0 | 37.45 | 31968 |
| quadratic-optimized | 0 | 20.027 | 31968 |

The last three measurements share a wrapper; their child-RSS maxima are
cumulative upper bounds over its sequential children. The quadratic outputs
report22 quantitative cases,6 smaller cases, literal11/42/163, residual sizes
at most two and13 controls. The linear outputs report33 cases through rank24,
literal11/137,17 controls and12 exact constant identities. Each normal and
optimized author output agrees with its respective source-pinned receipt.

## Scope and trust

The finite receipt corroborates rational identities and instances. Infinite
quantifiers use the complete ordinary proof in REVIEW.md: affine redundancy,
harmonic exhaustion, positive-tail sums, rescaled quotients, the separate
singular-value lower bound, repaired kernels, whole-vertex lift and tensor
endpoint argument. No proof assistant was used. Known failures below the
range apply only to the stated sparse ansatz. General H/I remain open.
No further resources are needed to reproduce the package.
