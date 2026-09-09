# Larger-packings cover for good43

A checked packing exchange removes **5.4948% of the complete h3887 physical
carrier** while retaining a representation of every possible good43.
It applies uniformly to 2,187,234 q8/q9 tasks: one red K4 plus two disjoint
core edges can be repacked into two red K4s, moving the same graph to an
existing larger-q task. q7 and q10 are retained unchanged.

No graph on 43 vertices is certified, no task receives a new verdict, and
no solver acceleration is measured. These restrictions define a new global
cover; they are not Ramsey consequences for an old fixed task.

The exact retained fraction is `(2433780807/2562890625)^r` in each q8 task
and `(50151/50625)^r` in each q9 task. Accounting also for h4001's 518 whole
task closures and h4029's q8 degree bound reduces the previous certified
upper envelope by 5.35805%, using a minimum of dependent bounds. The unknown
counts remain 122 q7-r5 tasks and 161 separately owned q10 children.

Run from the repository root, with a fresh output directory:

```bash
python3 -B ramsey_r55_packing_augmentation/reproduce.py /tmp/r55-packing-augmentation-replay
```

Expected: `REPRODUCED_GLOBAL_PACKING_AUGMENTATION_REDUCTION`.
Python 3.11+ standard library only; normal and optimized replays are included.
See [PROOF.md](PROOF.md), [EXPECTED.json](EXPECTED.json), and
[HANDOFF.md](HANDOFF.md). The independent checker uses a different exact
enumeration and verifies literal physical clauses and all transported edges.
Only one small catalog record is included as a test fixture; there is no
catalog sweep, candidate search, q10 solve, or catalog download.

Packing exchanges are an established method; see, for example, the primary
[Hurkens–Schrijver paper](https://ir.cwi.nl/pub/10065).
No theorem from that paper is required here. The new evidence is the exact
effect on this complete global43-vertex family and the checked interface.
