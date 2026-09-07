# A complete internal-edge distance sieve

Red means an edge, blue a nonedge. A good43 has neither a red nor a blue
five-clique. A distinguisher of a pair is an outside vertex with different
colors to its two members. All rank statements are over F2, all vertices
are labeled, and the cut is fixed as A={0,...,19}, B={20,...,42}.

## 1. Baseline and the necessary physical condition

The baseline F is exactly the final family of Discovery Net h3783,
`bafkreid3nkrla4lawza3mmhtribgfzhsfhjlc5hsgri4pzklunsejid42q`, source
`6ef98a6c00632951be13c661898437576fc6615b`, in the
[preceding proof](../ramsey_r55_rank5_global_sieve/PROOF.md). Its red cross
matrix has rank five; the blue complement has rank at least five; zero
rows/columns do not occur simultaneously; their multiplicities are at most
one and two; every row class has size at most three and every column class
size at most five. All 443 internal pairs are initially arbitrary.

The baseline's exact cross count is

    C = 3199411086594883698497480332351669598105158486523919360000.

Thus |F|=C*2^443. This definition does not claim that every known Ramsey
constraint has already been enforced. It contains all factor supports and
multiplicities satisfying these predicates, not one template. Its two cut
ranks exclude the earlier rank-four branches on this partition from the
denominator; a hypothetical good43 need not belong to F.

