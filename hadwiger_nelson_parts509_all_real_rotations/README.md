# All-real orthogonal classification of the Parts-509 L/S gadgets

## Exact result

Let `L` be vertices `0..373` and `S` vertices `374..508` of Jaan
Parts's strict 509-point unit-distance graph.  Their coordinates lie in

\[
K=\mathbb Q(\sqrt3,\sqrt5,\sqrt{11}).
\]

For any real orthogonal matrix `T`, let `G(T)` be the strict unit-distance
graph on the geometric point set `L union T(S)`.  This contribution proves:

> **Theorem (exact computer-assisted).**  Among all rotations
> `T in SO(2,R)`, `G(T)` is non-4-colourable at exactly six rotations.  They
> are the six `K`-rational rotations in the sibling exact classification.
> Every rotation whose matrix entries do not both lie in `K` gives a
> 4-colourable graph.

The reflection reduction in
[`hadwiger_nelson_parts509_orthogonal_reduction`](../hadwiger_nelson_parts509_orthogonal_reduction/README.md)
is field-independent: reflection of the entire plane sends every
determinant-minus-one placement to a rotation while preserving `L`.  It
therefore gives the following immediate corollary.

> **Corollary.**  The same classification holds over all `T in O(2,R)`.

The six exceptional placements are:

| `cos(theta)` | `sin(theta)` |
|---|---|
| `-1/2` | `-sqrt(3)/2` |
| `-(17+21sqrt(5))/64` | `(-17sqrt(3)+7sqrt(15))/64` |
| `-1/2` | `sqrt(3)/2` |
| `(-17+21sqrt(5))/64` | `(17sqrt(3)+7sqrt(15))/64` |
| `17/32` | `-7sqrt(15)/32` |
| `1` | `0` |

As certified in the sibling rotation contribution, all six have 509 distinct
points, 2,442 strict unit edges, chromatic number exactly five, and are
5-vertex-critical; they form three abstract isomorphism classes.  Thus no
origin-fixing orthogonal placement of these fixed `L` and `S` gadgets improves
the 509-vertex record.  This is a family closure, **not** a new record graph.
It says nothing about translations, different gadgets, or delete-and-repair
modifications.

## Structural reduction

Write a rotation as

\[
R(c,s)=\begin{pmatrix}c&-s\\s&c\end{pmatrix},\qquad c^2+s^2=1.
\]

For `p in L`, `q in S`, and `p != 0`, put

\[
A=p_xq_x+p_yq_y,\quad B=p_yq_x-p_xq_y,\quad
C=(\lVert p\rVert^2+\lVert q\rVert^2-1)/2.
\]

Then `p` and `R(c,s)q` are at unit distance exactly when

\[
Ac+Bs=C. \tag{1}
\]

Thus every non-invariant cross pair defines a `K`-rational projective line in
the `(c,s)` plane, and event rotations are its intersections with the unit
circle.  The discriminant

\[
\Delta=\lVert p\rVert^2\lVert q\rVert^2-C^2
\]

shows that the intersections lie in `K^2` exactly when `sqrt(Delta) in K`.
Tangency (`Delta=0`) is necessarily `K`-rational.

The decisive observation is this: if a non-`K` rotation satisfied two
nonproportional equations of the form (1), Cramer's rule would put both `c`
and `s` in `K`, a contradiction.  Hence **all cross edges at a non-`K` event
come from one projective line class**.  The two conjugate intersections of a
non-`K` line have exactly the same labeled edge set.  It is therefore enough
to 4-colour one finite graph per non-`K` line class, rather than enumerate or
compare arbitrary real algebraic angles.

Exact enumeration gives:

| item | count |
|---|---:|
| L/S radius-pair classes | 756 |
| admissible radius-pair classes | 547 |
| admissible non-invariant cross-pair incidences | 37,861 |
| tangent cross-pair incidences | 576 |
| projective event-line classes | 9,024 |
| line classes with `K`-rational intersections | 2,167 |
| non-`K` line classes | 6,857 |
| non-`K` event rotations (two per line) | 13,714 |
| `K`-rational event rotations (sibling theorem) | 790 |
| all real event rotations | 14,504 |

The 6,857 non-`K` graphs are covered by 55 explicit proper 4-colourings.  The
certificate binds the sorted canonical line keys by SHA-256 and assigns one
packed witness to every key.  The generator needed 54 SAT calls after seeding
the library with the prior generic coloring; SAT is not used by either
verifier.

