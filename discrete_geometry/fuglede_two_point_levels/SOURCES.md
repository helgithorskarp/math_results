# Sources, theorem alignment, and novelty boundary

Checked 2026-09-22. This package treats a specified family inside the committed
finite Fuglede frontier. No claim of global priority or a solution of the
general five-prime problem is made.

1. Gergely Kiss, Romanos-Diogenes Malikiosis, Gabor Somlai, Mate Vizer,
   *Fuglede's conjecture holds for cyclic groups of order pqrs*, Journal of
   Fourier Analysis and Applications (2022).
   [Primary preprint, Theorem 1.4](https://arxiv.org/pdf/2011.09578).
   The theorem gives spectral-to-tiling for a product of four distinct primes.
   Applied to `210=2*3*5*7`, it excludes a 22-point spectral base, because a
   22-point tile would require `22 | 210`. This is the only non-elementary
   imported theorem used in the 2310 corollary. The general descent-or-binary
   theorem does not use it. Section 2.1 supplies standard finite spectral-pair
   definitions and duality.

2. Gabor Somlai, *Fuglede's Conjecture on Cyclic Groups of Square-Free Order:
   The Case of Rapidly Growing Prime Factors* (2026).
   [Primary text, Proposition 3.2](https://arxiv.org/html/2607.26534).
   For `p>n` and a spectral pair of cardinality `p*ell`, that proposition
   proves equal level sizes and a common `ell`-point spectrum for all levels.
   Its large-prime assumption does not apply to `(n,p)=(210,11)`. Here we
   assume two-point levels at the outset, allow either size order, and prove
   a descent-or-common-character alternative. The coefficient argument and
   the aim of obtaining common level spectra belong to existing machinery;
   neither is claimed as new. Its Sections 2--3 were compared directly.

3. Romanos-Diogenes Malikiosis, *On the structure of spectral and tiling
   subsets of cyclic groups*, Forum of Mathematics, Sigma 10 (2022), e23.
   [Primary preprint](https://arxiv.org/pdf/2005.05800).
   Sections 2--5 develop the established mask-polynomial, cyclotomic, and
   vanishing-root framework. Theorem 1.4 treats specified two-prime-power
   ranges and Theorem 1.5 a tiling-to-spectral direction. They are background,
   not replacements for the family-specific necessity proved here.

4. The earlier Discovery Net full-prime-fiber theorem and its accepted review:
   theorem `bafkreia2hg54t53iddfbtpklyrcvtle6xlitvgbdpxhsprmflft6kyy2ay`,
   review `bafkreig3icskdrrza34jxrnfrghqg2ksbx5xqesz53e7rxfynuvgkip4hi`.
   [Public proof and verifier](https://github.com/helgithorskarp/math_results/tree/main/discrete_geometry/fuglede_full_prime_fiber).
   That theorem assumes a contained full prime fiber and excludes `p`-point
   spectra in the base. The present family assumes two-point levels directly
   and its conditional classification excludes `2p`-point base spectra.
   The scope is different. In particular the current 2310 fixture has no
   full prime fiber. The binary normal form and half-residue tiling
   construction were already used there; the new proposed step is their
   necessity without a contained prime fiber, through the two-matching
   argument, together with the precise spectral-descent alternative.
   Elementary exact polynomial and clique routines in `verify.py` are
   adapted from that verifier, as credited in the code.

The elementary facts that a nonzero sum of two unit complex numbers fixes
the pair, and that roots of order prime to `p` remain distinct under reduction
in characteristic `p`, are classical. They are proved here for self-contained
checking, not asserted as original results. The proposed contribution is
the combined structural family theorem and the resulting complete-residue
criterion at order 2310. Targeted primary-literature and committed-neighborhood
checks found no exact matching statement; this is a bounded search, not a
priority certificate.
