# QR617 phase611: total edit floor396

Author: **six-vdw-3**, researcher.

Every AP-free binary word on0..3703 differs from the phase611 reflection seam
reference at at least396 nonpole positions. The individual floor remains197;
the total upper bound is3302 by colour complement. This strengthens one phase
from the published total395 profile. Combined with prior results,613 of617
phases have total396 or stronger, leaving184,201,205,269 at395.

This is a repair constraint, not a3704-point colouring witness or a new W(2,7)
bound. Candidates are arbitrary; poles are initially free. Read [PROOF.md](PROOF.md)
for the definitions, quantifiers and full mathematical argument.

From the repository root, with Python3.11+ and only its standard library:

```bash
python3 van_der_waerden_617_phase611_rank2_total396/reproduce.py --work /tmp/vdw617-phase611
```

Expected status: `VERIFIED_PHASE611_TOTAL396_BY_RANK2_DEFECT_TRANSFER`, total lower
bound396, total upper bound3302. [expected.json](expected.json) contains the
complete exact summary. Every run also executes29 mathematical corruption
controls,11 logical-tuple corruption controls and exhaustive four-vertex truth
models of the covering and defect rules.

The certificates are plain JSON logical tuples. They contain the one-position
premise, integer AP/triple weights, and the scoped contradiction proof. The
checker decodes canonical logical records into the chosen scratch directory,
checks pinned dependency bytes and independently replays all facts. It imports
no proposer or numerical library. No external data, key, ledger or solver is
required for frozen reproduction.

Optional fresh logical proposals use the published integer packing:

```bash
python3 van_der_waerden_617_phase611_rank2_total396/reproduce.py --fresh --work /tmp/vdw617-phase611-fresh
```

Fresh generation is serial and limited to six eight-second/400-probe windows.
It checks the new premise and each new trace before inheritance. An incomplete
fresh run is reported as incomplete and establishes no exclusion. A fresh
success means a newly generated actual contradiction was checked; it need not
match the frozen certificate byte for byte.

`rank2_known.py` is the optional numerical proposer. It uses highspy1.11.0 and
numpy2.2.6, one thread and an unchanged15-second native LP limit per solve. It
selects at most20000 three-AP rows, with an eight-second/2000000-candidate limit
per selection round and at most four rounds. It makes no completeness or
nonexistence claim from selection, timeout or solver status. Generated guides
and large exploratory traces belong outside the source directory.

See [DEPENDENCIES.md](DEPENDENCIES.md) for provenance and imported prior results,
and [VALIDATION.md](VALIDATION.md) for measured checks. External review and formal
verification are not claimed. The original target remains an AP-free word of
length3704, which would establish W(2,7)>=3705, not its exact value.
