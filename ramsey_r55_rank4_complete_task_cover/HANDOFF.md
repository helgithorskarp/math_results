# Physical completion interface for team-r55-1

This is a complete queue of 10,959 target-facing tasks for the entire conditional rank-four 20+23 branch. It replaces choosing one occupancy template with an exact canonical cover. This contribution does not start the construction lane or run a solver on any target task.

`row_cover.tsv` has columns `code`, `zero`, `orbit_size`, `support`, `triples`, in strictly increasing numeric code order. Use `code` as the stable task identifier; the one-based data-row index can shard the queue. Each row means **all** allowed column supports and multiplicities, not one fixed cross matrix. `orbit_size` counts A multiplicity profiles represented by the row, not good graphs.

From the repository root, generate one complete instance:

```bash
python3 -B ramsey_r55_rank4_complete_task_cover/model.py \
  --row-code 24575 --cnf /absolute/private/path/task24575.cnf
```

The output path must be new and its parent must exist. The command reports exact variable/clause counts, bytes and SHA256. The representative task is an ordinary row profile and is not selected for presumed feasibility. Any of the 10,959 table codes is accepted. Target calls keep all 443 internal edges and all 23 column labels as variables. They include every physical five-set and the reviewed necessary conditions. A CNF is approximately 80–91 MB for the four audited representatives; keep generated formulas, models and proofs outside the repository.

If a solver returns SAT, validate and decode its complete DIMACS model:

```bash
python3 -B ramsey_r55_rank4_complete_task_cover/decode.py \
  --row-code 24575 --solver-output /absolute/private/path/task24575.out \
  --output /absolute/private/path/target43.json
python3 -B ramsey_r55_rank4_complete_task_cover/verify_target.py \
  /absolute/private/path/target43.json
```

The decoder requires a complete consistent assignment and exactly `s SATISFIABLE`, checks all base and gate clauses, constructs the physical graph, and independently checks all 962,598 five-sets before writing output. `UNKNOWN`, partial assignments and fabricated SAT models that violate a physical five-set are rejected. The final verifier requires exactly 43 vertices. An UNSAT exit alone is not a certified branch decision: retain and independently check its proof, then aggregate decisions against this exact table. A timeout decides no task and no branch.

For direct construction code, a canonical factor assignment uses exactly:

```json
{
  "row_code": 24575,
  "columns": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 10, 11, 12, 13, 14, 15],
  "internal_hex": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
}
```

This schema example is **not** a good43: its internal edges are all blue. The internal field has exactly 111 lowercase hexadecimal digits and represents an integer below 2^443. Its bit k colors the k-th same-side pair in lexicographic order among pairs 0≤i<j<43, least significant bit first. Thus its first 190 bits are A edges and its last 253 are B edges. `model.py --data parameters.json` reports necessary base-filter acceptance and constructs the graph; that acceptance alone is not a candidate certificate.

The physical graph schema is exactly `{ "n": 43, "red_hex": ... }`, with 226 lowercase hex digits representing 903 bits. Bit k colors the k-th pair in lexicographic order among all 43 vertices. The unused leading bit must be zero.

To transport another factor presentation into the cover, supply `normalize.py input.json` with exact fields `rows` (20 spanning labels), `columns` (23 spanning labels), and `internal_hex`. Rows must obey the necessary caps. The result contains `parameters`, `new_to_old` (the 43-vertex permutation), both linear label maps, the physical graph, and `base_filters_hold`. Transport is defined even for a graph failing necessary filters, and does not assert the graph is Ramsey.

The four full-support A tasks still admit B labels zero, missing labels and multiplicities three through five. Do not remove those entire tasks based on the known doubled-profile exclusion. Do not fix columns 1,2,4,8 after canonicalizing the rows; that additional restriction is not justified by this cover.

This covers graphs admitting a rank-four cut, not all good43. The rank-five distance-sieve retained interface and higher-rank cases remain separate. The saved B23 projection and its fixed-witness completion route remain parked; no data from that projection selects these tasks.
