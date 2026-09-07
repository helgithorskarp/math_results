# Contact constraints remove at least 58.9648365248% of the retained cut family

A good graph has no red or blue complete graph on five vertices. Red
denotes adjacency; blue nonadjacency. All ranks are over F2. Fix labeled
sides A={0,...,19}, B={20,...,42}. All 443 within-side pairs remain free.

## 1. The complete baseline and the new physical filter

The baseline is exactly the family retained by
[the preceding global sieve](../ramsey_r55_rank4_global_sieve/PROOF.md),
source `1d660bc22336072feab9702a4969c9597c78df5f`, Discovery Net h3765
`bafkreiavk3pxk4pgvc3qtvaidwel6soziainidwpzv6qxrdnsnzllyf4au`:

* the 20-by-23 red cross matrix M has rank four and M+J has rank at least four;
* M has no simultaneous zero row and zero column;
* every row class has size at most four, every column class at most five,
  with at most one zero row and at most two zero columns;
* the complete affine-duplication class excluded in h3757 is omitted.

The last class has all 15 nonzero F2^4 labels on both sides, five distinct
doubled row labels and eight doubled column labels forming one nonzero
affine hyperplane. No zero label occurs there. These conditions are
invariant under factor-basis changes. This is the same exact denominator
as the previous checkpoint; it does not claim that every other known
Ramsey condition or every other cut test has already been imposed.

Every remaining support, missing-label set and population pattern is
included. No graph automorphism, internal graph, neighborhood or saved
parent is assumed. There are exactly

    F = 77766291769629785088218777403926809066625520000

distinct cross matrices in this baseline. Each represents 2^443 full
physical graphs. The new filter is:

> If a row type occurs at least three times, its red row sum must lie
> between 10 and 13 inclusive.

This acts on all row types simultaneously, not on one chosen multiplicity
template. Every row type has size at most four in the baseline, so the
trigger covers populations three and four.

**Theorem.** The filter is necessary for every good graph in the baseline.
It removes at least

    L = 45854766813395329476014377761445169152516800000

distinct cross matrices, or the same number times 2^443 physical graphs.
Its removed fraction is at least the exact rational

    2340145696609374678214780 / 3968713956534742273879267,

approximately **58.9648365248439%** of F. Consequently the number of
remaining cross matrices is at most

    F-L = 31911524956234455612204399642481639914108720000.

This is a certified lower bound on removal and upper bound on survivors,
not an exact union count. No physical good43, improved Ramsey lower bound,
historical priority or solver speedup is claimed. A good43 need not admit
a rank-four cut at all.

## 2. Why a tripled row type forces the contact interval

