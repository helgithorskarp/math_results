# K4 expansion physical decision: UNKNOWN at 1,800 seconds

The first physical decision using the h3899 K4 expansion interface ended
**UNKNOWN** at its fixed 1,800-second boundary. The task was
`bo1-q7-r7-c000000`, exactly the task used at h3893. The CaDiCaL 3.0.1 binary,
machine, wall cap, ordered h3881 shared-triangle base, and result policy were
held fixed; only the h3899 unique-extension constraints were added.

The augmented formula has 10,868 variables, 923,269 clauses, maximum width
eight, and SHA-256
`755dbcd5677bbc57a0865637dbce19fa72084c4846b3996b8697bf1485070178`.
It was already generated and independently audited in the h3899 package.
The solver made one call and returned exit code zero with no status line and
the exact witness `c UNKNOWN`.

The h3897 separator classification underlying the expansion rule was
independently accepted at h3907. The dependent h3899 propagation interface
has not received an external review.

Compared with the h3893 base run, the expanded run recorded 16.78% fewer
conflicts, 16.99% fewer decisions, 82.77% more propagations, and a 20.44%
smaller partial DRAT stream. Both runs remained UNKNOWN. These numbers are a
controlled one-run comparison, not a speedup claim or evidence that another
cap would decide the task. In accordance with the 05:45Z principal boundary,
the monolithic physical-SAT tractability gate failed.

The 1,185,586,651-byte partial DRAT stream has SHA-256
`428b04fb2eb1a6500f56a3e292a7aaad315ba4325913f012b2652d3a11009fa6`.
It is not an UNSAT certificate, was not submitted to drat-trim, remains
private, and is not published. There is no SAT model. This result excludes no
task, constructs no good43, and proves no Ramsey-number improvement. All
2,189,178 h3887 tasks remain undecided.

## Compact verification

With CPython 3.11.2 and its standard library, from the repository root:

```sh
python3 -B ramsey_r55_k4_expansion_q7r7_boundary/compact_check.py
```

This checks the exact UNKNOWN scope, all compact identities, formula and
runner hashes, comparison arithmetic, one-call gate, and private receipt
hashes. It runs no solver.

To regenerate the exact 35.5 MB formula and independently audit every literal
under normal and `-O` Python, supply the four pinned h3873 catalog inputs:

```sh
python3 -B ramsey_r55_global_maximal_packing/catalog.py /tmp/k4e-data --download
python3 -B ramsey_r55_k4_expansion_q7r7_boundary/reproduce.py /tmp/k4e-data
```

`reproduce.py` deliberately does not repeat the 1,800-second solver call.
[RESULT.json](RESULT.json) records the exact boundary,
[COMPARISON.json](COMPARISON.json) gives the controlled telemetry comparison,
and [VALIDATION.md](VALIDATION.md) states the evidence and trust limits.

No further monolithic task, backend variant, or longer cap is opened here.
The next campaign milestone requires a qualitatively different decomposition
or decision mechanism.
