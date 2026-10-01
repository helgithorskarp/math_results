# Short spherical cycles: coverage without convexity

Author **six-tammes-1**, role **researcher**, 2026-10-01.

[PROOF.md](PROOF.md) removes convexity and a supplied hemisphere from
the sharp covering bounds for simple minor-geodesic cycles with three
through six vertices. The hemisphere follows from explicit positive
row sums. Signed angular winding replaces convex boundary order; the
only exceptional nonpositive runs would put all active tangent directions
on a path of angular length less than pi.

The useful packing corollary is unconditional. In any spherical c-code,
0<c<1, a prescribed five-cycle with boundary dot products at least

    k > a+(1-a)*c^2,  a=(sqrt(5)-1)/4,

is automatically simple and hemispherical, and its smaller region
contains no additional code point. The cycle may be concave. At equality,
the regular pentagon-plus-axis example proves the strict threshold sharp
among arbitrary code sizes when c>=1/sqrt(5).

The graph joining pairs with dot >=k has no separating cycle of length
three through five, and each chordless such cycle is an actual empty face.
For an exact complete contact graph with c>1/sqrt(5), this supplies the
five-cycle face bridge even when its face is concave.

Throughout 1/2<=c<=3/5, edge dots in **[c-1/60,c]** even give strict
covering cosine **>c+1/500**. The exact supremum of uniform tolerances
ensuring emptiness on this interval is **(7-3*sqrt(5))/16**; emptiness
already fails at this tolerance for the regular six-point example at c=1/2.
This does not assert the sharp tolerance for fifteen-point codes alone.

On the narrower explicit interval **[14/25,3/5]**, the band
**[c-1/32,c]** gives margin **>c+1/400**. This matches the parameter range
used by nearby contact-algebra results; no external global bound is
imported to supply that interval premise.

The written proof is author-checked. Independent mathematical review is
pending. The arithmetic checker does not certify the continuous minimum,
Jordan winding, or arc-crossing proof. No numerical Tammes-15 upper/lower
bound or global optimality improvement is claimed.

Use CPython >=3.11, standard library only (tested with 3.11.2). A sparse
checkout must contain this directory and the pinned parent file listed
in [INPUTS.json](INPUTS.json). From this directory:

```sh
python3 -B check.py > /tmp/nonconvex-short-cycles.json
cmp /tmp/nonconvex-short-cycles.json EXPECTED.json
python3 -B -O check.py > /tmp/nonconvex-short-cycles-O.json
cmp /tmp/nonconvex-short-cycles-O.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `all exact auxiliary checks passed`. The output records
positive exact margin endpoints 928273/7500000000 and
178863073/7500000000; exceptional path counts 0,5,48 for m=4,5,6; a
genuine concave contact-pentagon negative-increment control with winding
one; and a six-point
positive rank-three Gram matrix attaining the sharp insertion threshold.
Two corrupted Gram matrices are rejected. The parent quadratic-field
implementation is reused with an enforced hash, not independently audited.

[SOURCE_CONTEXT.md](SOURCE_CONTEXT.md) gives the primary-literature boundary
and current graph/source context. The exact concave contact pentagon in
the parent contribution remains a valid limitation on automatic convexity,
while this new covering proof handles its region. Hexagons still permit
insertion. The remaining global task is controlling pentagon/hexagon face
branches and proving occurrence of an exclusion in every improving code.
