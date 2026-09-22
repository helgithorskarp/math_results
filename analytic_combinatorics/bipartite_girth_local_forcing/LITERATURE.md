# Literature and graph provenance

Searched and checked on 2026-09-22. Novelty here is relative to the
sources inspected, not a certified historical-priority claim.

## Prior analytic inputs

1. L. Lovász, *Subgraph densities in signed graphons and the local
   Sidorenko conjecture*, [arXiv:1004.3026](https://arxiv.org/abs/1004.3026),
   [full text](https://arxiv.org/html/1004.3026). The proof uses Corollary
   2.7 and Lemma 2.22. The paper also already establishes local
   Sidorenko through signed-subgraph expansions. We do not claim these
   inequalities or this proof method as new.
2. J. Fox and F. Wei, *On the Local Approach to Sidorenko's Conjecture*,
   Electronic Notes in Discrete Mathematics 61 (2017), 459--465,
   [DOI](https://doi.org/10.1016/j.endm.2017.06.074). Its primary abstract
   states the qualitative local-forcing result for even-girth graphs.
   The publisher's full text returned HTTP 403 during this audit, so
   we cannot certify the absence of sharper statements in its body.
3. Y. Zhao, *Tensor Amplification and Spectral Transfer for Sidorenko-Type
   Inequalities*, [arXiv:2607.02260v1](https://arxiv.org/abs/2607.02260v1),
   [full text](https://arxiv.org/html/2607.02260v1). Its near-equality and
   regularization results supply important context; they are not a
   premise of our proof. We did not find the girth-dependent sharp cut
   constant or the extremizing-sequence characterization there.

## Substitution route considered and not claimed

S. Im, R. Li and H. Liu, *Sidorenko's conjecture for subdivisions and
theta substitutions*, Combinatorics, Probability and Computing 35
(2026), 269--279,
[DOI](https://doi.org/10.1017/S0963548325100242), already proves broad
substitution results. A. Kiem, O. Parczyk and C. Spiegel,
[arXiv:2412.12904](https://arxiv.org/abs/2412.12904), now titled
*Adjunctions, Box Products, and Forcing Families*, develops broad
forcing-preserving operations. These made a qualitative substitution
extension an unsuitable novelty target for this pass. Our theorem
instead concerns the exact local exponent, constant, and equality
profiles for arbitrary bipartite `H` with a cycle, including graphs
whose global Sidorenko status is unknown.

## Discovery Net dependencies and antecedents

The graph-first source is Sidorenko's conjecture, artifact
`bafkreifnkj3n6weqg74x6kiea6qiyzvedps3rnsrqttq2hfwo4h4oo6qim`.
Its relevant developed neighborhood contains:

* Complete-bipartite quantitative deficit:
  `bafkreiaup4htkgrnxthic2i4c3dn7qoxgxeyyyf2jrhx3fk7vzfjjnwfkm`.
* All-complete-bipartite cut modulus:
  `bafkreifvxdcjzqtr6houfh2eiak3pl6fdmmippxbfj3ms2wzc4a4nxdpde`.
* Sharp unrestricted complete-bipartite local constant:
  `bafkreig6uwsexevsatxxo2iyo6jugj24ljkj4entpegcynwccpptv6hdum`.
* Rank-one rigidity of asymptotic complete-bipartite cut extremizers:
  `bafkreiarfornxcaydnajmrv7u27ngyx2gsb3rinybdufekqjycgpp6da2a`.

The [public antecedent source](https://github.com/njallskarp/math_source_code_open/tree/main/complete_bipartite_graphon_stability)
contains the full complete-bipartite sequence and its exact audits.
The canonical degree/regular decomposition and the rooted-gluing
mechanism already occur there. This package credits that mechanism and
extends it using the homogeneous arbitrary-girth consequence of
Lovász's inequality. No source code from the antecedent package is used.

The earlier corrected modulus review is
`bafkreib7eoeya6zhoq3o3whb5cod2i52x75hgftxhsait2257k7dh4ddcq`;
the sharp unrestricted constant review is
`bafkreic3gaz5myjych3b3np7ro5gnxmx5yfi3ux5jmiorlmvheyms7dcyi`.
Their acceptance does not amount to independent verification of the
present all-girth theorem.

## Scope of the search

The committed graph was searched by Sidorenko, forcing modulus, girth,
local constant, and extremizer concepts, and incoming reviews and source
relations were followed. Primary literature searches combined those
concepts with sharpness, quantitative stability, and cut norm. No exact
match to the constant `1/(4*(c_g*p^(m-g))^(1/g))` together with the
unrestricted two-component expansion and sequence characterization was
located. The known qualitative result and inaccessible Fox--Wei full
text limit how strongly this can be advertised. The mathematical claim
is precise; publication significance and priority require human review.
