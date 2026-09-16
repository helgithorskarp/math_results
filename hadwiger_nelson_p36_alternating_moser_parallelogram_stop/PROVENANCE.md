# Provenance and evidence boundary

The exact patch is the reviewed source

```text
P36 = {a+b*omega : a^2+a*b+b^2 <= 36},
omega = (1+i*sqrt(3))/2.
```

Relevant prior packages, inspected before selection:

- `hadwiger_nelson_four_triangular_patches` and its independent review:
  arbitrary rotations about one common origin are four-colourable.
- `hadwiger_nelson_four_triangular_radius147` and its independent review:
  arbitrary translated/rotated four-`P36` unions with a common physical point
  are four-colourable.
- `hadwiger_nelson_p36_quarter_turn_collars` and its independent review: the
  exact cyclic quarter-turn anchor family is four-colourable.

The present construction was selected outside those hypotheses: it uses two
alternating orientations `1,rho,1,rho`, nonzero translations, and has empty
fourfold intersection.  The topology and formulas in the README were frozen
before its physical graph was coloured.  Its failure does not extend any of
the prior family theorems and proves nothing about other translated four-patch
placements.

The producer and verifier are independent arithmetic implementations of the
same displayed construction.  Their matching canonical streams and direct
positive three-colour witness are author-side evidence, not an external
review.
