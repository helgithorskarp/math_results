# Small-common exclusion for24-column prime617 repairs

Actual author **six-vdw-3**, role **researcher**, 2026-10-03.
The finite calculations are author checked by independent implementations.
The deductions are ordinary and unformalized; independent-person review of
this new result is pending.

## Statement

Let S,T be the nonzero squares and nonsquares of F617. For
delta in {285,314,362,381,409,570}, form the six physical endpoint sets
{1+j*delta:1<=j<=6}. Let V be their union and D=V union V^-1. Then
|S|=|T|=308, |V|=33, V intersect V^-1 is empty, and |D|=66.
The graph joins q in S to t in T when t/q belongs to D.
Put

```
V_bad={192,239,286,336,383,430},
D_bad=V_bad union V_bad^-1.
```

These twelve ratios are the unique parts of the first and sixth endpoint
sets. Other edges are good. For selected A,B let E be the edge count and
E_bad the bad-edge count. Let missing degrees be measured into the entire
selected B. Take ANY five least-missing rows A0 of A, with all ties retained,
and let C be their ENTIRE common neighborhood in T.
When the original smaller class is nonsquare, simultaneously multiply all
labels by a nonsquare to place it in S; every ratio and edge type is preserved.

**Exact finite theorem.** Suppose (|A|,|B|) is (11,13) or (12,12),
E>=120, and 2E-E_bad>=240. If the fifth least missing degree is exactly2,
then **|C|>=4**.

**Actual-coloring corollary.** In an AP7-free binary coloring of [1,N],
N>=3702, relative to one constant-phase affine quadratic character of
prime617, a nonempty actual nonroot flip support of size24 has balance
11/13 or12/12 by the preceding published119-edge theorem. In its smaller
class (either class when balanced), a least-five prefix whose fifth
missing degree is2 must now have at least four entire common neighbors.
The original root occurrences remain independently free. Edits may vary
between occurrences of a residue column; a column is counted only when
at least one actual point changes.

This removes the two- and three-common-column rank-two branches. It does
not exclude the larger-common branches, different fifth degrees, a whole
balance,24-column repairs,25-column repairs, or arbitrary AP-free words.
It gives no new numerical W(2,7) bound or coloring of [1,3704].

## Dependencies and actual-position bridge

[The endpoint lift9880](../character617-flip-rigidity/PROOF.md) proves that
every actual changed point has the required interval representative of
each nonconstant field endpoint progression when N>=3702. Each of the
six endpoint sets must therefore contain a selected outgoing neighbor.
The first five sets are disjoint, giving at least5m graph edges for m
flips. The directed ratio set V is disjoint from V^-1, so the counted arcs
are different underlying graph edges.

[The weighted endpoint lemma10086](../character617-balanced24/PROOF.md)
also gives 2E_good+E_bad>=10m, equivalently 2E-E_bad>=10m. A minimum
five-neighbor hit uses one neighbor from the shared triple
{477,524,571} and one from each of the four disjoint middle groups.
If the shared triple is omitted, both unique bad groups must instead be
hit. With weights2 for good edges and1 for bad edges, every vertex's
outgoing hit therefore has weight at least10. Summing gives the bound.
For m=24 these are precisely the theorem's two inequalities.

The same published10086 proves at most119 edges for10/14, excluding that
balance. [Review9976](../../six-reviewer-4/quantized617-audit/REVIEW.md)
supplies the earlier three-balance cover relative to its explicit9880/9904
premises. Those earlier reviews do not review this new calculation.
The abstract finite theorem above needs only its explicitly stated graph,
balance, missing-degree and weighted-edge premises.

## Complete physical prefix cover

The first five missing degrees are at most2, so their sum S5<=10.
Every additional selected row has degree at least2. Write B0=B intersect C,
s=|B0| and k=|B|-s. Every selected column outside ENTIRE C misses at least
one prefix row, so k<=S5. For11/13 with |C|<=3 this forces
c=s=3,k=10,S5=10. For12/12 it forces c>=2 and leaves exactly:

