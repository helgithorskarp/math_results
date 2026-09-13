# Complete coexistence of the specified path and module conditions

This is an exact countermodel to the inconsistency of a **specified necessary
system**, not to Ramsey(5,5) and not to any accepted theorem. No good43 or
whole-class exclusion is established. The first contracted gate is missed.

All graphs are finite, simple and labelled. Red means edge and blue means
nonedge. A good43 has order 43 and no monochromatic five-set. A proper module
M of an induced graph H has 2<=|M|<|H|, and each vertex of H-M has uniform
contacts to M. An induced blue P5 is an induced complement-P5 in the red graph.

## 1. The entire necessary system Q tested here

Q consists of the following conditions on a physical graph G of order 43:

1. Every colour degree is in 18..24. Every pair has at least eight outside
   distinguishers; every mixed triple has at least 17, and every monochromatic
   triple at least 18. A same-colour pair has at most 13 common neighbours of
   that colour.
2. Every induced subgraph on at least 36 vertices is prime.
3. Every induced subgraph on at least 28 vertices has no proper module of size
   at least three.
4. Every 26-set contains an induced P5 or complement-P5.
5. For every vertex v, every 18-subset of its red neighbourhood contains an
   induced red P5, and every 18-subset of its blue neighbourhood contains an
   induced blue P5.

The full deletion and subset quantifiers in items 2--5 are checked, not
replaced by aggregate distinguishing or path counts. These are necessary
conditions for good43 relative to the imported premises in DEPENDENCIES.md.

Q deliberately does not include the absence of monochromatic K5, the full
collection of its local consequences, or the hypothetical assertion that
different path components must be modules. In particular, Q does not include
the upper bound four on same-colour common neighbours of a monochromatic
triangle. The control violates that omitted bound. It must not be described
as satisfying every inherited Ramsey restriction.

**Exact outcome.** The unchanged graph in `control43.edges` satisfies Q and
has exactly seven monochromatic five-sets. Hence Q is consistent. No valid
contradiction can follow from Q alone. This does not decide whether the
conjunction of Q and full Ramsey avoidance has a model.

The graph was already source-published and is not a new construction. Its
input provenance and hash are in CONTROL_ORIGIN.json. No edge is modified.

## 2. An exact all-deletion module test

For any nonempty M subset V(G), let U_R(M) and U_B(M) be the vertices complete
and anticomplete to M, respectively, always outside M. Put U(M)=U_R(M) union
U_B(M). For k>=2 define

    L_k(G) = max { |M|+|U(M)| : |M|>=k, U(M) nonempty },

with maximum zero if the indexing set is empty.

**Lemma.** L_k(G) is exactly the largest order of an induced subgraph of G
having a proper module of size at least k.

**Proof.** If M is a proper module in G[W], then W-M is a nonempty subset of
U(M), so |W|<=|M|+|U(M)|. Conversely M is a proper module in the induced graph
on M union U(M) whenever U(M) is nonempty. Both inequalities follow. No
clique, degree, Ramsey, or catalogue assumption is used.

For the supplied graph the two algorithms below give

    L_2(G)=29,    L_3(G)=23.                     (1)

These values verify the requested 36- and 28-vertex conclusions directly.
They are values for this single defective control, not new module thresholds
for good43. Explicit attaining modules and their whole uniform outside sets
are recorded in EXPECTED.json.

### Direct enumeration with a witness of properness

If U(M) is nonempty, choose u in U(M) and its contact colour c. Then M is a
subset of N_c(u). Conversely each nonempty subset of N_c(u) has u as a uniform
outside vertex. Therefore enumerating all subsets of all 86 colour
neighbourhoods covers every relevant M. Duplication is harmless for a maximum.

`audit.cpp` uses this enumeration. While extending M it intersects the actual
red and blue neighbourhood bitsets, so its score is the literal |M|+|U(M)|.
It visits 196,081,820 occurrences of subsets of size at least two, exactly

    sum_(u,c) [ 2^|N_c(u)| - 1 - |N_c(u)| ].

This number counts rooted subset occurrences, not distinct modules, deletion
sets, graphs, or research tasks. There is no search budget or partial outcome
accepted as a proof.

### A separate complete intersection argument

Regard the 86 sets N_c(u) as attribute extents. For a relevant M intersect
all attribute extents that contain M, obtaining C(M). Then M subset C(M)
and U_R(C(M))=U_R(M), U_B(C(M))=U_B(M). One inclusion follows because C(M)
contains M; the other follows because all original uniform contacts were
among the intersected attributes. Thus C(M) has at least as large a score
and meets the same minimum-size requirement.

