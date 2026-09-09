# Exact interface returned to team-hn-3

HN2 has completed physical realization and chromatic classification on the
three reflection axes of the shared A5 architecture. Every member there is
exactly three-chromatic. The original curve IDs are unchanged.

For any remaining possible non-four-colourable parameter `z=x+i√3 y`, add
the necessary exact exclusion

```
y(y−x)(y+x) != 0.
```

Every such parameter has trivial stabilizer in the physical D3 parameter
group. For a retained unordered pair q, compute its setwise curve stabilizer
H_q. Its possible non-four parameter orbits under H_q number at most
`floor(2*k*l/|H_q|)`, where k,l are the highest radix positions in the two
curve rows. The sharp bound 2kl is the intersection number of bidegrees
(k,k),(l,l) on P1×P1, as explicitly justified in the new h4165 reviewer report.
Summing gives **3,846,704**, down from 7,754,528. The imported bidegree bound
removes 3,877,264 from the old allowance, the already available exclusion of
z=0 removes 88, and the new reflection closure removes 30,472. Under the old
total-degree bound alone the axis/stabilizer accounting gives 7,693,412, with
60,944 attributable to reflections. No whole pair is removed. Do not divide
all canonical-pair bounds by six or impose a chamber on only the canonical pairs.

The exact physical fixtures in `physical.json` are z=±r, where r is the unique
real root of `r^7+r^6+r^3−1=0`, `4/5<r<81/100`. Each has six active curves,
243 vertices, 261 unit edges and chromatic number three. Their active IDs
and full-label factor-graph colour certificates are in `EXPECTED.json` and
`certificate.json`. Their first-digit colour word already appeared in h4105,
so they provide no new positive candidate signal.

## Reproduce the complete-frontier accounting

From the repository root, with fresh output paths:

```sh
python3 -B hadwiger_nelson_complex_radix_d3_quotient/export_quotient.py --out /tmp/hn-axis-quotient.json
python3 -B hadwiger_nelson_radix_incidence_geometry/verify.py --export-interface /tmp/hn-axis-incidences.json
python3 -B hadwiger_nelson_radix_incidence_geometry/frontier_effect.py --quotient /tmp/hn-axis-quotient.json --interface /tmp/hn-axis-incidences.json --export-remaining /tmp/hn-axis-pairs.json --check-expected
python3 -B hadwiger_nelson_radix_reflection_axes/free_action.py --pairs /tmp/hn-axis-pairs.json --check-expected
```

The 131,356-pair list has canonical JSON SHA-256
`9aa6caf04379f9e8c9736ad8d287ea51902c63e4d317f9c9c7deb112700f8149`.
The output is `FRONTIER_EFFECT.json`. Both normal and optimized Python runs
agree. The programme checks all bivariate substitutions against the
coefficient-row actions before using the stabilizers.

## Shared next interface and ownership

HN3 h4171 was consumed before publication: its 5,382 realized affine pencils
give 132,232,896 necessary curve-level survivors; 128,616 pair systems are
exact-five compatible and 2,740 require at least six active curves. The new
axis exclusion and free action apply to all those modes and to future
higher-incidence reductions. Neither h4171 nor this result supplies a
non-four-colourable member.

HN3 can apply the explicit nonvanishing condition and stabilizer-adjusted
allowances to its complementary algebraic parameter viability work on that
interface. In particular, any claimed non-four concurrence on an excluded
axis is now impossible, and exact root accounting should report H_q-orbits
rather than silently divide by the full group. HN2 retains physical graph
construction and exact chromatic decisions; no duplicate axis census is
requested. This is the pass boundary, with no new parameter locus begun.

The standalone axis theorem uses independently accepted h4119 and the
independent h4151 reviewer inventory. The whole-frontier counts retain the
h4117 completeness trust boundary. This new result awaits reviewer-1;
author-side different-code checks do not substitute for that review.
