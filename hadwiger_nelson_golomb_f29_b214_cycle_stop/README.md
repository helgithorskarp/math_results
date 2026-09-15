# A heterogeneous cycle preserves every complete forcing-input colouring

The frozen cycle of a Golomb graph, F29 and Parts's B214 gadget has
**250 distinct exact points and 1,070 complete unit edges**. Every complete
four-colouring of B214 extends to the whole graph. The graph is exactly
four-chromatic, with no articulation or bridge, but no new private contact
beyond the three input graphs. This is a fixed construction stop, not a
five-chromatic candidate.

The intended input incompatibility was B214's published distance-three
unequal-pair relation, acting on a connected Golomb/F29 input which permits
its two tips to have the same colour. The planned finishing gate was precise:
if the common root and the Golomb tip, at distance two, became forced equal,
a two-copy spindle would use at most 499 points. A checked whole four-word
keeps those vertices different, so that equal-pair gate fails. The spindle
itself was not constructed or claimed four-colourable.

## Frozen geometry

Use the native complex coordinates G for Golomb, F for F29 and B for B214.
Put

```
eta = (sqrt(33)+i*sqrt(3))/6
u   = (-1+3*i*sqrt(7))/8
v   = (-3+i*sqrt(7))/4
G'  = 1-G
F'  = u*(1+conjugate(eta)*F)
B'  = 1+u+v*B.
```

All three multipliers have modulus one. Their only pairwise overlaps are

```
O = G'[1] = F'[9]   = 0
P = G'[4] = B'[187] = 2
Q = F'[12]= B'[186] = 2*u.
```

Thus `OP=OQ=2`, `PQ=3`, and the total is `10+29+214-3=250`.
Complete reconstruction gives exactly `18+75+977=1070` unit edges, all
inherited. The coordinates use rational coefficients in
`Q(i*sqrt(3),i*sqrt(11),i*sqrt(7))`, at common denominator 96. Each pair of
components shares only one point; the older two-overlap field theorem is not
being used to close this graph.

## Universal extension

Given any proper B214 word, let its colours at P,Q be a,b. Give O colour b.
A fixed F29 word has the same colour at vertices 9 and 12, so a colour
permutation extends the assignments at O,Q. Golomb has explicit templates
for both equality and inequality at vertices 1 and 4; choose the appropriate
one and permute its colours to match O,P. There are no further contacts.
This extends the **entire** B214 word, with no enumeration or solver assumption.
The argument also handles hypothetical a=b and does not need B214's forcing
theorem. The source relation is unchanged, not amplified by the cyclic join.

## Reproduce

Python 3.11+ and the standard library suffice, from the repository root:

```sh
python3 -B hadwiger_nelson_golomb_f29_b214_cycle_stop/verify.py --check-expected
python3 -O -B hadwiger_nelson_golomb_f29_b214_cycle_stop/verify.py --check-expected
python3 -B hadwiger_nelson_golomb_f29_b214_cycle_stop/controls.py
```

The checker collision-merges the exact coordinates, reconstructs all 31,125
pairs, checks literal whole four- and five-words and every extension template,
and certifies all 16 assignments to the two interface colours. It verifies
Golomb's lower bound by a complete `3^7` search. No negative SAT verdict is
used. See [PROOF.md](PROOF.md) and [PROVENANCE.md](PROVENANCE.md).

The named root/P equal-pair architecture is retired. No other pole, sign,
frame, source replacement, deletion order, receiver, or copy count was tried.
This does not exclude other heterogeneous interactions or incidental contacts
in a separately constructed larger union.

[Parts's 509-point/2,442-edge construction](https://arxiv.org/abs/2010.12665)
remains the supported unrestricted record, also stated by
[Haugland v4](https://arxiv.org/html/2608.04542v4). This result does not improve it.
