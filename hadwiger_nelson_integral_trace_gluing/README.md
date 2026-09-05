# The locally integral quadratic-trace obstruction

Let `E=Q(i sqrt(3),i sqrt(11))`, with its accepted embedding into
`U=Q_2(omega)`, `omega^2+omega+1=0`, and let `O=Z_2[omega]`.
For a unit complex rotation `u` of degree two over E, write its minimal
polynomial as `Z^2-T Z+J`.

If `T` maps into `O`, then **every union of two connected E-source graphs
placed by `g(z)=u z+h`, with `h in E(u)`, is four-colourable**. No cross
cycle, denominator, cardinality or disjointness restriction is needed.
Reflection is included by conjugating the second source.

The [proof](PROOF.md) treats two exhaustive cases:

- **Even local trace, `T in 2O`:** the cross-edge equation is
  `N(x)+N(y)-T conjugate(x)y=1`. Its scaled difference reduces to the same
  pair of binary trace functionals as the preceding trace-zero argument.
  The resulting affine residue colouring works at every negative depth.
- **Unit local trace, `T in O^*`:** normalize `w=u/T`. Its polynomial
  `w^2-w+1/N(T)` has two simple residue roots. Their unique compatible lifts
  give an embedding of the entire field `E(u)` into U commuting with
  conjugation. The whole field has chromatic number exactly four.

Here T is the relative algebraic trace over E, which can be non-real.
Local integrality refers to the fixed embedding with `sqrt(33)=1 mod 8`;
it is not the assertion that the displayed rational coefficients are
ordinary integers.

This extends the [trace-zero theorem](../hadwiger_nelson_trace_zero_gluing/PROOF.md).
**Negative-valuation traces, translations outside E(u), and general
forest interfaces remain open.** The even-trace result does not assert a
four-colouring of the whole extension. No five-chromatic graph with at
most 508 vertices has been established.

## Reproduce

From this directory in a complete repository checkout, use Python 3.11
or later, standard library only:

```sh
python3 check_algebra.py > /tmp/integral-trace-algebra.json
cmp expected_algebra.json /tmp/integral-trace-algebra.json
python3 examples.py > /tmp/integral-trace-examples.json
cmp expected_examples.json /tmp/integral-trace-examples.json
python3 audit_examples.py > /tmp/integral-trace-audit.json
cmp expected_audit.json /tmp/integral-trace-audit.json
sha256sum -c SHA256SUMS
```

`arithmetic.py` implements both colour recipes, exact local-coordinate
reduction, and the compatible binary root lift. Nonintegral traces are
rejected; the two recipes also reject use in the other's branch.
Imported field/residue arithmetic and polynomial utilities are hash-pinned.

`check_algebra.py` expands the two coordinate identities in the universal
scaled perturbation formula. It separately exhausts the quadratic root
sets for all 192 unit traces modulo 16: **49,152 candidates and 384 exact
roots**. The direct quotient-polynomial search matches the two Hensel
constructions entry for entry. Nine odd normalized constants are lifted
compatibly through 32 bits, with polynomial and conjugate-branch checks
at every precision. The finite computations supplement the proof of
arbitrary-precision lifting; 32 bits is not its validity limit.

## Boundary evidence

The rotation `(2+i sqrt(5))/3` has trace `4/3`, of local valuation two.
The new gluing theorem applies. Yet this extension has **no embedding
into U that commutes with conjugation**: a norm-one U-element's conjugate
trace is either odd or congruent to two modulo four, while `4/3` is zero
modulo four. The six norm-one elements modulo four verify this residue
obstruction. This does not prove that the extension needs five colours.

For the unit-trace rotation `(1+i sqrt(35))/6`, the source anchors `1` and
`1/3` both have residue one, but their placed separation is one. Plain
centred residues therefore fail; the compatible whole-field colouring
succeeds. This concrete control prevents dropping the even-trace condition
from that simpler colouring formula.

## Exact geometries

Thirteen cases are reconstructed by both geometry programs:

| Case | Physical vertices | Strict edges | Cross edges |
|---|---:|---:|---:|
| Even-trace control, two wheels | 14 | 25 | 1 |
| Even-trace control, mixed B292/V214 | 506 | 2,231 | 3 |
| Unit-trace control, two wheels | 14 | 25 | 1 |
| Unit-trace control, mixed B292/V214 | 506 | 2,229 | 1 |
| Even trace, depth 1 wheels | 14 | 25 | 1 |
| Even trace, depth 2 wheels | 14 | 25 | 1 |
| Non-real even trace, depth 2 mixed B292/V214 | 506 | 2,229 | 1 |
| Even trace, depth 3 wheels | 14 | 25 | 1 |
| Earlier quadratic path | 6 | 5 | 5 |
| Common-centre wheels | 13 | 24 | 12 labelled |
| Wheels without cross edges | 14 | 24 | 0 |
| Non-real unit-trace field grid | 49 | 168 | Not a two-source decomposition |
| Fractionally translated field grid | 49 | 168 | Not a two-source decomposition |

The wheel is the origin and the six unit triangular-lattice vectors.
The path sources satisfy one local-coset condition each; they are not
asserted connected. All other two-source cases have connected source
graphs. The field grids contain all `A+B u` for two seven-point coefficient
sets, testing the stronger whole-field result beyond a two-copy union.
One grid uses nonintegral coefficient offsets. Non-real-trace controls
use `rho=(-1+i sqrt(3))/2`, so the minimal polynomial has trace `rho T`
and constant `rho^2`. The exact recipes are in `examples.py`.

All paired cross interfaces are forests. The small cases and three
selected mixed placements calibrate the formula; they are not an
exhaustive placement search or difficult non-four-colourability tests.
The uniform theorem closes the stated algebraic stratum by proof.

## Independent audit and certificate conventions

The generator represents points in `E[u]` and computes norms by expanding
the quadratic algebra. The audit imports neither the new arithmetic nor
the generator. It reconstructs B using generic real-radical arithmetic,
then computes distances from real dot and signed-area expressions.
Every one of the **386,299 labelled pair distances**, every strict edge
and every supplied colour agrees. Cross acyclicity is checked by union-find.
These are independent author implementations, not external peer review.

Each rotation is `u=rho*(a+i sqrt(D))/b`, with `D=b*b-a*a>0`. Squared
distances have the unique rational-coefficient representation

```
A+B sqrt(33)+C sqrt(3D)+F sqrt(11D).
```

The non-base square tests ensure independence of this basis. For each
example, the complete distance hash uses ascending `i<j` lines
`i,j:A_n/A_d,B_n/B_d,C_n/C_d,F_n/F_d`, ending in newlines. Point labels use
source order, or product order for the grids. A coincident point keeps
its first label for strict-edge deduplication; the distance stream still
contains its zero-distance labelled pair. Strict-edge streams use sorted
physical-label pairs `i,j`, also ending in newlines. The expected JSON
contains complete colour strings and the small cross-edge lists.

The generic geometric reduction, local-coset argument, Hensel limit and
compatible-field embedding are unformalized mathematics. Sampling does
not establish their infinite quantifiers. No solver result, approximate
distance, private input or omitted large certificate is used. Full
distance streams are regenerated and hashed rather than stored. The
manifest pins all required code, input tables and proof/provenance files;
the reproduction commands require a complete checkout and no network.

Measured CPython 3.11.2 runtimes were 0.154,
7.441 and 4.591 seconds respectively, with maximum child peak
RSS 18,284 KiB across the serial workflow. No background computation remains.
