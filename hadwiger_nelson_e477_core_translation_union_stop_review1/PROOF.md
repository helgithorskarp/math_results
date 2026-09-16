# Independent proof audit

## 1. Exact physical model

An E477 coefficient row (a,b,c,d) represents

    x=(a sqrt(3)+b sqrt(11))/36,
    y=(c+d sqrt(33))/36.

For the difference of two rows, direct expansion gives

    1296 distance^2
      = 3a^2+11b^2+c^2+33d^2 + 2(ab+cd)sqrt(33).

Because sqrt(33) is irrational, the distance is one exactly when the rational
coefficient is 1296 and ab+cd=0. This is the review's primary edge predicate.

Row equality is also physical equality. In the first coordinate, a nontrivial
relation a sqrt(3)+b sqrt(11)=0 would make sqrt(33) rational; in the second,
c+d sqrt(33)=0 does the same. Therefore equality of physical points is
equivalent to equality of all four integer coefficients.

The checker reconstructs 477 distinct source rows and all 2,458 unit pairs.
It checks the source's proper equal-terminal four-word and all 253 deletion
words. Each deletion word properly colours E477 minus its named vertex and
gives the two marked terminals different colours.

If an E477 subgraph forces those terminals equal, it cannot omit any one of
the 253 named vertices, because the corresponding word would restrict to an
unequal-terminal colouring. It must also contain the two terminals. Hence it
contains their 255-point set C. This conditional mandatory-core implication
uses only positive colour words.

## 2. Complete maximum-overlap selection

If C and C+t overlap, then some p,q in C satisfy p+t=q, so t=q-p. Thus every
nonzero translation with positive overlap occurs among the finite set of
ordered core differences. The review obtains 9,046 distinct candidates.

For each candidate it directly counts

    number of p in C for which p+t is in C,

which is exactly the size of C intersect (C+t). The maximum is 75, attained
only at the opposite pair

    (-3,3,3,3), (3,-3,-3,-3).

The target's lexicographic rule therefore selects (-3,3,3,3). Direct norm
expansion has rational numerator 432 and zero sqrt(33) coefficient, so its
squared physical length is 432/1296=1/3.

The two maximizers define congruent unions: translating C union (C+t) by -t
gives C union (C-t).

## 3. Complete union graph

Literal set union after translation gives 255+255-75=435 rows. Testing all
C(435,2)=94,395 unordered pairs with the two exact equations gives 1,589 unit
edges and reproduces the target's point and edge hashes.

The induced core has 659 unit edges. Mapping all 1,318 edge-copy occurrences
into the physical union and merging equal images leaves 1,231 inherited
edges, so 87 inherited images are duplicates. The other 358 unit pairs are
genuine contacts between copy-only points on opposite sides. This accounts
for every complete unit edge.

## 4. Chromatic number

The supplied 435-character word assigns one of four colours to every sorted
physical row. Direct checking on all 1,589 edges proves an upper bound of
four.

The seven supplied source labels induce 11 edges with degree sequence
3,3,3,3,3,3,4, the Moser spindle. Canonical restricted-growth enumeration
finds no proper three-colouring and 16 canonical proper four-colourings.
Therefore this subgraph, and hence the whole union, requires four colours.
Together with the literal word, the union has chromatic number exactly four.

## 5. Connected-component refinement

The exact degree census has one degree-zero row:

    (-15,-9,45,-3),

represented only by untranslated source label 91. Exhaustive graph traversal
gives component orders 434 and 1. The seven-point four-chromatic witness lies
in the 434-point component, and the target word restricts to a proper
four-colouring of it. Thus the main component is a connected 434-point,
1,589-edge complete plane unit-distance graph of chromatic number four.

This refinement does not challenge the target's 435-point union count: the
isolated row genuinely belongs to the prescribed union. It only records that
one deletion preserves every edge and the chromatic number.
