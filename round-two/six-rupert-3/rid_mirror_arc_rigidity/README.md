# RID closed-fit rigidity on two mirror-plane arc families

**six-rupert-3, researcher.** Every closed scale-at-least-one projection
fit with receiving normal in the proper-body orbit of
`(s,0,1)/sqrt(1+s^2)` or `(0,s,1)/sqrt(1+s^2)`, `0<=s<=1/12`, has unit
scale, zero translation, and source frame `B1=±B2g` for a proper body
rotation `g`. All strict passages at those receivers are excluded.
Source normal, proper roll and physical translation start arbitrary.
The standard rhombicosidodecahedron's full Rupert property remains open.
This is a union of arcs, not a spherical cap of radius `1/12`.

Read [PROOF.md](PROOF.md) for the full continuum argument and scope.
The proof uses the published [width filter](../rid_low_area_width_filter/PROOF.md)
to locate every source, matches four actual equatorial originals, locks
one frame row using an unchanged coordinate width, then orders tilts by
exact physical area. [check.py](check.py) checks every new finite
hypothesis in exact ordered `Q(phi)`, including affine endpoint supports
that prove inequalities on the entire parameter interval. It first
replays all three complete prerequisite records with pinned hashes.
[DEPENDENCIES.json](DEPENDENCIES.json) names the immutable source and
committed graph reference. No numerical passage search is a premise.

Python 3.11+ and its standard library suffice. Run from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-rupert-3/rid_mirror_arc_rigidity/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O -B round-two/six-rupert-3/rid_mirror_arc_rigidity/check.py
```

Both outputs must byte-match [expected.json](expected.json). The six
damaged mathematical controls must reject in either mode. The written
proof is author-checked and unformalized; independent review and historical
priority are not asserted. Uniform rescaling, including unit edge,
preserves the theorem. Receiving directions off these arcs remain the
next frontier.
