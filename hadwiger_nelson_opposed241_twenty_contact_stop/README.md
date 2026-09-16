# A 481-point outside-field opposed-core assembly stops at four colours

Two congruent copies of the reviewed 241-point opposed-B214 conditional core
are placed in one exact, nonnative relative frame. They share only the origin
and have **20 genuine private cross contacts**. The complete strict plane
unit-distance graph has **481 distinct points and 2,002 edges**. It has no
articulation or bridge, minimum degree four, and its entire 481-point support
is the four-core.

The graph nevertheless has chromatic number **exactly four**. The certificate
contains a literal proper four-colour word checked on every physical unit
edge. Either copy contains the ten-point Golomb graph, whose normalized
three-colour assignments are exhausted directly. Thus this one higher-arity,
multiple-contact interaction is a decisive construction stop, not a
five-chromatic candidate or an improvement on the 509-point record.

## Frozen exact placement

Write a point of the source as

```text
(X, sqrt(3) Y),  X,Y in K=Q(sqrt(33)).
```

Let `t` be the positive real root of

```text
t^2 = (2+2 sqrt(33))/3.
```

The norm of the right side from `K` to `Q` is `-128/9`. It therefore cannot
be a square in `K`, since the norm of a square is a rational square. Hence
`1,t` is a faithful basis of the quadratic extension used by the checker.

The first copy stays in its published frame. Rotate the second about the
shared origin by the unit complex number whose coefficients are

```text
cos(theta) = 1/4 + sqrt(33)/12
             + (-5/16 + sqrt(33)/16) t,

sin(theta)/sqrt(3) = -5/12 + sqrt(33)/12
                     + (-1/16 - sqrt(33)/48) t.
```

The verifier derives this rotation from the requirement that source vertices
45 and 65 become unit-separated and checks its unit norm exactly. The angle is
approximately 325.8315 degrees, but no floating-point value enters the proof.
A geometry-only contact preflight fixed this frame before the colouring was
queried; no optimality of the frame is claimed.

Exact collision merging finds only the common origin. Exhausting all 115,440
physical pairs gives 1,982 inherited edges and the 20 cross edges stored in
the certificate. The point and edge stream hashes are respectively

```text
9ac902c4f179dbe1c1a3a2c76dab6225f77c7969041e9feef18d5455082adff6
57296047b72d08a553b2a84b22db353ad5a6af29369314e3bf74fa01ac4a287f
```

This support is not contained in the old native coordinate field, so its
failure is not inferred from the earlier whole-field four-colouring. It is
decided directly by its complete physical graph.

## Scope

The result retires exactly this two-core shared-origin rotation. It does not
classify other rotations, copies, fragments, contacts, or the full higher-
arity relation of the 241-point source. In particular, it must not be read as
a global theorem about opposed-B214 constructions. No neighbouring angle or
second frame was tested after the proper four-word appeared.

## Reproduce

From the repository root with CPython 3.11 or later and only its standard
library:

```sh
python3 -B hadwiger_nelson_opposed241_twenty_contact_stop/verify.py --check-expected
python3 -O -B hadwiger_nelson_opposed241_twenty_contact_stop/verify.py --check-expected
python3 -B hadwiger_nelson_opposed241_twenty_contact_stop/controls.py
sha256sum -c hadwiger_nelson_opposed241_twenty_contact_stop/SHA256SUMS
```

The checker reconstructs the source coordinates from the hash-pinned B214
fixture and conditional-core label list, derives the rotation, collision-
merges both copies, tests every pair exactly, checks the literal colouring,
and independently proves the Golomb lower bound. It imports no solver and
uses no numerical edge tolerance.
