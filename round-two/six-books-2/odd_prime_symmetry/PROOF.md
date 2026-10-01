# Ordinary order-seven obstruction and the remaining odd primes

Author: **six-books-2**, role **researcher**, 2026-10-01.

Let G be a simple red graph on22 vertices, with nonedges blue. Suppose
every red edge has at most three common red neighbors, every blue edge
has at most six common blue neighbors, and the maximum red degree is
at most ten. Books are ordinary, noninduced subgraphs; no condition is
imposed on edges among their pages.

**Ordinary conditional theorem.** G has no automorphism of order7,13,17 or19.
This ordinary proof uses only the stated maximum degree and page caps.
In particular, its order-seven case does not import the global
minimum-eight theorem, a spectral classification or a host census.

Together with the [ordinary order-eleven theorem](../order_eleven_correlation/PROOF.md)
(committed8767, source9d661fd0ac14a412f84c59a1cfa0315e73ada374), this
shows that |Aut(G)| has the form2^a3^b5^c for nonnegative integers a,b,c.

**Credited global corollary.** For every22-vertex (B4,B7)-free graph,
|Aut(G)|=2^a3^b. The [upper-ten degree theorem](../../../book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md)
(committed8012, sourcece3177a731086284ee89f18a8a3948b672b3c64e) supplies
the degree hypothesis. The [previous order-five exclusion](../order_five_four_cycles/PROOF.md)
and [its fixed-point cases](../order_five_four_cycles/FIXED_POINTS.md)
(committed8711, sourceb654bc6d037ce9f899eed2c4e04f045137944307) remove
prime5. The latter predecessor imports its finite phase proof, a regular
codegree result, and the historical-classification-dependent global
minimum-eight corollary. Those are inherited by this **combined global
corollary**, not by the new conditional order7/13/17/19 proof.

Every orbit of the full automorphism group of a valid22 graph therefore
has size in {1,2,3,4,6,8,9,12,16,18}. This is a necessary construction
restriction, not a classification of the hosts. The Ramsey endpoint
remains open, with the located interval22..23.

The small cases and their coverage are written below. Computation
validates the arithmetic and explicit books; no computational execution
is a premise of the ordinary theorem. The proofs are not formally
mechanized and independent review of the new theorem is pending.

## 1. One seven-cycle and fifteen fixed points

An order-seven permutation on22 points has7^k1^(22-7k), k=1,2,3.
A fixed point is uniformly red or blue to each whole seven-cycle.
Maximum degree ten allows it to join red to at most one cycle.

For k=1 let R be the fixed points red to the cycle and L those blue to
it. A blue pair in L would have all seven cycle vertices as blue pages,
so L is a red clique. The red cap three forbids a red K6, hence |L|<=5
and |R|>=10. A cycle vertex has red degree |R| plus its internal degree.
Maximum ten forces |R|=10, |L|=5 and no internal red edges. Any blue pair
inside the cycle now has five blue pages inside it and five in L. This
violates the blue cap six.

## 2. Two seven-cycles and eight fixed points

For k=2 partition fixed points into R_A,R_B,L according to a red join
to cycle A, a red join to B, or neither. A blue fixed pair must have one
endpoint in R_A and one in R_B: every other pairing shares a whole blue
seven-cycle. Thus R_A,R_B are red cliques and L is red to all other fixed
points. If either R_A or R_B were empty all eight fixed points would
form a forbidden red clique, so their sizes a,b are positive.

Put z=|L|. At a point in R_A, degree is at least7+(a-1)+z; similarly
it is at least7+(b-1)+z in R_B. Hence a+z<=4,b+z<=4. With a+b+z=8,
these inequalities force z=0,a=b=4. All joined fixed points already have
degree ten, so all R_A--R_B pairs are blue. An internal red pair in A
would have four common red pages in R_A. Thus A is independent in red,
and likewise B. A blue pair in A has five blue pages in A and four
in R_B, again violating cap six.

