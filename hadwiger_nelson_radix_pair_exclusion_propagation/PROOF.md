# Exact whole-frontier pair propagation

We continue A5(z)=T+zT+...+z^4T, T={0,1,omega}, omega=(1+i sqrt(3))/2.
The accepted collision, unit-circle and low-active branches remain closed.
This proof propagates existing physical exclusions; it claims no new graph
embedding or non-four-colourability witness.

## 1. The finite domain

For a displacement row with Eisenstein coefficients a_j+b_j*omega, reduce
coefficients modulo two into F4={0,1,alpha,1+alpha}, alpha^2=alpha+1. A noncircle
curve has a signature (n,c), the canonical nonzero-scalar normalization of

```
n = (a_j+b_j*alpha,j=1..4),  c = a_0+b_0*alpha.
```

Its forbidden additive four-colour words form the affine hyperplane n.w=c.
There are 336 realized signatures among the 340 theoretical types. H4171's
complete five-cover classification, after its partition alternative is excluded,
says an exactly-five-active counterexample must use one curve from each section
of a full affine pencil. We import that classification; no new active-count or
support-profile family is introduced.

There are 357 two-dimensional normal subspaces of F4^4 and 16 affine constant
functionals per subspace, giving 5,712 theoretical pencils. Exactly 5,382 have
all five types realized. The inherited h4181 rule removes the 54 pencils whose
normal supports use at most two coordinates. The h4185 first-anchor rule removes
216 further pencils having a first-coordinate section. These are prefilters,
not reopened geometric searches. The resulting catalogue has 5,112 pencils.

The producer reconstructs this catalogue by spanning pairs of nonparallel
realized affine signatures. The checker independently enumerates all rank-two
RREF matrices. For pivot pairs (0,1),(0,2),(0,3),(1,2),(1,3),(2,3), their counts
are respectively 256,64,16,16,4,1. Each of the 357 matrices gets all 16 constant
assignments; its five projective combinations give the pencil. Distinctness,
all 5,712 theoretical patterns, realization, inherited filters, and exact
catalogue equality are checked.

The original curve numbering is reconstructed from reviewer h4163's independent
inventory and bound by a digest. A pencil's five signature buckets are disjoint.
Thus choosing one curve per bucket is in bijection with an unordered five-curve
set. Different pencils cannot count the same five-curve set, since its five
signatures determine its unique pencil.

## 2. Complete relevance of the physical exclusions

The h4193 input preserves all 6,704 h4191/h4193 physical forbidden curve pairs.
No non-four-colourable member can satisfy both curves of any such pair, at any
larger active count. These pairs are disjoint from the 8,376 h4167 pairs. The
remaining h4167 constraints include 176,420 forbidden triples.

For two nonparallel sections the containing pencil is unique. The producer
assigns each new forbidden curve pair to the pencil spanned by its signatures,
if that pencil is retained. The checker uses another enumeration: it inspects
all 3,542,760 cross-section curve pairs across all 5,112 pencils. Their complete
assignments agree, not just their totals.

Exactly 5,280 of the 6,704 pairs can occur in this retained pencil family. They
affect exactly 226 pencils. A pencil outside that set contains no newly forbidden
pair in any lift, so these new constraints cannot change its lift count. The
checker also confirms that none of the old h4167 pair exclusions can occur in
any retained pencil. Old admissibility counts there therefore depend only on
the h4167 triples.

## 3. A short obstruction for every affected pencil

The compact certificate names three distinct section positions in each affected
pencil. Let their buckets be B1,B2,B3. The checker verifies literally that

```
for every (c1,c2,c3) in B1 x B2 x B3,
at least one pair {c_i,c_j} belongs to the new forbidden-pair list.
```

All 19,504 triples across these 226 witnesses are checked. Therefore no choice
from all five buckets can avoid the new pair exclusions. This conclusion is
independent of the old triples, the two other sections, or the number of
additional active curves in a physical graph. In particular all 226 affected
pencils are completely closed to a non-four-colourable physical member.
No minimality of the three-section witness is claimed.

