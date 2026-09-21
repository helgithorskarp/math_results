# Review package: stellar transport of toggle words

This directory contains an independent high-confidence review of
[`stellar_toggle_transport`](../stellar_toggle_transport/).

The review audits the universal carrier proof, exact Möbius identities,
local reversible macro, optimality argument, barycentric corollary, and
surface applications.  The verdict, human premises and limitations are in
[`REVIEW.md`](REVIEW.md).

## Reproduction

Use CPython 3.11.2 or later; only the standard library is required.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 audit_independent.py > actual.json
diff -u EXPECTED_OUTPUT.json actual.json
PYTHONDONTWRITEBYTECODE=1 python3 -O audit_independent.py > actual-optimized.json
diff -u EXPECTED_OUTPUT.json actual-optimized.json
sha256sum -c SHA256SUMS
```

The checker imports no target module.  It uses a dynamic-programming search
for local one-use macros, exhausts every four-label complex, verifies the
carrier and barycentric reductions, replays the three surface seeds, and
performs an independent shellability search.

`../stellar_toggle_transport/seeds.json` is its only external input.  No
solver, third-party package, randomness, floating point, generated catalogue,
or omitted certificate is used.
