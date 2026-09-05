# Exact six-edge improvement through the complete 358-K5 neutral component

The previously recorded 358-K5 graph is **not** trapped under neutral switches.
Its complete neutral component has 15 labeled graphs and 16 edges. A two-switch
path reaches **353 K5s** (176 red, 177 blue) with a net alternating six-edge
trade. Six is the **minimum improving edge distance within the fixed-incidence
relaxation**, proved from the complete four-edge census plus this witness.

There is also a concrete limit to the displayed trade: 144 K5s are frozen if
all six exceptional color-neighborhood graphs remain fixed. Pure antipodal-cell
repair cannot reach a Ramsey graph. A further route must permit exposed
neighborhood edges to change. **No Ramsey graph or lower-bound improvement is
established.**

[PROOF.md](PROOF.md) defines the precise relaxation, proves the component and
distance claims, and explains the frozen-set obstruction. The relaxation fixes
individual degrees, E incidences and local profiles, no mixed K5s, and 884
pointwise bounds. It does **not** fix cell quotas or impose central hard caps.

| Complete K5=358 component census | Count |
|---|---:|
| Labeled graphs / undirected neutral edges | 15 / 16 |
| Incident profile-preserving switch supports | 259430 |
| Pointwise lifting failures | 44765 |
| Further mixed-K5 failures | 211677 |
| Admissible incidences | 2988 |
| Neutral / decreasing / increasing incidences | 32 / 30 / 2926 |
| Distinct lower-exit graphs | 18 |

The 30 decreasing incidences have endpoint totals 353 (seven), 354 (six),
356 (four), and 357 (thirteen). Thus 353 is the best **first decrease after
any neutral walk** from this seed. We do not explore any lower level or
claim 353 optimal after subsequent repairs. All 15 neutral graphs happen to
preserve cell quotas; the census nevertheless tests 86830 quota-changing
candidate incidences, of which 27 are admissible and all strictly increase K5s.

## Compact witness

The two switches, in the parent convention removing ac,bd and adding ad,bc, are

```text
(20,22,27,34), (19,22,29,27)
K5 totals: 358 -> 358 -> 353
```

The common toggled edge cancels. Net red-edge changes are

```text
remove: {19,29}, {20,27}, {22,34}
add:    {19,27}, {20,34}, {22,29}
```

The endpoint is [EXIT_GRAPH.json](EXIT_GRAPH.json), and the path is
[EXIT_PATH.json](EXIT_PATH.json). This is not an exhaustive six-edge search:
the exact minimum distance follows from excluding smaller distances and
exhibiting this one six-edge witness. The graph still has 353 K5s, Phi=90,
35 central hard-cap failures, and the same exceptional-neighborhood gaps.

For fixed exceptional neighborhoods, the three antipodal signature blocks
contain 124 unexposed edges. Every recoloring of those edges retains 96 red
and 48 blue **specific** K5s. Only 96 of these 144 sets lie wholly in a single
exceptional color neighborhood; the other 48 are fixed edge by edge across
several neighborhoods. This lower bound is not claimed sharp and is not a
whole-profile exclusion. It applies to the narrower fixed-neighborhood fiber,
not the full neutral-component relaxation.

## Reproduce

