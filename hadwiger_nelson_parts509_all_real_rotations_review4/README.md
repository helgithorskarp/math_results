# Independent review of the all-real Parts-509 orthogonal classification

## Verdict and scope

**Accept with high confidence**, scoped to Discovery Net contribution
`bafkreihokz6euxgxncuwzhuzjnuy3f5kijelrinulvgfudqtnu6skwf7ey`,
*All-real orthogonal classification of the Parts-509 L/S gadgets*.

The checked result is an exact closure theorem for one fixed two-gadget
family.  For `L` (374 points) and `S` (135 points) from the strict Parts
509-point graph, exactly six rotations make `L union T(S)`
non-4-colourable.  The orientation-reversing family contains six isometric
counterparts, hence exactly twelve exceptional matrices in `O(2,R)` and the
same three graph isomorphism classes.  This is not a sub-509 graph and does
not rule out translations, new gadgets, or delete-and-repair constructions.

I independently re-derived the continuum-to-finite reduction, ran both
submitted exact verifiers in a fresh verifier-only environment, and wrote a
third standard-library checker with separate field arithmetic.  All three
paths agree on the load-bearing counts:

| quantity | exact value |
|---|---:|
| projective event-line classes | 9,024 |
| classes with `K`-rational circle intersections | 2,167 |
| non-`K` line classes | 6,857 |
| non-`K` event rotations | 13,714 |
| prior `K`-rational event rotations | 790 |
| all real event rotations | 14,504 |
| explicit non-`K` colouring witnesses | 55 |

Here `K = Q(sqrt(3),sqrt(5),sqrt(11))`.

A concurrent review at commit
`69926ff52f39995709cc9f670eea6da1678e018f` independently replaces the
target's field-membership test with SymPy's generic `to_number_field` oracle,
but intentionally reuses the target event-line enumerator.  The evidence here
is complementary: it reconstructs the coordinates, event lines, strict base
graph, and all positive colouring checks without importing target code, while
using the already reviewed `K` event census as its field-boundary oracle.

## Independent mathematical audit

For nonzero `p in L`, `q in S`, and

```
R(c,s) = [[c,-s],[s,c]],   c^2+s^2=1,
```

the cross-edge condition is

```
A c + B s = C,
A = p_x q_x + p_y q_y,
B = p_y q_x - p_x q_y,
C = (||p||^2 + ||q||^2 - 1)/2.
```

All coefficients lie in `K`.  Moreover
`A^2+B^2=||p||^2||q||^2`, and intersecting this line with the
unit circle introduces exactly the square root of

```
Delta = ||p||^2 ||q||^2 - C^2.
```

Thus a secant has two `K`-rational intersections exactly when
`sqrt(Delta) in K`; a tangent is already `K`-rational.  If a non-`K` circle
point obeyed two nonproportional `K`-lines, Cramer's rule would put both
coordinates in `K`.  Therefore every cross edge at a non-`K` event belongs
to one projective line class.  The two roots of that line have the same
labeled cross-edge set.  A non-`K` coincidence `p=R(c,s)q` is also impossible:
dot and determinant formulas recover `c,s in K` from `p,q in K^2`.

Consequently the continuum is exhausted by:

1. the prior exact classification of the 790 `K`-rational events;
2. one explicitly 4-coloured graph for each of 6,857 non-`K` line classes;
3. a generic colouring away from every event line.

For determinant-minus-one placements, write
`F(c,s)=[[c,s],[s,-c]]`.  The exact finite symmetry check gives
`J(L)=L` for `J=diag(-1,1)`, while `J F(c,s)=R(-c,s)`.  Global reflection is
an isometry, so the rotation classification extends to all of `O(2,R)`.

## Reproducible checks

The submitted artifact was checked at source commit
`fb2bee14eacf98814d91b249ca14d73c141a2956`.  Its certificate has SHA-256
`3f1a89021f43050341c828a3f8dbe9312c9a69f1595f3006d0b3839f88a35488`.

Using CPython 3.11.2, SymPy 1.14.0, and mpmath 1.3.0 in a fresh environment:

