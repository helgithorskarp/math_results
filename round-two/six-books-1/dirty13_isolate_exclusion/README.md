# A 952-byte proof certificate for the isolated dirty13 type

Actual author six-books-1, researcher. PROOF.md gives the conditional
108-edge/max-degree-ten theorem, the exact graph, and all coverage bridges.
No rootlessness or outside minimum degree is assumed. With classification
8939 the local domain drops from fourteen to thirteen marked types.
The surviving leaf type, other completions, and Ramsey endpoint remain open.

Run serially with Python 3.11.2 (standard library only):

```sh
python3 -B check.py
python3 -B verify.py
python3 -B -O verify.py
```

Expected: two direct degree cases have totals -24 and -1; all 297 split
cases are excluded by four integer vectors, with first-use counts
293,2,1,1. expected.json specifies complete records. Eight damaged inputs
must reject. Both algorithms must match the exact branch-set hash, not
just its size. Runs complete in under one second using under 20 MiB.
Every check uses explicit exceptions and remains active under Python -O.

certificate.json contains six integer counting vectors and their tag
orders. The complete finite pattern sets regenerate from compact source;
no private catalogue or downloaded optimizer is needed. The bit-pattern
producer and the literal-set checker share no implementation. Numerical
LP discovery, wheels, native SAT traces, and incomplete probes stay in
scratch and have no role in the public certificate replay. Ordinary
mathematical coverage and code correctness are unformalized. Same-author
algorithmic independence is not an independent peer-review verdict.

provenance.json records versions, resources and known primary-baseline
validation. MANIFEST.json hashes the compact public files.
