# A complete negative test of mixed Moser and L10,2 direction sums

The exact finite support in this package has **84,643 vertices and 633,126
unit edges**, and its chromatic number is **four**. The saved colouring rules
out every five-chromatic subgraph of this support, including every candidate
on at most 508 vertices. This is a failed construction route for the record
objective, with complete geometric and colouring evidence.

The mechanism combines two different unit-direction palettes **before** taking
point sums. It permits all resulting geometric contacts. It is separate from
the earlier E477 monochromatic-pair spindle attachments and the team's fixed
Parts/H632 support work. The negative result applies to the finite set defined
below, not to arbitrary sum depth, rotations, the entire coordinate field or
all mixtures of these motifs. No record improvement or priority is claimed.

## Construction

Identify the plane with the complex numbers. Define four unit numbers

```
rho   = (1 + i sqrt(3))/2,
eta   = (sqrt(33) + i sqrt(3))/6,
sigma = (sqrt(6)+sqrt(2) + i(sqrt(6)-sqrt(2)))/4,
tau   = (sqrt(6) + i sqrt(3))/3.
```

Let

```
A = {rho^k eta^j : 0 <= k < 6,  -2 <= j <= 2},
B = {sigma^k tau^j : 0 <= k < 24, -1 <= j <= 1},
U = A union B,   U0 = U union {0}.
```

