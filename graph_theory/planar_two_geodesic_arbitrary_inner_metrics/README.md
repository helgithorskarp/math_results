# Two-geodesic necklace separators with arbitrary inner lengths

A necklace with at least four branches, uniform wheel and cross-edge
lengths, and **arbitrary positive inner edge lengths** half-balances
every nonnegative vertex mass by two ambient geodesics, under the
attachment assumptions below. No comparison between different inner
arc totals is required. The proof combines the new quantitative lemma
here with the earlier [all-long theorem](../planar_two_geodesic_metric_necklaces/README.md).

The new lemma permits all but one inner arc to have unrestricted length.
The remaining arc is short and determines the admissible anchor. Its
proof repairs an A-step even when neither parent can be appended to the
usual inner carrier. At a D-step, a clipped distance threshold replaces
the former short-arc/long-arc case distinction.

This is a conditional structural result relevant to the exact half
threshold in [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).
It does not resolve the unrestricted planar question. The underlying
unit-edge necklace existence cases were already covered by the earlier
work; the advance here is the continuous metric region and its proof
mechanism. Independent review of this extension is pending.

## Statement and scope

Let t>=3. The core H consists of a root r, the outer cycle

```
a_0,b_0,a_1,b_1,...,a_(t-1),b_(t-1),a_0,
```

all root-to-outer spokes, branches c_0,...,c_(t-1) with outer neighbors
exactly a_j,b_j, and an inner path T_j from c_j to c_(j+1). Inner paths
have mutually disjoint degree-two interiors. Every wheel and cross edge
has length lambda>0. Individual inner edges have arbitrary positive
real lengths; write ell_j for the total of T_j. Indices are cyclic.

Let a finite connected simple positive-edge graph G contain H induced
and isometrically. Every component K of G-V(H), including zero-mass
ones, has boundary contained in {r}, {r,u}, or {r,u,v} for consecutive
outer vertices u,v. There are no inner attachments. Full-G planarity
is not required for this conditional result; the core is planar.

Suppose only that

```
ell_(t-1) <= lambda.                                    (1)
```

There is no restriction on any other ell_j. The designated triple is
S0={r,a_0,c_0}. For nonnegative real vertex masses of total W define

```
Y(K) = N(K) intersect the outer vertices;
D0 = sum w(K) over Y(K) empty or {a_0};
B = max_K w(K), with default zero;
M = W-w(S0)-D0,          h=max{M/2,B}.
```

**Quantitative lemma.** Two shortest paths in the original G collectively
contain S0 and leave every component of mass at most h. No treewidth
condition or maximum-sector choice is required for this bound. The
geodesic (r,a_0,c_0) need not remain an entire selected path.

Rotation and reflection allow any branch/parent triple for which the
arc preceding that parent in the displayed orientation satisfies (1).
We do not assert the bound for every prescribed anchor in every mixed
metric. In particular, arbitrary inner totals do not imply (1) for a
preselected triple.

**Arbitrary-inner-metric corollary.** Suppose t>=4 and each induced torso
G[K union N(K)] has treewidth at most three. With completely arbitrary
positive inner edge lengths, every nonnegative real mass has an exact
half separator equal to the union of at most two original-G geodesics.
The anchor may be selected from the metric and may change in the
heavy-attachment case.

Indeed, if an arc total is at most lambda, rotate/reflect to use it in
(1). If no such arc exists, all arc totals exceed lambda, and the
previous all-long theorem applies. If B<=W/2, either quantitative bound
is at most W/2. A component K heavier than W/2 is handled by the reviewed
width-three torso/centroid argument: a bag of at most four vertices cuts
the heavy torso appropriately and two ambient geodesics cover that bag.
See the [attachment review](../planar_two_geodesic_prescribed_attachment_review1/REVIEW.md);
the exact committed dependency is
`bafkreicahkd2dmvwewqdwfn2vjrzwh5p7jke46lh7q3oacii5iyfxkwkqu`.
The new proof below needs neither that heavy-case argument nor its
treewidth assumption for the quantitative lemma.

The statement does not permit arbitrary wheel/cross lengths, mass at
new subdivision vertices on those edges, inner attachments, or arbitrary
planar cores. It does not give a t=3 arbitrary-metric corollary by appeal
to the earlier all-long theorem, which requires t>=4.

## Exact distance profiles

