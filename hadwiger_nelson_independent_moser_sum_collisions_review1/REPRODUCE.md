# Reproduce the independent review

Requirements: CPython 3.11 or later and a C++17 compiler with signed
128-bit integer support. This review used CPython 3.11.2 and g++ 12.2.0.

From the repository root, build the target's exact native checker and replay
all physical graphs:

```bash
mkdir -p /tmp/hn-moser-collision-review
g++ -std=c++17 -O3 -Wall -Wextra -Wpedantic -Wconversion \
  -shared -fPIC \
  hadwiger_nelson_independent_moser_sum_collisions/geometry.cpp \
  -o /tmp/hn-moser-collision-review/geometry.so
python3 -B hadwiger_nelson_independent_moser_sum_collisions/verify.py \
  --library /tmp/hn-moser-collision-review/geometry.so \
  > /tmp/hn-moser-collision-review/verification.json
cmp /tmp/hn-moser-collision-review/verification.json \
  hadwiger_nelson_independent_moser_sum_collisions/expected.json
python3 -B hadwiger_nelson_independent_moser_sum_collisions/controls.py \
  /tmp/hn-moser-collision-review/geometry.so
(cd hadwiger_nelson_independent_moser_sum_collisions && \
  sha256sum -c SHA256SUMS)
```

Run the clean-room alternate-basis audit in both interpreter modes:

```bash
python3 -B \
  hadwiger_nelson_independent_moser_sum_collisions_review1/independent_audit.py \
  --certificate hadwiger_nelson_independent_moser_sum_collisions/certificate.json \
  --expected hadwiger_nelson_independent_moser_sum_collisions/expected.json \
  > /tmp/hn-moser-collision-review/independent.json
python3 -B -O \
  hadwiger_nelson_independent_moser_sum_collisions_review1/independent_audit.py \
  --certificate hadwiger_nelson_independent_moser_sum_collisions/certificate.json \
  --expected hadwiger_nelson_independent_moser_sum_collisions/expected.json \
  > /tmp/hn-moser-collision-review/independent-opt.json
cmp /tmp/hn-moser-collision-review/independent.json \
  /tmp/hn-moser-collision-review/independent-opt.json
cmp /tmp/hn-moser-collision-review/independent.json \
  hadwiger_nelson_independent_moser_sum_collisions_review1/EXPECTED.json
(cd hadwiger_nelson_independent_moser_sum_collisions_review1 && \
  sha256sum -c SHA256SUMS)
```

For full undefined-behaviour coverage, compile `geometry.cpp` with
`-O1 -g -fsanitize=undefined -fno-sanitize-recover=all`, use that shared
library in the same verifier command, and run Python with `-O`.
