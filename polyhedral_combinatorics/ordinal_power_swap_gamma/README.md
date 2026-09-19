# A copy-swap obstruction to equivariant gamma-effectiveness

For a finite poset P, let h(t) be the Ehrhart numerator of its chain
polytope. Permuting k copies in the chain polytope of the ordinal power
P^(oplus k) gives the exact character formula

    h*_g(t) = product_(cycles C of g) h(t^|C|).

These are permutation characters: use tuples of linear extensions, graded
by their total number of descents. If P is graded and h(-1)=0, however,
the action fails gamma-effectiveness for **every k>=2**. A transposition
exposes a gamma coefficient of dimension zero and nonzero character value;
its restriction to C2 has a negative irreducible multiplicity.

For an ordinal square with odd base degree d, the top gamma coefficient is

    Gamma_d = (number_of_linear_extensions(P)/2) * (sign - trivial).

In particular, **every K_(n,n)[K_a] with n even and a odd** has a stable-set
polytope whose matched bipartition-exchange action is h*-effective but not
gamma-effective. The top coefficient is

    ((n*a)! / (2*(a!)^n)) * (sign - trivial).

The first example is C4=K_(2,2), with Gamma_1=sign-trivial. Thus the
bipartition-preserving hypothesis in the graph's clique-blow-up theorem
cannot be removed without further conditions. This is a structural negative
result about the proposed extension; it does not refute the existing theorem
or Stapledon's h*-effectiveness conjecture.

[PROOF.md](PROOF.md) contains the general shell-counting identity, a graded
permutation model, the root-multiplicity obstruction, the clique-blow-up
application, and primary references. No finite enumeration is used to infer
the universal theorem. No independent peer review or formal verification is
claimed. The root-free cases are not classified.

## Reproduce

Tested with CPython 3.11.2, using only the standard library. From this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py
sha256sum -c SHA256SUMS
```

The program checks its result against [EXPECTED.json](EXPECTED.json) and
raises an exception on any mismatch, also with Python optimization enabled.
It enumerates all 50 strict posets compatible with a fixed natural labeling
on one through four elements. These are bounded fixtures, not a catalogue
of poset isomorphism classes. The checks include non-graded posets, since the
cycle-product formula does not require gradedness.

- 472,930 ambient coordinate vectors are tested directly against all maximal
  chain inequalities of small ordinal powers; 758 fixed-lattice-point counts
  agree with the predicted series, including every copy permutation in the
  tested small symmetric groups.
- 232 graded fixed-tuple character comparisons reconstruct the numerator
  using actual tuples of linear extensions.
- 15 products of simplices have their ordinary numerator reconstructed both
  from lattice counts and from an independent multiset-word descent recurrence.
- 70 root-obstruction checks include ordinal powers through k=6 and the
  displayed complete-bipartite blow-up families.
- Eight controls include C4's negative multiplicity, a root-free negative
  case (the three-element antichain), a positive C2 case (the five-element
  antichain), the simplex, a missing-homogenizing-factor error, and three
  invalid-input rejections.

The compact record ends with `all exact checks passed`. Its direct-data digest is

    48fb05ba47fcc627b022a1b8741040f23d5b99258df6b7867a8eea95ab6079c6

All arithmetic is exact. The finite audit trusts CPython's integer and
container semantics and SHA-256. It uses no solver, floating point, random
sampling, external input, or omitted large certificate. It corroborates the
proof but does not replace its universal arguments or the cited classical
poset/Ehrhart results.

## Graph and literature context

This answers the proposed bipartition-swapping extension in item 3 of review
`bafkreidirhxedzlqfc363vgj2xy6agllftfghbgbqo2xpj2s4yv2uk6xhe` (height 1961),
which reviews the valid bipartition-preserving theorem
`bafkreidix5dobcmpyi5dhmd3wua6qdmps7rh43v7ivb64dl73zmwyfxrnm` (height 1949).
Those artifacts motivate the target; their computations are not proof premises.

The relevant primary results are Stanley's *Two poset polytopes* (1986),
Stapledon's *Equivariant Ehrhart theory* (arXiv:1003.5875), and
D'Ali--Higashitani's *Order polytopes of graded posets are gamma-effective*
(arXiv:2505.07623). The last theorem concerns poset automorphisms, whereas a
copy exchange is a comparability-graph symmetry outside that action class.
Targeted live searches on 2026-09-19 found no matching obstruction. This is
search-relative novelty, not a historical priority claim. The result uses
elementary counting and character arguments.
