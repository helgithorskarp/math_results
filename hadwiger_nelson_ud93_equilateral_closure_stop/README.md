# The maximal capped UD9-3 equilateral closure is four-chromatic

## Result

Start with the displayed rigid nine-point Pegg graph
`{UnitDistance,{9,3}}`.  At every round, take the **complete** strict unit
graph on the current point set and adjoin both equilateral completions of
every unit segment.  Equal points are merged before the next round and every
physical unit pair is included.

The exact censuses are:

| round | distinct points | complete unit edges |
|---:|---:|---:|
| 0 | 9 | 15 |
| 1 | 24 | 45 |
| 2 | 50 | 108 |
| 3 | 91 | 209 |
| 4 | 140 | 333 |
| 5 | 196 | 486 |
| 6 | 267 | 677 |
| 7 | 346 | 891 |
| **8** | **432** | **1,134** |
| 9 | 533 | 1,415 |

Round 8 is the last complete stage below the 509-point record boundary.  Its
chromatic number is exactly four.  The lower bound comes from its embedded
nine-point source, whose three-colour impossibility is exhaustively checked;
the upper bound is a literal 432-character colour word checked against every
one of the 1,134 exact unit edges.  Round 9 has 533 distinct points, so the
next complete stage is over the 508-point campaign cap.

This closes this one monolithic architecture.  It is not a five-chromatic
graph, a record candidate, or an exclusion of selected-edge closures, partial
ninth rounds, different source realizations, deletions, hosts, or arbitrary
plane unit-distance graphs.

## Exact model

Write `rho=exp(pi*i/3)`, so `rho^2-rho+1=0` and

```text
|a+b*rho|^2 = a^2+a*b+b^2.
```

The source is defined by three generators `1,z,w`.  In the real basis
`1,rho`, put `z=(x,y)` and `w=(u,v)`.  The four rational quadratic equations
in [`verify.py`](verify.py) assert the five source direction classes have
unit norm.  [`certificate.json`](certificate.json) supplies a rational
midpoint, a rational approximate inverse Jacobian, and radius `10^-35`.
Exact contraction inequalities prove there is one and only one root in that
box.

Every closure point is regenerated as an affine expression in `1,z,w` with
coefficients in `Q(rho)`.  All 1,134 round-8 edges and all 1,415 round-9 edges
are rotations of one of five exact source directions.  Rational interval
bounds around the isolated root check all 234,874 point pairs in the two
rounds, prove every displayed address distinct, and exclude every undeclared
unit pair.  The squared separation and nonedge unit-gap lower bounds both
exceed the conservative thresholds recorded in [`EXPECTED.json`](EXPECTED.json).

## Reproduction

The proof checker uses Python's standard library only:

```sh
python3 -B hadwiger_nelson_ud93_equilateral_closure_stop/verify.py
python3 -O -B hadwiger_nelson_ud93_equilateral_closure_stop/verify.py
python3 -B hadwiger_nelson_ud93_equilateral_closure_stop/controls.py
```

To regenerate the untrusted root and colour certificate, use Python 3.11 and
the versions in [`requirements-producer.txt`](requirements-producer.txt):

```sh
python3 -m venv /tmp/ud93-closure-venv
/tmp/ud93-closure-venv/bin/pip install -r \
  hadwiger_nelson_ud93_equilateral_closure_stop/requirements-producer.txt
/tmp/ud93-closure-venv/bin/python -B \
  hadwiger_nelson_ud93_equilateral_closure_stop/build_certificate.py \
  /tmp/certificate.json
sha256sum /tmp/certificate.json \
  hadwiger_nelson_ud93_equilateral_closure_stop/certificate.json
```

The regenerated certificate must be byte-identical.  The producer's
CaDiCaL-backed positive search is not trusted by the proof: the standard-
library verifier checks the supplied word directly and proves the geometric
claims from exact rational arithmetic.

## Context

The source parametrization was identified in Parcly Taxel's Shibuya project
at commit `218097c9971db2b60ab94a0b8dae20d76741cc43`; this package gives a
self-contained exact definition and does not import Shibuya during proof or
production.  The unrestricted comparison remains Jaan Parts's 509-point,
2,442-edge strict construction in [*Graph minimization, focusing on the
example of 5-chromatic unit-distance graphs in the plane*](https://arxiv.org/abs/2010.12665).

The stable reader is the [`main`-branch directory](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_ud93_equilateral_closure_stop).
The verified publication commit is recorded separately in
[`PROVENANCE.md`](PROVENANCE.md).
