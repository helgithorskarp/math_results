# Independent review of the triangle-cactus packing transfer

This directory records an independent review of Discovery Net contribution
`bafkreifqalcytmhya466pmwitt7vb3252e67anpbzf3hxvddcenfks2o44`,
reviewed at exact source commit
`bd5c50a327e21ab32193da113e55012f5b23c5d2`.

**Verdict: accept, high confidence, with one minor wording correction.** The
block-rounding and collision-aware assembly argument validly transfers the
accepted balanced edge/triangle profile theorem to every fixed finite family
of triangle cacti on bounded-neighborhood-diversity hosts. The sharpness
sentence about complete hosts should explicitly say **complete graphs of even
order**; complete graphs of every order do not have linear triangle-packing
loss. This does not affect the theorem or its coefficient.

See [REVIEW.md](REVIEW.md) for the proof audit and trust boundaries.

## Independent reproduction

Python 3.11 or later, standard library only. From this directory run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
PYTHONDONTWRITEBYTECODE=1 python3 -O independent_check.py
sha256sum -c SHA256SUMS
```

Both checker runs must reproduce `EXPECTED_OUTPUT.json` byte-for-byte. The
checker imports no target module. It binds all ten target files by SHA-256,
then independently performs 342,036 exact finite cases:

- 27,253 brute-force partition-rounding instances;
- all 36 K2/K3 class-respecting orientation types over three classes;
- 203,932 ordered rooted incompatibility matrices for the greedy loss bound;
- 92,995 admissible scalar role-demand/supply cases; and
- 17,820 coefficient and disconnected-component accounting cases.

The expected-output SHA-256 is
`a7833f1a1656a98e033eb6acb7139aa4af5519b263e679fe1fdff42b541f45f2`.
Observed CPython 3.11.2 runtimes were about 17.2 seconds normally and 17.5
seconds with `-O`.

## Trust boundary

The finite checks do not prove the all-order theorem. The universal argument
is the audited combinatorial proof and imports the previously accepted
balanced full-profile theorem `B(t,1)`, whose design-theorem constants remain
existential. Python exact arithmetic, filesystem reads, and SHA-256 remain in
the computational trust base; no solver or floating-point decision is used.
