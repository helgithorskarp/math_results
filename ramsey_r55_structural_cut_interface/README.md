# A checked physical-edge cut with an exact global-family count

This package compiles one consequence of the accepted h4015 neighborhood
restriction into a **147-literal conflict clause on physical graph edges**.
Its 19 RUP additions are checked against 257 literal Ramsey five-set
premises. It excludes a complete family of more than **2^750 labelled
43-vertex assignments**, already restricted by h4009's edge window and the
chosen root's degree bound. The exact integer is in [EXPECTED.json](EXPECTED.json).

The family fixes a root's 18 same-color neighbors and the cross edges of
five modules of sizes `(4,4,4,3,3)` following a five-cycle. All 24 internal
module edges and all 732 other edges remain free. The graph has no imposed
automorphism. Both color choices are included and are disjoint for the
specified embedding. This family is decided completely, with no search
timeout or unresolved branch.

Under the 147 fixed edges the original global Ramsey CNF has **zero initial
unit or empty clauses**; the certified cut yields an immediate conflict.
This is an exact propagation comparison, not a solver-speedup claim: the
single native proof-generation call needed only four conflicts. Counts are
labelled complete assignments, not surviving search candidates or
isomorphism classes. Other vertices' degree restrictions are not imposed
in the count, embeddings are not multiplied, and no h3887/q10/q7r5 task is
declared closed. No good43 or improved Ramsey lower bound is established.

From the repository root, with CPython 3.11 or later (standard library only):

```sh
python3 -B ramsey_r55_structural_cut_interface/reproduce.py \
  /tmp/r55-structural-cut-replay
```

Expected status: `REPRODUCED_GLOBAL_STRUCTURAL_CUT_INTERFACE`. Replay checks
source hashes, regenerates the 24-variable/257-clause input, verifies the
saved proof in local and global variables, computes the family count in two
exact ways, and runs normal and assertion-disabled transport and corruption
controls. It invokes no solver and downloads nothing.

For a supplied ordered embedding, generate the physical clause, canonical
premises and lifted proof:

```sh
python3 -B ramsey_r55_structural_cut_interface/interface.py \
  --vertices 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18 \
  --color 1 --out /tmp/r55-cut.json
python3 -B ramsey_r55_structural_cut_interface/verify.py \
  ramsey_r55_structural_cut_interface /tmp/r55-cut.json \
  --out /tmp/r55-cut-verified.json
```

Use `--color 0` for blue. The first label is the root; subsequent groups of
4, 4, 4, 3, 3 labels specify the five modules. [HANDOFF.md](HANDOFF.md)
documents safe translation into an owner's edge numbering and fixed edges,
including literal five-set witnesses for completely assigned rejected graphs.
There is no embedding search and no access to teammate survivor inputs.

[PROOF.md](PROOF.md) gives an elementary proof, the relation to h4015, the
guarded RUP lifting and exact count. The cut itself imports no classification
or graph catalog. h4009 is used only to interpret the counting window as a
necessary target restriction; h4015 guided the selection. Dependencies and
related earlier work are recorded in [DEPENDENCIES.json](DEPENDENCIES.json).
The five-cycle covering argument is not claimed as new mathematics. The
deliverable is the checked physical interface and its quantified family
scope; external review of this package and historical novelty are unclaimed.
