# Complete propagation of the A5 physical pair exclusions

The h4191/h4193 pair exclusions close **226 additional affine pencils** and
their **3,064,704 previously admissible five-curve sets**. The exact-five
residual is now **4,886 pencils / 125,807,232 admissible five-curve sets**.
This is the complete effect of those pair exclusions on the h4185 pencil
frontier, alongside the h4167 incidence constraints.

Exactly **2,960** further global pair systems cannot support an exactly-five-
active counterexample. They move to the existing at-least-six mode. Every
retained exact-five pair has a checked constraint-avoiding extension:

| mode | systems | conservative orbit allowance |
|---|---:|---:|
| exact-five compatible | 118,520 | 3,503,032 |
| requires at least six | 10,176 | 310,400 |
| whole frontier, unchanged | 128,696 | 3,813,432 |

These are necessary-condition survivors, not physical candidates or root
counts. The result neither reduces the whole-system count nor closes A5.
No <=508 five-chromatic graph is established.

Each closed pencil has a small certificate: three of its sections such that
**every choice of one curve from each section contains a proven forbidden
pair**. Only 19,504 such triples need checking across all 226 witnesses.
The [proof](PROOF.md) gives the completeness and counting arguments, and
[FRONTIER.md](FRONTIER.md) specifies the exact residual and dependencies.

With the pinned source interfaces regenerated as in
[REPRODUCE.md](REPRODUCE.md), run from the repository root:

```sh
python3 -B hadwiger_nelson_radix_pair_exclusion_propagation/verify.py \
  --frontier /tmp/hn-propagation-input.json \
  --incidence /tmp/hn-propagation-incidence.json --check-expected
python3 -O -B hadwiger_nelson_radix_pair_exclusion_propagation/controls.py \
  --frontier /tmp/hn-propagation-input.json \
  --incidence /tmp/hn-propagation-incidence.json
```

The new scripts use CPython 3.11.2 and its standard library. The independent
checker takes about 14 seconds in the measured run. It enumerates rank-two
RREF normal spaces, checks literal Cartesian-product transversals, recounts
the entire changed subset, and verifies 118,520 constructive extensions.
The producer uses projective pair spans and integer bitset propagation and
also freshly reproduces the full 128,871,936-lift baseline.

The **8,672-byte** certificate SHA-256 is
`1ca587a034b9cd27f30c57bd1df9e5d3af46721cbc9fa0774f28261088899dec`.
Fresh generation is byte-identical, normal and optimized verification agree,
and all full residual exports agree byte-for-byte. The 2,774,033-byte residual
table is regenerated locally and is not committed. See
[EXPECTED.json](EXPECTED.json) and [VALIDATION.json](VALIDATION.json).

This new consequence is author-checked; independent reviewer-1 assessment is
pending. The physical implication imports h4191's pair theorem, and the global
allowances retain the upstream h4177/h4117/h4175 accounting boundary. HN3 remains
parked and has not been contacted. The completed pass stops at this propagation
boundary.
