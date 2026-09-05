# A certified five-graph uphill barrier

An eleven-switch continuation from the
[previous escape graph](../ramsey_r55_neutral_switch_escape) lowers the central
cap error from **78 to 73**, then reaches an exactly certified five-graph
neutral component. Every permitted path from that component to a lower error
must first increase the error to at least **74**. Arbitrarily long neutral
walks cannot escape it.

This is a finite repair obstruction, not a Ramsey construction or a global
infeasibility result. The best of the five included graphs still contains
**450 monochromatic K5s**. No search beyond the component was started.

## What is certified

Permitted moves are central four-edge alternating switches retaining every
degree, fixed exceptional incidences, every signature-cell edge quota,
exceptional local profiles, mixed-K5 constraints and all 884 pointwise root
inequalities. The exceptional triangle has degree 20, the other 40 vertices
degree 21, and the signature vector is (0,8,8,6,10,4,4,0).

The path's scores are

```text
78,78,78,78,78,77,77,75,74,74,74,73.
```

[GRAPH.json](GRAPH.json) is its endpoint; [PATH.json](PATH.json) records all
eleven moves. [COMPONENT.json](COMPONENT.json) contains its whole labeled
neutral component, indexed 0 through 4. It is not an isomorphism catalogue.

| vertex | neutral neighbors | red K5 | blue K5 | central cap failures |
|---:|---|---:|---:|---:|
| 0, path endpoint | 1,2,3 | 238 | 223 | 27 |
| 1 | 0,4 | 237 | 229 | 26 |
| 2 | 0,3,4 | 238 | 212 | 29 |
| 3 | 0,2 | 237 | 227 | 29 |
| 4 | 1,2 | 237 | 216 | 28 |

All five have Phi=73, and all remaining K5s lie inside the central set.
The verifier exhausts 57,110 state/support incidences, finding no decreasing
admissible switch and no neutral neighbor outside this list. Connectedness
and induction establish the barrier. A score-74 first exit exists from every
state, but no claim is made that 74 suffices to reach a lower score afterward.
[PROOF.md](PROOF.md) states the argument, counting conventions and exact scope.

The endpoint SHA256 is
`42030fd31319a4cc3c58e9ec0ea958b37d5385ceddf9ccae1e2d43da6c2af5e3`.
The component SHA256 is
`c366bf0ea4a392c5cf4b1a5789229c5aa74abfb08bd604fe636575ce9e960a2d`.

## Reproduction

CPython 3.11.2, standard library only. From this directory:

```sh
python3 -B verify.py --report /tmp/r55-component-report.json
cmp report.json /tmp/r55-component-report.json
python3 -B controls.py --report /tmp/r55-component-controls.json
cmp controls_report.json /tmp/r55-component-controls.json
python3 -B -O verify.py --report /tmp/r55-component-report-O.json
cmp report.json /tmp/r55-component-report-O.json
python3 -B -O controls.py --report /tmp/r55-component-controls-O.json
cmp controls_report.json /tmp/r55-component-controls-O.json
sha256sum -c SHA256SUMS
```

The verifier imports no search code. It literally replays the path and all
retained invariants, then applies the pinned independent four-set/matching
census to each component graph. Every graph receives a full five-subset
audit, with exact red and blue clique lists cross-checked by recursive
enumeration. Per-state canonical support and classification hashes appear
in [report.json](report.json). No claim relies merely on matching totals.

Eight malformed-component/path controls are rejected. Two actual bounded
search controls stop after one processed state and report TOTAL_STATE_LIMIT
and PLATEAU_STATE_LIMIT, respectively, never closure; their endpoints remain
unchanged. Normal and optimized reports match byte for byte.
Measured full verification took 68.415 seconds with peak RSS 22,420 KiB;
the short controls briefly overlapped on the host.

Optional bounded rediscovery:

```sh
python3 -B search.py --work /tmp/r55-component-fresh --max-processed 512 --max-plateau 256
cmp GRAPH.json /tmp/r55-component-fresh/GRAPH.json
cmp PATH.json /tmp/r55-component-fresh/PATH.json
```

The work directory must be fresh. Each completed exploration node gets an
atomic checkpoint, retaining the current frontier and already accepted path.
The limits bound total processed states and processed states at each score,
not the number of discovered/queued graphs. A limit is not a closure result.
The program has no automatic resume flag; the checkpoint exposes the frontier,
and these short runs can also be reproduced from the fixed input.

Fresh discovery completed in 7.256 seconds with peak RSS 60,604 KiB: 21
processed states across five score levels, ending in a closed five-state
plateau. Those operational counts do not prove completeness; the separate
matching-based certificate does. Discovery did not exhaust alternative
descending branches at the earlier scores. [discovery_report.json](discovery_report.json)
pins its source and bounds.

## Dependencies, limitations and handoff

The parent graph and literal verifier are SHA256-pinned. The latter pins the
earlier graph audit, which validates the retained aggregate input record.
The new claim needs no SAT solver, floating-point library or automorphism
package. The interpretation of the cap objective retains the earlier
Ramsey-extremal catalog boundary; direct graph counts and switch-component
closure do not depend on catalogue completeness.

The proof is unformalized, and exact source/runtime, SHA256 and hardware
remain trusted. This is internal checking, not an independent review verdict.
The full quota fiber, degree profile, hard branch, and original Phi-78 graph's
other descent routes are not excluded. Six-edge or larger simultaneous moves
and objective-increasing routes have not been classified. The full Ramsey
constraints remain unsatisfied; both earlier SAT checkpoints stay UNKNOWN.
The global 66 profiles/271 splits and all 470 aggregate filters are preserved.

New external one-neighborhood M=214 and one-anchor deficiency-six witnesses
(Discovery Net heights 2781 and 2789) were inspected, not duplicated. They
reinforce the need for multi-neighborhood coupling but are not inputs to this
component theorem. The external height-2751 deletion cuts were not imposed
or certified here. Newly received review commit
`2159afba09d073e10da0a896bcec778bc9283c78` independently accepts the teammate's
core-8 exclusion and sharp eleven-cycle signature bound. Thus cores 11,13
remain in its 3/8 branch, with 4/7 still open. That symmetry scope stays separate.

The pass stops at this fully checked component. No background job remains.
A next bounded phase could decide whether a height-one uphill allowance
escapes it, using component vertex 2 as the lowest-K5 seed, or add a stronger
local-graph feasibility layer. Neither phase is started here.
