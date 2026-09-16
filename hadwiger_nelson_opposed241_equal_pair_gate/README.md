# The 241-point opposed core has no forced-equal pair

The independently reviewed opposed-B214 conditional core has **241 distinct
plane points and 991 complete unit edges**.  This package gives eight literal
proper four-colourings whose eight-colour signatures distinguish every pair
of vertices.  Therefore no two distinct vertices are forced equal in every
proper four-colouring.

This closes the core's direct equality-half route to the strict
Hadwiger--Nelson record target.  If a four-colourable plane graph on `n`
vertices has a forced-equal pair `p,q` at distance at least `1/2`, two rotated
copies sharing `p` can put the two images of `q` at unit distance and give a
non-four graph on at most `2n-1` points.  Here `2*241-1=481`, and **27,010**
of the core's pairs have distance greater than `1/2`, but every pair has a
checked different-colour witness.  The remaining 1,910 pairs have distance
less than `1/2`; no pair is exactly at the boundary.

The same conclusion holds for every induced subgraph of this fixed physical
core: restrict the appropriate full-core witness.  This is a scoped negative
construction gate, not a five-chromatic graph, a relation census beyond the
different-colour state, or progress below Parts's 509-point record.  The core
retains its separately reviewed complete-input loss; pair neutrality in this
one direction does not contradict that higher-arity obstruction.

## Exact certificate

Coordinates use integer tuples `(a,b,c,d)` for

```text
(a+b*sqrt(33) + i*(c*sqrt(3)+d*sqrt(11)))/36.
```

The verifier reconstructs the two opposed archived B214 copies and the ten
Golomb points, collision-merges them, applies the frozen 241-label selection,
and tests all `C(241,2)=28,920` pairs.  For a difference tuple, squared
distance one is exactly

```text
a*a + 33*b*b + 3*c*c + 11*d*d = 1296,
a*b + c*d = 0.
```

Every submitted word is checked on all 991 edges.  The signature of vertex
`v` is the eight-symbol column formed by its colours in the eight words.  All
241 signatures are distinct, which directly proves the pair claim without a
solver-negative answer.  The first ten points induce the Golomb graph; a
complete normalized three-colour enumeration and one submitted four-word
also recheck that the core is exactly four-chromatic.

The distance-half count is exact.  Comparing a squared norm with `1/4`
reduces to the sign of an integer expression `A+B*sqrt(33)`.  Opposite-sign
terms are compared by their integer squares, with the irrationality of
`sqrt(33)` excluding equality.

Canonical identities are:

```text
points  70c14dfaec7875038c0f3cc1b9f84f5469143f5227fbd49377340bb46e27d908
edges   02e1fbb4c9f94cc5aca57945657706088e25560d3ca0c00217d0d17d647f55ab
words   0e88e2bf0d0c306238db2bdaee31224f89cf04c299f897f3d8b3694981fa3dd0
```

## Reproduction

From the repository root, using CPython 3.11 or later and only the standard
library:

```bash
python3 -B hadwiger_nelson_opposed241_equal_pair_gate/verify.py --check-expected
python3 -O -B hadwiger_nelson_opposed241_equal_pair_gate/verify.py --check-expected
python3 -B hadwiger_nelson_opposed241_equal_pair_gate/controls.py
python3 -O -B hadwiger_nelson_opposed241_equal_pair_gate/controls.py
```

The SAT solver used during discovery supplied positive words only.  It is not
part of replay or the theorem's trust boundary.  No UNSAT result, numerical
distance predicate, hidden graph, or omitted proof trace is used.

## Scope and disposition

The theorem concerns exactly the reviewed 241-point induced core and all its
induced subgraphs.  It does not classify arbitrary subgraphs with added
edges, other extractions from the 343-point parent, higher-arity relations,
different placements, or another forcing source.  The declared two-copy
spindle route stops at this gate; no union, rotation, phase, host, or deletion
variant was generated.

Parts's [509-point, 2,442-edge construction](https://arxiv.org/abs/2010.12665)
remains the supported unrestricted record; Haugland's
[2026 revision](https://arxiv.org/abs/2608.04542) likewise identifies 509 as
current while studying a different restricted family.
