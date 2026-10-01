# Sharp maximum 67 at an uncovered 19/20/20 triple

Actual author: **six-code-3, researcher**, 2026-10-01.

For an eighteen-point five-subset packing, distinct words meet in at most
two points. Suppose x,y,z have replications 19,20,20, their pair counts
are xy=xz=5,yz=4, and xyz is uncovered. The sharp maximum is **67**.
There is no symmetry or other point-degree hypothesis. This does not
improve the unrestricted 69--71 campaign interval.

The [proof](PROOF.md) states the reductions and their completeness.
[DEPENDENCIES.json](DEPENDENCIES.json) lists the imported, independently
audited nineteen-star census and SHA-pinned source helpers. This result's
ordinary bridges are unformalized; independent mathematical peer review
and historical priority are pending. The known 69 construction remains
prior art.

The full primary census and all 46 independent cases have completed.
[VALIDATION.json](VALIDATION.json) records the actual coverage and commands.
The final wrapper check reused the completed census records; it did not
repeat the cold census.

## Quick exact sharpness check

Python 3.11.2 was used; no third-party package or private corpus is needed:

```bash
python3 round-two/six-code-3/nineteen_twenty_twenty_interfaces/verify_witness.py
python3 -O round-two/six-code-3/nineteen_twenty_twenty_interfaces/verify_witness.py
python3 -O round-two/six-code-3/nineteen_twenty_twenty_interfaces/capacity_controls.py
```

The fixture [witness67.json](witness67.json) contains the 45-word core and
67-word code. All 670 triples are distinct; center replications are
19,20,20, pair counts 5,5,4, and the center triple is uncovered. Witness
SHA256: `3a732e14d328d895d4529372f9ddf7d1fde4cf3f563eada15ae55867e94f387a`.

## Full reproduction

Run from the repository root with Python 3.11.2 and g++ 12.2.0 or compatible
C++17 tools. All mathematical arithmetic is exact; no solver, numerical
library, network service or proof assistant is required. The imported
files already live in the publication repository.

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 round-two/six-code-3/nineteen_twenty_twenty_interfaces/reproduce.py \
  --work /tmp/a18-triple67
```

The cold driver compiles the two native engines, produces all 46 cases,
compares the exact expected manifest, independently replays every tail
choice and eleven-clique query, checks all residual certificates normally
and under Python -O, validates the positive fixture and damaged-evidence
controls, checks the Python/native port on three whole cases, and checks
actual witness-fiber queries with ASan/UBSan builds. Every stage runs
sequentially with one thread. Child failure or a guard gives an incomplete
run and never proves nonexistence.

If a private primary corpus is already available, `--reuse-primary`
checks its complete expected hashes and still runs the independent
replay. For a previously interrupted independent replay, use
`--resume-replay` and the same executable path supplied by
`--pivot-executable PATH`. This trusts only the runner's sealed local
execution records with unchanged source, executable and primary hashes.
The default is cold; a local execution checkpoint is not a portable
negative certificate. Default binaries are compiled under WORK/build.

The exact census has 46 marked inputs, 1,540,398 four-tail choices, 18,062
first-center completions and 77 distinct **labelled** 45-word cores. The
[expected manifest](expected.json) has SHA256
`952b768db8778961eaa16e14d8b684d642058bb62b8837c445ae4521893f5d58`.
The private query carriers are about 454 MiB and are regenerated, not
published. This is not an isomorphism census of all 67-word codes.

The [77 colorings](residual.json) have capacities 17..22 and prove at
most 22 further words at every core, hence 67 total. Candidate domains
contain 44..72 fifteen-point words. The independent checker reconstructs
all candidates and edges literally. Certificate SHA256:
`c0e000acb663736254eac5a0e2112d837ad703bd226c5baee31dbcd323d31651`.

## Individual stages and resumable coverage

For case K, `produce.py --case K --executable COLOR --work WORK` writes
its complete header, query transcript and cores. After K=0..45, run
`produce.py --summary --work WORK`. The default guards are two million nodes and
20 seconds per query, 60 seconds per case or bounded replay interval.
No guard is raised by the driver.

`verify.py --case K --start S --size 15000 --executable PIVOT --work WORK`
checks a precise half-open interval. `replay.py --work WORK --executable
PIVOT` runs all 46 cases in contiguous intervals, checks that there is no
gap or overlap, and saves source-bound local completion seals. Add
`--resume` only for those existing unchanged local records. It compares
full candidate and clique lists entrywise, not only aggregate counts.

The files [residual.py](residual.py) and
[verify_residual.py](verify_residual.py) separate deterministic coloring
discovery from exact literal certificate checking. Color/branch certificates
are supported, although all 77 published certificates are single proper
colorings. Regeneration needs the private cores from the cold census.

Reproduction uses standard library C++ bitsets of 256 vertices and exact
Python integers. Both native engines are checked on all 1024 five-vertex
graphs, additional ranks including 11, and boundary labels through 255.
Both have nine malformed/guard controls; literal checks reject ten damaged
capacity proofs and four damaged witnesses. Sanitizers cover the actual
positive witness fiber, not the full census. See the exact commands and
coverage in [VALIDATION.json](VALIDATION.json).
