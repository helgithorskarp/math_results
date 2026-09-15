# Independent review of the EI21 contact and self-sum stop

Verdict: **accept, with a strict one-root and one-operation limitation**.

An independent exact checker confirms both parts of the target theorem:

1. one isolated 21-point Exoo--Ismailescu framework root has exactly the 38
   source edges plus contact `(0,14)`, and its complete strict graph is
   four-chromatic; and
2. its complete commutative self-sum has between **210 and 231 physical
   points** and complete strict unit-distance chromatic number exactly **four**.

This construction is not five-chromatic and does not improve Parts's
509-point record.

## Independent method

The target uses aggregate perturbation formulas.  This review instead builds
an exact rational interval for every source coordinate, evaluates every
Jacobian entry on the whole box, and propagates those intervals through
`I-AJ(X)`.  The contraction norm is below `10^-22`, and the self-map bound is
below `10^-47` inside a radius-`10^-25` box.  Direct interval distances decide
all 210 source pairs and recover exactly 39 strict unit edges.

The 38 source edges are independently reconstructed from the pinned Shibuya
`ei21_vertices` operation sequence.  A fixed-label search replaces the
target's DSATUR and proves the source and contact graph non-three-colourable.
A fresh complete four-colour word is also found.

For the 231 canonical sum addresses, direct endpoint interval arithmetic
checks all 26,565 address pairs and reproduces:

```text
possible collision classes          210
possible-unit supergraph edges       731
supergraph SHA-256                   f1f4aaa4c263c7292925c5d00dac943945a2550c0b2c5195ead02a9b286d0442
proper target four-colouring          yes
```

The possible-class sizes are 195 singletons, ten pairs, four triples, and one
four-address class.  Every actual collision is internal to one class, and
every actual unit edge occurs in the conservative supergraph.

## Additional exact structure

The 21-point contact graph has vertex connectivity exactly three: there are no
cuts of size at most two and exactly twelve three-cuts.  The first is
`{3,5,15}`.

For each source index, its translated copy in the self-sum is injective and
four-chromatic.  Every pair of these 21 fibres intersects at the corresponding
sum point.  Their exact unit edges therefore form a connected spanning union,
and the actual self-sum graph is connected and bridgeless.

## Reproduction

CPython 3.11 or later and a complete repository checkout suffice; only the
standard library is used:

```sh
python3 -B hadwiger_nelson_ei21_contact_selfsum_review1/verify.py --check-expected
python3 -O -B hadwiger_nelson_ei21_contact_selfsum_review1/verify.py --check-expected
python3 -B hadwiger_nelson_ei21_contact_selfsum_review1/controls.py
(cd hadwiger_nelson_ei21_contact_selfsum_review1 && sha256sum -c SHA256SUMS)
```

The controls exercise 8,235 interval samples, compare the colouring search
with brute force in 1,024 graph/palette cases, test three known connectivity
examples, and reject four malformed or improper colour words.

See [PROOF.md](PROOF.md) for the complete proof reduction,
[REVIEW.md](REVIEW.md) for the verdict, [PROVENANCE.md](PROVENANCE.md) for
source hashes, and [VALIDATION.json](VALIDATION.json) for replay details.

## Exact limitations

The accepted theorem concerns only the unique exact root in the declared box
and its full commutative self-sum.  The conservative 210 classes and 731 edges
are not asserted to be the exact physical point and edge census; unresolved
addresses inside a class may be equal or distinct, and possible edges may be
false positives.

No other EI21 root, contact, sum, difference, rotation, shell, or copy count is
classified.  This is a restricted construction stop, not a global
Hadwiger--Nelson result or record candidate.
