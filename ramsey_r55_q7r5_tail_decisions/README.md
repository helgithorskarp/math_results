# 518 complete physical43 tasks excluded by exact residual decisions

The complete h3887 `q7,r5` macro class has **518 impossible tasks and 122
remaining tasks**, out of 640. This removes whole physical43 tasks from the
global cover, reducing it from **2,189,178 to 2,188,660** tasks. The other
17 macro classes are retained in full.

The mechanism decides the entire forced 23-vertex residual: its fixed
15-vertex catalog core, two blue K4 blocks, and all 136 edges between them.
Red K4 exhaustion forbids red K4s throughout that residual; the target
forbids blue K5s. All 640 residual formulas receive complete decisions.
Every negative has an independently checked proof, and every positive has
a literal 23-vertex witness. [PROOF.md](PROOF.md) establishes the reduction
and the completeness of the block relabeling used inside the residual test.

The 122 positive residuals do **not** establish physical43 candidates.
All 122 complete physical tasks remain UNKNOWN. No good43 or improved
Ramsey lower bound is established. The separate 161 h3987 q10 children are
unchanged. No carrier factors or q10 child counts are multiplied here.

## Verify

The only graph input is Brendan McKay's 12,800-byte `r44_15.g6` file:
https://users.cecs.anu.edu.au/~bdm/data/r44_15.g6 . Its required SHA-256 is
`53a46ba21cb16805eb07775b60746f783864388538368955e72cbdae5ae8f4e1`.
The scripts verify that identity before use.

From the repository root, these standard-library checks audit every
encoding, every saved positive residual, and the relabeling controls:

```sh
python3 -B ramsey_r55_q7r5_tail_decisions/verify.py --catalog /path/r44_15.g6
python3 -B ramsey_r55_q7r5_tail_decisions/controls.py --catalog /path/r44_15.g6
```

The first reports `VERIFIED_ENCODINGS_AND_SAT_WITNESSES`; it does not claim
to recheck the 518 negative proofs. One compact full-task certificate is
included, with an independent RUP checker and exact source-clause positions:

```sh
python3 -B ramsey_r55_q7r5_tail_decisions/check_example.py \
  --catalog /path/r44_15.g6 --scratch /new/path/example145
```

This needs a C++17 compiler and reports
`VERIFIED_EXAMPLE_FULL_PHYSICAL_TASK_UNSAT` for `bo1-q7-r5-c000145`.
It uses no SAT solver or imported Ramsey bound.

For **all 640 complete decisions**, install `python-sat==1.9.dev15` in an
isolated Python environment, build drat-trim at the source revision in
[TOOLS.json](TOOLS.json), and run:

```sh
python3 -B ramsey_r55_q7r5_tail_decisions/reproduce.py \
  --catalog /path/r44_15.g6 --scratch /new/path/full-tail-replay \
  --drat-trim /path/to/drat-trim --jobs 2
```

Expected: `REPRODUCED_ALL_640_TAIL_DECISIONS`, with 518 UNSAT and 122 SAT.
The complete generated CNFs and proofs remain in that scratch directory.
Every UNSAT proof is checked; proof bytes need not match across replays.
Use `verify.py --run /path/full-tail-replay --drat-trim /path/to/drat-trim`
to independently audit all generated formulas, witnesses and proofs again.
The recorded primary proofs total about 1.61 GB and are omitted from Git;
the source and compact evidence regenerate them. Tail runtime gives no
tractability estimate for the retained full43 tasks.

## Use the complete remaining family

```sh
python3 -B ramsey_r55_q7r5_tail_decisions/interface.py --registry
python3 -B ramsey_r55_q7r5_tail_decisions/interface.py --task bo1-q7-r5-c000000
python3 -B ramsey_r55_q7r5_tail_decisions/interface.py --task bo1-q7-r5-c000004
```

The last two report `CERTIFIED_UNSAT` and `UNKNOWN`, respectively. The
emitter refuses to generate a formula for an excluded task. For a retained
task it checks the pinned h3887 source and emits its **unchanged complete
physical formula**, preserving all original free edges:

```sh
python3 -B ramsey_r55_q7r5_tail_decisions/interface.py \
  --task bo1-q7-r5-c000004 --emit /path/to/h3887/catalogs \
  --output /new/path/retained43.cnf
```

The pinned h3887 source and its three dependencies must be sibling packages,
as in the shared immutable handoff. `--parent` can name another pinned copy
of its directory. The four catalog files are the parent's ordinary inputs.
No saved residual witness or residual-only ordering is imposed on emission.
[HANDOFF.md](HANDOFF.md) describes the exact scope and receiving checks.

This is a computer-assisted finite family reduction, with explicit
catalog/coverage and toolchain trust boundaries. It is not an external
review or formal proof-assistant result. No historical novelty is claimed
for clique-block normalization or residual SAT decision.