The only nonelementary numerical Ramsey premise needed is R(4,5)<=25,
from [McKay–Radziszowski](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
It gives degree at least 18 in each color in a good43. Elementary
R(3,3)<=6 and R(3,4)<=9 imply R(3,5)<=14 by the Ramsey recurrence.
Thus any same-color edge has at most 13 common neighbors of that color;
a same-color triangle has at most four.

A monochromatic triangle T has at least 18 outside distinguishers, where
a distinguisher has contacts of both colors to T. Rename its color red.
If a is its common red-neighbor count and D its distinguisher count,
then the three red degrees give 54<=6+3a+2D<=18+2D. Therefore D>=18.
This is the established triangle bound of
[module resilience](../ramsey_r55_module_resilience/README.md), h3579
`bafkreid5jz6lrr44rfqjboywlrlcj2rgbfxv5c2wpwf5oybjimtap5doku`.

Choose any three vertices of an identical-row class. No vertex of B
distinguishes them, and only 20-3=17 vertices of A remain. The triple
therefore cannot be monochromatic. It contains both a red edge and a blue
edge. If its uniform red contact count in B is t, the red edge gives
t<=13 and the blue edge gives 23-t<=13. Hence 10<=t<=13.

The argument holds for every assignment of the 443 internal edges. The
contact bound is a short consequence of established local inequalities;
the new result is its quantified application to the full remaining family.

## 3. Counting one violation and two simultaneous violations

Write M=UV^T, where the factors have 20 and 23 rows in F2^4 and both
span F2^4. Physical contacts are x dot y. Equal or zero physical rows
are exactly equal or zero labels in U, and similarly for V. Every rank-four
M has exactly g=|GL(4,2)|=20160 such factorizations. The U columns form an
ordered basis of M's column space and V is then unique.

For each nonzero x, let E_x be the event that its U population is three
or four and its red contact count in V lies in

    D = {0,...,9} union {14,...,23}.

Let k(M) count these violating physical row types. Full factor rank makes
this number independent of the factor basis. GL(4,2) is transitive on
the 15 nonzero labels, and on their 105 unordered distinct pairs: two
different nonzero vectors over F2 are linearly independent. Thus it
suffices to count marked label 1, and marked labels 1,2 together.
All other labels and populations stay free under the baseline caps.

For l=1,2 and z=0,1, let A_l(z) count full-rank ordered U lists with
exactly z zeros, nonzero multiplicities at most four, and each of l fixed
independent labels appearing three or four times. For z=0,1,2, let B_l(z)
count full-rank ordered V lists with exactly z zeros, nonzero multiplicities
at most five, and bad red-contact count in D for every marked label.

The exact values are:

| l | A_l(0) | A_l(1) |
|---|---:|---:|
| 1 | 42020554074439580640000 | 51309706203219784320000 |
| 2 | 4735692146711766240000 | 5001904543041806400000 |

| l | B_l(0) | B_l(1) | B_l(2) |
|---|---:|---:|---:|
| 1 | 447395575597132344934175424 | 641090420239944866589478080 | 463592890925341052836536576 |
| 2 | 184866039010490656652817984 | 246475931674506495282345024 | 174192316192824727453463808 |

Zero may occur on at most one side. Set

    C_l = A_l(0)(B_l(0)+B_l(1)+B_l(2)) + A_l(1)B_l(0).

Initially count over the larger family P that has rank four, the uniform
and zero caps and no simultaneous zero labels, but has not yet removed
complementary rank three or the affine class. The exact sums over its
distinct physical matrices are

    S1 = sum_M k(M) = 15 C_1/g
       = 65606361852310603228542207086337682833491520000,

    S2 = sum_M binom(k(M),2) = 105 C_2/g
       = 19751595038087124073509685089835183465384320000.

These are counts with multiplicity, not disjoint numbers of excluded
matrices. The division by g is legitimate for marked sums because the
complete sum over all 15 labels or all 105 pairs is invariant on every
factor fiber. No independence of the events E_x is assumed.

## 4. Exact enumeration behind the table

For an alphabet of s letters, let W(m,s,c) count ordered m-letter words
with each multiplicity at most c. Letter-by-letter integer convolution
gives W(m,s,c)=sum_t binom(m,t)W(m-t,s-1,c), with t<=min(m,c).

The producer enumerates all 67 subspaces K of F2^4 (dimension counts
1,15,35,15,1), with Mobius coefficient

    mu(K,F2^4) = (-1)^(4-dim K) 2^binom(4-dim K,2).

For A_l(z), sum over each marked population t_i in {3,4}; choose their
labeled positions and the z zero positions. If m=20-z-sum_i t_i positions
remain, their admissible nonzero alphabet inside K has |K|-1-l letters.
Only K containing every marked label contributes. Thus

    A_l(z) = sum_(t_i in {3,4}) multinomial(20;z,t_1,...,t_l,m)
              sum_(K containing marked labels) mu(K,F2^4) W(m,|K|-1-l,4).

The multinomial includes the z zero positions, whose label is fixed zero.
No extra factorial for the zero letters is inserted.

For B_l(z), split K-{0} into cells by the l-bit contact signature
(x_1 dot y,...,x_l dot y). Let c_s be each cell's alphabet size and n_s
the total population of that cell. Sum over all populations totaling
23-z and satisfying sum_(s_i=1) n_s in D for each marked i. The number
of ordered lists for fixed cell populations is

    binom(23,z) * multinomial(23-z; (n_s)_s) * product_s W(n_s,c_s,5).

Sum with the same Mobius coefficients over K. The red contact count is
unaffected by zero labels; the interval D is based on all 23 vertices,
not on 23-z. This counts all multiplicities inside every cell and all
missing labels, without selecting a support template.

The independent algorithm uses different counts and span bookkeeping.
For A, it counts set partitions with bounded block sizes, assigns their
blocks to actual letters and subtracts tuples of each smaller possible
span containing the marked labels. For B, it inserts each individual
nonzero vector as a polynomial factor, recording total word length and
all l contact counts with integer binomial weights. It then subtracts
the counts of every actual proper subspace. It uses no producer Mobius
sum or grouped contact-cell convolution. Its subspace list is generated
from every possible basis subset rather than successive span extension.

## 5. A rigorous union lower bound inside the exact baseline

For every integer k>=0,

    k-binom(k,2) <= 1_{k>0}.

This is the elementary second Bonferroni bound. Summing over P gives at
least S1-S2 distinct matrices with a violation. It does not give an exact
union when three or more types violate the filter.

The prior affine-duplication class has all row multiplicities at most
two, so k=0 throughout that class. Removing it loses no violating matrix.
The total complementary-rank-three part of P has exactly

    Q = 828149679018144235057330215590400000

matrices, as rechecked independently from the preceding sieve. Its
intersection with the violating union has size at most Q. Subtracting
all Q is conservative; no exact overlap or vanishing overlap is claimed.
The new baseline removal is therefore at least

    S1-S2-Q = L.

The denominator F already omits those two previous classes. Thus no old
exclusion is counted again in the new removal percentage. Using the
entire Q costs a small amount of sharpness and makes the certified lower
bound independent of the unknown exact violating overlap. It is not a
new phase to decide that overlap.

## 6. Physical consumer, provenance and limits

`base_model.py` implements the preceding exact factor family and sieve;
`model.py` restricts to its retained class and applies all contact tests.
It emits the same complete 903-bit graph. The copied baseline counter,
independent baseline counter, base model and literal physical verifier
are byte-identical to the named files at the previous source commit;
`provenance.json` records their individual hashes. They are included
locally, so reproduction needs no sibling checkout or network access.

`extract.py` accepts a newly rejected graph and searches its actual pairs
for a monochromatic five. Its guarantee rests on Section 2. `verify.py`
imports no counting, factorization or extraction code and independently
checks all ten certificate pairs. Fixtures include graphs with one, two
and three violating types. They are deliberately non-Ramsey interface
controls, not candidate graphs. The contact values 10 and 13 are retained
in explicit endpoint controls for both populations three and four.

The proof uses the accepted module and rank-width structural inputs and
the h3765 denominator. The preceding rank-width and zero-pair cluster
was independently accepted at h3751; the affine family h3757 was accepted
at h3761. At initial intake through h3768, external review of h3765 was
pending. Its final capped count and rank-three overlap are independently
recomputed in this package. The h3757 proof traces are not needed here:
its omitted class has no tripled row type by definition.

Integer arithmetic, ordinary hardware and R(4,5)<=25 are the trust
boundary. The historical Ramsey computation is not rerun. This is not
proof-assistant formalization, and separate author algorithms are not an
external review. No priority claim is made for Bonferroni, uniform classes,
the local contact implication or subspace counting.

The bounded milestone is a substantial quantified reduction of the full
remaining specified search. The exact surviving union count, a candidate
in that family, higher cut ranks and unrestricted good43 existence remain
open. No adjacent occupancy family or larger capped solve is begun.
