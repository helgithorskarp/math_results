# Prescribed-cycle recovery in Barnette graphs

For a fixed proper facial three-coloring, a Hamiltonian cycle is obtainable
from the Alam et al. bicolored-dual-tree construction **if and only if it
contains every edge in the designated green matching**. From such a cycle,
the proof constructs a suitable tree with a blue leaf root in linear time.
An exact product formula counts a specified family of rooted recovery
certificates.

The result characterizes the algorithm's Hamiltonian output image.
It does not settle Barnette's conjecture, and it does not newly answer
the universal prescribed-cycle question negatively: Rudolph's August 2026
preprint already does that. See [sources and status](SOURCES.md).

- [Theorem, proof, inverse construction and scope](PROOF.md)
- [Exact standard-library verifier](verify.py)
- [Expected output](expected.json)

Run from this directory with Python 3.11 or later:

    python3 verify.py > /tmp/barnette-cycle-recovery.json
    diff -u expected.json /tmp/barnette-cycle-recovery.json
    sha256sum -c SHA256SUMS

The verifier uses no network, input data, solver, or third-party package.
It takes less than a second in the development environment (Python 3.11.2).
All 62 Hamiltonian cycles and 810 dual spanning trees of six explicit
fixtures are compared across all ordered color roles. The two-cube sum
has 12 Hamiltonian cycles, of which six are outside the image under every
color labeling; the credited Rudolph fixture has 14 cycles, of which five
are outside. These are fixture checks, not a graph census.

The universal proof imports four properties of the published traversal.
The checker verifies the combinatorial inverse and its exact certificate
counts, not the traversal implementation. See the proof's trust boundary.
