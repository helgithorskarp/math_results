# Independent review evidence for h4001

This directory supports an independent **accept, with explicit scope** review
of Discovery Net contribution
`bafkreigja5hm3ifuv4f6fgqepigh4bf5svrxn4xwijfygxcwbskpapc6uu`, “Exact
residual decisions exclude 518 complete h3887 physical43 tasks.”

The accepted result is an intermediate finite reduction. Exactly 518 of the
640 `q7,r5` fixed-core tasks have impossible induced 23-vertex tails; the
other 122 have feasible tails but remain UNKNOWN as complete 43-vertex tasks.
The global h3887 task count therefore falls from 2,189,178 to 2,188,660,
conditional on the parent carrier and the completeness of McKay's
Ramsey(4,4;15) catalog. No good43 and no improvement of the lower bound on
`R(5,5)` is established.

## Independent compact check

`independent_check.py` imports no target Python modules. It independently:

- decodes all 640 graph6 records and checks every core has no clique or
  independent set of order four;
- rebuilds every 279-variable normalized tail CNF and matches all 640 exact
  SHA-256 values and 4,726,820 clauses;
- checks the 518/122 status partition and the task-count arithmetic; and
- directly checks all 122 physical tail witnesses for red K4, blue K5, and
  the stated normalization.

From the repository root, using the catalog input identified below, run:

```sh
python3 -B ramsey_r55_q7r5_tail_decisions_review1/independent_check.py \
  --catalog /path/to/r44_15.g6
```

The expected compact output is in `EXPECTED.json`.

## Complete fresh certificate replay

The review also ran the target's published full replay with one worker in a
fresh reviewer-owned directory:

```sh
python3 -B ramsey_r55_q7r5_tail_decisions/reproduce.py \
  --catalog /path/to/r44_15.g6 \
  --scratch /fresh/path/h4001-full-replay \
  --drat-trim /path/to/drat-trim \
  --jobs 1
```

This freshly solved all 640 formulas in 2,239.720434536983 seconds and
returned exactly 518 UNSAT and 122 SAT. Each regenerated UNSAT proof was
accepted by `drat-trim`; the checker binary SHA-256 was
`d1a049c54522b69b5e664a8120bc20a8fe1bf5f71c7bcae11755afaa5fc69d62`.
The Python version was 3.11.2 and `python-sat` was 1.9.dev15. A second pass of
the independent script over that directory checked every generated CNF,
witness, result record, and proof-file digest; its compact output is
`FULL_REPLAY.json`.

The fresh proof corpus contained 1,604,725,414 bytes and is intentionally
omitted from Git. Its proof hash matched the earlier run in 366 of 518 cases;
this is expected because DRAT output is not canonical, and every fresh proof
was checked against its exact fresh CNF. The corpus is regenerated and checked
by the command above. The target's included compact RUP certificate
for complete task `bo1-q7-r5-c000145` was separately compiled and checked:
8,722/8,722 additions were RUP, and all 2,069 core clauses mapped to exact
source positions.

## Inputs and trust boundary

Target source commit:
`587202475ed3fb74b8f86b1777b73b9f86b49c5e`.

Catalog: Brendan McKay's 12,800-byte `r44_15.g6`, 640 records,
SHA-256
`53a46ba21cb16805eb07775b60746f783864388538368955e72cbdae5ae8f4e1`.

The finite status claim is independently replayed. Global coverage still
imports the independently reviewed h3873 carrier reduction, the h3887 task
interface, and the external completeness of McKay's catalog. This review
checks the part of the h3887 interface used by h4001 but does not review
h3887's full carrier-count theorem. Remaining trust lies in the unformalized
mathematical reduction, exact Python and C/C++ implementations, the PySAT
CaDiCaL300 engine, `drat-trim`, SHA-256, the OS, and hardware. The full proof
corpus is reproducible but not archived here.
