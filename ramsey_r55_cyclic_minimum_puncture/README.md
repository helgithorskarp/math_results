# Minimum puncturing of Cyclic(43) cannot regrow to 41 vertices

**Exact result.** The largest induced (5,5)-Ramsey subgraphs of Exoo's
Cyclic(43) have 34 vertices. There are 215 labeled such cores, in five
dihedral classes. Their maximum possible orders after adding arbitrary
vertices and arbitrary incident edges are respectively

    39, 40, 39, 40, 38.

Each upper bound is attained by an explicit graph in `certificate.json`.
In particular **none of the 34-vertex cores extends even to 41 vertices**.
The construction attempt of minimally puncturing Cyclic(43) and freely
regrowing nine vertices is completely excluded. No automorphism is imposed
on the final graph. This is not a Ramsey-number improvement or a 43-vertex
construction. The displayed graphs are smaller than the known 42-vertex
examples and are not claimed to be historically new.

The result also gives a global constraint on repairs: a (5,5)-good graph
on at least 41 vertices has no common induced subgraph of order 34 with
Cyclic(43). Consequently, for **every labeling** of a hypothetical
Ramsey(5,5;43) graph, the graph of its edge disagreements with Cyclic(43)
has vertex-cover number at least 10. The same holds after color reversal.
This is a necessary separation condition, not a forcing of one of these
cores into a target or a claim that the value 10 is sharp.

## Complete minimum-puncture classification

Label Cyclic(43) by Z/43Z and color a pair red when its undirected cyclic
distance is in

    D = {1,2,7,10,12,13,14,16,18,20,21}.

Its 43 monochromatic five-sets are all red. Under the coordinate change
y=2x modulo 43 they are exactly the 43 consecutive five-windows. The
independent checker verifies this against all 962,598 physical five-sets;
it does not assume the earlier circulant classification or import a graph
catalog. Each vertex lies in five windows, so eight deletions can hit at
most 40 of them. Nine deletions suffice, as certified by the sets below.
Thus 34 is the exact maximum order of a good induced core.

In doubled coordinates a nine-set hits all five-windows precisely when
its nine positive cyclic gaps are at most five. The gap sum is 43; starting
from nine gaps of five leaves total deficit two. Thus either one gap is
three or two gaps are four. There are 9+choose(9,2)=45 rooted gap words,
giving 43*45/9=215 distinct nine-sets. Translation and reflection leave five
classes: one short gap, or two gaps of four at one of four cyclic separations.
Every orbit has size 43. Translation/reflection are checked physical
automorphisms of the seed; no other symmetry reduction is assumed.

The representative deletion sets use the original x labels:

| class | deleted vertices | blue/red core K4s | admissible stars | pair cap | exact maximum order |
|---:|---|---|---:|---:|---:|
| 0 | 0,2,4,9,14,19,28,33,38 | 409 / 519 | 16 | 5 | 39 |
| 1 | 0,2,7,9,14,19,26,33,38 | 370 / 575 | 13 | 7 | 40 |
| 2 | 0,2,7,12,14,19,26,31,38 | 356 / 589 | 13 | 5 | 39 |
| 3 | 0,2,7,12,17,19,26,31,36 | 396 / 547 | 17 | 6 | 40 |
| 4 | 0,4,9,14,19,23,28,33,38 | 435 / 477 | 36 | 4 | 38 |

Their unordered pairs of red/blue K4 counts are distinct, so these are also
five different core isomorphism types, even allowing color reversal. This
does not classify the extension graphs up to isomorphism.

## Every attachment and every pair of attachments

For one core C, list its 34 retained original vertices in increasing order
and relabel them 0..33. An attachment star is a 34-bit integer S whose bit i
indicates a red edge to core vertex i. A new vertex causes no monochromatic
K5 precisely when:

* every red core K4 has at least one blue contact;
* every blue core K4 has at least one red contact.

