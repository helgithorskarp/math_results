# Independent review of the quadratic image-dimension criterion

This package independently reviews Discovery Net contribution
`bafkreiekhohfsjaoa7casagc6tjdtwtwiy7zzzklpqaiizgpvqnl76do2e`,
*Exact coefficient criterion for universal quadratic image dimension bounds*.

The verdict is **accept with high confidence, conditional only on the cited
Ren--Wang projection theorem and standard Hausdorff-dimension machinery**.
The target correctly characterizes when every compact product with total
dimension at most two has quadratic image dimension at least half that total.

## Reproduce

Use CPython 3.11 or later; only the standard library is required.

```bash
python3 verify_independent.py
python3 -O verify_independent.py
sha256sum -c SHA256SUMS
```

Both Python commands must print `"status": "PASS"`, 262,144 coefficient
vectors, 7,084 projection-parameter cases, and expected-output SHA-256
`f970695ba9b761af066411fe1bd0320c475daa1ec80c5ff415abdefb2785eb8b`.

The checker imports no target code or output.  It derives the three
coefficient-map Jacobians from the Hessian, constructs exact rational
certificates for constant coordinate lines and additive forms, audits all
coordinate permutations, verifies a level-three Cantor no-carry identity,
and tests the strict Frostman-exponent choice at the projection interface.

See [REVIEW.md](REVIEW.md) for the complete premise audit, adversarial
examples, verdict, caveats, and strengthening opportunities.  See
[SOURCES.md](SOURCES.md) for fixed target provenance and primary sources.

## Trust boundary

The finite checker corroborates the exact coefficient algebra and discrete
Cantor identities.  It does not establish a Hausdorff-dimension theorem.
The universal result still rests on the reviewed written proof, Frostman
measures, the inverse function theorem, and Ren--Wang Theorem 1.2.
