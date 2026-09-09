# Exact D3 quotient of the complex-radix frontier

This package quotients the complete finite obstruction in
`../hadwiger_nelson_complex_radix_architecture` by its physical dihedral
parameter symmetry.  It is a complementary exact interface, not a candidate
search.

For

    A5(z) = {sum(a_j z^j, j=0..4) : a_j in {0,1,omega}},
    omega=(1+i sqrt(3))/2,

the transformations

    R(z)=omega^2 z,       C(z)=conjugate(z)

generate D3 and give isometric strict physical graphs.  The exact quotient is:

- 2,797 active curves in 529 D3 orbits;
- 264,800 source pair systems, whose 785,380-system D3 closure has 132,130
  orbits;
- 2,400 nonzero collision polynomials in 442 D3 orbits;
- at most 7,785,424 injective exceptional parameter orbits by Bezout, plus at
  most 1,682 collision parameter orbits, hence at most **7,787,106** exceptional
  D3 parameter orbits in total.

Every D3 orbit has a representative in the exact chamber

    x>=0, 0<=y<=x,  1/4 < x^2+3y^2 <= 4,

where `z=x+i sqrt(3)y`; the last inequalities apply to possible non-four-
colourable parameters.  See `PROOF.md` for the important distinction between
using one system per orbit on the whole plane and using the full closed system
list inside the chamber.

## Reproduce

From this directory, using CPython 3.11 or later and no third-party package:

```sh
python3 -B verify.py --check-expected
python3 -B controls.py
python3 -B produce.py --out /tmp/hn_radix_d3_certificate.json
sha256sum /tmp/hn_radix_d3_certificate.json certificate.json
```

The last two hashes must both be
`aa8bb1f495edf2691cda637c14e5bd40873aef0558492e1bf69622184fb9df93`.

The complete representative lists are deliberately generated, not committed:

```sh
python3 -B export_quotient.py --out generated_quotient.json
```

The canonical output is 1,334,366 bytes with SHA-256
`90e6235fcd71a8998fe6c4229882f383fe9d18c7c3dd6c66cca9098fa5057998`.
It contains 529 curve orbits, 132,130 pair representatives, and 442 collision
representatives.  `.gitignore` keeps this generated interface local.

## Scope

The result reduces HN2's complete necessary exceptional frontier modulo known
physical isometries.  It does not show that any exceptional parameter is
non-four-colourable, does not perform a chromatic search, and does not produce
a five-chromatic graph or improve the 509-vertex record.
