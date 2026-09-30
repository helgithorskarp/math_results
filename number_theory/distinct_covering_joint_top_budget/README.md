# Joint top-resource and known-footprint bounds

Actual author **six-covering-2**, role **researcher**.

The [proof](proof.md) computes the exact maximum combined unrestricted and
useful periodic top charge by a set-partition reduction. It also permits
the periodic weight to be positive on placed classes, charging their known
footprints with multiplicity. The latter removes the zero-weight barrier
caused by a placed modulus coprime to the weight period.

The result builds on six-covering-3's primitive-block argument and
equal-label merging, and cites that author's newer coarsest-resource upper
relaxation. The 20160 covering fixture is an attributed reproduction of
six-covering-1's construction. These are finite necessary inequalities;
neither10080 nor15120 is excluded here and no numerical bound improves.

From the repository root, with Python3.10+ and the standard library only:

```sh
python3 -B number_theory/distinct_covering_joint_top_budget/check.py
python3 -B -O number_theory/distinct_covering_joint_top_budget/check.py
```

Expected output: `all_passed: true`, `actual_phase_tuples_checked: 206532`,
`genuine_cover_cases: 45`, `malformed_inputs_rejected: 10`.
The complete compact evidence is [expected.json](expected.json). The
checker requires equality with that file; the maintenance-only
`--write-expected` option deliberately regenerates it.

[joint.py](joint.py) supports exact cofactors with at most four divisors,
returns actual phase witnesses, and evaluates all actual unused modulus
capacities. The universal partition theorem is written for any cofactor;
large-cofactor optimization is not implemented. All units are physical
residue weights. A primitive-block top budget has no N/Q multiplier.

Source files and exact Python arithmetic are software trust boundaries;
no formal kernel or independent reviewer certification is claimed. The
copied [positive_cover.json](positive_cover.json) is pinned to SHA256
`f3b7ab8112f2fdba3ab32ea992f2380c43c404e8b54c8abdd71c839a9f5424e3`.
Its authorship, source commit and independent review are identified in the
proof. Private discovery LPs, partial frontiers and raw logs are omitted.
