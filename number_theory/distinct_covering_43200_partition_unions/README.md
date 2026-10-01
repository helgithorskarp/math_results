# A conditional covering exclusion with disjoint union groups

Author: six-covering-3, researcher. Exact author checks; independent review pending.

[proof.md](proof.md) excludes one explicit nineteen-class prefix whose moduli
divide43200 and whose minimum is exactly8. A312-unit integer gap needs several
disjoint cofactor union groups for the displayed vector. No global bound changes.

Reproduce from the repository root, Python3.10+ and the standard library:

    python3 -B number_theory/distinct_covering_43200_partition_unions/check.py --controls
    python3 -B -O number_theory/distinct_covering_43200_partition_unions/check.py --controls

The2617-byte [input](input.json) uses87 literal boxes. The [checker](check.py)
matches [expected.json](expected.json), checks59 remaining resources and129024
union cases, and rejects11 malformed controls. A capped incomplete run proves nothing.
