# A complete field slice of the independently rotated three-spindle sum

**Every graph in the exact class below is four-chromatic.** The proof exhausts
1,152 exceptional phases, collision-merges their physical points, and checks
38 shared positive colour words against every strict unit edge. Generic phases
have a separately checked colouring. Every support has at most 343 points.

This closes the selected finite contact class and its generic complement.
It is not a five-chromatic construction or record advance. It does not close
arbitrary independent rotations, rotations outside the specified complex
field, or another choice of the fixed phase. The source is retired at this
complete negative gate; no phase, field, sum size, or host expansion follows
from the result.

## Exact physical class

Put

```
alpha = i sqrt(3),
F = Q(sqrt(5),sqrt(33)),   E = F(alpha),
omega = (1+alpha)/2,
eta = (5+i sqrt(11))/6 = 5/6 + alpha sqrt(33)/18,
rho = (7+i sqrt(15))/8 = 7/8 + alpha sqrt(5)/8,
M = {0,1,omega,1+omega,eta,eta omega,eta(1+omega)}.
```

For every `v in E` with physical complex norm `v conjugate(v)=1`, let

```
S(v) = M + rho M + v M.
```

Coincident addresses are identified, and the graph contains **every** pair
of distinct points at Euclidean distance one. `B=M+rho M` has 49 distinct
points and 154 strict unit edges. Thus `B+vM` has 343 formal addresses before
merging. All points are specified exactly; no abstract embedding is inferred.

The field condition is on the complex phase: `v=X+alpha Y` with `X,Y in F`.
Its Cartesian coordinates lie in `Q(sqrt(3),sqrt(5),sqrt(11))`, but the theorem
does not quantify over every cosine/sine pair in that larger real coordinate
field. This distinction is part of the scope.

