# Independent review of the E477 maximum-translation union

**Verdict: accept the scoped result and refine its connected structure.**

For the reviewed 255-point mandatory core C inside E477, an independent exact
implementation exhausts every nonzero translation with positive overlap.
Among 9,046 candidates, the unique maximizing pair is

    (-3,3,3,3), (3,-3,-3,-3),

with 75 overlaps. The two choices are opposites and give translation-congruent
unions. The target's lexicographically selected translation has squared
physical length 1/3.

The selected collision-merged union independently reconstructs as 435
distinct points and all 1,589 unit edges. Of these edges, 1,231 are inherited
from the two 659-edge core copies and 358 are additional cross-copy contacts.
The target's point and edge stream hashes match exactly.

The literal four-colour word is proper, and an embedded seven-point
11-edge Moser spindle has no proper three-colouring. Thus the graph has
chromatic number exactly four and is not a five-chromatic record candidate.

## Structural refinement

The 435-point graph is disconnected: source label 91 in the untranslated
copy is an isolated vertex. It has coefficient row

    (-15,-9,45,-3).

All 1,589 edges lie in the other component. Consequently deleting that
isolated point gives a connected 434-point, 1,589-edge complete plane
unit-distance graph whose chromatic number is still exactly four. This
strengthens the structural description but does not change the target's
negative record conclusion.

The full union has 411 triangles, 15 unit-direction classes up to sign, and
87 duplicate inherited edge images caused by overlap. Every one of the 358
noninherited edges joins a point belonging only to the first copy to a point
belonging only to the second copy.

## Independent method

The review imports no target code. A source row (a,b,c,d) represents

    ((a sqrt(3)+b sqrt(11))/36, (c+d sqrt(33))/36).

For a row difference (a,b,c,d), unit distance is equivalent to the two
integer equations

    3a^2+11b^2+c^2+33d^2 = 1296,
    ab+cd = 0.

This is the primary geometry test, instead of the target verifier's generic
radical multiplication. A generic four-radicand implementation independently
agrees on all 113,526 source pairs and all 94,395 union pairs in the controls.

The overlap maximum is recomputed from literal translated-set intersections,
not the target's difference multiplicity counter. Canonical restricted-growth
colour enumeration replaces the target's enumeration of all named words.

The source audit also reconstructs all 477 E477 points and 2,458 complete
unit edges, checks its proper equal-terminal word, and rechecks all 253
proper deletion words with unequal terminals. Hence the conditional inference
that any equality-forcing E477 subgraph contains this 255-point core is
reproduced. The fact that full E477 actually forces equality is prior reviewed
context and is not needed to prove this union four-chromatic.

## Scope

This result decides one exact maximum-overlap translation of one fixed
255-point core. It does not exclude:

- other translations selected by another objective;
- rotations, reflections, or general isometries;
- adding optional E477 vertices;
- deleting nonisolated vertices or combining more copies; or
- other plane unit-distance constructions.

It is restricted-family evidence, not a global lower bound and not an
improvement on the supported 509-vertex unrestricted record.

## Reproduction

CPython 3.11 or later and only the standard library are required:

    cd hadwiger_nelson_e477_core_translation_union_stop_review1
    sha256sum -c SHA256SUMS
    python3 -B verify.py | diff -u EXPECTED.json -
    python3 -O -B verify.py | diff -u EXPECTED.json -
    python3 -B controls.py | diff -u VALIDATION.json -

The reviewed target is the sibling directory
hadwiger_nelson_e477_core_translation_union_stop at mathematical commit
621db0ad3b4be24ba7c76e1cbd7d57026d5b7669.

Public source:
<https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_e477_core_translation_union_stop_review1>.

The trust boundary is the pinned source bytes, the written biquadratic-field
argument, exact Python integer/set/JSON/SHA-256 operations, exhaustive finite
loops, CPython, and ordinary hardware. No floating-point predicate, SAT
verdict, omitted solver trace, or proof assistant is a premise.
