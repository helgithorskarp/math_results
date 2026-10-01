# Period621 carry-aware construction frontier for W(2,7)

**six-vdw-1, researcher.** A complete period-621 reduction leaves 207 binary
orientation variables for each ternary skeleton. A general twisted-balance
lemma forces at least two thirds of its 21114 projected seven-AP supports
above the minimum local constraint count. The canonical decomposition thus
has **112608 to190026 distinct signed NAE constraints**, with total static
weight190026. [PROOF.md](PROOF.md) states the exact conventions and proof.

A valid cyclic word, including all repeated-residue windows, would repeat to
3726 points and prove `W(2,7)>=3727`. No such word or exclusion of period621
is claimed. The current located primary seed remains `>3703`; see the proof
for literature and the difference from period618 and other cyclic conventions.

Run the proof checks with Python3.11.2 or newer, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 round-two/six-vdw-1/reproduce621.py
```

Expected final line: `VERIFIED_CARRY_REDUCTION_AND_FINITE_AUDITS`.
The complete local classification checks2187 vectors and139968 multiplicity
entries. Six full weighted dictionaries are compared entry by entry against
literal cyclic enumeration, with hashes in [expected.json](expected.json).
Outputs stay in ignored `scratch/`. All computations use exact integers.
The written proof and the two same-author implementations are the trust
boundary; no independent peer review or proof-assistant check is claimed.

Optional bounded SAT construction probes require pinned
`python-sat==1.8.dev24`. Use a local virtual environment and one job at a time:

```sh
python3 -m venv round-two/six-vdw-1/scratch/venv
round-two/six-vdw-1/scratch/venv/bin/pip install -r round-two/six-vdw-1/requirements.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
timeout 30s round-two/six-vdw-1/scratch/venv/bin/python \
  round-two/six-vdw-1/search621.py --skeleton digit9 --conflicts 5000 \
  --output round-two/six-vdw-1/scratch/search-digit9.json
```

The conflict option is capped at10000. UNKNOWN
and an unchecked solver UNSAT carry no exclusion claim. SAT proposals must
pass a separate exact checker before the program writes a3726-point witness.

A six-state C++ search changes both skeleton and orientations, keeps a local
resumable checkpoint, and checks its cached scores by complete recomputation
every1000 moves:

```sh
g++ -std=c++17 -O2 -Wall -Wextra -Wconversion -pedantic \
  round-two/six-vdw-1/search621.cpp -o round-two/six-vdw-1/scratch/search621
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
timeout 60s round-two/six-vdw-1/scratch/search621 \
  round-two/six-vdw-1/scratch/joint.checkpoint 10000 55
python3 round-two/six-vdw-1/audit621.py \
  round-two/six-vdw-1/scratch/joint.checkpoint.best.bits --cyclic
```

Rerunning the same search resumes the state, RNG and tabu memory. It is a
heuristic with no coverage or nonexistence claim. A zero-cost proposal still
needs exact checking of its repeated integer word. Compiler, bounded search
observations, resource measurements and checks are in [VALIDATION.md](VALIDATION.md).
Generated checkpoints, proof traces, virtual environments and binaries are
ignored and omitted from publication.

Optional sanitizer, exact restart and independent cost checks run serially:

```sh
python3 round-two/six-vdw-1/validate_search.py \
  --work round-two/six-vdw-1/scratch/search-validation-fresh
```

Use a fresh work directory. Expected:
`HEURISTIC_SANITIZER_RESUME_AND_COST_CHECKS_PASSED`. These checks validate the
search implementation; they establish no mathematical nonexistence.
