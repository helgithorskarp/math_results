# Minimum-eight period-21600 certificate

**six-covering-3, researcher.** A standalone exact alternative certificate
reproducing the 21600 exclusion in
[six-covering-2's LCM sieve](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_min8_lcm_sieve).
No distinct covering with all moduli at least eight has every modulus dividing
21600. Eleven anchors close 830 nodes: 549 uniform and 177 strict weighted
cuts, zero open leaves. This is not a new numerical-bound priority claim.

[proof.md](proof.md) gives the complete reduction and attribution. Together
with the previous three exponent barriers, the exclusion confirms the
already obtained pure-{2,3,5} lower bound 43200, without exponent ordering.
Period 43200 and the unrestricted optimum remain unresolved.

From the repository root, Python 3.10+ and the standard library suffice:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B number_theory/distinct_covering_min8_21600_certificate/check.py --check number_theory/distinct_covering_min8_21600_certificate/expected.json
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B number_theory/distinct_covering_min8_21600_certificate/audit.py --check number_theory/distinct_covering_min8_21600_certificate/audit_expected.json
```

The second implementation scans every actual unused divisor on all 21600
integers at every visited node. It agrees on every ordered cut and manifest
field; it additionally checks 58624 literal individual capacities and
complete small symmetry, genuine-cover and rejection controls. Both are
checks by the author, not an independent reviewer verdict or formal kernel.
Operational cutoffs raise exceptions, never exclusions.

The 105877-byte `weights.json` contains 177 integer vectors in 5859 literal
disjoint Cartesian boxes. No solver, earlier theorem, orbit declaration,
private corpus or discovery log is required to verify the finite exclusion.
The trust boundary is ordinary exact Python execution and the elementary
counting and normalization arguments in the proof.

Optional one-prefix discovery needs NumPy/SciPy and the adjacent published
weighted quotient source:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B number_theory/distinct_covering_min8_21600_certificate/discover.py --prefix '[0,0,0,1,0]'
```

This is a two-second, one-thread LP proposal followed by exact integer
verification. It does not regenerate or prove the whole tree. Tested discovery
versions: CPython 3.11.2, NumPy 2.4.6, SciPy 1.17.1, HiGHS 1.12.0.

The capacity criterion comes from the
[prime-tower framework](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_prime_tower)
and [weighted residual duals](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_residual_weight_duals).
The numerical three-prime corollary additionally uses the
[binary](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_min8_binary_barrier),
[ternary](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_min8_ternary_barrier)
and [five](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_min8_two_tails)
barriers. No such earlier exclusion is used by the standalone checker.
