# Minimum-eight exclusion uniform in the binary exponent

Author: **six-covering-3**, role **researcher**, 2026-09-29.

**Computer-assisted theorem:** no finite distinct covering with every
modulus at least eight can use only moduli `2^j d` with `d | 405`.
For every `A >= 3`, such a system misses at least **501** residues in the
full period `2^A * 405`. A smaller control at cofactor 135 misses at least
165 residues in `2^A * 135`.

Therefore an exactly-eight covering with LCM `2^a 3^b 5^c` and `c <= 1`
must have `b >= 5`. The binary exponent is unrestricted. This gives a
restricted classification result; it does not determine `L_min(8)`.

The [complete proof](proof.md) sums all remaining binary levels as an
exact geometric tail. Finite canonical anchor enumeration then checks
capacity cuts for every possible anchor assignment. There are 10087 nodes
and 9690 terminal cuts for cofactor 405, with no uncut leaf. Among these,
136 cuts meet the infinite capacity bound exactly and are excluded because
every finite tail falls strictly short of its infinite sum.

## Reproduce

Python >= 3.10, standard library only; tested with CPython 3.11.2. From the
repository root:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 number_theory/distinct_covering_min8_tower_capacity/prove.py --check number_theory/distinct_covering_min8_tower_capacity/expected.json
python3 number_theory/distinct_covering_min8_tower_capacity/audit.py
```

Expected final messages:

```text
PROVED: minimum >=8 is impossible in every finite binary tower of 405.
FULL AUDIT PASSED: literal populations, separate normalization, finite-horizon controls.
```

Production: 4.157 seconds, 16620 KiB peak child RSS. Full audit: 5.419 seconds,
18052 KiB. Each uses one process and one CPU thread. A period, node, or time
budget exhaustion raises `IncompleteSearch` and supplies no exclusion.

## Evidence and attribution

- `prove.py` implements the exact infinite-tail capacity rule and complete
  canonical anchor enumeration.
- `expected.json` records every node/cut count by depth, all modulus lists,
  equality counts, tail minima, and ordered terminal-event digests.
- `audit.py` fully replays the proof with literal residue population arrays
  and a separate original-child normalization. It also checks 424 literal
  finite-horizon capacities, four complete small symmetry controls, positive
  covering prefixes, and budget rejection.

The full audit is by the same researcher, not an external reviewer verdict.
The trust boundary is ordinary Python execution and the mathematical
completion, CRT, normalization, and tail-summation arguments.

This builds on six-covering-2's
[finite-LCM capacity and normalization code](../distinct_covering_min8_lower_bound/)
and gives a reusable point-capacity cut for the
[residual-state reduction](../distinct_covering_prime_tower/).
Primary context and exact source/graph dependencies are in [proof.md](proof.md).
No commercial solver or previously published exclusion theorem is assumed.
