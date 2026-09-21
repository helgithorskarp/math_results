# Cyclic index four: the first signed local Ehrhart formula

This package determines the first residue-dependent Ehrhart coefficient when
the minimum nonintegral faces have cyclic active cokernel of order four.  It
is the first higher-`2`-power case beyond the accepted positive index-two
criterion, and it explains locally why determinant-four half-integral
polytopes can reinforce, cancel, or reverse the parity jump.

Let `P` be half-integral.  Among faces whose affine spans miss the lattice,
let `g` be the minimum codimension, `k=d-g`, and `M` the codimension-`g`
faces.  Suppose every `F` in `M` lies in exactly `g` facets and its active
image has cyclic cokernel `Z/4`.  Under any identification carrying the
class of the active right side to `2`, let

    q_(F,j) in {1,2,3}

be the class of the `j`th slack coordinate.  Put `r_F=#(q=1)`,
`s_F=#(q=3)`, and `h_F=#(q=2)`.  The local even-minus-odd jump is

    Delta_F = Re product_j (1-i^(q_(F,j)))^(-1)
            = 2^(-g) Re((1+i)^r_F (1-i)^s_F)
            = 2^(-h_F-(r_F+s_F)/2)
                cos((r_F-s_F)pi/4).

The last expression is always rational.  In
`L_P(n)=A(n)+(-1)^n B(n)`, the first coefficient that can vary satisfies

    [n^k]B = (1/2) sum_(F in M) vol_k(F) Delta_F.

Thus the coefficient is nonzero exactly when the displayed signed volume sum
is nonzero.  A single local jump vanishes precisely when
`r_F-s_F=2 mod 4`; unlike index two, positivity is false.

The proof and invariant normalizations are in [PROOF.md](PROOF.md).  A
canonical simplex for every profile realizes the formula.  In particular,

- `(1,3)` has positive jump `1/2`;
- `(1,1)` has jump zero and gives the McAllister--Woods collapsing triangle;
- `(1,1,1)` has negative jump `-1/4`.

Products with unit cubes preserve these three signs in every larger face
dimension.  This is a structural phase classification, not a larger table of
isolated period-collapse examples.

## Reproduce

Use Python 3.11 or newer, standard library only, from this directory:

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

Both Python commands reproduce [expected.json](expected.json) exactly and
write no files.  The checker constructs a lattice basis and every deleted-row
integral witness for all 1,086 ordered profiles of lengths one through six.
It then verifies 3,258 simplex-product families by exact parity interpolation
and unused holdouts, with literal slack enumeration for six fixtures.  These
finite checks support the algebra and constructions; the universal theorem
rests on the proof and the cited Berline--Vergne formula.

## Scope

The active quotient must be cyclic of order four, the polytope must be
half-integral, and local simplicity is required at the minimum nonintegral
faces.  The theorem gives the first varying coefficient; if its signed sum
vanishes, lower coefficients may still vary unless the construction has only
one bad vertex.  General finite cokernels, nonsimple faces, and a complete
period-collapse classification are outside scope.  Novelty is bounded and
search-relative; see [SOURCES.md](SOURCES.md).
