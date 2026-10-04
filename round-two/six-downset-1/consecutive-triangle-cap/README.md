# Consecutive unequal triangle counts: a uniform cap on every old cube

Actual author **six-downset-1**, role **researcher**, 2026-10-04.
Ordinary author proof plus a complete exact coefficient certificate;
unformalized and independently unreviewed.

For every integer **n>=3, h>=3**, take an old n-point Boolean cube and h
mutually private triangles at mark x, h-1 at a distinct mark y. Every
private pair is disjoint from the cube and all other pairs. With
q=2^(n-1), N=2q+12h-6, s=q+3h, there is a rational matrix M on all original
vertices, including the empty set, with

```
M=M', M1=1, M[A,B]=0 if A intersects B,
L=sI+(N-s)M >= 0, I-M >= 0,
rank L=rank(I-M)=N-1,
NI-L >= (1-8delta)(I-J/N), 1-8delta>3/4.
```

Both ranks are greatest among real competitors, and the unit eigenvalue is
simple. The exact delta, explicit inverse energy and whole physical-space
argument are in [PROOF.md](PROOF.md). Ordinary H existence and maximal
lower rank are credited prior9361; the new information is the cap and gap.
There is no statement about arbitrary unequal counts, overlapping facets,
n=2, h=2, arbitrary downsets, optimal gaps, or general Conjecture H/I.

The retained light facet mean must be kept. New harmonic facet coupling
controls the complete ten-dimensional aggregate; a three-pair repair then
attains greatest lower rank. Original row-space completeness and the
spectral/Schur arguments are ordinary written mathematics. Exact checks
verify the complete rational identities and signs, not those analytic
bridges by a proof assistant.

## Source-only reproduction

CPython **3.10+**, standard library only; actually tested with **3.12.14**.
From this directory run:

```sh
python3 -I -B reproduce.py --regenerate --check-expected
python3 -I -O -B reproduce.py --regenerate --check-expected
```

The entry point sets all six numerical thread variables to one, runs only
one arithmetic child at a time, and imposes an unchanged 60-second limit
on each child. Each child's actual exit is waited. On a slow machine an
interruption means incomplete validation, never a mathematical rejection.
The polynomial limit is 512 terms and packing limit 32MiB. Literal controls
keep n<=6, h<=10, N<=80; no resource increase or broad enumeration is needed.

Expected final mathematical replay SHA256:
`31e55ab9d9daa033d628b6d227ea6ff321a0247f471fb2f963e10f43e5b4a5e8`.
All mathematical checks run before comparing [expected.json](expected.json).
Generated original matrices, complete physical forms, inverse vectors,
expanded coefficients and stage records go to ignored `work/`.
`--regenerate` verifies the **entire** producer certificate against the
published compact certificate. Omitting it still checks that certificate
with the separate reader and reruns every original control/damage check.

## Exact certificate and trust boundary

[CERTIFICATE.json](CERTIFICATE.json) is **129898 bytes**, SHA256
`84d3cb749bf77359237d02c94c62de955b6deb3c0314e6714b0fbd71be94f44c`.
Lossless interning retains every original entry, pivot, update and coefficient;
the 3.77MB repeated-text producer record regenerates and is not published.

[check_harmonic.py](check_harmonic.py) imports no producer, physical recipe,
sector module or polynomial-field engine. Its [separate closed forms](independent_harmonic.py)
and conservative degrees check all **151** original rational identities
on the complete degree-(56,12) Cartesian grid: **741 nodes, 111891
comparisons**. Every one of **315** Gaussian identities is checked on its
complete degree grid, **4190 total nodes**. All **33** pivots have complete
nonnegative shifted coefficients and strictly positive constant terms:
**1142 coefficients**, with every denominator factor also positive on
auxiliary real h>=3,q>=4. The auxiliary identity grids are distinct from
enumeration of physical downsets.

Finite original controls at (n,h)=(4,3),(3,3),(3,4) check **6060 original
matrix entries** and **10566 metric/frame positions**, including every
cross-block entry, untouched old space, the actual empty row and all
physical-dual/full-inverse equations. These controls validate the mapping;
they are not the infinite-family coverage argument. Eight semantic
certificate damages are rejected in both modes. [VALIDATION.json](VALIDATION.json)
records completed research validation; [CREDITS.md](CREDITS.md) records the
exact reused utilities and method scope. Source integrity uses [SHA256SUMS](SHA256SUMS)
and a complete regular-file census, not a mathematical hash assumption.

Separate algorithms and optimization modes are same-author checks. They
are neither independent-person review nor formalization. No floating
point, solver status, stored expected summary, timeout, memory failure or
incomplete enumeration is a mathematical premise.
