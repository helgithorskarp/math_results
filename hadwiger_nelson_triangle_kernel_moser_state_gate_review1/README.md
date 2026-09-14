# Independent review: three-contact Moser state gate

Verdict: **accept with high confidence at the stated restricted scope**.

This review covers the theorem and evidence in
[`hadwiger_nelson_triangle_kernel_moser_state_gate`](../hadwiger_nelson_triangle_kernel_moser_state_gate/README.md)
at source commit `b9394bdeca548f1866b39278e9d10da6c1a5b3fc`, together
with the triangle exterior-kernel dependency at commit
`d1ef2c978a6659a4f0ab1ef748be88e57486a4cb`.

## Accepted statement

Let `D={0,1,omega}` be a unit equilateral triangle, let `X` be `D` and
the three complete unit circles centred at its vertices, and let `P` be the
standard 12-point patch in `X`. Let `W` be a congruent copy of the seven-point
Moser spindle. Assume:

1. every point of `W` is outside `X`;
2. there is no unit edge between `W` and `P`; and
3. every generic 18-point component `Q(u)=K3 square C6` of `X-D` has at
   most three unit-edge incidences with `W`.

Then the **complete strict unit-distance graph** on the uncountable point set
`X union W` is four-colourable. The finite kernel needed to test the possible
three-contact obstructions has at most 271 vertices.

This is a genuine exact restricted-family exclusion. It is not a
five-chromatic construction and does not improve the unrestricted published
record of 509 vertices and 2442 edges. (Qualifying placements can trivially
be put far from `X`; their existence is not the issue.) The newer 2131-vertex
result is smaller only in the Moser-spindle-free subclass, not in the
unrestricted problem. See
[Parts (2020)](https://arxiv.org/abs/2010.12665) and
[Haugland (2026)](https://arxiv.org/abs/2608.04542).

## Independent finite reconstruction

[`independent_check.py`](independent_check.py) imports no module from either
reviewed package. It hash-pins the reviewed files and works in a nested
`Q(sqrt(3),sqrt(11))` field representation different from the source
producer's XOR basis and its verifier's sparse-radicand implementation.

The clean-room computation establishes all of the following from coordinates
or graph definitions:

- `P` has 12 distinct points and all 24 geometric unit edges, and exactly one
  three-colouring after the centres are pinned to colours `0,1,2`.
- The standard Moser realization has 7 distinct points and all 11 geometric
  unit edges. It has no three-colouring and exactly 384 four-colourings.
- Its three-point subsets of circumradius one are exactly
  `013, 023, 046, 056, 124, 125, 126, 145, 245, 345`.
- The abstract generic shell `K3 square C6`, including the forbidden owner
  colour at each shell vertex, has 11 possible column states, 44 compatible
  ordered state transitions, and exactly 5,576 complete four-colourings.
- All 2,701 multisets of at most two forbidden-colour incidences extend.
  Among all 64,824 size-three multisets, exactly 18 fail: at one shell vertex,
  all three colours other than its owner-centre colour are forbidden.

The shell enumeration is exhaustive; it does not assume that all
four-colourings have one of the two special three-colour patterns used in the
analytic two-incidence extension lemma.

## Direct proof of the state gate

For each owner colour and each of the ten Moser triples above, a blocker type
means that the triple uses all three non-owner colours. Repeated occurrences
of a type can be deduplicated because they exclude the same Moser colourings.

For a fixed Moser vertex `w` and owner centre `d`, a physical blocker chooses
a common point of the two distinct unit circles `C(w)` and `C(d)`. Those
circles have at most two common points. Consequently, among the ten selected
triple types for one owner, every Moser vertex has degree at most two. The
checker enumerates all `2^10` subsets and finds 154 satisfying this capacity.
It then tests all

```text
154^3 = 3,652,264
```

three-owner selections directly against all 384 Moser colourings. No
selection covers every colouring. The strongest selection found blocks 378,
so every capacity-feasible abstract blocker collection leaves at least six
proper Moser colourings. In contrast, all 30 blocker types together do cover
all 384 colourings; the geometric capacity is essential.

This direct subset exhaustion is independent of the submitted SAT proof. As
corroboration, the checker also reconstructs the canonical 30-variable,
522-clause CNF byte for byte and reconstructs the published certificate
entrywise. It verifies all 20 LRAT additions by unit propagation over the
entire live clause database, without using LRAT hints to establish RUP, while
also checking that all 165 listed hint references are live. Removing the
final proof line is rejected.

## From the finite gate to the continuum

The finite UNSAT statement alone does not prove the theorem on `X union W`.
The bridge uses the exterior-kernel decomposition:

- the patch `P` takes its pinned three-colouring;
- a contacted generic component with at most two incidences extends by the
  explicit base-colouring and one-vertex repair lemma;
- a component with three incidences fails only in one of the 18 classified
  single-vertex patterns, and the state gate supplies a Moser colouring for
  which none of the physical blockers occurs; and
- distinct generic components have no mutual edges, so they extend
  independently. Components without contacts use the explicit analytic
  colouring, including the infinitely many uncontacted components.

The continuum decomposition ultimately uses the unit-rhombus identity for
cross-circle edges and the exact six-rotation orbit partition. Its underlying
dominating-triangle theorem already has an independent accepted review in
[`hadwiger_nelson_dominating_triangle_review1`](../hadwiger_nelson_dominating_triangle_review1/README.md).
For this review, the exterior-kernel source and verifier were also replayed,
and the specialized extension argument above was checked line by line.

Finally, each of seven exterior points meets each of three owner circles in at
most two points. There are at most `7*3*2=42` exterior-to-shell incidences and
therefore at most `42/3=14` three-contact components. The kernel bound is

```text
12 + 7 + 14*18 = 271.
```

This is a cap on a finite feasibility kernel, not a 271-vertex chromatic
witness.

## Reproduction

From the repository root, with CPython 3.11 or newer:

```sh
python3 -B hadwiger_nelson_triangle_kernel_moser_state_gate_review1/independent_check.py \
  > /tmp/moser-state-gate-review.json
diff -u \
  hadwiger_nelson_triangle_kernel_moser_state_gate_review1/EXPECTED_OUTPUT.txt \
  /tmp/moser-state-gate-review.json

python3 -OB hadwiger_nelson_triangle_kernel_moser_state_gate_review1/independent_check.py \
  > /tmp/moser-state-gate-review-optimized.json
cmp /tmp/moser-state-gate-review.json \
  /tmp/moser-state-gate-review-optimized.json

(cd hadwiger_nelson_triangle_kernel_moser_state_gate_review1 && \
  sha256sum -c SHA256SUMS)
```

The two modes produced byte-identical output in this environment and took
approximately 1.1 and 1.2 seconds. The source package's build, independent
verifier, optimized verifier, and negative controls all passed; the analogous
parent build and both verifier modes also passed.

## Limitations and trust boundary

The verdict does **not** cover Moser placements with patch contacts,
placements that give four or more incidences to some generic component, or
arbitrary non-Moser seven-point exteriors. It neither constructs nor rules
out a smaller five-chromatic plane unit-distance graph. The CNF is an abstract
obstruction covering calculation, but the accepted theorem concerns an actual plane
realization only after the circle-intersection capacity and continuum
decomposition are supplied.

The exact finite audit trusts CPython integer and `Fraction` semantics,
exhaustive-loop execution, faithful file reads, and SHA-256 collision
resistance. The analytic bridge retains elementary Euclidean facts about
unit chords, circle intersections, and the irrationality and positivity of
the displayed square roots. No floating-point comparison, external solver,
random sampling, or unverified abstract-to-geometric embedding is used.
