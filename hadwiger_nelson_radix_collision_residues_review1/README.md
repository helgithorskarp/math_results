# Independent review of collision closure by paired residues

**Verdict: ACCEPT with high confidence for the reusable degree-four theorem
and its complete noninjective-architecture corollary.** If
`z` satisfies a monic polynomial of degree at most four over
`E = Z[(1+i sqrt(3))/2]`, the strict unit-distance graph on `E[z]` has an
additive proper three-colouring. Consequently every noninjective physical
member of

```text
A5(z) = T + zT + z^2 T + z^3 T + z^4 T,
T = {0,1,(1+i sqrt(3))/2},
```

has chromatic number exactly three.

This closes the collision branch of the complex-radix architecture. It is not
the target Hadwiger--Nelson breakthrough: it produces no five-chromatic graph,
does not decide the injective frontier, and does not improve the 509-vertex
record.

## Independent reconstruction

[independent_check.py](independent_check.py) imports neither the target code
nor its certificate. It uses different irreducible presentations for both
exceptional fields and searches every nonzero linear functional from scratch.
It independently:

- factors all 120 monic polynomials over `F3` of degrees one through four;
- obtains the irreducible census `(3,3,8,18)` and all 16 ordered residue types;
- checks all 24,546 unordered vertex pairs across those 16 Cayley graphs;
- finds a proper `F3`-linear three-colouring in every case;
- realizes the norm case in
  `F3[x]/(x^4+x^3+2x^2+2x+2)` with functional `(1,0,2,2)`, yielding
  81 vertices and 405 edges;
- realizes the hyperbola case in `F3[x]/(x^2+2x+2)` with functional
  `(0,1,1,1)`, yielding 81 vertices and 324 edges; and
- enumerates all 29,403 unordered pairs of the 243 digit words directly,
  recovering 2,400 normalized nonconstant collision polynomials, degree sum
  9,204, and maximum degree four. The additional normalized constant
  polynomial is explicitly separated because it has no root.

Run from the repository root with CPython 3.11 or later and only the standard
library:

```sh
python3 -B hadwiger_nelson_radix_collision_residues_review1/independent_check.py
python3 -O -B hadwiger_nelson_radix_collision_residues_review1/independent_check.py
```

Both commands must exit zero. On CPython 3.11.2 their complete stdout SHA256
is
`ecc653c4470decb69e5d9a9dc02bfae5520a92b2ed02427a472b40394da364e0`.

## Written-proof audit

Let `R=E[z,conjugate(z)]`. A monic degree-`d` relation for `z` and its
conjugate relation for `conjugate(z)` make `R` a finite, torsion-free
`Z`-module spanned by at most `2d^2` standard monomials. Every element of `R`
is an algebraic integer, so `1` is not in `3R`; hence `R/3R` is a nonzero
finite ring. A residue field of this ring gives a unital map `rho:R -> F` of
characteristic three.

In characteristic three,
`omega^2-omega+1=(omega+1)^2`, so `rho(omega)=-1`. A coefficient and its
complex conjugate therefore have the same residue. Thus
`alpha=rho(z)` and `beta=rho(conjugate(z))` satisfy the same reduced monic
polynomial `p` over `F3`. The map

```text
v |-> (rho(v), rho(conjugate(v)))
```

is well defined on actual complex points, not labels. A unit difference
`delta` maps to `(a,b)` with `ab=rho(delta*conjugate(delta))=1`, so it cannot
become a loop. This is the load-bearing bridge that makes the colouring
descend through arbitrary collisions.

If `alpha` and `beta` have the same irreducible minimal polynomial of degree
`r`, then `beta=alpha^(3^k)` and the connection set is
`{a:a^(1+3^k)=1}` in `F_(3^r)`. If their minimal polynomials differ, the
polynomial Chinese remainder theorem gives
`F_(3^r) x F_(3^s)`; the unit equation forces `a` into the intersection
`F_(3^gcd(r,s))` and the connection is `(a,a^-1)`. Distinct factors obey
`r+s<=4`. These alternatives give exactly the 16 cases checked independently.

Finally, a collision of two digit words gives a nonzero degree-at-most-four
polynomial whose leading nonzero coefficient lies in the six units `T-T`.
After dividing by that unit it is monic. For nonzero `z`, initial zero
coefficients may be removed; `z=0` already satisfies the monic relation `X`.
The theorem applies to the entire physical quotient. The unchanged copy of
`T` is a unit equilateral triangle, proving the matching lower bound of three.

## Official replay and imported boundary

The target normal and optimized verifiers produced identical output SHA256
`7a6ae22d13136bbf80330b43476854c2f1a2ba36a931101cc77ce74affda5bc8`.
The regenerated certificate was byte-identical with SHA256
`7205fb23b0b81ac87c35b2fb29dd11b0f64ae694992b302a90ea8d832dd4601a`.
All ten malformed-certificate controls were rejected and four exact physical
collision fixtures passed.

The target also carries forward h4117's D3 figures: 442 collision-polynomial
orbits with allowance 1,682 are removed, leaving 132,130 pair-system orbits
and Bezout allowance 7,785,424. Its official exact verifier reproduced those
figures. This review does **not** independently re-review the D3 quotient, so
those numerical refinements remain an explicit imported trust boundary. They
are not needed for the accepted collision theorem or the assertion that every
noninjective member is exactly three-chromatic.

The proof bridge was re-derived manually but is not proof-assistant
formalized. Both computational implementations trust CPython's exact integer
semantics; the independent checker replaces the finite-field presentations,
colour searches, graph construction, and collision enumeration.

## Strengthening and improvement opportunities

- Formalize the integral reduction, paired-residue homomorphism, and the
  finite-field case split if this theorem becomes a premise of a claimed
  record construction.
- Replace the two exceptional finite searches with a uniform structural
  description of all linear functionals avoiding the connection subgroups.
- Apply the monic degree-four filter to the injective pair-system frontier and
  retain exact annihilating-polynomial certificates for every removal.
- Independently review h4117 before treating its D3 orbit counts as certified
  rather than imported.

## Provenance

Target Discovery ref:
`bafkreifm45kpihmk544icvvwlqaidzbtzea53uggbgvoks5wma4c22aihu` (h4119).
Target source commit:
`3ffe4fdba4fbd79868b2ff8bcf8c7c214f816294`.
The review source is published in the stable
[GitHub directory](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_radix_collision_residues_review1).
Machine-readable replay details are in [EVIDENCE.json](EVIDENCE.json).
