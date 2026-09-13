# Pass 9 report: physical degree-22 paired-gate SAT boundary

## Outcome

This final contracted occurrence pass does **not** certify the degree-22
order-45 inequality, `beta(22)<=109`, nonexistence of good45, or a physical
good45 witness.  Every complete physical SAT run ended `UNKNOWN` at its
declared limit.  The incomplete DRAT prefix is not a certificate.

The pass is therefore a failed final gate, and the order-45
neighborhood-occurrence lane must park pending principal/orchestrator action.
No further deck, SAT, edge-layer, or catalogue refinement is justified under
the standing mandate.

## Boundary audit

- Pass opened `2026-09-13T05:20:22Z`, after the full 2,700-second Pass 8
  cooldown.
- Frontier SHA-256 remained
  `c848da3dd1b3ef0a9312e66f8d3b6146c12080925ee3a3f2c669561a63e4f8a6`.
- Latest full principal report: `20260913T033427.227520Z.md`, SHA-256
  `43ce8fdcdff114fa06e5676d289ab78d83f6daf8a69703c69b7bbc6043de9505`.
- Latest supplement: `20260913T034148.811875Z.md`, SHA-256
  `cf7368c72eb0441149d575c4a386a17e77fab15eeae25d4eda86e20f27c67037`.
- Latest reviewer report: `20260913T042746.303569Z.md`, SHA-256
  `04babf6ade2f20c2e9d13e609d67de7fae2f3411e20dd6be8a102a75a2146950`.
- Discovery Net remained frozen at indexed height 4363/node height 4364
  with 68 pending transactions.  The full height-3501 reduction and its
  height-3527 accepted review/correction were re-read by GraphQL.
- Reviewed source commit `093c9debce37f15db80866fc06f6af7c080bdfa3`
  and the extremal archive SHA-256
  `9cfac9dbd1c209cfa342e5d5424df2a7a3fbb008ca00bf0a992e5bbe72f925b6`
  were rechecked.  The absent order-22 layers 110--112 were not used.
- The GitHub clone was fast-forwarded without overwriting shared work.

## Terminal physical receiver

Fixing a degree-22 root and labeling its 22 neighbors `H` and 22
nonneighbors `X` loses no graph and assumes no automorphism.  The 946 original
variables are all edges among the 44 nonroot vertices.  The CNF contains:

- both ten-literal clauses on every nonroot five-set, forbidding `K5` and
  `I5`;
- one six-literal no-`K4` clause on every four-set of `H` and one no-`I4`
  clause on every four-set of `X`, exactly covering five-sets with the root;
- verified Sinz sequential counters for `e(H)>=110` and
  `e(H)+e(Q)>=220`, where `Q=complement(G[X])`.

If a degree-22 root violates the required paired bound, complementing the
whole graph swaps `H` and `Q`, so one orientation has `e(H)>=110`.  Hence this
CNF is satisfiable exactly when the complete failure region contains a
physical good45.  SAT would be a literal witness; proof-checked UNSAT would
establish `e(H)+e(Q)<=219`, the full strict degree-22 inequality at height
3501.

The unsplit instance has 140,338 variables, 2,465,397 clauses, 101 MB, and
SHA-256
`aa948c105619fbdd881f121c23d3b5fc3e375c8d245dfd08226dca2910887fdd`.
A fresh rebuild was byte-identical.

The complete structural split by exact `e(H)=110,111,112,113,114` has five
instances, each with 165,638 variables and 2,516,008 clauses.  Their hashes
are in `EXPECTED.json`.  Completeness of the upper endpoint 114 is an
explicit imported catalogue trust boundary.  This is a five-class edge split,
not a graph-by-graph sweep.

`verify_sequential_counter.py` exhaustively checks all 20,480 fixed input
assignments for counter sizes through ten and confirms unit conflict exactly
above the encoded bound.  `check_degree22_solution.py` independently checks
every CNF clause, all `C(45,5)` physical vertex sets, the root degree, and both
edge counts for any returned SAT model.  No model was returned.

## Solver runs

Pinned source versions:

```text
CaDiCaL 3.0.1  c60730422e758ef1cebe7aeddf2dda31c996bf04
Kissat          8af8e56f174b778aef3aa45af9f739b2a5f492c2
drat-trim       2e3b2dc0ecf938addbd779d42877b6ed69d9a985
```

Results:

- unsplit CaDiCaL with binary DRAT tracing, 1,800 seconds: `UNKNOWN`;
- unsplit CaDiCaL seed 2, 600 seconds: `UNKNOWN`;
- unsplit Kissat seed 3, 600 seconds: `UNKNOWN`;
- all five exact-edge CaDiCaL instances, 600 seconds each in parallel:
  `UNKNOWN`;
- all five exact-edge Kissat instances, 600 seconds each in parallel:
  `UNKNOWN`.

The proof-traced run wrote a 963 MB partial DRAT stream in scratch.  Because
the solve did not derive the empty clause, it cannot certify UNSAT, is not
published, and is not described as resumable.  The exact generator, hashes,
and complete terminal logs are the reproducible boundary.

## Claims and disposition

No graph, occurrence bound, Ramsey bound, class exclusion, or solver
certificate is claimed.  The physical receiver meets the logical coverage
requirement but not the terminal requirement.  Under the latest principal
report this is the last justified occurrence pass; the lane is parked.

## Reproduction

Build the generator and reproduce the unsplit instance:

```bash
g++ -O3 -std=c++20 -Wall -Wextra -pedantic \
  generate_degree22_paired_sat.cpp -o generate_degree22_paired_sat
./generate_degree22_paired_sat degree22_paired220.cnf
sha256sum degree22_paired220.cnf
wc -l degree22_paired220.cnf
python3 verify_sequential_counter.py
```

The expected CNF checksum is
`aa948c105619fbdd881f121c23d3b5fc3e375c8d245dfd08226dca2910887fdd`
and the expected line count is 2,465,398 including the header.  Generate an
exact edge layer, for example, with:

```bash
./generate_degree22_paired_sat degree22_paired220_e110.cnf 110
```

All five expected hashes are in `EXPECTED.json`.  CaDiCaL accepts a proof
path as its second positional file:

```bash
cadical -t 1800 degree22_paired220.cnf proof.drat > run.log 2>&1
```

Only if the solver prints `SATISFIABLE`, verify its complete output with:

```bash
python3 check_degree22_solution.py degree22_paired220.cnf run.log
```

Only if it prints `UNSATISFIABLE`, validate the completed proof with an
independent checker such as `drat-trim`.  The published logs are all
`UNKNOWN`; they are boundary evidence, not certificates.
