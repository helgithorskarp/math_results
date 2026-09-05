# A sharp exposed-edge cover bound

## 1. Fixed graph and exact scope

Let G be the labeled graph in the parent's
[`EXIT_GRAPH.json`](../ramsey_r55_k5_neutral_component/EXIT_GRAPH.json), SHA256
`9f4bd3853e985697f7fc496c0544f9d800235c2ece4a25cb718a2c3181559916`.
It has 43 vertices, E={0,1,2}, C={3,...,42}, and 450 red edges.
E is a red triangle; its vertices have red degree 20 and all others degree 21.
Every exceptional local profile is (92,107), where the two entries count
red edges in its red neighborhood and blue edges in its blue neighborhood.
There are exactly 176 red and 177 blue K5s, all in C.

All graphs below are labeled, simple, and on this same vertex set. Define Q0
by the following conditions on a recoloring H:

1. All edges incident with E have the same colors as in G.
2. Each vertex has exactly its degree in G.
3. The three exceptional local profiles remain (92,107).
4. None of G's 353 **colored** K5s survives in its original color.

Condition 4 may allow new K5s, including an old five-set in its opposite
color. Let Q be the subset of Q0 satisfying all 884 pointwise root bounds
from the [original realization](../ramsey_r55_triple_graph_realization).
Those inequalities are restated below. Neither Q0 nor Q forbids all mixed
K5s or imposes the central hard caps. They are cover relaxations, not the
mixed-free repair family of the preceding component calculation.

Call a central edge visible if both its endpoints belong to at least one
of the six exceptional color neighborhoods. Exactly 656 of the 780 central
edges are visible. The other 124 have complementary three-bit signatures.
Indeed, an edge is invisible exactly when its endpoints have opposite
incidences to each of the three exceptional roots. No graph symmetry or
isomorphism quotient is assumed.

**Theorem.** Every H in Q0 differs from G on at least 34 visible edges and
at least 52 total edges. There exists H in Q with exactly 34 visible edits.
Consequently the minimum visible edit count is exactly 34 for both Q0 and Q.

In particular, any full Ramsey graph retaining the stated incidences,
individual degrees, and exceptional profiles would require at least 34
visible and 52 total edits. The theorem does **not** say that a full Ramsey
graph, a mixed-free repair, or a central-cap-feasible graph exists at either
bound. It does not cover changed exceptional incidences or profiles.

## 2. Exact edit encoding

For each central edge e=uv, let x_e be one if it is toggled and zero otherwise.
Let s_e=1 if e is blue in G and s_e=-1 if it is red. Thus the change in the
red edge indicator is s_e x_e. No edges incident with E are variables.

For a vertex u in C and an exceptional root r define

```text
D_u(x) = sum_{e incident with u} s_e x_e,
P_{r,R}(x) = sum_{e inside N_R^G(r), e central} s_e x_e,
P_{r,B}(x) = sum_{e inside N_B^G(r), e central} s_e x_e.
```

The forty D values and six P values must vanish. The blue-neighborhood
quantity P_{r,B} counts the **change in red edges**, hence its negative
is the change in the blue entry of the local profile. Both being zero is
equivalent. Fixed exceptional incidences make all these quantities linear.

For each original colored K5 K put h_K(x)=sum_{e in binom(K,2)} x_e.
Its original color survives exactly when h_K=0. Thus condition 4 is exactly
h_K>=1 for all 353 K, with x_e in {0,1}. Conversely every binary solution
of these equations and cover inequalities decodes to a graph in Q0.
There are no auxiliary variables, symmetry breaks, or fixed cell quotas.

The producer additionally uses the following 884 rows for Q. For disjoint
red clique A and blue clique B contained in E, A union B nonempty, put
S={v outside A union B: A subset N_R(v), B subset N_B(v)}. Then, for u
outside the roots, impose

```text
A subset N_R(u)  => d_R(u,S-{u}) <= U(4-|A|,5-|B|)-1,
B subset N_B(u)  => d_B(u,S-{u}) <= U(5-|A|,4-|B|)-1.
```

