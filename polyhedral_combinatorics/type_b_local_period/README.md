# Local facet structure and Ehrhart period for type-B systems

**Every simple polytope with primitive facet normals `+-e_i` or
`+-e_i+-e_j` and integer facet offsets has full Ehrhart period:** one when
its vertices are integral, two otherwise. The lattice throughout is Z^d.

The stronger theorem needs simplicity only along specific faces. Let P be
bounded and full dimensional, with those primitive normals and integer
offsets. Among its nonempty faces whose affine spans miss Z^d, let g be
the minimum codimension and M the faces of codimension g. Assume each
face in M lies in exactly g facets. Then

    L_P(n) = A(n) + (-1)^n B(n),
    deg B = d-g,
    [n^(d-g)] B = 2^(-g-1) sum_(F in M) vol_(d-g)(F) > 0.

Volume uses a unit lattice cube of volume one, with point volume one.
In particular the reduced denominator of the Ehrhart series is

    (1-t)^(d+1) (1+t)^(d-g+1).

This criterion includes the previously proved all-graph odd-girth theorem:
its relevant shortest-cycle faces satisfy the local facet condition even
when other vertices are nonsimple.

The proof reduces each relevant active system to one unbalanced signed
cycle, including even cycles and two-edge cycles. A named local cone lemma
then identifies the same positive parity jump for all of them. The proof
spells out each quotient-lattice translation and imports Berline--Vergne's
local Euler--Maclaurin theorem. See [PROOF.md](PROOF.md).

The local assumption matters. The polytope

    Q={x>=0, x<=y<=1-x, x<=z<=1-x}

has a fractional vertex in four facets, yet `L_Q(n)=binom(n+3,3)`. It is
unimodularly equivalent to Stanley's classical example, which we credit
rather than claim as a new construction. Our theorem shows that dimension
three is the first possible period-collapse dimension within this precise
facet-normal class. It gives a sufficient condition, not a characterization
of every polytope with full period.

## Reproduce

Use Python 3.11 or newer, standard library only, from this directory:

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

The two Python commands print [expected.json](expected.json) and fail on
any mismatch. They write no files and import no earlier research package.
The manifest authenticates all five substantive files.

The checker uses rational linear algebra to enumerate vertices, identify
actual facets, construct their face intersections, and test affine-lattice
integrality. Literal lattice counting is independent of the signed-cycle
formula. Exact interval lengths and polygon areas give the leading-face
volumes. Interpolation uses the known half-integral degree bound and is
checked at four unused dilation values per full-dimensional fixture.

Expected `PASS` covers:

- 81 explicitly specified planar systems, of which 64 are full dimensional
  and 36 are nonintegral; the other 17 are rejected as lower dimensional.
- Seven named fixtures: ordinary and unequal-capacity triangles, a signed
  even cycle, a digon times a square, its translated/reflected copy, a type-B
  alcove and Stanley's nonsimple negative control.
- 284 unused interpolation values and 213 comparisons with unpruned
  Cartesian-product lattice enumeration.
- 30 invertible signed-cycle matrices of orders two through five, 18,720
  slack-parity cases, 9,020 proper-face integer-affine checks, and five
  malformed-system rejections.

Finite records corroborate the proof and normalizations; they do not prove
the universal theorem by extrapolation or implement the full imported
analytic construction. The checker is not a general-purpose polyhedral
library: boundedness is explicit in its fixture definitions, and its direct
face-volume calculation supports at most two free coordinates.

## Attribution and scope

[SOURCES.md](SOURCES.md) gives primary sources and the graph provenance.
The new scope relative to the searched sources is the local facet criterion
and its consequence for simple polytopes in this root-normal class. The
root-system setting, half-integrality, graph special case, and classical
counterexample are prior. This new proof is unformalized and has not been
independently reviewed; the cited acceptance concerns its graph precursor.

Integer offsets are required after primitive normalization. Allowing
arbitrary rational offsets, changing the lattice, or deleting the local
facet condition is outside the theorem. No gamma-positivity or root-location
classification is asserted.
