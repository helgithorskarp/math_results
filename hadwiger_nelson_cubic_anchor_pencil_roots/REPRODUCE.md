# Reproduce the algebraic and physical classification

Run from the math_results repository root with CPython 3.11.2, SymPy 1.14.0, and python-flint 0.8.0. The final producer/checker does not require a SAT solver. Up to eight bounded worker processes are supported; four were used for the main checks on the 12-CPU host.

```sh
python3 -m venv /tmp/hn-cubic-cas
/tmp/hn-cubic-cas/bin/pip install sympy==1.14.0 python-flint==0.8.0
/tmp/hn-cubic-cas/bin/python -B hadwiger_nelson_cubic_anchor_pencil_roots/produce.py --jobs 4 --out /tmp/hn-cubic-roots.json
/tmp/hn-cubic-cas/bin/python -B hadwiger_nelson_cubic_anchor_pencil_roots/verify.py --jobs 4 --certificate /tmp/hn-cubic-roots.json --check-expected
/tmp/hn-cubic-cas/bin/python -O -B hadwiger_nelson_cubic_anchor_pencil_roots/controls.py --certificate /tmp/hn-cubic-roots.json
```

The local exact root table is1,742,210 bytes. Its SHA256 is
`7b7267c1f44082a4fdd54f22f0ef096408c937ee1eada024e7b258bdcdf76f2f`.
It is intentionally generated outside the public package rather than committed. No large external download or private input is needed for the named-class theorem. The source dependencies are existing sibling packages in this repository: the h4105 complex-radix architecture and the C0 exact algebra/physical-coordinate helpers.

The producer solves584 pairs by lexicographic Groebner elimination and generates592 canonical exact components. Its physical graph construction uses event-owned edges. The verifier instead recomputes resultants and fiber gcds from the original equations and constructs each physical graph by direct exact coordinates and all-pairs squared norms. It verifies the colouring after the collision quotient. The real-root table is not treated as authoritative input.

Expected: PASS;50 pencils,1,024,000 raw lifts, no full complex-affine concurrence,588 real components and 3,408 distinct real parameters. Every complete physical graph has chromatic number3. The 12 collision parameters, with 101 active events each, are part of the checked result. EXPECTED.json pins the complete result, histograms, and transcript hashes.

To regenerate the table using the second elimination algorithm and optimized Python:

```sh
/tmp/hn-cubic-cas/bin/python -O -B hadwiger_nelson_cubic_anchor_pencil_roots/produce.py --method resultant --jobs 2 --out /tmp/hn-cubic-roots-resultant.json
cmp /tmp/hn-cubic-roots.json /tmp/hn-cubic-roots-resultant.json
```

Both routes must produce the same bytes. The optimized controls retain positive147-point/651-edge and 108-point/432-edge collision graphs and reject six corruptions: a wrong real-root count, a colouring that fails to descend through collisions, an omitted physical edge, an omitted active event, an omitted exceptional algebraic component, and a fabricated full-pencil concurrence.

The default selection is the literal compact PENCILS.json class. To independently check that it is exactly the cubic-anchor class in h4195, regenerate the historical residual using `hadwiger_nelson_radix_pair_exclusion_propagation/REPRODUCE.md`, then add

```sh
--residual /tmp/hn-propagation-residual.json
```

to either producer or verifier command. Both check canonical SHA256
`42132ed90f7696d9cf7c17e7b47588ca717bb71b633141e29412a1b55b55e97d`
and compare every selected residual index and signature. The generated historical file is not committed here. This pass used that pinned file in all full runs.

No numerical root approximation, solver UNSAT claim, conditional orbit allowance, or parameter chamber is part of the proof. External independent-author review remains outstanding. Validation timings and source context are recorded separately in VALIDATION.json and CONTEXT.json.