These are negative and positive four-literal clauses. The certificate
contains every satisfying star, with the counts shown in the table.
`build.py` enumerates them using CaDiCaL via python-sat. `check.py` rebuilds
the physical clauses and exhausts both branches of a separate standard-library
DPLL recursion with unit propagation. Its node counts are 59,75,65,69,97.
The **entire sorted model sets** agree, not just their cardinalities.
The resulting upper-bound proof does not trust the producer's solver.

For two stars S,T, their mutual edge may be red precisely when S intersect T
contains no red core triangle. It may be blue precisely when the common
blue contacts contain no blue core triangle. These conditions are necessary
and sufficient for avoiding a monochromatic five-set using both new vertices
and three core vertices. They are only necessary for a larger assembly.

Every star paired with itself forbids both edge colors. Thus no extension
can repeat an attachment type, at any total order. Define the compatibility
graph on the star types by joining two distinct types when at least one
mutual color is allowed. Any extension's stars form a clique in that graph.
The numbers of compatible pairs are 74,62,59,97,120.

The producer finds pair-clique caps 5,7,5,6,4 by recursive enumeration.
The independent checker uses a different coverage method: it inspects every
subset of size cap+1 and finds an incompatible pair. The five counts are
8,008; 1,287; 1,716; 19,448; and 376,992, totaling 407,451. The checker derives
the pair relation from literal physical core triangles; no supplied
compatibility table or producer recursion is trusted.

## The last seven-vertex assembly and sharp lower witnesses

For classes 0,2,3,4, the pair cap is attained by a fully checked extension.
For class 1, there is exactly one compatible seven-set of attachment types:

    (0,1,3,6,9,10,12),

where type indices refer to the sorted star list in `certificate.json`.
Six of its 21 mutual edges allow both colors; the other 15 are forced.
All 64 assignments to those six edges have a monochromatic K5. The compact
certificate supplies one **literal five-set and color for each assignment**.
The independent checker enumerates all compatible seven-sets and all allowed
edge assignments afresh, checks exact case coverage, and checks all ten
physical pairs of every supplied witness. This lowers class 1's maximum
number of added vertices from seven to six. It is not inferred from a solver
status or pair consistency alone.

The same certificate contains explicit red edge lists of good extensions on
39,40,39,40,38 vertices. Every core and attachment is checked, and all physical
five-subsets are tested. These witnesses prove the lower halves of the exact
maximum-order claims. No classification of all maximum witnesses or all
intermediate extensions is claimed. Each displayed graph cannot itself be
extended by even one new vertex, since its fixed core already reaches its
proved maximum extension order. Consequently none can be an induced subgraph
of a good graph on 41 or more vertices.

## Construction scope and global repair consequence

For any one of the five fixed 34-vertex cores, all

    9*34 + choose(9,2) = 342

remaining physical edges of a 43-vertex graph are independent choices. The
family has 2^342 labeled graphs for that fixed embedding, all excluded.
All 215 literal minimum-puncture choices, all relabelings and color reversals
are covered. No cardinality is claimed for their overlapping union.
No small Ramsey bound, module theorem, Hill-Love classification, degree
profile, known 42-vertex catalog, or fixed star assignment is a premise.

For the global consequence, suppose a good graph H of order at least 41
shared an induced 34-vertex graph with Cyclic(43). That shared graph is good,
so it is one of the maximum cores completely classified above. Its occurrence
in H is an extension to at least 41, contradicting every row's maximum at
most 40. A larger common induced graph would contain a common 34-set, so the
common induced order is at most 33.

Now compare any labeled hypothetical Ramsey43 graph G with Cyclic(43), and
let Delta contain exactly their differing pairs. If nine or fewer vertices
covered all edges of Delta, at least 34 remaining vertices would have exactly
the same induced coloring in both graphs. This is impossible. Thus
tau(Delta)>=10 under every labeling, and also against the complementary seed.
This bound excludes any repair whose changed edges can all be covered by
nine vertices, irrespective of the number of changed edges. It does not
force a core into G or decide repairs beyond that bound.

