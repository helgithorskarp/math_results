# Positive Gaussian channels require affine means

[PROOF.md](PROOF.md) closes a proposed semigroup factorization for the
dimension-three Gaussian-majorisation campaign. A Markov kernel taking
every translate of one Gaussian covariance on an open convex set to a
Gaussian of fixed covariance has an affine mean map. Up to null sets,
the kernel must be the corresponding affine Gaussian channel. This
requires no Feller assumption and permits singular output noise.

The proof uses Holder's inequality for positive Gaussian transforms,
then analytic continuation and injectivity of Gaussian convolution.
It also supplies a finite obstruction with a positive error bound:

```text
source means: (-1,0,0), (0,0,0), (1,0,0)
target means: (1/2,0,0), (0,0,0), (3/4,0,0)
common covariance: I_3
every Markov kernel has maximum labelled TV error > 1/648.
```

The map is an injective strict contraction on these three sites. Every
prior on the sites still satisfies Gaussian majorisation by the known
dimension-one theorem. The error is for a **single channel required to
work for all priors**, not for majorisation. Prior-dependent couplings,
nonlinear common-set choices, and the unresolved heat-contact sign are
not excluded.

Gaussian-preserving operator rigidity is classical. [SOURCES.md](SOURCES.md)
compares the fixed-covariance statement with a primary classification
source and records the relevant team dependencies. No priority claim
or independent mathematical acceptance is made. The full conjecture
remains open.

Compact exact checks, CPython 3.11 or later, standard library only:

```sh
python3 audit.py --check EXPECTED.json
python3 -O audit.py --check EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `GAUSSIAN_CHANNEL_OBSTRUCTION_CONSTANTS_PASS`.
The program verifies all three strict distance inequalities, distinct
target labels, the two slab likelihood exponents, and rational Taylor
bounds used for the constant 1/648. It is not a proof assistant or a
test of the unrestricted majorisation conjecture. No numerical
integration, optimizer, search corpus, or external runtime package is
required.
