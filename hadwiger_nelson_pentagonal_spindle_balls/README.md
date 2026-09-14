# Pentagonal spindle balls: a direction barrier and two closed record tests

No sub-509 five-chromatic graph is found. This package gives three connected
results for a new pentagonal unit-direction construction:

- An explicit additive four-colouring for graphs whose complete edge
  directions are fifth-root rotations of unit elements of
  `Z[1/3,rho,eta]`, where `rho=exp(i*pi/3)` and `eta=(5+i*sqrt11)/6`.
- An exact **1801-point, 7170-edge** four-chromatic host containing all
  **252 named 451-point** five-orbit Cayley balls. Every subgraph of this
  host, including every support of at most 508 points, is four-colourable.
- **Sixteen 451-point, 1740-edge dyadic variants** using
  `w=(7+i*sqrt15)/8` also have positive four-colourings. Their labelled edge
  graphs are identical under the natural pair-sum labels.

All sixteen proper four-colour equality patterns of the aligned seven-point
Moser spindle extend to the first host and to every dyadic variant. Thus
neither tested cohort supplies a stronger relation on that chosen interface.
Arbitrary terminal sets, unions of the dyadic variants, and the complete
unit-distance graph of the coordinate field are not classified.

Each candidate is a genuine exact plane support. Five hexagonal orbits give
30 distinct unit directions; their two-vector sums give exactly **451 points**,
58 below the incumbent's order. Unit distances are reconstructed from the
actual coordinates, including accidental contacts. [PROOF.md](PROOF.md)
states the precise families, the additive colouring, and why the dyadic test
escapes its hypotheses but still fails the construction and interface tests.

## Reproduce

Use Python 3.11+, NumPy and a C++17 compiler; the verified versions were
CPython 3.11.2, NumPy 2.4.6 and g++ 12.2.0. From this directory:

```sh
python3 -m venv /tmp/hn-pentagonal-venv
/tmp/hn-pentagonal-venv/bin/pip install -r requirements.txt
/tmp/hn-pentagonal-venv/bin/python -O verify.py --work /tmp/hn-pentagonal-check --sanitize
sha256sum -c SHA256SUMS
```

The verifier needs no SAT solver. It independently constructs the points
in a different algebraic basis and checks **all 3,244,500 point pairs**
without a modular filter. Every one of the 35,010 exact edge entries agrees
with the producer's reconstruction. The 40,357-byte certificate contains
two sets of sixteen positive words. Its SHA-256 is

```text
667cd21e6e97bed25540469c4b117c2d628bb11614cf7c801cfc4e58cf50acde
```

Optional regeneration of the positive certificate:

```sh
/tmp/hn-pentagonal-venv/bin/pip install -r requirements-discovery.txt
/tmp/hn-pentagonal-venv/bin/python make_certificate.py --work /tmp/hn-pentagonal-words --output /tmp/hn-pentagonal-words/certificate.json
cmp certificate.json /tmp/hn-pentagonal-words/certificate.json
```

All geometry follows from displayed equations; no external graph file is
needed. Generated point/edge inventories, executables and scratch outputs
stay outside the repository. See `expected.json` and `VALIDATION.json` for
actual results and versions. Verification is author-side, not independent
peer review or proof-assistant formalization.

## Context and stop

The record comparison remains [Parts' 509 vertices and 2442 edges](https://arxiv.org/abs/2010.12665),
also stated in [Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4).
These primary sources and current team directions were refreshed on 2026-09-14.
Discovery Net's committed index remained stale at 4363; current durable
repository sources were used alongside it.

The earlier [integral CM obstruction](../hadwiger_nelson_cm_integral_colouring/README.md)
does not cover nonintegral eta, and the
[golden reciprocal-overlay closure](../hadwiger_nelson_golden_reciprocal_closure/README.md)
uses a different 16-point source and scaling rule. The present direction
colouring uses classical residue methods, without a priority claim for those
methods. This lane also avoids the team's A159, triple-Moser, affine-frame
and central-circle-belt constructions.

The declared tests are complete and retired. No larger orbit allowance or
arbitrary eta-power sweep is implied by this result.
