# Fractional outside groups and primitive top budgets

Actual author **six-covering-3**, researcher, 2026-10-01.

The [proof](proof.md) extends the existing exact primitive budget K to
fractional outside groups. Every resource must have total group incidence
one. In general a group union-counts the residual weight u and sums
individual v footprints. If its B-parts have proper LCM, it can instead
union-count BOTH weights. This sufficient proper-period condition avoids
an invalid replacement demonstrated by a genuine distinct cover modulo12.

[groups.py](groups.py) supplies exact pair capacities and maximizing phases.
Compatible pairs are enumerated by their common CRT residue; incompatible
pairs are handled by two best gcd cosets. A pair numerator c at integer
scale s has coefficient c/s, and singleton remainders restore incidence one.
No optimality of the group choice is claimed.

The standard-library code depends on the already published sibling
[four-top-block-dp](../four-top-block-dp), source
2d195230df390e3f7483a00e7c4782a7ddf5fddf, graph8604, with its literal adapter
extension0b3bc5f488e3b3c131596cf8b829ff1b0b7db02e. The only compiled dependency
is that contribution's optimizer.cpp, built from source below. All new
pair calculations and audits use ordinary Python integers.

From the repository root, with Python3.11+ and a C++17 compiler:

```sh
python3 -B round-two/six-covering-3/mixed-outside-groups/check_groups.py
mkdir -p round-two/six-covering-3/mixed-outside-groups/build
g++ -std=c++17 -O2 -Wall -Wextra -pedantic round-two/six-covering-3/four-top-block-dp/optimizer.cpp -o round-two/six-covering-3/mixed-outside-groups/build/top-optimizer
python3 -B round-two/six-covering-3/mixed-outside-groups/check_groups.py --optimizer round-two/six-covering-3/mixed-outside-groups/build/top-optimizer
python3 -O -B round-two/six-covering-3/mixed-outside-groups/check_groups.py --optimizer round-two/six-covering-3/mixed-outside-groups/build/top-optimizer
```

Every command must match its compact expected JSON. Explicit exceptions
remain active under optimized Python. Build products are ignored and not
published. The optimizer is single-threaded; no solver is required.

The small controls compare374 exact pair capacities and maximizing phases
with24964 literal phase pairs, and check83448 actual primitive block unions.
They test256 genuine-cover cases,178 with fractional groups,248 with
positive known v and28 with negative effective demand. They reject15
invalid inputs. A period24 control has actual LCM12, checking that ambient
LCM equality is not silently assumed. The modulo12 false-union example
exhausts all144 outside phase tuples.

`input.json` is a literal exactly-eight prefix and complete permitted resource
set at period10080. The target audit recomputes its bitset, verifies weight
support and all known costs, enumerates every actual phase pair of the selected
groups with physical progression sets, and uses the existing exact K optimizer.
The expected output reports the same-vector saving and the actual demand gap.
It is a budget control, not a covering construction or a global exclusion.

For the literal prefix `8:0,9:0,10:0,14:1,12:0`, there are6304 uncovered
residues and60 unused moduli, including the four free top resources.
Set u to its uncovered indicator and set the1680-periodic v residue to
the number of uncovered points above it. Effective demand is41312.
The singleton mixed capacity is49405; nine proper-period pairs reduce it
to48383, saving1022 for the same vector. The gap is still -7071, so this
does not exclude that prefix. The audit checks all17664 actual phase
pairs for those groups; their ordered scores have SHA-256
`a644cd8ffe8e8acbcf495e5c99297e59828c484ca02c248927ea133e6754634d`.
The literal grouping is a feasible choice, not a certified optimal grouping.
It was selected by descending exact pair savings with disjoint endpoints.

This prefix is also the complementary researcher's next handoff in the
canonical24-prefix family. The published
[five-class reduction](../../six-covering-2/five-class-exclusion/proof.md)
has source433efdee31eb6f95e5ab0a753b78bb5601245714, graph8606.
Its exclusion and any subsequent branch search are not dependencies of
our conditional group budget. No numerical exclusion is credited to this control.

Trust boundaries are the written unformalized counting/primitive argument,
Python integer execution, and the published exact C++ K optimizer. No
independent reviewer verdict, floating LP optimum or historical priority is
asserted. The global exactly-eight candidates remain10080,15120,20160;
the at-least-eight problem is separate.

Campaign context: [joint resource capacities](../../../number_theory/distinct_covering_joint_capacity/proof.md),
source d1c0f5712486644eb3963d074c81743bfc9e4bec, graph7228, and
[known top phases](../../../number_theory/distinct_covering_fixed_binary_clusters/proof.md),
source7fdc72707e47e4a230ef50b9c8fef55124599f51, graph7633. Their numerical
applications are not premises of the new group theorem. Primary literature:
[Zhang--Zhang](https://arxiv.org/html/2607.19029) and
[HKLT](https://arxiv.org/html/2605.18644). Neither supplies an unrestricted
minimum-eight optimum or a theorem being presented here as new.
