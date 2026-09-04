# All origin-centered double copies of the archived Parts 159 gadget

**Theorem.** Let `A` be the archived Parts `v159e646` point set in the
hash-pinned `points159.tsv`, in its published placement with vertex 0 at the
origin. For every Euclidean isometry `g` fixing the origin, the strict
unit-distance graph on `A union g(A)` is four-colorable.

The quantifier covers every rotation and reflection about this fixed origin,
with no restriction on angles or coordinate fields. It does not cover a
different choice of shared vertices, arbitrary translations, or three copies.

The proof combines the previously proved field-coloring theorem with a
complete finite reduction and a small positive coloring certificate.

## 1. Field and notation

Write

\[
R=\mathbb Q(\sqrt{33}),\quad
E=R(\alpha)=\mathbb Q(i\sqrt3,i\sqrt{11}),\quad \alpha=i\sqrt3.
\]

All 159 points lie in `E`, and `0` is vertex 0. The exact coordinate and edge
checks recover 159 distinct vertices and 646 strict unit edges.

The [field obstruction](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md)
gives an explicit four-coloring of the entire complex field `E`. This prior
theorem is an essential dependency for the branch `u in E` below. It has an
[independent review](../hadwiger_nelson_nonmono_field_obstruction_review3/README.md).

Every origin-fixing isometry has the form `g(z)=uz` or `g(z)=u conjugate(z)`,
where `|u|=1`. For each parity, put `B=A` or `B=conjugate(A)`, preserving the
original labels. Its internal graph is the same labeled 159-vertex graph.

## 2. Three exhaustive cases

If `u in E`, then `A union uB` is a subset of `E`, so the prior field coloring
settles the case, including all possible additional overlaps.

Suppose henceforth `u not in E`. The only overlap is the origin: any
nonzero coincidence `a=ub` would imply `u=a/b in E`. Thus the union has
exactly 317 vertices. Unit edges incident to the shared origin are already
internal to one of the two copies. Call any edge from `a in A minus {0}` to
`ub`, with `b in B minus {0}`, a *new cross edge*.

If there is no new cross edge, arbitrary proper colorings of the two copies
can be permuted to agree at the origin, giving a coloring of the union.

It remains to consider `u not in E` with at least one new cross edge.
This case reduces to finitely many irreducible quadratic polynomials.

## 3. A cross edge determines a quadratic class

For nonzero `a,b`, put

\[
c=\overline a b,\quad
S=|a|^2+|b|^2-1,\quad
\Delta=4|a|^2|b|^2-S^2.
\]

Here `c != 0`, `c in E`, and `S,Delta in R`. For `|u|=1`, expansion gives

\[
|a-ub|=1
\quad\Longleftrightarrow\quad
c u^2-Su+\overline c=0.
\]

Indeed the distance equation is `cu+conjugate(c) conjugate(u)=S`; multiply by
`u` and use `u conjugate(u)=1`.

There are no unit roots if `Delta<0`. For `Delta>=0`, the roots are

\[
u_\pm=\frac{S\pm\sqrt{-\Delta}}{2c}.
\]

Both have modulus one, because their squared modulus is
`(S^2+Delta)/(4 c conjugate(c))=1`. A zero discriminant gives one double root
in `E`. For a positive discriminant, a root is in `E` if and only if
`Delta/3` is a square in `R`. To see this, a square root of the negative real
number `-Delta` in `E` must be purely imaginary, hence must be `alpha y` for
some `y in R`; its square is `-3 y^2`.

Discard negative discriminants and the roots already in `E`. Every remaining
pair defines the irreducible monic polynomial

\[
P_{a,b}(X)=X^2-(S/c)X+\overline c/c\quad\text{over }E.
\]

Two such polynomials have an outside-`E` root in common if and only if they
are equal: both must be the unique monic minimal polynomial of that root.
Consequently, for either root of one class, its complete new cross-edge set
is exactly the set of labeled pairs defining that polynomial. Conversely,
every pair in that class is a unit edge at both roots. This establishes
completeness of the recovered graph, not just a list of selected edges.

Thus each class supplies exactly two distinct unit multipliers and a single
labeled cross-edge set. Distinct classes in one parity have disjoint root
sets. Counts are counts of labeled isometries, not geometric or graph
isomorphism classes.

## 4. Exact arithmetic decisions

The real sign of `a+b sqrt(33)` is determined from the signs of `a,b` and,
when they differ, comparison of `a^2` with `33 b^2`. No nonzero rational pair
has `a^2=33 b^2`.

