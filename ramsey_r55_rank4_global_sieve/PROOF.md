# A quantified sieve over the entire surviving rank-four cut family

A **good** graph has neither a red nor a blue complete graph on five
vertices. Red denotes adjacency, blue nonadjacency. Ranks are over F2.
Fix labeled sides A={0,...,19}, B={20,...,42}. All 443 within-side pairs
are free throughout. The cross matrix M has size 20 by 23 and rank four.
No symmetry, internal graph, neighborhood, saved parent, or occupancy
pattern is prescribed.

The structural inequalities below are established results, not new
invariants. This contribution turns them into one exact all-pattern search
reduction with the overlap against earlier exclusions removed.

## 1. The precise baseline and result

Let F be all such physical graphs satisfying these three cross conditions:

1. M does not have both a zero row and a zero column.
2. rank(M+J)>=4, where J is all ones.
3. M is outside the previously excluded affine-duplication class: in any
   full-rank factorization M=UV^T, each nonzero F2^4 label occurs on each
   side, five distinct row labels occur twice and the other ten once,
   and exactly the eight column labels in a nonzero affine hyperplane
   occur twice, the other seven once. Zero occurs on neither side.

These are basis-invariant conditions. They specify the denominator, not
all known necessary Ramsey conditions. In particular, F is not asserted
to pass every cut test on every partition or every local Ramsey test.
The third condition can be understood as a definition of the current
search without importing that class's SAT proofs into this new exclusion.
Its already published whole-family exclusion is credited below.

In a good graph in F, every identical-row class has size at most four,
every identical-column class size at most five, the zero-row class size
at most one and the zero-column class size at most two. These constraints
act simultaneously on every type, including absent types, in every
full-rank factorization. They are not a choice of one type pattern.

**Exact reduction.** The following counts are of distinct cross matrices,
not factorizations, unlabeled graphs, or isomorphism classes:

| class | number |
|---|---:|
| baseline F | 130462366516263974374824266855507767254963105600 |
| newly removed | 52696074746634189286605489451580958188337585600 |
| remaining after this sieve | 77766291769629785088218777403926809066625520000 |

Multiply every entry by 2^443 for physical 43-vertex graphs on the fixed
partition. The exact additional removed fraction is

    376310008768820496017231590851225959
    / 931649928837861438158324253913962509

or approximately **40.3917820546854%** of F. The final remaining set is
26.1896475091401% of all rank-four 20-by-23 binary cross matrices.
No fraction of the unrestricted 43-vertex graph space, union over cuts,
actual good graphs, or future solver running time is asserted.

## 2. Established structural bounds and a self-contained derivation

These uniform-class and zero-class bounds occur in Section 2 of the
[rank-width-four proof](../ramsey_r55_rank_width_four/PROOF.md), source
`931cd80b76854a3d42f605839508d4a72848fc7c`, Discovery Net h3735
`bafkreiedakh5pu7x2az265jg65bzpyaa5wfvmmdzcrlonjdqhlkggwnynq`.
The triple calculation and five-set distinguishing sum come from
[module resilience](../ramsey_r55_module_resilience/README.md), source
`823d258fe6dfa33a695e148bbed08b1709fbe3c9`, h3579
`bafkreid5jz6lrr44rfqjboywlrlcj2rgbfxv5c2wpwf5oybjimtap5doku`.
We restate the argument to make the present filter auditable.

