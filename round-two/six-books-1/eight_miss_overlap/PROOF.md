# Sharpening the overlap of two five-point miss rows

Actual author **six-books-1**, role **researcher**, 2026-10-01.

Use the hypotheses and notation of the committed
[eight-point miss-row lemma 8621](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_eight_miss_rows/PROOF.md),
artifact `bafkreiahiz6epzvowfeqssgvekewr2bjre4ld5gt2caexsjecyu4rok4ju`.
The graph has order 22, is red ten-regular, and avoids ordinary red B4
and blue B7. At the chosen root, A has ten points, P=G[A] is cubic
and triangle-free, and Z is an eight-point miss row. W=A minus Z has
two points. The other miss rows have sizes 5,5,4^8; call the five-rows
U,V. Both meet W, and the parent lemma proves |U intersect V intersect Z|<=2.

**Corollary.** In fact

    |U intersect V intersect Z| <= 1.                   (C1)

If the intersection is {a}, then

    (U union V) intersect W = W,                        (C2)
    N_P(a) = A minus D,
    D = ((U union V) intersect Z) union (U intersect V intersect W).
                                                           (C3)

The set in (C3) has exactly three points. In particular, if each five-row
uses just one W point and they share a Z point, those W points differ.
These are necessary conditions; the remaining host problem is open.

## Ordinary proof

Write I=U intersect V intersect Z, r=|I|, p=|U intersect W|,
q=|V intersect W|, and c=|U intersect V intersect W|. Here p,q are
one or two, and c>=p+q-2.

The parent's miss-pair bound is one on a red P pair and 4-c_P(i,j)
on a blue P pair. Since Z consumes every red pair within Z, both
U intersect Z and V intersect Z are independent in P.

Every point of I therefore has no P neighbor anywhere in
(U union V) intersect Z. It also has no P neighbor in
U intersect V intersect W: such a red pair would appear in both U,V,
exceeding its miss-pair bound one. Consequently

    N_P(a) is contained in A minus D for every a in I,
    |A minus D| = p+q+r-c <= r+2.                       (8)

Suppose r=2, with I={a,b}. The pair ab is blue and appears in Z,U,V.
Its three miss incidences force 3<=4-c_P(a,b), hence c_P(a,b)<=1.
But a and b both have three P neighbors in the same set A minus D,
whose size is at most four by (8). Inclusion-exclusion gives
c_P(a,b)>=3+3-4=2. This contradiction excludes r=2. The parent
already excludes r>=3, proving (C1).

If r=1, its point a has exactly three P neighbors, while (8) gives
at most three available points. Equality is forced throughout:
|A minus D|=3, c=p+q-2, and N_P(a)=A minus D. The equality for c
is equivalent to |(U union V) intersect W|=p+q-c=2, proving (C2).
This proves (C3) and the corollary.

The proof is analytic and unformalized. It imports exactly the parent
lemma's cubicity, row pattern, pair bounds and overlap-at-most-two
conclusion. It imports no computation or further global degree result.
The parent's dependencies remain credited there; independent review
of this corollary is pending. It strengthens the parent, rather than
correcting any false statement in it.

## Exact controls and limits

The two standard-library programs independently reproduce the compact
type table: direct labeled set enumeration versus multinomial counts.
All 196 choices of a five-set meeting W are considered in each ordered
slot, including repeated input sets. The parent overlap-at-most-two
restriction leaves 32,480 ordered pairs. The new overlap-two cut
eliminates 17,640; the equality-neighbor condition eliminates 2,240
more with overlap one. There are 12,600 retained labeled templates,
before imposing any further P or host condition. This is a count of
necessary set templates, not a count of valid graphs or an existence
claim. Every pair of triples in a four-point set intersects in at
least two points; exact controls check all sixteen ordered pairs.

The known 21-vertex baseline and current 22..23 Ramsey frontier were
rechecked in the parent publication. They are unchanged here. The
residual eight-row branch with Z overlap zero or one, all other regular
hosts, and the unrestricted Ramsey endpoint remain unresolved.
