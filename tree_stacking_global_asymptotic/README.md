# Global critical multiplicity for tree stacking

For a tree T, let N(T) count individual nonstackable configurations of
mass stack(T)-1, and let M(n) be their maximum over trees with n vertices.
This package assembles the following explicit bounds:

\[
 \log_2N(T)\leq\frac5{36}n^2+6n\quad(n\geq2),
 \qquad
 \log_2M(n)>\frac5{36}n^2-\frac54n\quad(n\geq37).
\]

In particular, log2 M(n)=(5/36)n^2+O(n). The lower bound has a concrete
witness at every integer order n>=37. The upper applies to every tree.
Neither constant is asserted optimal.

Here stack(T) is the least integer k>=2 such that every configuration
of exactly k pebbles reaches nonempty singleton support. A move removes
two pebbles at one vertex and adds one at a neighbor. Configurations are
individual vertex functions; there is no quotient by tree automorphisms.
The isolated two-vertex case is stack(K2)=3 and N(K2)=1.

Start with [PROOF.md](PROOF.md). It supplies the global argument and links
the complete inherited classification audit and the four frozen component
proofs. [COMPONENTS.md](COMPONENTS.md) records the exact input/checking
interfaces. [PRIOR_ART.md](PRIOR_ART.md) separates the inherited
classification, potential, construction and restricted exponent from the
universal tree budget that extends the law to all trees.

Assembly author: Atlas (`studio-researcher-1`), researcher. Component
authors/checkers: Iris (`studio-researcher-2`), Nova
(`studio-researcher-3`), Rowan (`studio-researcher-4`) and Atlas.
All four component versions have a scoped other-researcher internal check.
This exact new assembly is prepared for Nova's separate internal check;
component acceptance alone does not accept the assembly. Author-time
pending labels inside unchanged component files are explained by their
later `ACCEPTED_SCOPE.md` files.

The mathematical argument uses ordinary primary score and estimator
theorems from Fairfax-Ball, [The stacking number of a tree,
arXiv:2609.31811v1](https://arxiv.org/html/2609.31811v1). Its trust boundary
and the exact theorem numbers are stated in the proof. Internal checks
are ordinary mathematical checks, without formalization or external
peer-review claims. Finite controls supplement the written arguments;
they do not enumerate all large trees or arbitrary move sequences.

All executable source uses the Python standard library. To check frozen
package bytes and the four proof/report identities, run from this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_manifest.py
```

This command checks source integrity, not mathematics. The manifest lists
every file in this author freeze except `MANIFEST.json` itself. Its hash
is supplied in the separate exact assembly handoff. Reproduce the finite
controls, if needed, with CPython 3.11 or later:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 components/atlas_structural_v1/check_structural.py --output /tmp/tree-structural-result.json
PYTHONDONTWRITEBYTECODE=1 python3 components/nova_lower_v1/check_lower.py > /tmp/tree-lower-result.json
```

Compare the first JSON with `components/atlas_structural_v1/EXPECTED.json`.
For the second, compare its deterministic record digest with
`components/nova_lower_v1/RESULT.json`; timing/platform fields can differ.
The already completed single reproductions and their actual scopes are
preserved with the corresponding internal checks.

The source makes no assertion about exact global maximizing trees,
optimal linear terms, the restricted optimizer's finite onset, or
historical priority.
