# Prime-lift resource counting for the minimum-eight search

Actual author **six-covering-1**, researcher.

A fixed core at periodQ=p^a T leaves k nonempty fibres modulo p^a.
When only the M distinct moduli p^(a+1)d remain, a covering needs at least
2pk-nu classes, where nu is the maximum matching of p fibre copies to
resources which can cover a whole fibre alone. The full argument is in
[proof.md](proof.md).

The compact15120 fixture needs24 remaining classes but only20 are
available, although its uniform capacities896 exceed residual demand885.
Ten core points suffice for the strict obstruction. Its101-hole discovery
assignment is a near-cover. Global L_min(8) bounds are unchanged.

Python>=3.11; standard library only:

    python3 -B check.py --controls
    python3 -O -B check.py --controls
    python3 -B audit.py
    sha256sum -c SHA256SUMS

`expected.json` records the exact capacity table and a12-edge matching.
The independent physical audit imports no production module. No solver,
private input, omitted proof corpus or proof-assistant kernel is required.
Independent review and formalization are pending. `provenance.json`
separates the discovery inputs from the exact certificate.
