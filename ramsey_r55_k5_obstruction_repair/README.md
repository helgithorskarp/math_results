# K5-aware repair: 450 to 384 obstructions

Eleven degree- and cell-quota-preserving switches reduce the actual number
of monochromatic K5s from **450 to 384**, retaining all mixed-clique and
pointwise root constraints. The endpoint is a certified **strict local
minimum** for this four-edge move family: all 185 admissible neighbors have
more K5s, and none is neutral.

This is NOT a Ramsey(5,5;43) graph or an exclusion of the whole graph family.
The endpoint has **198 red and 186 blue K5s**, all central, and 36 central
local-cap failures. Its cap-error Phi rises from 73 to 84. Both statistics
are exposed; no local-cap feasibility is inferred from a lower K5 count.

## Structural mechanism

Every triple among the four vertices of an alternating switch is bichromatic.
Therefore a K5 changed by the switch uses exactly two switched vertices and
three outside vertices. Its change can be evaluated by **eight triangle
counts entirely in the old graph**: four red and four blue common-neighborhood
terms. The update needs no full graph recount for each candidate.
[PROOF.md](PROOF.md) gives the bijection, signed-product form and exact scope.

This replaces the cap-only ordering whose mismatch was exposed by the
[prior height-one escape](../ramsey_r55_neutral_component_barrier). The input
is its preserved 450-K5 component vertex 2, not the 477-K5 escape endpoint.
No general novelty claim is made for local clique-count updates.

## Certificate

[PATH.json](PATH.json) contains all eleven switches, separate red/blue counts
and Phi values. Total K5 counts are

```text
450,436,427,416,411,406,401,399,396,394,392,384.
```

[GRAPH.json](GRAPH.json) is the endpoint, SHA256
`c343c8ace3fb1c9dff6e90175ecdb1035989e0caf40a976a44d464a1381dc03c`.
Exceptional degrees remain 20, central degrees 21; every exceptional incidence,
every signature-cell quota and all exceptional local profiles (92,107) stay
fixed. Signatures remain (0,8,8,6,10,4,4,0). All 884 pointwise root bounds
and all mixed-K5 constraints are retained.

The endpoint's complete 11,419-support census rejects 1,515 moves by pointwise
conditions and 9,719 remaining ones by mixed K5s. All 185 admissible moves
increase actual K5 count, by 1 through 37 with gaps; the full histogram and
canonical hashes are in [report.json](report.json). There are three +1 exits.
Any path to fewer K5s must first reach at least 385, but no sufficiency claim
for that height is made. This is not an arbitrary edit-radius classification.

## Reproduction

CPython 3.11.2; standard library only. From this directory:

```sh
python3 -B verify.py --report /tmp/r55-k5-repair-report.json
cmp report.json /tmp/r55-k5-repair-report.json
python3 -B controls.py --report /tmp/r55-k5-repair-controls.json
cmp controls_report.json /tmp/r55-k5-repair-controls.json
python3 -B -O verify.py --report /tmp/r55-k5-repair-report-O.json
cmp report.json /tmp/r55-k5-repair-report-O.json
python3 -B -O controls.py --report /tmp/r55-k5-repair-controls-O.json
cmp controls_report.json /tmp/r55-k5-repair-controls-O.json
sha256sum -c SHA256SUMS
```

The verifier imports no search code. It performs exhaustive literal five-set
audits at all twelve path graphs, compares complete clique lists against
recursive enumeration, and checks every retained invariant. Its endpoint
census uses four-set/matching generation and full K5 enumeration at every
admissible neighbor, not the new incremental formula.

Controls exhaust all 131,072 seven-vertex switch completions, finding 1,568
nonzero color updates. Smaller controls deliberately expose their vacuity:
at most six vertices cannot support a changed K5. On the actual endpoint,
all 11,419 entries, support sets, feasibility decisions and admissible
color-count updates agree between search and checker, with classification
SHA256 `29ea386181faa78e4078351360fe49f2a4a04ec94be8f1a32f088fe8a4caff83`.
Two malformed switch controls and a one-step STEP_LIMIT control pass.
Normal and optimized reports are byte-identical.

Measured full verification took 28.329 seconds, peak RSS 22,296 KiB; full
controls took 17.992 seconds, peak RSS 34,708 KiB. Some validation processes
overlapped on the host. These are reproducibility records, not performance
comparisons against an unmeasured alternative.

Optional fresh bounded rediscovery:

```sh
python3 -B search.py --work /tmp/r55-k5-repair-fresh --max-steps 128
cmp GRAPH.json /tmp/r55-k5-repair-fresh/GRAPH.json
cmp PATH.json /tmp/r55-k5-repair-fresh/PATH.json
```

Fresh discovery took 2.588 seconds, peak RSS 65,740 KiB; the graph/path match
byte for byte. It stops at the first strict-descent barrier, a step limit, or
zero K5s requiring a full target audit. Candidate ties use Phi and then the
labeled tuple. A step limit is not a local-minimum claim. The search source,
complete step summaries and bounds are in [discovery_report.json](discovery_report.json).
Accepted states are saved atomically outside Git. There is no live job or
continued search beyond the endpoint.

## Trust and next boundary

The component input and predecessor verifier are SHA256-pinned; original
artifacts are unchanged. The direct graph and local-minimum claims require
no solver, floating point, automorphism package or catalogue completeness.
The unformalized arguments, exact Python/runtime, SHA256 and hardware remain
trusted. This is internal checking, not an independent peer-review verdict.

The fixed quota family, degree profile and hard branch are not excluded.
All 66 profiles/271 splits, 470 aggregate filters and earlier UNKNOWN SAT
verdicts are preserved. External guarded deletion cuts were not imposed or
certified along this path. The newly inspected external height-2811 diagonal
cut concerns a distinct fixed d=22 two-anchor instance; its derivation was
not duplicated. Teammate symmetry work stays separate.

This pass stops at the fully checked 384-K5 graph and reusable update lemma.
No neutral walk can leave this strict local minimum. A next bounded phase
must permit an actual-K5 increase, use larger constraint-preserving repairs,
or add stronger structural information. It must still target a genuine
K5-free 43-vertex graph; this certificate is only intermediate progress.
