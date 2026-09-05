# Exactly 34 exposed edits are needed for the old-obstruction cover relaxation

The [353-K5 endpoint](../ramsey_r55_k5_neutral_component/EXIT_GRAPH.json)
requires **at least 34 visible edits and 52 total edits** to destroy all its
original colored K5s while retaining its exceptional incidences, individual
degrees and exceptional profiles. An explicit graph attains 34 visible edits
and additionally satisfies all 884 pointwise root inequalities. Thus 34 is
the **exact visible-edge optimum for this cover relaxation**.

The sharpness witness uses 82 total edits and changes 15 cell quotas. It
destroys all 353 old obstructions but creates 621 new K5s, including 156
meeting the exceptional set. It is **not** a Ramsey graph, a mixed-free
repair, or an improvement to the retained 353-K5 endpoint. No optimal total
edit distance, new Ramsey bound, profile exclusion or radius classification
is claimed.

## The structural certificate

[PROOF.md](PROOF.md) defines the exact graph family and proves the encoding.
[certificate.json](certificate.json) contains two integer dual certificates.
The visible certificate uses only 54 actual K5s, twelve vertex-degree
equations and the two neighborhood counts of exceptional root 0:

```text
12 * visible_edits >= 398, hence visible_edits >= 34.
```

This is verified by checking capacities on all 780 individual edges. It
couples the exposed neighborhoods rather than freezing them. The total-edit
certificate gives at least 50473/1000 edits; equal red-edge counts force the
distance to be even, hence at least 52. Both lower bounds omit the 884 root
inequalities, mixed-K5 conditions and central hard caps. They therefore also
apply when those further necessary conditions are imposed.

[GRAPH.json](GRAPH.json) proves sharpness only for the explicitly weakened
cover system. Its 34 visible and 48 invisible edits preserve degrees
`20^3 21^40`, all exceptional profiles `(92,107)`, fixed E incidences, and all
884 pointwise rows. The new defects are 300 red and 321 blue K5s, of which
61 red and 95 blue meet E. There are 36 central hard-cap failures.
The complete audit and edit list are in [report.json](report.json).

The bounds concern this **labeled seed with fixed exceptional incidences and
profiles**. They do not apply automatically after changing those hypotheses.
They exclude no whole hard profile. In particular, the exact visible optimum
34 is **not** asserted for the preceding mixed-free family or for full
Ramsey graphs. The witness is deliberately labeled a cover witness.

## Reproduce the proof without a solver

