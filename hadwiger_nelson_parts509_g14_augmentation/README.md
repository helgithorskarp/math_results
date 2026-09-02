# G14 completion response inside Parts-509

**Claim status:** exact computer-assisted theorem.  This directory certifies a
510-vertex 5-vertex-critical unit-distance graph and a complete 16-case subset
profile arising from one exact G14 embedding in the completion geometry of
Parts's 509-vertex graph.  It also certifies that the reflected G14 embedding
cannot repair any single Parts-graph vertex.  The result does **not** improve
the 509-vertex record or the bounds `5 <= chi(R^2) <= 7`.

## Statement

Let `G` be the strict unit-distance graph on Parts's 509 points, and let `Q3[i]`
denote entry `i` of the exact completion list in
`../hadwiger_nelson_parts509_swap_closure/completion_points.json`.  The prior
embedding certificate in `../hadwiger_nelson_parts509_g14_g15_embedding`
identifies two extensions of a common 15-point carrier to the 14-point
three-distance graph G14.  Their four added completion points are

```text
A = (Q3[470], Q3[523], Q3[653], Q3[619])
B = (Q3[411], Q3[750], Q3[454], Q3[417]).
```

For `S` contained in the four points of `A`, form the strict unit-distance graph

```text
H_S = G - V[350] + S.
```

The complete subset classification is

```text
H_S is not 4-colourable  <=>  {Q3[523], Q3[619]} is contained in S.
```

The forward direction for the other twelve subsets is witnessed by twelve
explicit proper 4-colourings.  For the reverse direction it is enough to check
the minimal pair.  The graph

```text
H = G - V[350] + {Q3[523], Q3[619]}
```

has 510 vertices, 2,445 strict unit edges, and chromatic number five.  Moreover,
`H-v` is 4-colourable for every one of its 510 vertices, so `H` is
5-vertex-critical.  Its canonical edge-list SHA-256 (lines `u v\n` in the local
vertex order recorded in the certificate) is
`8a5667308a70cf60aaff2f2e5eee0234c94e9078713bd34373608b7852d4d51a`.

The reflected embedding behaves differently.  For every base vertex `v`, the
513-vertex graph `G + B - v` is 4-colourable.  Hence no subset of the four
points of `B` repairs any single vertex deletion of `G`.  The full B
augmentation has 2,458 strict unit edges and edge-list SHA-256
`5a218c1b896b1cca3971e7eaf9526c2d6cb4e3cfe45da996049a96b2f38d6e54`.

This is a structural bridge between the G14 three-distance gadget and ordinary
unit-distance criticality.  Targeted literature, repository, and committed
Discovery Net searches through 2026-09-02 found no statement of this exact
subset profile or 510-vertex critical graph; no priority claim is made.

## Certificate and proof architecture

`certificate.json` contains:

* all 510 proper 4-colourings of `H-v`, packed at two bits per retained vertex;
* one proper 4-colouring for each of the twelve A-subsets not containing the
  critical pair;
* all 509 proper 4-colourings of `G+B-v` for base vertices `v`;
* exact dependency, edge-list, and packed-payload hashes.

The proper-colouring claims are solver-free after generation: the verifier
reconstructs every strict unit edge by exhaustive exact arithmetic and checks
every retained-edge inequality.  Since adding one vertex increases chromatic
number by at most one, the deletion rows also give `chi(H-v)=4` once
`chi(H)=5` is established.

Non-4-colourability of `H` is the separate proof-checked boundary.  The
deterministic CNF has one at-least-one-colour clause per vertex and four
same-colour exclusion clauses per edge, plus three sound triangle pins.  The
encoding omits at-most-one clauses: adjacent vertices receive disjoint
nonempty selected-colour sets, so choosing any selected colour at each vertex
gives an ordinary proper colouring.  CaDiCaL `sc2021` produced a DRAT
refutation, and `drat-trim` returned `s VERIFIED`.  Exact hashes, byte counts,
and core statistics are in `proof_manifest.json`.  The CNF and 6.76 MB proof
remain under `/scratch` and are intentionally not committed.

## Reproduction

Verification uses the sibling Parts coordinates and completion list.  CPython
3.11 and SymPy 1.14.0 were used.

```bash
python3 g14_augmentation.py verify
python3 independent_sympy_check.py
```

The first checker uses exact rational coefficients in
`Q(sqrt(3),sqrt(5),sqrt(11))`.  The independent checker imports none of the
primary verifier or sibling field implementations: it reparses the coordinates
into SymPy's `AlgebraicField`, rebuilds every relevant unit edge, independently
decodes the certificate, replays 2,517,595 retained-edge checks, and rescans all
eight cited completion-point neighborhoods.  Expected summaries are in
`expected_output.txt`.

To regenerate the coloring witnesses, keep the environment and output under
`/scratch`:

```bash
python3 -m venv /scratch/g14-augmentation-venv
/scratch/g14-augmentation-venv/bin/pip install -r requirements.txt
/scratch/g14-augmentation-venv/bin/python g14_augmentation.py generate \
  /scratch/g14-augmentation-certificate.json --solver cadical195
```

SAT is used only to find the explicit colorings.  Different solver versions may
produce a different packed payload, but the result is valid if both solver-free
checkers accept it.

To regenerate and check the lower-bound proof:

```bash
python3 g14_augmentation.py cnf /scratch/g14-pair-4color.cnf
cadical -q /scratch/g14-pair-4color.cnf /scratch/g14-pair-4color.drat
drat-trim /scratch/g14-pair-4color.cnf /scratch/g14-pair-4color.drat
```

## Trust boundary

* Exact geometry trusts the published Parts coordinate input, CPython integers
  and `Fraction`, SymPy 1.14.0 for parsing/denesting, and the primary small
  multiquadratic-field implementation.  The independent checker replaces the
  latter with SymPy `AlgebraicField` arithmetic and uses no floating-point
  decision.
* The eight completion coordinates are imported from the separately certified
  exhaustive Q3 list.  Both checkers independently rescan their complete
  neighborhoods against all 509 Parts vertices; this directory does not
  re-enumerate the other 1,150 completion points.
* All 4-colourability and vertex-criticality upper-side claims trust only the
  compact witnesses and the two solver-free checkers.  PySAT/CaDiCaL model
  generation is outside that trust boundary.
* Non-4-colourability trusts the deterministic CNF bridge, the recorded proof
  bytes, and the C implementation of `drat-trim`.  The proof is not a
  proof-assistant formalization.

## Sources

* Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane*, Geombinatorics 29(4) (2020), 137--166:
  <https://arxiv.org/abs/2010.12665>.
* Canonical G14/G15 data and proofs:
  <https://github.com/HeliCorgi/fourteen-points-six-colors>.
