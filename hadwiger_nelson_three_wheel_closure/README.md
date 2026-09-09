# Every sum of three rotated unit wheels is four-colourable

Let `omega=(1+i sqrt(3))/2` and

```text
W={0,1,omega,omega-1,-1,-omega,1-omega}.
S(u,v)=W+uW+vW,  |u|=|v|=1.
```

**Exact computer-assisted theorem.** The strict physical unit-distance graph
of **every** S(u,v) is four-colourable, identifying all coincident labels and
including every unit edge. The bound is sharp, since the family contains
four-chromatic graphs already certified in h4073. Thus this entire architecture,
of order at most 343, cannot improve the five-chromatic planar record.

The new computation closes all **800** representative systems from
[h4071](../hadwiger_nelson_three_wheel_symmetry_frontier/README.md). The
noninjective branch was closed by
[h4073](../hadwiger_nelson_three_wheel_collisions/README.md).
There are **zero remaining injective physical classes**. No five-chromatic
graph or record improvement is claimed.

The [proof](PROOF.md) supplies a finite algebraic cover without real-root
isolation. Exact Sylvester resultants and quotient Euclidean algorithms give
1,447 projection branches, sharing 835 distinct quotient obligations. Of these,
773 have checked colour covers, 4 are empty, 47 have no real first parameter,
10 have no real second parameter, and one splits into two coloured children
(already included in the 773). All quotient dimensions are at most six.

The **56,033-byte** [certificate](certificate.json) stores projection factors,
proof recipes, and 62 four-colour words. Its SHA-256 is
`301ca9a0ee089dfa10ba1b7d29f4e0a23d2e446a2592101dcd60e6cf2a1e6385`.
The checker verifies **277,244** modular unit witnesses. These certify that
every potential monochromatic unit edge is absent at every relevant physical
root; no negative SAT verdict is used.

From the repository root, with CPython 3.11.2 and its standard library:

```bash
python3 -B hadwiger_nelson_three_wheel_closure/verify.py --check-expected
python3 -O -B hadwiger_nelson_three_wheel_closure/verify.py --check-expected
python3 -B hadwiger_nelson_three_wheel_closure/controls.py
```

The verifier imports neither a CAS nor a solver. It checks the pinned source
interfaces and reconstructs the actual squared-distance polynomials from
wheel coordinates. It independently replaces the producer's CAS elimination
and Groebner bases with integer determinants and rational Euclidean relations,
and replaces its multiplication-matrix unit test with an explicit algebraic
norm. Every resulting witness agrees, including under optimized Python.
Controls include degree loss, repeated roots, nonunits, bad reduction primes,
972 matrix/norm comparisons, and nine rejected corruptions. Details are in
[EXPECTED.json](EXPECTED.json), [CONTROLS.json](CONTROLS.json), and
[VALIDATION.json](VALIDATION.json).

Optional byte-for-byte regeneration uses the pinned packages in
`requirements.txt`:

```bash
python3 -B hadwiger_nelson_three_wheel_closure/produce.py --out /tmp/hn-wheel-closure-new
cmp /tmp/hn-wheel-closure-new/certificate.json hadwiger_nelson_three_wheel_closure/certificate.json
```

Use a fresh output directory. The measured producer run took about 48 seconds.
It used 52 SAT calls: 49 supplied positive colour words and 3 were discovery
failures subsequently resolved by stronger exact covers. Those three UNSAT
verdicts are not proof premises and no omitted UNSAT trace is needed.

The external trust boundary is the written geometric and algebraic reduction,
the h4065/h4071/h4073 theorems, CPython arithmetic and decoding, and the source
provenance. Basic univariate arithmetic is shared between implementations;
their elimination and final unit algorithms differ. This is author-checked
computer-assisted mathematics, not formalization or reviewer-1 acceptance.
[HANDOFF.md](HANDOFF.md) closes the parameter/candidate interface for this
architecture. No new architecture or local module audit was started.
