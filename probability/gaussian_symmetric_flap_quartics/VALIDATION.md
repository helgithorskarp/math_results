# Exact validation and trust boundary

Tested with CPython 3.11.2, standard library only, on 26 September 2026.
Both commands completed successfully with byte-identical expected output:

```sh
python3 verify.py --check
python3 -O verify.py --check
```

`EXPECTED.json` SHA256:

```
c3bde948a5d8bd5983a1acbb6ca93a14359bcb146b1e8dee41705fd50fc2c51e
```

The computation checks all 120 labelled pairs, with 42 strict squared
distance decreases, and computes paired rank six in exact rational
arithmetic. The rank is a control, not a proof of nonliftability.

For degrees 2, 3, and 4, two different replica calculations agree on
every signed histogram entry:

| Degree | Ordered tuples | Multisets | Nonzero histogram entries |
|---|---:|---:|---:|
| 2 | 256 | 136 | 6 |
| 3 | 4096 | 816 | 21 |
| 4 | 65536 | 3876 | 42 |

The ordered implementation adds pair distances. The multiset implementation
uses the centroid identity and exact multinomial multiplicities. Both
cover their entire stated finite spaces; neither samples labels or weights.

Five univariate positivity certificates contain 2,531 strictly positive
integer coefficients in total. They are constructed once by the binomial
basis formula and once by homogeneous Horner evaluation. Exact equality
of those transforms is required. Factor divisions are checked by multiplying
back. The coefficients' counts, minima, endpoint factors, and hashes are
recorded in `EXPECTED.json`.

All proof checks use explicit exceptions and remain active under `python -O`.
Python integers have arbitrary precision; no fixed-width overflow or
floating-point sign assumption occurs. An ordinary run took about one
second on the development host. The compact source regenerates the complete
certificate, so no large coefficient dump is published or required.

The written reduction is essential: positivity of the five polynomials
implies a determinant inequality for all nonnegative weight ratios and
all `q` in `[0,1]`. The Gaussian replica formula then covers all scales and
variances. The previous relative-gap theorem supplies the extra comparison
needed for quartics convex only on the density range.

These algorithmically different internal checks do not constitute external
peer review or proof-assistant formalization. Both remain pending. Finite
higher-degree experiments are not evidence for the theorem's universal
quantifiers and are excluded from this source packet.
