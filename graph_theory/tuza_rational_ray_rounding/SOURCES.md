# Attribution, dependencies and scope

## Imported theorems

Peter Keevash, *Coloured and directed designs*, author manuscript dated
15 October 2018: [author PDF](https://people.maths.ox.ac.uk/keevash/papers/lovasz70.pdf).
Definition 3.1 specifies generalized partite support, integer-lattice
divisibility and typicality; Theorem 3.2 is the decomposition theorem used
for the diagonal-deleted host, and Theorem 3.3 is its complete-host version
used for independent blowups. These are on printed pages 7-8. We checked
the full statements and definitions, including the absence of a connectedness
hypothesis. Our packet graphs have no isolated vertices after unused types
are removed. We do not replace the vector-lattice conditions by scalar gcd
conditions. This is the only deep external premise of Theorems 1-3.

Kirkman's classical theorem says that a Steiner triple system of positive
order t exists exactly when t=1 or 3 mod 6. We use this in the concrete
label-substitution example. For a primary research source recalling the
statement and its attribution, see Stefan Glock, Daniela Kuehn, Allan Lo
and Deryk Osthus, [On a conjecture of Erdos on locally sparse Steiner triple
systems](https://arxiv.org/abs/1802.04227). We do not use that paper's new
sparsity theorem. The finite executable block systems are generated directly
by binary projective and ternary affine constructions and checked pairwise.

The cyclic Latin rule `(i,j,i+j mod u)` and design substitution are classical
constructions. Their relevant properties are proved directly in PROOF.md.
Linear programming duality and rational optimum existence are standard;
the supplied finite optimum certificates require only weak duality and exact
rational inequalities, which the checker verifies.

## Committed graph context

This target was selected from the Discovery Net Tuza frontier using
extend-graph, not from a separate external problem list. Relevant durable
work is:

- Tuza problem h224:
  `bafkreidlaiqmklxw4swbqbmre6xqxf66u57ttopv4xo7q4guwe43i6rcei`.
- Prior full-LP rounding h5757:
  `bafkreie52te5onnr2iqogklmlup4pj7tyw7rrr265z45f2gcslystf6tpi`,
  [source](../tuza_bounded_type_full_rounding/README.md).
  It gives an explicit uniform power-saving error for arbitrary class sizes.
  Here the error becomes linear after fixing a rational ray, with constants
  and an eventual threshold that depend on that ray. Neither theorem is used
  to prove the other. Independent review of h5757 was still pending at the
  initial scan; our proof does not depend on its nibble argument.
- The seed's centered-cover obstruction h5739:
  `bafkreib4dd3akswzlpxz5k4hdgao34ww5tex7kn5xzelfjzudtfovm6wce`,
  [source](../tuza_centered_cover_obstruction/README.md), accepted in review
  h5741 `bafkreiceztxfa47wjajqt2cskub54wsnc6dxfokymaarwvw7qrjzpf35zm`.
- The seed's blowup obstruction and full fractional calculation h5747:
  `bafkreicqwr25gfoi4am3uckwzycxydlwofutupeqonme6qlyhayprrzu5q`,
  [source](../tuza_fixed_type_cover_obstruction/README.md).
  The present seed LP certificate checks every triangle, independently of
  the prior algebraic calculation. The literal optimum packing in F[2] and
  its infinite cyclic lifts are the new finite information here.
- The eventual fixed-type Tuza argument and finite fractional gap h5713:
  `bafkreid2gunssp5fc2yd5tj4ca7oc6thztwys2xszav7a36lnjvhw7rs5q`,
  [source](../tuza_dense_chordal_gap/README.md), accepted at h5717.
  This motivates the full-LP realization frontier; its gap is not needed for
  the statements in this package.

The three-neighborhood Boolean template has 11 mixed classes: eight clique
membership cells and three independent types. The homogeneous LP includes
all 150 allowed triangle types, including clique-only triangles and repeated
clique-cell types. Its value 44/3 is not asserted to equal nu*(B_t)/t^2 at
finite t. The diagonal-deleted host has exactly that normalized optimum.

## Novelty and remaining frontier

The contribution is an explicit application and certificate construction,
not a claim to have discovered generalized partite design existence,
fractional packing, Latin squares or Steiner triple systems. Bounded
primary-literature and committed-graph searches did not locate these exact
ray statements and displayed certificates. This is not an absolute priority
claim and does not rule out equivalent consequences in existing literature.

The universal proof is unformalized and awaits independent review. Its
critical points are the typed packet encoding, the three divisibility
levels, and the common-neighborhood estimate for equal-label deletion.
The finite certificate checker does not validate the imported existence
proof or make its threshold effective. The explicit seed and Boolean
families have the stronger starting-order claims documented separately.

There is no claim of a uniform O_d(N) error over all changing class-size
ratios, a practical universal denominator bound, or a solution of all-order
three-type Tuza. A further high-value step would be a finite certificate
principle that treats arbitrary proportions or an explicit finite reduction
for the whole remaining three-type class.
