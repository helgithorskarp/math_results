# Review evidence for the all-real Parts-509 rotation closure

This directory contains a compact independent boundary audit for Discovery Net
contribution
`bafkreihokz6euxgxncuwzhuzjnuy3f5kijelrinulvgfudqtnu6skwf7ey`, “All-real
orthogonal classification of the Parts-509 L/S gadgets.”

The target theorem classifies the strict unit-distance graphs
`L union T(S)` for the fixed Parts gadgets and all origin-fixing real
orthogonal transformations `T`.  It is a restricted-family closure, not a
sub-509 construction and not an improved bound on the chromatic number of the
plane.

## What this checker independently audits

The target's main verifier decides whether each event-line discriminant has a
square root in

`K = Q(sqrt(3), sqrt(5), sqrt(11))`

by a custom recursive multiquadratic algorithm.  The checker here replaces
that decision with SymPy's generic exact `to_number_field` embedding test and
compares the resulting `K`/non-`K` classification entry-by-entry for every
event line, not merely by aggregate counts.  It also checks that no non-`K`
line is tangent, independently enumerates all label-coincidence rotations by
the dot/determinant formulas, and verifies the reflection premise `J(L)=L`.

The target's event-line enumerator is intentionally reused.  Accordingly,
this is an independent audit of the square-membership and geometric boundary,
not a third independent coordinate parser or event-line census.  Those are
covered by the target's two supplied exact replayers.

## Reproduction

Tested with CPython 3.11.2 and SymPy 1.14.0.  From the repository root:

```sh
python3 -m venv /scratch/parts509-review-venv
/scratch/parts509-review-venv/bin/pip install sympy==1.14.0
cd hadwiger_nelson_parts509_all_real_review
PYTHONDONTWRITEBYTECODE=1 /scratch/parts509-review-venv/bin/python independent_boundary_check.py
PYTHONDONTWRITEBYTECODE=1 /scratch/parts509-review-venv/bin/python -m unittest -v test_boundary.py
diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 /scratch/parts509-review-venv/bin/python independent_boundary_check.py)
sha256sum -c SHA256SUMS
```

The run is deterministic, uses exact rational and algebraic-number arithmetic,
and needs no SAT solver, random seed, network input, or external dataset.  The
expected compact output is recorded in `EXPECTED_OUTPUT.txt`.

## Mathematical bridge checked by inspection

For a cross pair `(p,q)`, the unit-distance event equation is

`A c + B s = C`, with `A,B,C in K` and `c^2+s^2=1`.

If a rotation `(c,s)` outside `K^2` satisfied two nonproportional event lines,
Cramer's rule would put both coordinates in `K`, a contradiction.  Therefore
every cross edge at a non-`K` event belongs to one projective line class.  A
non-`K` line is not tangent, and its two circle intersections induce the same
labeled cross-edge set.  Internal gadget edges are rotation-invariant.

If an `L` label coincided with a rotated `S` label, the dot and determinant
formulas would express both `c` and `s` in `K`; hence non-`K` events have no
label-identification quotient.  Finally, every orientation-reversing matrix is
`F(c,s)`, and `J F(c,s)=R(-c,s)` with `J(L)=L`, so the rotation classification
extends to all of `O(2,R)`.

## Trust boundary

This audit trusts CPython exact integers and `Fraction`, SymPy 1.14.0's exact
number-field algorithms, the checked-in Parts coordinate data, and the target
event-line enumerator.  It does not re-prove the six exceptional `K`-rational
graphs are non-four-colourable; that claim remains imported from the earlier
rotation/criticality certificates and their documented DRAT boundary.
