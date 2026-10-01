# Uncovered 19/19/20 centers: sharp67 and checked structural refinements

Author: **six-code-3, researcher**. Read [PROOF.md](PROOF.md) for the exact
hypotheses, ordinary completeness arguments and trust boundary.
The new result is author checked; independent review and historical
priority remain pending. Unrestricted campaign bounds remain69--71.

Requires Python3.11+, G++12/C++17 and OpenSSL headers/libcrypto.
All combinatorial arithmetic and certificates are exact integers.
No optimization solver or nonstandard Python package is required.
Use one CPU-intensive process and one thread; no parallel case pool.

From a checkout of the whole authorized repository, run:

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 round-two/six-code-3/nineteen_nineteen_twenty_interfaces/reproduce.py \
  --work scratch/mixed19-reproduction
python3 round-two/six-code-3/nineteen_nineteen_twenty_interfaces/verify_refinements.py \
  --census-work scratch/mixed19-reproduction/census \
  --color-work scratch/mixed19-reproduction/residual
python3 -O round-two/six-code-3/nineteen_nineteen_twenty_interfaces/verify_refinements.py \
  --census-work scratch/mixed19-reproduction/census \
  --color-work scratch/mixed19-reproduction/residual
```

The first command builds both engines sequentially, runs native controls,
enumerates all46 marked types in both orientations, verifies complete
literal universes and matching full transcripts, generates all4871
proper colorings, checks the compact expected results and witness,
and runs normal/optimized standalone and damage checks. The last
commands verify literal leave/cycle refinements over the same full domain.
Cold computation takes roughly half an hour on the campaign's single
CPU scope; runtime depends on hardware and scheduling.

Expected:92 orientations,3080796 four-tail choices,39773 z20 prefixes,
4871 labelled44-word cores, residual capacities10--23, upper67 and
literal attainment67. The complete color certificate hashes to
`6e39d8a7116d4fcdb0a621f24f6b307b2cb949b0b16162b8522fdacfe683caba`.
Refinements: m_x=1, m_y in{0,1}; m_y=1 implies at most65;
anchor complement cycles4+6 imply at most60. Those subgroup bounds
are not asserted sharp. Counts and hashes are in
[expected.json](expected.json), [RESIDUAL_SUMMARY.json](RESIDUAL_SUMMARY.json)
and [REFINEMENTS.json](REFINEMENTS.json).

`--resume` on reproduce.py reuses only sealed complete local orientations
with identical source and rebuilt executable hashes. A changed compiler
may change executable bytes and therefore require a cold rerun in a new
work directory. Resume records are execution checkpoints, not portable
negative certificates. Guards remain2million nodes/20seconds per native
query,60seconds per whole native case,65seconds per subprocess, and
60seconds per100-core residual batch. A guard failure is incomplete;
it never becomes a zero case or a theorem.

The small witness can be checked without any generated census:

```bash
python3 round-two/six-code-3/nineteen_nineteen_twenty_interfaces/check_witness.py \
  round-two/six-code-3/nineteen_nineteen_twenty_interfaces/witness67.json --controls
```

All prerequisite source/data is already published in adjacent directories;
[DEPENDENCIES.json](DEPENDENCIES.json) lists exact file hashes and commits.
The unchanged include/exclude kernel is credited to six-reviewer-5 and
its review8855, source42daf31b272add94704834ca403f65fbc387359a.
That earlier review concerns19/20/20. Both executions here are by this
author and do not establish a new independent verdict.

Keep generated work under scratch. The full core/color arrays, binaries,
resume state, logs and earlier large raw transcripts are intentionally
absent from this public source bundle.
