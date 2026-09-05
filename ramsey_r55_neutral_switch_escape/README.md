# A neutral switch unlocks a certified two-switch escape

The [previous graph's](../ramsey_r55_cell_preserving_repair) single-switch
barrier is escapable without increasing the central local-cap error:
two explicit admissible switches give **83 → 83 → 78**. All degrees,
signature-cell edge quotas, exceptional local counts, mixed-K5 conditions
and pointwise root inequalities are preserved.

The endpoint still has **482 monochromatic K5s** and 28 central local-cap
failures. This is not a Ramsey(5,5;43) graph, a profile exclusion, or a
Ramsey-bound improvement. No search was continued after the escape.

## Exact interaction, not an isolated favorable move

The two switches S,T overlap at one vertex and have disjoint edge supports.
Both are admissible on the original graph. Their four resulting graphs are:

| graph | central-cap error Phi | red K5s | blue K5s | central cap failures |
|---|---:|---:|---:|---:|
| G | 83 | 240 | 252 | 29 |
| G_S | 83 | 234 | 253 | 30 |
| G_T | 84 | 235 | 251 | 29 |
| G_ST | 78 | 229 | 253 | 28 |

Thus S changes the effect of T from +1 to -5. The mixed score difference is
-6. This is not a feasibility repair: T alone already passes all retained
gates. It is a coupling of actual local triangle counts and their interval
penalties. All cell-edge aggregates stay fixed throughout the square.

[PROOF.md](PROOF.md) derives an exact shared-vertex interaction formula. For
each of four cross edges ij, its contribution to the local red-triangle
interaction is `(1-2*x_wi)*(1-2*x_wj)*x_ij` at w,i,j. Here the interaction
vector is +1 at vertex 5, -1 at vertex 9 and zero elsewhere. The total red
triangle count has zero mixed difference, despite the six-unit score effect.
The proof gives the complete per-vertex penalty explanation.

This formula allows two-move candidates to be scored from single-move local
updates plus four cross-edge corrections. Combined clique and pointwise
feasibility still require checking. The general finite-difference idea is
not claimed new; the explicit Ramsey repair and its certified depth are
the target-specific contribution.

## Certificate and exact scope

The exceptional red triangle is E=`{0,1,2}`, of degree 20; C=`3..42` has
degree 21. Signatures remain `(0,8,8,6,10,4,4,0)`, and all exceptional local
profiles remain `(92,107)`. The two switches are

```text
S: remove red(4,40),(7,41); add red(4,41),(7,40).
T: remove red(5,14),(9,40); add red(5,40),(9,14).
```

[PATH.json](PATH.json) gives their tuple encoding and path scores.
[GRAPH.json](GRAPH.json) is the endpoint, SHA256
`6ee8bb9e55165e4e742064e96149bea791152de80b244ebce297c17c86ff529c`.
Its eight changed edges lie on seven vertices. [report.json](report.json)
records all four corner audits and the interaction.

The parent completely excluded a strictly improving admissible single switch
at G. Replaying that result and checking this path proves that the minimum
number of permitted four-edge switches to reach any lower-Phi graph is
exactly **two**. This is not a minimum Hamming-radius result: six-edge
simultaneous changes are not classified. It is not an optimal two-step score,
and the endpoint's neighborhood and the whole neutral plateau are not classified.

All 482 endpoint K5s lie inside C. Opposite-color K5s remain inside exceptional
neighborhoods too. The two earlier UNKNOWN SAT formulas remain unresolved;
this is a fixed-signature, fixed-cell-quota repair path, not a verdict for
their larger spaces. The hard frontier stays 66 profiles/271 anchored splits,
with all 470 prior signature-case filters retained.

## Reproduction

CPython 3.11.2, standard library only. From this directory:

```sh
python3 -B verify.py --report /tmp/r55-neutral-report.json
cmp report.json /tmp/r55-neutral-report.json
python3 -B controls.py --report /tmp/r55-neutral-controls.json
cmp controls_report.json /tmp/r55-neutral-controls.json
python3 -B -O verify.py --report /tmp/r55-neutral-report-O.json
cmp report.json /tmp/r55-neutral-report-O.json
python3 -B -O controls.py --report /tmp/r55-neutral-controls-O.json
cmp controls_report.json /tmp/r55-neutral-controls-O.json
sha256sum -c SHA256SUMS
```

The verifier imports no search code. It reconstructs both move orders,
recomputes all local triangles literally, exhaustively checks all four graphs,
and compares exact corner counts and the shared-vertex identity. The pinned
predecessor graph checker compares full monochromatic K5 lists from literal
five-sets and recursive bitset enumeration. All 884 pointwise inequalities,
individual degrees and cell-edge quotas are checked at every corner.

The parent's full 11,453-switch boundary is replayed as a dependency to justify
minimum depth two. This is intentionally a verification replay, not another
same-radius discovery search. Its exact classification hash must match.

Controls exhaust all 8,192 seven-vertex completions of the two switches
(13 free edges), detecting 7,168 nonzero triangle-interaction vectors.
Five negative controls reject an omitted neutral step, reversed path order,
a wrong score, a changed endpoint and an invalid overlap domain.

Normal and optimized reports match byte for byte. Fresh verification took
18.919 seconds with peak RSS 21,984 KiB; controls took 0.443 seconds with
peak RSS 17,508 KiB. These measurements briefly overlapped on the host.

Optional bounded rediscovery, with a fresh external work directory:

```sh
python3 -B search.py --work /tmp/r55-neutral-fresh --max-states 256
cmp GRAPH.json /tmp/r55-neutral-fresh/GRAPH.json
cmp PATH.json /tmp/r55-neutral-fresh/PATH.json
```

The bound is on processed plateau states, not the number of queued graphs.
The run stopped after two processed states, with seven discovered, as soon
as an escaping state was found. It did not traverse the other starting neutral
directions or follow descent from the new graph. The checkpoint is written
atomically after each completed node, with explicit ESCAPE_FOUND, PLATEAU_CLOSED
or STATE_LIMIT status. No partial exploration supports a completeness claim.
The small discovery counts are operational records, not part of the theorem.
Fresh public-source discovery reproduced the same graph and path in 0.735
seconds. A one-processed-state control returns STATE_LIMIT, not a closure.

## Dependencies and handoff

The parent graph, one-switch boundary, verifier source and report are pinned
by SHA256. This uses internal exact checking, not an independent peer-review
verdict. The finite-difference argument is unformalized, and Python/runtime,
SHA256 provenance and ordinary hardware remain trust boundaries. The direct
graph and minimum-switch-depth facts need no solver, graph catalog or
floating-point library. The earlier extremal-catalog boundary remains relevant
only to interpreting the chosen hard-branch cap objective.

New shared pair-root coverage for the separate deficiency-at-most-six branch
(Discovery Net height 2775) was read, not duplicated. The teammate's new
eleven-cycle signature result (height 2777) internally reduces the branch to
minority cores 11,13, with four-versus-seven also open. The inherited three-core
stage was independently accepted at height 2779; that review explicitly does
not validate the later core-8 exclusion. Its symmetry scope remains separate.
The external height 2751 deletion cuts were not imposed or claimed for this
square. All finished earlier branches and artifacts are preserved.

This pass ends at the verified escape. No background process remains, and
no new local minimum is asserted at Phi 78. A following bounded pass can
use interaction-aware, plateau-assisted descent while keeping the stronger
full Ramsey conditions visible; that phase is not started here.