The palette sizes are |A|=30, |B|=72, |A intersect B|=6 and |U|=96. Each
vector has unit norm. The first two generators come from Moser-spindle edge
directions; the second two from the L10,2 construction. The generator pairs
and clipped-sum method are described separately in Section 6 of
[Voronov, Neopryatnaya and Dergachev](https://arxiv.org/html/2106.11824v4).
Here the tested construction mixes the two palettes at the outset. No theorem
about the chromatic number of their graphs is imported.

Use ordinary finite set addition, with coincidences deduplicated exactly:

```
P2 = U0 + U0,
D  = {p in P2 : |p| <= 1},
M3 = D + U0,
C8 = P2 union {q in P2+U : q has at least 8 neighbours in P2},
S  = M3 union C8.
```

A neighbour in the C8 rule means `q-p in U`. This explicitly defined
96-direction rule selects its vertices. **All** actual unit edges on S are
then included, whether or not their direction was used for selection. The
independent check finds that the final edge directions are exactly U.

| Set | Vertices | All unit edges |
|---|---:|---:|
| P2 | 4,609 | 20,202 |
| C8 | 5,233 | 27,240 |
| M3 | 84,487 | 630,594 |
| S | 84,643 | 633,126 |

The clip D has 1,537 points: 1,441 strictly inside the unit disc and the 96
unit vectors. P2 is contained in M3. C8 has 156 points outside M3; including
these in S checks their interactions with the entire clipped sum support.

Every point is in Q(sqrt(2),sqrt(3),sqrt(11))². A row has sixteen integer
coefficients: eight for x and eight for y, in the ordered radical basis

```
(1, sqrt(2), sqrt(3), sqrt(6), sqrt(11), sqrt(22), sqrt(33), sqrt(66)).
```

Divide each coordinate by 12. Lexicographically sort the rows of M3, then
append the lexicographically sorted rows of C8 outside M3. `colouring.txt`
gives one digit from 0 through 3 for each vertex in precisely this order.

## Proof and exact verification

The certificate is one proper four-colouring of **all** of S. Restricting it
to any subset, and deleting any edges, remains a proper colouring. Thus no
subgraph of this support can meet the five-chromatic target.

For the reverse bound, the verifier finds the seven points

```
0, 1, rho, 1+rho, eta², eta² rho, eta²(1+rho).
```

They form a Moser spindle. Each of the two diamonds forces its opposite
vertices to agree in any three-colouring, but their far endpoints are a unit
apart: `2*3*(1-5/6)=1`. The checked eleven edges therefore forbid a
three-colouring. Together with the positive four-colouring this proves
chi(S)=4. The final proof needs no SAT verdict or negative solver trace.

`generate.py` uses exact rational multiplication to enumerate A and B and
integer coordinate addition to construct the sets. Its clipping comparisons
use rigorous rational intervals; every unresolved boundary comparison must
be exactly unit norm or generation fails. The generator proposes edges by
hash lookup in the 96 declared directions.

`verify.py` independently checks every one of the **3,582,176,403** point
pairs. To make this feasible, a small C++ loop first rules out pairs using
rigorous integer intervals for their physical coordinates. For each radical,
`isqrt(d*Q²)/Q <= sqrt(d) <= (isqrt(d*Q²)+1)/Q`, with the upper endpoint
made exact when possible and Q=2²⁰. Signed coefficients are rounded outward. The stored interval endpoints
represent physical coordinates multiplied by 12Q.
The loop rejects a pair only when its squared-distance interval excludes 1.

The filter retains 634,718 pairs. A separate Python calculation expands exact
squared norms using `sqrt(r)sqrt(s)=gcd(r,s)sqrt(rs/gcd(r,s)²)`. It rejects
1,592 interval false positives and obtains exactly the 633,126 producer
edges. The verifier then checks every edge against the supplied colour word.
Point and edge hashes are pinned in the verifier. There is no floating-point
comparison in the public proof pipeline.

The native loop accepts interval endpoints only in [-10⁹,10⁹]. Differences
are at most 2*10⁹, squared terms at most 4*10¹⁸ and their sums at most
8*10¹⁸, below the signed 64-bit maximum. Input count, interval order,
missing or extra tokens, range bounds and output failures are checked.

The exact set-construction loops, radical-basis independence, Python integer
arithmetic, bounded native arithmetic and the written interval argument are
the trust boundary. The geometry verifier imports no producer multiplication
or edge-enumeration routine. The native filter is an acceleration of the
reference interval algorithm, not a second independent proof. No external
review or proof-assistant formalization is claimed.

## Reproduce

Use Python 3.11 or later, its standard library and a C++17 compiler. From this
directory:

```sh
mkdir -p out
c++ -std=c++17 -O3 -Wall -Wextra -Wpedantic -Wconversion \
  interval_pairs.cpp -o out/interval_pairs
python3 generate.py
python3 verify.py
python3 controls.py
sha256sum -c SHA256SUMS
```

`verify.py` prints the canonical result in `expected.json`; progress goes to
stderr. The recorded generator took about 18 seconds and the final exact
geometry check about 31 seconds. Generated points, edges and binaries stay
under ignored `out/`; they are intentionally omitted from the repository.
The roughly 85 KB positive colouring is the compact certificate.

Controls compare all 19,900 pairs of 200 interval fixtures with the Python
reference, including extreme signed-64-bit bounds, and reject ten malformed
native inputs. The same controls pass under address and undefined-behaviour
sanitizers. Further controls check all 96 unit-direction norms using separate
arithmetic, compare 13,041 pairs of a 162-point exact fixture, and reject five
malformed colour words. Normal and optimized Python controls agree.

Before using the native filter on S, its complete P2 output was compared with
the pure-Python reference at Q=2⁴⁰: both obtained exactly the same 20,202
unit edges across all 10,619,136 pairs. The reference also checked every C8
pair. It remains available in `reference_geometry.py`; applying it to the
full support is much slower and is not necessary for routine reproduction.

Optional discovery uses `python-sat==1.9.dev15` and bundled CaDiCaL 1.9.5:

```sh
python3 -m pip install python-sat==1.9.dev15
python3 search.py out/instance.json 300000
```

Exactly one colour is assigned to each vertex. Edge endpoints receive
different colours; three vertices of an actual triangle are pinned to 0,1,2,
which loses no colouring up to colour renaming. The full-support query found
a colouring in 2,087 conflicts, within the 300,000-conflict cap. The final
certificate is checked independently of this solver. Budget exhaustion is
reported as UNKNOWN, never as non-four-colourability.

## Decision and scope

The initial P2 and C8 tests, the full clipped sum M3, and their combined support
S are all closed by the saved colourings. The public S certificate alone
covers every one of these sets. No deletion order, radial threshold, direction
exponent or larger sum-depth sweep is warranted from this outcome; this exact
mixed-sum construction is retired for the record objective.

This does not determine the chromatic number of the infinite additive module
or of Q(sqrt(2),sqrt(3),sqrt(11))², and does not exclude different geometries.
It supplies useful negative evidence for this explicit combination of two
established motifs. The
[Parts paper](https://arxiv.org/abs/2010.12665) and
[Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4), checked
on 2026-09-07, retain 509 as the record comparison.

The earlier [E477 attachment closure](../hadwiger_nelson_e477_spindle_classification/README.md)
and HN2's [unpinned Parts-to-H632 map exclusion](../hadwiger_nelson_parts509_h632_one_collision/README.md)
are inspected coordination context, not premises. A later repository refresh
also found HN2's [complete near-injective planar realization classification](../hadwiger_nelson_parts509_plane_realizations/README.md); it concerns the fixed reduced
Parts source and does not restrict this mixed construction. The scoped graph refresh
through height 3620 found no new overlapping contribution. No subsequent
geometry phase was started.