|c|s|k|outside missing pattern|S5|
|---:|---:|---:|---|---:|
|2|2|10|ten singletons|10|
|3|2|10|ten singletons|10|
|3|3|9|nine singletons|9|
|3|3|9|eight singletons and one double|10|

Define U_i as columns outside C missing exactly prefix row i; define
U_ij as columns outside C missing exactly i,j. These are disjoint PHYSICAL
column classes. Put b=sum_i min(2,|U_i|). With k>=9 selected outside columns,
at least2k-S5>=8 of them are singletons. Per-row capacity2 gives b>=8.
At least three U_i thus have size>=2, including at least two nonanchor rows
after normalizing a prefix row to1. Deleting either such row leaves an
anchored quadruple whose entire common set C union U_i has size>=4.

Thus adding ALL304 physical fifth rows to every anchored threshold-four
quadruple covers every possible c=2/3 prefix. Insert the added row at ANY
label position and sort; no increasing-addition restriction is valid.
Two direct exhaustive implementations give the same **64,108** quadruples.
The first traverses increasing second rows, with compact column indices;
the second traverses descending largest rows, with physical field bit
positions, brute inverses and a different pruning order. A prefix common
intersection only shrinks when a row is added, justifying every prune.
Both implementations run in normal and optimized Python. Their merged
physical record digest is
`4c46d92606b10aea72510c503244c5f97ccd3fb1354db2b302b7fefc2d8a537c`.
The separately checked older closure-derived quadruple stream also agrees;
it is not a required input to the new source reproduction.

All **19,488,832** presentations (64,108 times304) are covered. They yield
317,880 capacity-bearing presentations and **105,590** distinct physical
prefixes:85,670 with c=2 and19,920 with c=3. The producer intersects literal
four-row masks. Its independent checker subdivides four-row columns by
their16 missing patterns, extends these to32 five-row patterns, and counts
the allowed physical occupancy vectors. All entire records, not only
counts or hashes, agree in normal and optimized Python.

## Weighted physical column coefficients

For a prefix define h(t) as its number of bad edges to actual column t.
All counts use nonnegative integer polynomials modulo y^3. For U_i put

```
L_i(y)=sum_(t in U_i) y^h(t),
Q_i(y)=sum_({t,u} subset U_i,t!=u) y^(h(t)+h(u)).
```

If n_r counts columns in U_i of cost r=0,1,2, then
L_i=n0+n1*y+n2*y^2 and
Q_i=C(n0,2)+n0*n1*y+(n0*n2+C(n1,2))*y^2.
For U_ij put L_ij=sum_(t in U_ij)y^h(t). The disjoint cases are

```
F10 = product_i Q_i,
F9_single = sum_i L_i*product_(j!=i)Q_j,
F9_double = sum_(i<j) L_ij*L_i*L_j*product_(k not in {i,j})Q_k.
```

Multiply by y^(sum_(t in B0)h(t)). All three PHYSICAL B0 subsets are
retained when c=3,s=2. Truncation discards only costs that later nonnegative
costs cannot reduce. The independent checker inserts individual actual
columns with occupancy limits0/1/2, without importing the polynomial
producer. A separate selector recomputes every original unweighted
coefficient before agreeing on all16,880 relevant prefix records.

The permitted tails and weighted budgets follow directly from total
missing counts M=|A||B|-E and 2E-E_bad>=240:

|balance|prefix deficit|additional missing degrees|E|total bad budget|
|---|---:|---|---:|---:|
|11/13|10|six2|121|2|
|11/13|10|five2 and one3|120|0|
|12/12|10|seven2|120|0|
|12/12|9|seven2|121|2|
|12/12|9|six2 and one3|120|0|

Every selected tail row has degree>=2, so this list is complete for these
prefix cases. In particular no higher-E case is possible here. The E=121
common-source endpoint restriction is not needed: the cost<=2 relaxation
already contains every admissible prefix choice.

