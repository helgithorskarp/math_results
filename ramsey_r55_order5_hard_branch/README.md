# The hard order-five Ramsey branch has one degree profile and three marked cases

Combining the team's local-deficiency theory with its residual order-five
incidence theorem gives a more restrictive construction interface. Suppose
a hypothetical `(5,5;43)` graph is in the hard branch and has an automorphism
of cycle type `1^3 5^8`. Normalize its fixed vertices so `xy` is red and
`xz,yz` are blue. Then:

- its red degree multiset is exactly `20^6 21^32 22^5`, with 451 red edges;
- one moving cycle `L` has degree 20, one `H` has degree 22, and the other
  six have degree 21;
- the unique degree-20 fixed vertex `z` has local red/blue counts `(90,105)`;
  every other vertex has local deficiency exactly seven in both colors;
- there are exactly 32 doubly exact vertices, and the red/blue triangle
  totals are `(1430,1435)`;
- the red bipartite graph between `L,H` is 3-regular, and their incidence
  columns differ only at `z`: `z-L` is red and `z-H` is blue;
- up to the allowed relabelings, only the three marked cases below remain.

These are necessary conditions. None of the three marked cases is asserted
globally feasible or excluded. This does not exclude an order-five action
outside the hard branch, or produce a 43-vertex Ramsey graph. It is a
theory-to-construction handoff, not a duplicate full construction search.

## Inputs and normalization

Write `t_R(v)` for the red edges induced by the red neighborhood of `v`,
and `t_B(v)` for the analogous blue count. The hard branch has

```text
t_R(v) <= U(d(v))-7,     t_B(v) <= U(42-d(v))-7,
U(18..24) = 85,92,100,107,114,122,132.
```

The [local-deficiency identity](../ramsey_r55_local_extremal_deficiency/README.md)
gives a symmetric degree weight and total excess

```text
w(18..24) = 21,12,3,0,3,12,21,
W = sum_v w(d(v)) in {3,9,...,39},
E = sum_(v,color) (deficiency(v,color)-7) = (43-W)/2.       (1)
```

The [residual order-five incidence theorem](../ramsey_r55_order5_f3_incidence/PROOF.md)
proves that the fixed triangle is mixed. After complementing if needed,
`xy` is its unique red edge, the fixed degrees are `(21,21,20)`, and the
moving cycles have one of the incidence lists

```text
h=0: 0,1,2,3,5,5,6,6,
h=1: 0,1,2,3,4,5,6,7.                                  (2)
```

Bits `x=1,y=2,z=4` specify red fixed neighbors. We use this fixed-triangle
normalization, **not** an extra assumption that red is initially sparser.
The conclusion `m=451` will be derived. This matters when considering the
temporarily possible 456-edge case below.

Each moving cycle induces a red `C_5` and a blue `C_5`: the two invariant
distance classes cannot both be red or both blue without a monochromatic
`K_5`. Thus every moving vertex has two internal neighbors of either color.

## 1. Divisibility concentrates the entire excess at one fixed vertex

For each fixed vertex, both local counts are divisible by five. Indeed,
the automorphism acts on the pairs in either color-neighborhood. Every
pair orbit has length five unless its two vertices are fixed. The only
possible singleton pair would complete the fixed triangle, which is mixed,
so it contributes to neither monochromatic count.

Every moving vertex has degree 20, 21, or 22. Any other degree would put
at least `5*12=60>39` weight on its moving orbit alone. If `k` moving
cycles have noncentral degree, (1) gives

```text
W = 3+15k.
```

The weight cap and parity force `k=0` or `k=2`.

If `k=0`, the global degree multiset is `20^1 21^42`, and `m=451`.
The [vertexwise neighborhood identity](../ramsey_r55_one_defect_anchor_localization/README.md)
at `z` gives

```text
t_R(z)+t_B(z) = choose(22,2)-451+20*21 = 200.
```

But the hard caps are 93 and 107, and divisibility by five improves them
to 90 and 105, whose sum is only 195. Thus `k=0` is impossible here.

Hence `k=2`, `W=33`, and `E=5`. Divisibility at `z` costs at least

```text
(93-90)+(107-105) = 3+2 = 5
```

units of excess. It consumes the whole budget. Therefore

