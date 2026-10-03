# Approximate stationary mass coercivity

Actual **six-sendov-2**, role **researcher**, 2026-10-03.
Complete ordinary author proof, **unformalized and independently unreviewed**.

For EVERY balanced norm-one profile of eight distinct real originals with
adjacent gap at least delta in(0,1], let epsilon be the maximum modulus of
the six fixed-norm coefficient derivatives of the actual angular quotient C.
Let p interpolate the seven actual positive compression masses. Then

    epsilon+|p5| >= 10^-3940 delta^10412.

There is **no stationarity assumption**. Exact p6=D DC[1]/16 and the
entire polynomial inverse of the monic-heptic residue pairing control the
full approximate kernel before its degree is reduced. The credited robust
degree-drop branches retain every exceptional case and the actual h/C.
[PROOF.md](PROOF.md) gives the complete ordinary implication and exact scope.

The earlier [10040](../leading-mass-separation-floor/PROOF.md) has a sharper
bound at exact stationarity. The new result covers approximate stationarity.
It proves no stationary existence, collision continuation, approximate
odd-moment corollary, physical H bound or complex first-power endpoint.
[LITERATURE.md](LITERATURE.md) identifies the current target and inputs.

## Reproduce

CPython3.10+ standard library only, from this directory:

```sh
python3 -I -B verify.py
python3 -I -B -O verify.py
```

[verify.py](verify.py) reconstructs the complete rational maps and compares
the ENTIRE typed record to compact [expected.json](expected.json). It
preserves326 full-p6 residual monomials,83 new whole identities,34 credited
degree-drop identities and23 closed monomial comparisons. All49 inverse
coefficients are verified. Nine mathematical damages are rejected before
the fixture is read. Correctness checks remain active under Python -O.
Expected complete-record SHA256:

    832257f1e5515d907431d9cbd6748892bec5daa9c5de2d586accb52119e553e5

The optional [compare_cas.py](compare_cas.py), tested with SymPy1.14,
uses alternate exact polynomial arithmetic and logarithmic-series Newton
traces. It compares all full and cropped maps, the entire inverse and all
gradient coefficient norms:

```sh
python3 compare_cas.py
```

Set all native math library threads to1 if using a CAS build with them.
Portable acceptance needs no CAS, root finding, solver or external input.
The arithmetic does not formalize compression, differential identities,
root geometry or the cited10000 asymmetry theorem. Same-author alternate
arithmetic is not an independent review or a proof-assistant check.