The complete weighted coefficient sums are:

|physical anchored prefix/column incidence|count|
|---|---:|
|11/13:c3,s3,k10, cost<=2|4,540|
|12/12:c2,s2,k10, cost0|2,015|
|12/12:c3,s2,k10, cost0|3,270|
|12/12:c3,s3,k9,double, cost0|52,590|
|12/12:c3,s3,k9,single, cost<=2|43,820|

These are **106,235** necessary incidences across1,860 anchored prefixes,
not admissible supports or interval colorings.

## Exact scalar quotient and literal tail contradiction

Simultaneous multiplication of row and column labels by a square preserves
all edge types, missing patterns, costs and tail degrees. A stabilizer of a
five-row set has order dividing both5 and308; therefore it is trivial.
Exactly five distinct versions are anchored at1, using inverse scalars of
the five rows. The least sorted version is a unique representative.
An independent checker visits all308 scalars and verifies every transported
physical B0 choice and full coefficient vector. It agrees in normal and
optimized Python. This is a symmetry only of the necessary field graph;
no interval coloring or occurrence edit is quotient-ed out.

There are **372** representatives, with542 distinct physical selection
cases and **21,247** canonical column incidences:908 for11/13 and20,339 for
12/12. For each case the generator lists all distinct physical B subsets
within its exact weighted coefficient budget, in strict lexicographic
order. The independent checker reconstructs adjacency by direct field
division, checks every B subset's nonsquare labels, ENTIRE-C membership,
missing pattern and bad cost, and tests all308 physical rows.

For each case, the valid distinct list size equals its separately proved
weighted coefficient. Membership, strict uniqueness and that exact
cardinality prove completeness; hashes alone are not used to infer it.
The merger checks contiguous coverage across all43 rank batches and strict
uniqueness across their boundaries, then compares every whole producer,
literal-normal and literal-optimized transcript.

**No tail survives.** Over all908 canonical11/13 incidences, at most **one**
outside-prefix row has missing degree2. Over all20,339 canonical12/12
incidences, at most **two** such rows exist. The complete tail table above
requires at least five degree-two rows for11/13 and at least six for12/12.
This is a contradiction in every case, proving the theorem.

The complete canonical physical tail record-stream SHA256 is
`9cccffac4760028130522a8b5565d8a9277fdd882d8aa9e8a29824612fe4031a`.
It is computed from canonical JSON of each ordered physical record,
followed by a newline. Compact expected results and source pins are in
this directory; the large full transcripts are regenerated locally.
The literal checker and merger also pass two intact controls and reject
fifteen genuine semantic damages per mode. These include changed physical
columns, missing or injected tail rows, forged bad counts and tail gates,
and truncated, overlapping or empty coverage. These are author controls,
not independent-person review.

## Reproduction, limits and literature

[README.md](README.md) gives the stdlib-only commands and trust boundary.
All mathematical children used threads1,20-second guards and the existing
1CPU/2GiB scope. The original incorrectly offset preliminary graph input
was rejected before enumeration and remains frozen. A later128-quad
literal checker lost its completion receipt during an interruption and
remains UNKNOWN. Only two disjoint completed64-quad replacements establish
that range's coverage. Neither failed input was retried under a different
path or counted as an exclusion. The public replay uses64-quad parts.

[Monroe's primary Table1](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
still lists length7/two colors>3703, and Table2 identifies prime617
(checked2026-10-03). His W(7,2) notation is length-first; here W(2,7) is
color-first. The underlying discrete-logarithm and cyclic-zipper context
is described by [Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf).
[Heule's asymmetric w(3,k) paper](https://www.cs.cmu.edu/~mheule/publications/JOC_08_03_A01.pdf)
concerns a different problem. These sources and bounded recent campaign
evidence are a literature/context check, not an exhaustive historical
priority claim. The new theorem is a restricted structural refinement;
the symmetric seven-term numerical frontier remains open here.
