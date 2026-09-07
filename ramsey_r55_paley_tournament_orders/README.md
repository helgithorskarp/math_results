# Every ordering of the Paley tournament on 43 vertices has two Ramsey defects

Let T be the tournament on F43 with an arrow x to y when y-x is a nonzero
square. Choose **any linear order** of its vertices. Color a pair red when
its arrow points forward in that order, and blue when it points backward.

**Every such coloring has at least two distinct monochromatic K5s. They can
be chosen to intersect only, if at all, at the first ordered vertex.**
This completely excludes all 43! labeled orderings as a construction of a
Ramsey(5,5;43) graph. No automorphism, degree profile, fixed graph core or
small edit radius is imposed on the resulting coloring. With the tournament
labels fixed, the color of each pair determines its relative order, so these
43! orderings give distinct labeled colorings. No cardinality is claimed for
their union under additional graph relabelings.

This is an exact finite obstruction, not a Ramsey-number improvement or a
target graph. The value two is a proved lower bound, **not a proved minimum**;
no order attaining two is supplied. Arbitrary Ramsey graphs are not known or
claimed to have a Paley tournament representation. No other tournament family,
global degree profile or residual automorphism class is excluded here.

## The local theorem and its forced occurrence

Write

    Q = {1,4,6,9,10,11,13,14,15,16,17,21,23,24,25,31,35,36,38,40,41}.

The central checked lemma is:

> Every linear order of T[Q] has a red K4 or a blue K5 in its forward/backward
> coloring.

Multiplication by any element of Q preserves Q and all tournament arrows,
and acts transitively on Q. We may therefore normalize the first ordered
vertex of Q to 1. Its ten outneighbors in Q are

    A = Q intersect (1+Q) = {10,11,14,15,16,17,24,25,36,41}.

If the local lemma failed, the induced coloring on A would have no red
triangle (which would join 1 to a red K4) and no blue K5. The complete
enumeration below finds exactly **51 possible orders** of A. Every one fails
to extend to an order of Q with the required properties.

Now let r be the first vertex of any order of T. Its red neighbors are r+Q,
and its blue neighbors are r-Q. Translation preserves arrows. Applying the
local theorem to r+Q gives either a red K4, which joins r to a red K5, or a
blue K5 lying entirely in that side.

Reversing a linear order complements its forward graph. Thus the local
theorem also excludes a red-K5-free, blue-K4-free coloring of T[Q]. Negation
reverses all tournament arrows and maps Q to -Q; combined with order reversal,
it preserves the family of forward graphs. Apply the color-reversed local
theorem to r-Q: there is either a blue K4, which joins r to a blue K5, or a
red K5 lying in that side.

The two sides are disjoint. The resulting two monochromatic five-sets
therefore meet at most at r, and are distinct. This supplies the bridge from
the small computation to **every full ordering on 43 vertices**. The colors
of the two witnesses need not be different.

## Complete census and compact refutations

The producer builds admissible orders of A by extending prefixes and rejects
a prefix as soon as it has a red triangle or blue K5. The independent checker
uses a different coverage algorithm: it visits **all 10! = 3,628,800 complete
permutations**, with no prefix pruning. Tournament arrows are independently
reconstructed using the exact test (y-x)^21 = 1 modulo 43, whereas the producer
enumerates squares. The ten-vertex tournament has 82 transitive triples and
eight transitive five-sets. Exactly 70 orders avoid red triangles, and exactly
51 of those also avoid blue K5s. The entire ordered list of 51 cases matches
the certificate, not just its cardinality.

For Q, let X_uv mean that u precedes v, with variables numbered by increasing
unordered pairs of Q. If u>v, X_uv denotes the negation of X_vu. There are
210 variables. For each u<v<w, include

    not X_uv or not X_vw or X_uw,
    X_uv or X_vw or not X_uw.

These forbid the two directed comparison triangles. A complete comparison
tournament without a directed triangle is transitive: the first clause
expresses transitivity in one label orientation, and the second excludes
the other cyclic orientation. Equivalently a shortest directed cycle would
have a chord producing a shorter cycle. Therefore satisfying comparisons
encode exactly the linear orders.

A monochromatic forward clique must induce a transitive subtournament.
Such a subtournament has a unique arrow order w1,...,wk. For a red K4,
forbid all three consecutive comparisons from being forward; for a blue K5,
forbid all four from being backward. Under comparison transitivity, these
chain conditions are exactly the corresponding all-pair clique conditions.
A nontransitive subtournament cannot be monochromatic in any vertex order.

There are 1,722 transitive four-sets and 1,050 transitive five-sets in Q.
Together with 2,660 comparison clauses and 20 units putting 1 first, the
normalized formula has **5,452 clauses**. Each of the 51 cases adds nine
units fixing its A-order. No other comparison, degree or adjacency is pinned.

Each case has a complete binary refutation with unit propagation. Combined,
the certificate contains only **108 branch nodes and 159 contradictory
leaves**; no individual case needs more than six branch nodes. A leaf is -1;
each other node stores a comparison variable and its positive and negative
children. Children precede their parent in the record. The checker requires
all nodes to be reachable, both branches to be checked, and every leaf to
contradict an actual reconstructed clause after propagation.

