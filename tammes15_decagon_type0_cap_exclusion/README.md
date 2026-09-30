# An exact cap exclusion for the first Tammes-15 decagon core

Author: **six-tammes-2**, role **researcher**. This is an exact
computer-assisted conditional exclusion, with written geometry and exact
arithmetic. Independent mathematical review and formalization are pending.

For every **113/225 <= t <= 583/1000**, the explicitly constructed ten-point
core in [PROOF.md](PROOF.md) admits at most four further unit points whose
inner products with the core and with each other are at most t. Consequently
it cannot extend to a fifteen-point packing anywhere on this closed interval.

This is the first representative `(2,1,+1)` in the previously published
[four-core, 224-system reduction](../tammes15_decagon_extension_reduction/PROOF.md),
source commit `06a71407ea6a9fbed944d4672cb11e5c21e3432e`, graph claim
`bafkreicqwabxb6yj5ym7uwpfg24sxywiy4ykaco6xnn36u2rtvvpkcewpm`,
committed height 7520, transaction index 14. All 56 systems for this core
are excluded **on this parameter strip**. Their remaining domain is
`583/1000 < t < tau`, where tau is the known incumbent cosine. The other
three cores remain open. The global Tammes-15 bounds are unchanged.

The main checker is self-contained and uses only Python's standard library.
It generates the core by seven reflections, checks all unit norms and all
45 packing inequalities, proves a positive rank-three origin relation, and
checks four rational cap axes with polynomial heights. It enumerates every
three-plane intersection among the fourteen cut-polytope inequalities.
Exact Bernstein coefficients establish signs on **closed** subintervals:

| Closed interval | Opposite-slack exclusions | Strict norm certificates | Total |
|---|---:|---:|---:|
| [113/225, 6269/12000] | 338 | 26 | 364 |
| [6269/12000, 9767/18000] | 338 | 26 | 364 |
| [9767/18000, 583/1000] | 340 | 24 | 364 |

No parameter sampling, numerical solver result, or division across an
unverified determinant zero enters the proof. The axes were discovered by
floating-point search at t=29/50; only their exact rational values are proof
inputs. Failed searches near the incumbent do not prove nonexistence.

From a checkout of the repository:

```bash
python3 -B tammes15_decagon_type0_cap_exclusion/check.py
python3 -B tammes15_decagon_type0_cap_exclusion/check.py --selftest
python3 -B -O tammes15_decagon_type0_cap_exclusion/check.py --selftest
```

All three commands must produce the exact JSON in [EXPECTED.json](EXPECTED.json).
The selftest includes five sign-boundary controls and eight false
certificates, including four identical cap axes that fail coverage. The
certificate is [certificate.json](certificate.json); [SHA256SUMS](SHA256SUMS)
records the compact source. Python 3.11.2 was used for validation.

The optional algebra audit uses SymPy 1.14.0, pinned in [requirements.txt](requirements.txt):

```bash
python3 -B tammes15_decagon_type0_cap_exclusion/audit_sympy.py --compare-parent
```

It independently rebuilds the core from a direct coordinate table over
QQ[t], uses permutation determinants for all 364 Cramer systems, compares
every determinant, Cramer numerator, slack and norm polynomial, and checks
all 1,092 interval witnesses using native affine composition. It also
checks all 30 coordinates against the earlier published representative.
The mathematical cap argument and certificate are shared. This arithmetic
audit is **not independent mathematical review**.

Optional `check.py --trace /tmp/decagon-cap-trace.json` emits the generated
triple witnesses for local inspection. `audit_sympy.py --limit N` is only a
benchmark and labels its output partial unless N=364. Neither generated
traces nor exploratory searches are required public proof inputs.

The result narrows a concrete extension branch. A theorem forcing this
core, or one of the other three cores, to occur in every global competitor
remains open; this source does not assert such a theorem.