## 3. Three seven-cycles: the fixed point and degrees

For k=3 there is one fixed point x. Its red degree is a multiple of
seven and at most ten, hence zero or seven. Degree zero is impossible:
any blue pair x,v has20-d(v)>=10 common blue neighbors. Thus x is red
to exactly one cycle, called A, and blue to the other cycles B,C.

Use Z7 coordinates on all three cycles, incremented by the same
automorphism. Internal red connection sets D_A,D_B,D_C are inverse-
symmetric, exclude zero, and have even sizes s_A,s_B,s_C. Let P,R,Q
be arbitrary oriented cross connection sets A to B, A to C, B to C.
Their cardinalities are m,n,q. Reverse connections use -P,-R,-Q;
no inverse symmetry of cross sets is assumed.

For a set T in Z7 put r_T(k)=|T intersect(T+k)|. It is symmetric in k,
and its sum over six nonzero shifts is |T|(|T|-1).

At a red spine x,a, the number of red pages is s_A, so s_A<=3 and
s_A is0 or2. At a blue spine x,b, its blue pages are precisely the
6-s_B internal blue neighbors of b in B and its7-q blue neighbors
in C. Therefore s_B+q>=7. Full degree d_B=s_B+m+q<=10 then gives
m<=3. Similarly n<=3 and s_C+q>=7.

If s_A=0, a blue pair inside A has

    5+(7-2m+r_P(k))+(7-2n+r_R(k))>=19-12=7

blue pages, impossible. Thus D_A={+/-a}, a!=0, and A is a red C7.
Write t=m+n and

    L(k)=r_DA(k)+r_P(k)+r_R(k).

Internal red spines in A have one fixed red page x and L(k) other
pages, so L(k)<=2 on the two shifts in D_A. Internal blue spines
have20-2(3+t)+1+L(k)=15-2t+L(k) blue pages, so L(k)<=2t-9 on the
other four shifts. Summing gives

    2+m(m-1)+n(n-1)<=4+4(2t-9),
    m^2+n^2-9(m+n)+34<=0.                         (1)

For integers0<=m,n<=3, the quadratic decreases in each variable.
Outside(m,n)=(3,3), its minimum is attained at(2,3) or(3,2), where it
equals2. At(3,3) it equals-2. Hence m=n=3 and d_A=9. The inequalities
s_B+q>=7 and d_B=s_B+q+3<=10 are equalities; likewise for C. Consequently

    d_B=d_C=10, s_B=s_C=s, q=7-s, s in {0,2,4,6}. (2)

No global minimum degree or total-edge bound was used. The forced
degree pattern is(7;9^7;10^14), with105 red edges.

In coordinates a,2a,3a, the correlations of D_A={+/-a} are(0,1,0).
Thus the remaining internal A bounds are

    (r_P+r_R)(a,2a,3a) <= (2,2,3).                (3)

## 4. Three-element sets and the outside internal degrees

For any three-set T in Z7, the vector r_T(1,2,3) is one of

    (2,1,0), (0,2,1), (1,0,2), (1,1,1).           (4)

This has an ordinary classification proof. If two unordered pairs have
the same difference class, their shared endpoint makes the three points
an arithmetic progression h+{-d,0,d}. Its correlations are2 at class d,
1 at class2d, and0 at the remaining class3d. The three possible step
classes give the first three vectors in(4). If there is no repeated
class, the three unordered pairs occupy all three classes once, giving
(1,1,1). Arithmetic progressions have a unique center in Z7, giving
21 such sets; the other14 sets give(1,1,1). This accounts for all35
sets without a host classification.

For an internal B spine the common red count is r_DB+r_P+r_Q. The
fixed point x contributes zero. Since d_B=10, a blue B spine has the
same number of blue pages as this red common-neighbor count. Summing
the red cap3 and blue cap6 over its six shifts gives

    s(s-1)+6+q(q-1)<=3s+6(6-s).

Together with(2), the complete table is

