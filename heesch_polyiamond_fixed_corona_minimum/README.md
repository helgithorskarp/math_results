# Fixed-corona positive-angle-surplus minimum

Agent: **six-heesch-2**, researcher.

Among topological-disc polyiamonds drawn from the 354-cell vertex halo of the
published 215-iamond, using its exact 131-copy five-corona fixture and having
more 300-degree corners than 60-degree tips, **the minimum is 215 cells**.
Corner locations and counts may vary. A cold UNSAT certificate excludes every
member with at most 214 cells; the original tile supplies attainment.

This conditional minimum identifies a limit of one compression family. It is
not a minimum over all finite-five polyiamonds, a new Heesch record, or an
exact Heesch-number result. The known-family attainment is attributed in the
sibling [hexapillar reproduction](../heesch_polyiamond_hexapillar/README.md).

Read [the proof and scope](proof.md). [encode.py](encode.py) regenerates the
necessary formula. [verify.py](verify.py) audits the angle indicators using a
separate incidence-graph definition, solves a fresh cold instance, checks the
trace with independent DRAT-trim, and replays the existing geometry checker.
[expected.json](expected.json) records compact counts and hashes.

From the repository root, with CPython 3.12.14 and `python-sat==1.8.dev24`:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
timeout 55s python3 heesch_polyiamond_fixed_corona_minimum/verify.py \
  --checker /path/to/drat-trim \
  --work /tmp/heesch-fixed-corona-minimum
```

The checked DRAT-trim source is the primary repository
[marijnheule/drat-trim](https://github.com/marijnheule/drat-trim), commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Build it separately with its `make`
command. No binary is included here. The solver is limited to 20,000 conflicts;
SAT, UNKNOWN, a timeout or a killed process cannot count as verification.

Expected CNF: 21,717 variables, 121,097 clauses, SHA256
`2c6d12be9f6eb13351dc5f0e12104106c00a77d6da8f6ab63f4e47fb82b0527a`.
Expected result: independently verified UNSAT at 214, followed by the
215-cell five-disc-corona attainment check. An alternative valid trace may
have a different proof hash; the CNF hash and independent verification remain
mandatory. The reference proof is 559,357 bytes and is regenerated in the
work directory. The repository includes no traces, CNFs, downloaded papers,
environments, ledgers or keys.

The sibling tile and corona inputs are pinned by SHA256 in expected.json;
their verified original source commit is
`a99c2e225437ead594ff90e13f232ab514200c16`. The universal encoding implication
is a written mathematical argument. Source publication and independent
certificate checking do not constitute a formal proof or a peer-review verdict.
