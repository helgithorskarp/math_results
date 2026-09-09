# A quantitative restriction on the complete current q8 branch

Let good43 mean a red/blue coloring of the pairs of 43 vertices with no
monochromatic five-set. The standard R(4,5)<=25 implies that every vertex
has red degree in [18,24]: 25 neighbors of one color would contain either
a same-color K4, extended by the root, or an opposite-color K5. The same
argument applied to the other color gives the lower bound. No improvement
to this degree interval, h4009's edge window or h4015's path theorem is made.

## The exact physical branch

Use the q=8 branch of h3873, with h3887's additional whole-block order.
Blocks B_i={4i,...,4i+3}, i=0,...,7, are monochromatic K4s. Blocks i<r are
red and the rest blue, where r=5,6,7,8. The last eleven vertices are one
of all 546,356 catalog Ramsey(4,4;11) representatives. Every core is retained.
No symmetry of the full graph is required. All 800 unfixed physical pairs
belong to 28 four-by-four matrix coordinates and 88 four-bit star coordinates.

An ordinary block-pair matrix must avoid a monochromatic five-set in its
eight-vertex union. There are 37,823 same-color states and 35,714 opposite-
color states. At the red root block B0, nonincreasing child column signatures
leave 1,998 red-child states and 1,931 blue-child states. A block/core star
allows all four-bit words except the word entirely in the block's color,
giving 15 states. Each coordinate controls disjoint physical pairs.

Write a=r-1, b=8-r and

```
Q_r = 37823^(C(a,2)+C(b,2)) * 35714^(a*b) * 15^88.
D_r = 1998^a * 1931^b.
M_r = C(1998+a-1,a) * C(1931+b-1,b).
J_r = C(1998,a) * C(1931,b).
L_r = a! * b!.
```

The h3873 parent has T_r=D_r*Q_r graphs for each core. The **current h3887**
task has P_r=M_r*Q_r, because whole nonroot blocks of each color are ordered
by their root matrices. Ties are allowed and must be counted as multisets.
J_r*Q_r of the ordered graphs have distinct root matrices within each color.
CARRIER_PINS.json matches the four P_r values with h3887's committed registry.
The complete ordered q8 count is P8=546356*sum_r P_r.

These carriers can fail maximality or remaining five-set constraints.
Their previous complete physical encodings still retain every such constraint.
The present filtered set is a necessary superset of possible good43 models,
not a collection of known Ramsey candidates. Other q values are not processed.

## Exact parent marginals

In one fixed parent task choose all 116 coordinates independently and
uniformly from their allowed domains. For each block i select two positions
S_i inside its four vertices, and let E_i require both red degrees in [18,24].
For each core vertex v let F_v require its red degree in the same interval.
There are nineteen events in total. Every matrix coordinate belongs to
the events of its two blocks. Every star coordinate belongs to its block
event and its core-vertex event. Thus every coordinate is read exactly twice.

For a selected pair of block positions, each incident matrix has an exact
bivariate degree polynomial. Use row sums at its left endpoint and column
sums at its right endpoint, including the root ordering when applicable.
Multiply the seven matrix polynomials and eleven star polynomials. Add
fixed degree three for a red block or zero for a blue block. Summing the
coefficients in the target rectangle gives the exact marginal probability.
All six position pairs at each of eight blocks are computed for each r:
192 bivariate marginals. The minimizing choices are deterministic.

For r=5 the root uses positions (0,1), every other red block (0,3), and
every blue block (2,3). For r=6,7,8 the root uses (0,1) and every other
block uses (2,3). Thus choices are identical among nonroot blocks of the
same color, which is needed for the sorting transfer below.

A core vertex's external red degree is the sum of the popcounts of its
eight star words. Maximize its degree-window probability over every possible
fixed internal red degree d=0,...,10. Denote the maximum by c_r. This is an
upper bound for every core vertex in every catalog record; no record needs
to be opened and no independence between fixed core degrees is assumed.

If p_ri is the chosen exact block marginal, the certified product is
W_r=(product_i p_ri)*c_r^11. Every quantity is rational. The square-root
upper bounds u_r are rounded **up** to multiples of 2^-40, with u_r^2>=W_r
checked by integer multiplication. Decimal displays are not proof steps.

