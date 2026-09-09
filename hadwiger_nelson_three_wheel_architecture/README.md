# Three unit-wheel sums: a finite 904,317-pair frontier

For the centre and six vertices W of a unit hexagon, consider the **complete
physical family** S(u,v)=W+uW+vW for all unit complex u,v. Each graph has at
most **343 distinct plane points**, with coincident labels identified and
all unit edges included.

**Every member is four-colourable outside an explicit finite set of at most
904,317 ordered rotation pairs.** Any non-four-colourable member must have
real Cayley parameters x,y with [Q(x,y):Q]<=16, and real coordinates in a
number field of degree at most 32. The exception set has not been isolated
into distinct real points or chromatically decided. This is a quantified
whole-architecture narrowing, not a record improvement or a complete closure.

The [proof](PROOF.md) consumes
[h4047's rotational-sum viability filter](../hadwiger_nelson_unique3_sum_viability/README.md)
and the [accepted H19+uH19 theorem](../hadwiger_nelson_hexagon_rotational_sums/README.md)
for degenerate pair alignments. It preserves the
[four-module](../hadwiger_nelson_four_module_synthesis/README.md) and
[A159 compression](../hadwiger_nelson_a159_module_compression/README.md)
obstructions; no source deletion audit is repeated. This family varies two
independent rotation angles. No larger hexagon or second construction source
is introduced in this milestone.

The decisive certificate is a **thirteen-word colouring cover**: four F3
product sign colourings from h4047 and nine linear F4 colourings. Every one
of the 988 unit-event factor graphs has a proper word. Simultaneous failure
of all thirteen words occurs only in a finite algebraic set. A checked cover
by 71,134 coprime factor pairs bounds that set by 902,481 points; a conservative
allowance of 1,836 triple-collision points gives the stated total. Entire
pair-collision lines are covered by the accepted H19 theorem.

## Reproduce the exact check

From the repository root with CPython 3.11.2 and the standard library:

```bash
python3 -B hadwiger_nelson_three_wheel_architecture/verify.py --check-expected
python3 -O -B hadwiger_nelson_three_wheel_architecture/verify.py --check-expected
```

The [31,680-byte certificate](certificate.json) contains integer factor
coefficients and multiplication identities. SHA-256:
`7d3813350faffa9e6710cddc44d528a93ece7a1405db28c799974afd38c96e49`.
Its factors use coefficient order x^i y^j, with i outer and j inner, both
ranging from 0 to 2. Factorization rows follow the lexicographically sorted
primitive-normalized F polynomials regenerated from the 1,144 displacement
orbits. The identically zero polynomial has an empty factor row.

The verifier checks:

- All 1,064 factorization identities against a separate squared-distance
  derivation, with exact integer arithmetic.
- Coprimality of all 487,578 active factor pairs by a modular proof. Every
  actual pair succeeds modulo 101; no CAS irreducibility claim is trusted.
- All thirteen words against every one of the 58,653 label pairs, together
  with complete event coverage and the finite intersection bound.
- Two exact physical 343-point graphs: a 1,764-edge three-chromatic graph,
  and a 1,848-edge four-chromatic graph containing a Moser spindle.
- Malformed factorization rejections and controls for shared factors,
  vertical factors, bad specializations and a bad first prime.

The detailed receipt is [EXPECTED.json](EXPECTED.json). No SAT solver,
computer algebra package, floating-point predicate, omitted proof trace or
unpublished graph data is required for verification. The written use of
Bezout's theorem, the inherited h4005/h4031 result and the h4047 layer argument
remain explicit mathematical dependencies. Author-run independent checks
are not reviewer-1 acceptance or proof-assistant formalization.

## Optional factor regeneration

With `sympy==1.14.0` installed in the selected Python environment:

```bash
python -B hadwiger_nelson_three_wheel_architecture/produce.py \
  --out /tmp/hn-three-wheel-factors
python3 -B hadwiger_nelson_three_wheel_architecture/verify.py \
  --certificate /tmp/hn-three-wheel-factors/certificate.json
```

The output directory must be new. The public producer regenerated the
certificate byte for byte in about seven seconds on the recorded run.
It uses exact factorization in ZZ[x,y]; the checker independently verifies
the identities and coprimality. An exploratory 54-query SAT pilot found
four-colour witnesses before the formula cover was extracted; none of those
solver answers or words is needed for the final result. Provenance is in
[DISCOVERY.json](DISCOVERY.json), with validation in [VALIDATION.json](VALIDATION.json).

## Exact frontier interface

After the proof check, export the equations locally:

```bash
python3 -B hadwiger_nelson_three_wheel_architecture/export_frontier.py \
  --out /tmp/hn-three-wheel-frontier
```

This regenerates the 71,134 factor pairs, thirteen failure-factor sets and
972 triple-collision displacement rows. The expanded interface is generated
state and is not committed. The exporter performs no root isolation or
chromatic solving. The [HN-3 handoff](HANDOFF.md) specifies the next exact
viability interface and leaves physical candidate construction with HN-2.
The current milestone stops at this finite architecture boundary.
