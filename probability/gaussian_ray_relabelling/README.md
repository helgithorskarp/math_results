# Full Gaussian majorisation by relabelling twelve rays

For a bounded class of measures on the twelve rays
`r(sigma e_i + tau e_j)`, an explicit relabelling proves **every Gaussian
hinge inequality at every positive variance**. The original contraction has
paired rank six; a second contraction has exactly the same output law and
paired rank five. This applies to nonatomic radial laws and arbitrary mass
at the origin, as well as to the uniform cuboctahedron-to-octahedron example.

The sufficient balance condition is equality of the radial measures on
the `(+,-)` and `(-,-)` rays in each coordinate plane. Positive-sign
branches need not have equal masses or equal radial distributions.

- [Complete proof and exact hypotheses](PROOF.md)
- [Independent exact checks](verify.py)
- [Validation and scope](VALIDATION.md)

Run with Python 3.11 or later, standard library only:

```sh
python3 verify.py --check
python3 -O verify.py --check
sha256sum -c SHA256SUMS
```

Expected status: `RAY_RELABELLING_CHECKS_PASS`.

This is a full-comparison class, not a solution of the general
three-dimensional conjecture. It does not include the four fixed anchors
of the sixteen-label simplex-flap fixture or arbitrary unbalanced weights.
The proof uses the team's earlier paired-rank theorem, which in turn uses
Aishwarya--Li's continuous-contraction theorem. External mathematical
review and formalization remain pending.

The useful search lesson is to examine alternative contracting maps with
the same two endpoint measures before treating the rank of a specified
label map as an obstruction. No historical priority claim is made for
cuboctahedral geometry or relabelling as a general idea.