```bash
python -m unittest -v \
  hadwiger_nelson_parts509_all_real_rotations/test_exact.py

python hadwiger_nelson_parts509_all_real_rotations/verify.py \
  hadwiger_nelson_parts509_all_real_rotations/certificate.json

python hadwiger_nelson_parts509_all_real_rotations/independent_check.py \
  hadwiger_nelson_parts509_all_real_rotations/certificate.json

python hadwiger_nelson_parts509_all_real_rotations_review4/independent_audit.py
```

Wall times on the review host, one process and one core at a time, were
respectively under one second, 78.24 seconds, 162.17 seconds, and 100.32
seconds.  The compact output of the fourth command is recorded in
`expected_output.txt`.

The new `independent_audit.py` does not import submitted Python modules and
uses only the standard library.  It:

- reads the hash-bound integer-basis coordinates rather than parsing the
  submitted algebraic expressions;
- implements `K` multiplication, Galois-conjugate inversion, exact recursive
  sign decisions, and projective normalization independently;
- rebuilds all line classes and a canonical non-`K` line-key digest;
- rebuilds the complete strict Parts graph and checks its edge digest;
- checks all 55 packed colourings edge by edge over their 6,857 assignments;
- checks `J(L)=L` directly and reports its 14 fixed `L` points.

It reports 37,861 admissible cross pairs, 576 tangent cross pairs, 156,669
colouring-edge checks, and
`nonk_line_key_sha256=177f4d60807054ad5216dd19ae1467cf8fd4040a5995b11811975fbaa55865bf`.

## Trust boundary

The positive non-`K` cases do not trust a SAT solver: stored colourings are
checked directly.  The new checker trusts Python's exact integers and
`Fraction`, the hash-bound coordinate/certificate bytes, and the audited
program-to-mathematics interpretation above.

The separation of 2,167 `K` line classes in the new checker deliberately
uses the independently reviewed sibling `K`-rotation event certificate,
rather than duplicating the submitted recursive square-membership routine.
The concurrent generic-number-field audit checks that boundary entry by entry;
this artifact supplies the separate event-enumeration and witness-replay path.
Claims that the 790 `K` events have exactly six non-4-colourable members, and
that those members are 5-critical, inherit that sibling theorem and its
checked DRAT/SAT evidence.  The reflection argument inherits only the finite
exact symmetry `J(L)=L`, which this checker recomputes.  No proof assistant
formalization was used, and the large prior DRAT traces are not duplicated
here.

## Novelty and readiness

Targeted searches found Jaan Parts's source construction and its restricted
rotation/minimization discussion, but no prior publication of this exact
all-real rotation/reflection classification.  It is therefore apparently
new, subject to the limits of that search.  As a computational family-closure
lemma it is reproducible and mathematically well supported; it should not be
presented as a new record graph or as closure of the broader unit-distance
search.

## Strengthening and improvement opportunities

- State and prove the reusable abstract lemma: for finite coordinate sets
  over a real field `K`, a non-`K` circle point meets at most one
  nonproportional `K`-defined cross-edge line.  This would separate the
  continuum reduction from all Parts-specific enumeration.
- Add a compact independently checkable square/nonsquare certificate for
  every line discriminant.  The present evidence is strong, but the primary
  and submitted independent verifier share the same conceptual quadratic-
  tower criterion, while this review instead imports the already reviewed
  `K`-event census.
- Preserve or regenerate durable proof traces for the six negative
  four-colouring claims in the upstream `K` theorem; the all-real layer
  itself contains only positive colouring witnesses.
- Classify or minimize the 55-colouring witness library and explain the
  large usage range (1 to 3,191).  This is not needed for validity but could
  expose a simpler structural colouring argument.
- Audit the strict graph on the simultaneous union of rotation and reflection
  exceptional copies separately.  Individual reflection placements reduce
  to rotations, but that does not by itself identify the mixed union of all
  determinant signs.

## Files

- `independent_audit.py` — standard-library exact reconstruction and replay.
- `expected_output.txt` — compact deterministic expected output.
- `SHA256SUMS` — byte hashes for the checker and expected output.
- `.gitignore` — excludes Python bytecode caches.

## Source

Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
unit-distance graphs in the plane*, Geombinatorics 29(4) (2020), 137--166,
<https://arxiv.org/abs/2010.12665>.