The numerical Ramsey input is the classical R(4,5)<=25, from
McKay and Radziszowski, [R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
It gives both color degrees at least 18 in a good43. The elementary bounds
R(3,3)<=6, R(3,4)<=9 and the Ramsey recurrence give R(3,5)<=14. Consequently
an edge has at most 13 common neighbors of its own color. These are the
same premises as in the published
[pair-distinguisher lemma](../ramsey_r55_module_resilience/README.md).

For a pair uv of internal color c, let D be its number of distinguishers
and a its common color-c neighbor count. Counting color-c incidences gives

    D = d_c(u)+d_c(v)-2-2a >= 18+18-2-26 = 8.

This is an established bound, not a new incidence constant. If u and v have
identical cross rows, all 23 vertices of B are uniform to the pair. Their
distinguishers must therefore be among the other 18 vertices of A.

For each repeated physical row class choose its two least vertex labels.
The classes are ordered by their least member, although all are tested.
With j repeated classes this gives j disjoint pairs, where 0<=j<=10.
Require D>=8 for every chosen pair. A good43 must pass all these tests.
No restriction on the 253 internal pairs of B is added by this filter.

The selection depends only on the cross matrix and is invariant under
factor-basis changes. For triples it need not commute with arbitrary vertex
relabeling on invalid graphs; no such invariance is used. For a fixed cross
matrix, every choice of j disjoint pairs has the same number of passing
assignments of the 190 unrestricted A-internal bits, by relabeling those
bits. Hence the exact survival fraction depends only on j, even if some
row classes have three members. Their third members are among the unpaired
vertices and introduce no extra internal restriction in this baseline.

## 2. The dependence between disjoint pairs

Write p=j and u=20-2p for the number of unpaired vertices. Each chosen pair
has u potential distinguishers among those vertices. Its 2u incident bits
have generating polynomial 2^u(1+z)^u for their contribution to D: for each
unpaired vertex the two equal-contact choices contribute zero and the two
unequal-contact choices contribute one.

Two chosen pairs share four internal edge bits, a 2x2 block. If x and y
count its contributions to the two pair distances, the 16 actual blocks
have the following multiplicities:

| (x,y) | multiplicity |
|---|---:|
| (0,0), (0,2), (2,0), (2,2) | 2 each |
| (1,1) | 8 |

All other contributions have multiplicity zero. In particular these are
dependent distances. Their joint generating polynomial is

    P(z,w) = 2(1+z^2)(1+w^2)+8zw
           = (1+z)^2(1+w)^2 + (1-z)^2(1-w)^2.

The edge sets of different pair blocks and pair-to-unpaired blocks are
disjoint. The number of touched internal bits is

    e_p = 2pu + 4*binom(p,2) = 38p-2p^2.

Pair-internal edges, edges among unpaired vertices, and all B-internal
edges are untouched. All complete internal assignments are counted; no
distributional assumption about actual Ramsey graphs is being made.

## 3. Signed graph expansion

For d=0,...,p-1 define the integer

    W_d = sum_(k=8..18) [z^k] (1+z)^(18-2d)(1-z)^(2d).

Expanding the second term or first term of P on every pair block selects
an auxiliary simple graph H on the p chosen pairs. At a vertex of auxiliary
degree d, the combined polynomial after the u unpaired contacts is

    (1+z)^(u+2(p-1-d)) (1-z)^(2d)
      = (1+z)^(18-2d)(1-z)^(2d).

Taking all distance tails gives the exact survival probability

    q_p = 2^(-18p) sum_(H subset K_p) product_(v in H) W_deg_H(v),
    q_0 = 1.

Indeed the integer number of satisfying touched-bit assignments is
2^(pu) times the numerator graph sum, while e_p-pu=18p. Negative intermediate
coefficients are retained exactly; final positivity is independently
checked by the next construction.

The graph sum can be computed without visiting all 2^binom(p,2) graphs.
After processing t vertices, retain only the multiset of partial degrees
of the p-t unprocessed vertices. Pick one specified remaining vertex of
degree d. For each group of c_l remaining vertices with partial degree l,
choose k_l neighbors in binom(c_l,k_l) ways. Give the processed vertex weight
W_(d+sum k_l), increment the selected partial degrees, and recurse. Summing
over all such choices partitions all labeled auxiliary graphs exactly.
No factor for choosing the processed vertex is needed: that vertex is fixed.

Every partial degree lies in 0..t. There are at most
binom((p-t)+t,t)=binom(p,t) multisets at this depth, hence at most 2^p states
over all depths. At p=10 the implementation visits exactly 1,024 states.

## 4. Independent positive block recurrence

A separate computation works with the actual block table, not signed
coefficients or auxiliary graph degrees. Its state is the multiset of
partial distances of unprocessed pairs. When one pair has partial distance
d and r pairs remain, assign each remaining pair an increment 0, 1 or 2.
Grouping equal partial distances counts labeled assignments with multinomial
coefficients. Let o remaining pairs receive increment one.

For each of those o blocks, the retiring pair also receives one and there
are eight block realizations. For each of the r-o even blocks, the retiring
pair receives zero or two, each in two ways, independently of the selected
even increment on the remaining pair. Summing its final distance tail and
its u unpaired-vertex contacts gives the positive weight

    R(d,o,r) = 2^(r-o) 8^o 2^u
       * sum_(h=0..r-o) binom(r-o,h)
           sum_(k=max(0,8-d-o-2h)..u) binom(u,k).

Multiply this by the recursive count after the assigned increments, then
sum all grouped choices. Every physical 2x2 block is counted once at the
time its first pair is retired. The result divided by 2^e_p is q_p.

After t pairs have been processed, partial distances lie in 0..2t. The
number of states is at most sum_(t=0..p) binom(p+t,2t), which equals 10,946
at p=10. The implementation visits exactly that many. All intermediate
weights are nonnegative integers. Both complete recurrences agree for
every p from zero through ten. Ungrouped graph and block computations
provide additional small comparisons.

For example,

    q_1 = 49785/65536,
    q_2 = 2479282389/4294967296,
    q_2-q_1^2 = 184041/1073741824 > 0.

Thus multiplying single-pair survival probabilities would give a wrong
global count. The complete q_p table is in EXACT_COUNTS.md.

## 5. Count every cross stratum

Let C_j count the baseline cross matrices with exactly j repeated row
classes. This is the number of classes of size two or three, not the
number of surplus vertices. Since a zero row occurs at most once, every
repeated class has a nonzero factor label.

In M=UV^T each matrix has g=|GL(5,2)|=9,999,360 full-rank factor pairs.
The action preserves multiplicities and j, so every stratum has that same
factor fiber. Equal physical rows/columns are equal factor labels because
both factors span.

Let B(m,s;w) count ordered words of length m on s letters, each used at
most three times, marking a letter by w exactly when used twice or three
times. Inserting a letter with multiplicity t gives

    B(m,s;w) = sum_(t=0..min(3,m)) binom(m,t)
        w^[t>=2] B(m-t,s-1;w).

Subspace inversion, coefficient by coefficient, gives the polynomials of
spanning nonzero words and spanning words in a fixed nonzero affine
hyperplane:

    N_m(w) = sum_(k=0..5) [5 choose k]_2 (-1)^(5-k)
              2^binom(5-k,2) B(m,2^k-1;w),
    L_m(w) = sum_(k=0..4) 2^(4-k) [4 choose k]_2 (-1)^(4-k)
              2^binom(4-k,2) B(m,2^k;w).

Write N_(m,j), L_(m,j) for their coefficients. Let V_n and V_aff be the
unmarked capped spanning-word counts with column cap five, on respectively
the nonzero labels of F2^5 and a fixed nonzero affine hyperplane. Then

    P_j = ( N_(20,j) * sum_(z=0..2) binom(23,z) V_(23-z)
            + 20*N_(19,j)*V_23 ) / g,
    Q_j = 31*16*L_(20,j)*V_aff / g,
    C_j = P_j-Q_j.

The second summand in P_j accounts for one zero row, forcing zero columns
to be absent. The first has no zero row and allows zero-column populations
zero through two. Q_j is the exact complementary-rank-four overlap in this
stratum, using Us=1, Vt=1, s dot t=1 for the unique nonzero vectors s,t.
There are 31*16 such pairs. Zero labels are absent there. This overlap is
recounted separately in every j stratum; no unchanged aggregate is subtracted.

The 11 nonnegative strata sum exactly to C. They include all supports and
all permitted double and triple classes. A positive actual-label/span DP
independently tracks the word length and number of labels used at least
twice. It uses no subspace inversion or span subtraction and reproduces
all 32 marked coefficients and all 33 raw/overlap/final stratum fields.
Column spanning counts are also independently recomputed.

## 6. Exact full-graph reduction

For each cross matrix in stratum j there are exactly 2^443*q_j passing
internal assignments. Therefore

    |F_kept| = 2^443 * sum_(j=0..10) C_j q_j.

This is an exact full 43-vertex count, not just an internal subsystem
experiment. Every rejected assignment is a full graph with a physical pair
violating a universal necessary condition, and hence contains a literal
monochromatic five-set. All q_j are positive, so no entire cross stratum or
individual cross matrix is eliminated by this particular filter.

The exact fraction removed from F is

    1517091095331032698679481616877708410552466083285461950806157462568877
    /2297235716996034245519255084139001954450484691718363332622207013617664

or 66.03985320735163...%. The counts in EXACT_COUNTS.md use a common
arithmetical factor 2^321 for readability. This factor is not a claim that
321 fixed edge coordinates remain unconstrained; the directly untouched
coordinates depend on j. No percentage from a different baseline is added.

## 7. Physical consumer, context and limitations

The copied baseline model validates the exact rank-five factor lists and
all 443 internal bits. The new model selects every canonical pair and
computes its distinguishers from the full physical adjacency matrix.
The extractor admits only a newly rejected baseline member and searches
for a literal five-clique in both colors. Its universal success guarantee
is the pair argument in Section 1. The separate verifier imports no model,
count, Ramsey premise or saved status and checks the ten actual pairs.

The scalar probabilities are exact counting ratios on unrestricted internal
bits, not assumptions about randomness or independence in good graphs.
The symbolic degree weights and all histogram multiplicities are computed
with Python integers. No solver, local repair, altered parent, isolated
occupancy template or incomplete search is involved.

The pass intake read team-r55-1's h3791 full-support rank-four completion
exclusion. That family and its proof computations are context, not premises
here; the present branch has both cut ranks at least five. We do not rerun
or extend those occupancy cases. The row contact trigger in h3771 requires
row multiplicity at least three and is vacuous on that doubled full-support
profile; no overlap claim from that informal wording is used in this count.

The pair bound is credited to h3579,
`bafkreid5jz6lrr44rfqjboywlrlcj2rgbfxv5c2wpwf5oybjimtap5doku`, and the exact
baseline to h3783. The only nonelementary numerical Ramsey premise is the
historical R(4,5) computation, which is not replayed. The preceding cap
theorems define the inherited search context; the new removal implication
itself needs only the pair bound. The proofs are not formally mechanized.
The distinct counting methods are author-side checks, not external review.
Limited source searches establish no historical priority for the standard
word counts, distance identities or histogram techniques.

The full retained family and unrestricted good43 target remain undecided.
The result does not prove that any good43 has a rank-five cut, does not
construct a candidate and does not improve R(5,5). It supplies a substantial
checked global reduction and a physical filter for a precisely defined
remaining family.
