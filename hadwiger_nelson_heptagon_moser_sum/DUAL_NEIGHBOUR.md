# Common neighbours in both factors and the remaining contact indices

**Subsequent complete cohort closure:** [CONTACT_ENVELOPES.md](CONTACT_ENVELOPES.md)
closes all 126 proposed unit-M contact equations using exact elimination
supergraphs and explicit four-colourings. Only both-nonunit contacts
remain, with a bound of 6720 angles or 960 sevenfold-rotation classes.
The earlier assessment below retains its historical scope.

**Theorem.** Use the fixed 21-point H and seven-point M from
[PROOF.md](PROOF.md), with their existing labels. Let C be the complete
252-rotation collision set, whose sum graphs are four-chromatic by
[COLLISIONS.md](COLLISIONS.md). If distinct h_i,h_j have a common unit
neighbour in H, b is a unit difference of M, and

```
|r|=1,   |h_j-h_i+r*b|=1,
```

then r belongs to C. The complete H incidence check covers 105 of its
168 nonadjacent pairs; 63 nonadjacent pairs have no common unit neighbour.
Together with the [unit-H common-neighbour theorem](COMMON_NEIGHBOUR.md),
this bounds all possibly non-four-colourable rotations by **8484**, or
**1212 classes under sevenfold rotation**. These are upper bounds on an
explicit necessary-event set, not exact angle counts or evidence that
any non-four-colourable sum exists. The full H+rM family remains open.

## The factor-exchanged geometric argument

More generally, suppose h_i,h_j in a finite set A have a common unit
neighbour h_c in A. Put u=h_i-h_c, v=h_j-h_c and a=v-u. Let b=m_p-m_q
be a unit difference of a second finite set B. Both u and v are unit,
and u != v. The rotations satisfying |a+r*b|=1 are exactly

```
r_1=u/b,   r_2=-v/b.
```

Indeed a+r_1*b=v and a+r_2*b=-u. Expanding the squared norm gives a line
meeting the unit circle in at most two points, since a and b are
nonzero. The displayed roots differ unless v=-u. In that tangent case,
a=-2u and |r*b-2u|=1 with |r*b|=1 forces Re(r*b*conjugate(u))=1,
hence r*b=u; the single displayed root is complete. This is also the
previous common-neighbour lemma after exchanging the two factors.

Every root produces a collision of distinct labelled sums:

```
r*b=u   => h_i+r*m_q = h_c+r*m_p,
r*b=-v  => h_c+r*m_q = h_j+r*m_p.
```

The centre must belong to A. No colouring assumption or algebraic
coordinate hypothesis enters this geometric lemma. For our fixed
factors, the already proved all-collision theorem puts these roots in C.

## Complete incidence and root certificate

Every unordered H pair is included in
[dual_neighbour_certificate.json](dual_neighbour_certificate.json).
The rows are `[i,j,unit_edge,common_neighbours]`; the common-neighbour
list is complete, not a selected witness list.

| Pair type | Number of common unit neighbours | Number of pairs |
|---|---:|---:|
| Unit edge | 0 | 21 |
| Unit edge | 1 | 21 |
| Nonedge | 0 | 63 |
| Nonedge | 1 | 105 |

Thus 126 pairs are covered and each has a unique centre. There are 14
distinct directed unit differences of M. Checking both roots for every
covered pair gives 126*14*2=3528 records, including 2940 records for
nonadjacent H pairs. Each contact equation and labelled collision is
checked in a separate exact coordinate basis. The distinct root set
equals C; equality is additional validation, while inclusion suffices
for the theorem. None of these fixed-factor cases is tangent. The
general tangent case and the excluded zero and nonunit inputs are
checked separately.

Using unordered H pairs loses no contact: reversing a can be absorbed
by simultaneously reversing b, and both signs occur among the directed
unit M differences. The 21 uncovered unit H pairs are already handled
by the previous unit-H theorem. The current result does not close all
contacts with a unit M difference: the 63 uncovered nonedges remain.

## Remaining necessary-event set

Let D consist of h_j-h_i for all i<j whose H pair is nonadjacent, and
let U be the subset whose endpoints have no common unit neighbour in H.
All 420 nonzero directed H differences are distinct, so D and U are
sets of representatives of 168 and 63 difference sign classes. Let
B_1 and B_n be the distinct nonzero directed M differences of unit and
nonunit length, respectively. Their sizes are 14 and 20. Define

```
I = (D x B_n) union (U x B_1),
E = {r : |r|=1 and |a+r*b|=1 for some (a,b) in I}.
```

The two parts of I are disjoint and have sizes 3360 and 882. Each
equation has at most two roots, so

```
|I| = 168*20 + 63*14 = 4242,
|E| <= 2*4242 = 8484.
```

Every sum outside E is four-chromatic. For r in C this follows from
the inherited colouring theorem. For r outside C the sum map is
injective, with 147 points. Any mixed unit edge with a unit H
difference would force r into C by the previous theorem. Any mixed
edge with unit M difference and a covered H pair would do the same
by the new lemma. All other mixed unit edges are indexed by I, using
simultaneous sign reversal when necessary. Thus outside both C and E
there are no mixed unit edges: the induced unit graph is the Cartesian
product of the factor graphs and has the inherited proper XOR
four-colouring. Every sum also contains a translated rotated Moser
spindle, giving chromatic number at least four.

