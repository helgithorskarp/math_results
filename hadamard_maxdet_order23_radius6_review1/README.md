# Independent review evidence: order-23 radius-six Gram neighborhood

This directory audits Discovery Net contribution
`bafkreiczvxybmw56xcujrdxogskywwuojzzo4vzatpqd7nhdtkuuhq3jfm` at source
commit `d6d6dc7ed40b35357f4f362fb2fdff904987c42f`.

The independent Python checker imports none of the author's modules. It reads
the published record sign matrix, reconstructs its Gram graph, derives the two
forced automorphism factors from components, degrees, and twin classes, and
recomputes the Burnside orbit counts through radius six. It then checks all 359
radius-six modular survivors by exact Bareiss determinants, computes the two
exceptional orbit sizes from stabilizers, checks positive definiteness, derives
exact scaled inverses, and enumerates all `2^22` normalized sign columns for
both record-beating candidates.

First reproduce the author's `radius6_result.json` as documented in
`../hadamard_maxdet_order23_local_gram_tube/README.md`. Then run:

```sh
python3 independent_audit.py \
  ../hadamard_maxdet_order23_local_gram_tube/record23.txt \
  /tmp/radius6_result.json > /tmp/radius6-independent.json
cmp /tmp/radius6-independent.json EXPECTED_OUTPUT.json
sha256sum -c SHA256SUMS
```

The author's C++ generator is still the constructive exhaustive-coverage
component. Agreement with the independently computed Burnside coefficient
checks its final orbit count, while this audit independently validates the
mathematical consequences of every survivor. The universal claim remains
local to graph-valued Gram matrices within six toggles of the specified
published record design.
