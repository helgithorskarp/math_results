# Fixed Steiner repairs: the empty parents must cover at most fourteen points

Actual author **six-code-2**, role **researcher**.
For the literal 68-block D, with zero noncontained y-tails and exactly
four unrepresented deleted D-parents H, any packing of size at least 69
requires |union H|<=14. All 72,165 quartets with union>=15 are bounded
by 68, with sharp 68 for unions 15/16 and sharp 67 for union 17.
See the precise hypotheses and ordinary proof in [PROOF.md](PROOF.md).
This does not change the unrestricted endpoint A(18,6,5).

The eight standalone Python sources use only the standard library;
Python 3.10+ is required for integer bit counts and dictionary unions.
The author's execution version is recorded in [EXPECTED.json](EXPECTED.json).
Run from this directory, choosing fresh generated directories outside
the repository. Keep native threads one and the existing 1CPU/2GiB scope.

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -B replay.py --mode normal --work /tmp/union-ge15-normal
python3 -B replay.py --mode optimized --work /tmp/union-ge15-optimized --normal /tmp/union-ge15-normal
```

Each replay runs 42 ordinary children serially and takes several minutes
in the author's one-CPU scope. Every child retains its original 60-second
and two-million-state guards and a 60-second process guard. Completed
case journals and failure receipts are retained; an incomplete stage
does not establish a mathematical bound. No resource escalation is
needed for the reported completed runs.

For campaign use, set `DISCOVERY_OPERATIONS_STATE` to the existing
operations-state directory. Every child then observes its PAUSED and
HANDOVER markers read-only. This optional path is unnecessary outside
the campaign and never modifies host, accounts or controls.

Expected completion is `COMPLETE_SOURCE_ONLY_ALL13_CASES` in both
`JOURNAL.json` files; the optimized journal additionally records
`whole_normal_optimized_equal: true`. Both entire `EXACT_RESULT.json`
files must have the same bytes. All finite/cover packets and every
case's whole core/graph/positive packets, all mathematical summaries
and full ordered traces are compared. Timing/RSS and a verified raw
producer-summary binding are the only permitted volatile exclusions.
[EXPECTED.json](EXPECTED.json) records the full result pin, complete
physical fields and compact packet pins. [PRIOR_EXPECTATIONS.json](PRIOR_EXPECTATIONS.json)
freezes the prior invariant mathematical records before the cold runs.

The small input fixtures and literal maximum witnesses are public.
The several gigabytes of generated core/graph packets are regenerated
locally, never shipped in this source bundle. All algorithms are by
the same author; independent-person review and priority remain pending,
and the ordinary completeness bridges are unformalized. Reproducing
the credited ACL69 baseline is prior-art validation.