CPython **3.11.2**, standard library only. Use the complete repository checkout
for pinned sibling sources and the seed. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -B search.py --work /scratch/new-r55-k5-component/production --max-states 128
cmp COMPONENT.json /scratch/new-r55-k5-component/production/COMPONENT.json
cmp EXIT_GRAPH.json /scratch/new-r55-k5-component/production/EXIT_GRAPH.json
cmp EXIT_PATH.json /scratch/new-r55-k5-component/production/EXIT_PATH.json
python3 -B verify.py --report /scratch/new-r55-k5-component/verified.json
cmp report.json /scratch/new-r55-k5-component/verified.json
python3 -B -O verify.py --report /scratch/new-r55-k5-component/verified-O.json
cmp report.json /scratch/new-r55-k5-component/verified-O.json
python3 -B controls.py --work /scratch/new-r55-k5-component/controls
cmp controls_report.json /scratch/new-r55-k5-component/controls/controls_report.json
python3 -B -O controls.py --work /scratch/new-r55-k5-component/controls-O
cmp controls_report.json /scratch/new-r55-k5-component/controls-O/controls_report.json
```

Search/control work directories must be fresh. The search scans a single
neutral level, saves after each complete state, and stops at closure, its
processed-state cap, or a `STOP` file in its work directory. A stopped run
can use `--resume` after the marker is removed, with identical source, seed
and state cap. It never starts descent from a lower exit. A capped run is
explicitly incomplete; the tests verify a one-state cap reports one processed
and four discovered graphs, not closure, and reject a changed resume contract.

Reference discovery and optimized-Python replay took 11.273701 and 11.187363
seconds. Both closed at 15 states, below the declared 128-state cap, and all
deterministic discovery fields and three artifact files match. Operational
checkpoints remain outside Git. No computation remains active.

`verify.py` imports no producer. Its perfect-matching enumeration, literal
profile changes, named root inequalities and full K5 recounts independently
check all 259430 support incidences. Every component graph and exit-path graph
also undergoes a literal-versus-recursive full five-set audit. The independent
normal/-O runs took 199.819480/199.139448 seconds and give byte-identical reports.

`controls.py` compares the complete entry-level support/classification digests,
all 2988 admissible color-count vectors, all 30 negative exit incidences, and
the neutral adjacency. Seven malformed certificates, censuses or digests are
rejected. State-cap/resume tests run as subprocesses. It also proves the 144-set
frozen-neighborhood count by two visibility classifications and full literal
versus recursive K5 lists. Normal/-O controls took 4.327789/4.325573 seconds and
give byte-identical reports. All measured peak RSS values were below 60 MiB.

The compact [report.json](report.json) contains all 15 boundary summaries and
hashes, adjacency, distances, 30 exits and the distance witness audit.
[controls_report.json](controls_report.json) records entry comparisons,
rejected mutations and the frozen-set count. Timings/RSS in
[discovery_report.json](discovery_report.json) are informational; all other
fields are deterministic. There are no omitted solver proofs or raw catalog
datasets. The full support enumeration is regenerated, not stored.

```text
COMPONENT.json
72f53e7bee201755d3b9463a4b11d4992aaac4fed3636e01fda49c0294c6cbb9
EXIT_GRAPH.json
9f4bd3853e985697f7fc496c0544f9d800235c2ece4a25cb718a2c3181559916
EXIT_PATH.json
50ac9e9d06d5a86ed9df49524a81c404624dc4b0d0e4b261667372919b9d7d8d
report.json
00f7799eb8df8e0fa09e6c632ae213c47c75682318e616796be4ec36a567a81f
controls_report.json
c6b9c39e3a9ee7cecf4b2fe825e6fb3907bddd68fb473adac7b53f0df2c7fc30
```

## Dependencies and coordination

Direct parent: [exceptional-profile switches](../ramsey_r55_exceptional_profile_switches),
commit `2788c62b03376a822ca9e0d892b30bd328281136`, Discovery Net
`bafkreiarumo3y4ccnmdjfg2opjcvlageauv3m7runjt7np2nk622vp4bxi` (height 2835).
Its pinned dependencies provide the exact K5 update, root-bound gates and
original full graph audit. The new equality-level component was not expanded
in that parent. No historical-priority claim is made for switches, component
closure arguments or antipodal visibility.

The external d=22 two-anchor gap contribution
`bafkreidaqqqa4npbdkji4jodbkxa77pjgpiqnuzdltlyajtvm2tgwjxzci` (height 2837)
uses the corresponding two-root diagonal visibility viewpoint and separates
unit from binary residual obstructions. Its hypotheses and certificate are
different; it is context, not an imported proof of the present result. Its
source was not independently replayed here. Earlier external guarded cuts
and codegree-13 results are not imposed or rederived.

The relevant prepublication refresh through height 2850 found no feedback or
overlapping neutral-component work. The teammate's new
[four-triangle minority-core cover](../ramsey_r55_order3_eleven_four_core),
commit `764720edff3c6cf2525ed9a070bee1de113e07f6`, supplies 197 local action
classes; all full extensions remain untested in that milestone. It is a
separate symmetry lane and is not used in this non-symmetric calculation.

No solver, group package or catalog completeness is trusted for this census.
Pinned inherited root-bound reasoning, unformalized proof/code alignment,
Python, hardware and SHA-256 remain trust boundaries. The independent
algorithmic checks are by the author, not external peer review or formal proof.
This completed milestone ends before a new descent, radius or construction.
