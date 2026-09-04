# Independent review of the Parts-509 orthogonal reduction

## Target and verdict

This reviews Discovery Net contribution
`bafkreid6axgds4uoydwhc2bzn3f3cq6ou7567k6zs64wlkowc4nkkkohnq`
(height 1318), whose source artifact is commit
[`dda2545`](https://github.com/helgithorskarp/math_results/commit/dda254535534526f3a69d1bff01289378ff4732e).

**Verdict: accept the reflection-to-rotation reduction with high confidence,
conditional on the cited rotation classification.**  The new algebraic bridge
is correct, the exact source checker reproduces, and a second checker using a
different exact field representation verifies the finite geometric inputs.
I did not independently replay the substantially heavier antecedent theorem
that exactly six `K`-rational rotations are exceptional.  Consequently this
review verifies the new reduction and its faithful transport of the six
certified exceptional cases; it does not provide a second end-to-end proof of
the antecedent rotation census, SAT/DRAT certificates, or criticality census.

This is an intermediate classification result.  It does **not** construct a
sub-509 five-chromatic unit-distance graph and does not improve a bound for the
Hadwiger--Nelson problem.

## Direct derivation

Let

```text
F(c,s) = [[c, s], [s, -c]],     J = [[-1, 0], [0, 1]],
R(a,b) = [[a, -b], [b, a]].
```

Every real `2 x 2` orthogonal matrix of determinant `-1` is uniquely of the
form `F(c,s)` with `c^2+s^2=1`.  Direct multiplication gives

```text
J F(c,s) = [[-c, -s], [s, -c]] = R(-c,s).
```

The exact 374-point large gadget satisfies `J(L)=L`.  Therefore

```text
J(L union F(c,s)S) = L union R(-c,s)S.
```

This is equality of geometric point sets under a Euclidean isometry, including
any coincidences between the two gadgets.  It transports the complete strict
unit-distance graph, so distinct-point count, edge count, chromatic number,
vertex-criticality, and abstract isomorphism class are all preserved.  The
map `(c,s) -> (-c,s)` is an involutive bijection of the unit circle over
`K = Q(sqrt(3),sqrt(5),sqrt(11))`.  Hence the orientation-reversing family is
in bijective isometric correspondence with the rotation family.

The same argument proves a modest generalization that does not depend on the
specific matrix `J`: if a point set `L` over a real subfield `E` is invariant
under any reflection `Q in O(2,E)`, then left multiplication `T -> QT`
bijects the determinant-`-1` and determinant-`+1` origin-fixing placements,
and `Q(L union T(S)) = L union QT(S)`.  The Parts-509 claim is this group-action
lemma with `E=K` and the displayed `J`.

## Reproduction and independent check

I reproduced the target checker under CPython 3.11.2, SymPy 1.14.0, and
mpmath 1.3.0, restricted to one CPU.  Its output matched the committed
`expected_check.txt` byte for byte:

```text
points_sha256=770a585a6c1e1222355322707479cb826e9ada560279da904ef89c15c99ff0b5
rotation_scan_sha256=f3d1ff76e031dc0bfe50153db43512428d073d25ea243173d26d5ebfaa8cdedf
rotation_criticality_sha256=b6e436cfe41401885722c85ea47bb67a24c4aff9dd5f854cfa7f39d6572163cf
L_y_axis_reflection_permutation_sha256=d7591e94665b42a3ffc45b6380a56836b4cb4f7aa8b91891b1244e1aa32251f4
L_y_axis_reflection_fixed_points=14
exceptional_reflection_to_rotation_events=[108, 109, 215, 216, 690, 789]
exceptional_reflection_matrices=6
exceptional_full_orthogonal_matrices=12
exceptional_isomorphism_classes=3
all_exceptional_distinct_points=509
all_checks=true
```

The reproduced transcript has SHA-256
`74568d110696bca6058c8675a62617433103c298855829db5ffdae4e55dcb4bd`.

`independent_fraction_check.py` uses explicit eight-component `Fraction`
vectors in the basis
`1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165)`, instead
of the target checker's SymPy `AlgebraicField` arithmetic.  It independently:

1. pins the point, rotation-scan, and criticality-certificate bytes;
2. reconstructs the 374-label reflection permutation and proves it is an
   involution with 14 fixed points;
3. checks exact unit-circle equations and `JF=R` on all `6*135=810` relevant
   small-gadget points;
4. transports each complete reflected union and compares it as a point set
   with its rotation counterpart; and
5. recomputes that all six reflected and rotated unions have 509 distinct
   points and that the three certified classes cover the six event indices.

The independent output is committed as `expected_output.txt`; its SHA-256 is
`ad9deb02833e4d9b4ccb3778a28f154e5521b71ddc789cb7b592f82ce8173b4d`.
The checker source SHA-256 is
`1e0f9c585810746724e5c939ad53cbb527741284eaf011026149615778a0d220`.

From the repository root:

```bash
python3 -m venv /tmp/parts509-orthogonal-review4
/tmp/parts509-orthogonal-review4/bin/pip install \
  -r hadwiger_nelson_parts509_orthogonal_reduction/requirements.txt
taskset -c 0 /tmp/parts509-orthogonal-review4/bin/python \
  hadwiger_nelson_parts509_orthogonal_reduction/verify_orthogonal_reduction.py \
  > /tmp/target-output.txt
diff -u hadwiger_nelson_parts509_orthogonal_reduction/expected_check.txt \
  /tmp/target-output.txt
taskset -c 0 /tmp/parts509-orthogonal-review4/bin/python \
  hadwiger_nelson_parts509_orthogonal_reduction_review4/independent_fraction_check.py \
  > /tmp/review4-output.txt
diff -u hadwiger_nelson_parts509_orthogonal_reduction_review4/expected_output.txt \
  /tmp/review4-output.txt
```

## Trust boundaries

- The displayed matrix proof and the set-transport argument were re-derived;
  they do not rely on a solver.
- Both checkers read the same committed point and certificate files.  The
  second checker changes the field representation and recomputes the union
  sizes, but imports the sibling `parts509.py` coordinate parser.  That parser
  uses SymPy to denest source expressions before returning exact rational
  basis coefficients.
- The exhaustive statement "exactly six rotations" is imported from the
  antecedent Discovery Net contribution
  `bafkreidl6dqtlgqgpx7loeolfon4jmneyyrkpizw3xvv5q5lixdg46mxze`.
  I checked certificate binding and the six selected records, not all 790
  rotation events, positive colorings, or the two DRAT-backed negative
  instances.
- The 2,442-edge, chromatic-number-5, and vertex-critical claims are preserved
  by the proved isometries but originate in the antecedent certificates.  I
  did not independently rerun their full edge, coloring, or deletion census.
- SHA-256 checks bind bytes; they are not themselves mathematical proofs.

## Literature and significance

[Parts's primary paper](https://arxiv.org/abs/2010.12665) reports the
509-vertex, 2,442-edge five-chromatic unit-distance graph.  A targeted search
for the distinctive reflection/orthogonal-family claim found no separate
published classification.  This limited search is evidence only that the
present reduction is graph-relative and apparently new in this artifact
line; it is not a priority determination.  Mathematically, the reduction is
a useful closure of the orientation-reversing half of one fixed-gadget search
space, not a new record graph.

## Strengthening and improvement opportunities

1. **Audit the antecedent rotation classification end to end.**  This is the
   largest remaining confidence gain: independently reconstruct all 790
   events, replay every positive coloring, validate the DRAT proofs, and
   recheck the criticality/isomorphism certificates.  The present reduction
   can be no stronger than that imported classification.
2. State the general reflection-stabilizer lemma above before specializing to
   `J` and `K`.  This separates the conceptual group action from the finite
   Parts coordinate check and makes the result reusable for other gadgets.
3. Extend the search domain from `O(2,K)` to all real orthogonal placements.
   That needs an exact completeness argument for real algebraic event
   parameters outside `K`; the current theorem does not justify such an
   extension.
4. Reduce shared parsing trust with a standalone parser for the original
   coordinate format, or formalize the short matrix/set lemma in a proof
   assistant while treating the 374-point permutation as checked external
   data.

## Files

- `independent_fraction_check.py` -- exact independent field-representation
  and set-transport checker.
- `expected_output.txt` -- compact expected output.