| s | q | left side | right side |
|---:|---:|---:|---:|
| 0 | 7 | 48 | 36 |
| 2 | 5 | 28 | 30 |
| 4 | 3 | 24 | 24 |
| 6 | 1 | 36 | 18 |

Only s=2,4 remain. The same calculation holds for C; reversal of Q
does not change its correlations.

## 5. Outside C7s are impossible

Suppose s=2, so D_B={+/-b} and D_C={+/-c}. Put T=Z7 minus Q, a
two-set. Then r_Q(k)=3+r_T(k) for k!=0. At the red B shift b,
r_DB(b)=0, so the red cap forces

    r_P(b)=r_T(b)=0.

By(4), P is an arithmetic progression of step class2b, with correlations
(0,2,1) in coordinates b,2b,3b. At the blue shift2b, the bound six reads
1+2+3+r_T(2b)<=6, so r_T(2b)=0. The one nonzero difference class of T
must therefore be3b.

Repeating in C, using -Q and -T, gives step class2c for R and difference
class3c for the same two-set correlation. Hence c=+/-b. The vectors of
P,R are equal and their sum is4 at class2b. This violates(3), whose
bound is at most three at every nonzero class. Thus s=2 is impossible.

## 6. Outside complements of C7: forced step classes

Suppose s=4. Write

    D_B=Z7 minus {0,+/-b}, D_C=Z7 minus {0,+/-c}.

In coordinates b,2b,3b, the correlations of D_B are(3,2,1). Equality
in the displayed s=4 budget forces every internal B bound to be an
equality, so

    (r_P+r_Q)(b,2b,3b)=(3,1,2).                   (5)

Substituting the four vectors in(4), the only way to obtain(3,1,2)
is(2,1,0)+(1,0,2). Thus P,Q are arithmetic progressions of step classes
b and3b, in some order. Similarly R,Q have step classes c and3c.

If b=+/-c, P and R have the same step class and their correlation sum
has a4, again contradicting(3). Otherwise P,R have distinct step classes
and Q has the remaining class: there are only three classes altogether.
In coordinates a,2a,3a, the sums of two distinct progression vectors are

    (2,3,1), (3,1,2), (1,2,3).

Only the last satisfies(3). Hence P,R have steps2a,3a and Q has step a.
Exchange B,C if necessary so P has step2a. Equation(5) then gives
b=+/-2a and c=+/-a. Multiply every coordinate by a^{-1} to make a=1.

Independent translations of B,C make the unique centers of P,R zero,
leaving a free center h for Q. This preserves every page cap and retains
every phase. The entire remaining family is therefore

    D_A={1,6}, D_B={1,3,4,6}, D_C={2,3,4,5},
    P={0,2,5}, R={0,3,4}, Q=h+{0,1,6}, h in Z7.   (6)

The normalization used units, orbit exchange and translations only.
It did not assume symmetric cross masks initially; their arithmetic
progression forms were forced by the bounds.

## 7. An ordinary phase obstruction and an explicit blue book

Consider a red A--C spine a_0,c_k, where k is in R. Its common red
neighbors within A and C number exactly two for each k=0,3,4, by the
displayed masks. Its remaining pages lie in B and number

    |P intersect(k-Q)|=|P intersect(k-h+{0,1,6})|.

For P={0,2,5}, the latter count as a function of t=k-h is

    f(0,1,2,3,4,5,6)=(1,2,1,1,1,1,2).

The red cap three therefore requires k-h not in {1,6} for all k in R.
But R+{1,6}={1,2,3,4,5,6}. All nonzero h are excluded, so h=0.

Now a_0,b_1 is blue. It has two common red neighbors in A, three in B
and one in C, for a total of six. Their degrees are9 and10, so their
common blue count is20-9-10+6=7. Explicit blue pages are

    a_2,a_4,a_5,b_3,b_6,c_5,c_6.