## The twofold product-space inequality

For completeness, let Omega be any finite product of coordinate domains,
and let A be the intersection of events whose input sets cover each
coordinate exactly twice. If A is empty the bound is immediate. Otherwise
let Z be uniform on A. The entropy chain rule and the fact that conditioning
cannot increase entropy give

```
2 H(Z) <= sum_events H(Z restricted to the event's coordinates)
       <= sum_events log(number of allowed assignments on those coordinates).
```

The first inequality follows by expanding each restricted entropy in a
common coordinate order and conditioning each term on all preceding
coordinates; every coordinate then occurs twice. The second bounds entropy
by the logarithm of support size. Since the full coordinate-domain sizes
also appear twice, exponentiation gives

```
(|A|/|Omega|)^2 <= product_events Pr(event).
```

This is the uniform finite read-two/Shearer inequality, a special case of
established product-measure inequalities. Here it bounds the parent degree-
event intersection by T_r*u_r. Degree-valid graphs are a subset of that
intersection. We do not assume the nineteen events are independent.

## Transfer to the current h3887 carrier, including root ties

The parent product measure is **not** the uniform measure on the sorted
carrier. Applying u_r directly to P_r would be unjustified. Whole-block
sorting preserves the selected degree event: root/core labels stay fixed,
and selected positions agree among every block of the same color.

When root matrices within each color are distinct, every sorted physical
graph has exactly L_r distinct parent labellings obtained by permuting the
whole blocks. The entire degree event is preserved by these permutations.
Thus the number of sorted degree-event graphs with distinct roots is at
most T_r*u_r/L_r. All sorted graphs with repeated roots number exactly
(M_r-J_r)*Q_r; we conservatively charge all of them as surviving.
Consequently each current task has at most

```
P_r * v_r,
v_r = u_r*D_r/(L_r*M_r) + (M_r-J_r)/M_r
```

degree-valid graphs. No assumption is made about automorphisms or equal-key
cross edges, and no independent reduction factors are multiplied. The
repeated-root term is essential. Finite controls demonstrate a concrete
failure of naive division by the block factorial and verify this safe bound.

The exact rational v_r have the following conservative decimal upper bounds:

| r | Parent u_r, approximate | Current v_r, rounded up |
|---|---:|---:|
| 5 | 0.046466915 | 0.05533 |
| 6 | 0.042396203 | 0.05315 |
| 7 | 0.039842988 | 0.05445 |
| 8 | 0.035463337 | 0.05590 |

Every v_r is below 1/16. The weighted complete q8 bound satisfies

```
sum_r 546356*P_r*v_r < (681/12500)*P8 < P8/18.
```

Its integer ceiling is below 2^748. EXPECTED.json contains all exact
probabilities and intermediate integer counts; SUMMARY.json gives the
full P8 and retained upper integer. These are upper bounds on retained
cardinality, not an exact enumeration of the remaining set.

## Physical interface and scope

degree_filter.py evaluates all 43 red degrees of a supplied complete graph.
Any failure gives 25 same-color neighbors. The program searches that set
for a same-color K4 or opposite-color K5 and returns a literal bad five-set
in the full graph. A separate verifier uses just the ten physical pairs
and graph hash, so a reported rejection does not depend on trusting the
degree theorem. A pass says only that all degrees lie in the allowed range.
This standard rejection mechanism is not claimed as new mathematics.

The count theorem applies to the subset accepted by this filter inside
the current q8 carrier. The interface accepts arbitrary complete graphs;
it does not certify carrier membership, find core representatives, enumerate
accepted graphs, or rewrite an owner's solver. No timing improvement is
measured. No task is declared UNSAT, including any q8 task.

h4009's 390..513 edge window and h4015's neighborhood theorem remain
accepted. Applying those conditions as well can only shrink the retained
set, but this package does not quantify another factor conditional on them.
The effect proved here is relative to the exact h3887 q8 carrier.

Trust includes the classical R(4,5) bound; h3873/h3887's coverage, catalog
completeness and physical injectivity; the elementary entropy and sorting
arguments; exact code, compiler/interpreter and hardware. Domain generation
and marginal arithmetic are independently checked. The proof is not
formalized, and no new external review or historical priority is claimed.
