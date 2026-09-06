# A certified 560-point seed and a 68-selector family boundary

One bounded deletion sweep of the [certified 630-point seed](../hadwiger_nelson_heule632_pair_pilot/README.md)
produced a **560-vertex, 2,758-edge unit-distance graph of chromatic number
exactly five**. A fresh direct four-colour CNF has a checked DRAT refutation,
and the inherited five-colouring is verified on every retained edge.

There are also **492 verified singleton-deletion four-colourings**. Therefore
every non-four-colourable subgraph of this final support must contain the same
492 vertices. Only 68 vertices remain optional. A graph on at most 508 vertices
exists inside this support if and only if one of the induced graphs containing
the 492 mandatory vertices and exactly 16 of the 68 optional vertices is
non-four-colourable. [PROOF.md](PROOF.md) proves this precise equivalence.

This is a reduction to a finite family, **not a family closure or a record**.
The 68 unresolved singleton queries do not prove those vertices removable or
necessary. No minimality or vertex-criticality claim is made. The reduction
concerns only the final 560-point support, not all subsets of H632 or the
preceding 630-point seed.

## Exact graph and lower-bound certificate

Use the same host labels and exact coordinate sources as the parent package:
old H510 labels 0 through 509, followed by all 122 archived fresh centres in
increasing `centre_index` order, labelled 510 through 631. Each coordinate is
an eight-entry rational vector in the basis
`(1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165))`.
Scaling by 96 makes all coefficients integral.

[`certificate.json`](certificate.json) specifies the complete retained set
and its five-colouring. It contains 507 old points and 53 fresh points; the
omitted old labels are **399, 462 and 507**. All 199,396 pairs of the original
632-point host are checked exactly before restricting the graph. The host has
3,112 unit edges, and this support has exactly 2,758.

The final direct four-colour formula has 2,240 variables and 14,955 clauses.
The first retained triangle is pinned to three distinct colours; a global
palette permutation preserves satisfiability. Its SHA-256 is

```text
9dbec7853461556956cd34e406d475ba1f13144fae87e72b6f136e2b4805d673
```

Kissat 4.0.4 generated a 2,891,913-byte binary DRAT proof, SHA-256

```text
1044755e0d6697500bc7c67ac8124e5361cf97e72c02b5ace24d592c063f7b1d
```

The proof checker returned exit code zero and the exact line `s VERIFIED`.
Standalone regeneration produced the same proof and passed another check.
The five-colouring directly verifies all 2,758 retained unit edges. These
checks establish the exact chromatic number without trusting exploratory
UNSAT statuses.

## The completed sweep

The frozen [plan](plan.json) prescribed one order: all fresh vertices first,
then all old vertices, sorted within each block by initial seed degree and
label. Every trial retains the two original omissions. Previously checked
colourings permit a vertex to be kept without another query. A degree-at-most-
three restoration rule was implemented but did not fire in this run.

The search uses PySAT 1.8.dev24 with Glucose4.1, 20,000 conflicts and a
two-second interrupt request per query. A timeout leaves the vertex retained.
Exploratory negative results permit provisional deletion, but no smaller
five-chromatic graph is claimed before its final direct proof check.

| Outcome | Count |
| --- | ---: |
| Vertices covered by a known positive witness | 23 |
| Native queries with a directly checked SAT model | 469 |
| Native queries with provisional UNSAT | 70 |
| UNKNOWN queries, vertex retained | 68 |
| Ordered vertices processed | 630 |
| Native queries | 607 |

The sweep finished in 304.62 seconds with peak process RSS 175,428 KiB.
The timer requests interruption; it is not a strict wall-time guarantee for
the solver call. Fixed solver and clause ordering are reproducible, while
wall interrupts can change the UNKNOWN frontier on another machine. The
published retained set is fixed regardless of a rerun's exploratory outcome.

[`sweep.tsv`](sweep.tsv) preserves the compact outcome sequence. All 70
deletions are contained in the final checked support transition. No second
order, retry of UNKNOWN queries, or extension of their runtime was performed.

## The family boundary

[`boundary.json`](boundary.json) lists the mandatory set M and optional set U.
There are 488 old and four fresh vertices in M; U contains 19 old and 49 fresh
vertices. The exact target family has

```text
binomial(68,16) = 1469568786235308
```

