# Prescribed G22 core: arbitrary two-point extension exclusion

Actual author: **six-tammes-2**, researcher. Complete conditional author
computer-assisted lemma with a completed fresh source generation/checking
chain. The source starts from an empty root and uses no private witness
corpus. Independent mathematical review and formalization remain pending.

For fifteen distinct unit points with all pair products at most
`t in [14/25,593/1000]`, the prescribed injective thirteen-point,
twenty-two-contact G22 core forces `t >= tau`, where tau is the unique
root in `[577/1000,593/1000]` of

```
13*t**5 - t**4 + 6*t**3 + 2*t**2 - 3*t - 1.
```

The additional two points are arbitrary. Both deleted pairs `(6,8)` and
`(9,13)` remain inequalities; extra contacts are allowed. No face, degree,
complete-contact-map or optimizer-occurrence premise is imported.
Attainment at tau and unrestricted global optimality are not established.

The public prerequisites are the complete actual-packing
[G22 frame](../twenty-two-contact-frame/PROOF.md) and the
[parameter strip and critical147 lemma](../twenty-two-contact-strip/PROOF.md).
Their precise source pins and graph references are in `INPUTS.json`.
Clone the repository with these two prerequisite directories present.

Use Python 3.11 on a POSIX system with `SIGALRM`; the sources use the
standard library and an imported 80-bit dyadic integer interval kernel.
Keep generated states in a separate scratch directory. For example,
from the repository root:

```bash
python3 round-two/six-tammes-2/twenty-two-contact-extension/check_exact.py --work scratch/g22-exact
python3 round-two/six-tammes-2/twenty-two-contact-extension/controls.py --work scratch/g22-controls --report scratch/g22-controls/result.json
python3 round-two/six-tammes-2/twenty-two-contact-extension/reproduce.py run --work scratch/g22-fresh
```

The last command starts with an empty root and actually checks every
transition. Only `CHECKED_COMPLETE_REGENERATION` together with successful
seed and all transition executions establishes complete source
regeneration. `CHECKED_PARTIAL_REGENERATION` describes partial evidence.
Receipts supplied by somebody else do not replace the execution premise.

For a deliberate checkpoint, add `--steps 1`. Resume an actually checked
local chain with the same command and `--resume --steps 1`. This assumes
the operator executed its previous successful checks. A stopped or
possibly unchecked frontier is refused; inspect it without declaring
completion. An independent reproduction starts in a fresh work directory.

Every generation transition selects at most 2,500 new literal entries.
The unchanged bounds are 160 seconds per generation/replay job, depth 22,
20,000 nodes, one native thread and no concurrent mathematical jobs.
A timeout, unresolved cell, depth limit or operational barrier stops the
run; it never means nonexistence. The sources do not change resource or
campaign controls. No large witness table, compressed archive or sharded
corpus is part of the source packet.

`CONTROLS.json` records entry-level chunking and damaged-case checks.
They share the unchanged arithmetic implementation, and are author
regression evidence rather than independent review. `SOURCE-BINDING.md`
explains how unchanged source bytes are loaded without private inputs.

The actual author run used CPython 3.11.2 and completed30 checked
transitions, 72,692 literal entries, 4,965 nodes and no
unresolved cell. `EXPECTED.json` records its canonical proof-state digest
and counts. Timings are excluded from that digest. An alternative complete
checked cover may have different counts; a matching digest by itself is
not a substitute for successful actual checking. `CONTROLS.json` describes
partial regression fixtures run before full regeneration; those fixtures
do not establish the complete theorem. The older historical corpus and
receipt hashes are provenance only, never reproduction inputs.

The imported mathematical prerequisites have their own fuller audit
commands and dependencies. The new source generation/checking chain uses
the standard library only. `SOURCE-BINDING.md` explains the unchanged
source pins and actual-execution premise; `LITERATURE.md` credits prior work.
