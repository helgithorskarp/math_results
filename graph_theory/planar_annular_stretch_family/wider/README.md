# Wider stretched cylinders and the required boundary depth

The half-separator theorem for independently stretched or deleted vertical
edges extends to **circumference 10 at every height `h>=2`**, and
**circumference 12 at every height `h>=4`**. For every nonnegative real vertex
mass, at most two shortest paths in the original graph leave every component
with at most half the total mass. Cap, horizontal, and alternating diagonal
edges retain length 1; each vertical edge independently has any real length
at least 1 or is deleted. The [proof](PROOF.md) specifies the graphs fully.

Two changes make these wider families accessible. An interior row is covered
by two disjoint arcs, each with `m/2` vertices and only `m/2-1` edges. Boundary
medians use three-row and four-row kernels, with three and thirteen explicit
candidate separators. These depths are **minimal for this proxy-avoiding
boundary reduction**: any `k`-row unit kernel fails the anchored lemma when
`m>2(k+2)`, by a concrete mass assignment and a path-length bound. This is a
limitation of the reduction, not a planar counterexample.

The result extends the [earlier circumference-6/8 theorem](../PROOF.md).
It does not establish arbitrary circumferences, unrestricted edge lengths,
or the independent-vertical regime at circumference 12 and height 3.
[Barbados Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf)
remains outside the proved scope. The earlier common-short-vertical potential
also applies here; the [reviewer's layer-dependent extension](../../planar_annular_stretch_family_review1/REVIEW.md)
is a separate previously proved strengthening. No literature-priority claim
or independent review of this new supplement is asserted.

## Reproduce

With Python 3.11 or later, from the repository root:

```sh
python3 graph_theory/planar_annular_stretch_family/wider/verify.py --check
```

Only the standard library is needed. The verifier reconstructs the graphs,
checks each listed path against original-graph BFS distances, checks that no
vertical edge or forbidden proxy appears, recomputes components, and verifies
each forced-heavy-component step. No solver or exhaustive graph generator
is used. The three finite certificates are:

| Circumference | Kernel height | Half-mass anchor | Cuts | Distinct paths |
|---:|---:|---|---:|---:|
| 10 | 3 | near cap and first row | 3 | 6 |
| 12 | 4 | near cap and first two rows | 13 | 26 |
| 10 | 2 | none; whole-graph statement | 8 | 14 |

The last kernel handles the short cylinder before the boundary contraction
applies. [certificate.json](certificate.json) contains the path lists in a
forcing order; [expected.json](expected.json) records component orders and
the unique-compatible-component counts, ending in zero.

Expected result: `PASS`, 980 constructed witnesses through height 33 and
order 398, 33,968 quotient-edge checks, and six rejected invalid controls.
Witness distances are independently checked with exact integer Dijkstra,
including unit, independently stretched, partially deleted, and wholly
deleted vertical-edge fixtures. The certificate SHA-256 is
`65a17bee5fd4e1b38911fe09d02076bff15ea5d350eb466e965785556970ff93`.

The all-height, arbitrary-real-mass and arbitrary-real-length conclusions
depend on the written reduction and the exact finite component certificates.
Finite mass fixtures are consistency checks, not the source of those
quantifiers. The discovery search used exact mass constraints and all tied
allowed geodesics; neither its solver nor its completeness is needed to
verify the displayed positive certificates.
