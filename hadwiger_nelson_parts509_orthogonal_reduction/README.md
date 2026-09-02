# Orthogonal closure of the Parts-509 L/S placement family

## Exact result

Let `L` be vertices `0..373` and `S` vertices `374..508` in Jaan Parts's
strict 509-point unit-distance graph, and put

\[
K=\mathbb Q(\sqrt3,\sqrt5,\sqrt{11}).
\]

For an origin-fixing orthogonal matrix `T` with entries in `K`, let `G(T)` be
the strict unit-distance graph on the geometric point set `L union T(S)`.
Then:

> Exactly twelve matrices `T` in `O(2,K)` make `G(T)` non-4-colourable: the
> six rotations in the sibling exact rotation classification and six
> orientation-reversing counterparts.  All twelve exceptional placements
> have 509 distinct points, 2,442 strict unit edges, chromatic number 5, and
> are 5-vertex-critical.  They form the same three abstract isomorphism
> classes already found in the rotation family.  Every other `T` in
> `O(2,K)` gives a 4-colourable graph.

In particular, allowing origin-fixing reflections of the fixed `S` gadget
does not produce a unit-distance graph smaller than 509 vertices.  This does
not improve the 509-vertex record or the bounds
`5 <= chi(R^2) <= 7`.

## Solver-free reduction

Every determinant-minus-one matrix in `O(2,K)` has the form

\[
F(c,s)=\begin{pmatrix}c&s\\s&-c\end{pmatrix},
\qquad c^2+s^2=1.
\]

Let

\[
J=\begin{pmatrix}-1&0\\0&1\end{pmatrix}
\]

be reflection in the `y`-axis.  Exact reconstruction of all 374 points of
`L` verifies `J(L)=L`; the induced label permutation is an involution with 14
fixed points.  Direct multiplication gives

\[
J F(c,s)=
\begin{pmatrix}-c&-s\\s&-c\end{pmatrix}
=R(-c,s).
\]

Consequently, reflection of the entire drawing gives an isometry

\[
J\bigl(L\cup F(c,s)S\bigr)=L\cup R(-c,s)S.
\]

The parameter map `(c,s) -> (-c,s)` is a bijection on the `K`-rational unit
circle.  Thus the orientation-reversing placement family is isometric,
parameter by parameter, to the already classified rotation family.  This
argument is solver-free; all SAT/DRAT trust belongs to the prior rotation
classification that it invokes.

The six exceptional reflections correspond to rotation events as follows.

| reflection `c` | reflection `s` | rotation event |
|---|---|---:|
| `1/2` | `-sqrt(3)/2` | 108 |
| `1/2` | `sqrt(3)/2` | 109 |
| `(17+21sqrt(5))/64` | `(-17sqrt(3)+7sqrt(15))/64` | 215 |
| `(17-21sqrt(5))/64` | `(17sqrt(3)+7sqrt(15))/64` | 216 |
| `-17/32` | `-7sqrt(15)/32` | 690 |
| `-1` | `0` | 789 |

## Reproduction

The checker uses the sibling rotation contribution's independent exact
coordinate parser and certificate decoder.  From the repository root:

```bash
python3 -m venv /scratch/parts509-orthogonal-venv
/scratch/parts509-orthogonal-venv/bin/pip install \
  -r hadwiger_nelson_parts509_orthogonal_reduction/requirements.txt
/scratch/parts509-orthogonal-venv/bin/python \
  hadwiger_nelson_parts509_orthogonal_reduction/verify_orthogonal_reduction.py
```

The final line is `all_checks=true`; the complete compact output is in
`expected_check.txt`.  The checker:

1. parses all coordinates exactly in `K`;
2. reconstructs and checks the 374-label permutation induced by `J`;
3. verifies the matrix bridge on every one of the 135 `S` points at every
   exceptional parameter;
4. binds the rotation and criticality certificates by SHA-256;
5. checks that the three certified isomorphism classes cover all six
   exceptional rotation events and that each has 509 distinct points.

To replay the substantially heavier prior rotation theorem rather than just
checking the new bridge, run its sibling independent checker as documented in
[`hadwiger_nelson_parts509_rotation_scan`](../hadwiger_nelson_parts509_rotation_scan/README.md).

## Trust boundary and scope

- The new reduction itself is elementary matrix algebra.  The finite fact
  `J(L)=L` is recomputed exactly with SymPy's algebraic-field representation;
  no floating-point comparison is used.
- The claims that exactly six rotations are exceptional, that they form three
  graph classes, and that they are 5-vertex-critical depend on the sibling
  rotation scan and criticality certificate.  That contribution separately
  checks positive colourings and exact event completeness, and uses
  DRAT-checked refutations for its new negative instances.
- SHA-256 binds bytes but does not prove their mathematical interpretation;
  that interpretation is supplied by the exact parser, bridge checker, and
  the prior contribution's independent checker.
- The theorem covers only origin-fixing orthogonal transformations over `K`
  of these fixed `L` and `S` gadgets.  It says nothing about translations,
  transformations outside `K`, different gadgets, or delete-and-repair
  modifications.

Parts's primary paper describes type-M constructions using relative rotations
and says that working constructions with other rotations were not then known:
<https://arxiv.org/abs/2010.12665>.  A targeted search located no published
reflection-family classification.  The result here is best viewed as a short
structural corollary that closes an explicit caveat of the prior rotation
scan, not as a priority claim for any individual drawing.

## Files

- `verify_orthogonal_reduction.py` — exact symmetry and certificate-binding
  checker.
- `expected_check.txt` — compact expected output.
- `requirements.txt` — pinned material Python dependency.
