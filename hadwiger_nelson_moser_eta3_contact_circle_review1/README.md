# Independent review: the eta-cubed Moser contact circle

## Verdict

**ACCEPT with high confidence** at mathematical target commit
`b638e1b31f53afc986e3be1fdd125bdbc524157d`. The reviewed package is
[`hadwiger_nelson_moser_eta3_contact_circle`](../hadwiger_nelson_moser_eta3_contact_circle/README.md).

For the displayed seven-point Moser spindle `M`, put

```text
eta = (5+i*sqrt(11))/6,       u = eta^3.
```

For every unit complex number `v`, the complete strict plane unit-distance
graph on the set of physical points

```text
M + uM + vM
```

has chromatic number exactly four. The same conclusion holds for
`u=eta^-3`. This is a universal theorem on two one-dimensional phase circles,
not an angle sample.

The scope is nevertheless restricted. It eliminates these two fixed-first-
phase circles from one particular three-Moser construction architecture. It
does **not** close the remaining two-parameter phase torus, construct a
five-chromatic graph, improve a global lower bound, or improve the published
509-vertex plane unit-distance record.

## Mathematical audit

The algebraic reduction and all finite exceptional cases were independently
checked.

1. In the alternate representation
   `E=Q(sqrt(33))[alpha]/(alpha^2+3)`, the checker reconstructs
   `eta^3=(-5+8*i*sqrt(11))/27` and proves by exact enumeration that
   `B=M+eta^3 M` has 49 distinct points. All points of `B` and `M` are
   integral in the selected unramified 2-adic completion.
2. If `v` is in `E` and has complex norm one, conjugation preserves the local
   valuation and `v*conj(v)=1`, so `v` is a local unit. Every physical point is
   integral and reduction modulo the maximal ideal gives a proper `F_4`
   colouring, including collision phases. If `v` is outside `E`, the map
   `B x M -> B+vM` is injective. With no mixed contact, the residue-sum word
   properly colours all 1,617 Cartesian edges; the checker verifies every one.
3. A mixed edge has nonzero differences `a in B-B`, `b in M-M` and satisfies
   `N(a+vb)=1`. With `c=conj(a)b` and
   `S=N(a)+N(b)-1`, this is exactly
   `c v^2+S v+conj(c)=0`. An outside-field root therefore has the unique monic
   polynomial `v^2-Tv+J`, where `T=-S/c` and `J=conj(c)/c`. Thus all contacts
   at that phase, and only those contacts, share the same exact `(T,J)` key.
4. The clean-room program classifies all 1,224 nonzero `B` differences times
   all 34 nonzero `M` differences directly, without the target's norm-shape
   cache. It independently obtains 38,844 locally closed directions, 816 with
   nonpositive discriminant, and 1,956 event directions. The last group into
   922 irreducible quadratics with 134 radicands. Its complete serialized
   inventory SHA-256 is exactly the target value
   `39afe794...c0b09`.
5. For each quadratic, the checker constructs both physical roots
   `T/2 +/- alpha*sqrt(Delta/3)/(2c)`, proves the unit and minimal-polynomial
   identities, constructs all 343 distinct physical points, and compares every
   pair with the direction-key graph. The metric kernel was newly written in
   the alternate basis and imports no target code. Both roots agree in every
   case: 108,156,132 unordered pair tests in total.
6. All 922 assigned positive words are directly checked. Their edge histogram
   and complete edge-stream hash match the target. The eleven-edge Moser
   spindle is verified non-three-colourable and four-colourable, so every
   support has chromatic number exactly four, not merely at most four.
7. The exact identity `(eta*rho)*conj(M)=M` sends the `eta^3` circle to the
   `eta^-3` circle and preserves the free unit phase, establishing the stated
   conjugate case.

The trace-valuation exclusions and the fact that a positive real-subfield
element square in `E` is already a real-subfield square are dependencies of
the parent collision theorem. They were not silently assumed here: this
review pins the source of the earlier independent acceptance, which separately
audited the Hensel/conjugation argument and these field reductions.

## Reproduction and source integrity

The author verifier was run completely under its normal optimized build and
again with undefined-behaviour sanitization and Python assertions disabled.
Both runs reproduced `expected.json` byte-for-byte and checked the target's two
exact metric formulas over all 108,156,132 pairs. The manifest passed.

The 40,974-byte positive certificate has SHA-256
`3dae836a7c05791df98e24ab19bd6b7cb56a5dbad89c8b2a6c08b0e929676bdd`.
Regeneration with the target's pinned PySAT 1.9.dev15/CaDiCaL 1.9.5 stack was
byte-identical. Solver behavior is not a theorem premise: both target and
review check the resulting words directly.

The independent checker imports no code from the reviewed package. Its normal
and sanitized executions were byte-identical. Besides the full alternate-
basis geometry census, it performs 3,688 Python-fraction metric spot checks,
1,617 residue-colouring checks, 1,844 damaged-word rejections, four malformed-
certificate checks, and signed-128-bit range accounting. The largest guarded
input is 321,968,547, the largest denominator is 99,944,928, and a conservative
bound puts every native intermediate below 2^101, far below 2^127.

Run the complete independent replay from this directory:

```sh
./reproduce.sh
```

It requires CPython 3.11+, g++ with C++17 and undefined-behaviour sanitizer
support, and the two hash-pinned sibling directories already in this
repository. No SAT package is needed for independent verification.

## Trust boundary and campaign context

The continuum reduction and local-field argument are written mathematics, not
proof-assistant formalizations. The review replaces the target inventory and
metric implementations, but deliberately reuses the hash-pinned arithmetic
from the accepted independent review of the parent theorem. The certificate is
shared data, not shared executable code. Ordinary Python/C++ semantics and the
compiler remain trusted.

The pre-publication refresh inspected repository main through
`852529c3c6ffc82aad399367119b604c3cb5b164`, including the newly landed
origin-anchored Parts affine-frame gate. That finite deformation exclusion is
a different restricted lane and does not supersede this continuum review.
Discovery Net's committed index remained stale at height 4,363 while the RPC
node remained at height 4,364; the target and recent team submissions are
therefore reported as pending, never as committed.

Record calibration uses Parts,
[*Graph minimization*](https://arxiv.org/abs/2010.12665). Haugland's
[2026 construction](https://arxiv.org/abs/2608.04542) has 2,131 vertices under
the additional Moser-spindle-free restriction and does not supersede the
unrestricted 509-vertex benchmark.
