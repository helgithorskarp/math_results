# A five-colour projection obstruction for shared Schur fibres

A particular six-colour construction on the nonzero residues modulo `5a`
cannot exceed endpoint **394** if its two special axis classes can be
merged. This follows by explicitly constructing a five-colouring modulo
`2a` and using [Heule's theorem S(5)=160](https://arxiv.org/abs/1711.08076).
The result concerns the family defined below. The unrestricted classical
lower bound for S(6) remains 536; the [July 2026 shifted-template
paper](https://arxiv.org/abs/2607.15034) uses that bound. All sum-free
conditions here include equal summands.

## The specified construction

Let `a` be odd and coprime to 5, and write `A=Z/aZ`. Choose symmetric
partitions, allowing empty classes,

```text
A minus {0} = E0 disjoint-union E1 disjoint-union ... disjoint-union E5,
A = R disjoint-union C2 disjoint-union C3 disjoint-union C4 disjoint-union C5,
0 belongs to R.
```

Symmetric means that each set equals its negative. Colour the nonzero
points of `A x Z/5Z` as follows:

* On the zero fibre, give `(x,0)` colour `i` when `x` belongs to `Ei`.
* On the four nonzero fibres, give every `(x,b)` colour `i` when `x`
  belongs to `Ci`, for `i=2,3,4,5`.
* For `x` in `R`, give `(x,+-1)` colour 0 and `(x,+-2)` colour 1.

The Chinese remainder theorem identifies this with a symmetric colouring
of the nonzero residues modulo `5a`. In particular, a valid construction
would colour the integer interval `[1,5a-1]`.

**Exact validity criterion.** The construction is sum-free if and only if

1. Each `Ei` and each `Ci` is sum-free in `A`.
2. `(E0 union E1)` is disjoint from `R-R`.
3. For `i=2,3,4,5`, `Ei` is disjoint from `Ci-Ci`.

For colours 0 and 1, adding two points with nonzero second coordinates
can return to the same colour only on the zero fibre. Adding a point of
that fibre to a nonzero-fibre point gives the same difference condition.
For an ordinary colour `i>=2`, the possibilities are two zero-fibre
points, two nonzero-fibre points, or one of each. They give exactly the
sum-free and difference conditions above. Symmetry gives `B+B=B-B` for
each of the relevant sets `B`. This proves necessity and sufficiency,
including repeated summands.

## Projection lemma and proof

**Lemma.** Suppose the construction is valid and `E0 union E1` is
sum-free. Then there is a symmetric five-colouring of the nonzero
residues modulo `2a`.

Put `F0=E0 union E1`, and for `j=1,2,3,4` put `Fj=E(j+1)`.
Put `D0=R` and `Dj=C(j+1)` for those same four indices. Partition the
nonzero points of `A x Z/2Z` into the five sets

```text
Bj = (Fj x {0}) union (Dj x {1}),  j=0,1,2,3,4.
```

Every `Fj` is sum-free by hypothesis and the validity criterion. Every
`Fj` is disjoint from `Dj-Dj`: this is condition 2 for `j=0` and
condition 3 for the other indices. Therefore each `Bj` is sum-free:

* two second-coordinate-0 points cannot sum to another such point of `Bj`;
* two second-coordinate-1 points cannot sum into `Fj`, since
  `Dj+Dj=Dj-Dj`;
* a second-coordinate-0 point and a second-coordinate-1 point cannot sum
  into `Dj`, by that same difference exclusion.

The `Bj` partition every nonzero point, and their symmetry is inherited
from the original sets. Since `a` is odd, the Chinese remainder theorem
identifies `A x Z/2Z` with `Z/(2a)Z`. This proves the lemma.

The resulting ordinary five-colouring has endpoint `2a-1`. The established
equality `S(5)=160` gives `2a-1<=160`; integrality and oddness give
`a<=79`. Thus the original shared-fibre construction has endpoint
`5a-1<=394`. No attainment claim is made for 394.

**Consequence for the target `a=109`.** Every valid shared-fibre
six-colouring modulo 545 must have a Schur triple inside `E0 union E1`.
Since each `Ei` is itself sum-free, that triple uses both special axis
colours. In particular both classes must be nonempty. This excludes the
entire subfamily with either special axis colour absent, regardless of
the other axis classes or fibre sets. A five-colour axis whose absent
colour is one of `2,3,4,5` is still allowed by this lemma.

## Compact certificates and checks

`fixtures.json` contains complete zero-based colour words, together with
their symmetric axis and fibre halves:

* `a=47`: a valid six-colouring on `[1,234]`, with mergeable special axis
  classes, and the resulting valid five-colouring on `[1,93]`.
* `a=7`: a valid colouring on `[1,34]` whose special axis classes cannot
  be merged. Its recorded projection has four modular violations, all
  in the merged axis. This checks the need for the extra hypothesis.

These are calibration examples below the known bounds. They were obtained
by bounded SAT search; their verification uses no solver or search code.
The independent standard-library checker reconstructs every listed word,
checks all integer and modular sums including doublings, and checks the
set criterion directly. It also exhausts all `6^3 * 5^3 = 27000`
symmetric assignments on a `Z/7Z` axis. Of these, 3096 give valid original
colourings, and 2664 have mergeable special axis classes. Every one of
the 2664 projections is checked literally. For the other valid inputs,
the projected defects occur precisely within the merged zero fibre.

From this directory, with CPython 3.11 or later and no third-party packages:

```sh
sha256sum -c SHA256SUMS
python3 -B verify.py
```

The program must reproduce `expected.json` exactly as structured data and
report `status: PASS`. A run takes about one second. The all-parameter
lemma is proved above; the small exhaustive audit validates its concrete
implementation. The separate theorem `S(5)=160` is imported from Heule's
work, and its large proof is not part of this artifact.

Primary-source and committed-graph overlap checks were refreshed on
28 September 2026. This note records a restriction on the specified
construction; no historical-priority claim is made for the underlying
two-layer sum-free construction.