There is no hidden quotient problem from coincident labels.  If `p=R(c,s)q`,
then direct dot/determinant formulas express `c,s` using `p,q in K^2`, so the
rotation is `K`-rational.  The independent checker reconstructs 66 such
coincidence rotations.  Thus no non-`K` event identifies an `L` label with an
`S` label; the explicit labeled colorings descend to the strict geometric
point sets.  The prior `K`-rotation checker handles coincidences at the 790
`K` events.

For the orientation-reversing corollary, every determinant-minus-one matrix
has the form

\[
F(c,s)=\begin{pmatrix}c&s\\s&-c\end{pmatrix}.
\]

The exact finite symmetry check in the sibling orthogonal reduction gives
`J(L)=L` for `J=diag(-1,1)`, and `J F(c,s)=R(-c,s)`.  This argument uses no
field-membership hypothesis, so it applies to every real `(c,s)` on the unit
circle.

## Reproduction

CPython 3.11 and the pinned packages in `requirements.txt` were used.  Keep
the environment outside the repository:

```bash
python3 -m venv /scratch/parts509-all-real-venv
/scratch/parts509-all-real-venv/bin/pip install -r requirements.txt

# Primary exact solver-free replay (about 3 minutes on the reference host).
/scratch/parts509-all-real-venv/bin/python verify.py certificate.json

# Separate parser/field representation and exact replay (about 5 minutes).
/scratch/parts509-all-real-venv/bin/python independent_check.py certificate.json

# Fast arithmetic and serialization boundary tests.
/scratch/parts509-all-real-venv/bin/python -m unittest -v test_exact.py
```

Expected compact outputs are in `expected_verify.txt` and
`expected_independent.txt`.  To regenerate the witness library (CaDiCaL is
used only here):

```bash
/scratch/parts509-all-real-venv/bin/python generate_certificate.py certificate.json
```

To replay the heavier theorem for the 790 `K`-rational events and the six
exceptional placements, follow the commands in the sibling
[`rotation_scan` README](../hadwiger_nelson_parts509_rotation_scan/README.md).

## Evidence and trust boundary

- `verify.py` reparses all 509 coordinates, uses rational arithmetic in the
  eight-element multiquadratic basis, rigorously decides signs by refining
  integer-derived dyadic intervals for the basis radicals, re-enumerates all
  event lines, and checks square membership with a recursive exact tower
  algorithm.  It recomputes the 2,412 internal gadget edges and replays every
  assigned coloring without a solver.
- `independent_check.py` uses the sibling independent parser based on SymPy's
  `AlgebraicField`, converts to the multiquadratic basis only after deriving
  each line, independently reconstructs the same class digest and square
  split, rebuilds the strict Parts edge list from the hash-bound coordinates,
  and replays all witnesses.  It imports neither the new generator nor
  `common.py`.
- The new positive 4-colourability claim does not trust CaDiCaL: every model
  is stored and checked edge-by-edge.  CaDiCaL/Python-SAT is only a witness
  discovery mechanism in `generate_certificate.py`.
- The claims about the 790 `K` events, the six non-4-colourable exceptions,
  criticality, and their isomorphism classes depend on the sibling exact
  rotation and criticality certificates.  Their bytes are bound here by
  SHA-256.  The two new negative SAT instances in that work are bound to
  scratch-only DRAT proofs checked by `drat-trim`; those large traces are not
  duplicated here.
- The structural line-class and reflection arguments are elementary exact
  algebra but are not formalized in a proof assistant.  Parsing trusts SymPy
  1.14.0; subsequent equality, sign, field membership, coloring, and digest
  checks use exact integer/Fraction operations.
- SHA-256 binds source and certificate bytes but does not by itself establish
  their mathematical interpretation; the two re-enumerators and explicit
  proof above provide that bridge.

## Files

- `common.py` — primary exact field arithmetic, sign bounds, and event-line census.
- `generate_certificate.py` — deterministic SAT-assisted witness discovery.
- `certificate.json` — 55 packed colorings, 6,857 assignments, source hashes, counts, and line-key digest.
- `verify.py` — primary solver-free exact checker.
- `independent_check.py` — separate SymPy-field census and replay.
- `test_exact.py` — fast exact-arithmetic and serialization tests.
- `expected_verify.txt`, `expected_independent.txt` — compact expected output.
- `requirements.txt` — pinned material Python dependencies.

## Sources

- Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane*, Geombinatorics 29(4) (2020), 137–166,
  <https://arxiv.org/abs/2010.12665>.
- Marijn J. H. Heule, *Computing Small Unit-Distance Graphs with Chromatic
  Number 5*, Geombinatorics 28(1) (2018), 32–50,
  <https://arxiv.org/abs/1805.12181>.
