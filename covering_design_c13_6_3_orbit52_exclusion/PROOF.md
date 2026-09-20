# Proof and certificate boundary

## 1. Conditional normal form

Let `B` be a 20-block `(13,6,3)` cover with point degrees `(12,9^12)`. Write
`h` for the degree-12 point and label the low points `0,...,11`.

At a low point `p`, deleting `p` from its nine incident blocks produces an
optimal nine-block `(12,5,2)` cover. The imported exact classification says
that every point degree in this link lies in `{3,4,5}` and that at most three
link points have degree five. Therefore every low pair has block codegree
between three and five.

In particular, every pair `{h,p}` has codegree at most five. Summing these 12
codegrees over the 12 blocks through `h` gives `12*5=60`, so all are exactly
five. Thus every low point occurs five times through `h` and, since its total
degree is nine, four times in the eight blocks away from `h`. Since `h` is
already a degree-five point in the link at `p`, at most two other low points
`q` can have low-pair codegree five with `p`.

Suppose three blocks through `h` share a low triple and their residual pairs
form `P3+K2`. Relabeling the low points makes their residues

```text
01234, 01245, 01267.
```

Put `Q={0,1,2}`, let `Y` be the nine remaining through-`h` residues, and let
`Z` be the eight blocks avoiding `h`. Their row sizes and column sums are

```text
Y: row size 5, column sums (2,2,2,4,3,4,4,4,5,5,5,5),
Z: row size 6, column sums (4^12).
```

Every low pair not covered by a fixed residue must occur in `Y`, because the
corresponding triple with `h` must be covered. Every low pair has total
codegree in `{3,4,5}`, each low point has at most two codegree-five low
neighbors, and every low triple occurs in a fixed row, `Y`, or `Z`. These are
exactly the constraints encoded by `generate_orbit52_cnf.py`.

## 2. Seventeen `Q`-free row orbits

The three `Q` columns have only six incidences among the nine `Y` rows, so
some row avoids `Q`. Outside `Q`, the fixed configuration is a path on
`{3,4,5}`, an edge on `{6,7}`, and four unused points `{8,9,10,11}`.

A `Q`-free 5-set is classified under the full residual automorphism group by

```text
(whether 4 is chosen,
 number chosen from {3,5},
 number chosen from {6,7},
 number chosen from {8,9,10,11}).
```

The four entries sum to five. There are exactly 17 feasible vectors. Direct
enumeration of all `C(9,5)=126` rows gives orbit sizes

```text
2,4,2,16,12,4,12,4,1,8,6,8,24,8,6,8,1,
```

which sum to 126. The audit derives this list without accepting a table from
the manifest. Designating one `Q`-free row and mapping it to the representative
of its orbit is therefore exhaustive.

## 3. Dual Venn split

The three fixed rows cover, for any pair inside `Q`, third points `h`, the
third point of `Q`, and all five points of the residual support. The four
unused low points still require coverage. Thus each `Q` pair occurs in one
or two additional rows, because its total codegree is at most five. Up to
permuting `Q`, the three additional-codegree labels are

```text
111, 211, 221, 222.
```

After the designated `Q`-free row is removed, let `T_i` be the two remaining
`Y` rows containing `i in Q`. The orbit of the three labelled 2-subsets under
row permutation is determined by

```text
(a,b,c,t) = (|T0 intersect T1|, |T0 intersect T2|,
             |T1 intersect T2|, |T0 intersect T1 intersect T2|).
```

For `221`, the stabilizer swaps the first two coordinates; for `222`, all
three pair-intersection coordinates may be sorted. If `e_ij` is the prescribed
additional codegree, the corresponding size-four column sets among the eight
`Z` rows must have pair intersections `e_ij-|Ti intersect Tj|`. Their triple
intersection determines all eight Venn-cell sizes. Nonnegativity leaves four
joint types for `221` and seven for `222`.

The audit independently enumerates all triples of 2-subsets and 4-subsets of
an eight-set and recovers every allowed through type and triple-intersection
value. The `111` and `211` cases are left unsplit and use only sound row
sorting. Therefore the case family is complete and has size

```text
17 * (2 + 4 + 7) = 221.
```

## 4. CNF equivalence and symmetry

The 204 primary variables are the entries of the `9 x 12` matrix `Y` and the
`8 x 12` matrix `Z`.

- Tseitin variables are equivalent to their two- or three-entry conjunctions.
- One-hot saturated-count automata enforce row sums, column sums, pair
  codegrees, and codegree-five neighbor counts exactly.
- Through-row pair conjunctions cover every triple `{h,p,q}` not already
  covered by a fixed row.
- Through/away triple conjunctions cover every low triple not already covered
  by a fixed row.
- Strict binary row ordering is imposed only among rows with the same fixed
  `Q`-membership data. This removes row permutations and no designs.
- Remaining through rows are forbidden to equal the designated row or any
  fixed row. Strict ordering makes the remaining through rows and all away
  rows distinct.

Distinctness loses no target: a repeated block in a 20-block cover could be
deleted to give a 19-block cover, contradicting the imported lower bound 20.

Conversely, the primary part of any satisfying assignment gives three fixed
blocks, nine additional through-`h` blocks, and eight away blocks with the
specified degrees. The pair clauses cover all triples containing `h`; the
triple clauses cover all-low triples. Hence it decodes to the normalized
target cover. The CNF family is therefore equisatisfiable with the orbit-52
extension problem.

The audit exhausts 2,531 truth-table checks for the conjunction, exact-count,
and lexicographic primitives, directly checks the orbit partitions, and
regenerates every CNF hash.

## 5. Certificate result

CaDiCaL 3.0.1 returned UNSAT on all 221 instances. Unmodified `drat-trim`
independently accepted all 221 binary DRAT traces. The exact aggregate sizes
are

```text
CNFs:        275,677,984 bytes,
DRAT traces: 460,621,219 bytes.
```

`EXPECTED.json` records each instance size and SHA-256 and each proof size,
SHA-256, solver exit, and checker status. The ordered CNF-hash-list and
proof-hash-list SHA-256 values are respectively

```text
a3d5697a32cf574b9a3cb69a85bb4c771bd2b1ab1395997748224be6442d3c02
3f63974f370643e121368072157209807636839c70ac707c84bd2caa41ed2e66.
```

Thus the normalized `P3+K2` extension is impossible.

## 6. Structural corollary and scope

Three distinct residual pairs have one of five support types:

```text
3K2, P3+K2, P4, K1,3, K3.
```

The predecessor certificate excludes `3K2`; this theorem excludes `P3+K2`;
and the sharp support lemma excludes `P4`, `K1,3`, and `K3`. Consequently, in
the exceptional `(12,9^12)` profile, no three blocks through `h` share a low
triple.

The theorem trusts the written normal-form and completeness arguments, the
imported optimal-link classification and lower bound, CPython integer/file
semantics, the compact generators, and `drat-trim` plus its build/runtime and
hardware. DRAT checking removes reliance on CaDiCaL's UNSAT reasoning, but
not on the mathematical encoding or certificate checker. This result closes
one local stratum; it does not exclude the point-degree profile or determine
`C(13,6,3)`.
