# Unrestricted four-class trades for the classical Schur-six target 537

This directory provides exact SAT instances and independently audited source
for a nonlocal search for a six-colouring of `[1,537]`. It reports **no new
Schur bound**. The public starting word has exactly two monochromatic Schur
triples, `(12,12,24)` and `(12,24,36)`; `check.py` independently counts both.
The baseline largest-colourable convention remains `S(6) >= 536`
([Fredricksen–Sweet, 2000](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32)).
`seed537.txt` is the normalized [public two-defect near-colouring by
umaia1234](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/README.md);
the [original class file](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/near_537_two_violations.col)
is distributed under Apache-2.0. `best3.txt` is the independent starting
word already recorded in the [nonlocal search
artifact](../schur_s6_nonlocal_doubling_search/best3.txt).

## Exact search family

Let `B_i` be the positions marked `i` in `seed537.txt`. For each pair `ij`
among `12,13,15,16,23,25,26,35,36,56`, preserve every position of `B_i`
and `B_j` in its original colour and recolour **every other position
independently**, subject only to the Schur constraints. Old class `B_4` is
defective, so it cannot be among the two fixed classes. A satisfying model
would be a complete valid 537-word and would establish `S(6) >= 537` after
`check.py` verifies it. If all ten instances were *certifiably* unsatisfiable,
any valid 537-word would have to change entries from at least five old
classes of this particular starting word. No such UNSAT certificates are
claimed here.

The four output labels outside the fixed pair are interchangeable. The
encoder chooses their order of first appearance on the free positions by
restricted-growth clauses. This is a sound colour permutation: every word in
the stated search family has a relabelling that obeys these clauses while
the two fixed output labels remain fixed.

A free position may also acquire a *fixed* output colour when inserting that
position alone into the corresponding fixed class does not form a Schur
triple. These necessary single-insertion domains are exact for any valid
word. All interactions among multiple insertions are still checked by the
triple clauses. In the `23` case, the only seven such `(position, colour)`
options are `(37,2)`, `(298,3)`, `(351,3)`, `(352,2)`, `(364,2)`,
`(495,3)`, `(507,3)`; `audit.py` derives them independently by scanning
triples. In particular, the encoding does not silently forbid using either
fixed output colour on free positions.

`encode.py` has one exactly-one colour constraint for each free position and
one prohibition for each colour common to an unordered triple
`x <= y`, `x+y=z <= 537`. The 72,092 triples include 268 doubling triples
with `x=y`. `audit.py` derives the domains and every clause by a separate
`x`-first traversal, then compares the exact DIMACS clause multiset. It also
checks the starting word's two defects. `verify.py` regenerates and audits
all ten cases and checks their byte hashes against `expected.json`.

## Reproduce

Requires Python 3.11 or newer for `hashlib.file_digest`; the exact audits
use only the standard library. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -B check.py seed537.txt
python3 -B check.py best3.txt
python3 -B verify.py
python3 -B encode.py --seed seed537.txt --fixed 23 --cnf /tmp/schur-fourtrade-23.cnf
python3 -B audit.py --seed seed537.txt --fixed 23 --cnf /tmp/schur-fourtrade-23.cnf
```

The first `check.py` result has two defects as above; the second has three.
`verify.py` prints `PASS selected_zero_defect_cases=10`. The `23` zero-defect
CNF has 1,027 variables, 37,927 clauses and SHA-256
`1624cd0a078dcaf3428c801c2bb5df5def46325497f919755e0a9b23fac42c3e`.
The other nine dimensions and hashes are in `expected.json`. The exact CNFs
are generated locally, not stored in Git.

For a bounded alternative search, install `python-sat==1.9.dev15` from
`requirements.txt` and run:

```sh
python3 -B solve_probe.py --seed seed537.txt --fixed 23 \
  --cnf /tmp/schur-fourtrade-23.cnf --out /tmp/schur-fourtrade-witness.txt \
  --budget 1000000
```

If the solver finds a model, `solve_probe.py` reconstructs the complete word,
counts every Schur triple directly, and writes the word only after the check
passes. `result=None` means the conflict budget was exhausted and proves
nothing. The optional `--phase-hint` starts with the seed's palette order.

`one_defect.py` constructs a relaxed variant using one selector per
potentially monochromatic triple and a sequential at-most-one counter.
`verify.py` checks hashes for the `12`, `23`, and `56` relaxed instances.
This variant can discover a new one-defect word, but a satisfying model alone
would not improve the Schur bound. The relaxed clauses are derived from
`encode.py`; the independent multiset audit currently covers the zero-defect
instances only.

For a whole-word stochastic experiment including the doubling triples:

```sh
g++ -O3 -std=c++20 full_score.cpp -o /tmp/schur-full-score
/tmp/schur-full-score seed537.txt 20260928 100 50000 20 2 15 7
```

The `FINAL` line independently recounts all triples of the best state.
Every printed `BEST_COLOR` is a complete 537-digit word and can be checked
with `check.py` after saving it as a file. The C++ run is exploratory and
cannot establish unsatisfiability.

## Bounded observations, 28 September 2026

- CaDiCaL 1.9.5, seed `20260928`, 300 seconds per instance: all ten exact
  zero-defect CNFs returned `UNKNOWN` or reached the time limit. Their
  incomplete proof streams were discarded. There is **no exclusion**.
- PySAT Glucose3, one million conflict budget: `12`, `23`, and `56`
  zero-defect cases returned `None`. The `23` at-most-one-defect case also
  returned `None`; the larger `12` and `56` relaxed probes reached a
  300-second external limit. These are inconclusive.
- Two independent 5-million-step C++ trajectories from `seed537.txt` kept
  best score 2. Two 10-million-step trajectories from the distant
  `best3.txt` kept best score 3. Every final best score equalled the direct
  recount. These scores are search diagnostics, not lower bounds.

The current obstacle is solving the exact nonlocal instances or producing a
complete valid word. The source and hashes preserve this benchmark for
different solvers, portfolio search, and independently checkable future
certificates.
