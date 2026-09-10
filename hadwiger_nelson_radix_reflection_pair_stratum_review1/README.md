# Independent review of the A5 reflection-stabilized pair stratum

Verdict: **ACCEPT with high confidence** for the standalone h4191 theorem:
every physical member of the 2,232 named A5 pair systems whose pair stabilizer
contains a reflection is exactly three-chromatic. The selection, unique
rotation normalizations, complete algebraic covers, component colour words,
and all 6,696 D3-expanded pair exclusions reproduce independently.

I also accept the deletion of exactly 2,232 rows from the pinned h4185
interface. The resulting pair/orbit allowance totals remain **conditional**:
they are exact transformations of that interface and retain its unreviewed
h4177, h4117, and h4175 trust boundary. The 2,291 chart records may overlap and
are not a count of distinct physical parameters.

This is an intermediate exclusion, not the campaign target. It constructs no
non-four-colourable graph and does not improve the 509-vertex record. It leaves
128,700 global pair systems, including four rotation-only systems that h4191
explicitly preserves. The later h4193 decision of those four systems is not
part of this review milestone.

## Why h4191 was selected

At selection time the only new committed claims were h4191 and its downstream
h4193 refinement. h4191 is load-bearing: it closes 2,232 canonical systems and
6,696 symmetry images, whereas h4193 closes four rows and explicitly depends
on h4191. No new R(5,5) contribution had been committed. h4191 had no incoming
independent review or reproduction.

## Independent symmetry and selection audit

The reviewer checker imports no h4191 module. It imports only the earlier
reviewer h4181 curve reconstruction, pinned by SHA-256
`5a3804b9e39e55686fd2ffa377f7bc60323b46c33c45f88f16076fe529a3de23`.
That source reconstructs all 2,797 A5 unit-event curves directly from the
`7^5-1` nonzero digit-displacement rows over the Eisenstein integers and is
independent of h4191's h4163 inventory import.

From the digit action, the checker rebuilds multiplication by `omega^2` and
conjugation on every curve ID, verifies the six-element D3 group, and checks
every submitted pair orbit. For each of the 2,232 rows it verifies:

- the pair is the canonical D3 representative;
- its stored stabilizer mask is exact, has order two, and contains a
  reflection;
- its Bezout/product allowance fields agree with the curve degrees;
- exactly one of the three rotations makes both curves individually fixed by
  conjugation; and
- multiplying each normalized displacement polynomial by the conjugate of
  its first nonzero coefficient gives coefficients in `{-1,0,1}`.

This yields 112 distinct real-coefficient norm curves. The complete
normalization and expanded-orbit digests match h4191 exactly:

```text
normalizations  718f835ae027a1906fae3c33cd9e39d81f1afd02aa169d41072af595dfd4b553
expanded pairs  49b59ab8ac504f3ccb5821661f26826d0b77abf661fbb3ac7ac6142dc43cf059
```

For the frontier check, I used the h4185 interface freshly regenerated during
the preceding independent review, not an h4191-produced table. Selecting
exactly the rows whose mask contains a reflection gives 1,760 inherited
exact-five rows and 472 already-at-least-six rows. The four rotation-only rows

```text
(318,340), (318,341), (319,340), (319,341)
```

remain present, confirming that the author's corrected 2,232-row intake is
complete and does not silently consume the downstream h4193 stratum.

## Independent algebraic cover

For a normalized real-coefficient polynomial
`P(z)=sum_j a_j z^j`, the checker does not use h4191's power-trace recurrence.
It writes

```text
z = x + i*sqrt(3)*y,  D = 3*y^2,
z^j = A_j(x,D) + i*sqrt(3)*y*B_j(x,D)
```

and advances the independent recurrence

```text
A_(j+1) = x*A_j - D*B_j,
B_(j+1) = A_j + x*B_j.
```

Thus `|P|^2-1 = A^2+D*B^2-1`. Substitution of
`x=(u-r)/2` and `D=r-x^2` gives equations in the author's chart variables
`u=trace+radius` and `r=radius` by a different derivation.

For every normalized pair, python-flint's multivariate resultant eliminates
`r`. This differs from h4191's reviewer-facing custom Sylvester/Bareiss
determinant, while the author producer uses SymPy Gröbner bases. Every
resultant factor product is checked. A reviewer-written Euclidean algorithm in
`Q[u]/(q)` inverts a leading coefficient only after checking an explicit
extended-gcd unit identity. Nonlinear fibres occur only over rational `u` and
are factored and substituted back directly. Every standard and exceptional
chart is substituted into both original norm equations.

Entry-level reconstruction gives exactly:

```text
source pair systems                         2,232
distinct algebraic chart records            2,291
pair/chart incidence slots                  3,903
empty / linear / quadratic / cubic fibres   118 / 3,778 / 66 / 10
```

The complete component and pair-cover hashes match the certificate. The
independent eliminant inventory is
`79692a62a6048f688761be7cdc388e181687450e3662f5cf6f63748801ad0c9c`,
also exactly matching h4191. Resultant factors need not be trusted as
irreducible: every division is justified by a checked unit identity.

## Independent colour proof

The checker enumerates all 29,403 unordered digit-label pairs and assigns each
one directly to a universal edge or a reconstructed displacement event. It
does not import h4191's projected-curve inventory. For every one of the 26
submitted F3 weight words that is actually used, all universal edges are
properly coloured.

For a general event polynomial `F(x,y)=E(x,y^2)+y*O(x,y^2)`, an event at a
physical point would force

```text
E^2 - y^2*O^2 = 0.
```

