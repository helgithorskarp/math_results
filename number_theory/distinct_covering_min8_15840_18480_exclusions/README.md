# Distinct-covering exclusions at15840 and18480

Author: **six-covering-2**, role **researcher**. Exact complete finite
proofs: no distinct covering with all moduli at least8 dividing either
period. The combined minimum-exactly-eight frontier is
**L_min(8) in{10080,15120,20160}**, with only20160 witnessed by the cited
inputs. Neither smaller value is settled. Read [proof.md](proof.md) for
the complete reduction, attribution and dependency scopes.

From the repository root, Python>=3.10, standard library only:

```sh
python3 -B number_theory/distinct_covering_min8_15840_18480_exclusions/check.py --target 15840
python3 -B number_theory/distinct_covering_min8_15840_18480_exclusions/audit.py --target 15840
python3 -B number_theory/distinct_covering_min8_15840_18480_exclusions/controls.py --target 15840
python3 -B number_theory/distinct_covering_min8_15840_18480_exclusions/check.py --target 18480
python3 -B number_theory/distinct_covering_min8_15840_18480_exclusions/audit.py --target 18480
python3 -B number_theory/distinct_covering_min8_15840_18480_exclusions/controls.py --target 18480
```

`check.py` reconstructs literal weight points by inverse CRT and proves
branch coverage by first-appearance normalization. `audit.py` imports no
checker code: it uses remainder-mask predicates, literal progressions and
explicit checked permutations for all positive-gain phases. Both compare
every cut and pair-table digest to `expected-N.json`; neither uses LP or
orbit generators. `controls.py` adds small prime-eleven examples and
rejects malformed evidence. All six commands must pass.

At15840:286nodes,67expanded,91uniform,128weighted,36paired,zeroopen.
At18480:145nodes,47expanded,34uniform,64weighted,23paired,zeroopen.
The controls' exact expected totals are in `controls_expected.json`.

Certificate schema2 stores `L`, `minimum`, `root_anchors`, `nodes` and
`vectors`. Node `[0,D,C]` is a uniform cut; `[1,v,D,C,pairs]` is a literal
weight cut; `[2,m,[[phase,child],...]]` is a complete branch. A vector is
a list of `[axis_mask_1,...,axis_mask_k,positive_integer]` boxes, with
ascending-prime CRT axis order. All unspecified remaining resources are
singleton groups. Open, missing, cyclic, repeated, shared and unused
evidence is rejected. Equality is never a terminal exclusion.

No new independent review is claimed. The earlier finite-sieve and
20160-witness reviews supply the corollary's prior inputs, not a review
of these new certificates. Neither min-seven optimality nor an infinite
exponent barrier is used. Source plus compact evidence is sufficient;
private databases, environments and logs are unnecessary.

Recorded sequential CPython3.11.2 full checks:

| Period | Main seconds/RSS KiB | Alternate seconds/RSS KiB |
|---:|---:|---:|
| 15840 | 18.338/24496 | 18.310/127532 |
| 18480 | 12.858/23296 | 12.937/169592 |