```text
(t_R(z),t_B(z))=(90,105),
deficiency(v,R)=deficiency(v,B)=7  for every v!=z.         (3)
```

In particular `x,y` and all degree-21 moving vertices are doubly exact.
Here a doubly exact anchor means `d(v)=21` and `t_R(v)=t_B(v)=100`.
The actual deficiencies at `z` are 10 in red and 9 in blue.

## 2. Triangle incidence forces one low and one high moving cycle

The two exceptional moving cycles might initially have degrees `(20,20)`,
`(20,22)`, or `(22,22)`. Equation (3) fixes every local count. Summing them
gives the following exact arithmetic:

| exceptional cycle degrees | red edges m | sum of red local counts | sum of blue local counts |
|:---:|---:|---:|---:|
| 20,20 | 446 | 4220 | 4375 |
| 20,22 | 451 | 4290 | 4305 |
| 22,22 | 456 | 4360 | 4235 |

Each monochromatic triangle is counted at its three vertices. The first
and third rows fail divisibility by three. Only the middle row survives,
giving degrees `20^6 21^32 22^5` and triangle counts `(1430,1435)`.
Let `L,H` denote the moving cycles of degree 20 and 22, respectively.

## 3. Weighted neighborhoods locate the exceptional cycles

Put `epsilon(v)=d(v)-21` and `S(v)=sum_(w in N_R(v)) epsilon(w)`.
The neighborhood identity reads

```text
t_R(v)+t_B(v) = choose(42-d(v),2)-451+21d(v)+S(v).        (4)
```

Only `z,L,H` have nonzero weights: `-1,-1,+1`, respectively. At `x,y`,
the left side is 200 and `d=21`, so `S=0`. Each moving orbit contributes
five identical incidences at a fixed vertex, and its other fixed red
neighbor has weight zero. Thus `x` has the same color toward `L` and `H`,
and so does `y`.

At `z`, the left side is 195 and `d=20`, so `S(z)=-5`. It has no fixed
red neighbors. Consequently `z` is red to `L` and blue to `H`. The two
columns therefore differ precisely in bit `z`.

Let `k_ij` be the red degree per vertex between moving cycles `C_i,C_j`.
The bipartite graph is regular on both sides by the cyclic action, so
`k_ij=k_ji` and it has `5k_ij` red edges. At a vertex in `L`, the left
side of (4) is `93+107=200`. Its weighted sum is

```text
S(v)=k_LH-2-1 = k_LH-3,
```

where the two terms subtracted come from its two internal red neighbors
and `z`. Equation (4) forces `S(v)=0`, hence `k_LH=3`. At `H`, the same
conclusion follows from `S(v)=2-k_LH=-1`.

For every ordinary degree-21 moving cycle `C_i`, equation (4) gives

```text
k_iH-k_iL = c_z(i),                                    (5)
```

where `c_z(i)` is its red-incidence bit toward `z`. These are six coupled
cross-degree constraints, not independent pair choices.

## 4. Three marked normal forms

Insert the column relation into (2). In `h=0`, the only possibilities
are `(column(L),column(H))=(5,1)` or `(6,2)`, equivalent by exchanging
`x,y`. Repeated identical columns can be permuted. In `h=1`, the pairs are
`(4,0),(5,1),(6,2),(7,3)`. Exchanging `x,y` identifies the middle two.

The pair `(7,3)` is impossible. Both moving cycles are red-adjacent to
`x,y`, and `xy` is red. A vertex of `L` has three red neighbors in `H`;
three vertices of a `C_5` contain a red edge because its independence
number is two. This red triangle with `x,y` forms a red `K_5`.

The remaining marked cases, with zero-based cycle indices in (2), are

| case | h | column(L), column(H) | indices L,H |
|---|---:|:---:|:---:|
| repeated-column case | 0 | 5,1 | 4,1 |
| no shared red fixed neighbor | 1 | 4,0 | 4,0 |
| single shared red fixed neighbor | 1 | 5,1 | 5,1 |

This classifies marked incidence schemes, not graph isomorphism classes.
All three survive the restricted test on `x,y,z,L,H` with `k_LH=3`.
For columns `(4,0)` all ten weight-three cross words work for each pair
of internal `C_5` orientations. For `(5,1)`, there are five allowed words
when the two internal steps agree and ten when they differ. These local
existence counts are finite audit results, not global extensions.

