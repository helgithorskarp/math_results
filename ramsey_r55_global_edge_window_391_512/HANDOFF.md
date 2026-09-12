# Complete-class handoff

For any complete physical red/blue coloring of `K_43` that avoids a
monochromatic `K5`, the 903 physical red-edge bits satisfy

```text
391 <= sum_(0<=i<j<43) x_ij <= 512.
```

This replaces the accepted `390..513` necessary window.  After color
complementation to at most 451 red edges, an unrestricted construction
search may use `391..451`.  The theorem covers arbitrary labels, degree
sequences, and automorphism groups; no conversion through a packing carrier
is required.

The two newly closed physical classes are exactly `e=390` and `e=513`.
The result does not assert that any graph at another edge count is good, and
it does not retire an existing carrier task unless that task's physical
constraints force one of these two totals.

The proof imports the accepted full-catalog boundaries listed in
`DEPENDENCIES.json`.  A consumer that does not accept those finite-data
premises must not use the strengthened inequality as an unconditional
constraint.

The next mathematical layer is explicit rather than open-ended: at total
degree excess eight (`e=391`), the dense-neighborhood threshold becomes
`s_v>=4` and the local overlap obligation becomes common deficit at most
four.  The same coarse scan leaves 26 profile pairs in seven bins, so any
continuation must physically classify those survivors and close the global
excess-eight incidence join.  Merely reporting the 26-pair census would not
be a further milestone.
