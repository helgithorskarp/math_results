# Simple Ehrhart period collapse at determinant bound three

A simple rational three-polytope can have an integral primitive facet
matrix whose largest full minor is three, vertex denominator three, and
the Ehrhart **polynomial**

    L_P(n)=71n^3+35n^2+7n+1.

The twelve inequalities are in [WITNESS.json](WITNESS.json) and
[PROOF.md](PROOF.md). The example has twenty vertices, exactly two
nonintegral. Exhaustive rational geometry and a finite all-dilation
certificate verify it without relying on the local Fourier argument.

The proof establishes the sharp boundary: the prior simple-bimodular
theorem excludes collapse at determinant bound two in every dimension;
we prove that determinant bound three excludes collapse in dimensions
one and two. Thus both the determinant bound three and dimension three
are sharp for this first failure. No vertex/facet minimality is claimed.

A uniform construction explains the mechanism. For every odd `q>=3`,
truncate six corners of a cube in the index-`q` lattice
`u_1+u_2-2u_3=0 mod q`. The two retained nonintegral vertices have opposite
character profiles `(1,1,-2)` and `(-1,-1,2)`. Their nonconstant local
terms cancel, giving period one with exactly two nonintegral vertices in
dimension three. The construction includes composite odd denominators.
Its global determinant bound is three **only in the stated `q=3`
specialization**; no bound by `q` is asserted for other moduli.

Arbitrary-denominator period collapse was known previously. The scoped
advance is the determinant threshold and realization of this specified
pair of local cones. See [SOURCES.md](SOURCES.md) for the primary literature
and graph dependencies. This is an unformalized research result with an
exact computational certificate; independent review is pending.

## Reproduce

CPython 3.11 or later; standard library only. From this directory:

```bash
python3 verify.py --check
python3 -O verify.py --check
sha256sum -c SHA256SUMS
```

Expected checker message:

```text
PASS: trimodular geometry, all-n Ehrhart certificate, odd-denominator construction, and cancellation.
```

Run `python3 verify.py` for the compact exact record in
[EXPECTED.json](EXPECTED.json). The checks include all 220 full minors,
every vertex and facet, direct counts for `0<=n<=14`, a different cube-cap
counter, and small literal lattice enumerations. Four counts in each
residue modulo three certify the entire fixed-witness Ehrhart function
using Ehrhart's degree bound; three later counts are holdouts.

The general construction is proved for all odd moduli in PROOF.md.
Finite checks at `q=3,5,7,9,15,25`, including nonprime roots in an exact
rational quotient ring, are corroboration of that universal argument.
They also check the stated closed Ehrhart polynomial. All failures use
explicit exceptions and remain active under Python optimization.

The compact source consists of the proof, literature comparison, literal
witness, constructor, verifier, expected record, and checksum manifest.
There are no solver binaries, external datasets, or numerical tolerances.
The mathematical trust boundaries are Ehrhart's theorem and, for the
structural and obstruction proofs, the cited Berline--Vergne formula and
reviewed graph dependencies. Source publication does not constitute peer
review or formal verification.
