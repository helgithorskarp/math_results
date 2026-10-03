# An exact quadruple lift for the remaining size24 character balances

Actual author **six-vdw-3**, role **researcher**, pass32, 2026-10-03.
New ordinary author-checked reduction; unformalized and not independently
reviewed. No new finite census or coloring is asserted. The separate
119-edge computation and its threshold-four cover have completed.

Let G be the prime617 square/nonsquare ratio graph defined in
[PROOF.md](PROOF.md). Let A0 be five selected rows, anchored
at field row1, let C be their ENTIRE common neighborhood, and write c=|C|.
For each row i, let u_i be the number of physical columns outside C
missing exactly that row of A0. Put b=sum_i min(2,u_i).

**Lemma.** Suppose each A0 row is missed by at most2 selected columns,
the selected outside-column count k is at least9, and c>=2. Then A0
contains an anchored four-row subset whose entire common neighborhood
has size at least4. In fact at least two such subsets can be obtained
by deleting nonanchor rows with u_i>=2. Consequently every such A0
is obtained by extending a tuple in the complete threshold-four
anchored four-row family by one arbitrary physical row.

**Proof.** A selected outside column misses at least one of the five
rows. At most b of the selected columns can be singleton-missing;
the others consume at least two units of total row capacity10.
Therefore 2*k<=10+b, so b>=8. If at most two rows have u_i>=2,
then b<=2*2+3*1=7, a contradiction. At least three rows have
u_i>=2, and at least two are different from the anchor row1.

Delete any such nonanchor row i. A column common to the other four
rows is either in C or misses exactly row i. Hence the deleted
quadruple's ENTIRE common neighborhood has size c+u_i>=c+2>=4.
It retains anchor1 and belongs to the complete increasing anchored
four-row family. The removed row is a physical row outside that
quadruple. Append it at any position and sort the full five-row tuple.
No additional normalization, ordering assumption, or coloring symmetry
is used. This proves coverage of every anchored eligible prefix. QED.

If k=10, b=10 and all five rows have u_i>=2. Then every nonanchor
deletion qualifies. The proof needs only the capacity bound; it does
not claim that exchanging selected columns preserves an interval
coloring or that a capacity-compatible prefix is attainable.

## Exact application to the two remaining balances

For11/13 with missing budget23 and fifth least missing degree2,
S5<=10 implies |B0|>=3 and c>=3. A missing c=3 prefix necessarily
has |B0|=3 and k=10. The lemma covers it, and every nonanchor
deletion has common size at least5. All c>=4 prefixes already belong
to the complete threshold-four five-row family.

For12/12 with missing budget24 and fifth least missing degree2,
S5<=10 implies |B0|>=2 and c>=2. At c=2, |B0|=2 and k=10.
At c=3, |B0| is2 or3 and k is10 or9. These are exactly the small
common cases, and the lemma covers all of them. At c=2 every
nonanchor deletion has common size at least4; at c=3 at least two
nonanchor deletions have common size at least5. Again c>=4 is
already in the existing threshold-four five-row family.

Thus a NEW complete threshold-three or threshold-two closure queue
is not necessary for either degree-two branch. Its role can be
replaced by a lossless extension of the already checked anchored
four-row family, followed by exact physical-capacity checks.

## Quantified future census and limitations

The complete threshold-four checker independently visited exactly
64,108 anchored four-row tuples with whole common size>=4, in
normal and optimized Python. Each has exactly308-4=304 possible
physical fifth rows. Therefore at most **19,488,832** raw labeled
quadruple-extension trials cover the new small-common prefixes.
This is an exact count of the proposed raw trial domain, not a
count of distinct five-row prefixes, admissible cores, supports,
or colorings. Distinct ordered presentations must be deduplicated
as sorted physical five-row sets after their whole common sets
and capacities have been recomputed. Never require the new fifth
row to exceed the quadruple's largest label.

The numerical64,108 premise is in the fully checked threshold-four
record and the compact candidate packet's [COVER.md](COVER.md)/[EXPECTED.json](EXPECTED.json).
The checker is [check-character617-threshold-four.py](check-character617-threshold-four.py): increasing
tuples retain a branch exactly when its whole common size>=4.
Every qualifying final quadruple has qualifying intermediate
prefixes, so that recorded count covers the stated tuple family.

The concrete next computation is to regenerate this complete
quadruple family independently, partition its304-row extensions
into bounded disjoint stages, filter only c=2 or3 with the stated
physical row capacities, and compare complete physical tuple sets
and exact column-factor coefficients. All nineteen million trials
remain PLAN ONLY here. No native input, resource escalation,
failed-range retry or new computation is part of this lemma.

The degree-one and degree-three branches retain their separate obligations;
this lemma does not exclude them. The actual interval lift, independent
root occurrences and outdegree premise still require credited9880.
This reduction changes neither the existing24-flip lower bound nor the
119-edge theorem, and establishes no25-flip bound, feasible24-support,
3704-point coloring or numerical improvement of W(2,7).

## Closed physical coefficients and the exact tail gate

For a fixed eligible prefix, let v_ij be the number of actual outside
columns missing exactly rows i and j. With the five capacities equal to2,
the number of physical ten-column selections is exactly

    P10 = product_i binomial(u_i,2).

Ten noncommon columns consume at least10 units. Since total capacity is10,
all columns are singleton-missing and each row is missed exactly twice.
The disjoint singleton types give the product above.

The number of physical nine-column selections is exactly

    P9 = sum_i u_i * product_(j!=i) binomial(u_j,2)
         + sum_(i<j) v_ij*u_i*u_j
                          * product_(l not in {i,j}) binomial(u_l,2).

Nine columns have total missing cost9 or10. In the first case all are
singletons: four rows are missed twice and one row once. In the second
case there are eight singletons and one double-missing column: the two
rows of its missing pair each receive one singleton and the other
three receive two. More double columns or a triple column would exceed
total capacity10. These cases are disjoint and exhaustive, and the
formula counts every physical choice with all labels. A zero binomial
coefficient correctly handles unavailable choices. For a common set of
size c and a selected subset of size s, multiply by binomial(c,s) to
count labeled (prefix,B) incidences, retaining each actual B0 separately.

For11/13's small-common degree-two branch, c=s=3 and k=10.
Every counted B13 has S5=10. Its six additional least-order-compatible
rows each have degree>=2; budget23 permits only six degree-two rows,
or five degree-two rows and one degree-three row.

For12/12, c=2,s=2 and c=3,s=2 both have k=10,S5=10.
Budget24 forces all seven added rows to have degree exactly2.
For c=3,s=3,k=9, the all-singleton term has S5=9 and permits seven
degree-two rows, or six degree-two rows and one degree-three row.
The one-double term has S5=10 and forces all seven added rows to have
degree2. These degrees are measured into the FULL actual selected B,
including B0. The outside columns always lie outside the ENTIRE C.

Thus the future small-common computation can enumerate physical column
sets using P10/P9, then apply the stated exact added-row degree gate.
No large weighted six- or seven-row subset enumeration is needed for
these branches. Formula counts, prime617 evaluations, column censuses
and exclusions remain uncomputed here; these ordinary consequences
provide a lossless finite plan, not a negative result for either balance.
The additional bad-edge restrictions in [WEIGHTED_ENDPOINTS.md](WEIGHTED_ENDPOINTS.md) can be
applied to each physical prefix-column choice and its tail degree gate.
