# Primary-source and attribution audit

Checked 22 September 2026.

1. Gautam Aishwarya and Dongbin Li, **The Kneser--Poulsen phenomena for
   entropy**, IMRN 2025(12), rnaf140.
   [Journal](https://academic.oup.com/imrn/article/2025/12/rnaf140/8160080);
   [author manuscript v3, 14 July 2025](https://arxiv.org/html/2409.03664v3).
   Theorem 1.5 gives the Gaussian Rényi contraction comparison, with a
   first-moment assumption below order one. Section 3, particularly
   equations (18)--(25), supplies the posterior-divergence argument and
   doubled-dimensional contracting path. These are credited methods.

2. Gautam Aishwarya and Dongbin Li, **Gaussian Convolution, Internal
   Energies, and the Kneser--Poulsen Conjecture**,
   [arXiv:2609.07041v2, 13 September 2026](https://arxiv.org/html/2609.07041v2)
   ([version history](https://arxiv.org/abs/2609.07041)).
   Theorem 1.3 and Examples 2.8(ii) already imply the moment-free
   comparison at every finite positive Rényi order. Its Theorem 1.2
   treats full majorization in dimension two, and Theorem 1.12
   characterizes Gaussian kernels through infinitesimal volume
   contraction. That kernel characterization differs from the present
   characterization of entropy equality for a fixed input and map.
   The displayed results and proofs were inspected; the present
   rigid-motion error bound and posterior maximum-density estimate
   were not located. The preprint is prior work, not a peer-reviewed
   acceptance of the present proof.

3. Gautam Aishwarya, Irfan Alam, Dongbin Li, Sergii Myroshnychenko, and
   Oscar Zatarain-Vera, **Entropic exercises around the Kneser--Poulsen
   conjecture**, Mathematika 69(3) (2023), 841--866.
   [Journal](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/mtk.12210);
   [author manuscript](https://arxiv.org/abs/2210.12842).
   Theorem 4.2 includes order-two comparison for radial log-concave
   noise. Its discussion of stability across Rényi orders is a
   different question from distance to rigid motions.

The path (5) is classical (Alexander's higher-dimensional motion;
Bezdek--Connelly, *Pushing disks apart*, Lemma 1), and is reproduced
explicitly in source 1. The proof here verifies its identities directly,
without importing a geometric theorem about unions of balls.
The integer-order Gaussian replica integral used by the checker follows
by completing the square; related formulas also occur in source 2.

Live searches included the paper titles and combinations of
Kneser--Poulsen, entropy, equality, rigidity, stability, and quantitative
rigidity. Source 2 was discovered during the audit, correcting the initial
impression from source 1 that moment removal was still open.
Neither the known qualitative comparison nor that removed hypothesis is
claimed as new. The proposed novelty is the complete equality statement,
the all-order quantitative bound with sharp exponent, and the sharp
posterior coefficient. A bounded search does not establish historical
priority or replace expert review.
