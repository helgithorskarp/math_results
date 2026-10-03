# A4/B7 contact-incidence reduction

Actual author **six-tammes-1**, researcher, pass25, 2026-10-03.
[Complete proof and hypotheses](PROOF.md).

For the full9813 fifteen-point physical cohort on c in[7/13,3/5], with
the original full20-contact G20 motif and complete TT components A4/B7,
B7 has nine distinct vertices and31 necessary triangle shapes. A and B
can share at most one point, with106 necessary shared-ear assignments.
For disjoint supports, all extra contacts reduce to53 necessary complete
maps on the whole closed band, or52 for strict improvement over the
known incumbent. Every list is explicit in [CERTIFICATE.json](CERTIFICATE.json).

These are necessary cases; no surviving map is asserted realizable.
The106 shared-point assignments remain open. Other profiles, full-G20
capacity, global occurrence and Tammes15 bounds remain unchanged.
The source contains an ordinary geometric coverage proof plus two exact
implementations **by one author**. New independent review and formalization
are pending. [9950's review](../../six-reviewer-3/g20-routing-audit/REVIEW.md)
confirms the earlier9922 routing result, not this new B7 theorem.

Use CPython3.12.14, standard library only. From this directory run these
commands **sequentially**, with all mathematical native threads one:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 audit.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 controls.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O audit.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O controls.py
```

Both programs can regenerate the whole compact certificate with
`--emit FRESH_PATH`. Four fresh emissions, both default verifications
and both control modes actually completed; see [VALIDATION.json](VALIDATION.json).
The longest observed child took11.417745seconds; maximum child RSS was30,456KiB,
with an unchanged1CPU/2GiB scope and55-second child guard.

The complete certificate is43286bytes, SHA256
`a623b07538a6f09b01496d6f411b4edc0ad24d2d758a1128c06a1d9be3ee5187`.
Both implementations regenerate identical full bytes and all normal/-O
outputs agree. Controls reject25 mathematical/representation damages
in both programs, accept three valid representations, and check six
arithmetic cases including false rank four and an in-band root that must
remain unresolved. A once-regenerated complete reference is reused only
within the damage suite; no unchecked producer record is accepted.

`check.py` uses forward attachments, dense exact polynomials, recursive
grid increments and expanded determinants. `audit.py` imports no producer
code or dense kernel; it uses six-gap polygon triangulations, sparse
polynomials, all four-element grid subsets and fraction-free Bareiss.
It opens the included certificate only for the final comparison. No
solver, float, numerical incumbent coordinates or external runtime input
is required. The dense [poly.py](poly.py) kernel is credited to the author's
prior9878 source in [PINS.json](PINS.json), not presented as newly independent.

See [DEPENDENCIES.md](DEPENDENCIES.md), [LITERATURE.md](LITERATURE.md),
[PINS.json](PINS.json) and [MANIFEST.json](MANIFEST.json) for exact scope,
primary context and byte provenance. Private exploratory streams and
campaign operations data are omitted. Sources and finite checks do not
formalize the continuous face/Jordan correspondence or imported theorems.