The checker substitutes the independently derived chart functions and tests
this necessary event polynomial in `F_1000003[u]/(q)`. It verifies the prime,
all parameter degrees, and all rational denominators. A gcd of one makes
multiplication by the event polynomial invertible modulo the prime, hence its
determinant is nonzero over `Q`; the event cannot occur at a characteristic-zero
chart root. This argument requires neither factor irreducibility nor a sampled
real-root list.

All **1,265,523** component/projection unit checks pass. Therefore every actual
unit edge on every algebraic chart is properly coloured. Selecting one label
representative for each physical point handles any collision, and the
permanent triangle `0,1,omega` proves the lower bound three. This establishes
chromatic number exactly three for every physical member of the named
stratum—including additional active curves not named by the source pair.

## Independent physical fixture

The quartic fixture is independently recognized as component 1000 in the
complete chart set and as a component of source pair `(27,1257)`. A custom
rational Sturm implementation proves that

```text
q(u) = 3*u^4 - 3*u^3 + 22*u^2 - 5*u - 8
```

has exactly two real embeddings, one in each stated interval. Its reduction
modulo seven has no linear or quadratic factor, so the quartic is irreducible
over `Q`.

The checker then rebuilds all 243 coordinates in the Cartesian extension
`Q[u]/(q)[y]/(y^2-D)` using only `Fraction` polynomial arithmetic. It tests all
29,403 unordered pairs at each embedding and searches the 81 normalized F3
weight words rather than trusting the fixture word. The first common word
found is `(1,0,1,1,2)`. The exact results are:

| embedding | vertices | unit edges | active curves |
|---|---:|---:|---|
| negative `u` | 243 | 378 | 170, 257, 1873, 2133, 2792 |
| positive `u` | 243 | 378 | 86, 257, 1928, 2133, 2791 |

Both edge hashes match the independently regenerated physical certificate.
This fixture is corroboration and a concrete new physical example; the
universal theorem rests on the chart-wide colour audit above.

## Submitted replay and fresh generation

Using CPython 3.11.2, python-flint 0.8.0, and SymPy 1.14.0:

```text
target verifier, ordinary                 370.4 s
target verifier, optimized                444.8 s
seven target corruption controls           30.2 s
target physical verifier, ordinary/opt    8.8 / 8.8 s
fresh independent Gröbner producer         213.9 s
reviewer checker, ordinary/optimized      603.1 / 625.3 s
```

The 47,105-byte main certificate and 16,641-byte fixture regenerated
byte-for-byte:

```text
main      b561346fe17e07bf1b362611414d7b00c7bb3aae1f4ede096800f2cbf9a21953
physical  8322a08a8b6bfda7fc0c0a4c63fcda382f28a4a8121a13c28b49cfbf4745f68b
```

The target controls rejected a wrong colour, modular degree loss,
zero-divisor inversion, a composite modulus, an incomplete cover, a false
physical coordinate, and an omitted real embedding. Ordinary and optimized
reviewer runs have identical mathematical output; timings are excluded from
the expected comparison.

From the repository root, first regenerate the h4185 `target-frontier.json` as
documented by the preceding anchor review, placing the multi-megabyte interface
under reviewer scratch. Then run:

```sh
python3 -B hadwiger_nelson_radix_reflection_pair_stratum_review1/independent_check.py \
  --frontier /scratch/research-team-v2/tmp/reviewer-1/h4185-review/target-frontier.json \
  --check-expected --progress
```

The transient h4185 input and 2.39 MB h4191 residual interface are not
committed. The public contribution contains only source and compact expected
evidence.

## Trust boundaries

The standalone theorem trusts CPython arbitrary-precision integer and
`Fraction` arithmetic, SymPy 1.14.0 for symbolic expression construction,
python-flint 0.8.0 for exact polynomial resultants/factorization, the pinned
reviewer h4181 curve inventory, inspected exhaustive-loop coverage, and the
modular determinant argument. It uses no floating point, random search, or
solver verdict and is not proof-assistant formalized.

FLINT factorization is not accepted as an irreducibility oracle: exact factor
products, direct substitutions, and unit identities carry the proof. The
reviewer geometry shares FLINT as an arithmetic library with the target but
uses FLINT's multivariate resultant on independently derived equations rather
than the target's custom determinant; the author's separate producer uses
SymPy Gröbner bases. This shared native-library boundary is explicit.

The complete 2,232-row selection is accepted relative to the pinned,
previously reviewed h4185 interface. The global pair and allowance totals
additionally inherit h4177, h4117, and h4175, which remain unreviewed here.
HN3's h4187 overlap audit is compatible author-side corroboration but is not
needed for the standalone theorem and is not treated as independent evidence.

## Strengthening and improvement opportunities

- Independently review h4175/h4177 and ultimately h4117 before promoting the
  downstream pair/orbit allowance totals to unconditional status.
- Publish a compact batch unit certificate or product tree for the 1.26
  million colour-obstruction checks; the current direct replay is exact but
  takes about ten minutes.
- Formalize the resultant-cover lemma and modular-unit implication in a proof
  assistant, leaving only compact polynomial identities as external data.
- Propagate the 6,696 pair exclusions through the remaining pencil and
  higher-incidence frontier; h4191 intentionally claims no new mode moves or
  pencil census.
- Review h4193 separately before accepting the claim that every remaining
  pair stabilizer is trivial.

## Provenance

Target Discovery ref:
`bafkreie5w6pudf4bh52i3ltb6yhewzuizcquca4jj7hupvwd46wzwytdgy` (h4191).
Target source commit:
`36657746aa40fac0f7af517c76b847682ffaf808`.

Target source and proof:
[directory](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_radix_reflection_pair_stratum),
[PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/hadwiger_nelson_radix_reflection_pair_stratum/PROOF.md).
Machine-readable review results are in [EVIDENCE.json](EVIDENCE.json).
