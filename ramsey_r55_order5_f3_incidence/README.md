# Two incidence patterns for an order-five Ramsey automorphism

Let `G` be a hypothetical `(5,5;43)` graph with an automorphism of type
`1^3 5^8`. Its three fixed vertices cannot form a monochromatic triangle.
After a global color reversal and relabeling, their edges are
`xy=red`, `xz=yz=blue`, their red degrees are `21,21,20`, and the
fixed-to-cycle incidence matrix is one of exactly two necessary patterns.

Encode a column by the subset of red fixed neighbors, with bit weights
`x=1`, `y=2`, `z=4`. Up to moving-cycle permutation the column lists are:

```text
h=0: 0 1 2 3 5 5 6 6
h=1: 0 1 2 3 4 5 6 7
```

The equivalent multiplicity table is:

| red fixed neighbors | h=0 | h=1 |
|---|---:|---:|
| empty set | 1 | 1 |
| `{x}` | 1 | 1 |
| `{y}` | 1 | 1 |
| `{x,y}` | 1 | 1 |
| `{z}` | 0 | 1 |
| `{x,z}` | 2 | 1 |
| `{y,z}` | 2 | 1 |
| `{x,y,z}` | 0 | 1 |

This is an **analytic necessary-condition theorem**, with finite audits.
It is not an exclusion of `1^3 5^8`, a 43-vertex witness, or an improvement
to the Ramsey bound. Combined with the
[automorphism handoff](../ramsey_r55_automorphism_exclusion_handoff), it
applies to every possible order-five element of `Aut(G)`.

## Proof mechanism

The [complete proof](PROOF.md) uses `R(4,5)<=25` to force each fixed
vertex to meet exactly four moving cycles in red. Common-neighborhood
bounds give pairwise row intersections at most two. The decisive extra
restriction is a mixed common-neighborhood bound: when `uv` has color
`c`, vertices joined to `u,v` in `c` and to the third fixed vertex in
`1-c` form a `(3,4)` coloring. There can be at most eight such vertices,
hence at most one whole 5-cycle. These inequalities force the table by
three row equations. Elementary proofs of `R(3,4)<=9` and `R(3,5)<=14`
are included, so only `R(4,5)<=25` is imported.

An immediate corollary is that the total edge count is `1` modulo five
in the chosen normalization, or `2` modulo five after color reversal.

## Reproduction

Requirements: Python 3.11 or later, a POSIX shell, `cmp`, and `sha256sum`.
No third-party Python packages, SAT solvers, graph catalogs, network
downloads, or external certificates are required. Tested with Python
3.11.2 on Linux.

```sh
sh verify.sh
```

The command verifies source hashes, regenerates `result.json`, and
byte-compares both it and the two audit summaries with the committed
reference files. It runs in a few seconds on the research host.

- `enumerate_multiplicities.py` exhausts all 6,435 multisets of eight
  three-bit columns and all relevant fixed-triangle colorings. It finds
  57 balanced multisets, 15 satisfying the pair caps, 15 equivalence
  classes before the mixed cap, and **two classes after it**. The latter
  correspond to 12 column multisets with fixed labels retained, or
  302,400 incidence matrices with fixed and moving-cycle labels retained.
- `audit_rows.py` uses a different parameterization: fix the first row's
  four-subset, enumerate the other two rows and the fixed edges, and test
  the conditions by direct set intersections. It tests 39,200 choices
  and finds 4,320 survivors: 864 of type `h=0` and 3,456 of type `h=1`.
  Multiplying by the first row's 70 possible four-subsets agrees with
  the other enumerator. No symmetry-canonicalization code is shared.
- `audit_local_pairs.py` constructs every 13-vertex coloring consisting
  of the three fixed vertices and two selected moving cycles, for all
  internal `C_5` choices and all 32 cross words. It checks rotation
  invariance and tests all 1,287 five-sets for monochromaticity. There
  are 224 templates and 7,168 colorings across the two patterns; every
  template has between six and 32 allowed cross words.

These are audits by the same researcher, not an independent peer review
or a proof-assistant formalization. The mathematical proof does not rely
on their completeness. The local-pair existence assertion does rely on
the direct finite audit.

## What remains

Both patterns survive the full no-monochromatic-`K_5` check on the three
fixed vertices together with any two moving cycles, for either internal
coloring of those cycles. Their cross words may be chosen independently
for these pair tests, but this does not control sets meeting three or
more moving cycles, nor does it impose all 43-vertex degrees. A full
extension computation must couple those pair choices.

The next useful finite split is therefore the **two displayed incidence
patterns**, with the full Ramsey constraints retained. This package does
not launch that computation or claim either split is feasible or
infeasible. The recorded representatives specify 27 edge-orbit colors
(24 incidences and three fixed edges); 16 internal and 140 cross-cycle
edge orbits remain before using the internal `C_5` identities. The whole
action has 183 edge orbits.

## Prior work and scope

The external [wustep/maths q4 source](https://github.com/wustep/maths/tree/main/problems/ramsey-r55/compute/q4)
certifies other order-five types but records its maximal type `1^3 5^8`
as unresolved. Its [neighborhood enumerator](https://github.com/wustep/maths/blob/main/problems/ramsey-r55/compute/q4/neighborhoods.py)
uses one fixed vertex's selected moving cycles. The present proof couples
all three fixed incidence rows using the mixed `(3,4)` cap; it does not
replay that neighborhood enumeration. This distinction was checked
against the public q4 source and the committed Discovery Net context
on 2026-09-04. No universal priority claim is made.

The imported bound is McKay--Radziszowski,
[*R(4,5)=25*](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf),
J. Graph Theory 19 (1995), 309--322. The proof is conditional on that
established theorem; the package does not rerun its computation.
