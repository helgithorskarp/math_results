# Two entire three-original Q inventories obstruct large common tail support

Author: **six-covering-1, researcher**. Ordinary conditional counting proofs,
with separate definition-level exact audits. Unformalized; independent external
review pending. The bounds below are not claimed sharp.

## Model and results

Let F={t modulo180: t is not3 modulo9}. Take five copies of F. One copy is
marked and may receive at most one additional whole modulo9 row. Every ORIGINAL
label d dividing720, d not in{1,2,4}, is a separate resource. There are27 labels.
A resource may be omitted or spent in one copy, using one phase modulo
e=d/gcd(d,4). Its support is that class intersected with F. Inactive physical
phases have empty support. Equal projected moduli remain different ORIGINAL
resources, with separate ownership and phase choices.

Write C_s for each copy's union, including its possible supplemental row, and
K for the intersection of the five unions. Suppose an UNMARKED copy Q has
one of the following ENTIRE original inventories, with no additional original
label spent there:

1. {d3,8,720}, d3 in{3,6,12}. Then |K|<=110.
2. {d3,8,d5}, d3 in{3,6,12}, d5 in{5,10,20}. Then |K|<=106.

Reserved Q resources may have empty support. All remaining originals, owners,
phases and omissions are free. There is no binary-core ownership assumption,
no required placement of16,48 or144, and no restriction on which of the other
four copies is marked. These are conditional obstructions to construction
templates. They do not normalize all distinct coverings to these inventories,
prove a global LCM15120 exclusion, or change bounds for L_min(8). Minimum
EXACTLY8 remains separate from minimum AT-LEAST8.

The physical interpretation uses x=4t+3 modulo720 and five native copies
s=0,...,4 corresponding to x modulo7 equal to s+2. For projected phase r put
b=(4r+3) modulo d. The ORIGINAL progression is

    A modulo7d, A=b+d*((s+2-b)*inverse(d modulo7) modulo7).

All these d are coprime to7. The marked row models one effective TOP-completion
resource, not a second independently selectable original63. The earlier model
is in [supplemental-tail support](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-1/supplemental63-tail-support/proof.md).
The separate [entire four-original Q obstruction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-1/entire-q-tail-bound/proof.md)
motivated the present change of construction inventory. Its numerical bounds
are not premises in either proof here.

## A monotone resource cost

For a target S and a prefix P of resources in the four copies other than Q,
give original i a credit w_i at least as large as every possible phase footprint
on S. Give the possible supplemental row credit20. Define

    cost_S(P)=sum_{i in P}w_i
              -sum_{four copies s}|union_{i in P} D_i(s) intersect S|.

An omitted, inactive or unavailable resource has empty support. Cost is
nonnegative. Adding a resource increases cost by its credit minus its marginal
newly covered incidence. That increment is nonnegative, and can only increase
if more supports have already been added in the same copy. Overlaps belonging
to different pairs are never assumed additive.

If all four copies cover S, the full-pool cost is total credit minus4|S|.
Every prefix must have at most that cost. Also, if K is a subset of S, then
cost_S(P)<=cost_K(P). This lets the second proof work on a whole Q footprint
without enumerating or guessing which subset becomes the common support.

## Singleton Q: the only possible111-point target

The three projected Q resources are3,2,180. The modulo3 colour populations
in F are40,60,60, and each parity has80 points. A colour0 plus a parity covers
100 points. A positive colour a plus a parity p covers110. The original720
resource adds at most one point. Hence |C_Q|<=111.

If |K|>=111, C_Q=K=T must have111 points. Necessarily

    T=T0 union{z},
    T0={t in F: t mod3=a or t mod2=p},
    a in{1,2}, p in{0,1}, z in F outside T0.

There are200 such targets. In particular z has the opposite parity and is
outside the full colour a. All four other copies must cover the whole T.

The24 remaining ORIGINAL resources have the following maximum phase sizes
on T, independent of the choice of d3:

| Projected e | Multiplicity | Credit per original |
|---|---:|---:|
| 3 | 2 | 60 |
| 4 | 1 | 40 |
| 5 | 3 | 23 |
| 6 | 1 | 30 |
| 9 | 3 | 20 |
| 10 | 1 | 16 |
| 12 | 1 | 15 |
| 15 | 3 | 12 |
| 18 | 1 | 10 |
| 20 | 1 | 8 |
| 30 | 1 | 6 |
| 36 | 1 | 5 |
| 45 | 3 | 4 |
| 60 | 1 | 3 |
| 90 | 1 | 2 |
| Total | 24 | 432 |

These are CRT fibre counts. For example, parity p contributes16 points in
each modulo5 column and40 in each modulo4 class of that parity. The full
colour contributes12 per modulo5 column,15 per modulo4 phase and20 per
modulo9 row. Their union T0 has22 points in every modulo5 column. Only the
column of z has23 in T. A non-full-colour modulo9 row has at most11 points.
Full-colour fibres give the other displayed maxima; every phase vector is
also independently counted by the literal audit.

Including the supplemental row, the total credit is452, while the required
four-copy incidence is444. Thus every prefix must cost at most8.

