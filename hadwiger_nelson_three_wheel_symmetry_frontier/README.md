# Three-wheel exact frontier: at most 5,114 physical classes

Let

```text
W = {0, 1, omega, omega-1, -1, -omega, 1-omega},
S(u,v) = W + uW + vW,        |u|=|v|=1,
omega = (1+i sqrt(3))/2.
```

The [source theorem](../hadwiger_nelson_three_wheel_architecture/README.md)
proves that every possible non-four-colourable member belongs to a finite
exceptional set of at most 904,317 ordered parameter pairs.  This package
quotients that exact frontier by all evident physical symmetries.

**Theorem.** Up to Euclidean graph isomorphism, at most **5,114** members of
the complete three-wheel architecture can still be non-four-colourable.
The injective branch is covered by 800 certified event-curve-pair
representatives whose `P1 x P1` intersection numbers sum to **5,110**.  The
collision branch has only **four** nonalignment parameter orbits.  This is a
necessary frontier, not a claim that any of the 5,114 classes is
non-four-colourable.

The acting group has order 432: independent sixth-root rotations of the two
free wheels, all six permutations of the three summands, and reflection.  On
the nonalignment domain it permutes the 972 relevant event factors in eleven
orbits and permutes the thirteen source colour words.  Of the source cover's
71,134 pairs, 66,515 survive alignment removal; their invariant closure has
280,197 pairs in exactly 800 group orbits.

## Exact replay

CPython 3.11.2 and the standard library suffice:

```bash
python3 -B hadwiger_nelson_three_wheel_symmetry_frontier/verify.py --check-expected
python3 -O -B hadwiger_nelson_three_wheel_symmetry_frontier/verify.py --check-expected
python3 -B hadwiger_nelson_three_wheel_symmetry_frontier/controls.py
```

The verifier replays the source factorization and all 487,578 source
coprimality witnesses, checks 3,888 exact generator identities, reconstructs
the 432-element group and all pair orbits, and verifies the ten collision
norm types and their exact representatives.  No solver, CAS, floating-point
predicate, unpublished expanded frontier, or graph candidate is used.

Optional byte-for-byte regeneration uses `sympy==1.14.0`:

```bash
python3 -m venv /tmp/hn-three-wheel-symmetry-venv
/tmp/hn-three-wheel-symmetry-venv/bin/pip install -r \
  hadwiger_nelson_three_wheel_symmetry_frontier/requirements.txt
/tmp/hn-three-wheel-symmetry-venv/bin/python -B \
  hadwiger_nelson_three_wheel_symmetry_frontier/produce.py \
  --out /tmp/hn-three-wheel-symmetry-certificate
cmp /tmp/hn-three-wheel-symmetry-certificate/certificate.json \
  hadwiger_nelson_three_wheel_symmetry_frontier/certificate.json
```

The 122,751-byte [certificate](certificate.json) has SHA-256
`14e2a5e3fc00af36d4ef57b6a8fdd964450633b0ab76f0f2783094172ec69132`.
See the [proof](PROOF.md), [validation receipt](VALIDATION.json), and
[HN2 handoff](HANDOFF.md).

No five-chromatic unit-distance graph is produced, so this is not a record
improvement.  Root isolation, strict physical graph reconstruction, and
chromatic decisions remain open.
