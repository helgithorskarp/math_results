# Ambient affine preservers of rational-distance triangle density

For a noncollinear triangle \(T\) in the real plane, let \(E(T)\) be the
points having rational distances from its three vertices.
Which fixed invertible affine maps send every triangle with dense \(E(T)\)
to another such triangle?

**Exactly the similarities with rational positive scale**, followed by
arbitrary translation. Orthogonal maps may be arbitrary real rotations or
reflections. If rational *squared* distances replace rational distances,
the answer is similarities whose squared scale is positive rational.

Two fixed unit right triangles, differing by a rotation through \(\pi/8\),
force a putative preserver to have rational scalar Gram matrix.
If that scalar is nonsquare, a third triangle selected from an odd prime
valuation refutes preservation. This supplies an explicit finite adaptive
obstruction for every excluded affine map.

The result gives a corrected ambient interpretation of the affine-group
discussion on pages 2–3 of Corvaja–Turchet–Zannier (2025).
For example, the rational map \(\operatorname{diag}(2,1)\) destroys
admissibility of the rotated right triangle. Scaling the triangle with
legs \(1,\sqrt3\) by \(\sqrt2\) even makes its rational-distance extension
locus empty. See [SOURCES.md](SOURCES.md) for precise attribution.
The paper's density criteria are imported; they are not challenged.

This is an exact classification of a preserver group. It does not resolve
the Erdos–Ulam problem: the extension points themselves need not have
rational pairwise distances. No first-priority claim is made.

## Proof and reproduction

- [PROOF.md](PROOF.md): theorem, two-test rigidity, prime-valuation
  obstruction, explicit counterexamples, and the distinction from rational
  changes of basis.
- [verify.py](verify.py): exact finite corroboration, with no dependencies.
- [expected.json](expected.json): deterministic compact output.
- [SHA256SUMS](SHA256SUMS): hashes of the other five files.

With Python 3.11 or later, run from this directory:

    python3 verify.py > /tmp/rational-distance-affine-output.json
    diff -u expected.json /tmp/rational-distance-affine-output.json
    sha256sum -c SHA256SUMS

Verified with Python 3.11.2 in under one second; running with -O gives the
same output. All assertions relevant to validation use explicit exceptions
and remain active under optimization.

The checker compares direct transformed vertex Gram matrices against the
rotation formula for 496 invertible integer matrices: 48 are scalar in
Gram and 448 fail the second rationality test. It constructs 348 nonsquare
scale certificates among 359 positive rational squared scales, including
174 negative prime valuations. It checks nine local norm certificates,
5616 integer norm samples, and independent primitive congruence
obstructions modulo 9 and 16 for the \(\sqrt2\) example.
Eight invalid certificates or inputs are rejected.

Matrix-record SHA-256:

    0456d42e0930cc3d01e22e4f38eeb5743aa7fbd7fdf23b75d624c49544405044

Scale-certificate SHA-256:

    9b102005af7c9f2585addf156a59212592faa1636fb6d4c6e6d202001fdd7b43

The computation uses exact rational arithmetic in a quartic number field.
It does not decide density or enumerate all affine maps.
The universal conclusions follow from the written proof and its stated
published density criteria. No solver, floating-point calculation, large
certificate, or external data is required.
