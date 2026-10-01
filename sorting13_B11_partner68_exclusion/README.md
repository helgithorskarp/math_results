# Complete B11 allowed-partner (6,8) exclusion

**six-sorting-2, researcher**, 2026-10-01. Written unformalized intermediate
lemma:36 complete quota classes/421920 effective orders at arbitrary depth,
all permitted physical-loop placements. All actual first touches are(6,10).
The exact high-zero-component argument explains this necessity.
With the named pinned prior results,153 conditional classes/772110 orders
remain and every surviving quota contains(5,10). Global S13 remains44..45;
non-P19 coverage and written all-real bridges remain unresolved.
See [PROOF.md](PROOF.md) for scope, imports and mathematical reasoning.

Python3.11+ with assertions enabled; PySAT1.8.dev24 only for complete CNF
generation and the genuine positive control. Solver/BLAS/OpenMP threads1;
one intensive job at a time. From this directory in the full repository:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B reduce.py
python3 -B verify.py
python3 -B tail_build.py --skip-search
python3 -B tail_audit.py
python3 -B tail_proof.py
python3 -B controls.py
python3 -B frontier.py
```

An explicit sparse checkout uses `--repository /path/to/full/input/repo`
and `--output /path/to/private/generated` consistently on every command.
The pinned files are listed in dependencies.json. Generation emits large
deterministic tables/formulas/metadata locally in ignored generated/.
Neither formulas, raw proof corpora, environments, binaries nor logs are
published. All negative search can be skipped: supplied compact evidence
is checked against the regenerated complete formulas. The positive
insertion36/full69 control is still actually generated and checked.

Expected finite evidence:36 classes,480 phase triples,21048 normalized
prefixes,6838 literal image/budget pairs=6434activity+354basic+35fourport
cuts+15complete C11 refutations. The finite verifier's pending-tail label
marks its structural role; separate encoding and proof checks complete
all fifteen leaves. Main proof output FIFTEEN_TAIL_PROOFS_ACTUALLY_VERIFIED
has29004coreclauses/8429RUPadds/zero deletions and RAT. Actual complete
clause audit1466368negativeclauses/1491cardinalityblocks,23195relevant flag
assignments. Positive control328921clauses/8192original inputs. Six actual
semantic corruptions are rejected after bypassing hashes; tinyRUP4608.

Optional fresh native checking, after separately installing/compiling
DRAT-trim at source2e3b2dc0ecf938addbd779d42877b6ed69d9a985:

```bash
python3 -B tail_build.py
python3 -B tail_proof.py --drat-trim /path/to/drat-trim
```

The native checker replays full raw DRAT with zeroRAT, checks its generated
core and exact trim, then independently replays the deletion-free compact
proof. Formula/core membership and solver-free Python RUP are also checked.
Removing native deletion lines retains clauses and preserves RUP.
Known source/checker versions and actual hashes are recorded in the
manifest. A changed solver log is not substituted for the supplied proof.
A SAT answer is decoded and tested on all8192original Boolean inputs;
UNKNOWN/timeout/resource termination/incomplete results prove no exclusion.
Per-class finite stages45s, negative solver40s/30000conflicts, no resource
escalation. Public proofs total725851bytes in30separate instance files,
largest59322; full formulas and native traces are locally regenerated.
All current finite/clause/native/Python/controls checks actually passed.
Independent algorithms are not independent-person review or formalization.
