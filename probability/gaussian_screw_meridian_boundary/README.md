# Exact screw/meridian endpoint boundary

For a contracting finite matching of two full-dimensional rigid groups,
with proper relative isometry, [PROOF.md](PROOF.md) classifies whether the
matching extends to a rotationally equivariant 1-Lipschitz map in **any**
independent endpoint frames. For a nontrivial relative rotation the only
possible axis is the screw axis, and the decision is an exact cross-pair
inequality. Translation, zero pitch, common norm anchors, the scalar-defect
criterion and paired affine rank are also classified.

The two existing screw controls give a strict separation:

| Preserved control | R5 contracting motion | Equivariant endpoint completion |
| --- | --- | --- |
| Eight-site positive screw6456 | Yes, inherited analytic construction | Impossible in every frame |
| Twenty-four-site obstruction6472 | No, inherited author obstruction | Yes, even globally on R3 |

The motion columns import the original proofs; this checker only verifies
the new endpoint calculations. Both motion claims remain separately
identified author-proof dependencies without independent acceptance in
the recorded refresh. Neither control is a Gaussian
counterexample. The unrestricted dimension-three question remains open.

Reproduce from the repository root with CPython3.11, standard library only:

```bash
python3 -B probability/gaussian_screw_meridian_boundary/verify.py
python3 -O -B probability/gaussian_screw_meridian_boundary/verify.py
python3 -B probability/gaussian_screw_meridian_boundary/verify.py probability/gaussian_screw_meridian_boundary/INPUT.json
```

The first two commands compare exact output with [EXPECTED.json](EXPECTED.json)
and finish with status `EXACT_SCREW_MERIDIAN_BOUNDARY_PASS`. They check five
motion types, three independent endpoint reframings including reflection,
five rejected invalid inputs, an explicit orbit loss `-4/5`, and the
universal paraboloid identity. Runtime is about one second on the author's
host. No solver, numerical integration, randomness or old motion checker
is used.

The third command illustrates classification of a supplied rational
matching. [INPUT.json](INPUT.json) has exactly two groups, each with
`source` and `target` lists of points. Coordinates must be integers or
rational strings. Each group must affinely span R3, preserve all distances,
and the combined endpoints must contract. Improper relative isometries
are rejected, even though either independent endpoint frame may be
improper. This decision concerns the stated rotational extension problem;
`equivariant_completion: false` does not mean Gaussian majorisation fails.

[INPUTS.json](INPUTS.json) pins six public dependency files. The only
external data read are the existing compact 24-site witness and those
public files for hash verification. [SHA256SUMS](SHA256SUMS) covers this
directory. A full repository checkout supplies the relative dependencies.

[HANDOFF.md](HANDOFF.md) states the geometric consequence and limits.
[SOURCES.md](SOURCES.md) records primary literature and graph dependencies.
The theorem is an author proof with reproducible exact controls, not a
formal proof, independent acceptance, or established priority claim.
