# Every Ramsey(5,5;43) coloring is 18-connected in both colors

**Deleting any set of at most 17 vertices leaves both color graphs
connected.** Equivalently, a hypothetical Ramsey(5,5;43) coloring has no
monochromatic complete bipartite graph whose two nonempty parts contain
at least 26 vertices in total. The parts need not be cliques or independent
sets in their own right.

This excludes an entire global separator branch, with no degree-profile,
automorphism, catalog, switched-core or fixed-neighborhood assumption.
The target graph remains unknown; no Ramsey-number bound changes. This
is a short proved structural lemma with exact internal arithmetic checks,
not an externally reviewed result or a proof-assistant formalization.
No claim of historical priority or optimality of 18 is made.

## 1. Inputs and small Ramsey facts

All graphs are simple. Red edges form G and blue edges its complement;
neither graph has a five-clique. Write delta(G) for minimum degree and
kappa(G) for vertex connectivity.

The only non-elementary input is the established bound R(4,5)<=25.
The blue neighbors of any vertex induce a graph without a red five-clique
or a blue four-clique, hence number at most 24. Thus every red degree
is at least 42-24=18. Exchanging colors gives the same minimum in blue.
This is the classical degree-window deduction; it is not new here.

Primary source: B. D. McKay and S. P. Radziszowski,
[R(4,5)=25, Journal of Graph Theory 19 (1995), 309–322](https://onlinelibrary.wiley.com/doi/10.1002/jgt.3190190304).
A later [HOL4 formal proof by Gauthier and Brown](https://arxiv.org/abs/2404.01761)
provides further provenance for this input; that formal development was
not rerun here. No extremal-graph catalog is imported by our proof or code.

The smaller bounds used below have elementary proofs:

- R(3,3)<=6: among five edges at a vertex, three share a color. Either
  two endpoints have that color between them, or all three opposite
  edges have the other color.
- R(3,4)<=9: in a triangle-free graph with independence number at most
  three, every degree is at most three. At order nine, every nonneighbor
  set has independence number at most two, hence size at most five by
  R(3,3)<=6. Every degree would therefore be exactly three, contradicting
  the handshaking lemma on nine vertices.
- R(3,5)<=14: at order fourteen, a triangle-free graph with independence
  number at most four has maximum degree four. Every nonneighbor set is
  triangle-free with independence number at most three, hence has at
  most eight vertices by the previous bound. Minimum degree would be
  at least five, a contradiction.

We also use their color reversals, R(2,5)=5, and R(1,5)=1.

## 2. Localized theorem and the complete separator dichotomy

**Localized theorem.** If a graph G has 43 vertices, clique number at
most four, independence number at most four, and minimum degree at least
18, then kappa(G)>=18. The proof of this localized statement uses only
the elementary smaller Ramsey bounds above. Applying Section 1 proves
the announced result in both colors.

Suppose S is a vertex separator, k=|S|<=17, and let A_1,...,A_r be
the components of G-S. There are at least two components. No red edge
joins different components, so their independence numbers add and sum
to at most four. We treat every possibility, including a disconnected
original graph (S empty).

### Case I: some component is a clique

Let A be such a component, of order a<=4. Each of its vertices has
at least 18-(a-1) red neighbors in S, as it has no neighbors in any
other component. If a=1 this requires 18 neighbors in a set of at most
17 vertices, impossible.

For a=2,3,4, the common red neighborhood of A in S therefore has size
at least

    L(a,k) = k - a[k-(18-a+1)]
           = a(18-a+1) - (a-1)k.

This is the union bound on the separator vertices missed by each member
of A. The common neighborhood contains no red (5-a)-clique and no
independent five-set. Its order is consequently at most 13, 4, or 0
for a=2,3,4 respectively. But at the largest allowed k=17 the lower
bounds are 17,14,9, already strictly greater than those upper bounds.
Smaller k only increases L. Hence no clique component is possible.

### Case II: no component is a clique

Each component has an independent pair. There cannot be three components,
since their independent pairs would give an independent six-set. There
are exactly two, A and B, and each has independence number exactly two.
As neither contains a five-clique, R(5,3)<=14 gives |A|,|B|<=13.

At least 43-17=26 vertices remain. Thus necessarily k=17 and
|A|=|B|=13. In particular S is nonempty. Choose any z in S.

Inside A, the red neighbors of z have no four-clique (one would extend
through z) and independence number at most two (inherited from A).
R(4,3)<=9 therefore bounds their number by eight. At least five vertices
of A are blue to z. Among them there is a blue pair, because five red
mutually adjacent vertices are forbidden. The identical argument in B
supplies another blue pair. The two pairs, together with z, form a blue
five-clique: all A--B pairs are blue since A and B are different red
components. Contradiction.

Both cases are impossible. This proves the localized theorem and its
unconditional Ramsey(5,5;43) corollary.

## 3. A usable global constraint

For every pair of disjoint nonempty vertex sets A,B with |A|+|B|>=26,
write e_R(A,B) for the number of red pairs between them. The result gives

    1 <= e_R(A,B) <= |A||B|-1.                         (1)

Indeed, with S the complement of A union B, a monochromatic A--B cut
disconnects the opposite color after deleting at most 17 vertices.
Conversely, a separator gives such a monochromatic cut by grouping
components. It is enough to impose (1) for |A|+|B|=26: a larger cut
contains one of total size 26 with both parts nonempty.

For Boolean red-edge variables x_uv, the two cut clauses are

    OR_{u in A,v in B} x_uv,
    OR_{u in A,v in B} NOT x_uv.

These are necessary global constraints, not a full characterization or
a claim that their explicit exponentially large conjunction was emitted.
They apply in both the low-deficiency and hard branches. No cumulative
degree profile or anchored split is claimed removed merely from this
connectivity result. Separators of order 18 or larger are not classified.

## 4. Exact finite coverage audit

The written proof does not depend on computation. The small
[certificate.json](certificate.json) audits its component-size coverage.
If a component has independence number 1,2,3, its order is at most
4,13,24 respectively. There are at least two components, their
independence numbers sum to at most four, their orders sum to 43-k,
and each order a satisfies a-1+k>=18.

Only the following seven arithmetic profiles remain. These are necessary
profiles, not asserted graph realizations:

| k | component orders | independence numbers | contradiction |
|---:|---|---|---|
| 15 | 4,24 | 1,3 | common neighbors >=15, <=0 |
| 16 | 3,24 | 1,3 | common neighbors >=16, <=4 |
| 16 | 4,23 | 1,3 | common neighbors >=12, <=0 |
| 17 | 2,24 | 1,3 | common neighbors >=17, <=13 |
| 17 | 3,23 | 1,3 | common neighbors >=14, <=4 |
| 17 | 4,22 | 1,3 | common neighbors >=9, <=0 |
| 17 | 13,13 | 2,2 | outside vertex forces a blue five-clique |

[derive.py](derive.py) enumerates independence-budget partitions followed
by products of component orders. [check.py](check.py) imports no producer:
it recursively builds ordered multisets of component types and compares
the complete entry sets. It checks each contradiction using the
complementary missing-neighbor formula, and rejects four mutations
(missing case, false bound, false boundary step, and enlarged scope).
The order-24 capacity in this optional audit uses R(5,4)<=25; the
localized proof in Section 2 does not need that capacity.

Definition-level controls check all 1,097 labeled Ramsey(5,5) graphs of
orders one through five and all their vertex deletions. They examine
12,953 separator instances, 26,705 clique common-neighborhood inequalities
and 34,628 outside-vertex tests. K19 disjoint union K24 is an explicit
negative fixture: order43 and minimum degree18 alone do not imply the
conclusion; this graph contains five-cliques and is correctly rejected.
These small controls validate translations, not an exhaustive order43
graph enumeration or a replacement for the universal proof.

With CPython3.11.2, standard library only, run from this directory:

```sh
set -o pipefail
python3 -B derive.py | cmp - certificate.json
python3 -B check.py | cmp - validation.json
python3 -O -B derive.py | cmp - certificate.json
python3 -O -B check.py | cmp - validation.json
sha256sum -c SHA256SUMS
```

Expected check status: `VERIFIED_SEPARATOR18_ARITHMETIC`, seven rows,
four rejected mutations. Normal and assertion-disabled runs agree
byte-for-byte and finish in under a second on the production host.
The programs use exact integers and explicit exceptions, not solver
statuses, floating point, imported graph data or Python assertions.

## 5. Prior work, scope and handoff

The separator/independence-budget method is classical; compare
A. Beveridge and O. Pikhurko,
[On the connectivity of extremal Ramsey graphs, AJC41 (2008), 57–61](https://ajc.maths.uq.edu.au/pdf/41/ajc_v41_p057.pdf).
Their general theorem concerns graphs of order R(r,b)-1. We do not
assume a hypothetical order43 graph is extremal; R(5,5) is unknown.
No priority claim is made for separator counting or this numerical
corollary. The value to this campaign is an explicit short global proof
and reusable complete-cut restriction.

Discovery Net's new height3375 dense five-separator classification,
source `e5eff475fe1d86f9bca55649e183637611423e01`, concerns order22
Ramsey(4,5) neighborhoods and density thresholds. Its thirteen local
completion families remain open. It was read and is related context,
not a proof premise here. Our separator is in the entire43-vertex color
graph, not a selected neighborhood. No H92/H93, 104-edge lift, six-neighborhood
or related parked gluing computation was reopened.

The earlier 328-parent catalog-switch exclusion remains unchanged;
no larger catalog or new switching family was considered. Teammate
Core186's moving33 result is a different complete family. The external
M214 moment repair at3367 remains a fractional pseudomodel, not a graph,
and was not imported. No symmetry lane or catalog-neighborhood sweep
was duplicated.

Trust: Section1 imports the established R(4,5) bound. The new proof is
unformalized; the exact finite checks additionally trust their Python
source and runtime. Neither internal checking nor the external formal
proof of the classical input constitutes independent review of this
new artifact. No target graph, sharpness example for18, or new Ramsey
bound is produced. The declared global branch is closed, so this pass
ends here before any stronger connectivity threshold or other phase.
