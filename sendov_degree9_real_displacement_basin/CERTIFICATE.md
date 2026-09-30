# Complete rational cube certificate

Author **six-sendov-2**, role **researcher**, 2026-09-30.
Notation and cleared numerator/denominator are in PROOF.md, (12)--(13).

All boxes below have three nonzero rational side lengths. For each
polynomial the checker determines its coordinate degrees, makes the exact
affine substitution to the unit cube, and converts power coefficients to
the full tensor Bernstein basis. Every coefficient, including zeros, is
checked. A separate inverse binomial transformation reconstructs the
complete normalized power polynomial. Thus no sampled value or supplied
large certificate is a proof input.

## Low middle slope

Let \(x=X\), and use the two charts (14). Remove exactly \(x^2h^2\)
from \(780D-N\); divisibility and multiplication back to the original
polynomial are both checked. Each resulting polynomial has degree
\((12,10,8)\), giving **1,287 coefficients per box**.

For the first chart, the nine boxes are:

| Record | \(x\) | \(h\) | \(k\) |
|---|---|---|---|
| low0_0 | \([0,3/8]\) | \([0,1/2]\) | \([0,1]\) |
| low0_1 | \([0,3/8]\) | \([1/2,1]\) | \([0,1]\) |
| low0_2 | \([3/8,3/4]\) | \([0,1/2]\) | \([0,1]\) |
| low0_3 | \([3/8,9/16]\) | \([1/2,3/4]\) | \([0,1]\) |
| low0_4 | \([3/8,9/16]\) | \([3/4,1]\) | \([0,1/2]\) |
| low0_5 | \([3/8,9/16]\) | \([3/4,1]\) | \([1/2,1]\) |
| low0_6 | \([9/16,3/4]\) | \([1/2,3/4]\) | \([0,1]\) |
| low0_7 | \([9/16,3/4]\) | \([3/4,1]\) | \([0,1/2]\) |
| low0_8 | \([9/16,3/4]\) | \([3/4,1]\) | \([1/2,1]\) |

For the second chart, take the four products of
\(x\in[0,3/8]\) or \([3/8,3/4]\),
\(h\in[0,1/2]\) or \([1/2,1]\), and \(k\in[0,1]\).
Record order is increasing \(x\), then increasing \(h\), with names
low1_0 through low1_3. These explicit boxes partition each chart domain.

Every coefficient is nonnegative. There are 27 zeros in low0_0 and
126,110 zeros in low1_0,low1_1; all other entries are positive. Zero
coefficients do not invalidate a nonnegativity certificate. Generic
density and the credited spectral continuity handle points where the
original denominator or a removed factor vanishes.

## Large smallest slope

Use (15), with coordinate order \((d,x,s)\). Remove \(d^6x^2\)
from \(780D-N\), then substitute either corner chart (16) and remove
\(h^2\). The coordinate order becomes \((d,h,k)\); the box in both cases
is \([0,3/4]\times[0,1]^2\).

| Record | Degree | Entries | Minimum |
|---|---|---:|---:|
| high0 | \((8,16,8)\) | 1,377 | \(7893099/4096\) |
| high1 | \((8,16,10)\) | 1,683 | \(7893099/4096\) |

All coefficients are strictly positive. The two charts cover the square
in \(x,s\) by ordering \(1-x\) and \(1-s\). The factor identities and
both reconstructions are exact polynomial equalities.

## Competitive cap and scalar reproduction

Use (17), with coordinate order \((t,s,u)\). Remove \(t^2\) from both
\(N,D\), giving \(N_2,D_2\), and remove \(t\) from
\(j_ND_2-j_DN_2\). All 990 coefficients of the quotient are positive
on \([0,1/4]\times[0,1]\times[0,1/4]\). The degree is \((9,8,10)\),
and the minimum is \(34642049301/1146880\). The exact scalar denominator
and interlacing bounds in PROOF.md turn this into \(j(u)-J\ge(1-X)/2\).

The additional six coefficients of the credited scalar reproduction
\(-[T'(u)+90000]\) on \([0,1/4]\) are positive, with minimum \(141084\).
The checker verifies \(j'=T/j_D^2\), the exact rational competitor
\(j(1/9)=5472/7\), 40 rational root-bisection steps and an exact interval
Horner enclosure of the previously known \(B_*\). The scalar maximum
and the weaker sufficient \(450\) quadratic loss retain their predecessor
attribution; these extra checks do not claim a new one-variable theorem.

## Counts, hashes and trust boundary

There are **16 cube boxes and 20,781 cube coefficients**, plus six scalar
reproduction coefficients, totaling 20,787. The manifest reports 21,431
exact checks and nine rational grouped-spectral controls. It records the
degree, entry count, zero count, exact minimum, complete polynomial hash
and complete coefficient hash for every box.

Manifest coefficient-record SHA256:

```text
0a00cbd17d1ee8b0cc22a03c10933a443881a92473f06d7e821400b09ab7557b
```

Hashes identify regenerated data; each sign is actually checked and each
polynomial is reconstructed. The entire expected.json object is compared,
including controls and interval results. `python -O` keeps every guard.
The optional `--write-expected` mode regenerates a fixture only after
all proof checks pass; ordinary verification always requires and compares
the complete fixture. Missing, altered or truncated fixtures fail.

The commutant controls use rational Gaussian elimination with nonzero
pivots, check every original commutation equation after rank selection,
and check Frobenius orthogonality. Generic samples compare the cubic
oracle to the definition. Singular samples use the definition directly;
zero generic denominators are never evaluated. These finite controls are
not the universal coverage proof.

The small sparse kernel and projection method adapt the author's earlier
published code openly. The separable conversion and inverse reconstruction
are distinct exact basis calculations, not an independent peer review or
formalization. The mathematical coverage, collision continuity, interlacing
and all-real displacement bridge remain ordinary written arguments.
