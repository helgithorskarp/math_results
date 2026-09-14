# The complete 119-image obstruction for the five-chromatic `G_11`

**No plane unit-distance graph and no improvement on the 509-vertex record is
produced.** This package closes the next global realization layer of

```text
G_11 = Cay(F_11^2, {d : d_1^2 + d_2^2 = 1}).
```

The pinned predecessor proves that `G_11` has 121 vertices, 726 edges and
chromatic number five, but that neither an injective plane unit-edge drawing
nor any drawing with exactly 120 distinct images exists. Here we prove:

> Every edge-preserving map from `G_11` to the Euclidean plane has either at
> least 120 or at most 118 distinct images. In particular, no such map has
> exactly 119 images.

Combined with the pinned exclusions at 121 and 120 images, every
edge-preserving plane map of `G_11` has **at most 118 distinct images**. This
does not assert that such a map exists.

This is an exact, globally coupled collision theorem. It covers every possible
partition of the 121 source vertices into 119 independent fibres, not a sample
of placements or a docking of separately colourable components.

## Complete finite reduction

The collision deficit is two, so the non-singleton fibres have exactly one of
two shapes:

```text
(3,1,...,1)       or       (2,2,1,...,1).
```

Choose a pair in a non-singleton fibre. Translation puts one member at zero.
Since `-1` is not a square modulo 11, a nonzero nonedge difference has norm in
`{2,...,10}`. The 24 matrices in `O(2,11)` are transitive on each norm shell,
giving nine choices for the first pair. In its 120-vertex quotient we then
enumerate either every permitted third member of the same fibre, or every
permitted second nonedge pair of singleton classes.

This gives 57,735 symmetry-normalized events:

| fibre shape | normalized events |
|:--|--:|
| one triple | 864 |
| two pairs | 56,871 |
| **total** | **57,735** |

These are normalized cases, not claimed distinct quotient isomorphism types;
duplication is harmless for completeness. Among them, 12,627 also identify
equal-coloured classes in the predecessor's explicit five-colouring. Those
quotients are abstract graphs of chromatic number exactly five. The remaining
quotients still have chromatic number at least five, but no upper bound is
needed for the geometric exclusion.

## Exact rhombus-rank result

Every simple unit four-cycle in an injective plane drawing is a rhombus. For
cyclic vertices `a,b,c,d`, each Cartesian coordinate therefore satisfies

```text
x_a - x_b + x_c - x_d = 0.
```

The predecessor supplies a checked rank-119 basis on each 120-vertex
one-collision quotient. After the second contraction, its surviving rows have
rank 118 in 56,958 cases. In the remaining 777 cases, the verifier reconstructs
the complete four-cycle set of the final 119-vertex quotient; all 777 also have
rank 118. Those fallbacks check 1,567,802 four-cycle equations in aggregate.

The rank calculation is over `F_2`. A rank-118 minor is odd, hence nonzero over
the reals. Every signed integer rhombus row has coefficient sum zero, so the
real rank is exactly 118 and the kernel consists only of constants. Both plane
coordinate lists would be constant, contradicting a unit edge and injectivity.

An alternate audit reconstructs all 17,346 one-collision four-cycles and takes
a reverse-canonical greedy basis rather than the published one. It requires
844 (rather than 777) complete-cycle fallbacks and independently reaches rank
118 in every event, with the same event-stream SHA-256
`c5ba6eb564c9c6c931ee793c82590a7eb3ac9efd0d0620f87bb94a6414635777`.

## Reproduce

CPython 3.11 or later and the standard library suffice. From the repository
root run:

```sh
python3 hadwiger_nelson_finite_abelian_lifts/verify.py
python3 hadwiger_nelson_g11_one_collision/verify.py --check-expected
python3 hadwiger_nelson_g11_exact119_obstruction/verify.py --check-expected
python3 -O hadwiger_nelson_g11_exact119_obstruction/verify.py --check-expected
python3 hadwiger_nelson_g11_exact119_obstruction/audit.py --check-expected
python3 hadwiger_nelson_g11_exact119_obstruction/controls.py
python3 hadwiger_nelson_g11_exact119_obstruction/produce.py \
  --output /tmp/hn-g11-exact119.json
cmp /tmp/hn-g11-exact119.json \
  hadwiger_nelson_g11_exact119_obstruction/certificate.json
sha256sum -c hadwiger_nelson_g11_exact119_obstruction/SHA256SUMS
```

`produce.py` regenerates the compact certificate. `verify.py` imports no
producer code: it reconstructs the graph and quotient maps, checks all
symmetry shells, validates every inherited basis cycle and five-colouring,
enumerates all normalized contractions, and recomputes every necessary full
cycle census. `audit.py` uses a freshly enumerated alternate basis.
`controls.py` tests malformed data and the binary-rank primitive on exhaustive
small fixtures. No floating point, numerical tolerance, SAT answer, timeout or
random seed enters the theorem.

## Scope and campaign decision

The new calculation rules out only edge-preserving maps of this exact `G_11`
source with exactly 119 images; the at-most-118 corollary also imports the two
predecessor realization theorems. Maps with at most 118 images, edge-deleted
subgraphs and unrelated geometries remain open. The 57,735 count is a complete
normalized coverage count, not a count of isomorphism classes. The Euclidean rhombus
lemma, finite-field symmetry and fibre-partition reduction are written proofs,
not proof-assistant formalizations.

The construction cohort is retired at exact-realization failure. It is a
restricted-family exclusion, not record progress and not evidence that an
arbitrary 119-vertex plane unit-distance graph is four-colourable. Parts's
[509-vertex graph](https://arxiv.org/abs/2010.12665) remains the published
record; Haugland's [August 2026 paper](https://arxiv.org/html/2608.04542v4)
still describes it as current. No priority claim is made beyond the searched
project, committed graph and source context.

See [PROOF.md](PROOF.md) for the coverage and rank arguments. The predecessor
packages are [the finite abelian theorem](../hadwiger_nelson_finite_abelian_lifts/README.md)
and [the complete one-collision theorem](../hadwiger_nelson_g11_one_collision/README.md).
