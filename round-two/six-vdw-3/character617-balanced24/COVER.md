# Complete least-five-row and capacity cover

Actual author **six-vdw-3**, role **researcher**, 2026-10-03. This ordinary
reduction and exact computation is part of the [119-edge theorem](PROOF.md).
It is author-checked with separate implementations, unformalized, with
independent-person review pending.

Use the graph G and missing-count notation of PROOF.md. Assume |A|=10,
|B|=14 and M<=20. The five least-missing rows A0 have fifth degree exactly
2, all prefix degrees <=2 and all other selected degrees >=2. Their whole
common neighborhood C has size <=8 and B0=B intersect C has size >=4.
Normalize one prefix row to 1 on the necessary field graph, retaining all
physical labels and ties.

## Singleton replacement and physical column coefficients

For a finite labeled family of nonempty missing subsets of r rows, with
integer row capacities c_i, let u_i be the available singleton multiplicity
at row i. Some maximum-cardinality selection contains min(c_i,u_i)
singleton items at each row. If an unused singleton has an unfilled row,
add it, contradicting maximality. If its row is full, then either all
selected items there are singleton, in which case its target has already
been reached, or replace an incident nonsingleton by the unused singleton.
Cardinality is preserved and other capacities are released. Repetition
increases singleton count without removing any selected singleton. This
proves the assertion for every row. It is a local capacity relaxation,
not a transformation preserving an actual coloring.

Here r=5 and c_i=2. Put b=sum_i min(2,u_i). Any outside-column selection
has at most floor((10+b)/2) items: at most b are singleton and every other
item consumes >=2 units of total capacity 10. After filling these singleton
slots, the producer computes the exact maximum with at most 3^5 residual
capacity states. The checker instead multiplies the full 31-type physical
column polynomial, including every singleton and nonsingleton type with
binomial multiplicities. Every row exponent stays <=2. Coefficients count
physical selections separately for each outside size; labels are retained.

## Complete threshold-four domain

The producer starts with the whole neighborhood of row 1 and intersects
each queued state with every one of the 308 row neighborhoods, retaining
intersections of size >=4. The queue is exhausted at 47,347 distinct
closed states, 14,582,876 tested transitions and 556,347 retained
transitions. Full square closures have maximum size 12. Every hypothetical
K13,4 can be normalized at a row, and its common neighborhood is visited
by these intersections, so this also proves no K13,4.

All 76,735 increasing anchored five-row tuples are extracted, with full
common-size histogram 4:65090;5:9960;6:1420;7:240;8:25. In particular,
there is no K5,9. The independent checker reconstructs literal ratio
adjacency from squares and Euclidean inverses and visits every increasing
anchored tuple, pruning only when its whole common set has size <4.
Every qualifying final tuple has all intermediate common sizes >=4, so
this covers all final tuples. Retained tuple counts for sizes 1 through 5
are 1,305,15801,64108,76735; extension trials are
307,46553,1571548,4543974. Every final tuple and whole common set equals
the producer's record; all closed states and retained transitions are
also checked. The source runs these checks in normal and optimized Python.

Canonical state digest:
`e28ce01b7aab42b857aebe0e8f89c12103eb2ffdb6a6ab87fbdd0b7fb4140c19`.
Canonical five-row digest:
`91e05116779017c8c5ed60a23094a1cc3cfc15a8193aa5c010151916253d4f4b`.

## Capacity cut and complete C4 exclusion

The exact local capacities reduce 76,735 prefixes to 1,070:
110 full-C4, 340 full-C5, 415 full-C6, 180 full-C7 and 25 full-C8.
All selected common sizes are covered, with 3,900 labeled (A0,B0) cores.
The independent full column-factor calculation checks all prefixes and
every positive maximum, admissible common size and corresponding count.
There are 10,698,760 labeled (A0,B14) incidences, not distinct supports,
feasible colorings or orbits. The canonical capacity record digest is
`709c375afac0a4fb76946d5590df22bd23b26eb2334049b01f121f4b31e6b768`.

If |C|=4, B0=C and all ten outside columns must be singleton-missing.
Each prefix row is missed twice and S5=10. M<=20 and the remaining rows'
degree >=2 force all five remaining selected rows to have degree exactly
2. All 110 eligible prefixes give 660 physical B14 choices: 650 have no
such added row and 10 have only one. None has five. The producer and
literal checker enumerate all labeled pairs of singleton columns per
row. Independent binomial-product counts certify completeness for each
prefix. Canonical record digest:
`70ccee54b99dd3967dfcbb99e6b816023087fd13dfe01876a3ec7199bb014fef`.
Thus C4 is impossible.

## Complete C5 exclusion

If |C|=5, the selected common size is 4 or 5. At size 4 the ten outside
columns are all singleton-missing. At size 5, nine outside columns and
S5<=10 require either nine singletons or eight singletons plus one
double-missing column. These exhaust the patterns under five capacities
2. Across all 340 prefixes, the three physical counts are 150, 1950 and
35920, totaling 38,020 B14 choices.

For each B14, all five additional selected rows have missing degree >=2.
The prefix's S5 plus the five smallest such degrees among all 303
additional rows is a necessary lower bound for M. Its complete domain
minimum is 28>20. This 28 applies to the stated C5 prefix domain, not
arbitrary 10-by-14 subgraphs.

The checker verifies every actual column set, B0=B intersect C, capacity
bounds, uniqueness and exact coefficient count for each prefix and
selected common size. Legality, uniqueness and equality to the complete
physical factor count prove no omission. It adds literal reverse-adjacency
columns with bit-sliced counters and reconstructs every row deficit and
lexicographic five-row minimizer. The producer uses row-intersection
population counts. All 4096 small three-row/four-column counter fixtures
are checked. Canonical record digest:
`88612d5977b3f0ae9e9af7e1aa2ee2288e2bf840a871004193a9408d2d43f9ba`.
Thus C5 is impossible.

## Remaining exact domain and controls

The remaining 620 prefixes and 3,400 labeled cores are:

| Full common size | Prefixes | (A0,B0) cores | Labeled (A0,B14) incidences |
| --- | ---: | ---: | ---: |
|6|415|895|239430|
|7|180|1300|1246740|
|8|25|1205|9173910|

The 10,660,080 incidences are a necessary-prefix count. A B14 may recur
with different A0. Every remaining core has |B0|>=5. PROOF.md completes
the five additional rows and exact relaxed column minima for this domain.

In both modes, 3699 exhaustive small singleton-replacement fixtures use
literal item subsets as an oracle. Eleven repaired-digest semantic damages
per mode reject for their intended mathematical reasons; three valid
checker controls per mode pass. These controls supplement, rather than
replace, the complete prime-617 finite checks. All checkers use explicit
exceptions, including under Python optimization.

The entire cover and subsequent row computation are regenerated by the
single command in README.md. Inputs are source only; large generated
record lists, queue checkpoints and logs remain in the chosen work
directory. Fixed 20-second mathematical child guards, one child at a time
and numerical threads one are preserved. Canonical digests are compact
regression summaries; complete independently reconstructed records are
the checking mechanism.
