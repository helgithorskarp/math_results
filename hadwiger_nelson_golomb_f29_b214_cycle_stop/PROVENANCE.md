# Provenance and trust boundary

The physical source was chosen as one finite, heterogeneous three-component
cycle with a conditional 499-point spindle completion. Selection preceded
complete contact reconstruction and colour testing. Neither S343 finishing
nor either Parts receiver was used.

- F29 coordinates and positive source word come from the exact
  [frozen-centre package](https://github.com/helgithorskarp/math_results/tree/ef05942eeebba29628dc02f37a5792ac7d4122b8/hadwiger_nelson_frozen_centre_transfer).
  The reused `points.tsv` hash is
  `3631210e31697804a86437cc7b6f734870097e22de50e5c4721ecea6ab633924`.
- The B214 fixture is
  [points214.tsv](https://github.com/helgithorskarp/math_results/blob/fa6f78f998ba36a40a8077f2c00d3656d0b40322/hadwiger_nelson_nonmono159_214_lowden2/points214.tsv),
  hash `97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f`.
  Its published distance-three unequal-pair interpretation motivated the
  incompatibility test. The stopping theorem uses only the exact coordinates
  and a directly checked proper word, not that negative forcing property.
- Golomb coordinates are stated directly in the checker. Their complete
  18-edge graph and three-colour impossibility are re-established there.

The initial fixture audit corrected a reversed prose labelling of B186 and
B187: the fixture has B186=+3/2, B187=-3/2. This correction occurred before
any physical graph was constructed. The displayed isometry and physical
positions of P,Q did not change.

The producer used the eight-dimensional complex monomial basis with squares
-3,-11,-7. The verifier independently rebuilds both Cartesian axes with
positive real radicals. All 250 coordinates, 1,070 edges and 31,125 squared
norms agree entrywise. Graph reconstruction took about 2.5 seconds in the
simple producer and less than a second in the standalone checker.

Kissat 4.0.4 was used for exactly two positive queries, each with
`--time=10 --conflicts=100000`: a proper colouring of the 38-point connected
Golomb/F29 input with equal tips, and a whole-graph colouring with O!=P.
Both returned SAT, in approximately 0.003 and 0.063 seconds, and their decoded
words are checked against the exact physical graphs. No solver UNSAT,
UNKNOWN, floating predicate or unprovided proof file is a premise. No solver
is needed to reproduce the theorem. Operational CNFs and logs remain local.

Normal and Python optimized verification agree. Controls reject an improper
whole word, an incorrect equality template, an improper F29 template, a false
input word and a hypothetical extra private contact that defeats the extension
rule. All 16 interface-colour assignments are checked on valid templates.
These are author-side checks, not independent review of the new source.

The claimed scope is the one frozen 250-point graph, universal projection
onto the complete B214 input, and failure of its selected root/P equal-pair
gate. No full enumeration of B214 words, new forcing relation, five-chromatic
spindle or global heterogeneous-composition exclusion is claimed.