The only nonelementary numerical Ramsey premise needed is R(4,5)<=25,
from McKay and Radziszowski,
[R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
Its historical computation is not replayed. Thus every degree in a
good43 lies in [18,24]. R(3,3)<=6 is the elementary three-contact argument.
For R(3,4)<=9, a triangle-free nine-vertex graph with independence number
at most three would be 3-regular: neighborhoods are independent and
nonneighborhoods have order at most five by R(3,3)<=6. Its degree sum
would be odd. The Ramsey recurrence gives R(3,5)<=5+9=14.

Consequently a same-colored edge has at most 13 common neighbors of its
color, and a same-colored triangle at most four. Every good set of at
least 14 vertices contains a triangle in each color.

Every triple has at least 17 outside vertices with nonuniform contacts.
For a red triangle with D distinguishers and a common red neighbors,
the red degree sum gives 54<=6+3a+2D<=18+2D, so D>=18.
For a mixed triple, rename vertices and colors so 01 and 02 are red
and 12 blue. Write C01,C02 for the two common red counts and C12 for
the common blue count. None counts the third triple vertex. The identity

    x0*x1+x0*x2+(1-x1)*(1-x2) = 1_{x0=x1=x2}+x0

on all eight outside contact signatures gives

    C01+C02+C12 = 40-D+d_red(0)-2 <= 39.

Thus D>=d_red(0)-1>=17.

**Row classes have size at most four.** If five vertices have the same
contacts across the cut, sum distinguishing counts over their ten triples.
The lower bound is 170. The five vertices contribute at most 20 in all;
each of the other 15 vertices of A contributes at most nine, because among
its five contacts some triple is uniform. B contributes zero. This gives
170<=20+9*15=155, impossible. Selecting any five proves the cap even for
larger classes.

**Column classes have size at most five.** Suppose six vertices of B
have identical cross contacts. They contain, say, a red triangle by
R(3,3)<=6. Their red-contact set in A has at most four vertices. Their
blue-contact set therefore has at least 16 vertices and contains a blue
triangle. Any blue edge among the six would extend that blue triangle.
All six would therefore be red-complete, also impossible. Reverse the
colors if the initial triangle is blue.

**Zero-class caps.** Since the opposite side contains a blue triangle,
each zero class is red-complete. A red pair whose red neighbors are
confined to a side of order m satisfies

    34 <= (m-2)+13.

Indeed the two red degrees minus their internal edge contribute at least
34, while each of the other m-2 vertices contributes at most one plus
one additional incidence for at most 13 common neighbors. For m=20 this
is impossible, so A has at most one zero row. A red triangle confined to
a side of order m similarly satisfies

    54 <= 6+2(m-3)+4 = 2m+4.

At m=23 this is impossible. Thus B has at most two zero columns.
These arguments hold for arbitrary internal edges and do not assume rank
four. The factor model is solely the counting and generator consumer.

## 3. Counting every label pattern without selecting templates

Write M=UV^T with U of size 20 by 4, V of size 23 by 4, both full rank.
Contacts are x dot y. Full rank implies equal physical rows exactly when
the corresponding U labels agree, and likewise for columns and V. Zero
rows or columns are exactly zero labels.

Every rank-four M has exactly g=|GL(4,2)|=20160 such factorizations: the
columns of U are an ordered basis of the column space of M, and V is then
unique. Basis changes preserve every condition used in the count. The
action is free because the factors have full rank.

Let B(m,s,c) count ordered m-tuples from s letters with each multiplicity
at most c. Adding the last letter gives the exact recurrence

    B(m,s,c) = sum_(t=0..min(m,c)) binom(m,t) B(m-t,s-1,c),
    B(0,0,c)=1, B(m,0,c)=0 for m>0.

Let N(m,r,c) count spanning tuples of nonzero vectors of F2^r with the
same cap. Subspace-lattice inversion gives

    N(m,r,c) = sum_(k=0..r) [r choose k]_2
               (-1)^(r-k) 2^binom(r-k,2) B(m,2^k-1,c).

Equivalently, independent triangular inversion by actual span dimension
gives B(m,2^r-1,c)=sum_k [r choose k]_2 N(m,k,c).
The second checker computes B through set partitions: choose the block
containing the first position, then inject its blocks into the letter set.
Thus it does not reuse the letter-by-letter convolution or Mobius sum.

For row nonzero cap a, column nonzero cap b, and zero multiplicity caps
p,q, the number of matrices with no simultaneous zero labels is

    P(a,b,p,q) = (1/g) sum_(0<=i<=p,0<=j<=q, i*j=0)
       binom(20,i) binom(23,j) N(20-i,4,a) N(23-j,4,b).

This includes every ordered list, all missing labels and all allowable
multiplicities; it does not enumerate just a representative support.
The unrestricted stage uses (a,b,p,q)=(20,23,20,23). The sieve uses
(4,5,1,2). The zero caps are below the uniform-class caps, so the
nonzero-class cap formulation is exactly the physical filter after the
zero step.

## 4. Removing overlap with the two previous exclusions

First remove complementary rank three. Rank(M+J)=3 can occur only if
the all-one vectors lie in both the column and row spaces of M. If
either fails, adjoining the corresponding one vector and elementary
elimination gives rank at least four. If both hold, there are unique
nonzero vectors s,t with U s=1 and V t=1. Then

    M+J = U(I+s t^T)V^T,

which has rank three exactly when t dot s=1. There are 15*8 such ordered
pairs (s,t). The labels of U lie in the eight-point hyperplane H_s,
and those of V in H_t. Zero is absent, so this overlap is unaffected
by the zero caps. A spanning tuple in H_s has full affine span of its
three-dimensional affine space.

Let L(m,r,c) count capped, linearly spanning tuples in a fixed nonzero
affine hyperplane of F2^r. For positive m, affine-subspace inversion gives

    L(m,r,c) = sum_(k=0..r-1) 2^(r-1-k) [r-1 choose k]_2
       (-1)^(r-1-k) 2^binom(r-1-k,2) B(m,2^k,c).

There are 2^(r-1-k)[r-1 choose k]_2 affine k-subspaces. Therefore the
rank-three overlap at each stage is exactly

    Q(a,b) = 120 L(20,4,a) L(23,4,b) / 20160.

The independently computed triangular recurrence sorts tuples by their
actual affine span. Exhaustive physical small matrices test this overlap
formula together with the main count. In particular the correction is
recomputed after each cap, rather than subtracting an unchanged overlap.

Next remove the prior affine-duplication family. For each choice of its
15 hyperplanes and binom(15,5) doubled row-label sets, the vertex-list
counts are 20!/2^5 and 23!/2^8. Thus its distinct cross count is

    E = 15 binom(15,5) 20! 23! / (2^13 * 20160)
      = 17154780486757774613743095705600000000.

Every one of these matrices satisfies all the present caps, so this
subtraction is unchanged at every stage. It has complementary rank five:
neither full set of 15 nonzero labels is contained in a nonzero affine
hyperplane, so neither one vector lies in the corresponding factor's
column space. Thus E is disjoint from Q. Its whole-family exclusion is
in [the affine-duplication package](../ramsey_r55_affine_duplication_cut/PROOF.md),
source `a960dc16a0377c12e93d1ed5afd6da92fe10b833`, h3757
`bafkreiffq7rohzu5n36ofcrt6gyxnvm5trsv2itm3i7irz6rn6ooxc5d3m`.
The pre-publication refresh found its independent acceptance at h3761,
`bafkreifojsvu5b2odgdvbnpeqxc7nle6v6kwbccssh7jnrmnhgbpjxcqge`, with a
[fresh 32-proof replay and independent audit](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_affine_duplication_cut_review1),
source `5dee01c748cdf6ec359c867d61afcc74f3c161c3`.
Here membership and E are rederived; the numerical pruning and the new
exclusion remain valid for the defined F independently of that review.

The displayed baseline and survivor counts are P(20,23,20,23)-Q(20,23)-E
and P(4,5,1,2)-Q(4,5)-E. `counts.py` gives each disjoint intermediate
removal. For comparison with the accepted zero-pair reduction alone,
P(20,23,20,23)=130462366537469674573235644260325500723394324800
and P(4,5,1,2)=77766291787612715253994696252727234987815920000.

The [zero-pair source](../ramsey_r55_rank4_cut_search_reduction/PROOF.md),
`c9a59be222cb0ce9a2ec7e9411a05441a2a7f261`, h3747
`bafkreie4butunagwcncfbmzzk7euolicwrayfnpfjrjowc6xgmtvzpoxne`,
counted its 56.0636965570% removal before these two overlap adjustments.
The combined independent acceptance of h3735 and h3747 is h3751
`bafkreihwelfcwkwvc5po2ho4u7n54rexswefzesxxzdtixx5u2qdzy7b34`.

## 5. Physical consumer and limits

`model.py` accepts the two complete factor lists and all 443 internal
bits, returns the exact 903-bit physical graph and the baseline/sieve
classification, and is invariant under factor-basis changes. It does
not silently treat a surviving input as Ramsey. All 443 internal bits
are individually checked against the physical pair map.

`extract.py` accepts any newly rejected member of F and searches both
colors exhaustively for a literal five-clique. The universal guarantee
comes from Section 2, not from a saved status. `verify.py` independently
decodes the physical graph and checks all ten pairs of the returned
certificate. This optional certificate path demonstrates physical
discrimination; no generated fixture is claimed to be a candidate.

The computation uses Python integers and the standard library. It imports
no graph catalog, SAT solver, stored proof verdict, large proof file or
network input. The reasoning is not proof-assistant formalized and the
author's distinct checks are not an external review. The upper Ramsey
input and ordinary hardware remain trust boundaries. No historical
priority claim is made for uniform classes, span enumeration or the sieve.

This closes the stated bounded gate: it eliminates the entire violating
part of a globally specified search, quantified after earlier exclusions.
It neither decides the remaining class nor raises the rank-width lower
bound. A good43 might have no rank-four cut. No physical good43, improved
Ramsey lower bound, candidate-quality fraction, or solver acceleration
has been established.
