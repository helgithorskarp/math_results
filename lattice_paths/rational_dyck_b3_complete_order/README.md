# Complete matching order and covers on D(a,3)

For every `a>3` coprime to three, this contribution classifies **all**
matching covers on the rational Dyck paths from `(0,0)` to `(a,3)`.
Every matching score is distinct. An explicit three-block order gives
arithmetic rank, inverse rank, and cover tests without evaluating a
continued fraction.

The previous height-three results gave local comparisons and one infinite
family of nonlocal covers. The new completion proves that this family is
exhaustive and gives the full relation between the two orders, using the
previously accepted Lagrange classification. With `m=floor(a/3)`, there
is exactly one nonlocal matching cover at each Lagrange-fibre distance
`2,...,m-1`. There are exactly `binom(m+1,3)` unequal-fibre pairs whose
matching and Lagrange orders disagree.

[PROOF.md](PROOF.md) states the full chain and closed rank formulas,
proves every comparison, and gives exact cover and fibre-gap histograms.
It includes two new six-term positive certificates for the layer boundaries.
[SOURCES.md](SOURCES.md) distinguishes the earlier ingredients, the new
classification, and the current literature.

The universal matching proof is self-contained after the standard
continued-fraction definition. The comparison with Lagrange scores uses
the explicitly cited prior height-three theorem. This does not classify
height four or higher, and no independent review of this new package is
claimed.

## Reproduce

Use CPython 3.11 or newer; there are no third-party requirements. From this
directory:

```bash
python3 -B identities.py
python3 -B verify.py --check
python3 -B -O verify.py --check
sha256sum -c SHA256SUMS
```

The final verifier line is:

```text
PASS: complete order, arithmetic ranks, all covers, exact Lagrange comparisons, and universal identities
```

[EXPECTED.json](EXPECTED.json) contains deterministic counts and hashes:

* 66,417 literal paths and all 66,339 matching covers at the 78 endpoints
  `4<=a<=120`, `3` not dividing `a`;
* 2,741 paths and 165,866 cyclic digit cuts for exact Lagrange comparisons
  through `a=40`, checking all 2,716 matching covers in that range;
* nine universal Laurent identities, including twelve positive boundary
  coefficients;
* 36 rank/inverse-rank checks at large endpoints up to 1,001 digits, and
  thirteen rejected malformed inputs or altered chains.

The default audit took approximately 9.25 seconds on the original Linux
host under CPython 3.11.2. Runtime is corroborative metadata, not an expected
result. The finite audit independently generates the carrier and sorts
literal scalar-continuant scores. It does not use the proposed chain to
prune candidates. Lagrange values are compared as exact rational squares
at every cyclic digit cut, including cuts inside `1,1` blocks.

The universal identity certificate digest is
`a7aad546e8415382930a6f8647a8015a64585c61416b353e87ea5eb7fb4e25e9`.
The matching-record digest is
`4516ae0a5acfe87478cec05c537689b56c3ee8267cf26e2e16c6f4fd401a2ee2`.
The Lagrange-record digest is
`b4feeac97db45affd56d4feb64bbb6a4ad45bf3d8c9818eb860a76708064e609`.

## Use the arithmetic classification

```bash
python3 -B order.py 31
python3 -B order.py 31 --rank 30 1 0
python3 -B order.py 31 --unrank 11
```

The second command prints `11`; the third prints `30 1 0`.
For `a=31` there are 176 paths, 175 matching covers, 140 common oriented
covers, 26 matching covers tied in the Lagrange order, one reversed
adjacent-fibre cover, and eight nonlocal covers. The nonlocal fibre
distances are exactly `2,...,9`.

All source and evidence are compact text. The checkers use Python integers
and `Fraction`, with no numerical zero tests, solver, random sample,
external dataset, generated catalogue, or large certificate. They are not
proof-assistant kernels. Finite verification corroborates the written
universal proof rather than replacing it.
