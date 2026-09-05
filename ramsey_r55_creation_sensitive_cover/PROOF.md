# Creation-sensitive repair requires at least 39 visible edits

## Scope

Let G be the unchanged labeled 353-K5 seed in
[`EXIT_GRAPH.json`](../ramsey_r55_k5_neutral_component/EXIT_GRAPH.json), SHA256
`9f4bd3853e985697f7fc496c0544f9d800235c2ece4a25cb718a2c3181559916`.
Its exceptional set E={0,1,2} is a red triangle of degree-20 vertices.
The forty central vertices C={3,...,42} have red degree 21. There are 450
red edges, and all three exceptional local profiles are (92,107).
All 176 red and 177 blue K5s are contained in C.

Consider any labeled graph H such that:

1. Every edge incident with E has its color in G.
2. Every vertex keeps its individual red degree in G.
3. Each exceptional local profile remains (92,107).
4. Every original colored K5 of G is destroyed in its original color.
5. H has no monochromatic K5 meeting E.

No cell quota, central hard cap, pointwise root inequality, graph symmetry,
or isomorphism normalization is imposed. New central K5s are allowed.

A central edge is **visible** if it lies in at least one of the six fixed
exceptional color-neighborhood vertex sets. There are 656 visible edges.
The remaining 124 join complementary three-bit incidence signatures.

**Theorem.** Such an H differs from G on at least 39 visible edges.
More precisely, the exact linear certificate proves at least
95427/2500 = 38.1708 visible edits before integrality is used.

The earlier [cover theorem](../ramsey_r55_visible_obstruction_cover) proved
an exact visible optimum of 34 when condition 5 was omitted, even after
adding all 884 pointwise rows. Thus mixed-K5 prevention forces a gap of
**at least five visible edits** over that optimum. The old 34-edit cover
witness does not contradict this theorem: it contains 156 mixed K5s.

This is not a claim that 39 is sharp, that a graph satisfying 1--5 exists,
or that a full Ramsey graph exists. It excludes all visible budgets at most
38 in this fixed-incidence/profile setting, not an entire degree profile or
the full 43-vertex Ramsey problem. The earlier total-edit lower bound 52
remains applicable. No new total-distance optimum is computed here.

## Individual-edge encoding

For each of the 780 central edges e let x_e in {0,1} indicate a toggle.
Put s_e=1 for an originally blue edge and s_e=-1 for an originally red edge.
The red-indicator change is s_e x_e. The vanishing conservation expressions
are the forty degree changes and the six red-edge changes inside fixed
exceptional color neighborhoods:

```text
D_u = sum_{e incident with u} s_e x_e,
P_{r,R} = sum_{e inside N_R^G(r), central} s_e x_e,
P_{r,B} = sum_{e inside N_B^G(r), central} s_e x_e.
```

The last expression is the negative of the *blue* local-profile change.
Fixed exceptional incidences make every expression linear. We use no
cardinality auxiliaries or symmetry breaking.

For an original colored K5 K, h_K=sum_{e in binom(K,2)} x_e must be at
least one. This condition forbids its original color, not necessarily the
opposite color on the same five-set.

For a possible mixed K5 T in color c, every fixed edge must already have
color c; otherwise it is impossible under every assignment. Let M be the
central edges of T originally having color c and B its central edges of
the opposite color. Avoiding the forbidden configuration is exactly

```text
sum_{e in M} x_e + sum_{e in B}(1-x_e) >= 1,
or  sum_{e in M} x_e - sum_{e in B} x_e >= 1-|B|.
```

This follows by requiring at least one edge of T to end in the opposite
color. It is valid for simultaneous edits, not just individual flips.
Together with the degree/profile equations and binary boxes, all 353 old
cover rows and all mixed rows encode conditions 1--5 exactly.

There are 31153 distinct mixed rows: 31125 have six free edges and 28 have
three. One root and four central vertices give the former. A red pair of
exceptional roots and three common red central neighbors give the latter.
Three exceptional roots cannot occur in a red K5 here because the triple
common-red signature cell is empty; two roots cannot occur in a blue K5
because E is red. Literal enumeration checks all 304590 five-sets meeting E.