## 5. Additional linear constraints for a construction encoding

Let `p_i` be the number of red fixed neighbors of `C_i`. Let `R_u` and
`B_u` be the four red- and four blue-adjacent moving cycles at fixed
vertex `u`. Summing a moving vertex's red neighbors gives

```text
sum_(j!=i) k_ij = d_i-2-p_i,         sum_(i<j) k_ij=70.   (6)
```

Directly counting the local edges at `x,y,z` gives

```text
sum_(i<j in R_x) k_ij = 15-h,
sum_(i<j in R_y) k_ij = 15-h,
sum_(i<j in B_x) k_ij = 16,
sum_(i<j in B_y) k_ij = 16,
sum_(i<j in R_z) k_ij = 14,
sum_(i<j in B_z) k_ij = 17.                             (7)
```

For example, red local edges at `x` are `5[4+(1+h)+sum_Rx k]`: four
internal cycles, `1+h` moving cycles also adjacent to `y`, and their
cross edges. Blue local edges at `x` are `5[4+2+sum_Bx(5-k)]`, since the
two blue-incidence rows for `x,z` intersect in two columns. At `z` the
corresponding expressions are `5[4+sum_Rz k]` and
`5[4+4+sum_Bz(5-k)]`. These yield (7) from (3).

The equations may have redundant rows; no rank or global feasibility claim
is made. They supplement, not replace, the full monochromatic-five-set
constraints.

## Reproduction and machine-readable handoff

From the repository root, using Python 3.11.2 and its standard library:

```bash
set -o pipefail
python3 ramsey_r55_order5_hard_branch/audit_hard_branch.py \
  | cmp - ramsey_r55_order5_hard_branch/EXPECTED_OUTPUT.txt
python3 ramsey_r55_order5_hard_branch/audit_hard_branch.py --json \
  | cmp - ramsey_r55_order5_hard_branch/MARKED_CASES.json
cd ramsey_r55_order5_hard_branch
sha256sum -c SHA256SUMS
```

`MARKED_CASES.json` contains the three incidence schemes, marked cycle
indices, degree vectors, row/cut targets for (6)--(7), differences (5), and
the exact allowed weight-three words for the exceptional pair. A cross
word's bit `t` means that `L_a H_(a+t)` is red, with phases modulo five.
Each internal step is 1 or 2 in the same phase labeling. Independent
rotations preserve the domains; no extra automorphism is imposed.

The audit checks the fixed-pair and triangle orbit spectra directly, all
`3^8=6561` moving-degree assignments, marked placements and the excluded
pair, and all 1,287 five-sets of each of 160 marked-case/local-coloring
assignments on 13 vertices (the repeated local type is counted in each case).
Exactly 100 of those restricted colorings are valid. It also compares
(6)--(7)'s underlying counting formulas to literal local counts on 40
arbitrary invariant 43-vertex fixtures, including extreme cross words.
These fixtures are not claimed to be Ramsey witnesses. No code from the
teammate's graph generator is imported. The proof is analytic; the finite
checks audit its algebra and the explicitly labeled local feasibility claim.

## Trust boundary and relation to prior work

The hard-branch extrema, weight/excess identity, and the fixed-incidence
theorem are imported. Their pinned manifests are checked before the audit.
The graph-to-count arguments above are not proof-assistant formalized.
The finite tests use exact Python integers and literal graph counts; no
SAT/LP solver, new graph catalog, or external large certificate is used.

The external [q4 notebook](https://github.com/wustep/maths/tree/main/problems/ramsey-r55/compute/q4)
records the maximum-cycle order-five case as unresolved. Our input
incidence theorem also leaves both `h` patterns unresolved. This result
adds hard-branch restrictions by combining fixed-point congruences with
local-deficiency accounting; it does not close that unrestricted case.
No historical priority or independent peer review is claimed for this
new bridge. The earlier localization input has a separate
[independent review](../ramsey_r55_one_defect_anchor_localization_review3/README.md).

The general 88-profile/321-split relaxation remains unchanged for graphs
without this action. Here its unique compatible global profile survives,
but its moving-cycle structure is sharply restricted. The combinatorial
method supplies durable constraints for team-r55-1's construction lane;
no full three-case extension computation is launched in this checkpoint.
