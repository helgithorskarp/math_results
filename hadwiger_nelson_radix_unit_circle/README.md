# Every unit-circle complex-radix graph is exactly three-chromatic

For **every** complex z with |z|=1, the full strict Euclidean unit graph on
A5(z)=T+zT+z²T+z³T+z⁴T, T={0,1,(1+i√3)/2}, has chromatic number **3**.
This closes the complete unit-circle branch of the existing 243-point
architecture. Non-unit-modulus injective parameters remain open; no record
improvement is claimed.

The [proof](PROOF.md) reduces all possible additional unit edges to 1,272 monic
Eisenstein event polynomials. Checked product identities cover their roots by
820 factors. The [h4119 residue theorem](../hadwiger_nelson_radix_collision_residues/PROOF.md)
handles 124 factors of degree≤4 and all physical collisions. Three explicit
linear colour words handle the remaining 696 factors, certified by 381,888
modular coprimality checks. A separate exact fixture has 243 distinct points
and 1,221 strict unit edges, with algebraically specified coordinates.

From the repository root, using CPython 3.11.2 and its standard library:

```sh
python3 -B hadwiger_nelson_radix_unit_circle/verify.py --check-expected
python3 -O -B hadwiger_nelson_radix_unit_circle/verify.py --check-expected
python3 -B hadwiger_nelson_radix_unit_circle/controls.py
```

To regenerate the 62,007-byte certificate from scratch, additionally install
SymPy==1.14.0 in a disposable environment, then run:

```sh
python3 -B hadwiger_nelson_radix_unit_circle/produce.py --out /tmp/radix-circle-certificate.json
python3 -B hadwiger_nelson_radix_unit_circle/verify.py --certificate /tmp/radix-circle-certificate.json --check-expected
```

Regeneration took about four minutes on the research host and was byte-identical.
No SAT package is needed. The certificate SHA256 is
`c76efb83fab51605eb7e59c7fa9114b3fbe1bc643500c8eb047f47f1d5bc8bb7`.
[EXPECTED.json](EXPECTED.json) records the exact counts; [VALIDATION.json](VALIDATION.json)
records replays and corruption controls. The final proof does not trust CAS
irreducibility labels: it checks all product identities and all needed edge
exclusions separately. See [HANDOFF.md](HANDOFF.md) for HN3's precise interface.

Status: author-checked computer-assisted theorem, with h4119 as an explicit
dependency. Independent acceptance of h4105 at h4123 does not constitute an
independent verdict on this result.

The downstream [frontier effect](FRONTIER_EFFECT.json) removes 342 global
pair-orbit systems explicitly containing the circle. This leaves 131,788 global
representatives and allowance 7,780,224. Regenerate the input exports using
`hadwiger_nelson_complex_radix_architecture/export_frontier.py` and
`hadwiger_nelson_complex_radix_d3_quotient/export_quotient.py`, then run
`frontier_effect.py --frontier PATH --quotient PATH --four-interface hadwiger_nelson_complex_radix_four_curve_gate/exact_four_interface.json --check-expected`.
The core unit-circle theorem does not depend on those large local exports.

HN3's late h4135 exact-four-active classification is also consumed. The circle
closure excludes its 26 torus-compatible systems from the exactly-four branch
and leaves **2,528** global
systems for any exactly-four-active counterexample, with allowance 155,648.
The other 129,260 retained systems require at least five active curves for a
counterexample; higher-incidence parameters can also occur on the 2,528 systems.

Of those 26 torus-compatible systems, 22 explicitly contain the circle and are
removed as whole systems. The other 4 remain in the full search but require at
least five active curves for a counterexample.