This is a literal B7, completing the order-seven exclusion. For
supplementary validation, [phase_books.json](phase_books.json) lists
one explicit B4 or B7 for each of the seven phases, using vertex
numbers A=0..6,B=7..13,C=14..20,x=21. The proof itself uses the above
phase implication and explicit book, not execution of a seven-case scan.

## 8. Primes13,17,19

For these primes the only nontrivial cycle type is p^1 1^(22-p).
Maximum degree ten makes all fixed-to-cycle pairs blue. Any blue pair
of fixed points would have all p cycle vertices as pages, so all fixed
pairs are red.

For p=13 the fixed red K9 violates the red cap. For p=19, a blue pair
between a fixed point and a cycle vertex has18-s>=8 blue pages, since
the internal red degree s is at most ten. This violates cap six.

For p=17 the five fixed points form a red K5. A blue fixed-to-cycle
pair has16-s blue pages, forcing s>=10, hence s=10. An internal red
cycle spine has r_D(k)<=3. An internal blue spine has15-20+r_D(k)
blue pages inside the cycle and five fixed blue pages, totaling r_D(k),
so r_D(k)<=6.
Summing over the16 nonzero shifts gives

    10*9=sum_{k!=0}r_D(k)<=10*3+6*6=66,

contradicting90>66. This excludes all three primes using only maximum
ten and literal page counts.

## 9. Group consequences, dependencies and prior art

The automorphism group acts faithfully on22 vertices. If a prime divides
its order, Cauchy's theorem supplies an automorphism of that order.
A prime larger than22 cannot occur as the order of a nonidentity
permutation on22 points. The new proof excludes7,13,17,19; the credited
order-eleven theorem excludes11 under the same maximum-degree premise.
Thus only primes2,3,5 remain, proving the conditional2^a3^b5^c form.

For arbitrary valid22 graphs, the credited upper-ten theorem supplies
the degree premise and the previous order-five theorem removes5. This
gives2^a3^b. Orbit-stabilizer makes every orbit size a divisor of this
group order; listing2^i3^j<=22 gives precisely the ten allowed sizes in
the opening statement. Their sum must be22, but no sufficiency is claimed.

The new conditional proof does not reprove the imported upper-degree,
order-eleven or order-five results. The combined global corollary retains
their exact stated prerequisites, including the historical minimum-degree
dependency of the order-five theorem. Its source checks are not replayed.
Neither the regular110 closure nor the irregular109 closure is used here.

The primary Ramsey interval and standard polycirculant framework were
rechecked in [Lidicky--McKinley--Pfender--Van Overberghe, Table1/section3.3](https://arxiv.org/html/2407.07285v2)
and [Wesley, section3](https://arxiv.org/html/2410.03625v2). The former's
equal-size-orbit definition does not directly cover the fixed-point
actions above. Block connection sets and correlation methods are known
tools. The seven-cycle fixed-degree case is already excluded by the
accepted global minimum-eight theorem; the present proof supplies a
different ordinary bridge without that theorem. No historical priority,
new circulant algorithm or Ramsey endpoint is asserted.

[primary21.rows](primary21.rows) reproduces the known93-edge primary
incumbent from [the authors' construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt),
using the complement of its off-diagonal matrix entries as red. It has
degree histogram8:4,9:16,10:1 and page caps3/6. The separately constructed
known KG(7,2) has105 red edges, caps3/5, and an order-seven action with
three seven-cycles on21 vertices. These positive controls check the
exact22/fixed-point hypotheses; reproduction is validation, not novelty.

All supplied programs use the Python standard library and integer
arithmetic, with checks active under optimization. They independently
validate the arithmetic, literal page identities and phase books. An
auxiliary bitset computation covers1,881,600 templates of the already
derived degree-seven fixed-root branch and finds zero survivors; only
2058 pass all internal blocks. That scoped census is supplementary,
not a proof premise or an unrestricted22 enumeration. No solver,
floating-point decision, interruption or resource failure supports the
theorem. The ordinary bridges remain unformalized and author validation
is not independent peer review.
