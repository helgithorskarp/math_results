# Exact illumination from order ideals

For every nontrivial join of comparability graphs
`G=G(P_1) vee ... vee G(P_k)`, `k>=2`, and every strictly positive edge
weighting, the graphical zonotope satisfies

\[
 I(Z_G)=I_f(Z_G)=i(G)-1=\sum_{j=1}^k(|J(P_j)|-1).
\]

Here `i` counts independent sets **including the empty set**, and `J(P)`
is the set of order ideals. The proof supplies an optimal illuminating
set and a matching antipodal vertex certificate. It extends the
[complete multipartite formula](../multipartite_zonotope_illumination/)
to factors with arbitrary comparability edges.

The two mechanisms have separate scopes. Proper order ideals give an
antipodal lower certificate for every connected comparability graph.
A direction with one concentrated negative coordinate gives an upper
cover whenever every nonempty independent set has a common neighbor.
These bounds meet for the stated joins. This is a full family theorem,
not an extrapolation from the finite checks.

For any bipartite graph `H` on `n>=1` vertices, it follows that

\[
 B_H=[-1,1]^n+\sum_{ij\in E(H)}[-(e_i-e_j),e_i-e_j]
 \quad\text{has}\quad I(B_H)=I_f(B_H)=i(H).
\]

Together with the classical exact `#BIS` theorem, this gives
`#P`-completeness under polynomial-time Turing reductions for computing
either parameter on this graph-indexed, integer-generator input class.
It asserts no approximation hardness or complexity classification for
unrestricted convex bodies.

Read [PROOF.md](PROOF.md) for all hypotheses, certificates, proofs and the
input convention; [SOURCES.md](SOURCES.md) distinguishes prior inputs and
the proposed contribution. Historical priority and independent review
remain unclaimed. The general illumination conjecture and arbitrary
graphical zonotopes are outside the exact formula.

## Reproduce

From this directory, using CPython 3.11 or later and only its standard library:

```sh
python3 verify.py > /tmp/order-ideal-illumination.json
diff -u expected.json /tmp/order-ideal-illumination.json
sha256sum -c SHA256SUMS
```

The checker uses integer and rational arithmetic. It reconstructs weighted
vertices and support values directly, checks an actual positive rational
step into the interior, verifies every antipodal pair, and compares two
orientation-enumeration algorithms where specified in the source. It
also checks the cube-plus-difference generator map. It uses no solver,
random sampling, external data, or unpublished certificate.

The deterministic [expected output](expected.json) records:

- All 203 connected naturally labeled posets on two through five elements:
  26,745 weighted antipodal-pair checks.
- 165 distinct join graphs: 16,378 vertices, 334,722 strict active-cut
  checks, 49,134 rational interior steps, and 36,954 weighted antipodal pairs.
  The family includes 99 ordinal-sum graphs through five vertices, all
  64 cones over bipartite graphs with fixed parts of sizes two and three,
  and two specified larger examples.
- The counting reduction on all 64 of those bipartite inputs, two named
  noncomparability upper-bound examples, and nine rejection/scope controls.

Normal and `python3 -O` runs give identical output; a reference run on
CPython 3.11.2 took about seven seconds. Expected-output SHA256:
`0eaa6e4b3a27437d3255ceee6156780c5d55033969f47d90625a3926f08de7d5`.
These finite checks corroborate the written all-order argument; they are
neither its logical basis nor independent peer review.
