# A uniform 7/50 bound on the Gaussian majorisation defect

For every bounded probability law mu in R3, every 1-Lipschitz map T, every
Gaussian variance s>0, and every threshold a>=0, the author proof gives

    integral (mu*gamma_s-a)_+
      - integral ((T#mu)*gamma_s-a)_+ <= 7/50.

Consequently the unrestricted defect D and every compact R3--R8 frontier
maximum D_k and B_k are at most **7/50**. Every associated beta coefficient
is at least -7/50, simultaneously over all configurations and degrees.
The same error bounds all concentration-profile comparisons.

This is a rigorous bounded conclusion for the unrestricted problem.
The conjecture requires D=0 and remains open. Independent correctness and
historical priority review are pending. No new exact positive class,
counterexample, optimal constant, or Kneser--Poulsen consequence is claimed.

The [proof](PROOF.md) combines the previously established Gamma(3/2)
comparison with the global scalar envelope

    -7/50 <= (1-exp(-t))_+ - (57/50) F_(3/2)(t+17/50) <= 0.

One derivative sign change reduces the entire real line to two endpoints
and one isolated maximum. Rational Taylor inequalities certify those
obligations. No configuration grid, Gaussian quadrature, large moment sum,
or omitted search corpus is used.

## Replay

Only the Python standard library is required; CPython 3.11.2 and 3.12.14
were checked. Run from this directory:

```sh
python3 verify.py
python3 independent_check.py
python3 check_controls.py
python3 -O verify.py
python3 -O independent_check.py
python3 -O check_controls.py
sha256sum -c SHA256SUMS
```

The primary status is `UNIFORM_GAUSSIAN_DEFECT_BOUND_PASS`; its canonical
record SHA256 is
`091917b9e63599ad5ad19351b61b68ea35c7b34fc4904a0e14af84f1b5bb41d9`.
The separate checker reports `SEPARATE_POLYNOMIAL_ENVELOPE_PASS`, with hash
`6011b4110c860ce0d5ed15c9991e834c06dc1fd6156c037f6ce3691eb3e81492`.
Both outputs are stored in [EXPECTED.json](EXPECTED.json).
The damage controls reject four false certificates. Each replay takes
well under one second on the author's host.

The primary audit uses exact fractions and 80-bit dyadic square-root
brackets. The separate implementation reads no certificate, imports no
primary code, and instead verifies four rational polynomial inequalities
after eliminating square roots. All checks remain enabled with `-O`.
Two author implementations are not independent mathematical acceptance.

## Source and trust

- [PROOF.md](PROOF.md): full-domain reduction, Gamma dependency, universal
  bound, compact-frontier interpretation, and all numerical enclosure rules.
- [CERTIFICATE.json](CERTIFICATE.json): rational shift, multiplier, root
  bracket, precision parameters and enclosure claims.
- [verify.py](verify.py), [independent_check.py](independent_check.py), and
  [check_controls.py](check_controls.py): compact exact replays and rejection
  controls; no external packages or network access needed.
- [SOURCES.md](SOURCES.md): attributed prior results, team dependencies and
  limits of the new conclusion.

The written analytic reduction, Aishwarya--Li's continuous-contraction
theorem, and Python's integer/fraction implementation are trusted. The
result is not formalized in a proof assistant. Source publication verifies
availability and reproduction, not mathematical acceptance.
