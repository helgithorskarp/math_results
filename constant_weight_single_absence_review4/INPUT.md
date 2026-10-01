# Inputs and provenance

The only input to the independent theorem computation is [input.json](input.json), the literal twenty-quadruple packing Q on0,...,16, with x14,y17. These bytes are the frozen mathematical premise from six-code-3's source commit **dff39045011d66f45ab84a3aaa5e5a254ef00141**, directory `coding_theory/a18_6_5_single_absent_sharp16`. Input file SHA256:

`f2a577cc13f865e8400fea7d0a09e9099edf187743d9cf109110f04400b35fe6`.

The shortened y star has profile(4^5,5^12); high points0,1,3,6,14; high leave is C4 on the first four with marked x14 isolated. Its uncovered x neighbors are2,9,15,16. Our code checks these facts and tests every labeled neighbor, with no orbit reduction. Q is an existing template credited to Stanton--Street1987, not a newly discovered packing in this review. The historical case-to-label isomorphism is credited to the target and the earlier independently reviewed classification; this pass does not claim a new historical identification.

The broader marked-star interpretation imports classification8350, source **43dc0a95a2232b6b9ff1e85d18a1a34fe5705bbc**, independently reviewed8401 by six-reviewer-5, source **b45ab435bac5ce32ee8ef711bdc879497f3044b6**. This pass read that premise and review and does not repeat the already sufficient whole classification. The literal Q result requires none of its computed classifications or automorphism output.

[AUTHOR_INPUT.json](AUTHOR_INPUT.json) records all14 frozen author file sizes and SHA256 digests used for supplementary replay. Author `manifest.json` file digest d4d1749b094946ab308e58efb7376553ce56198160d4f146cfc06c6360b251ad was reproduced byte for byte. Author witness file digest542feecc290d72c48b7ba10d100a0f54599623503ac5bb63c45554e7d9614265 was verified.

Our internal array digests use sorted-key compact JSON **without** a final newline. The author canonical-word digest uses the same encoding **with** a final newline. They are different serialization conventions and are never equated. File hashes in SHA256SUMS hash the actual complete file bytes.
