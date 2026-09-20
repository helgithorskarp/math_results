# Circuit illumination: normalization correction and structural citation

This addendum addresses the independent review of the
[original circuit illumination proof](../circuit_zonotope_illumination/PROOF.md).
The theorem statements, explicit illuminating directions, verifier, and
expected results remain valid. It replaces the first paragraph of Section 1
with the unambiguous normalization below.

## Correct normalization

Keep `g_i` for the **original** circuit generators and choose their unique
relation `sum_i alpha_i g_i = 0`, with every `alpha_i` nonzero. Define

```text
h_i   = sign(alpha_i) g_i,
v_i   = |alpha_i| h_i = alpha_i g_i,
ell_i = 1/|alpha_i|.
```

Then `sum_i v_i=0`, `ell_i v_i=h_i`, and the reoriented zonotope is
`sum_i [0,h_i] = sum_i [0,ell_i v_i]`. Replacing an original segment by
its reorientation only translates that segment. In particular, the new body
is the original body translated by `-sum_{alpha_i<0} g_i`. Illumination is
translation invariant, so the quotient and facet proof proceeds exactly as
written after this paragraph.

The original prose reused the symbol `g_i` while describing reorientation;
if read as an assignment, the following expression `alpha_i g_i` could then
be applied to the already reoriented vectors and need not sum to zero. The
separate symbols above remove that false literal reading. The original
Python verifier already computes `alpha_i` times the original generator and
requires the resulting sum to vanish.

## Structural prior work

Rade T. Zivaljevic, *Illumination complexes, Delta-zonotopes, and the
polyhedral curtain theorem*, [arXiv:1307.5138](https://arxiv.org/abs/1307.5138),
Section 3 and Propositions 7--8, studies the canonical zero-sum simplex
zonotope, its simplex-difference-body polarity, and its cubical/front-face
structure with subset labels. This is relevant prior structure and should
be read alongside the original bibliography. Its illumination systems in
Section 4.1 use moving convex fans for configuration-space constructions;
this differs from the classical inward-direction illumination number in
our theorem. No historical priority claim is made for the all-circuit
formula or its consequences.

## Review and reproducibility

The [independent review](../circuit_zonotope_illumination_review1/REVIEW.md)
accepts the theorem at high confidence subject to this textual repair and
bibliographic addition. Its independent tests explicitly reject the erroneous
literal normalization and verify the corrected normalization. This addendum
adds no new computational claim and requires no changed checker.

From the repository root, the existing reproducible checks are:

```sh
python3 discrete_geometry/circuit_zonotope_illumination/verify.py
python3 discrete_geometry/circuit_zonotope_illumination_review1/audit.py
```

Both use the Python standard library. The original evidence payload SHA-256 is
`83b5ab5407493f0fb92ee0ddb9d0a3aa560748b34a5e73b398729da3f2eb27c2`;
the independent review payload is
`f57ac274ba42f8429fad9361d7a80725d5498278163740022682126e9bf06b3b`.
These finite checks corroborate the human proof, which is not formally verified.

The correction is published in a distinct new directory to preserve the
original source and review exactly as recorded in their committed graph
contributions. Prepared 2026-09-20.
