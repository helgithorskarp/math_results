# All collisions in the complex-radix architecture are three-colourable

Every noninjective physical member of
A5(z)=T+zT+z²T+z³T+z⁴T, T={0,1,(1+i√3)/2}, has chromatic number **exactly 3**.
This closes the complete collision branch left by h4105, whose nonzero roots
were bounded by 9,204. It does not close the injective frontier or improve the
509-vertex record. Consuming HN3's h4117 symmetry quotient, the remaining
necessary frontier has 132,130 pair-orbit representatives and a conservative
allowance of 7,785,424 parameter orbits.

The reusable theorem is stronger: if z satisfies a monic polynomial of degree
at most four over the Eisenstein integers E, the entire strict unit-distance
graph on E[z] admits an additive three-colouring. Paired reduction of a point
and its complex conjugate in characteristic three makes the colouring descend
through all physical coincidences. The proof reduces to 16 finite-field cases;
two exceptional graphs have 81 vertices and explicit linear three-colourings.
See [PROOF.md](PROOF.md) and the concrete [HN3 interface](HANDOFF.md).

From the repository root, using CPython 3.11.2 and only the standard library:

```sh
python3 -B hadwiger_nelson_radix_collision_residues/verify.py --check-expected
python3 -O -B hadwiger_nelson_radix_collision_residues/verify.py --check-expected
python3 -B hadwiger_nelson_radix_collision_residues/controls.py
python3 -B hadwiger_nelson_radix_collision_residues/produce.py --out /tmp/radix-residue-certificate.json
python3 -B hadwiger_nelson_radix_collision_residues/verify.py --certificate /tmp/radix-residue-certificate.json --check-expected
```

Expected: 120 monic polynomial factorizations, 32 irreducibles, 16 residue
case types, 6,480 unordered pair checks, and proper three-colour words on the
405-edge norm graph and 324-edge hyperbola graph. Certificate SHA256:
`7205fb23b0b81ac87c35b2fb29dd11b0f64ae694992b302a90ea8d832dd4601a`.
Normal and optimized checks and regenerated certificate agree. The proof's
algebraic bridge is written mathematics; finite arithmetic is independently
checked. This is author-checked evidence, pending independent review.

The finite residue graphs serve as colouring targets. They are not claimed
physical realizations or five-chromatic candidates. No external input or SAT
solver is required for reproduction. [VALIDATION.json](VALIDATION.json) records
controls and the exploratory solver provenance.
