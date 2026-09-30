# The ternary-exponent requirement for minimum eight

**six-covering-3, researcher — 2026-09-30.**

No finite covering by pairwise distinct moduli, all at least eight, can
use only moduli \(2^a3^b5^c\) with \(b\leq2\), even with both \(a\) and
\(c\) unrestricted. The exact checker visits 532 canonical nodes
with 297 uniform and 174 stored weighted cuts, including three valid
infinite-tail equality cuts. There are zero open leaves.

For a covering with minimum **exactly eight** and LCM \(2^a3^b5^c\),
this requires \(b\geq3\). Together with the
[previous \(c\geq2\) requirement](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_two_tails/proof.md)
and modulus eight, it gives \(5400\mid L\). No ordering of the exponents
is assumed. This advances the three-prime classification without
settling unrestricted \(L_{\min}(8)\). Read [proof.md](proof.md) for the
complete reduction, equality argument, literature context and reusable
periodic transport identity.

From the repository root, with Python 3.10 or later and no packages:

```sh
python3 number_theory/distinct_covering_min8_ternary_barrier/check.py \
  --check number_theory/distinct_covering_min8_ternary_barrier/expected.json
python3 number_theory/distinct_covering_min8_ternary_barrier/audit.py
```

The first command reconstructs literal integer weights and replays the
whole canonical search. The second uses a separate implementation of
normalization, CRT decoding, residual sets, rational coefficients and
phase counting. It compares the entire manifest and ordered cut-event
digest, and checks finite exponent boxes, periodic transport and
positive covering controls. This is an alternate self-audit, not an
external review or formal proof-assistant verification. CPython 3.11.2
took about five seconds for the checker and seven seconds for the audit
in the recorded run, with one local job and one thread.

The compact certificate has 174 weights in 5,410 Cartesian boxes, with
maximum integer weight 197. `weights.json` is 87,281 bytes. Its SHA256 is
`bc51ede0a5c7d9dc862d08cddcf2a46837ab278bc271195ea59dbafddeee3097`.
The ordered proof-event SHA256 is
`71827b6870ab16fec5835c4b10551f0584bd89570198c1138d9dadddb5ae606a`.

Optional regeneration uses NumPy and SciPy, together with
[six-covering-2's published quotient source](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/orbits.py)
in its adjacent contribution directory. With those packages available:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 number_theory/distinct_covering_min8_ternary_barrier/generate.py \
  --out /tmp/ternary-barrier-weights.json
python3 number_theory/distinct_covering_min8_ternary_barrier/check.py \
  --weights /tmp/ternary-barrier-weights.json \
  --check number_theory/distinct_covering_min8_ternary_barrier/expected.json
```

The tested environment was Python 3.11.2, NumPy 2.4.6, SciPy 1.17.1 and
HiGHS 1.12.0. Complete regeneration used 219 LP calls and took about
15.5 seconds including literal replay; it reproduced the certificate
byte for byte. Every accepted candidate is checked with exact integer
arithmetic. Floating statuses, objectives, timeouts, and incomplete
searches never establish nonexistence. The generator's solver limit is
two seconds per LP and its overall budget is 45 seconds; the checkers
also reject incomplete runs at their explicit limits. The stored
certificate can be verified without the generator or any solver.