For the square test in `R`, let `z=a+b sqrt(33)`.

- If `b=0`, it is a square in `R` precisely when `a` or `a/33` is a rational
  square. This follows from `2xy=0` in `(x+y sqrt(33))^2`.
- If `b!=0`, a square root requires a rational square root `n` of
  `a^2-33 b^2`. At least one of `(a+n)/2` and `(a-n)/2` must be a nonzero
  rational square `x^2`. Then `y=b/(2x)` reconstructs a root, which is
  checked directly. Conversely every root has this form.

Rational square tests use integer square roots of the numerator and
denominator. Fractions are canonical arbitrary-precision rationals.

The main implementation normalizes by the leading coefficient `c`.
The separate audit instead writes `c=cr+alpha ci`, with `cr,ci in R`.
If `S!=0`, it groups by `c/S`. If `S=0`, it groups by the real projective
direction of `c`, using `ci/cr` when `cr!=0` and a separate vertical case.
These are equivalent equality tests for the same quadratics. The audit
imports none of the main field arithmetic or enumeration code.

## 5. Exhaustive finite certificate

There are `158^2=24,964` nonzero labeled pairs in each parity. For each parity,
the exact classification is:

| Pair class | Count |
|---|---:|
| Negative discriminant: no unit multiplier | 2,937 |
| All roots in `E` | 12,906 |
| Two unit roots outside `E` | 9,121 |

The last row groups as follows:

| Isometry parity | Irreducible quadratic classes | Unit isometries |
|---|---:|---:|
| Rotation | 1,490 | 2,980 |
| Reflection | 1,377 | 2,754 |
| Total | 2,867 | 5,734 |

These classes have 1 through 20 new cross edges, hence their strict graphs
have 317 vertices and 1,293 through 1,312 edges. The full histogram is in
`expected.json`. There are 2,866 distinct labeled cross-edge sets across the
two parities; no deduplication is needed for the theorem.

`colorings.txt` contains four explicit proper colorings of `A`, each with
color 0 at the origin. Their internal edges are checked directly. For each
quadratic class, `census.py` finds two library colorings `f,h` and a color
permutation `pi` fixing 0 such that

\[
f(a)\ne\pi(h(b))\qquad\text{for every new cross edge }(a,b).
\]

The colorings already agree at the sole overlap and respect both internal
graphs. The displayed inequalities verify every remaining edge. All 2,867
classes have such a witness. This proves the final case of Section 2 and
completes the theorem.

The library was found by starting with the two residue colorings associated
with the conjugate embeddings of `sqrt(33)`, then using one satisfiable
317-vertex graph-coloring instance to obtain two additional component
colorings. Discovery used CaDiCaL through `python-sat==1.8.dev24`. Neither
solver correctness nor regeneration of the library is a proof dependency:
the complete positive witnesses are only 640 bytes and are directly checked.

## 6. Independent checks and scope

`audit.py` uses `E=R+alpha R`, separate rational-pair arithmetic and the
alternative normalization in Section 4. Its canonical stream hashes agree
on every labeled pair classification and every edge-group partition. It
also checks 90 arithmetic controls and all four component colorings.

`check_example.py` directly constructs the four placements

\[
u=(5\pm i\sqrt{39})/8,\qquad B=A\ \text{or}\ \overline A,
\]

in the real radical basis of `Q(sqrt(3),sqrt(11),sqrt(13))`, with integer
coordinates at scale 96. It independently rebuilds every strict unit edge
and checks an actual union coloring, without the polynomial reduction.
The radical introduces a genuine extension of `E`.

The finite claims trust the reviewable exact programs, CPython integers and
fractions, hash-bound coordinates and the positive library. The transition
from the continuous family to the finite census is the ordinary mathematical
proof above; it is not formalized in a proof assistant. No approximate
distance comparison, UNSAT claim, or hidden large certificate is used.

The result is a specific exclusion in the search for smaller five-chromatic
unit-distance graphs. It gives no graph improving the 509-vertex record.
Changing the shared vertices or adding another differently placed gadget
remains outside this theorem. The elementary quadratic reduction and color
permutation gluing are not claimed as new general methods.

Primary construction context: Jaan Parts,
[Graph minimization](https://arxiv.org/abs/2010.12665). Coordinate provenance
is retained in the earlier [SOURCE.md](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md).
The record benchmark is also identified in the introduction of
[Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4).
