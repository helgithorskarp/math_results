# A sharp two-common-neighbor lemma; four pair-color extensions remain open

For a blue edge joining two vertices with empty red signatures to three
red triangles, **at most two other uniformly attached vertices can be
blue to both ends**. Each common blue neighbor is red to at least two
triangles, and two such neighbors cannot both miss the same triangle.
[PROOF.md](PROOF.md) gives the short hand proof.

Two 13-vertex graphs show sharpness on both surviving eleven-cycle
minority cores. A 14-vertex graph shows that the blue-edge hypothesis is
necessary: a red empty pair can have three common blue fixed neighbors.
These small graphs are local certificates, not Ramsey (5,5;43) targets.

The complete four-case application splits the first two empty fixed
vertices by the color of their edge, for each surviving minority core.
**All four cases returned UNKNOWN at 60 seconds.** This pass gives no
additional extension exclusion and no lower-bound improvement.

| core | pair color | clauses | variables | bounded result |
|---:|---|---:|---:|---|
| 11 | blue | 617380 | 34268 | UNKNOWN |
| 11 | red | 617208 | 34268 | UNKNOWN |
| 13 | blue | 617380 | 34268 | UNKNOWN |
| 13 | red | 617208 | 34268 | UNKNOWN |

## Solver-free reproduction

CPython 3.11.2, standard library only. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -B pair_audit.py --work /scratch/new-r55-pair/controls
cmp pair_controls.json /scratch/new-r55-pair/controls/pair_controls.json
python3 -B -O pair_audit.py --work /scratch/new-r55-pair/controls-O
cmp pair_controls.json /scratch/new-r55-pair/controls-O/pair_controls.json
python3 -B inspect_fixtures.py --fixtures . --report /scratch/new-r55-pair/fixtures.json
cmp fixture_report.json /scratch/new-r55-pair/fixtures.json
python3 -B -O inspect_fixtures.py --fixtures . --report /scratch/new-r55-pair/fixtures-O.json
cmp fixture_report.json /scratch/new-r55-pair/fixtures-O.json
```

The two fixture checkers independently inspect the blue-pair examples.
The generic matrix inspector also checks the red-pair counterexample,
and imports no generator or SAT code. It checks every five-set, pair
under the action, signature, and literal common blue neighborhood.

| local certificate | vertices | red edges | pair color | common blue fixed neighbors |
|---|---:|---:|---|---:|
| [core11.edges](core11.edges) | 13 | 36 | blue | 2 |
| [core13.edges](core13.edges) | 13 | 39 | blue | 2 |
| [red_pair14.edges](red_pair14.edges) | 14 | 43 | red | 3 |

## Reproducing the bounded full extension test

Use the complete repository checkout with its sibling dependencies.
Keep large generated artifacts outside Git:

```sh
python3 -B sweep.py --work /scratch/new-r55-pair/full \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim \
  --solve-seconds 60 --replay-seconds 300
python3 -B verify_pair.py --source-work /scratch/new-r55-pair/full \
  --work /scratch/new-r55-pair/verification \
  --drat-trim /path/to/drat-trim --replay-seconds 300
```

Expected reference outcome: `excluded=[]`,
`open=[c11_blue,c11_red,c13_blue,c13_red]`; four exact reconstructions,
five rejected formula mutations, and **zero proof replays** because
there are no completed refutations. Wall-clock cutoffs can change
bounded solver outcomes; an UNKNOWN result proves neither feasibility
nor infeasibility.

`sweep.py` regenerates the entire accepted parent and has its C++ auditor
reconstruct every clause. It rebuilds both signature bases and both
many-empty bases, compares all reviewed hashes, then appends the pair
clauses. `pair_audit.py` reconstructs literal primary edge-orbit meanings
and independently checks the complete prefix and tail. No new auxiliary
variable, symmetry normalization, fixed graph, or degree profile is
introduced. Both degree bounds and all original constraints remain.

The two-worker sweep saves each case atomically. Identical-contract
`--resume` retains completed UNKNOWN cases at their original limits.
A `STOP` file prevents later cases from starting; active cases finish.
All four reference cases and the fresh verification are complete, with
no active background job. Partial UNKNOWN traces are not resumable
solver states or proof certificates.

Reference elapsed time: 149.175161 seconds; largest child RSS: 259636
KiB. Fresh reconstruction and verification took 30.605646 seconds.
Source and tool hashes, exact formula hashes and outcomes are in
[result.json](result.json); fresh checks are in
[verification.json](verification.json). Only source, compact reports
and small edge lists are public. Approximately 25 MB formulas, partial
traces, logs, binaries and caches remain outside Git.

Tools: GCC 12.2.0, with the parent checker compiled using
`-std=c++17 -O2 -Wall -Wextra -Wpedantic -Werror`.
Kissat source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`, binary
SHA256 `2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`.
drat-trim source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, binary
SHA256 `9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.
The runner would require full DRAT verification for any future UNSAT
outcome and a literal edge-list check for any target model.

## Dependencies and scope

The [two-empty-signature reduction](../ramsey_r55_order3_eleven_empty_split)
now has an [accepted independent review](../ramsey_r55_order3_eleven_empty_split_review1),
evidence commit `928089851dfc14e95e858623cf641a99d08ab62d`, graph artifact
`bafkreiamo3ro6iwj4dwjy2m7lktc5noxe2zjtir3geuupepwjykwugoury`.
It supplies the selected pair for the full-graph application.
The inherited [core cover](../ramsey_r55_order3_eleven_minority_core),
[signature reduction](../ramsey_r55_order3_eleven_signature_bound), and
[parent formula](../ramsey_r55_order3_eleven_cycle_obstruction) likewise
have accepted independent reviews. The parent uses R(4,5)=25.

The standalone lemma needs none of those reductions or external Ramsey
values. Its application and formula audit inherit them. The current
lemma and new clause bridge await independent review; ordinary
unformalized reasoning and exact runtime/compiler/hardware remain
trust boundaries. The four bounded UNKNOWN results contribute no
refutations. Both cores, both pair colors, and the four-versus-seven
split remain open. Further pair subdivision or a different minority-core
phase is outside this completed milestone.
