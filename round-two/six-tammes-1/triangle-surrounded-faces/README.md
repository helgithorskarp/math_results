# A physical short-face filter for Tammes fifteen

Actual author: **six-tammes-1**, researcher, 2026-10-02.

For a spherical packing with all different-point inner products at most
\(c\in[1/2,3/5]\), consider a simple actual contact face of length four,
five or six, with disk closure and all its own interior angles at most
\(\pi\). Suppose every other sector at each boundary vertex is an actual
triangular face. Then a quadrilateral or pentagon is impossible. A hexagon
forces the twelve-point regular hexagonal antiprism at \(c=1/\sqrt3\),
which can extend to at most fourteen points. Thus none of these
vertex-surrounded faces can occur for fifteen or more points.

[PROOF.md](PROOF.md) gives the physical hypotheses, the ordinary reflection
and capacity arguments, and the exact finite closure reduction.
The condition concerns every other sector at each boundary vertex;
triangular neighbors merely across the boundary edges do not suffice.

In a connected physical contact map whose faces are all simple disks of
length three through six and whose nontriangle angles are at most \(\pi\),
each vertex is on a nontriangle face and each nontriangle shares a vertex
with another. The graph of nontriangular faces joined by shared vertices
has at most half as many components as faces. For the known T11/Q3/P3
profile, at most three such components cover all fifteen vertices.
Occurrence of this profile or of a G22 motif in every optimizer remains
unproved. No global Tammes-15 bound or historical priority is claimed.

From this directory, with Python 3.12 and its standard library:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B check.py
python3 -B audit.py
python3 -B controls.py
python3 -B -O check.py
python3 -B -O audit.py
python3 -B -O controls.py
```

Run the commands sequentially. `check.py` regenerates and compares the
complete included certificate; `--emit PATH` instead writes it to a
chosen private output. `audit.py` imports neither the producer nor its
polynomial helpers. The producer uses fan recurrences and dense rational
polynomials, while the auditor uses literal transfer matrices, dictionary
polynomials, and coefficient identities. Both are authored checks,
not independent researcher review or proof-assistant formalization.

Expected producer summary: 56 closure words, 55 strict full-band
exclusions, one exceptional hexagon, twelve core points, and total point
bound fourteen. The certificate SHA-256 is
`d52ac93547ec986d51b653b88bce1776264753fe15b3948a9f3aabac2ecc3a49`.
The auditor checks all 144 Gram positions, 24 contacts and 42 strict
unordered pair gaps. Controls reject twelve damaged certificates, accept
a valid rescaled witness, and recover the three classical antiprism
closures exactly. [VALIDATION.json](VALIDATION.json) records complete
normal and optimized outputs and measured resource use.

The proof requires no externally fetched input. See
[DEPENDENCIES.md](DEPENDENCIES.md) for the trust boundary and
[LITERATURE.md](LITERATURE.md) for classical context and current status.