Both remaining projected3 originals must use the full60-point colour a.
Every other colour phase has at most31 points, losing at least29>8. They must
have distinct owners A and B: repeating the full colour in one copy costs60.

Original16 projects to4. A wrong-parity phase has at most16 points and loses
at least24>8. A parity-p phase has40 points and meets the full colour in15,
so it cannot go to A or B. Name its third owner C and the fourth copy D.
The prefix cost is zero.

The originals5,10,20 each give one modulo5 column of T, with credit23. On
A/B they meet12 already covered full-colour points and cost at least12. On
C they meet8 already covered modulo4 points and cost at least8. Omission
or inactivity costs23.

If a column goes to C, there can be only one such column. The other two must
go to D. Repeating a D column costs at least23. Two distinct D columns have
combined size at most45 for credit46, so they cost at least1. Thus a C column
and the other two D columns cost at least8+1=9>8. Consequently all three
columns go to D, in distinct phases. They cost2 or3.

Each projected9 original has credit20. A phase outside the full colour has
at most11 points and loses at least9>8. A full-colour row on A/B is already
covered; on D it meets the three columns in12 points; on C it meets the
modulo4 class in5. Only C is possible within the budget, at additional cost5.

A second projected9 original costs at least5 more. On C a different full-colour
row still meets5 points, while repeating the first row gains nothing. Every
other choice has cost at least9,12 or20 as above; omission costs20. The
resulting prefix cost is at least2+5+5=12>8. This proves |K|<=110. The third
projected9 original and all other unused resources remain free.

## Column Q: a whole-footprint relaxation and raw credits

The three projected Q resources are3,2,5. Replacing any empty Q phase by an
arbitrary active phase enlarges C_Q without changing the free original pool.
It is therefore enough to handle complete active footprints

    T={t in F: t mod3=a or t mod2=p or t mod5=q}.

If a=0, |T|=112 and every projected3 phase on T has at most40 points. If
a is positive, |T|=120. In that case the full colour a has60 points, the
other positive colour has36 and colour0 has24. The Q column q has32 points;
every other modulo5 column has22.

Give each original its maximum phase size on the whole F. The27 ORIGINAL
credits are as follows:

| Projected e | Multiplicity | Raw credit per original |
|---|---:|---:|
| 2 | 1 | 80 |
| 3 | 3 | 60 |
| 4 | 1 | 40 |
| 5 | 3 | 32 |
| 6 | 1 | 30 |
| 9 | 3 | 20 |
| 10 | 1 | 16 |
| 12 | 1 | 15 |
| 15 | 3 | 12 |
| 18 | 1 | 10 |
| 20 | 1 | 8 |
| 30 | 1 | 6 |
| 36 | 1 | 5 |
| 45 | 3 | 4 |
| 60 | 1 | 3 |
| 90 | 1 | 2 |
| 180 | 1 | 1 |
| Total | 27 | 600 |

The three Q resources consume credit60+80+32=172. Thus the remaining24 have
credit428, or448 including the supplemental row. Suppose |K|>=107. Since
all four other copies cover K, every prefix has cost_K at most

    448-4|K| <= 20.

Its cost_T is no larger. It suffices to show that the free originals cannot
have all prefixes costing at most20 on T. This argument keeps arbitrary
subsets K of T and every supplemental-row placement.

If a=0, the two remaining projected3 resources each intrinsically lose at
least60-40=20. Their combined cost is at least40>20. Hence a is positive.
Both projected3 resources are forced to the full colour a, since every
other phase has at most36 points and loses at least24. They must have
distinct owners, which we name A and B. Their cost_T is zero.

## Exhausting original16 and the two remaining columns

In T a projected4 phase of parity p has40 points, while a wrong-parity phase
has20. Every projected4 phase meets the full colour in15 points and the whole
column q in8 points.

A wrong-parity original16 phase has cost at least20. To stay within20, both
remaining projected5 resources would have to cost zero. Their only possible
zero-loss phase is q, since every other column has22 instead of its credit32.
Column q cannot cost zero on A/B, which already have12 of its points, or on
the original16 owner, which has8. Only one empty copy remains. Spending both
copies of q there repeats32 points. This case is impossible. Omitting or
inactivating original16 costs40 and is also impossible.

A parity-p original16 on A/B costs15. Both columns must then be phase q on
the other two empty copies: another phase costs at least10, and a placement
on A/B costs at least12. A repeated q phase in one copy costs32. Every
projected9 original subsequently costs at least4: a full-colour row meets
the q column in4 points on either new owner and is already covered on A/B;
every other row has at most12 points of T, losing at least8. The three such
originals therefore give total cost at least15+3*4=27>20.

The remaining possibility is a parity-p original16 on a third copy C. Name
the empty fourth copy D. The cost so far is zero. The first-placement costs
for a projected5 resource are exact:

| Column phase and owner | Cost_T |
|---|---:|
| q on A or B | 12 |
| other column on A or B | 22 |
| q on C | 8 |
| other column on C | 18 |
| q on D | 0 |
| other column on D | 10 |
| omitted/inactive | 32 |

