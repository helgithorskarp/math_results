# Exact reflection-axis closure for the five-digit radix architecture

Every physical graph

`A5(z) = T + zT + z²T + z³T + z⁴T`, `T={0,1,ω}`, `ω=(1+i√3)/2`,

on a D3 reflection axis is **exactly three-chromatic**. In coordinates
`z=x+i√3 y`, these axes are `y=0`, `y=x`, and `y=−x`.

The real-axis classification checks 1,433 norm polynomials and 1,198 monic
factor blocks. The accepted h4119 theorem closes 192 blocks of degree at most
four. Four explicit colour words three-colour the full event graphs of all
1,006 higher blocks. The only higher-degree blocks with at least five active
curves have six active curves each. Their two real physical graphs both have
243 vertices, 261 strict unit edges, and chromatic number three; exact
coordinates, edges, colourings and a compact independent checker are included.

This physical closure implies that D3 acts freely on every possible
non-four-colourable parameter. Pair-stabilizer accounting reduces the complete
frontier's conservative orbit allowance from **7,754,528 to 3,846,704**, also
using the sharper bidegree intersection bound in the new h4165 reviewer report.
The accounting separates the imported bidegree improvement (3,877,264), the
old rotational fixed-point exclusion (88), and the new reflection contribution
(30,472). All **131,356 pair systems remain**. The bound is conditional on the
imported h4117 complete quotient and h4105 curve irreducibility.
It is not a count of distinct roots. No five-chromatic candidate or record
improvement is established.

## Reproduction

Run from the repository root with CPython 3.11.2 or later. Verification needs
only the standard library and the checked predecessor source in this repository:

```sh
python3 -B hadwiger_nelson_radix_reflection_axes/verify.py
python3 -O -B hadwiger_nelson_radix_reflection_axes/verify.py
python3 -B hadwiger_nelson_radix_reflection_axes/physical.py
python3 -O -B hadwiger_nelson_radix_reflection_axes/controls.py
```

Expected results are in `EXPECTED.json`, `PHYSICAL_EXPECTED.json` and
`VALIDATION.json`. The first full checker performs 717,003 modular polynomial
coprimality checks and can take several minutes. Checks remain active under
`python3 -O`.

Optional fresh generation uses python-flint 0.8.0 and SymPy 1.14.0. Output
paths must not exist:

```sh
python3 -B hadwiger_nelson_radix_reflection_axes/produce.py --out /tmp/hn-axis-certificate.json
python3 -B hadwiger_nelson_radix_reflection_axes/physical.py --produce /tmp/hn-axis-physical.json
cmp /tmp/hn-axis-certificate.json hadwiger_nelson_radix_reflection_axes/certificate.json
cmp /tmp/hn-axis-physical.json hadwiger_nelson_radix_reflection_axes/physical.json
```

The whole-frontier accounting uses the regenerated h4167 retained-pair list;
see [HANDOFF.md](HANDOFF.md) for its exact generation commands and digest.
The mathematical proof and trust boundary are in [PROOF.md](PROOF.md) and
[DEPENDENCIES.md](DEPENDENCIES.md). These are author-side independent code
checks, pending reviewer-1's independent verdict on this new result.