Let delta(u,v) be distance in the intrinsic weighted inner cycle, which
need not be isometric in H. Put delta_j=delta(c_0,c_j), L_cyc=sum ell_j,
and write d for the ambient distance. The wheel is isometric: any inner
excursion between outer vertices uses two cross edges and costs at least
2lambda, at least their wheel distance. Replacing subsequent excursions
by wheel routes and inspecting the first cross exit gives, without (1),

```
d(c_0,a_j)=lambda+min{delta_j,lambda+delta_(j-1),2lambda};
d(c_0,b_j)=lambda+min{delta_j,lambda+delta_(j+1),2lambda}.
                                                               (2)
```

The three candidates are an inner route exiting at c_j, one exiting at
the relevant neighboring branch followed by an outer edge, and a route
through the root. Every other first exit costs at least 3lambda. Each
candidate which realizes the minimum is attainable. The exceptional
coincident endpoints have the cheaper direct cross edge.

Condition (1) gives the essential anchored profile

```
d(a_0,c_j)=lambda+min{delta_j,2lambda}.                  (3)
```

To prove it, apply the same first-entry argument starting at a_0. Entry
at c_0 costs lambda, at c_(t-1) costs 2lambda, and every other branch
costs at least 3lambda. Since
delta_j<=ell_(t-1)+delta(c_(t-1),c_j)<=lambda+delta(c_(t-1),c_j),
the second entry cannot improve the first; the root gives the cap.
This proof allows all the other arc totals to be arbitrary.

Also d(r,c_j)=2lambda. At a D-step from (b_j,c_j) to
(a_(j+1),c_(j+1)), put

```
k=min{lambda,ell_j,L_cyc-ell_j}.
d(b_j,c_(j+1))=d(a_(j+1),c_j)=lambda+k.                (4)
```

Here the outer-edge route costs 2lambda; the other possibility is one
cross edge plus an intrinsic inner shortest route. Other outer entries
cannot improve these. Core isometry transfers all formulas to G.

For an arc T=(v_0=c,...,v_n=d) of length ell, let z_i be cumulative
length, with 0=z_0<...<z_n=ell. If a specified shortest u-to-c path
avoids T's interior, its extension to v_p is geodesic exactly when

```
2z_p <= ell+d(u,d)-d(u,c).                              (5)
```

Reverse the inequality for extension from d. All paths below enter an
arc only at its endpoints. The non-strict comparisons include ties and
arbitrary gaps between consecutive vertex coordinates.

## Sweep and component bounds

Set o_(2j)=a_j and o_(2j+1)=b_j. Partition the represented vertices of
mass M into the disjoint groups

```
alpha_i: o_i and all K with Y(K)={o_i}, for i!=0;
gamma_j: {c_j}, for j!=0;
kappa_i: all K with Y(K)={o_i,o_(i+1)};
tau_j: interior vertices of T_j.
```

The zero-index alpha and gamma groups are empty. At state (i,j), set

```
L(i,j)= union_(s<i)(alpha_s union kappa_s)
        union union_(h<j)(gamma_h union tau_h);
R(i,j)= represented vertices minus L(i,j),alpha_i,gamma_j.
```

Indices wrap at the final state. Deleting (r,a_0,c_0) and
(r,o_i,c_j) at the incident states leaves every component meeting H
inside L(i,j) or R(i,j). Other components are individual whole K, of
mass at most B. The two spokes are ambient geodesics.

For completeness, removing outer and inner sites cuts both cycles into
matching intervals; each cross edge stays within a matching interval.
An outside K cannot bridge cuts because its outer sites are at most two
consecutive vertices. If all its boundary is removed, it detaches as one
whole K. This also proves the bounds below, and additional core deletions
only split components.

Sweep through A-steps (a_j,c_j)->(b_j,c_j), then D-steps
(b_j,c_j)->(a_(j+1),c_(j+1)). The left mass increases and right mass
decreases from (0,M) to (M,0), with their sum at most M<=2h. If no
spoke pair has both sides light, choose the first transition with new
left mass >h. Its old right mass is also >h. Its old left and new right
sets, denoted below by L,R, are light. We construct either one pair
leaving only those light sets, or two alternative pairs whose potentially
heavy supports are disjoint subsets of M. Two disjoint supports cannot
both exceed h.

At an A-step, removing S0,a_j,b_j,c_j leaves only L,R and individual K.
At a D-step, removing S0 and both outer sites together with a suffix
v_q,...,v_n leaves core components in

```
L union gamma_j union {v_1,...,v_(q-1)},       R.         (6)
```

Removing a prefix v_0,...,v_p gives

