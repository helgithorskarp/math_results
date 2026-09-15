# Independent review of the Pegg12 reflection completion

**Verdict: accepted with the fixed-completion scope stated by the target.**

The exact Pegg UD12-2 realization has 12 distinct points, 21 complete unit
edges, and chromatic number four. Reflecting it in the line through source
vertices `(0,6)` produces a 22-point, 50-edge complete plane unit-distance
graph with exactly two shared points and eight genuinely non-inherited unit
contacts. Of the source's 756 proper four-colourings modulo global colour
permutation, exactly 136 do not extend and 620 do.

The declared union of 18 reflected copies has 165 collision-merged points and
597 complete unit edges. The published 165-character word is proper, while
the embedded source rules out three colours, so its chromatic number is
exactly four. This validly closes that fixed completion as a non-record route.
It is not a five-chromatic graph or an improvement of the 509-vertex record.

## Stronger selector audit

The review checks all `binom(12,2)=66` source-pair reflection axes, rather than
only replaying the selected 18. The listed axes are exactly the axes having
both a genuine private unit contact and strict source-colouring loss:

- 12 axes have eight private contacts and block 136 inputs;
- 6 axes have four private contacts and block 136 inputs.

Six additional axes block 136 inputs only through extra point collisions:
they give 18-point unions with six collision classes and no private edge.
They correctly fall outside the target's genuine-private-contact selection
criterion. No other source-pair axis blocks a source input. Thus the selected
18-axis pool is exhaustive for its stated criterion, although the target does
not classify axes outside the 66 source-pair axes, other realizations, or later
compositions.

## Independent method

`verify.py` imports no target code. Its field representation is indexed by the
actual radicands `1,3,11,33`; multiplication is derived from square-free gcds
and inversion from the four Galois conjugates. Reflection is computed as
twice the projection onto the axis minus the original offset, not through the
target's reflection matrix.

The source-colouring census uses restricted-growth words in vertex-label
order. Every canonical source colouring is expanded to all 24 colour-name
permutations, giving 18,144 labelled colourings. For each reflected union,
large integer bitsets impose every exact overlap equality and cross-edge
inequality. This exhausts the extension relation without using the target's
DSATUR search. The selected 18-axis relation hash nevertheless matches the
target exactly.

For the `(0,6)` union the review independently finds all eight private edges,
the three edges individually critical for the displayed blocked input, and
vertex connectivity three. There are exactly six three-vertex cuts; the
target's `(2,8,11)` is the first. For the full union it additionally determines
the 27 collision-class size distribution: 12 classes of size 2, six of size
3, six of size 5, and three of size 6.

## Reproduction

CPython 3.11 or later and only the standard library are required:

```bash
cd hadwiger_nelson_pegg12_reflection_completion_review1
sha256sum -c SHA256SUMS
python3 -B verify.py
python3 -O -B verify.py
python3 -B controls.py
```

The verifier prints `EXPECTED.json`; the controls print `VALIDATION.json`.
Controls check 792 reflection involutions, 4,356 exact distance-preservation
identities, 72,576 entry-level relation decisions against direct enumeration,
four independent field inverses, and three malformed colour words.

Public source:
<https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_pegg12_reflection_completion_review1>.
The verified mathematical commit is recorded after the initial local commit.

## Scope and trust boundary

The result concerns the displayed exact Pegg12 realization, the 66 axes
through pairs of its source points, the `(0,6)` interaction, and the fixed
union of the 18 selected reflections. It says nothing about other realizations
of the abstract graph, axes not through source pairs, additional copies,
receivers, or arbitrary continuations.

Trust remains in the pinned target bytes, CPython exact `Fraction`, integer,
JSON and SHA-256 operations, the finite loops, the field-basis interpretation,
and the written colouring-enumeration argument. The four-colour upper bound
uses a literal positive certificate. The three-colour lower bound is the
complete restricted-growth enumeration on the 12-point source. No SAT solver,
floating-point predicate, or proof assistant is used in the mathematical
verification.