CPython 3.11.2, standard library only, with the full repository checkout for
the pinned sibling seed. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -B verify.py --report /scratch/new-r55-visible/verified.json
cmp report.json /scratch/new-r55-visible/verified.json
python3 -B -O verify.py --report /scratch/new-r55-visible/verified-O.json
cmp report.json /scratch/new-r55-visible/verified-O.json
python3 -B controls.py --report /scratch/new-r55-visible/controls.json
cmp controls_report.json /scratch/new-r55-visible/controls.json
python3 -B -O controls.py --report /scratch/new-r55-visible/controls-O.json
cmp controls_report.json /scratch/new-r55-visible/controls-O.json
```

Expected: `VERIFIED_EXACT_VISIBLE_COVER_OPTIMUM`, visible optimum 34, total
lower bound 52; ten malformed-input controls rejected. The checker imports
no producer, solver, or inherited checker. It reconstructs graph quantities
directly using sets and literal combinations. Complete seed and witness K5
lists are compared with a separate recursive clique enumeration. Every dual
edge coefficient is checked in integer arithmetic. Controls also test all
780 coordinate derivatives of the degree/profile map and all 2048 original
color / ten-edge flip patterns for the cover equivalence.

Normal and optimized Python agree byte for byte on verification and control
reports. The seed is preserved in its parent directory. There is no omitted
solver proof or large certificate needed to establish the claims.

```text
certificate.json
1536b4a174d040d172be05e472e065baf4c36ca562b68204f727caa7113736f7
GRAPH.json
af270eec6c09af7733598a8569075380fe01fa1ea1b8c310722debad31f67cfc
report.json
0ce52d955b6cae9d43db7ed86f22e0643f1179124acb4d71586d953a27617509
```

## Optional bounded discovery replay

The numerical discovery environment was NumPy 2.2.6, SciPy 1.15.3, bundled
HiGHS 1.8.0, CPython 3.11.2. With those packages available:

```sh
python3 -B generate.py --work /scratch/new-r55-visible/production --seconds 60
cmp certificate.json /scratch/new-r55-visible/production/certificate.json
cmp GRAPH.json /scratch/new-r55-visible/production/GRAPH.json
python3 -B verify.py --certificate /scratch/new-r55-visible/production/certificate.json --graph /scratch/new-r55-visible/production/GRAPH.json --report /scratch/new-r55-visible/replay-check.json
python3 -B -O generate.py --work /scratch/new-r55-visible/production-O --seconds 60
cmp certificate.json /scratch/new-r55-visible/production-O/certificate.json
cmp GRAPH.json /scratch/new-r55-visible/production-O/GRAPH.json
```

Work directories must be fresh. The producer solves two LPs, converts their
duals into exact integer certificates, then makes one bounded integer call
minimizing visible edits. The model has 780 binary variables, 353 old-K5
cover rows, 46 degree/profile equalities, and 884 pointwise rows. It imposes
no symmetry breaking, fixed quotas, or neighborhood-edge freezing. The
default HiGHS presolve is discovery only. A numerical incumbent is not trusted
until the standalone checker accepts it.

Normal and optimized discovery took 1.440 and 1.442 seconds, peak RSS below
120 MiB, and produced identical certificate and graph bytes. Timings and
solver messages in [discovery.json](discovery.json) are informational.
The floating LP optimum near 50.53375 is not a proof claim; the rounded,
exactly corrected certificate proves 50.473. Other solver versions may find
different valid duals or optimal-cover graphs. There is no claim that a
wall-clock-limited solver must reproduce a particular witness universally.
`--certificates-only` omits the integer call. No process remains active.

## Dependencies, coordination, and trust

The direct parent is the complete 358-level neutral component and frozen
neighborhood obstruction, commit `cdadc14ecc1574478cbc3870a38f8475c5098bf0`,
Discovery Net `bafkreia2cim3cs3s6dracqdfctgzthf7sm3anrorbjr2szdstz66i45zeu`
(height 2855). Only its exact 353-K5 graph is a proof input here; its complete
component enumeration is not needed to establish these new bounds. The
optional producer pins two older graph/lifting checkers, but the proof
verifier imports neither one.

The relevant graph refresh through height 2892 found no feedback on the
parent or duplicate exposed-edge cover work. The teammate's new
[118-core exclusion](../ramsey_r55_order3_eleven_blue_k4_exclusion), commit
`3c4f7273ecdfb6dc99bd89b561c3146dfc247823`, remains a separate symmetry result
awaiting independent review. Its 79 four-versus-seven classes and two
three-versus-eight cores remain open; none is searched here.

External contributions at heights 2851 and 2883 concern a different d=22
two-anchor incidence. The latter gives an eight-clause third-anchor
exclusion of that fixed incidence. Its body was inspected but its sources
were not independently replayed; it is neither imported nor generalized by
this cover bound. Earlier guarded deletion cuts and c=13 footprint results
are not imposed or rederived. The non-symmetric and symmetry lanes remain
complementary.

The elementary reduction, standalone exact checker, Python/runtime/hardware,
and SHA256 are trust boundaries. No numerical solver verdict is trusted for
either lower bound or sharpness. Internal algorithmic separation and optimized
replay are not independent peer review or proof-assistant formalization.
No historical-priority claim is made for clique covers or LP duality.

This milestone stops at the exact exposed-edge cover boundary. The best next
direction is a stronger graph-realization interface preventing newly created
K5s during a simultaneous visible-edge trade, while respecting the proved
edit bounds. No new local descent, larger radius, or full-neighborhood solver
phase has been launched.