Different column phases are disjoint, so these costs add when both go to
one owner in different phases. Repeating a phase in one owner costs32 for
the second resource. The complete list of column pairs with cost at most20
is given below. A/B denotes either of those owners, and "other" means a
column different from q. Each fine-row floor bounds the marginal cost of
EVERY projected9 choice after the pair, so it applies to all three originals
without assuming pairwise-overlap additivity.

| Column pair | Pair cost | Fine-row floor | Cost after three fine rows |
|---|---:|---:|---:|
| q on A/B and q on C | 20 | 0 | >=20 |
| q on A/B and q on D | 12 | 4 | >=24 |
| q on C and q on D | 8 | 4 | >=20 |
| q on C and other on D | 18 | 4 | >=30 |
| other on C and q on D | 18 | 4 | >=30 |
| q and other, both on D | 10 | 5 | >=25 |
| two distinct other columns, both on D | 20 | 5 | >=35 |

For the floors, a full-colour row has20 points. It meets a modulo4 phase in5,
one whole column in4, two columns in8, or the union of a modulo4 phase and
one column in5+4-1=8. On A/B it is already covered. Every other modulo9 row
has at most12 points of T and intrinsically loses at least8. These facts
exhaust every row and owner, including empty phases and omissions.

## The equality states cannot place all three projected15 originals

Only the first and third rows of the table can survive the budget20.
In the first, each fine original must cost zero and therefore use a distinct
full-colour row on D. In the third, each must cost exactly4 and again use a
distinct full-colour row on D. There are exactly three such rows. Repeating
one gains nothing. In both cases D now has the full colour a, and the total
prefix cost is exactly20.

The resulting state has the full colour on A, B and D; a parity-p modulo4
phase on C; and the entire q column on C and one owner E in{A,B,D}. This
includes both placements of the repeated Q column; it does not presume E=D.

The three remaining projected15 originals are15,30,60, each of credit12.
A full-colour phase is already covered on A/B/D and meets6 covered points
on C. In the other positive colour, a phase in column q has12 points and
can gain12 only on the TWO owners without the q column. These are the only
two zero-cost slots. Its other column phases have6 points. A colour0 phase
has at most8 points, also fewer than its credit12.

Repeating a zero-cost slot gains nothing a second time. Three distinct
original resources can therefore gain at most12+12+8=32 for credit36. Their
additional cost is at least4. The prefix cost exceeds20, a contradiction.
Thus |K|<=106.

## Exact audits and their trust boundary

The two standalone Python audits import no previous research code, native
builder, solver or generated corpus. They compare every original residue
modulo7d directly on period5040 with its projected F footprint:16,877 maps,
3,225 nonempty and13,652 empty;3,495 are gate-compatible. The latter count
includes projected phases landing on the deleted row. Original aliases and
both erased native copies are retained.

For the singleton proof, audit_parity.py checks all1,080 canonical Q phase
tuples, all200 high targets and all three ORIGINAL Q types. It compares all
308,400 typed original phase-capacity entries. Its monotone local pruning
accounts for3,704,400 column owner/phase/omission triples, with24,000 feasible
ordered triples. All4,000 distinct column-prefix states,148,000 first fine-row
options and444,000 second options are checked. The smallest final cost is12.

For the column proof, audit_column.py has five disjoint partitions q=0,...,4,
covering all30 canonical Q tuples,20 positive footprints and10 colour0
footprints. It checks all nine ORIGINAL inventory types and186,030 typed
phase entries. Its149,940 local modulo4/column-pair tuples retain omissions,
all owners and all phases. Complete monotone fine-prefix accounting covers
194,507,520 nominal LOCAL fine-row triples, using1,631,840 visited prefix
states. The2,880 equality survivors contain all three possible E owner types.
All881,280 visited projected15 prefixes fail to complete the three resources
within the budget. These are local arithmetic audits, not full-allocation or
K-subset enumeration. Copy renaming only names the two forced full-colour
owners; the proof disregards marked-row location, so no marked-copy symmetry
assumption is required.

Normal and optimized Python outputs agree as complete records and complete
entry-stream digests. The ordinary proofs supply the universal implications
within the stated inventories. They are not formalized, and matching runs
by the same author are not independent external review. The initial singleton
checker had an incorrect expected phase census; its failed run is preserved
privately and is not a premise. The corrected standalone source regenerates
the full mathematical records without that failure or any private input.

## Literature and construction consequence

[Zhang and Zhang, Least common multiples of distinct covering systems](https://arxiv.org/html/2607.19029)
provides the L_min definition and the known minimum-seven value10080; that
published result is context, not a new claim or an imported numerical premise
here. The companion [distinct-covering source](https://arxiv.org/html/2605.18644)
was checked for current context. No priority claim or higher-minimum record
claim is made.

The two entire three-original inventories above cannot reach common111,
and the column inventory cannot reach107. Together with the separately proved
four-original inventory obstruction, this rules out reusing those templates
for a common111 construction. Other Q inventories, joint BASE/TOP gluing,
LCM10080 and15120, and the global minimum-EXACTLY8 problem remain open in this
work. There is no full covering or new universal exclusion in these files.
