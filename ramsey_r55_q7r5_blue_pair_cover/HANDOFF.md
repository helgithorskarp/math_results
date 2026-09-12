# Four complete full43 receivers; original c000004 remains UNKNOWN

The new physical restriction is: the blue cross edges between the two prescribed blue K4 blocks form a matching of size at most three. All 93 orbit types outside this condition have actual checked tail refutations and an explicit restriction/relabeling bridge into the original physical scope.

The original ID is `bo1-q7-r5-c000004`. The complete residual consists of:

| representative | blue cross-matching size | labeled matrices | tail evidence | full43 status |
|---:|---:|---:|---|---|
| 31711 | 3 | 96 | literal SAT tail | UNKNOWN |
| 31743 | 2 | 72 | literal SAT tail | UNKNOWN |
| 32767 | 1 | 16 | literal SAT tail | UNKNOWN |
| 65535 | 0 | 1 | undecided | UNKNOWN |

Every full receiver includes all five red K4 blocks, both blue K4 blocks, the literal 15-core, the fixed representative matrix, all physical K5 prohibitions and the entire 23-tail red-K4 exclusion. There are 740 free physical edge variables and 446 ordering auxiliaries. All incidences to the twenty red-block vertices remain free. No saved tail is imposed. The only extra ordering acts on the five red blocks using core signatures; it never competes with the fixed blue-pair matrix.

The zero-blue-edge tail was stopped without a verdict after the forbidden-geometry theorem was complete. Its exact input, STARTED marker and unfinished trace are preserved locally and are not evidence. Resolving that relaxation is not required to use this four-unit physical cover. The next endpoint is the original task, through the complete full43 units.

## Exact input generation

`FULL_FRONTIER.json` pins every complete receiver's input digest and separate physical audit. From this directory, for a fresh receiving directory:

```sh
mkdir /tmp/r55-full
for rep in 31711 31743 32767 65535; do
  mkdir /tmp/r55-full/pair-$rep
  python3 -B bridge.py emit --representative "$rep" --output /tmp/r55-full/pair-$rep/input.cnf
  python3 -B verify_full.py --representative "$rep" --input /tmp/r55-full/pair-$rep/input.cnf
done
```

These are complete physical work units; emitting or starting one does not decide it. The independent audit covers all 962,598 five-subsets, all 8,855 tail four-subsets, and the 465 comparator bit positions, with fixed-edge simplification and the proved redundancy of all-red five-sets wholly in the red-K4-free tail.

## Admission and parent retirement

A full43 model must be decoded into all physical edge bits and checked against the literal target definition. `problem.check_graph(rep, graph, full=True)` performs this check for the receiver's labeling. A 23-vertex tail word is never accepted in place of that graph.

For negative admission, store each actual full proof as `/tmp/r55-full/pair-REP/proof.drat` alongside its exact input, then run:

```sh
python3 -B bridge.py join --run /tmp/r55-blue-pair-replay --drat-trim /tmp/r55-drat-trim/drat-trim --parent-root .. --catalog /tmp/r55-blue-pair-input/r44_15.g6 --full-dir /tmp/r55-full --output /tmp/r55-final-join.json
```

The join rechecks every one of the 93 actual tail proofs, the entire original-source map, each presented full input, its independent physical audit, and its actual proof. Missing full proofs remain UNKNOWN. Only four successful full refutations permit `CERTIFIED_ORIGINAL_TASK_UNSAT` and `original_tasks_excluded: 1`. The tested pass-31 join returns `CERTIFIED_SUBDIVISION_PARENT_UNKNOWN` and zero original exclusions.

The four full formulas use an allowed relabeling cover, not literal equality to the old root-ordered parent formula. PROOF.md proves that every original-task model maps into one of them. They retain the same graph, core and monochromatic blocks. By contrast, the separate core-exchange normal form may redirect to another original task and requires its own global join; its clauses have not been appended here.

All original registry counters remain unchanged: 518 accepted exclusions, 2,188,660 UNKNOWN. The 956 q8 jobs, q8,r8 imported edge-119 branch and mixed-premise join, and the q10 99/161 physical-child ledger are unchanged. The 94 q10 color redirects are not exclusions. This package does not restart the parked cohort-0 gate or any historical computation.

The main first-pass milestone is the complete forbidden-geometry decision and exhaustive four-unit residual. A sequence of isolated new children is not the next milestone: the remaining trial requires an original-carrier consequence and, by its third pass, closure of a whole original task/family or a verified target graph.
