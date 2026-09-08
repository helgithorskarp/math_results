# Validation record

Development host validation used CPython 3.11.2 and
`g++ (Debian 12.2.0-14+deb12u1) 12.2.0`.

The release build used:

```sh
g++ -O3 -std=c++20 -Wall -Wextra -Werror -pedantic enumerate.cpp -o /tmp/drt-enum
/tmp/drt-enum core.edges
```

It returned status zero and exactly `EXPECTED.txt`. The complete 352,716-row
enumeration took about 0.05 seconds.

The independent standard-library Python checker used a distinct prime and
returned exactly `EXPECTED.json` in about 1.2 seconds:

```sh
python3 -B verify.py core.edges
python3 -B -O verify.py core.edges
```

Both ordinary and optimized modes agreed. The checker also literally tested
all 5,985 four-sets and 20,349 five-sets needed to confirm that the forward
core has no `K4` and no independent five-set.

Strict UBSan and combined AddressSanitizer/UBSan builds both returned the same
transcript as the release build. `reproduce.py` retains UBSan in the standard
replay and exercises three malformed-input controls against both
implementations: a false header count, a duplicate edge, and truncation. All
six damaged-input runs fail visibly.

All modular accumulators are signed 64-bit integers. The largest unreduced
sum in the reconstruction has at most 21 terms below `p^2`, hence is below
`21(1,000,003)^2 < 2.2e13`, far below `2^63-1`. Exact integer commutator and
Gram sums have 21 terms in `{-1,1}` and are likewise safe. Mask enumeration
uses an unsigned 32-bit value for `2^21` states.