Here U(1,b)=U(a,1)=1; otherwise U(a,b) is U(a-1,b)+U(a,b-1), minus one
when both summands are even. Membership in S and applicability at u depend
only on fixed exceptional incidences. The producer translates each row
into an affine inequality in the individual x_e. The standalone checker
instead reconstructs A, B, S and the actual red/blue degrees of the graph.
The inherited Ramsey interpretation of these rows is not needed for the
two lower-bound certificates: both certificates omit them altogether.

## 3. A 54-clique capacity certificate gives 34 visible edits

The visible certificate in [`certificate.json`](certificate.json) selects
54 genuine original colored K5s and gives each a positive integer weight
a_K. Their total weight is 398. Define the conservation expression

```text
L(x) = sum_{u=3}^{10} D_u(x) - sum_{u=39}^{42} D_u(x)
       - P_{0,R}(x) + P_{0,B}(x).
```

The data certify nonnegative integer edge residuals r_e such that

```text
12 sum_{visible e} x_e
  = sum_K a_K h_K(x) + 12 L(x) + sum_e r_e x_e.
```

This is a coefficient identity on all 780 individual central edges. The
checker derives each clique's ten edges literally, computes the signed
degree/profile coefficients from the graph, and checks every residual
exactly. Residuals lie between 0 and 24; no x_e<=1 multipliers are needed.
The full canonical residual vector has SHA256
`cfd2939f15f8427c026363761e2082eae9ba4c4e920f455df2dca1b8822183bc`.

For H in Q0, L=0, h_K>=1 and x_e>=0. Therefore

```text
12 sum_{visible e} x_e >= 398,
sum_{visible e} x_e >= 199/6,
sum_{visible e} x_e >= 34 for integral edits.
```

In fact this certificate uses only twelve of the vertex-degree equations,
both neighborhood counts of root 0, and 54 of the 353 cover rows. This
exposes the coupling behind the bound; it is not another count-only cell
feasibility test. The other equations and all pointwise rows are unnecessary
for this lower bound but are satisfied by the sharpness witness.

## 4. An exact total-edit bound

The total certificate uses 183 K5 rows, 38 degree equations and five profile
equations. At scale D=1000 its positive clique weights sum to 50535. It
also has 57 nonnegative upper-box penalties p_e totaling 62. The checker
verifies nonnegative residuals r_e in the identity

```text
1000 sum_e x_e
  = sum_K a_K h_K(x) + sum_j b_j E_j(x)
    - sum_e p_e x_e + sum_e r_e x_e,
```

where E_j ranges over the specified vanishing degree/profile expressions.
Since 0<=x_e<=1, this proves sum_e x_e >= (50535-62)/1000 = 50.473.
Both graphs have the same number of red edges, so red deletions equal red
additions and their edge Hamming distance is even. Thus it is at least 52.
No optimal total distance is claimed. In particular, 52 is a lower bound,
not a discovered 52-edge witness or an exhaustive radius classification.

The scale-1000 data were obtained by rounding a numerical LP dual and then
repairing *every* overloaded edge by an exact upper-box penalty. This is
why the rational bound is slightly below the numerical LP optimum near
50.53375. The proof uses only integer sums and nonnegative residuals; the
numerical solver's status, tolerances, and optimality are not trusted.

## 5. Sharpness and the remaining gap

[`GRAPH.json`](GRAPH.json) is an explicit graph in Q. Direct checks give:

- 82 toggled central edges: 34 visible and 48 invisible;
- 41 red additions and 41 red deletions;
- all individual degrees, exceptional incidences and profiles retained;
- all 884 pointwise inequalities satisfied;
- all 176 red and 177 blue original obstructions destroyed;
- 15 changed signature-cell edge quotas.

Together with the visible lower bound this proves exact sharpness for Q0
and Q. However, the graph has **300 red and 321 blue new K5s**, of which
61 red and 95 blue meet E. Examples are red {0,3,20,23,36} and blue
{0,11,13,14,15}. There are also 36 failed central hard caps. It is not a
member of the preceding mixed-free family, not a candidate improvement,
and not the new campaign endpoint. The earlier 353-K5 graph is preserved.

This gives a useful exact interface for a subsequent graph-realization
phase: any finishing recoloring in this fixed-incidence/profile scope
must cross both edit lower bounds, and merely covering all original K5s
is insufficient. The next missing condition is prevention of newly created
obstructions across the simultaneously changed neighborhoods. No such
stronger search, new radius, or local descent was started in this milestone.
