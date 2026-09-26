# Symmetric simplex flaps have no convex quartic witness

For the canonical depth-one, sixteen-label simplex-flap contraction in
`R^3`, every spatial scale, positive Gaussian variance, and tetrahedrally
invariant weight balance satisfies

```
2*d3^2/(3*d2*d4) <= 4*sqrt(2)/7 < 1
```

when the gaps are nonzero. Together with the sharp relative moment-gap
bound, this proves comparison for every polynomial of degree at most four
that vanishes at zero and is convex on the possible density range.

This does **not** prove full majorisation, cover asymmetric weights, or
exclude higher-degree witnesses. The constant is not claimed optimal.
The fixture's obstruction to a continuous contraction in five dimensions
is classical, not a new claim.

[PROOF.md](PROOF.md) gives the exact reduction. `verify.py` checks 69,888
ordered replicas against 4,828 multisets, then certifies 2,531 positive
integer Bernstein coefficients covering the whole parameter domain.
No sample grid is used in the proof.

Reproduce with Python 3.11 or later, standard library only:

```sh
python3 verify.py --check
python3 -O verify.py --check
sha256sum -c SHA256SUMS
```

Expected status: `ALL_PARAMETER_QUARTIC_CERTIFICATE_PASS`.
The run takes about one second on the development host. `EXPECTED.json`
records the exact certificate hashes and output. Mathematical review and
proof-assistant formalization remain pending.

See [SOURCES.md](SOURCES.md) for dependencies and prior-work boundaries.
