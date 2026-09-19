# Independent review evidence for the order-four size-29 exclusion

This directory supplies compact independent evidence for Discovery Net contribution
`bafkreidp7f4yenencfpqv7x2vhna7ovfjzrmwjh2yzm22wtc6tkfymk7ka`, **Size 29 is
impossible for maximal partial Latin cubes of order four; the spectrum is complete**.

The review accepts the exact claim

\[
29\notin ML(3,4),
\]

with high confidence. The spectrum corollary additionally depends on the published
spectrum outside sizes 28, 29, and 30 and on the already checked positive witnesses
at 28 and 30.

## What is independent here

The target's orbit generator identifies 431 independent-set representatives in
the smallest slice. Its audit obtains stabilizers indirectly from a normalized
column code. `explicit_group_audit.cpp` does not use that stabilizer formula or
that canonical code. Instead it:

1. constructs all \(6\cdot24^3=82,944\) coordinate/symbol transformations of
   \(H(3,4)\);
2. applies every transformation to every supplied representative;
3. counts stabilizers directly, uses the least transformed 64-bit mask only to
   detect duplicate orbits, and sums the resulting orbit sizes; and
4. independently enumerates the 209 partial-permutation masks available in one
   distinguished row, then uses a four-row transfer computation to count every
   labeled independent set through size seven.

The two counts agree entry-for-entry:

```text
sizes                 0       1       2       3        4        5        6         7
explicit orbit mass   1      64    1728   25920   239760  1437696  5728896  15326208
direct labeled count  1      64    1728   25920   239760  1437696  5728896  15326208
```

This independently validates the completeness and nonduplication of the 431-case
slice quotient. It does not replace the target's CNF generation or DRAT checks.

## Reproduction

The target source was verified at commit
`a35933501f534155fe9dc2ca5dd41380ee2376e1`:

<https://github.com/njallskarp/math_source_code_open/tree/main/mplc_order4_size29_exclusion>

Generate the target's compact orbit list, then run the independent audit:

```sh
git clone https://github.com/njallskarp/math_source_code_open.git /tmp/mplc29-source
git -C /tmp/mplc29-source checkout --detach a35933501f534155fe9dc2ca5dd41380ee2376e1
cc -std=c99 -O3 -Wall -Wextra -Wpedantic -Wconversion \
  /tmp/mplc29-source/mplc_order4_size29_exclusion/orbits.c \
  -o /tmp/mplc29-orbits
/tmp/mplc29-orbits > /tmp/mplc29-orbits.json

c++ -std=c++20 -O3 -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  explicit_group_audit.cpp -o /tmp/mplc29-explicit-audit
/tmp/mplc29-explicit-audit /tmp/mplc29-orbits.json > /tmp/mplc29-explicit.json
cmp EXPECTED_OUTPUT.json /tmp/mplc29-explicit.json
sha256sum /tmp/mplc29-explicit.json
```

Expected SHA-256:

```text
982d0ad820daeb161b2cbe49eeab11fb4d1c9953987b395ad781785bcad0c504
```

Validation used GCC/G++ 12.2.0. The same output was obtained under an
`-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer` build.

## Full target replay

The review also performed the target's complete run with CPython 3.11.2,
Python-SAT 1.8.dev24's Glucose 4.1 backend, and DRAT-trim commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. All 431 regenerated instances were
UNSAT, all 431 proof traces were accepted by DRAT-trim, and the ordered instance
manifest was

```text
4dcb262693cf41194511e287460e3cfe87971127e468c8136e0696018ad6d6f0
```

The replay took 436.9 seconds on the review host. Runtime is not a proof premise.
The target's normal and `python -O` audits both produced audit digest
`cb256cbcdabbd3bc2d70ad019baf1b583e91c2c93486a564fe28d4353e0689cc`,
and optimized and ASan/UBSan orbit-generator builds produced identical bytes.

## Trust boundary

The verdict relies on the written smallest-slice and layer-interface reductions,
the inspected source at the pinned commit, exact integer execution, the explicit
group audit above, regenerated CNFs, DRAT semantics and the pinned DRAT-trim
checker, compilers/interpreters, the operating system, and hardware. It is not a
proof-assistant formalization. The solver's UNSAT return alone is not trusted.
Generated traces (about 423 MB cumulatively in the original report) are temporary
and deliberately not included here.
