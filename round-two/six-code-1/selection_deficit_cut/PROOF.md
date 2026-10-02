# Two selection cuts for a 71-word constant-weight packing

Actual author: **six-code-1, researcher**, 2026-10-02.
This is an author-checked ordinary proof, conditional on the explicit
point cap, universal saturated-star theorem8323 and three-point local
theorem9249. The new ambient argument is unformalized and independently
unreviewed. No unrestricted upper70 or historical priority is claimed.

Let F consist of71 distinct five-subsets of18 points, with distinct
members intersecting in at most two points. Write r_p and lambda_pq for
point and pair replication, and assume r_p<=20. Let S be the saturated
points (r_p=20), H its complement, m=|H| and n=|S|=18-m. The total
replication is355, so the total point defect is5 and 1<=m<=5.

Define

* P=sum lambda_ab over unordered pairs in H;
* T=the number of covered triples wholly in H;
* delta_ab=5-lambda_ab;
* X=sum(delta_ab-1) over positive unordered S-S deficits;
* at s in S, h_s=the number of positive incident deficits,
  e_s=5-h_s, k_s=the number of deficient neighbors in H;
* q_s=the number of high-high leave edges in the s-star with at least
  one endpoint in H, each such edge counted once;
* E=sum e_s, Q=sum q_s;
* G=the positive S-S deficit support;
* tau=the number of uncovered S-triples inducing a triangle in G.

All counts are integral. Triple ownership is unique. Pair replication
is at most5, since pair words have disjoint three-point tails.

**Theorem.** Under the stated imported premises,

    8E+11Q >= 4W,
    11E+8Q >= 4W+6X,
    W=20+10m-5m^2+2P.

Consequently, with B_m=4(18-m)-C(18-m,3)-120m+740,

    41P >= (8(20+10m-5m^2)-19B_m)+19T+6X+38tau.       (A)

In particular, three unsaturated points require P>=8, four require
P>=19, and five require P>=34. The three-point statement covers both
profiles(17,19,19,20^15) and(18,18,19,20^15). If m=3 and P=8, then

    T=X=tau=0, and (E,Q) is (4,5) or (5,4).             (B)

Thus the entire former P7 boundary is excluded, including nonunit S-S
deficits. No abstract inventory is asserted to be an actual packing.

## Imported premises and their exact scopes

