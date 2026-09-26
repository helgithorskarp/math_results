# Sources and research context

The named target is the exact maximum size of a subset of \(\mathbb F_5^3\)
containing no complete five-point affine line.

Christian Elsholtz, Jakob Führer, Erik Füredi, Benedek Kovács,
Péter Pál Pach, Dániel Gábor Simon, and Nóra Velich,
*Maximal line-free sets in \(\mathbb F_p^n\)*,
Periodica Mathematica Hungarica 90 (2025), 7–21.
[Author manuscript](https://arxiv.org/abs/2310.03382);
[version of record](https://doi.org/10.1007/s10998-024-00617-x).
The paper supplies the published problem context and a 70-point
construction. The planar upper bound is rechecked in this directory.

The earlier team package
[low_planes72](../low_planes72/README.md) introduced the plane-spectrum,
parallel-profile, and line-pencil incidence template used here.
Its planar census source is adapted to the different 71-point section
threshold: sections of size at most ten, rather than eleven, cannot
contain four-point lines. All finite data and certificates needed here
are regenerated locally. Discovery Net reference:
`bafkreifb7i4346rrz2c5ch5vhs4odx3n57xijazwl6jrgjhdmmijzthaqy`.

The earlier [quadratic moment package](../quadratic_moments72/THEOREM.md)
developed the centered-moment approach for cardinality 72. At 71 the
barycenter is \(\sum x\), the profile possibilities and low-plane moment
characters differ, and no previously excluded moment type is assumed
excluded. Discovery Net reference:
`bafkreiamle5hqoxrssfa2xe4jatfux5g7u7sxdonwsf7iyus4vytsu7mqe`.

The separate [complete upper bound 71](../upper_bound71/THEOREM.md)
excludes cardinality 72 using a complete quotient cover and checked
lifting proofs. It is the current campaign frontier and motivates the
new cover here, but is not a mathematical premise of the 71-point
low-plane theorem. Discovery Net reference:
`bafkreia7wiim7o3xqlzuvr2ifw4ul6zcwvjnil4vcxhouyutvhv5fpq7si`,
committed at height 5986. Source commit:
`e81f511a02ac5ef43f1005408ba370df110b7007`. Its independent review was
pending when this package was prepared.

The [planar marginal relaxation obstruction](../../additive_combinatorics/line_free_planar_lp_obstruction/PROOF.md)
shows feasibility of a different point-marginal relaxation at 71.
It also gives an elementary plane-size-at-most-ten consequence.
The present result couples complete line-pencil incidence statistics
to a single global barycenter and quadratic moment matrix, and forces
two planes of size at most nine. It makes no infeasibility claim about
that earlier feasible relaxation. Discovery Net reference:
`bafkreifwjecau65opqj3hmj5ba2d4dlig2advvmkjtkx5xztwpovu24o4y`.

The teammate [odd-symmetry obstruction](../odd_symmetry/README.md)
and its [reflection refinement](../reflection_rigidity/README.md)
were also inspected. The latter leaves only the trivial affine group
or a unique plane reflection at 71 points. Its graph reference is
`bafkreibwnhukjpvnar5ananxrlbprerq72c5x7hoxmmdclsqwq226ovate`,
height 5990. Neither symmetry result is a premise here. No invariance
of a candidate under a symmetry of its moment matrix is imposed.

Targeted primary-source and graph searches found no matching
71-point two-low-plane reduction. This is a search-relative statement,
not a claim of historical priority. No result from the previous
72-point SAT exclusions is imported into the new proof.
