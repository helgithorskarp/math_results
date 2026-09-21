# Fixed points of total-graph clique complexes

For every finite simple graph G and subgroup H of Aut(G), put
A=|Cl(G)| and X=|Cl(T(G))|, where T is the total-graph operation.
Then X^H is homotopy equivalent to A^H with a sphere
S^(o_H(tau)-1) attached at the barycenter of every setwise H-invariant
triangle tau. Here o_H(tau) is the number of H-orbits on its vertices.

| Action on an invariant triangle | Added fixed-space piece |
| --- | --- |
| Three singleton orbits | A 2-sphere |
| Two orbits, of sizes 2 and 1 | A circle |
| One transitive orbit | One new isolated point |
| Triangle is not setwise invariant | Nothing outside the old fixed space |

The proof constructs an Aut(G)-equivariant homotopy model by attaching
reduced-permutation representation spheres to A. It does not choose an
equivariant global wedge basepoint. It also yields a componentwise
fixed-space asphericity criterion and the integral signed-triangle
summand in H_2.

The ordinary nonequivariant sphere decomposition is already
[Adamaszek, Theorem 5.1](https://arxiv.org/html/1104.0433).
The increment here is the explicit symmetry-compatible refinement.
This is a bounded structural lemma, not a resolution of Whitehead's
asphericity conjecture. Historical priority is not asserted;
independent review is pending.

- [Proof, including equivariant attachments and all subgroup fixed spaces](PROOF.md)
- [Attribution and precise novelty boundary](REFERENCES.md)
- [Direct exact verifier](verify.py)
- [Compact expected evidence](expected.json)

## Reproduce

From the repository root:

    python3 combinatorial_topology/total_graph_fixed_points/verify.py

Or from this directory:

    python3 verify.py
    python3 -O verify.py
    sha256sum -c MANIFEST.sha256

CPython 3.10 or newer; tested with 3.11.2. Standard library only, no
downloads or external mathematical data. The check takes about one
second or less on the development host. Use --emit to print all compact
evidence without reading expected.json.

Expected: PASS, 19 graph/action fixtures over both F_2 and F_3,
182 integer octahedral cycles, 85 generator-action sign checks, and
126 rational star-deformation controls. Three deliberately invalid
controls are rejected.

The verifier constructs the geometric fixed spaces as clique-orbit
support complexes, then computes exact simplicial boundary ranks. It
does not use the claimed deformation to calculate homology. Fixtures
include transpositions, transitive actions, permuted triangle orbits,
empty fixed spaces, preexisting circle/sphere homology, a 3-sphere
flag complex, and the barycentric projective plane with its
characteristic-dependent homology.

Finite exact checks corroborate the universal written proof. They do
not prove equivariant homotopy equivalence or integral homotopy type
by themselves. The proof is unformalized; using a different verification
method here does not constitute independent peer review. No exhaustive
graph or automorphism census is claimed.

The manifest covers all five other files; it does not hash itself.
