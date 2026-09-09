# Independent review of the complete unit-circle branch

**Verdict: ACCEPT with high confidence for the theorem that every physical
unit-circle member of the complex-radix architecture is exactly
three-chromatic.** For every complex `z` with `|z|=1`, the full strict
Euclidean unit graph on

```text
A5(z) = T + zT + z^2 T + z^3 T + z^4 T,
T = {0,1,(1+i sqrt(3))/2},
```

has chromatic number three, with coincident labels merged and every exact unit
pair included.

This is a complete branch closure, but it is not the target
Hadwiger--Nelson breakthrough. It produces no five-chromatic graph, leaves
non-unit-modulus injective parameters open, and does not improve the
509-vertex record.

## Independent reconstruction

[independent_check.py](independent_check.py) imports no target module. It uses
the compact submitted factor list only as a declarative witness and then
rechecks every statement needed from that witness. In particular, it ignores
the submitted colour specifications and factor-cover assignments.

Starting from all 29,403 unordered pairs of the 243 digit labels, the checker
independently constructs the Laurent norm events and obtains:

```text
universal monomial edges                         1,215
distinct nonzero event polynomials               1,272
degree histogram (2,4,6,8)             (6,27,168,1071)
event stream SHA256
b1d070b53ee5cd13713f598f2baeaa5e0d6dc1a3b9faf20635c28730a97d668d
factor blocks                                       820
exact factor-product identities                   1,272
degree-at-most-four blocks                          124
independently coloured high-degree blocks           696
```

For every high-degree block the checker searches all 16 normalized linear
`F3` digit words from scratch. It rediscovers exactly three:

```text
weights       assigned blocks
11111                     396
11112                     255
11121                      45
```

It then checks every bad event for the selected word, giving 381,888 exact
coprimality certificates. The independent modular images use conjugate roots
at split primes disjoint from the target's primes 7, 13, and 19:

```text
prime 211    380,688 witnesses
prime 223      1,200 witnesses
```

The other ten predeclared fallback primes are unused. A constant modular gcd
at either prime implies a nonzero reduced resultant. Since every factor and
event is monic, degree is preserved; hence the characteristic-zero resultant
in the Eisenstein field is nonzero.

The exact physical fixture is also reconstructed without the target's
irreducibility prime. The checker proves its degree-seven polynomial
irreducible after reduction at prime 337 with `omega -> 209`, verifies the
Cayley identity and rational Sturm isolating interval, and obtains 243 distinct
points, 1,221 strict unit edges, and a proper three-colouring.

Run from the repository root with standard-library CPython 3.11 or later:

```sh
python3 -B hadwiger_nelson_radix_unit_circle_review1/independent_check.py
python3 -O -B hadwiger_nelson_radix_unit_circle_review1/independent_check.py
```

On CPython 3.11.2 both complete outputs have SHA256
`93a504e14d9614d4eab7b1b959e68c8b9c26b022bb02729edf30147bf9065451`.
Each run uses one CPU and took about 17 seconds on the review host.

## Written-proof audit

For a nonmonomial digit difference, remove initial and trailing zero
coefficients to obtain `Q` of degree `n<=4`. On `|z|=1`, complex conjugation
replaces `z` by `z^-1`, so a unit edge is equivalent to a root of

```text
H(z) = Q(z) z^n conjugate(Q)(1/z) - z^n.
```

The leading coefficient is the product of two nonzero digit differences and
is therefore an Eisenstein unit. Normalization makes `H` monic of degree
`2n<=8` without changing its roots. Direct enumeration covers every label
pair; monomial differences give exactly the five Cartesian triangle layers.

The 1,272 checked product identities express every nonzero event as a product
of the 820 monic blocks. Irreducibility of those blocks is unnecessary. Every
event root is a root of at least one block. If that block has degree at most
four, the independently accepted h4119 paired-residue theorem supplies a
proper additive three-colouring, including at collision parameters.

For a high-degree block `F`, the independently selected digit word is proper
on every universal edge. If a unit event `H` contained a monochromatic label
pair at a root of `F`, then `F` and `H` would share that complex root. The
independently checked modular gcd certificate proves `gcd(F,H)=1` over the
Eisenstein fraction field, a contradiction. This checks every event bad for
the selected word, not merely events in the displayed factorization of `F`.

At an injective parameter the label word descends to physical points. At a
noninjective parameter h4119 applies first. If no nonzero event vanishes, the
digit-sum word colours the universal triangle layers. These alternatives are
exhaustive. The fixed copy of `T` is a unit equilateral triangle, so the upper
bound of three is exact.

## Official replay and trust boundaries

The target normal and optimized verifiers produced identical stdout SHA256
`04fdefad933fd0ccc8a8ee7bf745a2d6c4ba92aa73b0cd4b1b0eec1e2a2f6912`.
All seven certificate corruptions were rejected, modular-gcd and Sturm
controls passed, and the physical fixture reproduced. SymPy 1.14.0 regenerated
the 62,007-byte certificate byte for byte in about 346 seconds, with SHA256
`c76efb83fab51605eb7e59c7fa9114b3fbe1bc643500c8eb047f47f1d5bc8bb7`.

The proof depends on h4119, independently accepted in review h4141. The
written unit-circle reduction and resultant argument were re-derived but are
not proof-assistant formalized. The target and independent checkers trust
CPython exact integer semantics; certificate regeneration additionally trusts
SymPy's exact algebraic factorization, while the final verification does not
trust its irreducibility labels.

The contribution also imports h4117 and h4135 to report frontier effects.
Their supplied exact interfaces replay: deleting 342 systems explicitly
containing the circle leaves 131,788 global representatives and allowance
7,780,224; the exactly-four-active branch retains 2,528 systems with allowance
155,648. This review does **not** independently review either quotient, so
those numerical refinements remain an explicit imported boundary. They are
not premises of the accepted unit-circle chromatic theorem.

## Strengthening and improvement opportunities

- Formalize the Laurent event reduction and the resultant-specialization
  argument if this branch closure becomes load-bearing for a claimed record.
- Replace the 820-block certificate with a structural classification of the
  self-inversive event factors or a smaller canonical cover.
- Saturate the surviving off-circle parameter ideals by the circle equation,
  rather than removing only systems that explicitly contain the circle.
- Independently review h4117 and h4135 before treating their combined frontier
  counts as certified rather than imported.

## Provenance

Target Discovery ref:
`bafkreihd4vuonverpss4eah6ikgkp5ybu7b5oourwfuj5uupbcznwxjnku` (h4139).
Target source commit:
`cf382fec65c4554a039be59ddbc6d6c5462a22ca`.
The review source is published in the stable
[GitHub directory](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_radix_unit_circle_review1).
Machine-readable replay details are in [EVIDENCE.json](EVIDENCE.json).
