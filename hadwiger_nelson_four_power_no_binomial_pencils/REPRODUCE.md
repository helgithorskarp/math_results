# Reproduce the intrinsic class and physical classification

The finite classification alone uses CPython 3.11.2 standard-library arithmetic:

```sh
python3 -O -B hadwiger_nelson_four_power_no_binomial_pencils/classification.py
```

It independently enumerates9,720 projective-column matrices,180 per row space, giving all 54 pencils and 110,592 lifts. The main interface instead uses unique rank-two RREF matrices among all 357 row spaces. Their exact pencil sets must agree.

The full algebraic and physical proof uses SymPy 1.14.0 and python-flint 0.8.0. Run from the math_results repository root:

```sh
python3 -m venv /tmp/hn-four-power-cas
/tmp/hn-four-power-cas/bin/pip install sympy==1.14.0 python-flint==0.8.0
/tmp/hn-four-power-cas/bin/python -B hadwiger_nelson_four_power_no_binomial_pencils/produce.py --jobs 4 --out /tmp/hn-four-power-roots.json
/tmp/hn-four-power-cas/bin/python -B hadwiger_nelson_four_power_no_binomial_pencils/verify.py --jobs 4 --certificate /tmp/hn-four-power-roots.json --check-expected
/tmp/hn-four-power-cas/bin/python -O -B hadwiger_nelson_four_power_no_binomial_pencils/controls.py --certificate /tmp/hn-four-power-roots.json
/tmp/hn-four-power-cas/bin/python -O -B hadwiger_nelson_four_power_no_binomial_pencils/boundaries.py --certificate /tmp/hn-four-power-roots.json
```

The producer's default method is lexicographic Groebner elimination. The verifier independently uses resultants and quotient-field Euclidean gcds, then directly constructs every physical point and unit edge. Both fail on unsupported algebraic fibers; none occurs here. The final colour witnesses use no SAT solver. The code imports the accepted h4105 norm architecture and exact C0 field/coordinate helpers from sibling packages in this repository; those source dependencies must be present.

The locally generated root table is2,184,292 bytes, SHA256
`f7dc43ce1f68eee6715a48527367d219b3cc592a7c82029b94831234a6587f50`.
It is not committed. No private data or large external input is needed for the intrinsic theorem. EXPECTED.json records the full result, physical graph and active-curve histograms, and transcript hashes.

To generate the same table with the second elimination route:

```sh
/tmp/hn-four-power-cas/bin/python -B hadwiger_nelson_four_power_no_binomial_pencils/produce.py --method resultant --jobs 2 --out /tmp/hn-four-power-roots-resultant.json
cmp /tmp/hn-four-power-roots.json /tmp/hn-four-power-roots-resultant.json
```

Both complete tables must be byte-identical. Expected totals:864 pairs,907 irreducible component records,885 real components,2,988 distinct physical parameters and no full-pencil concurrence. Every complete physical graph is exactly three-chromatic. The optimized controls retain129-point and 27-point collision graphs, exhaust all 81 normalized positional weight choices at the first graph, and reject six corruptions. The boundary audit identifies all twelve roots of z^12=1 as the envelope's unit-circle parameters.

To check historical residual membership, regenerate h4195 following `hadwiger_nelson_radix_pair_exclusion_propagation/REPRODUCE.md`, then append

```sh
--residual /tmp/hn-propagation-residual.json
```

to producer or verifier. They check canonical SHA256
`42132ed90f7696d9cf7c17e7b47588ca717bb71b633141e29412a1b55b55e97d`
and every selected index/signature. All full runs in this pass included that check. The intrinsic54-pencil classification does not depend on the historical residual.

Four workers were used for Groebner generation and the full direct check, two for resultant regeneration; the command-line limit is eight. Timings are in VALIDATION.json. No numerical tolerance, solver UNSAT verdict, parameter chamber or conditional global allowance is used. External independent-author review remains outstanding.
