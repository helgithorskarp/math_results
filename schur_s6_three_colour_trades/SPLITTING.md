# At least four original colour classes must split

Let `F` be any of the four explicit assignments in `fixtures.json`: the
Fredricksen--Sweet colouring of `[1,536]`, the external two-defect assignment
on `[1,537]`, or Sol's one-defect assignments 190 and 359 on `[1,537]`.
Write `A_i={x:F(x)=i}` for its six old classes.

**Theorem.** In every valid classical six-colouring `C` of `[1,537]`, at
least four of the old sets `A_i` contain vertices of at least two different
`C`-colours. Equivalently, at most two old classes remain monochromatic.
Repeated summands are included. No old colour labels are prescribed in
this statement: a class that remains monochromatic may initially have
any new label.

This strengthens the earlier [three-colour trade obstruction](PROOF.md).
It rules out every repair that keeps any three old classes intact, even
when vertices from other classes may be added to those intact classes.
The result concerns four specified inputs, not all 536-colourings. It is
neither a new lower bound nor an unrestricted upper bound for `S(6)`.

## 1. No two old classes can merge

For each pair `i<j`, the certificate supplies an integer Schur triple
whose old colours are exactly `{i,j}`. If `A_i` and `A_j` were both
monochromatic in the same new colour, that triple would become
monochromatic. Thus monochromatic old classes must receive distinct new
labels. The checker directly validates all 15 pair witnesses for each
of the four assignments: 60 small triples in total.

If three old classes remain monochromatic, their three new labels are
therefore distinct. Extend the bijection from those new labels to their
old labels to a permutation of all six labels, and apply it to `C`.
This preserves sum-freeness and fixes every old member of those three
classes pointwise. It is enough to rule out this latter situation.

## 2. Blocking every colour of a fixed class

Let `A` be an old class whose vertices keep colour `d`. For a vertex `v`
outside `A`, colour `d` is forbidden if any of these holds:

1. `v=a+b` for some `a,b in A`, allowing `a=b`;
2. `a+v=b` for some `a,b in A`;
3. `v+v=a` for some `a in A`.

Each condition exhibits a monochromatic triple if `v` receives `d`.
These are also all the ways adding a single vertex can destroy sum-freeness.
Hence, for a sum-free `A`, its individually admissible insertions are

    [1,537] minus (A union (A+A) union positive(A-A)
                       union {a/2 : a in A and a is even}).

Individual admissibility does not imply that several insertions are
jointly compatible. No such implication is used.

The discovery program uses the displayed sum/difference/halving formula.
The verifier instead enumerates all integer triples `x<=y`, `x+y=z<=537`.
For each target among the triple's distinct vertices, it records colour `d`
as forbidden when every other distinct vertex has old colour `d`.
If that class is fixed, all those premises remain true. Distinct vertices
are essential: `v+v=a` has just one other vertex, not two independent ones.

## 3. Fifty forced three-colour kernels

Fix three old classes and let `T` be the complementary palette of three
free labels. Let `U_T` be the union of the old classes in `T`, together
with 537 in the baseline extension case. Define `K_T` to be the vertices
of `U_T` blocked from **each** of the three fixed colours.

Every vertex of `K_T` must use a colour in `T` in any hypothetical repair,
even though vertices outside `K_T` may enter the fixed classes. For every
required palette, the certificate supplies a subset `W_T` of `K_T` that
is not three-colourable into sum-free sets. Restricting a valid `C` to
`W_T` would contradict this fact.

There are 20 palettes for the valid baseline. Each near-colouring has
exactly one defective old class. That class cannot remain monochromatic
under any new label, because it already contains an integer Schur triple.
It must therefore be among the three free classes, leaving ten palettes
per near-colouring. All other choices of three fixed classes are already
excluded by that internal old violation.

| Input | Required kernels | Witness sizes | Exhaustive search nodes |
| --- | ---: | ---: | ---: |
| `baseline` | 20 | 33–80 | 720,107 |
| `near537` | 10 | 14–48 | 19,966 |
| `team_near_190` | 10 | 21–74 | 105,692 |
| `team_near_359` | 10 | 25–96 | 138,393 |

The verifier checks 7,047 forbidden-domain incidences, one for each
witness vertex and each of its three frozen colours. It then uses the
existing exact finite-domain enumerator to prove each `W_T` not
three-colourable. The proof of that enumerator is in [PROOF.md](PROOF.md),
Section 4: global root-colour normalization, sound singleton propagation,
and recursion on every remaining colour choice. No search cutoff or SAT
answer enters the successful verification. The 984,158 search nodes
exhaust all branches of all 50 cases.

Together with the distinct-label argument in Section 1, this proves the
theorem. The absence of a cutoff is important: no unfinished search is
accepted as non-colourability.

## Reproduction and provenance

Verification requires Python 3.11 or later and the standard library:

```sh
python3 -B check_splitting.py
python3 -B test_splitting.py
```

Expected output from the checker:

```text
PASS four_class_splitting fixtures=4 pairs=60 kernels=50 nodes=984158 max_vertices=96
class_splitting_sha256=027b1c25df0ed2c21cbf25f653a8abb6e13bbc8dc2e0dfb868bc6da7a4812a81
```

`class_splitting.json` is 14,481 bytes and binds the unchanged fixture file
by SHA-256. Full input attribution remains in [README.md](README.md).
The standard-library run took about 24 seconds and 18 MiB resident memory.
The normal and optimized (`python3 -B -O check_splitting.py`) runs agree.
Three test groups compare blocking with direct sum-freeness for all 151
sum-free subsets of `[1,10]`, explicitly exercise both directions of
doubling and the difference condition, and reject missing pair witnesses,
missing kernel cases, an unblocked witness vertex and a colourable kernel.
The unchanged enumerator's separate controls are in `test_checker.py`.

Optional discovery uses `python-sat==1.9.dev15` through the existing guarded
one-hot producer. For example, inside a suitable virtual environment:

```sh
python3 discover_splitting.py near537 4 5 6 \
  --seed 1 --budget 3000 --output /tmp/schur-splitting-candidate.json
```

Different deletion orders can produce different witnesses. Discovery is
outside the proof's trust boundary. The theorem needs only the finite
data, literal blocking checks, exhaustive enumerator and the elementary
relabeling argument above. It has not been formalized in a proof assistant.
No historical novelty is claimed for the blocking or relabeling principles;
the finite splitting exclusions are the contribution.

## Consequence for constructive searches

The previous attempt allowed all individually admissible insertions into
otherwise fixed classes. The kernels explain why none of the cases with
only three free old classes can succeed. Allowing four old classes to
change leaves two fixed classes. The new theorem then requires **each**
of the four free old classes to split; no free class may merely change
its label as a whole.

`probe_insertions.py` reproduces this bounded constructive test. It builds
an exact domain model, retains all Schur constraints, and accepts a SAT
model only after a direct check of the full colouring. The following uses
the same optional PySAT dependency:

```sh
python3 probe_insertions.py --inputs team_near_190 team_near_359 \
  --size 4 --mode all --seed-phases --force-split --budget 100000 \
  --output /tmp/schur-four-class-probe.json
```

All 20 tested models returned UNKNOWN at that budget, both with and
without the splitting constraints. These are unfinished searches, not
further exclusions. No valid 537-colouring was found. No raw solver log,
large trace or environment is included in the source publication.
