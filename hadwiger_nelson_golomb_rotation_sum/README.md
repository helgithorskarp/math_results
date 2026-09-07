# Every rotational self-sum of the Golomb graph is four-chromatic

Let `G` be the exact ten-point Golomb graph defined below. For every complex
number `u` with `|u|=1`, form the point set

```text
S(u) = {g_i + u*g_j : 0 <= i,j < 10},
```

identifying coincident points and including every actual unit edge.

**Exact result.** The strict unit-distance graph on `S(u)` has chromatic
number exactly four for every `u` on the unit circle. It has between 46 and
100 vertices and between 141 and 372 unit edges. Thus this complete
construction family lies below the campaign's 508-vertex target but produces
no five-chromatic graph.

This is a two-factor rotational composition of a different four-chromatic
atom. It does not extend the retired T375 completion source or classify the
three-Moser-spindle sums previously studied by HN-2. No record or priority
claim is made.

## Exact Golomb atom

A row `(a,b,c,d)` represents

```text
(a + b*sqrt(33))/36 + i*sqrt(3)*(c + d*sqrt(33))/36.
```

The ten rows, in fixed order, are

```text
(  0, 0,  0, 0)
( 36, 0,  0, 0)  ( 18, 0, 18, 0)  (-18, 0, 18, 0)
(-36, 0,  0, 0)  (-18, 0,-18, 0)  ( 18, 0,-18, 0)
(  6, 0,  0, 2)  ( -3,-3,  3,-1)  ( -3, 3, -3,-1)
```

Geometrically these are the centre and six vertices of a regular unit
hexagon, followed by the three rotations through 120 degrees of

```text
q = (1 + i*sqrt(11))/6.
```

The final three points form a unit equilateral triangle; they attach to
alternate vertices of the hexagon. Exact expansion of all 45 squared
distances gives 18 unit edges.

This graph is not three-colourable. Pin the centre and two consecutive outer
vertices to three distinct colours. The outer six-cycle must alternate the
two colours not used by the centre, so the three alternate attachment
vertices have one common colour. The inner triangle uses all three colours,
and one inner vertex then conflicts with its attachment. The verifier also
exhausts all `3^7 = 2,187` assignments after the pin. A checked four-colouring
gives the matching upper bound.

For every `u`, the addresses `(i,0)` are the ten distinct points `g_i` because
`g_0=0`. Their 18 edges remain present. Consequently every member of the
rotational family contains a copy of `G` and needs at least four colours,
even when other addresses collide.

## Finite reduction of the whole unit circle

Write a formal address as `(i,j)` and compare two addresses. Their difference
has the form

```text
a + u*b,
```

where `a` and `b` are differences of Golomb points. Put

```text
K = Q(sqrt(33)),
a = ax + i*sqrt(3)*ay,
b = bx + i*sqrt(3)*by,
conjugate(a)*b = p + i*sqrt(3)*q,
```

with every displayed coefficient in `K`. For `u=x+i*sqrt(3)*y`, the unit
or collision condition is a line

```text
2*p*x - 6*q*y = target - |a|^2 - |b|^2,
x^2 + 3*y^2 = 1,
```

where `target` is one for a unit edge and zero for a collision. A nonconstant
condition therefore has at most two orientations. The certificate producer
enumerates all 4,950 formal address pairs, intersects every normalized line
with the unit circle exactly, and groups all lines meeting at the same
`K`-valued point. If a secant has roots outside `K`, no distinct `K`-line can
share either root: two distinct lines over `K` would have a `K`-valued
intersection. Its two roots consequently have the same event set.

This gives 432 real event lines. Their exceptional orientations consist of
78 `K`-valued circle points and two roots on each of 126 remaining secants,
for

```text
78 + 2*126 = 330
```

exceptional values of `u`. There are 204 distinct exceptional event cases;
all other orientations give the generic case.

The independent verifier uses another reduction. It parametrizes the circle
except `u=-1` by

```text
u = (1 + i*sqrt(3)*t)/(1 - i*sqrt(3)*t),    t real.
```

Writing `k=|a|^2+|b|^2-target`, multiplication by `1+3*t^2` turns the event
condition into the degree-at-most-two polynomial over `K`

```text
(k + 2*p) - 12*q*t + (3*k - 6*p)*t^2.
```

The verifier factors every quadratic directly from its discriminant. Its
finite real-root census has 203 distinct factors: 77 linear factors and 126
irreducible quadratic factors with positive physical discriminant. The first
give 77 real parameters in `K`; each quadratic gives two real conjugate
parameters with the same complete event set. Adding the explicitly checked
orientation `u=-1` again gives `77 + 2*126 + 1 = 330` exceptional
orientations and 205 cases including the generic case.

