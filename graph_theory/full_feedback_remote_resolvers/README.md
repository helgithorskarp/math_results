# Remote resolvers for full-feedback directional localization

This directory proves a parameter-uniform sufficient condition for one-cop
full-feedback directional localization on independent substitutions (false-twin
blow-ups).  It also gives an infinite family on which false-twin replication
strictly lowers the parameter:

\[
  \zeta_D^*(C_5)=2,
  \qquad
  \zeta_D^*\!\left(C_5[\overline K_{m_0},\ldots,
  \overline K_{m_4}]\right)=1
  \quad(m_0,\ldots,m_4\ge 2).
\]

The human-readable proof is in [THEOREM.md](THEOREM.md).  The standard-library
checker in [verify.py](verify.py) audits the response formula, the stated
strategy, all connected labelled base graphs through order 5, all 243 vectors
`(m_0,...,m_4) in {2,3,4}^5`, and the cycle-signature classification through
order 50.  These finite checks test the implementation and proof interfaces;
the written argument, not enumeration, establishes the universal theorem.

## Reproduce

Python 3.11 or later is sufficient; there are no third-party dependencies.

```bash
python3 -m unittest -v test_verify.py
python3 verify.py
sha256sum -c SHA256SUMS
```

The second command should print exactly [EXPECTED_OUTPUT.txt](EXPECTED_OUTPUT.txt).

## Scope and trust boundary

The code uses exhaustive exact set computations only.  It is not a solver
certificate and needs no external data.  The literature-status statement and
notation are sourced in [SOURCES.md](SOURCES.md).