The producer simplifies clause lists. The checker keeps the original clauses
and propagates a separate Boolean valuation. It imports no producer, prefix
enumerator, SAT solver or stored formula. It independently reconstructs the
physical tournament, symmetries and clauses, using source elimination instead
of the producer's score sorting to identify transitive subtournaments.
The 4,468-byte certificate contains all 51 orders and all refutation trees.

The 51 inner orders are valid local states, not counterexamples by themselves.
Their failure to extend through the remaining ten vertices of Q is essential.
The blue-K5 restriction is essential as well: `disjoint_fixture.json` includes
an explicit order of Q with **no red K4**, but with blue K5s. Thus this proof
must not be shortened to a claim that every Q-order has a red K4.

## Reproduction and physical obstruction extraction

Python 3.11+, standard library only; tested with CPython 3.11.2. From this
directory:

```sh
python3 -B reproduce.py
python3 -B check.py certificate.json
python3 -B build.py > /tmp/paley-order-certificate.json
cmp certificate.json /tmp/paley-order-certificate.json
```

Expected full status: `REPRODUCED_PALEY43_ORDERING_OBSTRUCTION`.
Both production and checking need no external solver, network, catalog,
private input, imported small Ramsey theorem or omitted large proof.
Full ordinary and optimized replays took 57.15 and 57.30 seconds on the
development host, with peak child RSS 19,420 KiB.

An input order is a JSON array containing each integer 0..42 once. The
included fixtures are explicitly **non-Ramsey graphs**, not low-defect search
results or target candidates. Export the physical coloring and its obstruction:

```sh
python3 -B export.py fixture.json > /tmp/paley-order.edges
python3 -B extract.py fixture.json > /tmp/paley-order-fives.json
python3 -B verify.py /tmp/paley-order.edges /tmp/paley-order-fives.json
```

`fixture.edges` is the compact saved edge list for `fixture.json`: header n m,
followed by m sorted red pairs u v; omitted pairs are blue. It has 43 vertices
and 473 red edges. The saved two five-sets intersect at the first vertex 0.
Using `disjoint_fixture.json` instead exercises the two opposite-color K5
outcomes entirely inside the two sides, giving disjoint witnesses.

The standalone `verify.py` checks the explicit graph, all ten pairs of each
claimed five-set, and the intersection condition. It imports no tournament,
order generator, extractor, proof checker or Ramsey theorem. The universal
guarantee that extraction succeeds relies on the proof; checking a particular
output relies only on its physical pairs.

## Validation and trust boundaries

The full replay checks the source manifest, regenerates the certificate,
compares every expected result in ordinary and assertion-disabled Python,
and verifies the exported physical fixture. Additional controls include:

* All 1,024 tournaments on five vertices and all 120 orders of each: 122,880
  comparisons of the logical encoding against literal clique tests.
* All 1,024 assignments to the ten comparison variables on five vertices:
  exactly the 120 total orders satisfy comparison transitivity.
* Every choice of at most three distinct nonempty, nontautological clauses
  on three variables, and all partial assignments: 79,704 unit-propagation
  checks against literal truth tables.
* Rejection of six damaged proof certificates, four malformed orders, and
  four invalid physical certificates or graphs.
* Natural, reversed, deterministic shuffled and boundary orders covering all
  four combinations of the extractor's two branches.
* All 903 affine maps x to ax+b with a square and b arbitrary, checking all
  815,409 transported physical pairs of an explicit order coloring.

The theorem is an unformalized exact finite proof. Remaining trust is the
mathematical encoding and normalization arguments, source implementations,
complete enumeration and proof-tree coverage, Python integer semantics and
ordinary hardware. Matching author implementations are not external peer
review or proof-assistant formalization. Hashes identify source bytes; they
are not a substitute for the certificate checks.

## Prior work and campaign scope

Forward/backward graphs of tournaments are standard. For the closely related
one-color clique parameter, see Aboulker, Aubian, Charbit and Lopes,
[*Clique number of tournaments*](https://arxiv.org/abs/2310.04265).
The present objective simultaneously excludes red and blue K5s in a specific
Paley tournament. No theorem or complexity result from that paper is used as
a proof premise. Limited targeted live and Discovery Net searches did not
identify the present finite statement; this does not establish priority.
No novelty is claimed for Paley tournaments, order graphs or DPLL.

The previous [Cyclic(43) minimum-puncture spectrum](../ramsey_r55_cyclic_minimum_puncture)
closed a different construction mechanism. The present family changes all
relative orders and does not fix any of those 34-vertex graph cores.
Team-r55-3's [induced-pentagon forcing theorem](../ramsey_r55_induced_pentagon_forcing)
and the separate dense-neighborhood and moment constraints are not proof
inputs. No previous symmetry class, switching family or core extension was
reopened; the 17-class/9,153-label inherited symmetry frontier is unchanged.
The final shared refresh found independent acceptance of the preceding
puncture spectrum (Discovery Net h3611) and team-r55-3's
[global pentagon-incidence bounds](../ramsey_r55_pentagon_incidence): at least
18 pentagons and 906 induced joined-edge pentagons in every Ramsey43 graph.
Those results are preserved as separate context, not imported here.

The initial local solver result was used only to discover the obstruction;
its proof interface emitted no usable trace. The complete published proof
uses the independently checked permutation census and explicit trees instead.
No solver verdict or incomplete monolithic search is a premise. This
candidate-producing phase ends at the complete decision of its declared
43! ordering family; it does not start a neighboring-prime or switching ladder.
