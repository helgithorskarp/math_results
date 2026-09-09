# Complete physical closure of the A5 reflection-pair stratum

Every physical A5(z) member represented by any of the **2,232 post-h4185
surviving pair systems with a reflection in its stabilizer** is exactly
three-chromatic. The closure includes every additional unit edge and every
higher incidence on those systems. It is a complete decision of this named
stratum, not a restriction to parameters on reflection axes.

An exact reduction gives 2,291 algebraic chart records. All have verified
three-colour words. Two explicit fixtures from a nonintegral quartic chart,
outside the previously closed anchor, radial-circle and reflection-axis loci,
each have **243 distinct points, 378 unit edges, five active curves, and
chromatic number three**. [PROOF.md](PROOF.md) gives the complete argument.

The result removes **2,232 global systems** and allowance **30,220**, leaving
**128,700 systems / 3,813,472 conservative allowance**. Its 6,696
symmetry-expanded pair exclusions are returned in the [HN3 handoff](HANDOFF.md).
The global accounting retains the h4177/h4117/h4175 trust boundary. The new
result is author-checked; independent reviewer-1 assessment is pending.
No <=508 five-chromatic graph has been established, and the full A5
architecture remains open.

From the repository root, using CPython 3.11.2 and python-flint 0.8.0:

```sh
python3 -B hadwiger_nelson_radix_reflection_pair_stratum/verify.py --check-expected
python3 -B hadwiger_nelson_radix_reflection_pair_stratum/physical.py --check-expected
python3 -O -B hadwiger_nelson_radix_reflection_pair_stratum/controls.py
```

The core verifier takes about six minutes in the tested environment. It
computes integer Sylvester determinants, checks complete factor products and
quotient-ring Euclidean divisions, then uses **pure-Python modular arithmetic**
and the actual 29,403 label pairs to exclude every colour-bad unit edge.
The physical checker uses only the standard library, reconstructs all points
in Cartesian coordinates, and checks all 58,806 pair decisions, reusing 2,801
exact displacement classes. It does not assume the quadratic real-coordinate
extension is irreducible.

The compact main certificate is 47,105 bytes, SHA-256
`b561346fe17e07bf1b362611414d7b00c7bb3aae1f4ede096800f2cbf9a21953`.
The shared-coordinate physical fixture is 16,641 bytes, SHA-256
`8322a08a8b6bfda7fc0c0a4c63fcda382f28a4a8121a13c28b49cfbf4745f68b`.
Verbose eliminants, algebraic charts and the full frontier table are regenerated
locally and are not committed. Chart counts are not counts of physical roots.

Fresh production uses SymPy 1.14.0 and python-flint 0.8.0. After regenerating
the h4185 frontier as described in the handoff:

```sh
python3 -B hadwiger_nelson_radix_reflection_pair_stratum/produce.py \
  --frontier /tmp/hn-h4185-frontier.json --out /tmp/hn-reflection-certificate.json
cmp /tmp/hn-reflection-certificate.json hadwiger_nelson_radix_reflection_pair_stratum/certificate.json
python3 -B hadwiger_nelson_radix_reflection_pair_stratum/physical_generate.py \
  --out /tmp/hn-reflection-physical.json
cmp /tmp/hn-reflection-physical.json hadwiger_nelson_radix_reflection_pair_stratum/physical.json
```

Output paths must not exist. The producer uses bivariate Groebner bases and
direct coefficient norms; the verifier uses Sylvester/Bareiss elimination,
fibre Euclid, and bivariate curve substitution. Every source pair's complete
chart set agrees between them, and fresh certificates are byte-identical.
Expected results and checks are in [EXPECTED.json](EXPECTED.json),
[PHYSICAL_EXPECTED.json](PHYSICAL_EXPECTED.json), and [VALIDATION.json](VALIDATION.json).
