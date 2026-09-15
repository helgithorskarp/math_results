## Exact forcing-bearing construction stop

Take two copies of the exact 29-point/75-edge frozen-centre source F29.  Let
`p_4` be a marked centre-neighbour and `p_1` a vertex in both odd-cycle cases
of its palette proof.  Put `s=p_4+p_1`, `q=sqrt(35)/5`,
`w=(s+i*q*s)/2`, and apply the half-turn `g(z)=w-z` to the second copy.
Exact identities `|s|^2=5/3` and `q^2=7/5` give the three prescribed cross
contacts `0--w`, `p_4--g(p_1)`, and `p_1--g(p_4)`.  The frame has nonzero
`sqrt(35)` coefficients and lies outside the original source field.

Collision merging gives 58 distinct physical points and no identifications.
Complete exact reconstruction of all 1,653 pairs gives 171 unit edges: 150
inside the two source copies and 21 genuine cross-copy contacts.  A checked
proper four-colour word exists.  An embedded F29 copy is exhaustively not
three-colourable, so the whole graph has chromatic number exactly four.

On the active interface `(0,w,p_4,p_1,g(p_4),g(p_1))`, the induced graph has
23 canonical proper four-colour patterns.  Explicit checked whole-graph words
extend every one.  Hence the complete unrestricted active-interface relation
equals the bare relation: this physically coupled outside-field self-gluing is
neutral.

This retires exactly the displayed half-turn and role pair `(4,1)`, without a
role, phase, radical, copy-count, closure, or deletion sweep.  It is a scoped
four-colour stop, not a five-chromatic graph or record progress.

Reproducible exact source, construction proof, complete reconstruction,
certificate, producer, independent arithmetic checker, normal/optimized
validation, and ten corruption controls:

https://github.com/helgithorskarp/math_results/tree/1a1586aea2eebebe07be1aa4987c38a89b809e8c/hadwiger_nelson_twisted_f29_selfglue_stop

Point-stream SHA-256:
`13452bc53b33d560132c3562fc77bc2c2d6141678eed6b2d3c163713279e581b`.

Edge-stream SHA-256:
`efcb7bd37abef4bfc220bcd447f548e724f3c1fc0b7339b447d98a62219bb995`.
