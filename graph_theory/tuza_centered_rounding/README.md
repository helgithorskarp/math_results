# Centered packing rounding and an explicit split-graph Tuza cutoff

For an independent set with neighborhood classes `S_i` and arbitrary
positive multiplicities over a finite simple base graph, put
`D=sum_i |S_i|`. Restrict triangle packings to triangles with one vertex in
the independent set. The complete author proof establishes

    nu_c >= nu_c* - 3D/2.

This additive loss has the correct linear order, even for one neighborhood
over a clique; the constant is not claimed sharp. The proof rounds an
optimal basic LP solution and uses Vizing edge coloring.

For split graphs with clique order `k` and `r` active neighborhood types,
if a fractional centered packing saturates every spoke, then

    2nu-tau >= k^2/66-(1/2+12r/11)k+5/12-4r-48r^2/11.

In particular, `k>=80r+40` implies strict Tuza. The condition
`sum_{i:u,v in S_i} m_i/(|S_i|-1)<=1` for each clique pair is an explicit
sufficient certificate of saturation. No restriction on neighborhood
overlaps is imposed. No regularity or asymptotic packing theorem is used.

This is a theorem about **centered** rounding with a conditional Tuza
corollary. It does not bound the unrestricted `nu*-nu` by a linear error
or make the cutoff in the earlier [dense chordal theorem](../tuza_dense_chordal_gap/README.md)
effective for every fixed-type split graph. The
[independent h5735 review](../tuza_centered_rounding_review1/REVIEW.md)
accepts both statements with high confidence. Its literature-attribution
recommendation is addressed in SOURCES.md.

- [Complete proof, hypotheses, sharpness example, and limitation](PROOF.md)
- [Exact LP and packing implementation](rounding.py)
- [Supplementary exact audit and witness generator](audit.py)
- [Expected output](AUDIT.json), [run metadata](RUN.json), [hashes](SHA256SUMS)
- [Prior work and dependencies](SOURCES.md)

## Reproduce

Python 3.11.2 was used; there are no third-party packages or external data.
From this directory:

```sh
python3 audit.py > /tmp/tuza-centered-audit.json
cmp /tmp/tuza-centered-audit.json AUDIT.json
sha256sum -c SHA256SUMS
```

The deterministic audit checks all 33,868 labeled graphs through order
six for valid `Delta+1` edge coloring, plus 60 seeded larger graphs. It
checks 266 split LP instances and 24 arbitrary-base instances using exact
rational primal/dual certificates and an independent active-row rank
check. For 190 small split instances it computes the integer centered
optimum by enumerating matchings at the individual centers. All generated
packings are checked for graph membership and edge disjointness.

There are 31 exact controls for the linear-loss sharpness family,
1,881 exact algebra checks, and five negative controls, including
an optimal nonextreme fractional point which must not be blindly floored.
The large witness has a 280-vertex clique, three crossing neighborhoods of
size 140, and 34 copies of each. The generator verifies 14,646 packed
triangles and a cut cover of size 23,931. Its pairwise neighborhood unions
have sizes 210, 280, 210, so the earlier co-sunflower theorem does not apply.

The audit is supplementary to the universal human proof. The LP solver is
an exact dense simplex implementation for small audits, not an optimized
large-instance solver; Vizing coloring is constructive. Every reported
fractional optimum has a checked rational primal/dual pair. No floating-point output
or exploratory optimization is theorem evidence. The large packing is
regenerated from source and hashed; no bulk triangle list is required.
