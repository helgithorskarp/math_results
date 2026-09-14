# Four 127-point triangular patches are four-colourable

Let

```text
P36 = {a+b*omega : a^2+a*b+b^2 <= 36},
omega = (1+i*sqrt(3))/2.
```

For **every four rotations** of `P36` about their common origin, the strict
plane unit-distance graph on their physical union is four-colourable. Equal
points are merged and all unit pairs are included. The patch has 127 points,
so every member has at most 505 physical vertices.

This closes the full continuum of the maximal radial four-patch architecture
that generically fits below the 509-vertex working record. It is a
restricted-family exclusion, not a global vertex lower bound, and produces no
five-chromatic graph.

The proof uses a four-colour residue ansatz with two independent parity
systems. An exact event reduction shows that any obstruction would contain a
triangle or four-cycle of contact phases. The exhaustive physical census has:

- 528 primitive pair-contact lines and 594 exact event phases;
- 99 phase classes after quotienting the six patch symmetries;
- 186 normalized active triangles;
- 8,100 normalized four-cycles, including 324 fully active six-interface
  placements; and
- explicit proper physical four-colourings after all coincidences and strict
  edges are reconstructed.

See [PROOF.md](PROOF.md) for the mathematical reduction, completeness
argument, exact colouring, and scope.

## Reproduce

From the repository root, using Python 3.11 or later and only its standard
library:

```sh
python3 -B hadwiger_nelson_four_triangular_patches/verify.py --check-expected
python3 -B hadwiger_nelson_four_triangular_patches/controls.py
```

The verifier uses exact integers, rational numbers and sparse squarefree
radicals. It does not use floating point, a SAT solver, an abstract source
graph, or external data.