```
L,       R union gamma_(j+1) union {v_(p+1),...,v_(n-1)}.(7)
```

Removing the whole arc but just its new outer site instead gives
L union alpha_i union kappa_i, R, where i=2j+1. With just the old
outer site it gives L, R union alpha_(i+1) union kappa_i. These bounds
include the seam, with its empty zero-index groups.

## A-steps, including bypassed parents

Let I_j be an intrinsic inner shortest c_0-to-c_j route. For j=0 use
(r,a_0) and (c_0,b_0). For j>0 proceed as follows.

If delta_j>=2lambda, (3) makes (a_0,r,a_j,c_j) geodesic. Pair it
with any shortest c_0-to-b_j path from (2). This removes both parents,
c_j and S0, so all residual core components lie in light L,R.

Suppose delta_j<2lambda. If I_j followed by b_j is shortest, use it
with (a_0,r,a_j). Otherwise, if I_j followed by a_j is shortest,
use it with (a_0,r,b_j). The wheel complements have length 2lambda.
The only possibly adjacent exception in the second pair is j=t-1;
there delta_j<=ell_(t-1)<=lambda, so the first choice is already
shortest by (2). Thus this exception does not occur.

It remains that **neither parent can be appended**. By (2),

```
delta_j>lambda+delta_(j-1),
delta_j>lambda+delta_(j+1).                             (8)
```

Both neighboring deltas are below lambda. Also j!=t-1 by (1).
The inner route I_j enters c_j through one of its two incident arcs.

If it enters through T_(j-1), write I_j=I_(j-1) followed by that whole
arc. Equation (8) makes the detour

```
J=I_(j-1), b_(j-1), a_j
```

shortest, of length delta_(j-1)+2lambda. Compare the two pairs

```
J,                (a_0,r,b_j);
(a_0 followed by I_j),       (r,b_j).                   (9)
```

The second anchor path is geodesic by (3). The first pair removes both
parents and c_(j-1), leaving its only possibly heavy core support inside

```
H1=R union gamma_j union tau_(j-1).
```

The second removes c_j, b_j, and the entire T_(j-1); its only possibly
heavy support is inside

```
H2=(L minus tau_(j-1)) union alpha_(2j) union kappa_(2j).
```

The other components lie in L or R or are whole K. H1,H2 are disjoint:
the inner arc which the first pair leaves attached to c_j is entirely
deleted by the second pair. Hence one pair works.

If I_j enters backwards through T_j, use instead

```
J=I_(j+1), a_(j+1), b_j;
J,                (a_0,r,a_j);
(a_0 followed by I_j),       (r,a_j).                  (10)
```

The potentially heavy supports are respectively

```
H1=L union gamma_j union tau_j;
H2=(R minus tau_j) union alpha_(2j+1) union kappa_(2j).
```

They are disjoint for the same reason. All paths in (9),(10) are
shortest by (2),(3) and wheel isometry. Inner route ties may be resolved
either way, as long as its actual entering arc is used consistently.
This proves every A-step without a condition on its two incident totals.

## D-steps with clipped thresholds

At a D-step write a=b_j, b=a_(j+1), c=c_j, d=c_(j+1),
x=delta_j, y=delta_(j+1), and ell=ell_j.

First suppose x,y>=2lambda. Both root carriers
(c_0,a_0,r,a) and (c_0,a_0,r,b) are shortest by (2). With k from (4),
choose q first with 2z_q>=ell-k and p last with 2z_p<=ell+k. Compare

```
(c_0,a_0,r,a),     (b,d,v_(n-1),...,v_q);
(c_0,a_0,r,b),     (a,c,v_1,...,v_p).                  (11)
```

The second paths are shortest by (4),(5). Since q<=p+1, their potentially
heavy supports from (6),(7) are disjoint. The other sides are L,R.

Now suppose min{x,y}<2lambda. If x<=y, an inner shortest I_j avoids
the current arc: traversing it from d would have cost strictly greater
than y. By (2), I_j followed by a is geodesic. Compare first

```
I_j followed by a,           (a_0,r,b).                 (12)
```

Its only possibly heavy support is H1=R union gamma_(j+1) union tau_j.
The closing step cannot occur here, since there y=0<x. The wheel path
is therefore shortest. By (3),(5), the anchor path starting a_0,c_0
and following I_j extends through a prefix with

```
2z_p <= theta=ell+min{y,2lambda}-x.
```

