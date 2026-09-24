# Dependencies and novelty boundary

## Primary sources inspected live on 24 September 2026

1. Andrea Paone and Marco Paone, *Line-Graph Signature Beyond the 2-Core:
   Counterexamples, Pendant Attachments, and Bounds at Fixed Cyclomatic
   Number*, version 1.3, 30 July 2026.
   [Primary full text](https://aletheia-technologies.it/research/line-graph-signature-beyond-the-2-core/reader/).

   Conjecture 5.4 is `2s(L(G))<=c(G)+1`. Its pendant-tree formula explains
   why deleting trees need not preserve or lower signature. Our construction
   addresses the conjecture by preserving its slack while changing the
   graph, rather than assuming such deletion is monotone. The incidence
   identities and congruence machinery are classical.

2. Andrea Paone, *Unbounded Signature of Line Graphs: Counterexamples and
   Transfer Principles*, version 2.0, editorial revision 2, 1 August 2026.
   [Primary full text](https://aletheia-technologies.it/en/research/unbounded-signature-line-graphs/reader/).

   This is the source of the zero-response rooted C4--C5 module, its
   inertia `(6,0,5)` and determinant `-8`, and its arbitrary-host attachment
   principle. It also proves a period-four edge-subdivision congruence and
   credits earlier internal-path work of Ma--Yang--Li and Wang--Fan.
   None of those results is claimed as new here. Our proof independently
   verifies the module's small matrix identities.

3. Andrea Paone and Marco Paone, *Line-graph inertia of roses and generalized
   theta graphs*, version 1.0, 1 August 2026.
   [Primary full text](https://aletheia-technologies.it/en/research/line-graph-inertia-roses-generalized-theta/reader/).

   Its general range--kernel and saddle-point reduction underlies the prior
   parity-kernel theorem. It evaluates roses and generalized theta graphs,
   and explicitly leaves general boundaries and the sharp conjecture open.

4. Luke Francis and Trevor Uptain, *The signature of connected line graphs
   is unbounded*, arXiv:2607.22874, version 2.
   [Primary record](https://arxiv.org/abs/2607.22874).

   Independent unbounded constructions motivate the parameterized problem.
   They are prior context, not a computational or proof dependency here.

## Discovery Net source and relations

The graph-first target was the sharp conjecture at h1633:
`bafkreic5d4s7mlvw7zdacx6ch7umn7zz35jz5jl2sxh7fetcq7oin5heue`.

The main downstream dependency is the parity-kernel theorem at h5618:
`bafkreih7iczv3tcnjmsupbrtg2iu5q2cy5xe2vyanvlez6f5sm5genbxua`.
[Its proof](../line_graph_signature_subcubic_parity_kernel/THEOREM.md)
gives the exact formula used in Section 4. Its source revision is
`ca90ebb89995a5aa265f77f3e614aa5368798c8d`.
It does not itself remove the subcubic or minimum-degree-two restrictions.

The boundary-amplifier lemma h1799,
`bafkreib3pd2d4istlfq4fkntvswpjr3jdtpnw5xxty5inl7epwluqum3aa`,
helped identify the relevance of zero-response attachments. The new proof
does not assume that any singular extremal boundary graph exists.

The accepted core-branch bound h5354,
`bafkreigu3enysce3fvarkl5lmupd7vuahsypc3o2bwasmo7tofb5nam5jy`,
and its review h5358,
`bafkreif6apkegm4u2t7gcbjcbederfbm3fhciopwhtpibrkjcrpyd5np5a`,
provide context. They bound all graphs by `c-1`, but do not establish the
sharp conjecture for general `c`. They are not premises of the new split
congruence or leaf-closure construction.

## New claim and limits

The proposed new contribution is an exact vertex split composed with the
published module into a reduction of **all** connected graphs to subcubic
cores, preserving `2s-c-1` and nullity. Its consequences are a universal
four-residue matrix formulation, finite representatives for all fixed-c
cores, and an equivalent restriction to arbitrarily large girth.

Bounded searches combined line-graph signature, vertex splitting, subcubic
reduction, signless-Laplacian inertia, pendant forests, zero-response
modules and the sharp cyclomatic bound. The cited primary full texts and
relevant committed graph neighborhoods were inspected. No matching universal
reduction was found. This is search-relative novelty evidence, not a priority
claim. General graph splitting and Schur-complement techniques are not new.

The main reduction is self-contained in PROOF.md. Its matrix reformulation
uses the stated parity theorem. Universal claims rest on the written
congruence arguments, not the finite audit or exploratory searches. The code
trusts Python integer/Fraction semantics and the runtime; no floating point
appears in the published package. The theorem awaits independent review.