It is consequently enough to inspect all intersections of subfamilies of
these 86 sets, including the full vertex set for the empty subfamily.
Intersections of size less than two and their descendants can be discarded.
The full set has empty U and cannot certify a proper module.

`check.py` generates this closure under intersection and checks every remaining
extent's actual uniform sets. It obtains 135,790 extents of size at least two,
and the same maxima (1). This algorithm does not enumerate the producer's
rooted subsets or import its source. Its completeness follows from the
intersection argument, not from agreement of aggregate counts alone.

## 3. All 26-subsets: an exact global coverage join

Partition the fixed control's labels into X={0,...,20} and Y={21,...,42}.
The binary certificate supplies:

- An induced P5 or complement-P5 in every 13-subset of X: 203,490 records.
- Such a pattern in every 14-subset of Y: 319,770 records.

Every 26-set meets X in at least 13 vertices or Y in at least 14 vertices:
otherwise its size is at most 12+13=25. Each larger intersection contains
one of the checked subsets. This proves item 4 of Q for every 26-set of the
control. The fixed partition is a certificate for this supplied graph,
not a restriction on a good43 candidate or a claim about graph symmetry.

## 4. All neighbourhood 18-subsets, in both colours

For each labelled vertex, the certificate next gives an induced path of the
required colour in every 18-subset of each colour neighbourhood. The number
of records is 187,055 over all 86 neighbourhoods. The checker reconstructs
the actual neighbourhoods from the edge list and visits every subset; it
does not infer coverage from a lower bound on the total number of paths.

The complete certificate has 710,315 records. Each record is an unsigned
43-bit vertex mask stored in eight little-endian bytes, and names exactly
five vertices. Record order is:

1. Lexicographic 13-subsets of X, then lexicographic 14-subsets of Y.
2. Vertices 0 through 42, red then blue at each vertex, and lexicographic
   18-subsets of the corresponding sorted neighbourhood.

The producer recognizes P5 by its degrees and connectedness and the
complement pattern in the opposite colour. The checker constructs all 60
path edge words from vertex permutations and their 60 complements. For
every record it verifies containment in the represented subset, cardinality
five, and the ten literal pair colours. It rejects missing, invalid, wrong
colour and trailing records. The subset coverage and join above are part of
the proof; the producer's choice of witness has no authority by itself.

The full certificate is 5,682,520 bytes. Its SHA-256 is

    cbbc3cb64905648f5ec05960b08ac1b1f67c3d1af0a509d9ae7531306a971801.

It is regenerated outside Git. No omitted external data is required.

## 5. Complete physical audit and the omitted condition

Both implementations scan all 962,598 five-sets. The graph has 53,993 red
P5 sets and 69,855 blue P5 sets. Its joint path hypergraph is connected and
spanning. These counts describe the control and are not new necessary bounds.

The seven defects, with vertices in increasing order, are:

    red:  (0,1,21,22,42)
    blue: (2,3,6,40,41), (2,3,37,40,41), (14,17,18,22,23),
          (17,18,22,23,26), (17,20,21,25,26), (20,21,25,26,29).

The checker also obtains minimum pair distinguishing count 14, minimum
triple distinguishing count 21, and maximum same-colour pair common count
13. These verify item 1 of Q. They do not certify a Ramsey graph.

There are 16 monochromatic triangles with more than four same-colour common
neighbours; the maximum is five in each colour. For example the red triangle
(0,1,21) has the five red-common neighbours {14,22,23,31,42}. The accepted
Ramsey argument forbids this configuration in a good43, but Q contains only
its displayed distinguishing consequences, not that actual condition. All
16 violations are explicit in EXPECTED.json. No repair of this graph or
search around it is attempted.

## 6. First-gate assessment and the remaining trial

The pass predeclared the exhaustive partition D/C: the hypergraph of all
induced P5 or complement-P5 five-sets is disconnected (including isolated
vertices), or it is connected and spanning. The intended milestone was to
exclude the entire D class using module resilience. That theorem was not
obtained. A disconnected path component need not automatically be a module;
the necessary nonlocal bridge is still missing. The control is in C and
does not refute a possible future D-class exclusion.

The new certificate instead settles the narrower methodological question:
all the specified path-cover and full module-resilience conclusions coexist
physically on order 43 with Ramsey defects. It supplies no finishable
all-good43 decomposition and does not meet the first contracted gate.

One final mathematical pass remains under the human contract. It requires
one high-level correction: stop attempting an inconsistency of Q and use
actual monochromatic-K5 avoidance in a global structural argument. No short
complete route is established here. More path coverage, module thresholds,
local attachment tables or countermodel checks are not proposed as another
milestone. Failure of the final gate requires reassignment within R(5,5).