Here theta>=ell. Take the last such p and the first q with 2z_q>=ell.
Then q<=p+1. The pair

```
(a_0 followed by I_j, v_1,...,v_p),
(r,b,d,v_(n-1),...,v_q)                                (13)
```

is geodesic by (3),(5) and d(r,c)=d(r,d)=2lambda. It covers every
vertex of the current arc and the new outer site. Its only possibly
heavy support is H2=L union alpha_i union kappa_i. H1,H2 are disjoint.
This proves the case whether the current arc is short, long, dominant,
or crossed by the intrinsic antipode.

If x>y, reverse the construction. Use I_(j+1) followed by b, with
(a_0,r,a), except that at the closing step the latter path is simply
(r,a), because the former already contains a_0. The first step cannot
occur in this case. Its potentially heavy support is
H1=L union gamma_j union tau_j. For the split pair choose q first with

```
2z_q >= theta=ell+y-min{x,2lambda},
```

and p last with 2z_p<=ell. Now theta<=ell and q<=p+1. Use

```
(a_0 followed by I_(j+1), v_(n-1),...,v_q),
(r,a,c,v_1,...,v_p).                                   (14)
```

Its potentially heavy support is H2=R union alpha_(i+1) union kappa_i,
disjoint from H1. The same distance and component arguments apply.
All coordinate thresholds lie in [0,2ell] by the triangle inequality
in (5), so the indicated endpoints exist. This completes the quantitative
proof and hence the arbitrary-inner-metric corollary.

## Exact finite checks and trust boundary

Python 3.11+, standard library, assertions enabled; from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_arbitrary_inner_metrics/verify.py --check
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_arbitrary_inner_metrics/audit.py
```

The main checker uses Fraction arithmetic, whole-graph exact distances,
actual components, disjoint support sets, sphere incidence and attachment
decompositions. It checks every displayed path and component bound on
the documented fixtures, rotates/reflects through all anchors satisfying
(1), and checks the quantitative mass choices and the inherited heavy-K
repair. It imports earlier graph builders and mass-selection helpers.
Its seeded extra core models test geometry and support containment only.
The complete expected counts are in [expected.json](expected.json).
There are eight attachment fixtures with 40 admissible anchor orientations,
100 further core models, 3,947 checked component cuts and 9,290 mass
checks. The new A-step alternatives occur 17 times; D-step disjoint-support
checks occur 758 times. The main seed is 2026092925.

The separate audit rebuilds named graphs and computes Floyd distances;
it imports no research implementations. It constructs local path banks
by exhaustive shortest-path recursion between the specified local
endpoints, deduplicates vertex sets, and derives critical supports from
actual components, rather than the proof's coordinate or side formulas.
Its finite models differ from the main checker and do not reproduce the
main case stream entry by entry. Literal controls check the two parent
bypasses which invalidate the naive appended-parent route. This is a
separate check by the same researcher, not independent peer review.
With seed 2026092926 it checks 240 models and 2,640 local steps: 2,318
have a single sufficient pair and 322 use two disjoint supports. It
examines 81,810 distinct admissible pair unions in those local banks.

For the literal previous-arc control take t=4, lambda=12 and inner edge
lists `(1),(6,6,6),(6,6,6),(1)`. At c_2 the inner route has length 19,
but appending either parent gives length 31 against distance 25. Give
mass 3 to the first interior vertex of T_1, mass 3 to the singleton
attachment on `{r,a_3,b_3}`, and mass 4 to the singleton attachment on
`{r,a_2,b_2}`. Thus W=M=10, B=4 and h=5. The first pair in (9) leaves
residual mass 6; the second leaves 4. Replacing T_0's length by 2 and
using the reversed inner arrival gives the next-arc control in (10):
the inner route still has length 19, both parent appends still fail,
and the analogous masses give residuals 6 and 4. The precise labeled
paths and masses are in `audit.py`.

The arbitrary-order, arbitrary-real-length and all-real-mass statements
rest on the written proof. The finite checks are regression evidence.
No solver, proof assistant, external dataset or omitted large artifact
is required. The arbitrary-metric half corollary additionally uses the
earlier all-long and heavy-torso results.

## Priority boundary

The [official schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html)
announces Pilipczuk's disproof of a Codsi conjecture concerning balanced
planar separators. A bounded primary-source refresh on 2026-09-29 did
not identify its exact statement or witness. This note does not assert
that the posted Problem 31 is still open, claim historical priority, or
identify that talk with a proved resolution of the stated target.
