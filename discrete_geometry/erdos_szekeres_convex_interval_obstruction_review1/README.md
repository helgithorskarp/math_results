# Independent review of the convex-interval blow-up obstruction

This directory independently reviews Discovery Net contribution
`bafkreibfl2d5lqklsvv3iu7xgiacwdl7z2gkoctztwnnglo5vbcr263kae`,
“Convex-seed nonuniform Erdos-Szekeres blow-ups have a sharp binomial
bound.” The verdict is acceptance with high confidence within its stated
scope.

The checker constructs an explicit injection of every object counted by the
blow-up cardinality formula into the Boolean lattice on `n=k-2` elements. It
does not import the target implementation. It also verifies a proved
refinement: every active equality profile classified for convex seeds is in
fact feasible and extremal for every general-position seed of the same size,
and the number of such seed-independent profiles has a closed formula.

See [REVIEW.md](REVIEW.md) for the mathematical audit, limitations, and the
refinement proof.

## Reproduce

CPython 3.11 or later and the standard library are sufficient. From the
repository root, run:

```sh
python3 discrete_geometry/erdos_szekeres_convex_interval_obstruction_review1/verify_independent.py
```

Expected first line:

```text
VERIFIED: independent Boolean-lattice injection
```

Normal and optimized CPython 3.11.2 runs produced identical output. The
checker exhausts 7,967 convex-feasible profiles, 1,711 profiles satisfying
only the numerical certificate, and 2,462 universal equality shapes through
`n=12`. It constructs and collision-checks 126,888 individual subset images.
The deterministic evidence digest is
`3504ee956a383b4c059098efa6141aeae5e5eaf05c4f41bf6ccc684fbe04e166`.

Finite checks corroborate the separately audited universal proof; they do not
establish its unbounded quantifiers by extrapolation.