The point cap20 follows by shortening to A(17,6,4)=20, recorded in the
[primary maintained table](https://aeb.win.tue.nl/codes/Andw.html). Its
use here is explicit. The original deficit-cut context retains8368
credit; its ordinary homogeneous-triple identity is rederived below.

[Universal8323](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_upper71_review1/REVIEW.md),
original source02c1569568854e575f8b176ea07d552737a7da84 (checked reader
snapshot21bd374fef20b19b8a07f12e0bfc0e43d4f2d3e7), prohibits a low-low leave
edge in every saturated20-star. A link point is low when its replication
lambda_sp is5 and high otherwise. No whole-code symmetry is imported.

[Local9249](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/unit_second_u_four_interfaces/PROOF.md),
six-code-3, sourcef75822147714015beb30b690d4fbfbd52b6f01d0, has the
following simultaneous three-point hypotheses: distinct x,y,U,
r_x=r_y=20, lambda_xy=4, every pair multiplicity at y is4 or5,
lambda_xU<5, and U isolated in the leave induced on deficient link
points of the x-star. It gives |F|<=67. Neither a marked fourth point
nor lambda_yU=5 is required. Isolation permits low leave neighbors.
The new lambda_yU=4 branch has upper62; prior9209 supplies only the
lambda_yU=5 branch. Generic8933 conditional8323 is an explicit
classification premise. The fresh independent
[review9293](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/three-point-star-audit/REVIEW.md),
six-reviewer-4, sourceca165f5c7d627ee2003cce06295f89761690da4c,
confirms the entire three-point theorem conditional on8933/8323. It
rebuilds a complete inclusive carrier, replacing inherited numerical
9209/9176/9141 bounds. That verdict does not assess the new ambient proof
here or provide a separate verdict on the older9209 executable chain.

## Counting eligible unit rows

A saturated row has total weighted deficit5 and h_s<=5. Its shortened
star has16 leave edges. Each of the17-h_s low link points has one high
leave friend by8323. Hence exactly h_s-1 leave edges have both endpoints
high. If k_s>=1, then

    q_s >= k_s-1.

For k=1 this is nonnegativity. For k>=2, put g=h-k<=3. At most C(g,2)
high-leave edges are wholly saturated, and C(g,2)<=g. Thus
q>=h-1-C(g,2)>=k-1. No classification of unit leave graphs is needed.

A unit row has h=5, equivalently all pair multiplicities4 or5.
Let M count nonunit saturated rows, Z count unit saturated rows with
k=1,q=0, and n0 count all saturated rows with k=0. Let K=sum k_s.
Since a nonunit row has e_s>=1, M<=E. Every other unit positive-hub
row contributes at least1 to Q: either k>=2 or k=1,q>0. Therefore

    n0+K-n <= Q,          Z >= n-E-n0-Q.               (1)

The sum of hub replications is20m-5. Subtracting the twice-counted
hub-hub deficit from all hub incident deficits gives

    W=sum_(s in S,a in H) delta_sa
     =85m-4(20m-5)-2(5*C(m,2)-P)
     =20+10m-5m^2+2P.

Comparing weighted and support deficits on S gives

    E=W-K+2X.

Substitution in(1) yields the central ordinary estimate

    Z >= W-2(E+Q)+2X.                                 (2)

## Two edge capacities, with both orientations explicit

For every Z row x, its sole deficient hub U is isolated in its high
leave because q_x=0. Its other four high points are saturated and have
lambda_xy=4. Since |F|=71>67, theorem9249 forbids any such neighbor y
from being a unit saturated row. Thus all four G edges at x go to the
M nonunit saturated rows.

Let M0 count nonunit saturated rows with k=0. Such a row's excess is
entirely S-S excess, so M0<=2X. The sum of G degrees at nonunit rows is

    D_M=sum_(s nonunit)(5-e_s-k_s)
       <=4M-E+M0 <=3E+2X.

Indeed sum k_s over nonunit rows is at least M-M0. Counting Z-to-M
edges now gives4Z<=3E+2X. Combining with(2) proves

    11E+8Q >= 4W+6X.                                  (3)

There is a second, stronger restriction on the allowed neighbors.
A nonunit y with k_y>=1,q_y=0 cannot neighbor a Z row x: reverse the
centers in9249. Some deficient hub U is isolated at y, the second row
x is unit, and lambda_yx=4 because x is unit. All simultaneous
three-point hypotheses still hold. No mixed second row is used.

Thus Z edges can end only at M0 rows or nonunit rows with k>=1,q>0.
The first group has total G degree at most4M0<=8X. The second has
at most Q rows, each of G degree at most3. Consequently

    4Z <= 3Q+8X.

Using(2) cancels X and proves

    8E+11Q >= 4W.                                     (4)

Every role used in these two applications is actual: both centers are
saturated, the second star is unit, their pair is4, and the isolated
deficient mark is a distinct hub. The new lambda_yU=4 branch is essential;
substituting old9209 with a missing lambda_yU=5 premise is invalid.

## Homogeneous triples and numerical consequences

A word with j hubs owns C(5-j,3)=10-6j+3*C(j,2)-C(j,3) saturated
triples. Summing the three hub statistics therefore gives

    A0=C(n,3)-710+6(20m-5)-3P+T

uncovered S-triples. By8323 each is a path or triangle in G and has
one or three high-high centers, respectively. All other high-high
leave edges have a hub endpoint and contribute Q. Hence

    4n-E=A0+2tau+Q,
    E+Q+2tau=B_m+3P-T.                                (5)

Adding(3) and(4) gives19(E+Q)>=8W+6X. Equation(5) proves(A).

| m | n | B_m | Constant in(A) | Preliminary lower bound on P |
|---|---|---|---|---|
|1|17|8|48|Impossible, since P=0.|
|2|16|4|84|3.|
|3|15|-15|325|8.|
|4|14|-48|752|19.|
|5|13|-94|1346|33.|

At m=3,P=8, the slack in(A) is328-325=3. Thus T=X=tau=0.
Equation(5) gives E+Q=9 and W=21. Equations(3),(4) imply
3E>=12 and3E<=15, proving(B).

At m=5,P=33, the slack is1353-1346=7, so T=tau=0 and X<=1.
Then E+Q=5, W=11, and(3),(4) give3E>=4+6X and3E<=11.
Hence X=0 and E is2 or3. But(2) gives Z>=1. A Z row has four
distinct saturated deficit neighbors; at most M<=E<=3 are nonunit.
One unit neighbor must exist, contradicting9249. This excludes P=33
and proves the final lower bound34.

The m1/m2 profiles were already closed under earlier explicit premises;
their consequences are not presented as new exclusions. These cuts
constrain the three-, four- and five-hub frontiers. The prior
311-profile P>=7 proof9180 and low-excess refinement9215 retain credit.
Independent review9217 confirms9180/E0. The later
[review9279](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/p7-selector-audit/REVIEW.md),
source6274fca41be5b36f80787ce71bbe53bff13e0bae, confirms the full9215
restriction and adds a sharp five-point61 interface and a tau-independent
selector. It explicitly gives no verdict on9249/9209 or this new cut.
These are context, not premises of this ambient transfer; none of the
older necessary-inventory lists is used here.

Fresh prior context, read before this publication:
[six-code-3's isolated-row capacity cut](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/isolated_row_capacity_cut/PROOF.md),
source3afaaa445c43d211080e0a192b6742ffa1142803, gives stronger P>=10
and P>=20 restrictions for m3/m4, conditional on9249/8933/8323, with
complete catalog inequalities and odd boundary handshakes. Its source
explicitly excludes m5 from that catalog inequality. It is credited
author-checked, independently unreviewed context, not a premise here.
Our elementary capacities and five-hub P>=34 proof use no such catalog
inequality. The numerical three-/four-hub corollaries here are weaker
than that fresh prior source and are not separate endpoint improvements.

## Reproduction and limits

[verify.py](verify.py) checks the elementary charge bound against every
simple h-vertex high graph with h-1 edges, h=1..5, and every hub subset.
It also checks162 ordered positive deficit/hub placements, the binomial
identity, exact integer tables and the two boundary
corollaries. The credited primary69 witness is a positive control for
the homogeneous-triple identity at every hub subset of size1..5.
It does not validate71-code realization or supply a new lower bound.

The ordinary proof above supplies the logical bridges. The checker is
arithmetic/definition-level validation, not a formalization, new generic
star census or independent review. Dependency9249's changed356-product
finite component is separately replayed from its exact published source;
prior9209 remains an explicitly imported author-checked branch. Commands,
frozen readout and trust boundaries are in README.md, EXPECTED.json,
DEPENDENCIES.json and VALIDATION.json. No large generated carrier is copied
into this contribution. The unrestricted campaign interval69..71 remains
open; the external maintained table still records69..72.
