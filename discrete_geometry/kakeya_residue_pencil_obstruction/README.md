# Residue pencils cannot minimize length-two Kakeya sets

Let `R` be a finite commutative local ring with nonzero principal maximal
ideal `m`, `m^2=0`, and odd residue field of order `q`. Its order is `q^2`.
A Kakeya set contains a full affine line in every unimodular projective
direction. A **residue-pencil witness** chooses one such line in every
direction, with all reduced lines concurrent in the residue plane.

Every set admitting this witness has at least

\[
                  L_q=(q^4+q^3+q-1)/2
\]

points. An explicit competing Kakeya set has

\[
                  U_q=(q^4+q^2)/2
\]

points, so **no cardinality minimizer admits a residue-pencil witness**.
The separation is `(q-1)(q^2+1)/2` points. Neither the lower bound nor
the competitor is claimed optimal in its respective class.

The proof turns each residue-direction group into an auxiliary finite-field
Kakeya problem and assembles disjoint residue fibers. The external input
is Blokhuis--Mazzocca's sharp odd-field theorem. A quadratic-discriminant
construction supplies the comparison. This is a uniform finite geometric
obstruction, with no Euclidean dimension or infinite-ring measure claim.

- [PROOF.md](PROOF.md): complete argument, hypotheses and scope.
- [SOURCES.md](SOURCES.md): primary-source attribution and novelty limits.
- [verify.py](verify.py): exact finite corroboration, standard library only.
- [expected.json](expected.json): deterministic compact evidence.

From the repository root, with CPython 3.11+ (tested 3.11.2):

```sh
python3 discrete_geometry/kakeya_residue_pencil_obstruction/verify.py
python3 -O discrete_geometry/kakeya_residue_pencil_obstruction/verify.py
```

Both print JSON with status `VERIFIED`, matching `expected.json` byte for
byte. From this directory, run `sha256sum -c SHA256SUMS`.

The verifier reconstructs all 640 construction lines in ten rings:
`Z/p^2` and dual numbers over `F_p` for `p=3,5,7,11`, plus dual numbers
over `F_9` and `(Z/9)[i]/(i^2+1)`. It checks every primitive-vector
normalization and compares the actual union with the discriminant formula.
It compares 38,884 residue-direction groups point by point (29,254,564
membership comparisons), exhausting every intercept function over `F_3`
and `F_5`, with deterministic polynomial fixtures over `F_7` and `F_9`.
Finally it checks all 531,441 origin-centered pencil systems in each of
the two rings with residue order three. Their minimum observed size is
56, confirming that the universal lower bound 55 need not be sharp.
These two small censuses are corroboration, not the all-ring proof.

Negative controls distinguish finite slopes from all directions, primitive
from nonprimitive vectors, length two from length three, and odd from even
residue characteristic. There is no solver, floating-point calculation,
random sample, external dataset or hidden large certificate. Independent
peer review and formal verification remain pending. Minimum cardinality
is not the same as inclusion minimality.