Some members of E can already belong to C; others can be four-colourable
for unrelated reasons. We have not solved the equations defining E,
removed duplicates, or tested their sum graphs.

## Sevenfold symmetry and a finite next cohort

Write zeta=exp(2*pi*i/7). The exact coordinates satisfy zeta*H=H, with
label permutation `7*(i//7)+(i%7+1)%7`. The 168 nonadjacent H pairs
form 24 orbits of size seven; the 63 uncovered ones form nine such
orbits. The full orbits, and indices selecting the uncovered ones,
are included in the compact certificate.

Choose the lexicographically least unordered pair in each orbit and
orient it by increasing label. The reduced event list consists of
these 24 differences paired with B_n and the nine uncovered differences
paired with B_1. It has

```
24*20 + 9*14 = 606 equations,
```

and hence at most 1212 root representatives. Rotating a representative
equation by zeta^k multiplies its root by zeta^k. If the resulting H
endpoint labels reverse order, replace both a and b by their negatives;
the norm equation is unchanged. The separate checker expands all 606
indices and compares the resulting set entrywise with all 4242 elements
of I. It handles 324 label-order reversals explicitly. No invariance
of H under negation or reflection is assumed.

Consequently E is a union of C7 orbits, with at most 1212 orbits. The
graphs at r and zeta^k*r are isometric, since multiplying the entire
sum by zeta^k takes H+rM to H+zeta^k*r*M. Further graph isomorphisms
could reduce this count, but are not used.

The next proposed actual-placement cohort is the unit-M part: nine H
pair representatives

```
(0,3), (0,10), (0,11), (0,16), (0,19),
(7,8), (7,15), (7,20), (14,16)
```

paired with the 14 directed unit M differences, whose labels are also
in the certificate. This gives 126 equations and at most 252 root
representatives before feasibility, collisions and duplicate removal.
The number 252 here is an upper bound for an unenumerated cohort; it
is not an identification with the already closed set C, also of size
252. A later pass may construct and certify this cohort with exact
algebraic root handling and actual induced unit graphs. The present
incidence and symmetry mechanism is complete; no such root enumeration,
new sum graph, colouring query, or enlarged factor was started.

## Reproduction, dependencies, and scope

Use a full checkout, Python 3.11.2 (tested), the standard library and
assertions enabled. From this directory choose a fresh external output:

```bash
python3 -B dual_neighbour.py --out /scratch/fresh-heptagon-dual-neighbour
python3 -B dual_neighbour_audit.py --work /scratch/fresh-heptagon-dual-neighbour
sha256sum -c SHA256SUMS
```

The audit status is
`DUAL COMMON-NEIGHBOUR EXCLUSION AND RESIDUAL INDEX SET VERIFIED`.
[dual_neighbour_expected.json](dual_neighbour_expected.json) records
counts and hashes; [dual_neighbour_validation.json](dual_neighbour_validation.json)
records the measured run and pinned inputs. The 5033-byte certificate
is public. The complete 3528-root transcript is generated locally and
identified by SHA256 in the expected results, not committed as bulk data.

The producer uses the inherited cyclotomic-plus-s basis. The checker
imports neither dual_neighbour.py nor field.py. It reconstructs the
factors in the separate zeta7/omega6/w basis, computes the common
neighbours by testing distances to every third H point, and determines
pair orbits by acting on coordinates instead of the producer's label
formula. Every root and labelled collision is checked and compared
with the inherited 36-orbit colouring certificate. All residual event
indices, including sign handling, are compared entrywise. Seven invalid
inputs or corrupted incidence/orbit certificates are rejected. Generation
took 1.73 seconds and the complete audit 5.56 seconds, one thread; peak
memory was not measured.

The trust boundary is exact Python arithmetic and finite-loop
correctness, the earlier coordinate-field justification, the stated
geometric proof, and the inherited colouring theorems. The checks are
author-run; no external-author review is claimed. The old sum graphs
and their colourings were not regenerated. The mathematical dependencies
are the common-neighbour source `6882c980c31f08481228629aa5ea193c04e32ca2`,
all-collision source `4ec850c8ba08f8beea0a811c49e3b526aa123e38`, and the
unit-contact colouring source `73513299bf4d669ce305a9e4c061fee5f0f7eb93`.

The target remains a five-chromatic Euclidean unit-distance graph with
at most 508 vertices. Record calibration was checked live on 2026-09-06
against [Parts' source](https://arxiv.org/abs/2010.12665) and
[Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4).
Only H's coordinates are imported from the latter; its larger
construction and numerical assertions are not premises of this result.
No record improvement or priority claim for this elementary geometric
lemma is made. The full rotation family remains open.

The relevant prepublication graph refresh reached indexed height 3099
with no new overlapping contribution. The accompanying repository
refresh found HN-2's [small-block family closure](../hadwiger_nelson_heule517_small_pilot/README.md),
source `6c88f992e5effaf0cea806f8066c80986edef08a`. It proves every H517
subgraph with at most 133 small-block vertices four-colourable, while
the unrestricted at-most-508 family remains open. This is a separate
family and supplies no mathematical premise here. Its new graph
contribution and final report were not yet visible in that refresh.

Stopping decision: preserve this complete dual incidence and event-index
checkpoint, and yield before the proposed unit-M placement cohort. No
background computation or incomplete certificate remains.
