# Independent two-five Tammes audit

Actual author **six-reviewer-3**, independent mathematical reviewer.
Target9025: verified within its complete contact-map hypotheses, with full
exclusion extended to closed `[1/2,3/5]` and the noncontacting case separately
extended to `[1/2,1)`. See [the complete proof and trust boundary](REVIEW.md).

Python3.11+ standard library, no runtime network input to the independent
mathematical checker. The exact source-field comparison uses the frozen
author record, when explicitly supplied. No CAS, solver, proof assistant,
original coordinates, graph, ledger or signing key is required.

From the repository root:

```sh
python3 -I -B round-two/six-reviewer-3/two-fives-audit/audit.py
python3 -I -B -O round-two/six-reviewer-3/two-fives-audit/audit.py
```

Both produce:

```text
PASS 266 exact checks; 8 damages rejected; full-record SHA256 b68fad64d50e7ee5f05a9c5fdb8850c882d5e015526fc0c48c0674085f8bc9b0
```

The entire canonical typed record is compared with [EXPECTED.json](EXPECTED.json).
`--emit-fixture PATH` is a generation command and does not validate a frozen
record; use the default commands above for validation.

For public source downloads and full source comparisons, with network access:

```sh
python3 -I -B round-two/six-reviewer-3/two-fives-audit/replay.py --fixture-damages
```

The replay verifies all 23 pinned input hashes, compares all ten complete
mathematical source fields, reruns both original programs in both modes,
compares COMPLETE stdout with their exact frozen files, and rejects six
missing/malformed/sign-altered independent external fixtures. All mathematical
jobs run sequentially with native thread variables set to one and 20-second
guards. [VALIDATION.json](VALIDATION.json) records observed resources.

This independent finite check uses actual-role paths, degree-deficit contacts,
connected full link cycles, original endpoint/opposite aliases, QQ incidence
budgets and literal exact endpoint Gram data. It explicitly imports the
already sufficiently reviewed7767 continuous local core on the open interval.
It does not independently regenerate that continuous certificate or the
earlier complete catalogue derivations. [INPUTS.json](INPUTS.json) binds each
source and states its role. Written geometry, original-label correspondence
and coverage reductions remain ordinary mathematics, without formalization.
No global numerical Tammes improvement is claimed.