The producer finds these witnesses with common-neighbour bit masks. The checker
enumerates the three Cartesian factors and tests the literal pair disjunction,
without those masks. The certificate's section indices are relative to the
hash-bound canonical 5,112-pencil catalogue, so no numerical interval or
geometric guess is hidden in an index.

## 4. Exact lift subtraction

The 226 closed pencils have 3,481,088 raw lifts. The checker enumerates every
one directly. A lift is counted in the old admissible frontier exactly when
none of its ten three-element subsets is an h4167 forbidden triple; the
impossibility of the old pairs was separately checked above. The old-admissible
count is 3,064,704, with agreement for each pencil individually.

The accepted h4185/h4189 baseline has 128,871,936 admissible lifts. Subtracting
the disjoint changed subset gives

```
128,871,936 - 3,064,704 = 125,807,232
```

remaining lifts in 5,112-226=4,886 pencils. This is a count of curve sets satisfying
the stated necessary conditions, not of physical parameters or graphs.

For additional internal validation, the producer freshly counts all 5,112
pencils and reproduces the complete baseline. Its recursion stores selected
curves, the union of their forbidden partners, and the forbidden third curves
for every selected pair. At the fifth section, a bit count counts all remaining
choices exactly. The independent checker deliberately imports the accepted
baseline total and recomputes the complete changed subset by direct products;
it does not claim another independent replay of every unchanged baseline lift.

## 5. Complete pair-mode propagation

The h4193 input contains 121,480 inherited exact-five-compatible global pairs
and 7,216 already requiring at least six active curves. Every first-mode pair
has two distinct signatures and a unique retained pencil. Exactly 2,960 belong
to the newly closed pencil set. An exactly-five-active counterexample on any
one would need a lift of that unique pencil, which is impossible. Thus they
move to the existing at-least-six mode, carrying allowance 87,728.

For every other pair, both implementations produce the first admissible
extension in a fixed domain order. The producer uses forward bitset propagation;
the checker uses literal Cartesian products of the other three sections and
tests every pair and triple in the five-set. This supplies 118,520 checked
witnesses, with agreement of their complete deterministic transcript. The
checker tests 279,443 candidate extensions in obtaining them.

The witnesses prove that no further mode move follows from this constraint
set. They are not physical realizations and do not establish non-four-colourability.
Their 118,520-row table need not be published: the algorithms regenerate it and
the compact certificate binds its full transcript.

The resulting exact transformation is

| mode | before systems / allowance | after systems / allowance |
|---|---:|---:|
| exact-five compatible | 121,480 / 3,590,760 | 118,520 / 3,503,032 |
| at least six required | 7,216 / 222,672 | 10,176 / 310,400 |
| total | 128,696 / 3,813,432 | 128,696 / 3,813,432 |

No global system is deleted and the total conservative orbit allowance does
not decrease. The material reduction is the complete closure of 226 pencils
and their admissible lifts, with the consequent exact pair-mode changes.

## 6. Symmetry and trust boundary

The checker reconstructs the named D3 action from Eisenstein rows. It verifies
that the new pair exclusions, inherited pencil domain and newly closed pencil
set are invariant. It also checks every imported representative's canonical
pair and exact trivial stabilizer. The result therefore descends to the global
quotient convention. No representative is restricted to a fundamental chamber,
and no second division by symmetry is applied.

The finite certificate verification uses exact standard-library arithmetic and
explicit exhaustive loops. The physical conclusion imports the earlier pair
theorems; the baseline subtraction imports the accepted h4185/h4189 census;
global quotient completeness and orbit allowances retain the h4177/h4117/h4175
dependencies. Their status is not upgraded by this calculation. See
DEPENDENCIES.md for pinned sources. The new result is author-checked and awaits
independent reviewer-1 assessment. No <=508 record is established.
