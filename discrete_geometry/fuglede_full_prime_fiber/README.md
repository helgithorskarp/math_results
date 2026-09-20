# Full prime fibers in spectral sets of size twice a prime

This package classifies spectral sets of size $2p$ that contain a full
prime fiber in $\mathbb Z_n\times\mathbb Z_p$, assuming $\gcd(n,p)=1$
and that $\mathbb Z_n$ has no spectral subset of size $p$.

After translating the contained fiber to $\{0\}\times\mathbb Z_p$,
the remaining points must be $(a_j,j)$, one on each level, with
all $a_j$ having the same 2-adic valuation less than $v_2(n)$.
This condition is also sufficient, and gives an explicit common
spectrum and tiling complement.

For $\mathbb Z/2310\mathbb Z$, this settles the entire size-22
family containing a full order-11 coset: the remaining first
coordinates are precisely arbitrary odd residues modulo 210.
Every such set tiles with the fixed complement
$22\mathbb Z_{2310}$ of size 105.

- [PROOF.md](PROOF.md): theorem, graph-spectrum dichotomy, fiber
  deletion identity, valuation criterion, and exact scope.
- [verify.py](verify.py): independent definition-level arithmetic
  and Fourier-zero clique checks.
- [expected.json](expected.json): deterministic exact output.
- [SOURCES.md](SOURCES.md): prior results and the novelty boundary.
- [SHA256SUMS](SHA256SUMS): file-integrity manifest.

From this directory, using Python 3.11+ and the standard library:

    python3 verify.py > /tmp/fuglede-full-fiber.json
    diff -u expected.json /tmp/fuglede-full-fiber.json
    sha256sum -c SHA256SUMS

The comparison must be empty and all checksums must pass. The full
check takes about one second on the development machine. It covers
4,890 full-fiber candidate sets, 14,375 graph-spectrum candidate
pairs, exact deletion checks, and explicit tilings including order
2310. The finite censuses support the written proof and are not a
search over all 22-point subsets of that group.

The unrestricted size-22 Fuglede question remains outside the claim.
Historical priority is not asserted.
