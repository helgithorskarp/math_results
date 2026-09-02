# Exact rigidity and sharp edge resilience of the Parts-509 framework

## Result and scope

Let `(G,p)` be the strict bar-and-joint framework on Jaan Parts's 509 exact
points: `G` contains every one of the 2,442 pairs at Euclidean distance one.
Write `R(G,p)` for its `2442 x 1018` planar rigidity matrix.

This directory certifies the following exact statements.

1. `rank R(G,p) = 1015 = 2*509-3`; hence `(G,p)` is infinitesimally rigid.
2. For every vertex `v`, the inherited framework `(G-v,p)` has rank
   `1013 = 2*508-3`; hence all 509 one-vertex deletions are infinitesimally
   rigid.
3. For every edge set `D` with `|D| <= 2`, `rank R(G-D,p) = 1015`; deleting
   any two bars still leaves an infinitesimally rigid framework.
4. The edge bound is sharp.  Vertex 310 has four incident edges, with canonical
   edge-list indices `[1277,1435,1784,1804]`.  After deleting the first three,
   the rank is exactly 1014.  Thus the minimum number of edge deletions that
   produces an infinitesimal flex is three.

The sibling criticality certificate establishes that `G` is 5-chromatic and
every `G-v` is 4-chromatic.  Combining the two results, all 509 chromatic
vertex deletions remain rigid frameworks.  This contribution does **not** find
a graph below 509 vertices, improve `5 <= chi(R^2) <= 7`, prove global rigidity,
or exclude a discrete construction outside this fixed drawing.  In particular,
an infinitesimal-rigidity statement must not be inflated into uniqueness of all
unit-distance realizations.

## Rigidity matrix

For an edge `uv`, its row has the two-vector `p(u)-p(v)` in the columns of `u`,
the opposite vector in the columns of `v`, and zero elsewhere.  An
infinitesimal motion `z` satisfies

```text
(p(u)-p(v)) dot (z(u)-z(v)) = 0
```

for every edge.  Translations and rotation give a three-dimensional kernel,
so the rank is at most `2n-3`.  Equality is precisely infinitesimal rigidity in
the plane.  This is the standard rigidity-matrix criterion; see Asimow and
Roth, *The rigidity of graphs*, Trans. AMS 245 (1978), 279-289,
<https://www.ams.org/journals/tran/1978-245-00/S0002-9947-1978-0511410-9/>.

## Exact finite-field certificate

Every coordinate lies in

```text
K = Q(sqrt(3), sqrt(5), sqrt(11)).
```

The primary checker maps the coordinate ring to `F_p` for `p=1000081` using

```text
sqrt(3) -> 35512, sqrt(5) -> 183365, sqrt(11) -> 29480.
```

The three displayed squares are `3,5,11 (mod p)`, and no coordinate
denominator vanishes.  A matrix minor that is nonzero after this specialization
was nonzero over `K`: a ring homomorphism cannot map zero to a nonzero element.
Thus every modular lower rank bound below is also a characteristic-zero lower
rank bound.  The Euclidean upper bounds then give equality.

The deterministic reduction finds a 1,015-row basis `B`, 1,015 coordinate
columns `C`, and the invertible square matrix

```text
M = R[B,C].
```

For the 1,427 nonbasis rows `N`, put

```text
A = R[N,C] M^(-1).
```

After changing row coordinates by the invertible matrix `M`, the full row
matroid is represented by `[I; A]`.

### Why the coefficient checks prove two-edge resilience

Every column of `A` has at least two nonzero entries.  Therefore, after deleting
one basis row and at most one nonbasis row, another nonbasis row replaces the
basis row.  Moreover, the 1,015 columns of `A` are pairwise nonproportional
(the checker normalizes each at its first nonzero entry and compares the exact
vectors).  Hence every two columns have rank two, so after deleting two basis
rows two nonbasis rows replace them.  If no basis row is deleted, `B` itself
survives.  These three cases exhaust every deletion of at most two edges.

The primary support range is `2..1379`; the SHA-256 of the normalized column
stream is

```text
b0b9d158e84cae41a5cd20c80de5983fa40276cba6db429ce3084e9c99bd3538
```

### Why the coefficient checks prove all vertex deletions rigid

