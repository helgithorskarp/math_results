# Unrestricted global construction mechanism for `R(5,5,43)`

This directory supplies a complete four-branch, counterexample-guided SAT
(CEGIS) mechanism for constructing a 43-vertex graph with no clique or
independent set of size five.  It also supplies an independent physical graph
verifier.

This is a pass-1 construction framework, **not a good43** and not a Ramsey
bound improvement.  The target pilot ended `INCOMPLETE` in all four branches.
See [PROOF.md](PROOF.md) for the coverage and finite-termination theorem.

## Why the search is unrestricted

Every hypothetical good43 has all degrees in `[18,24]`.  After optional color
complementation and vertex relabeling, it occurs in one of the four branches

```text
degree(0) = 18, 19, 20, or 21.
```

Apart from the root normalization and the universal degree bounds, every one
of the remaining physical edges is a free SAT variable.  The engine adds
literal no-monochromatic-five constraints found by scanning all 962,598
five-subsets of each model.  A SAT round may change any set of edges; no fixed
automorphism, seed graph, catalog, edit radius, matching support, or local walk
is imposed.

## Files

- `cegis.cpp`: incremental exact producer and semantic checkpoint writer.
- `run_portfolio.py`: process-isolated driver for all four target branches.
- `verify.py`: independent dense physical verifier.
- `controls.py`: exhaustive small verifier and normalization controls.
- `resume_control.py`: target-size semantic checkpoint continuation control.
- `check_calibration.py`, `calibration_good32.json`: deterministic good32
  construction replay.
- `check_target_pilot.py`: exact comparison of a fresh target pilot with its
  archived compact receipt.
- `fixtures/good42.g6`: one published positive verifier fixture.
- `target_pilot.json`: compact pass-1 target execution receipt.
- `environment.json`: exact toolchain receipt for the archived execution.
- `SHA256SUMS`: integrity manifest for the hand-written source and compact
  evidence.

Raw target logs and CEGIS checkpoints are generated operational state and are
kept outside Git.

## Requirements and build

- CPython 3.11 or later, standard library only.
- GCC 12.2 or another C++20 compiler.
- [CaDiCaL 1.9.5](https://github.com/arminbiere/cadical/releases/tag/rel-1.9.5),
  built as `build/libcadical.a`.

The campaign build used CaDiCaL source commit
`146207318796f094dcded87349a64f0c6927309e`.  From this directory:

```sh
make CADICAL_ROOT=/path/to/cadical-1.9.5 check
make CADICAL_ROOT=/path/to/cadical-1.9.5 sanitize
```

A standalone CaDiCaL checkout can be built with its documented
`./configure && make` sequence.  `environment.json` records the source commit,
static-library hash, compiler, Python, and operating system used for the
archived receipts.

Expected terminal check records include

```text
CARDINALITY_SELF_TEST status=PASS cases=3584
{"exhaustive_graph_words":33867,...,"status":"PASS"}
{"clauses_added":66011,"five_subsets_checked":201376,"rounds":858,"status":"REPRODUCED_GOOD32"}
```

The good42 verifier fixture alone can be checked without CaDiCaL:

```sh
python3 -B verify.py --graph6 fixtures/good42.g6 --expect good
```

It checks all 850,668 five-subsets and reports zero red and blue `K5`s.

## Target execution

Choose a fresh directory outside the checkout:

```sh
make CADICAL_ROOT=/path/to/cadical-1.9.5 \
  WORK=/tmp/r55-cegis-pilot pilot
```

The four processes use deterministic seeds and write a compact summary plus
one log and resumable semantic checkpoint per root degree.  `GOOD_GRAPH` is
emitted only after the producer's full scan; the driver then independently
decodes and scans the physical word again.  `INCOMPLETE` means only that the
declared round budget ended.  `UNSAT_SUBFORMULA` is not a certified exclusion
unless a separately generated proof is retained and checked.

After the run, the Make target compares all four exact branch outcomes,
physical counts, graph hashes, checkpoint hashes, and commands with the
archived pilot receipt.  A fresh work directory is required so operational
checkpoints cannot be overwritten accidentally.

To continue one checkpoint to a larger total number of rounds, repeat its
recorded producer command with the same options, a larger `ROUNDS` argument,
and the same checkpoint path.  The explicit formula, best graph, and clause
selection RNG are restored; internal CaDiCaL learned clauses are not.

## Trust boundary

Positive existence is definition-checked independently and does not rely on
SAT-solver soundness.  The construction trajectory trusts the pinned CaDiCaL
version, C++ compilation, Python file/JSON semantics, SHA-256, the written
coverage proof, and ordinary hardware.  No UNSAT theorem is claimed here.

The good42 fixture is copied byte-for-byte from McKay's published Ramsey data
as already preserved in this repository.  Dataset completeness is irrelevant:
the fixture is used only as a positive physical-verifier control.
