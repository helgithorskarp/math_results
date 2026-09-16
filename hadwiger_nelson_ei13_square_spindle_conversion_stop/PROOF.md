# Proof of the fixed construction result

## 1. Source identity and its distinct metric meaning

The source's 13 coordinates are transcribed in `SOURCE` in `verify.py` as
rows `(a,b,c,d)`, representing `((a+b sqrt7)/4,(c+d sqrt7)/4)`. Exact expansion
of all 78 pair distances gives precisely the listed 20 unit pairs and 14
distance-`sqrt(2)` pairs. Those lists agree with the second proof of Theorem
3.1 in the cited Exoo--Ismailescu paper.

The source's proper five-word is checked on all 34 pairs. Exhaustive
four-colouring enumeration finds zero words. Vertices are ordered by
decreasing degree, breaking ties by source index. At each step the recursion
tries every allowed colour among the already used colours and at most the
next new colour. Every colouring admits exactly one such relabelling, so
restricted-growth enumeration preserves existence. The recursion visits 89
states and no full assignment. Thus the two-distance graph has chromatic
number five. This is a source audit, not an assertion about a unit graph.

## 2. Physical construction and cap

For a diagonal `A,B` of squared length two, the points
`(A+B +/- i(B-A))/2` complete a unit square. Their four directed boundary
sides therefore have unit length. The 20 original unit sides also have that
length. The construction contains 76 directed side occurrences, with the
orientations specified in `ARCHITECTURE.json`.

On a normalized directed side `0->1`, the spindle's other five points are

```
(1/2, -sqrt(11)/2),
(1/4 + sqrt(33)/12, -sqrt(11)/4 + sqrt(3)/12),
(1/4 - sqrt(33)/12, -sqrt(11)/4 - sqrt(3)/12),
(3/4 + sqrt(33)/12, -sqrt(11)/4 - sqrt(3)/12),
(3/4 - sqrt(33)/12, -sqrt(11)/4 + sqrt(3)/12).
```

These are the two unit-circle intersections for each pair `(0,H)` and
`(1,H)`, where both pairs have distance `sqrt(3)`. Direct all-pairs checking
gives seven distinct points and eleven unit edges. Transport by the exact
direct similarity `z -> A+(B-A)z` preserves them. This expanded formula is
the verifier's construction, distinct from the producer's intersection rule.

Keeping all source points and square corners, then adding at most five points
per spindle, proves the pre-collision bound `13+28+76*5=421`.
Duplicate side occurrences and coincident points are retained in provenance
but merged in the physical support; no vertex is deleted to reach the cap.

## 3. Exact equality and complete strict graph

The square-base coordinates have denominator 8 and lie in `Q(sqrt7)^2`.
Multiplying by the normalized spindle's denominator-12 coordinates gives
integer coefficients with common denominator 96 in
`K=Q(sqrt3,sqrt7,sqrt11)`. The independent square classes of the three
distinct primes show that `[K:Q]=8`. Consequently the eight radical
coefficients represent each field element uniquely.

The verifier labels each basis element by its squarefree radicand and uses

```
sqrt(r)*sqrt(s) = gcd(r,s) * sqrt(rs/gcd(r,s)^2).
```

Thus collision comparison is coefficient comparison. A pair is a strict
unit edge exactly when its squared-distance coefficients are
`(96^2,0,...,0)` before division by `96^2`.

Reconstruction gives 334 distinct coefficient rows. Every one of their
55,611 unordered pairs is tested, giving 851 unit pairs. Their canonical
streams match the hashes in `README.md` and `certificate.json`. The 662
distinct inherited source/spindle edges are a subset; all 189 other unit
pairs are included. The producer and verifier agree on both entire streams,
not only their aggregate counts.

## 4. Ordinary chromatic decision on that same graph

`four_word` supplies one colour in `{0,1,2,3}` per canonical physical point.
The checker directly tests every one of the 851 complete edges; each has
different endpoint colours. Therefore the complete graph is four-colourable.

The seven `moser_ids` are distinct and induce exactly the eleven template
edges. The same exhaustive colour-enumeration rule finds zero proper
three-colourings and sixteen canonical proper four-colourings on these
seven vertices. Hence the whole graph cannot be three-colourable, proving
its chromatic number is exactly four. The final upper and lower bounds do
not rely on solver UNSAT output.

The complete physical word restricts to source labels 1 through 13 as

```
3,3,1,3,0,1,2,3,1,3,0,2,3.
```

It makes the distance-`sqrt(2)` pairs `(2,4)`, `(2,8)`, `(2,10)`, `(3,6)`
and `(4,13)` monochromatic, in the paper's one-based labels. These five
failures explain why the source's two-distance obstruction does not lift
through this conversion. They are not physical unit edges.

## 5. Trust and scope

The proof is an exact computer-assisted finite construction result with
public source and a positive colouring certificate. It trusts the published
algorithms, Python's arbitrary-precision integer arithmetic and their
execution. No floating comparisons, guessed contacts, incomplete
enumeration, restricted physical-colouring class or SAT lower-bound oracle
enters the conclusion. The original SAT discovery used CaDiCaL 1.9.5;
its returned word is checked independently of that solver and encoding.

Normal and optimized runs agree; controls reject eleven semantic corruptions.
These are author-side checks and do not constitute independent peer review.
The result concerns exactly this fixed 334-point support, and does not imply
a global four-colouring theorem or an exclusion of other EI13 conversions.