## One-hole repair implications

The exact certificate uses 96 of the original K5 rows and 224 mixed rows.
**Every selected mixed row has exactly one originally opposite-colored
edge.** If that edge is f, the row becomes the homogeneous implication

```text
x_f <= sum_{e in M} x_e.
```

Thus toggling the unique missing edge must be accompanied by a repair flip
elsewhere in the same five-set. These rows express creation dependencies,
not just destruction of existing K5s. They remain necessary even if many
edges are changed at once. Each triggering edge is visible, since it is
central inside a fixed color neighborhood of an exceptional root.

For example, {0,11,13,14,27} is blue except for red edge {11,14} in G. It gives

```text
x_11,14 <= x_11,13 + x_11,27 + x_13,14 + x_13,27 + x_14,27.
```

The certificate weights this row by 564. In all, the 224 rows cover 99
distinct triggering edges. They consist of 104 blue and 119 red five-sets
with one exceptional root, and one red five-set with two exceptional roots.
Their total multiplier is 275676. The condition itself is the elementary
colored-K5 clause, not a claimed novel general implication principle.

## Exact weighted edge-capacity proof

All data are in [`certificate.json`](certificate.json). Write q_T for the
left side sum_{M}x-sum_{B}x of a selected mixed row; here q_T>=0. At scale
10000 the checker verifies the coefficient identity on every central edge

```text
10000 sum_{visible e} x_e
 = sum_K a_K h_K + sum_T w_T q_T + sum_j b_j E_j
   - sum_e p_e x_e + sum_e r_e x_e.
```

Here a_K,w_T are positive integers, E_j are fourteen degree and five profile
expressions, all p_e>=0, and all residuals r_e>=0. The weights a_K total
383172. Eighty upper-box penalties p_e total 1464. Therefore, using h_K>=1,
q_T>=0, E_j=0 and 0<=x_e<=1,

```text
10000 visible_edits >= 383172 - 1464 = 381708,
visible_edits >= 95427/2500 > 38.
```

Integrality gives at least 39. The certificate actually requires only the
selected 96 old rows and 224 one-hole implications, rather than every old
or possible mixed K5. No 884 pointwise inequalities occur in this proof.

The integer weights were discovered by rounding a numerical LP dual at
scale 10000. Every overloaded edge was repaired by an exact upper-box
penalty. The numerical optimum near 38.1790847 and an exploratory solver
infeasibility message are not proof inputs. All arithmetic in the checker
is integer arithmetic or exact rational reduction. The complete residual
vector has SHA256
`18e606baeebec7211f90d78a7c1858d834fbc6c51b4a39b0a117d4fc06acbbe7`.

## Verification and boundary

The proof checker imports no producer or solver. It pins and reuses the
parent's exact seed decoder, visibility definition and seed K5 audit. New
weighted rows are reconstructed independently as literal edge-color
disjunctions. Each fixed edge, original-colored K5, selected mixed five-set,
degree/profile charge and all 780 residual capacities are checked directly.

Separately, the full mixed formula is reconstructed by visiting every mixed
five-set, rather than generating root-neighborhood four-sets. Complete
canonical row and equality hashes agree with the producer. Formula
completeness is useful for reproduction but is not needed for the bound:
the selected inequalities alone suffice.

Nine corrupted certificates or encoding fingerprints are rejected. All
8320 truth-table combinations of original coloring, final coloring and
forbidden color are checked for widths three and six. Every selected row
is independently checked to have precisely one hole. Normal and optimized
Python agree on the certificate, full encoding hashes, report and controls.

The lower bound closes the previous cover optimum and all budgets through
38 under creation-sensitive conditions. It does not settle the next budget
or all central K5 prevention. No graph is produced in this pass, and the
353-K5 endpoint remains unchanged. No new radius, descent or subsequent
construction phase was started after obtaining this certificate.