The rationale was a complete, capped event decision using familiar spindle
and rotation ingredients from [de Grey's construction](https://arxiv.org/html/1804.02385v2).
The sqrt(5) phase leaves the previously four-colourable base complex field
`Q(i sqrt(3),i sqrt(11))`. This is not a new construction method or a claim
that these 343-point graphs were already known to be five-chromatic.

The prior [correlated family](../hadwiger_nelson_correlated_moser_cube/README.md)
has phases `(1,u,u^2)`, and the accepted
[collision-locus theorem](../hadwiger_nelson_independent_moser_sum_collisions/README.md)
excludes all noninjective independent three-spindle sums. Here the first
phase rho is fixed and the other phase ranges over E. There are 1,092
injective exceptional phases; the collision cases are included for a complete
self-contained check. Neither earlier theorem is an imported proof premise.

## Complete finite reduction

Order B lexicographically by its eight rational coefficients, and use the
displayed order of M. Formal address `7*i+j` denotes `B[i]+v*M[j]`. All
coordinates of B and M have denominator 288 in the basis

```
1, sqrt(5), sqrt(33), sqrt(165),
alpha, alpha sqrt(5), alpha sqrt(33), alpha sqrt(165).
```

For each of the 58,653 unordered address pairs, write its difference as
`a+v b`. When one of a,b is zero, the unit condition is independent of v.
These give exactly 1,617 generic edges, the Cartesian graph of three spindles.
If both are nonzero, set

```
c = conjugate(a)*b,
s = N(a)+N(b)-1,
Delta = 4*N(a)*N(b)-s^2.
```

Here the displayed formulas use actual coordinates; the implementation clears
the common denominator and replaces 1 by `288^2` in s. For a unit phase,

```
N(a+v b)=1  <=>  c*v^2+s*v+conjugate(c)=0.
```

Since `c != 0`, the only possible roots in E are

```
v = (-s +/- alpha*sqrt(Delta/3))/(2*c).
```

They are physical unit roots exactly when `Delta/3` has a square root in F.
Necessity also follows directly: for a unit root the real part of `2cv+s`
vanishes, so `(2cv+s)/alpha` is real and belongs to `E intersect R=F`.
Sufficiency is checked by substitution and norm one for every returned root.
Thus negative radicands, nonsquares, repeated roots and both signs are handled
without numerical approximation or a root-isolation tolerance.

The producer keeps 18,636 equations after dividing their integer coefficient
vectors by a rational scalar. This is not a quotient by arbitrary F-scalars;
redundant equations are harmless. Exactly 2,104 equations have roots in E.
Their roots are deduplicated by exact rational coefficient tuples.

A collision requires `v=-a/b` and `N(a)=N(b)` when both differences are
nonzero. These are separately exhausted and give 60 collision phases.
Together, unit and collision events give **1,152 distinct phases**. For phases in E outside
that finite set, there are no collisions and only the 1,617 generic edges.
A supplied generic colour word therefore covers every remaining unit phase
in E, including phases not explicitly listed by the enumeration.

## Exhaustive square testing

`model.py` decides square membership in F by the tower
`Q subset Q(sqrt(5)) subset Q(sqrt(5),sqrt(33))`. The following elementary
recursion proves completeness. At a stage `K(sqrt(d))`, write the proposed
square as `A+B sqrt(d)` and a putative root as `x+y sqrt(d)`.

If B is zero, `2xy=0`, so test a square root of A in K and a square root of
`A/d` in K. If B is nonzero, x and y are nonzero and

```
(x^2-d*y^2)^2 = A^2-d*B^2.
```

Find a square root t of the right side in K. If none exists, the original
element is not a square. Otherwise test both signs of t, then test a square
root of `(A+t)/2` in K and set `y=B/(2x)`. Check the resulting square exactly.
These alternatives are exhaustive. The recursion ends with perfect-square
tests of rational numerators and denominators. The positive nonsquare tower
generators 5 and 33 ensure the stated unique coefficient representations.

## Colour and complete-geometry certificates

`certificate.json` contains 38 length-343 words, a pointer for each exceptional
phase, a generic pointer, and the hash of the regenerated exact phase order.
Every event word respects all equal-address constraints and every unit edge.
The point counts are:

| Distinct points | Phases |
|---:|---:|
| 182 | 2 |
| 245 | 2 |
| 252 | 4 |
| 259 | 4 |
| 294 | 8 |
| 301 | 16 |
| 308 | 8 |
| 315 | 8 |
| 329 | 8 |
| 343 | 1,092 |

The complete physical graphs have 769--1,631 edges. Every S(v) contains the
original M, and all `3^7` assignments fail on its eleven unit edges, proving
the lower bound four. The words prove the matching upper bound.

The required C++ audit independently constructs the collision quotient from
literal integer coordinates, reconstructs **all 66,674,426 unordered pairs**
of distinct physical points, compares the full edge lists, and checks the
colouring on **1,851,504 physical unit-edge incidences**. It uses direct
four-coefficient norm formulas, while the event census uses recursive field
multiplication. Coordinate construction for the audit uses a separate flat
bit-mask product. No contact candidate or edge is omitted by a floating filter.

The audit checks that every numerator and positive denominator has magnitude
below `2^50`. Coordinate differences are below `2^51`; every norm coefficient
is then below `2^112`, safely within signed 128-bit arithmetic. Python field
arithmetic uses arbitrary-precision integers and exact fractions.

## Reproduce

Verification needs Python 3.11+ and a C++17 compiler (validated with g++ 12.2).
From the repository root, write generated files outside the checkout:

```
g++ -O3 -std=c++17 hadwiger_nelson_fixed_rho_moser_field_slice/audit.cpp -o /tmp/hn-rho-audit
python3 -B hadwiger_nelson_fixed_rho_moser_field_slice/verify.py --audit-binary /tmp/hn-rho-audit --work /tmp/hn-rho-check
python3 -B hadwiger_nelson_fixed_rho_moser_field_slice/controls.py --audit-binary /tmp/hn-rho-audit
```

The verifier output equals `EXPECTED.json`; Python `-O` gives the same bytes.
Controls check all 64 basis products, 625 constructed rational squares,
all 1,827 norm-pair discriminants using the reversed real-field tower, a
positive direct-audit fixture, and rejection of seven deliberately corrupted
geometry/colour inputs. The public producer regenerates the compact certificate
byte for byte in the recorded environment:

```
python3 -m pip install -r hadwiger_nelson_fixed_rho_moser_field_slice/requirements-search.txt
python3 -B hadwiger_nelson_fixed_rho_moser_field_slice/produce.py --output /tmp/hn-rho-new-certificate.json
```

Use a separate environment for this optional producer. It uses CaDiCaL 1.9.5
through python-sat 1.9.dev15 with a 200,000-conflict cap on each fresh positive
query. Only 38 colour words were needed; there was no UNKNOWN or non-four
signal. A failed query stops regeneration and cannot certify an exclusion.
The verifier needs no SAT solver, negative proof or trusted solver verdict.
Large inventories and direct-audit streams remain outside Git and regenerate
from the source. The compact certificate is 15,620 bytes.

## Claim status and stopping boundary

This is an author-verified, complete restricted-family exclusion with a
written finite-reduction proof. It is not independent review, formalization,
or a priority claim. The common number-field routines remain part of the
implementation trust boundary, alongside ordinary compiler/runtime arithmetic;
the separate physical audit and reversed-tower controls reduce that shared
risk without constituting external verification.

The class was selected under the certificate-first HN lane reset after the
fixed Parts/L374 a=8 residual was banked. That master and its 17,269 cuts were
not reopened or changed. R1's positive-parent superposition, R3's coupled
realization work, and R4's bottom-up weighted sums are separate ownership
lanes. The present theorem is not a local terminal relation or a pair-docking
census; it decides the complete graph at every phase in the specified field.

The published vertex benchmark remains
[Parts's 509-point construction](https://arxiv.org/abs/2010.12665), also stated
in [Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4),
checked on 14 September 2026. This theorem does not improve that benchmark.
