# Complex-radix unit-distance architecture: finite exact obstruction

For arbitrary complex z, construct the strict physical graph on

    A5(z) = {a0+a1*z+a2*z^2+a3*z^3+a4*z^4 : aj in {0,1,omega}},
    omega=(1+i*sqrt(3))/2.

The family has at most **243 vertices** and includes dilation and digit
coincidences. It is a new architecture following the retired three-wheel
family; no fixed host or record graph is deleted or modified.

Every possible non-four-colourable parameter lies in a reproducibly specified
finite set of at most **15,522,676** complex numbers. The exact gate yields:

- 2,797 pairwise coprime, absolutely irreducible real event curves;
- explicit three-colourings of every single-curve graph;
- 264,800 pair systems covering every injective possible counterexample,
  with a Bezout bound of 15,513,472 points and parameter field degree at most 64;
- an additional complete collision inventory with at most 9,204 roots;
- the necessary bounds **1/2 < |z| <= 2** and, for injective non-four-colourable
  graphs, **at least four simultaneous active event curves**.

This is a quantified obstruction for the whole architecture. The exceptional
set remains unresolved. No five-chromatic graph, full four-colour closure,
or improvement to the 509-vertex record is claimed.

From the repository root, with CPython 3.11.2 and no third-party dependency:

```sh
python3 -B hadwiger_nelson_complex_radix_architecture/verify.py --check-expected
python3 -O -B hadwiger_nelson_complex_radix_architecture/verify.py --check-expected
python3 -B hadwiger_nelson_complex_radix_architecture/controls.py
```

Regenerate the compact certificate in a fresh local directory:

```sh
python3 -B hadwiger_nelson_complex_radix_architecture/produce.py --out /tmp/hn-radix-new
cmp /tmp/hn-radix-new/certificate.json hadwiger_nelson_complex_radix_architecture/certificate.json
```

Generate the larger exact frontier locally when needed; it is not required
for replay and is not committed:

```sh
python3 -B hadwiger_nelson_complex_radix_architecture/export_frontier.py --out /tmp/hn-radix-frontier.json
```

The proof is in [PROOF.md](PROOF.md), the compact evidence in
[certificate.json](certificate.json) and [EXPECTED.json](EXPECTED.json), and
the complementary team interface in [HANDOFF.md](HANDOFF.md). Exact
Q(omega) simple-root tests and a reciprocal Eisenstein argument establish
absolute irreducibility without a CAS factorization premise. An independent
binomial expansion checks every distance polynomial. No solver verdict,
floating predicate, or external reviewer acceptance is used.
