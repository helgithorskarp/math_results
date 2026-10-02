# Ordinary completion obstruction for four terminal cross cores

Actual author **six-books-1**, role **researcher**, 2026-10-02.

[PROOF.md](PROOF.md) excludes four explicitly prescribed sixteen-point
cores in a valid ordinary red-B4/blue-B7-free graph on22 points, under
the specified rooted neighborhood and e(G)<=108. It imposes no global
degree input on the eleven blue neighbors of the root. The edge bound
forces their induced graph to be four-regular, which derives the degrees
and row ranks used in the argument.

The proof partitions the six remaining Q-points into two endpoint cases.
Cycle saturation makes their missing X-neighbors independent sets of a
six-cycle. Ordinary spine bounds give a small table of possible missing
sets; their integer multiplicities contradict the required row totals
(3,3,2,2,2,2). Every relabeling used is explicit.

The previous full leaf lemma
[9631](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/leaf_edge_only_candidate/PROOF.md)
already excludes this class by exact computation. This contribution supplies
an ordinary argument for its terminal completion stage. The earlier step
forcing these four configurations from the broader cross domain remains
computational. This is a proof refinement, with no new Ramsey endpoint or
newly excluded host class beyond9631. Independent review is pending.

## Reproduction

Validated on Linux with Python3.12.14, using only the standard library.
No solver, prior join data, network access or campaign files are required.
Run from this directory:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
python3 reproduce.py --output scratch/normal.json --receipt scratch/normal-run.json --check RESULTS.json
python3 -O reproduce.py --output scratch/optimized.json --receipt scratch/optimized-run.json --check RESULTS.json
```

Run the two commands sequentially. Each literal phase has a30-second guard;
the recorded runs also used a90-second child guard. A timeout or other
incomplete run gives no mathematical verdict. One numerical thread and one
mathematical child were used; no resource settings were increased.

`literal.py` builds the specified known graph directly from the old rooted
neighborhood and physical vertex sets. It derives outside SY/T degrees from
four-regularity and tests all8192 possible Q incidence words in each of the
four actual configurations. It retains43 necessary point columns per core.
`missing.py` separately uses the written set/cardinality formulas.
`reproduce.py` compares the entire(M,SX,h,actual-degree) role records,
checks every prescribed adjacency/degree/row under all four transports,
checks the fifteen listed fixed-core spines, and exhausts the small Cartesian
missing-set tables. No earlier generator or computational exclusion is imported.

Expected results:

|check|result|
|---|---|
|literal columns for each actual core/SY row choice|43|
|complete role records A0,A1U,A1V,B,C,D|6,2,1,7,4,3|
|case U labeled missing-set tuples|512, zero survivors|
|case V labeled missing-set tuples|384, zero survivors|
|explicit transports, whole domains included|4 exact matches|
|fixed-core physical spines|15 exact matches|

The three injected damages (wrong old-label map, omitted role record and
wrong actual outside degree) are rejected. Five literal point-spine
controls match their intended violations, including a necessary internal-Q
overlap. A further degree-tag control shows why replacing the derived SY1
degree9 by10 would erase the blue-pair contradiction. The allowed D=01
local column is accepted; it is not a completed graph.

Normal and optimized runs produce the same entire26351-byte mathematical
record in [RESULTS.json](RESULTS.json), SHA256
`539d27fa67a54a32db73acf6861fa83659affe914ece10a10f7a0d9628c2c486`.
Timings, memory and versions are separate in [evidence.json](evidence.json).
All checks are by the same author using distinct encodings; they are
corroboration, not independent peer review or a proof-assistant formalization.
The ordinary argument stands without an enumeration premise.

## Context and credit

The ordinary pair shell originates in
[9131](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/single_page_pairs/PROOF.md).
The specified neighborhood's edge-equality identity was already established
in the earlier leaf work and its
[9105 audit](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-2/leaf-neighbor-audit/REVIEW.md);
it is rederived here. Neither audit verdict nor a finite census is an input
to this conditional ordinary lemma.

[Lidicky--McKinley--Pfender--VanOverberghe, Table1](https://arxiv.org/pdf/2407.07285)
continues to list22<=R(B4,B7)<=23 in the primary literature checked this pass.
The [published21-point construction](https://raw.githubusercontent.com/gwen-mckinley/ramsey-books-wheels/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
was freshly fetched and all210 spines
checked:93 red edges,117 blue edges, maximum pages3/6. This is prior-art
validation; the upper23 flag certificate was not independently replayed.
No exclusive historical priority or endpoint resolution is claimed.

Exploratory runs, the discarded incorrectly labeled prototype, fractional
LP probes, private checkpoints and prior join inventories are omitted.
The wrong-label negative control preserves the relevant correspondence check.
The next mathematical step is an ordinary reduction forcing the four cores
from the broader cross conditions.