## Stand-alone verification and optional production

Requirements for all certificate checking: Python 3.11+, standard library
only. Tested with CPython 3.11.2. From this directory run:

```sh
python3 -B reproduce.py
python3 -B check.py certificate.json
python3 -B verify_graph.py maximum40.edges
```

Expected full status: `REPRODUCED_CYCLIC_MINIMUM_PUNCTURE_SPECTRUM`.
The last command verifies 40 vertices, 397 red edges, and zero forbidden
five-sets in both colors. It is a valid smaller graph, not the target.

The edge-list format has first line `n m`, followed by m sorted distinct
red pairs `u v` with 0<=u<v<n; all omitted pairs are blue. To export any of
the five maximum witnesses:

```sh
python3 -B export.py 0 > /tmp/maximum39.edges
python3 -B verify_graph.py /tmp/maximum39.edges
```

`verify_graph.py` imports no construction code, certificate checker, solver,
or orbit model. It independently compares literal five-set enumeration with
bit-intersection clique counting. All five witnesses receive both checks.

To regenerate the certificate, optionally install `python-sat==1.9.dev15`
in a local environment and run:

```sh
python3 -B build.py > /tmp/puncture-certificate.json
cmp certificate.json /tmp/puncture-certificate.json
```

The producer uses the bundled CaDiCaL 1.9.5 backend (`cadical195`). Solver
model order is immaterial because all domains are sorted before assembly.
Checking and full reproduction need no solver, external data, network, private
files, or large generated artifact. The initial prototype's solver-found
nine-cover is not used in the proof of minimality or the complete cover census.

`reproduce.py` checks the source manifest and all expected output in normal
and assertion-disabled Python. Controls compare the DPLL routine against
literal truth tables on all 16,384 monotone-sign CNFs on three variables,
check the five sharp edge-list witnesses using both clique algorithms, and
reject six altered certificates and four malformed physical graphs. The
proof computation is exact integer arithmetic. Cryptographic hashes identify
files, not mathematical truth. The universal extension reduction, exhaustive
coverage arguments, source implementations, Python semantics and ordinary
hardware remain unformalized trust boundaries. No independent-author review
or proof-assistant formalization of this new result is claimed.

## Prior work and campaign context

Cyclic(43) and its defects are classical construction context. See Ge,
Jayasooriya, Qiu, Sun and Yuan,
[*Study of Exoo's Lower Bound for Ramsey number R(5,5)*](https://arxiv.org/abs/2212.12630),
and [Exoo's construction page](https://cs.indstate.edu/ge/RAMSEY/).
The seed's complete circulant classification is separately available in
`../ramsey_r55_circulant43_classification`. This package reconstructs the
specific seed and all its defects independently; it does not import that
classification as a proof premise. No novelty is claimed for graph growth,
puncturing, compatibility graphs, DPLL, or the 43 seed defects.

Limited live and graph searches found no matching minimum-puncture extension
spectrum; that does not establish historical priority. The construction
attempt ended because its entire regrowth family was decided, before any
heuristic restarts or timeout ladder. It produces five smaller maximal
Ramsey graphs and a repair obstruction, not a new graph below seven defects
on 43 vertices. The theorem separates these cores and their extensions from
every good graph of order at least 41; it makes no isomorphism-separation claim
against saved defective 43-vertex search states.

The separate [module-resilience theorem](../ramsey_r55_module_resilience) and
team-r55-3's [induced-pentagon forcing theorem](../ramsey_r55_induced_pentagon_forcing)
are not proof inputs here. The latter, published during this computation,
closes the induced-C5-free branch at orders at least 42. The present result
changes neither the inherited 17-class/9,153-label symmetry frontier nor
any global degree-profile count. It supplies no forcing of a prescribed
34-vertex core, and does not settle construction methods beyond the exact
minimum-puncture family.
