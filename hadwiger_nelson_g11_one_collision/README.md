# The complete one-collision quotient family of the five-chromatic G_11

**No unit-distance graph and no improvement on the 509-vertex benchmark is
produced.** The benchmark is Parts's
[509-vertex construction](https://arxiv.org/abs/2010.12665), still described
as the current record in Haugland's
[August 2026 paper](https://arxiv.org/abs/2608.04542). This package closes a target-bearing repair of an abstract
five-chromatic source. Let

```text
G_11 = Cay(F_11^2, {d : d_1^2+d_2^2=1}).
```

The pinned predecessor package proves that `G_11` has 121 vertices, 726
edges and chromatic number exactly five, but has no injective unit-distance
drawing in the Euclidean plane. A natural repair is to identify one
nonadjacent pair, changing the edge set and lowering the physical order to
120. Every such quotient is still non-four-colourable: a four-colouring
would pull back along the quotient map to a four-colouring of `G_11`.

This package proves that **none of those one-pair quotients has an injective
unit-distance drawing in the plane**. Equivalently, no edge-preserving map of
`G_11` to the plane has exactly 120 distinct images. It also gives and checks
an explicit five-colouring of every quotient, so all nine quotient types have
chromatic number exactly five as abstract graphs.

The nine cases below are the complete symmetry classes. The last column is
the rank over `F_2` of 119 certified four-cycle rows on 120 quotient vertices.

| squared difference norm | representative | edges | all rhombus equations | certified rank |
|---:|:---:|---:|---:|---:|
| 2 | (1,1) | 724 | 1910 | 119 |
| 3 | (0,5) | 724 | 1910 | 119 |
| 4 | (0,2) | 725 | 1927 | 119 |
| 5 | (0,4) | 726 | 1948 | 119 |
| 6 | (1,4) | 726 | 1949 | 119 |
| 7 | (2,5) | 724 | 1910 | 119 |
| 8 | (2,2) | 724 | 1884 | 119 |
| 9 | (0,3) | 726 | 1959 | 119 |
| 10 | (1,3) | 726 | 1949 | 119 |

## Why the rank certificate is conclusive

In an injective plane drawing, a four-cycle whose four edges have length one
is a nondegenerate rhombus. If its cyclic vertices are `a,b,c,d`, then

```text
p_a + p_c - p_b - p_d = 0.
```

Apply these equations separately to the two Cartesian coordinates. Each
integer row has coefficient sum zero, so its characteristic-zero rank is at
most 119. The certificate supplies 119 rows whose reductions modulo two are
independent. A corresponding `119 x 119` integer minor is odd, hence nonzero;
the characteristic-zero rank is therefore at least 119. Its kernel consists
only of constant vectors. Both Cartesian coordinate lists would be constant,
contradicting any unit edge and injectivity.

Translation sends one member of a collision pair to zero. Since `-1` is not
a square modulo 11, `x^2+y^2=0` has only the zero solution. A nonzero
nonedge difference consequently has one of the nine norms 2 through 10.
The verifier enumerates all 24 matrices in `O(2,11)` and checks that each of
these nine 12-point norm shells is one orbit. Thus the certificate covers
every allowed pair, not a sample.

## Reproduce

CPython 3.11 or later and its standard library suffice. Run from the
repository root:

```sh
python3 hadwiger_nelson_finite_abelian_lifts/verify.py
python3 hadwiger_nelson_g11_one_collision/verify.py --check-expected
python3 -O hadwiger_nelson_g11_one_collision/verify.py --check-expected
python3 hadwiger_nelson_g11_one_collision/controls.py
python3 hadwiger_nelson_g11_one_collision/produce.py \
  --output /tmp/hn-g11-one-collision.json
cmp /tmp/hn-g11-one-collision.json \
  hadwiger_nelson_g11_one_collision/certificate.json
sha256sum -c hadwiger_nelson_g11_one_collision/SHA256SUMS
```

The independent verifier reconstructs the 121-vertex source and every
quotient directly, enumerates the orthogonal group and all norm shells,
checks all 726 source edges under each quotient map, enumerates the full
four-cycle equation census, checks every certified cycle, recomputes all
nine binary ranks, and validates every five-colouring. It imports no producer
code and uses no floating-point arithmetic or solver.

`controls.py` rejects seven certificate corruptions and exhausts 689 small
binary-rank fixtures against a definition-level span census. The source
five-colouring and compact four-colour refutation are pinned by SHA-256. The
first reproduction command independently checks that preceding chromatic
certificate, including 539 RUP additions; the present verifier treats its
lower bound as an explicit imported theorem.

## Files and scope

- `PROOF.md` gives the reduction, completeness argument and exact rank lift.
- `certificate.json` stores 1,071 four-cycle basis rows, nine inherited
  five-colourings and the pinned predecessor hashes.
- `produce.py` regenerates the certificate from the graph definition and the
  pinned source colouring.
- `verify.py` is the independent exact checker.
- `controls.py`, `EXPECTED.json`, `VALIDATION.json` and `SHA256SUMS` record
  negative tests and deterministic validation.

The theorem excludes only maps with exactly 120 images, equivalently exactly
one two-vertex fibre. Maps with at most 119 images can have interacting
collisions and are not classified. Arbitrary edge-deleted subgraphs and
quotients that delete edges rather than inherit all quotient edges are also
outside the theorem. The planar rhombus lemma and the finite-field symmetry
argument are written proofs rather than formalized theorems. The broader
search for a five-chromatic unit-distance graph on at most 508 vertices
remains open.

The chromatic premise is the repository's pinned
[finite abelian Cayley lift theorem](../hadwiger_nelson_finite_abelian_lifts/README.md).
The construction was selected because that theorem explicitly left
noninjective homomorphic images open. No priority claim is made beyond the
searched project and graph context.
