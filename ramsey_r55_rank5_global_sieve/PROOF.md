# Global four-set obstruction and rank-five coverage

A good graph here is a simple graph on 43 vertices with no monochromatic
five-clique when edges are red and nonedges blue. A vertex distinguishes
a set if its contacts to that set are not all the same color. Ranks are
over F2. All statements concern physical graphs, not feasible scalar
summaries of their neighborhoods.

## 1. Imported bounds and the equality case

The only nonelementary numerical premise is R(4,5)<=25, proved by
McKay and Radziszowski, [R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
Its historical computation is not repeated. Every color degree in a good43
is at most 24, hence at least 18. The elementary bounds R(3,3)<=6,
R(3,4)<=9 and the Ramsey recurrence give R(3,5)<=14 and R(4,4)<=18.
For completeness, a triangle-free nine-vertex graph with independence
number at most three would be 3-regular: its neighborhoods are independent,
while each nonneighborhood has at most five vertices by R(3,3)<=6. The odd
degree sum is impossible. Thus no other historical computation is needed.

An edge has at most 13 common neighbors of its own color. Otherwise its
common neighborhood contains a triangle of that color or an opposite
five-clique. A monochromatic triangle has at most four common neighbors
of its own color: they must be independent in that color.

The [module-resilience proof](../ramsey_r55_module_resilience/README.md)
established that every triple has at least 17 distinguishers, and every
monochromatic triple at least 18. Here is the equality information needed.
For a red triangle with D distinguishers and a common red neighbors,

    54 <= 6 + 3a + 2D <= 18 + 2D.

For a mixed triple label its red edges 01 and 02, and its blue edge 12.
Let C01,C02 count common red neighbors and C12 common blue neighbors.
The third triple vertex is not counted in any of these. On every outside
contact signature (x0,x1,x2),

    x0*x1 + x0*x2 + (1-x1)*(1-x2)
      = 1_{x0=x1=x2} + x0.

Summing over the 40 outside vertices gives

    C01+C02+C12 = 38-D+d_red(0) <= 39.

Therefore D>=d_red(0)-1>=17. If D<=17, equality forces D=17,
d_red(0)=18 and all three common-neighbor counts equal 13. Under color
reversal, the center of the majority color has degree 18 in that color,
or red degree 24 when that majority color is blue.

## 2. Every four-set has at least 17 distinguishers

Suppose a four-set Q has at most 16 outside distinguishers. Each triple
T in Q has at most those 16 plus the fourth vertex as distinguishers.
Thus no T is monochromatic, and every T has exactly 17 distinguishers.
It follows that Q has exactly 16 outside distinguishers; its other 23
outside vertices are uniform to all four vertices of Q. The fourth vertex
distinguishes each T, and each of the 16 outside distinguishers must
distinguish every one of the four triples.

A four-contact signature distinguishes every triple exactly when it has
two contacts of each color. Hence the 16 outside distinguishers contribute
exactly 32 red incidences with Q. Write t for the number of the other 23
vertices that are all red to Q. Their contribution is 4t. Since Q has an
edge of each color, the common-neighbor caps give

    t <= 13,  23-t <= 13,  hence 10 <= t <= 13.

Every vertex of Q has internal red degree one or two. Degree zero or three
would force a monochromatic triple either with that vertex or among the
other three. Let a be the number with internal red degree one. The internal
red degree sum is 8-a, so a is even: a is 0, 2 or 4.

A vertex of internal red degree two is the red center of a mixed triple,
and therefore has total red degree 18 by the equality case. A vertex of
internal red degree one is the blue center of a mixed triple, and has total
red degree 24. The total red degree sum over Q is consequently 72+6a.
Counting the same incidences by location gives

    72+6a = (8-a) + 32 + 4t,
    4t = 32+7a.

For a=0,2,4 this requires t=8, 23/2,15, respectively. None is an integer
in [10,13]. This contradiction proves the claim for every four-set in
every good43, without any rank or symmetry hypothesis.

In a 20+23 cut, four vertices of the 20-side with the same cross row have
at most the other 16 same-side vertices as distinguishers. Thus every row
class has size at most three. Equivalently, no four-vertex module can remain
after deletion of at most 16 other vertices. No stronger module statement
for other sizes is being asserted here.

`quadruple.py` checks all eight triple signatures, the equality boundary,
all 64 labeled K4 colorings and all 16 four-contact signatures. It finds
the 18 nonmonochromatic K4 colorings and verifies the impossibility for
each one. These finite checks audit the displayed argument; they are not
a replacement for its global incidence interpretation.

## 3. The complete global family and the other predicates

Fix A={0,...,19}, B={20,...,42}. Let F5 be all full graphs with red cross
matrix M of rank five and blue cross matrix M+J of rank at least five.
All 443 within-side edge bits are independent free coordinates. F5 includes
every label pattern and every internal graph. It is a selected branch,
not a claimed universal normal form for good43.

Every good member of F5 must satisfy all these physical cross conditions:

1. There is no simultaneous zero row and zero column.
2. The zero-row class has at most one member and the zero-column class
   at most two.
3. Every identical-column class has at most five members.
4. Every identical-row class has at most three members, by Section 2.

The first three statements were already proved in the earlier
[rank-four reduction](../ramsey_r55_rank4_cut_search_reduction/PROOF.md)
and [global sieve](../ramsey_r55_rank4_global_sieve/PROOF.md), without rank
hypotheses on these structural implications. We recall their proofs.

If u in A is a zero row and v in B a zero column, u has at least 18 red
neighbors within A, all blue to v. R(4,4)<=18 gives a red four-clique
extending with u or a blue four-clique extending with v.

Each zero class is red-complete: the opposite side has at least 20 vertices
and hence a blue triangle by R(3,5)<=14, which would extend any blue edge
in the zero class. Two zero rows would have their red neighborhoods confined
to A and force 34<=18+13=31 by the edge common-neighbor bound. Three zero
columns would form a red triangle confined to B and force
54<=6+2*20+4=50 by the triangle common-neighbor bound.

Six identical columns contain a monochromatic triangle, say red, by
R(3,3)<=6. Their red contact set in A has size at most four, so their blue
contact set has at least 16 and contains a blue triangle. Any blue edge
among the six then extends that triangle. The six would have to be
red-complete, another contradiction. Reverse colors if needed.

For staged attribution we also record the established older row cap four:
five identical rows would require at least 170 total triple distinguishers.
The five vertices contribute at most 20 and each of the other 15 vertices
of A at most nine, giving at most 155. The last stage tightens four to three;
it is the only new structural predicate in the numerical reduction.

The denominator F5 does not require all previous predicates on every cut,
nor even every known predicate on this cut. This qualification is necessary
when interpreting the percentage. Complementary rank-four matrices are
outside F5 even if they survived the older rank-four filters: we do not
claim that entire excluded-from-denominator branch is impossible.

## 4. Exact counts, covering all supports and multiplicities

Write M=UV^T with both factors full column rank five, of orders 20-by-5
and 23-by-5. Equal physical rows correspond exactly to equal U labels;
equal columns correspond exactly to equal V labels. Zero is also detected
literally. Every rank-five matrix has exactly

    g = |GL(5,2)| = 31*30*28*24*16 = 9999360

factorizations. Choose an ordered basis of its column space for U; then
V is uniquely determined. The action is free, and all the predicates are
basis-invariant. Every count below is divided by this constant fiber.

Let B(m,s,c) be the number of words of length m on s letters with each
multiplicity at most c. With B(0,0,c)=1 and B(m,0,c)=0 for m>0,

    B(m,s,c) = sum_(0<=t<=min(m,c)) binom(m,t) B(m-t,s-1,c).

The number of spanning words from the nonzero labels of F2^r is

    N(m,r,c) = sum_(k=0..r) [r choose k]_2
              (-1)^(r-k) 2^binom(r-k,2) B(m,2^k-1,c).

This is inversion on the subspace lattice. If nonzero row/column caps are
a,b and zero caps p,q, matrices satisfying the no-zero-pair condition number

    P(a,b,p,q) = (1/g) sum_(0<=i<=p,0<=j<=q,ij=0)
        binom(20,i) binom(23,j) N(20-i,5,a) N(23-j,5,b).

The total number of rank-five matrices before any predicates is

    T = product_(i=0..4) (2^20-2^i)(2^23-2^i) / g.

These formulas include absent labels, arbitrary supports, all ordered
vertex lists and all allowed repetitions; no occupancy template is selected.

The blue rank can be four, five or six. For rank four, both all-one vectors
must belong to the corresponding factor column spaces. There are then
unique nonzero vectors s,t with Us=1 and Vt=1, and

    M+J = U(I+s*t^T)V^T.

This has rank four exactly when t dot s=1. There are 31*16 such pairs.
The U and V words lie in specified nonzero affine hyperplanes; zero is
absent, so the zero caps do not affect this overlap.

For positive m, the number of capped spanning words in one such hyperplane
is

    L(m,r,c) = sum_(k=0..r-1) 2^(r-1-k) [r-1 choose k]_2
              (-1)^(r-1-k) 2^binom(r-1-k,2) B(m,2^k,c).

The coefficient counts affine k-subspaces; full linear span of a nonzero
affine hyperplane word is equivalent to full affine span there. Thus the
blue-rank-four overlap is exactly

    Q(a,b) = 31*16*L(20,5,a)*L(23,5,b)/g.

It must be recomputed at every cap stage. The baseline is T-Q(20,23),
and the final surviving set has size P(3,5,1,2)-Q(3,5). No affine-template
subtraction or rank-four contact moment is imported into this new count.

## 5. Independent positive enumeration and result

`counts.py` implements these integer convolutions and inversion sums.
`direct_span.py` independently processes each actual vector label, tracking
the concrete linear span S as a subset of F2^5 and occupied word length k.
Giving the next label multiplicity t changes S to span(S,label) when t>0
and multiplies the word count by binom(k+t,t). Zero multiplicity preserves
S. This is a positive dynamic program with no Gaussian coefficient, Mobius
inversion or span subtraction. Processing the actual nonzero label set,
the 16 labels of an affine hyperplane, and all 32 labels reproduces every
one of the 212 target spanning-word entries used or cross-checked here.
All raw and overlap-adjusted stages agree entry by entry.

The resulting exact counts are

    baseline = 5265776463769286448156565145344760253473964876758764876800
    removed  = 2066365377174402749659084812993090655368806390234845516800
    remaining= 3199411086594883698497480332351669598105158486523919360000.

The removed fraction is exactly

    72250993667250533318774539803589602314409997
    / 184119220220965173622650664548131290651799397,

or 39.24141845731297...%. After the older caps and zero predicates, the
denominator is 3519050688364123854062405339332286937833671593864516480000.
The new row cap alone removes 319639601769240155564925006980617339728513107340597120000,
the fraction

    1381295518673381498026176252447729
    / 15207280070793831858140556386411641

or 9.08312013879597...% of that denominator. No percentages are added as if
their denominators agreed. Every full-graph count has the common factor 2^443.

## 6. Scope and provenance

The new structural argument refines the mixed-triple equality boundary
from module resilience, Discovery Net h3579
`bafkreid5jz6lrr44rfqjboywlrlcj2rgbfxv5c2wpwf5oybjimtap5doku`, source
`823d258fe6dfa33a695e148bbed08b1709fbe3c9`. Established zero and class bounds
are credited to h3747 and h3765. The latter's source is
`1d660bc22336072feab9702a4969c9597c78df5f`, contribution
`bafkreiavk3pxk4pgvc3qtvaidwel6soziainidwpzv6qxrdnsnzllyf4au`.
The pass intake read its new independent acceptance h3775,
`bafkreidecchjvcc76x2y6ly7nl7nebqoqxrt6bujkey7u3gauq7gu2zxve`.
All needed structural proofs and count formulas are restated above.

The four-set theorem is global, while its quantified consumer covers one
rank-five branch on one partition. Neither the remaining family nor
unrestricted good43 existence is decided. The source does not contain an
isomorphism classification, a SAT search, or a promising candidate.
The previous rank-four contact bound remains an upper bound on its own
residual family, and is not used as a denominator here. No construction,
local-repair basin or isolated occupancy-template search is reopened.

The independent algorithm is an author-side check, not external review.
This proof is not formally mechanized; the imported R(4,5) computation,
ordinary Python execution and hardware remain trust boundaries. Limited
primary-source searches do not establish historical priority for the
four-set refinement, standard finite-field counts or the combined sieve.
