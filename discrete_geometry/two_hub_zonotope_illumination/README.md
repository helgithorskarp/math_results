# Exact illumination for weighted `K_(2,n)` zonotopes

For every `n>=1`, and arbitrary strictly positive edge weights on the
graph with two hubs and `n` common neighbors,

\[
                         I(Z)=I_f(Z)=2^n+2.
\]

The zonotope has dimension `n+1`. The proof constructs an optimal set of
directions, valid for every positive choice of weights, and `2^n+2`
pairwise antipodal vertices giving the matching fractional lower bound.

For unit weights an explicit linear change of coordinates gives

\[
 P_n=\{(x,z): |x_i|\le1,\quad |z|+\sum_i|x_i|\le n\}.
\]

The directions are `(eta,(n-1) product_i eta_i)` for all sign vectors
`eta`, together with the two pure vertical directions. The sign parity
lets the same set enter every nonpolar vertex strictly. Positive edge
rescaling preserves the normal cones; it does not assert affine
equivalence of the weighted bodies.

- [PROOF.md](PROOF.md): complete geometric proof and boundary conventions.
- [SOURCES.md](SOURCES.md): classical inputs, known small cases and
  search-relative novelty limitations.
- [verify.py](verify.py): exact model and independent graph-representation
  checks, using CPython 3.11+ and the standard library only.
- [expected.json](expected.json): compact deterministic results.

From the repository root:

```sh
python3 discrete_geometry/two_hub_zonotope_illumination/verify.py
```

Expected output: JSON with status `VERIFIED`, exactly matching
`expected.json`. Tested with CPython 3.11.2. From this directory:

```sh
sha256sum -c SHA256SUMS
```

The model checks cover all 2,058 vertices for `1<=n<=6`, testing 18,298
active inequalities and 2,925 antipodal pairs. Independently, all 1,364
edge orientations for `1<=n<=5` are tested by topological sorting. The
664 acyclic orientations recover exactly the model vertices. Three
positive rational weight assignments at each order give 18,390 strict
supporting-cut tests and 2,340 antipodal-pair checks on the original
weighted generators. Tangent rays and a construction without parity
alternation fail as expected; invalid weights and `n=0` are rejected.
Checks remain active under Python `-O`.

The universal theorem is the written proof, not a finite census or
set-cover computation. There is no solver, floating-point arithmetic,
random sampling, external dataset or hidden large certificate. Independent
peer review and formalization are not included. Zero edge weights and
arbitrary graphical zonotopes are outside scope; no global priority or
resolution of the general illumination conjecture is claimed.