For a vertex `v`, let `I_v` be the positions in `B` of the basis edges incident
with `v`, and let `J_v` be the retained nonbasis edges.  Directly from `[I;A]`,
the row rank after removing every edge incident with `v` is

```text
1015 - |I_v| + rank A[J_v,I_v].
```

The checker evaluates these 509 small matrices.  Every result is 1013, the
maximum possible rank after the two coordinate columns of `v` are removed.

### Sharpness at three edges

Deleting three of the four edges incident with vertex 310 leaves that vertex
with one constraint.  The framework on the other 508 vertices has rank at most
1013, and the last incident row raises rank by at most one, so the resulting
rank is at most 1014.  Direct modular elimination gives rank 1014, proving
equality and showing that the two-edge resilience cannot be strengthened.

## Independent check

`independent_check.py` neither imports the primary checker nor the sibling
multiquadratic-field implementation.  It parses and denests the raw Mathematica
coordinate expressions itself, specializes at the different splitting prime
`p=131` with roots `(38,23,50)`, and uses SymPy's sparse `DomainMatrix` linear
algebra instead of python-flint.  It independently obtains

```text
rank=1015
coefficient support range=2..1374
distinct projective coefficient columns=1015
vertex deletion rank histogram={1013: 509}
sharp three-edge deletion rank=1014
```

Both implementations select the same deterministic row basis, whose index-list
SHA-256 is

```text
6bfc39c58d4e26f46498fecd338d185ff58a615c359b871abf6b13c941d71df3
```

Agreement at two different primes is additional fault-detection, while either
successful specialization alone suffices for the exact lower-rank proofs.

## Reproduction

From the root of this repository, using CPython 3.11 or newer:

```bash
python3 -m venv /scratch/parts509-rigidity-venv
/scratch/parts509-rigidity-venv/bin/pip install -r \
  hadwiger_nelson_parts509_rigidity/requirements.txt

/scratch/parts509-rigidity-venv/bin/python \
  hadwiger_nelson_parts509_rigidity/rigidity_certificate.py verify
/scratch/parts509-rigidity-venv/bin/python \
  hadwiger_nelson_parts509_rigidity/independent_check.py verify
```

Expected final lines from both programs include:

```text
all_checks=true rank=1015 edge_deletion_tolerance=2 vertex_deletions_rigid=509 sharp_three_edge_rank=1014
```

On the certification host the primary and independent runs took about 30 and
10 seconds respectively when run concurrently.  Generated matrices and any
diagnostic output belong under `/scratch`; none is committed.

## Inputs and trust boundary

The primary checker imports the sibling
`hadwiger_nelson_parts509_criticality/parts509.py`, reconstructs all exact unit
pairs from `parts509.vtx`, and requires:

```text
coordinate SHA-256  770a585a6c1e1222355322707479cb826e9ada560279da904ef89c15c99ff0b5
edge-list SHA-256   5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c
```

Its trust boundary is CPython rational arithmetic, SymPy 1.14.0 for coordinate
parsing/denesting, the sibling eight-basis field implementation, python-flint
0.8.0 modular linear algebra, and the input coordinates.  The independent
checker trusts its separately written SymPy parser, SymPy's `DomainMatrix`, and
the hash-pinned sibling `edges.json`; it verifies every listed edge after
specialization but inherits exact edge completeness from the primary checker.
Neither route uses floating-point arithmetic, a SAT solver, or an uncommitted
proof log.  The short human bridge from modular minors and `[I;A]` to the stated
rank conclusions is not formalized in a proof assistant.

## Status and prior work

This is an exact computer-assisted structural theorem about the known record
framework, not a new chromatic construction.  Parts's paper introduces the
509-vertex graph and its minimization method but does not appear to discuss the
rigidity matrix or deformation resilience:

- Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane*, Geombinatorics 29(4) (2020), 137-166,
  <https://arxiv.org/abs/2010.12665>.

Targeted searches on 2026-09-02 for the Parts graph together with “rigidity,”
“infinitesimal rigidity,” “framework,” and “flex” found no prior rank,
vertex-deletion, or edge-resilience classification of this realization.  The
result is therefore described only as apparently new to the searched sources;
no historical-priority claim is made.