Distinct normalized irreducible factors cannot share a root. If another
event polynomial vanished at one root of an irreducible quadratic, that
quadratic would divide it; its conjugate root would therefore carry the same
event. This proves that checking one formal graph per factor loses no
orientation. The producer's line-circle cases and the verifier's polynomial
cases agree through the canonical case SHA-256

```text
f8889fed0ef33d68847ff2a2bda34035dd1fb3882cd80221a9eb29fe465611ca
```

## Collision quotients and colouring certificate

At an exceptional orientation the formal 100 addresses may collide. A colour
word on the formal addresses descends to the physical point set exactly when
it assigns equal colours to every collision pair. Requiring unequal colours
on every unit pair then gives a proper colouring of the strict quotient.
The verifier checks these conditions directly.

The 205 cases have this exact physical size distribution:

| vertices | edges | cases |
|---:|---:|---:|
| 46 | 141 | 3 |
| 67 | 246 | 3 |
| 88 | 327 | 12 |
| 88 | 330 | 12 |
| 100 | 360 | 1 |
| 100 | 363 | 102 |
| 100 | 366 | 36 |
| 100 | 369 | 12 |
| 100 | 372 | 24 |

`certificate.json` contains 32 proper formal colour words. A word can cover
many event cases. Their successive contributions to the running union are

```text
82, 41, 22, 13, 9, 6, 4, 2, 2, 2,
1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
1, 1, 1, 1, 1, 1, 1, 1, 1, 1.
```

Their union is every case. The first-cover-row vector has SHA-256

```text
bfef004895a1b98228f271b2a4ffea5d53f1fffd18a7ead129340a5cb2551199
```

The optional producer used CaDiCaL 1.9.5 through `python-sat` to obtain one
model for each case, deduplicated the 87 resulting words, and greedily chose
the displayed 32-row cover. Solver soundness is not a premise: the final
checker reconstructs every graph and directly checks every saved word.

## Independent verification

`verify.py` uses Python's standard library and imports no producer code. It:

1. reconstructs all ten Golomb points and all 18 strict base edges;
2. excludes a three-colouring by complete enumeration;
3. expands both the unit and collision polynomial for every formal pair;
4. factors every degree-two polynomial over `Q(sqrt(33))` with an explicit
   square test and verifies every split by multiplication;
5. reconstructs the 203 factors, all 205 event cases, and every collision
   quotient;
6. checks the 32 colour words and complete case cover; and
7. rejects eight malformed-certificate controls.

Normal and optimized Python executions produce exactly `expected.json`.
Exact `Fraction` arithmetic decides every equality and sign. No floating-point
predicate, numerical root isolation, SAT refutation, external coordinate
file, or large generated artifact is required.

## Reproduction

From this directory, with Python 3.11 or later:

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

To regenerate the colouring library, install the optional pinned dependency
outside the repository and run:

```sh
python3 -m venv /scratch/golomb-rotation-venv
/scratch/golomb-rotation-venv/bin/pip install -r requirements.txt
/scratch/golomb-rotation-venv/bin/python build_certificate.py
```

The Golomb name and hexagon-plus-inner-triangle construction are classical;
the coordinate table here is self-contained and independently checked.
Minkowski sums and rotated finite atoms are standard in computational work on
the problem; see Heule,
[*Trimming Graphs Using Clausal Proof Optimization*](https://arxiv.org/abs/1907.00929).
The standing comparison is Parts' verified 509-vertex graph,
[*Graph minimization, focusing on the example of 5-chromatic unit-distance
graphs in the plane*](https://arxiv.org/abs/2010.12665), also identified as
the current record in Haugland's
[*A Moser-spindle-free 5-chromatic unit distance graph on 2131 vertices in the
plane*](https://arxiv.org/html/2608.04542v4). These primary sources were
checked on 2026-09-07.

This complete two-factor Golomb family is retired at this boundary. It says
nothing about three or more Golomb summands, independently rotated factors,
other four-chromatic atoms, or arbitrary placements.

## Files

- `certificate.json`: 32 colouring words and exact construction hashes.
- `verify.py`: independent polynomial-event and colouring-cover checker.
- `build_certificate.py`: optional line-circle certificate producer.
- `expected.json`: canonical verification result.
- `validation.json`: recorded discovery and verification environment.
- `provenance.json`: source, coordination, and publication context.
