# Finite polyomino-corona CNF with local topology constraints

six-heesch-1 — researcher — 2026-09-29.

This directory proves and implements a complete finite reduction for
**square-grid-aligned** unmarked polyomino coronas. The topology part adds O(HN)
CNF size for H prefixes with N possible cells. A cumulative selection encoding
avoids explicit tile-pair adjacency exclusions; the full generator has O(HNm)
size, where m is tile area. See [proof.md](proof.md) for the definitions,
finite-radius proof, soundness and completeness, and the redundant-adjacency lemma.

The useful step is enforcing topology directly on **every occupied prefix**.
For connected square-cell sets the classical Euler equality

    cells - side_pairs + full_2x2_blocks - diagonal_pinches = 1

is exactly hole freedom. Forbidding diagonal pinches additionally forces a closed
topological disc. The default corona command uses disc prefixes; `--allow-pinches`
permits connected hole-free prefixes with corner pinches. `--holes-last` relaxes
the topology requirement only in the last corona. Upper obstructions apply to
the stated grid convention. No reduction of arbitrary rigid motions to this grid
is asserted, and no new finite Heesch record is claimed.

The Euler identity is established prior art, notably Gray (1971). Kaplan (2022)
already developed the grid-corona SAT approach and used iterative hole cuts.
This is a self-contained application and exact encoding refinement, with no
priority claim for Euler counting or for general topology constraints in SAT.

## Reproduce without a SAT solver

Tested with CPython 3.11.2. Run these commands from the repository root:

```bash
python3 heesch_polyomino_euler_cnf/validate.py
mkdir -p scratch/heesch-euler
python3 heesch_polyomino_euler_cnf/corona.py \
  heesch_polyomino_euler_cnf/fixtures.json --depth 2 --generate-only \
  --cnf scratch/heesch-euler/seven_depth2.cnf
python3 heesch_polyomino_euler_cnf/check_rup.py \
  scratch/heesch-euler/seven_depth2.cnf \
  heesch_polyomino_euler_cnf/seven_depth2.rup
python3 heesch_polyomino_euler_cnf/corona.py \
  heesch_polyomino_euler_cnf/fixtures.json --depth 1 \
  --check-only heesch_polyomino_euler_cnf/seven_depth1.witness.json
python3 heesch_polyomino_euler_cnf/corona.py \
  heesch_polyomino_euler_cnf/kaplan17.json --depth 3 \
  --check-only heesch_polyomino_euler_cnf/kaplan17_depth3.witness.json
```

Expected substantive results:

- All 65,536 subsets of a 4×4 cell box satisfy the local Euler identity, explicit
  cubical V−E+F identity, and flood-fill component/hole identity. The connected,
  connected-hole-free, and disc totals are 37,196, 28,732, and 9,349.
- 5,147 arithmetic assignments and 4,608 independent unit-propagation checks pass.
- The seven-cell depth-two formula has 32,514 variables and 134,801 clauses;
  the included 92-clause, 8,892-byte RUP certificate gives `VERIFIED UNSAT`.
  Its one-corona witness has 8 outer copies and 63 total occupied cells. This
  certifies grid-disc Heesch number one for an **already published** tile.
- The published 17-cell tile's depth-three witness has 6, 12, and 17 added copies.
  Prefix areas are 17, 119, 323, and 612; every prefix has Euler characteristic
  one, zero holes, and zero diagonal pinches. This reproduces the existing
  construction side only; the included artifacts do not certify its upper bound.

Exact hashes and counts are in [evidence.json](evidence.json). Timings are machine
dependent: the full standard-library validation took about eight seconds, the
small certificate check about four seconds, and the 17-cell depth-three search
about five seconds to build and six seconds to solve on the campaign host.

## Optional fresh searches

Python-SAT is needed only for solver searches and existential CNF projection
checks. Keep solver/BLAS/OpenMP threads at one. A resource timeout is inconclusive.

```bash
python3 -m venv scratch/heesch-euler-venv
scratch/heesch-euler-venv/bin/python -m pip install \
  -r heesch_polyomino_euler_cnf/requirements.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  scratch/heesch-euler-venv/bin/python heesch_polyomino_euler_cnf/validate.py --sat
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  scratch/heesch-euler-venv/bin/python heesch_polyomino_euler_cnf/corona.py \
  heesch_polyomino_euler_cnf/kaplan17.json --depth 3 \
  --witness scratch/heesch-euler/kaplan17_fresh.json
```

The `--sat` validation adds all 1,024 occupancy/auxiliary-projection checks on a
3×3 box in both topology modes. Fresh UNSAT searches can write an untrusted proof
with `--proof FILE`; check that proof separately before treating it as a certificate.
The small included certificate was extracted from Glucose 4.1 (via Python-SAT
1.8.dev24), then checked by both the included occurrence-counting RUP verifier
and [DRAT-trim](https://github.com/marijnheule/drat-trim), inspected version
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. The verifier accepts deletion-free
RUP only, and requires a checked empty final clause.

## Sources and trust boundary

- Craig S. Kaplan, [Heesch Numbers of Unmarked Polyforms](https://arxiv.org/abs/2105.09438),
  Contributions to Discrete Mathematics 17(2), 150–171 (2022).
- The seven-cell input is record 1 of Kaplan's [07omino dataset](https://cs.uwaterloo.ca/~csk/heesch/omino/07omino_0up.txt).
  The 17-cell input is record 44 of his [17omino dataset](https://cs.uwaterloo.ca/~csk/heesch/omino/17omino_2up.txt).
  Coordinates are attributed fixtures; new witness patches were generated here.
- Stephen B. Gray, [Local Properties of Binary Images in Two Dimensions](https://doi.org/10.1109/T-C.1971.223289),
  IEEE Transactions on Computers C-20(5), 551–561 (1971).
- Kaplan's [current implementation](https://github.com/isohedral/heesch-sat)
  was inspected at `d12a527c04310fed51d522318126781e2f7ed56d` (2026-08-30).

The proofs are written mathematics, not proof-assistant formalizations. Exact
integer Python code, its runtime, and the mapping from cells to geometry remain
the computational trust base. The pure Python witness checker uses direct halo
coverage and flood fill, not the SAT encoding. The RUP checker verifies Boolean
UNSAT; the finite-candidate and encoding proofs bridge that statement to grid
coronas. Generated CNFs, native binaries, the full untrimmed trace, and scratch
search output are omitted; source and the small certificate suffice to reproduce
the reported checks. No comparison of solver performance with Kaplan's method
has been established.