supports `M union T`, with `T` a 16-element subset of U. None of those target
supports has been queried as a new candidate in this milestone. The final
graph's five-colouring restricts to each one, so a checked four-colour
refutation of any member would prove an exactly five-chromatic 508-point
graph.

The original archive audit verifies all 492 deletion witnesses, totalling
1,351,849 retained edge inequalities. A separate regeneration uses a different
selector encoding and produces 492 new proper witnesses, with the same edge
count, in 94.84 seconds. The original and regenerated witness bytes differ;
both are accepted by direct mathematical checks. No hash equality between
alternative colourings is required.

## Reproduction

The exact graph and proof verifier uses only the Python standard library,
plus Kissat and `drat-trim`. From the repository root:

```sh
python3 -B hadwiger_nelson_heule632_minimize/verify.py \
  --out /tmp/hn560-proof --regenerate-with /path/to/kissat \
  --drat-trim /path/to/drat-trim
```

Expected: `EXACT FIVE-CHROMATIC SEED VERIFIED`, 560 vertices, 2,758 edges.
Standalone proof regeneration and verification took 6.23 seconds here.
A supplied proof can instead be checked with `--proof /path/to/four.drat`.
The verifier always requires a real proof for the lower bound.

To reproduce the mandatory-vertex certificate, use a Python environment with
`python-sat==1.8.dev24`:

```sh
python3 -B hadwiger_nelson_heule632_minimize/check_boundary.py \
  --out /tmp/hn560-boundary --regenerate
```

Expected: `MANDATORY492 OPTIONAL68 FAMILY REDUCTION VERIFIED`, 492 positive
witnesses and 1,351,849 edge checks. This regenerates the local witness file
using at most 492 queries, with 200,000 conflicts and a five-second interrupt
request each. If a bound is reached, it saves completed witnesses and reports
incompleteness; no negative conclusion follows. Alternatively, supply the
original or another complete valid witness file with
`--witnesses /path/to/final_deletions.json` instead of `--regenerate`.

The original experimental sweep can be replayed separately:

```sh
python3 -B hadwiger_nelson_heule632_minimize/search.py \
  --out /tmp/hn560-controls --controls
python3 -B hadwiger_nelson_heule632_minimize/search.py \
  --out /tmp/hn560-search \
  --run-with-controls /tmp/hn560-controls/controls.json
python3 -B hadwiger_nelson_heule632_minimize/verify.py \
  --out /tmp/hn560-archive-audit --archive /tmp/hn560-search \
  --regenerate-with /path/to/kissat --drat-trim /path/to/drat-trim
```

The sweep pins the executed PySAT native-module hash. The final verifier
permits another solver build, requiring its actual checked proof. Native
binary hashes, input hashes, resource limits and fixed order are in the plan.
Kissat's source ID is `8af8e56f174b778aef3aa45af9f739b2a5f492c2`.
Output directories must be new and should be outside the repository.

## Evidence and trust boundary

The search imports the parent's ordered-convolution geometry; the verifier
uses its independently written sparse-radical geometry and direct CNF builder.
It imports no `search.py` code. The archive audit replays every support
transition, verifies 83,736 initial positive edges and 1,290,001 edges in
native positive rows, then verifies all final singleton witnesses. Controls
cover 262,144 Boolean assignments over all eight graphs on three vertices
and all 32 selected subsets of K5. Improper positive certificates are rejected.

The witness regenerator forces inactive colour variables false, while the
search gates edges by selectors and retains one colour at inactive vertices.
Every regenerated witness is checked on the exact graph, so its SAT engine
is only a witness finder. The lower bound relies on the direct CNF equivalence
and DRAT checker, exact CPython arithmetic and the radical basis. No
proof-assistant formalization, second DRAT implementation, or independent-
author review of this new result is claimed.

Raw proofs, CNFs, solver logs and the roughly 342 KB original witness table
remain local. Public source regenerates the proof and a complete witness
table; the package contains only compact inputs, counts, hashes and the final
five-colouring. [validation.json](validation.json) records actual checks.

The completed milestone supports a changed family-level test on 68 selectors.
One possible next step is exact minimum-degree and cardinality feasibility
with M forced and at most 16 optional vertices, followed by a bounded actual
candidate decision if feasible. That phase has not started. Repeating this
same deletion order or merely extending UNKNOWN runtimes is not the next step.
