# A six-chromatic residue quotient whose exact orbit ball is three-chromatic

No five-chromatic plane graph is produced here, and the 509-vertex record is
unchanged. This package gives a sharp construction-selection stop: an exact
mixed unit contact and all six of its rotations make a natural 256-state
auxiliary quotient six-chromatic, but the corresponding complete 289-point
strict plane unit-distance support has chromatic number exactly three.

The result is useful precisely because it separates an abstract chromatic
signal from its physical realization. It retires this declared weighted
mixed-orbit ball without turning quotient unsatisfiability into a plane-graph
claim.

The input mixed contact comes from the independently accepted
[`weighted_rotation_residue_obstruction`](../hadwiger_nelson_weighted_rotation_residue_obstruction/README.md)
at source commit `7b66b3e53fdbda9d18530b8c2cfb64e27f661806`, with high-confidence review
at commit `904dcc43b17d44df17f217adde1f33a20dd92ce2`. The earlier
[`common_neighbour_phase_sumsets`](../hadwiger_nelson_common_neighbour_phase_sumsets/README.md)
screen tested the same broad `D+D` shape only for specified phases in
`Q(sqrt(3),sqrt(11),i)`; the present `sqrt(13)` phases are outside that census
and were admitted by the exact quotient signal rather than contact density.

## The auxiliary signal

Let

```text
R = (Z/4Z)[w]/(w^2+w+1).
```

Write `U` for the six elements of norm one, `V={2,2w,2+2w}`, and let `T`
be the six-element `U`-orbit of `2+w`. On the additive group `R x R`, take
the undirected Cayley graph with directions

```text
{(0,e),(e,e): e in U} union {(v,0): v in V}
union {(t,t): t in T}.
```

It has 256 vertices, degree 21 and 2,688 edges. A checked six-colour word is
embedded in `verify.py`. The standard five-colour CNF has 1,280 variables and
16,259 clauses after exact-one constraints and three sound triangle pins.
Its SHA-256 is

```text
c5b0faf45916cef4f2e65b025c93d16f4b27bef696da814df56e23b09f3b8525
```

Kissat 4.0.4 generated a transient DRAT refutation, and `drat-trim` commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` returned `s VERIFIED`. Thus the
auxiliary graph has chromatic number exactly six. The 63 MiB trace remains
under `/scratch`, as required by repository policy; deterministic source for
the CNF and exact reproduction commands are included below.

Adding only the displayed mixed direction and its negative gives a
17-direction, 2,176-edge quotient with an embedded proper four-colouring.
The full rotational orbit is therefore essential to this auxiliary signal.

## The exact physical gate

Put `alpha=i*sqrt(3)`, `s=sqrt(13)`, and `rho=(1+alpha)/2`. The four unit
phases selected by the quotient calculation are

```text
1,
(5+s*alpha)/8,
(s+alpha)/4,
(-s+2*alpha)/5.
```

Close them under the six rotations by `rho`, obtaining 24 distinct unit
directions `D`, and form the single frozen support

```text
P = D+D.
```

All coordinates lie in `Q(sqrt(13),i*sqrt(3))`. Exact collision merging and
all-pairs distance reconstruction give

| quantity | value |
|---|---:|
| ordered sum addresses | 576 |
| distinct physical points | 289 |
| complete strict unit edges | 1,032 |
| generator-direction edges | 1,032 |
| incidental unit edges | 0 |

The address multiplicities are `24 x 1`, `264 x 2`, and `1 x 24`. The degree
histogram is `24 x 3`, `24 x 4`, `216 x 6`, and `25 x 24`.

The embedded 289-symbol word is a proper three-colouring of every reconstructed
edge. Vertices `0,1,62` form a unit triangle, so the physical graph has
chromatic number exactly three. This is much stronger than a four-colour stop.

The four phases are not guessed analogues. For the reviewed weighted map

```text
W(a,p)=(1-u)*a+u*p,  u=(5+s*alpha)/8,
```

they are exact representatives of the diagonal, horizontal, vertical and
mixed quotient direction classes. Specifically, take

```text
v=2*alpha/3,  d=alpha/15,  r=3*alpha/5.
```

Then `(1-u)*v=(s+alpha)/4` and
`(1-u)*d+u*r=(-s+2*alpha)/5`. Sixth-root rotation supplies the full residue
orbits. `verify.py` checks these identities directly.

## Why the quotient does not lift

The quotient records labels modulo four. Its Cayley edges include torsion
translations that need not occur between representatives in one injective
plane support. In the exact radius-two support above, every physical unit
edge has one of the 24 generating directions and there are no additional
contacts. The supplied three-colouring is therefore the decisive physical
test; the six-chromatic quotient is only the selector that led to it.

This package does not claim a plane realization of the quotient, a bound for
arbitrary weighted supports, a result for other phase sets, or a theorem about
larger/selected word balls. The next complete word-radius event exceeds the
declared architecture rather than authorizing a pruned or phase-varied sweep.

The unrestricted published comparison remains Parts's
[509-point, 2,442-edge graph](https://arxiv.org/abs/2010.12665). Haugland's
[August 2026 v4 paper](https://arxiv.org/html/2608.04542v4) likewise identifies
509 as current; its 2,131-point result has the additional Moser-spindle-free
restriction and is not an unrestricted order improvement.

## Reproduce

CPython 3.11 or later and the standard library verify all exact geometry and
positive colour words:

```bash
python3 -B hadwiger_nelson_weighted_mixed_orbit_gap/verify.py --check-expected
python3 -O -B hadwiger_nelson_weighted_mixed_orbit_gap/verify.py --check-expected
python3 -B hadwiger_nelson_weighted_mixed_orbit_gap/independent_check.py
python3 -O -B hadwiger_nelson_weighted_mixed_orbit_gap/independent_check.py
sha256sum -c hadwiger_nelson_weighted_mixed_orbit_gap/SHA256SUMS
```

To regenerate and independently check the auxiliary non-five proof, with
Kissat 4.0.4 and `drat-trim`:

```bash
python3 -B hadwiger_nelson_weighted_mixed_orbit_gap/verify.py \
  --emit-cnf /scratch/weighted-mixed-quotient-5.cnf
kissat --no-binary /scratch/weighted-mixed-quotient-5.cnf \
  /scratch/weighted-mixed-quotient-5.drat
drat-trim /scratch/weighted-mixed-quotient-5.cnf \
  /scratch/weighted-mixed-quotient-5.drat
```

The recorded ASCII proof has SHA-256
`8f084faba331c1654e09b656989af6cd5497b68a965510d7de59d42688dba150`.
`drat-trim` retained 12,961 input clauses and 237,478 of 416,389 lemmas,
using 11,536,956 resolution steps and 3,851 RAT lemmas. A proof with a
different byte stream is acceptable if the emitted CNF hash matches and an
independent checker verifies it.

The independent checker reconstructs the physical support with the alternate
real/imaginary representation
`x=a+b*sqrt(13), y=sqrt(3)*(c+d*sqrt(13))`; it uses the quadratic norm formula
and an explicit 60-degree rotation, not the primary field multiplication.
The trust boundary is the displayed exact algebra, rational arithmetic, both
complete all-pairs reconstructions, direct checking of the positive words,
and `drat-trim` for the auxiliary lower bound. The auxiliary proof is not a
premise of the physical three-colour conclusion.
