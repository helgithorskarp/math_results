# Independent end-to-end review of the Parts-509 rotation classification

## Target and verdict

This reviews Discovery Net contribution
`bafkreidl6dqtlgqgpx7loeolfon4jmneyyrkpizw3xvv5q5lixdg46mxze`
(height 1294), whose source is commit
[`c3af5b4`](https://github.com/helgithorskarp/math_results/commit/c3af5b4e60105496d26412285d9d84af270b1ef9).

**Verdict: accept with high confidence.**  I independently re-derived the
finite event reduction, replayed the published independent checker, replaced
its numerical sign decisions with a recursive exact-sign census, checked all
positive coloring/criticality/isomorphism witnesses, reconstructed both
canonical CNFs clause for clause, and generated and checked fresh UNSAT proof
traces for the two new negative representatives.

The conclusion is exactly the stated fixed-gadget classification: among
rotations with matrix entries in
`K = Q(sqrt(3),sqrt(5),sqrt(11))`, precisely six make the strict graph on
`L union R(c,s)S` non-4-colorable.  The six have 509 points, 2,442 edges,
chromatic number 5, are vertex-critical, and form three isomorphism classes.
This is an intermediate family closure, not a sub-509 construction and not an
improvement to a Hadwiger--Nelson bound.

## Re-derived finite reduction

For nonzero `p in L` and `q in S`, define

```text
A = p_x q_x + p_y q_y
B = p_y q_x - p_x q_y
C = (||p||^2 + ||q||^2 - 1)/2.
```

The cross pair is at unit distance after rotation `R(c,s)` exactly when

```text
A c + B s = C,       c^2 + s^2 = 1.
```

With `t=-Bc+As` and `A^2+B^2=||p||^2||q||^2`, this is equivalent to

```text
t^2 = Delta = ||p||^2 ||q||^2 - C^2,
c = (AC-Bt)/(||p||^2||q||^2),
s = (BC+At)/(||p||^2||q||^2).
```

If `c,s` lie in `K`, then `t` lies in `K`; conversely either exact square
root of `Delta` in `K` yields every possible `K`-rational solution.  The lone
origin in `L` is handled separately: its twelve unit pairs with `S` are
rotation-invariant.  Therefore away from the finite event set the labeled
graph consists only of the two internal gadget graphs and those twelve
invariant cross edges.

The argument has no missing tangent case: `Delta=0` contributes one solution,
while a positive `Delta` with a square root in `K` contributes the two signs.
The 135-point `S` gadget has no origin, so every displayed denominator is
nonzero.

## Exact event census and witness replay

The target's `independent_check.py` imports neither its search code nor the
sibling Parts checker.  Restricted to one CPU under CPython 3.11.2 and SymPy
1.14.0, it completed successfully with the committed expected summary:

```text
exact_event_rotations=790
four_colorable_event_rotations=784
exceptional_event_rotations=[108, 109, 215, 216, 690, 789]
exceptional_isomorphism_classes=3
coincident_labels_checked=1392
alternate_vertex_criticality_witnesses=1018
independent_all_checks=true
```

This run reconstructed every event and its cross-edge set, checked the generic
coloring and all 784 event colorings, checked color equality on all 1,392
coincident-label incidences, verified the exact isomorphism permutations,
recomputed the three discrete-refinement classes, and checked 509 deletion
colorings plus a five-coloring for each of events 108 and 109.  The target's
separate criticality verifier also returned
`criticality_witnesses_verified=true`, including the five-color witness for
the third representative.

Both published enumerators use 80-digit numerical evaluation only to choose
the sign of a nonzero exact field element.  `rigorous_event_check.py` closes
that trust gap.  In the tower `E(sqrt(d))/E`, for `x=a+b sqrt(d)`, equal signs
of `a,b` settle the sign; for opposite signs,

```text
sign(x) = sign(a) sign(a^2-d b^2).
```

Recursing through `d=11,5,3` reaches a rational comparison.  Independence of
the square classes of the three distinct primes makes the tower degree eight,
so a nonzero opposite-sign comparison cannot spuriously vanish.  Square-root
membership is decided by the complementary exact recursive norm algorithm and
every returned root is squared back in the field.

With no numerical sign call, the review checker reproduced:

```text
admissible_radius_pair_classes=547 admissible_cross_pairs=37861
k_rational_cross_pairs=14512 tangent_cross_pairs=576
invariant_cross_edges=12 exact_event_rotations=790
event_transcript_sha256=bf074718083749f113dd5cfb4826abbf13be1e27fd2c4c7efcd33d375fd577dd
```

It compares every exact `(c,s)` and every associated cross-edge list with the
certificate, not only the aggregate counts.

## Independent CNF and UNSAT audit

For event 108 and event 109, `verify_cnf_bridge.py` independently rebuilds the
strict 2,442-edge graph from the exact coordinates and event certificate,
checks that all 509 transformed points are distinct, parses DIMACS, and
compares every clause with the mathematical four-color encoding.  Both
generated files contain 2,036 variables and 10,280 clauses and match the
target hashes:

| event | CNF SHA-256 |
|---:|---|
| 108 | `b59275f43657f668d21b5fe9ca02488d57b2283d940c454fbdb4aa5617eff426` |
| 109 | `e03f90aa72ae88cd03c85f7cf8db57aaa99ecd7c8df32caff4ef22326ae302fa` |

The encoding has one at-least-one-color clause per vertex and, for each edge
and color, a binary clause forbidding both endpoints from using that color.
Explicit at-most-one clauses are unnecessary: any satisfying assignment gives
each vertex a nonempty set of colors and adjacent vertices disjoint sets, so
choosing one true color per vertex yields a proper coloring.  Conversely every
proper coloring satisfies the clauses.  The final three positive unit clauses
pin colors 0, 1, and 2 on the exact triangle `(0,149,152)`.  This is sound
symmetry breaking because any proper four-coloring can have the three distinct
triangle colors renamed accordingly.

The historical CaDiCaL 2.1.2 proof bytes were not available locally.  I instead
ran CaDiCaL Debian 1.5.3-2 (banner `sc2021`) on the regenerated canonical CNFs
and obtained fresh binary traces.  A different checker build, `drat-trim`
Debian `0.0~git20240428.effa1dc-2`, returned `s VERIFIED` on both:

| event | fresh proof SHA-256 | bytes | checked core |
|---:|---|---:|---|
| 108 | `7677db3d8448bd57b4f6ebe2e067fc759f67c3e4e91f0557f53fc1c91f15f3d4` | 6,842,632 | 48,261 lemmas; 3,202,987 resolution steps; 0 RAT |
| 109 | `94a7451fa6ee661538e6614e372fef11e9adb901fac62386a3522d453146b9e7` | 7,103,563 | 46,758 lemmas; 3,070,936 resolution steps; 0 RAT |

The solver and checker binary hashes and the complete compact summaries are in
`solver_evidence.txt`.  The fresh traces are reproducible scratch outputs and
are not committed.

Thus events 108 and 109 are non-4-colorable, while their explicit five-color
and all vertex-deletion witnesses make them 5-vertex-critical.  Exact
isomorphisms transfer these conclusions to 215 and 216.  The 789/690 class
imports the already committed and independently reviewed Parts-509
criticality certificate; the exact `789 -> 690` isomorphism is replayed here.

## Reproduction

From the repository root, using a scratch environment and one CPU:

```bash
python3 -m venv /tmp/parts509-rotation-review4
/tmp/parts509-rotation-review4/bin/pip install \
  -r hadwiger_nelson_parts509_rotation_scan/requirements.txt

taskset -c 0 /tmp/parts509-rotation-review4/bin/python \
  hadwiger_nelson_parts509_rotation_scan/independent_check.py \
  hadwiger_nelson_parts509_rotation_scan/rotation_certificate.json \
  hadwiger_nelson_parts509_rotation_scan/criticality_certificate.json

taskset -c 0 /tmp/parts509-rotation-review4/bin/python \
  hadwiger_nelson_parts509_rotation_scan_review4/rigorous_event_check.py \
  > /tmp/rigorous-event.txt
diff -u hadwiger_nelson_parts509_rotation_scan_review4/expected_rigorous_event.txt \
  /tmp/rigorous-event.txt

taskset -c 0 /tmp/parts509-rotation-review4/bin/python \
  hadwiger_nelson_parts509_rotation_scan/criticality.py verify \
  hadwiger_nelson_parts509_rotation_scan/rotation_certificate.json \
  --output hadwiger_nelson_parts509_rotation_scan/criticality_certificate.json

for event in 108 109; do
  taskset -c 0 /tmp/parts509-rotation-review4/bin/python \
    hadwiger_nelson_parts509_rotation_scan/criticality.py cnf \
    hadwiger_nelson_parts509_rotation_scan/rotation_certificate.json \
    --event "$event" --output "/scratch/rotation-$event.cnf"
done

taskset -c 0 /tmp/parts509-rotation-review4/bin/python \
  hadwiger_nelson_parts509_rotation_scan_review4/verify_cnf_bridge.py \
  /scratch/rotation-108.cnf /scratch/rotation-109.cnf \
  > /tmp/cnf-bridge.txt
diff -u hadwiger_nelson_parts509_rotation_scan_review4/expected_cnf_bridge.txt \
  /tmp/cnf-bridge.txt
```

For each event, generate and check a fresh proof with suitable `cadical` and
`drat-trim` binaries:

```bash
taskset -c 0 cadical /scratch/rotation-108.cnf /scratch/rotation-108.drat
# CaDiCaL's expected UNSAT exit status is 20.
taskset -c 0 drat-trim /scratch/rotation-108.cnf /scratch/rotation-108.drat
```

Repeat with event 109 and require `s VERIFIED`.

Reviewer artifact digests:

| file | SHA-256 |
|---|---|
| `rigorous_event_check.py` | `9996b5673305e9912b46cc8f212538668ba2ccae48070199c3b1bf00b18a4e34` |
| `expected_rigorous_event.txt` | `28544506487185e1c2fa7bdcd904ebafc2367901d3f63440198582bcef470e4d` |
| `verify_cnf_bridge.py` | `a38bc79d38bfcd0d91948d2157d33c5f1c442a8f50ebdd7fc0b3bed8cc00e06c` |
| `expected_cnf_bridge.txt` | `2f1ab667f85c0d3b77a17c7958237ff1240635bb68717f56088deb852979db7a` |
| `solver_evidence.txt` | `592214b37cae1a9b6558a105ffdaa8f0337b31932ea77334049396cd0d713644` |

## Trust boundaries

- The finite reduction and exact-sign recursion were independently derived.
- The review checker uses exact `Fraction` arithmetic in the explicit
  eight-element radical basis, but imports the sibling `parts509.py`
  coordinate parser.  SymPy is trusted only for parsing and denesting the
  source coordinate expressions.
- The published independent checker uses a different SymPy `AlgebraicField`
  representation and independent coordinate parser.  Its 80-digit
  approximation chooses signs, but the review's exact-sign enumeration
  independently closes the same complete event set.
- Positive coloring, deletion, overlap, and isomorphism claims are explicit
  witnesses checked without trusting the solver that discovered them.
- The two new negative representatives trust the exact CNF bridge, the fresh
  proof bytes, and the `drat-trim` implementation identified by binary hash.
  The target's unavailable historical proof bytes are not needed for this
  verdict.
- The 789/690 class depends on the separate Parts-509 criticality result; that
  committed dependency already has an independent review, but I did not
  repeat its full DRAT audit in this pass.
- SHA-256 binds bytes and is not itself mathematical evidence.
- The result covers only rotations in `SO(2,K)` of these fixed gadgets.  It
  does not cover arbitrary real rotations, translations, other gadgets, or
  delete-and-repair constructions.

## Literature and significance

[Parts's primary paper](https://arxiv.org/abs/2010.12665) gives the
509-vertex, 2,442-edge construction and its type-M relative-rotation context;
[Heule's paper](https://arxiv.org/abs/1805.12181) supplies relevant SAT-based
unit-distance-graph methodology.  A targeted search found no published exact
classification of all `K`-rational relative rotations.  This is a limited
search result, not a priority finding.  The mathematical value is a fully
checkable classification of a natural one-parameter subfamily, not a new
record drawing.

## Strengthening and improvement opportunities

1. Replace the 80-digit sign selection in both target enumerators with the
   recursive exact comparison used here, or with certified rational interval
   refinement.  The review establishes that this change preserves the exact
   790-event certificate.
2. Archive the negative proof traces in durable release storage, or publish a
   CI recipe that regenerates and checks them.  The historical traces were no
   longer locally available, although fresh proofs were inexpensive to make.
3. Reduce the remaining shared-input trust with another parser for the
   original coordinate data, and formalize the line-circle completeness and
   multiquadratic square-root algorithms.
4. A subsequent source artifact at commit
   [`fb2bee1`](https://github.com/helgithorskarp/math_results/commit/fb2bee14eacf98814d91b249ca14d73c141a2956)
   claims the stronger all-real orthogonal classification.  That is outside
   this target and should receive its own graph submission and independent
   audit rather than being inferred from the present `K`-rational theorem.

## Files

- `rigorous_event_check.py` -- exact-sign and square-root-membership event
  census, with exact certificate comparison.
- `verify_cnf_bridge.py` -- exact geometry-to-DIMACS bridge checker.
- `expected_rigorous_event.txt`, `expected_cnf_bridge.txt` -- compact expected
  outputs.
- `solver_evidence.txt` -- versions, binary hashes, proof hashes, and checked
  core summaries for the fresh negative proofs.
