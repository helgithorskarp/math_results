# A 41-hole obstruction to repairing a specified period-10080 base

Actual author: **six-covering-1**, role **researcher**. All team signatures
share an identity, so this name identifies the mathematical author.

The supplied 65-class assignment has distinct moduli, minimum exactly 8,
actual LCM 10080, and **87 uncovered residues**. It is a near-cover.
Its 30 congruences whose moduli are not divisible by 7 form a specified
base on 1440 residues. Keeping that base fixed and choosing arbitrary
full phases for any subset of the other 35 eligible moduli always leaves
**at least 41 uncovered residues in a full period**. In particular, changing
the tails' allocation among the seven slices cannot repair this base.
The conditional optimum remains between 41 and 87.

A 76-point integer weight vector, with weights at most four, gives the
certificate. Its base weight is 232, full-period weight is 1624, and the
sum of all 35 tail capacities is 1463. The deficit is 161. These are exact
ordinary congruence calculations, with no optimizer in the proof.

The same weights give a necessary phase constraint for **any** distinct
covering whose moduli are divisors of 10080 and are at least 8. If `R` is
the sum of the selected base-phase coefficients defined in [the proof](proof.md),
then a covering must have **R >= 23**. The supplied assignment has R = 0.
This is a construction constraint, not an exclusion of period 10080.
It neither establishes an exact conditional optimum nor changes a global
bound on the minimum LCM at minimum modulus exactly eight.

Reproduce from the repository root with Python 3.11 or later; the standard
library suffices:

```bash
python3 -B number_theory/distinct_covering_10080_fixed_base_weights/check.py \
  number_theory/distinct_covering_10080_fixed_base_weights/near_cover.tsv \
  number_theory/distinct_covering_10080_fixed_base_weights/certificate.json
python3 -B number_theory/distinct_covering_10080_fixed_base_weights/check_controls.py
```

The first command checks all 10080 physical residues, all 34391 eligible
tail phases, and all 4893 base-phase coefficients. Expected totals are
`1624, 1463, 161, 41, 23`; the fixture has 87 literal holes and missed
weight 212. The second command checks 12 complete tiny families, including
omitted labels, with 9342 phase/omission vectors and six malformed inputs.
The control-event SHA256 is
`88799a49ebfabef0ce20333dc7d41d09580553b57daf5c7a045f5029f5579879`.

The fixture SHA256 is
`50a6b10a90b3ab3172b2e011b459a30cf3f1a41afba6b4b6a78f2f3076da0801`;
the certificate SHA256 is
`7d1013ff4270d65e329ba02328343e1b9921fe9f355e44d1f989b48bab51d964`.
The checker, written separately from the discovery code, imports no LP,
SAT, CRT updater, or projected-capacity routine. This is an author check;
independent review and proof-assistant certification are not claimed.

Weighted resource counting is already part of
[six-covering-2's weighted quotient work](../distinct_covering_residual_weight_duals/proof.md).
The contribution here is this explicit certificate, its conditional
41-hole bound, and its corresponding necessary phase inequality.

Primary problem context is [Zhang–Zhang](https://arxiv.org/html/2607.19029)
and [HKLT Problem 3](https://arxiv.org/html/2605.18644). The minimum-seven
statement and the pure 2/3/5-support question are separate from this claim.
No general weighted-counting theorem or published result is claimed as new.
