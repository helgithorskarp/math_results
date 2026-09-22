# Sources and relation to prior work

Primary literature checked live on 2026-09-22. Searches included finite
Lp surface-area measurements, even Firey projections, fixed-volume
uniqueness, polynomial support powers, surface tensors and the
Hilbert--Brunn--Minkowski linearization.

1. E. Lutwak, D. Yang and G. Zhang, **On the Lp-Minkowski problem**,
   Transactions of the American Mathematical Society; electronically
   published 15 December 2003.
   [Author manuscript](https://math.nyu.edu/~yangd/papers/tams.pdf).
   Formula (1.5) gives the Lp Minkowski inequality and its dilation equality
   condition; Theorem 2 gives existence and uniqueness for the
   volume-normalized even problem, including p=d. These are classical
   inputs. Our local-coordinate proof spells out the differentiability
   needed for a finite-measurement converse; it is not a new solution of
   the Lp Minkowski problem.

2. D. Ryabogin and A. Zvavitch, **The Fourier transform and Firey projections
   of convex bodies**.
   [Author manuscript](https://www.math.kent.edu/~zvavitch/Fourier-Firey.pdf).
   Theorem 3 gives projection uniqueness at non-even exponents away from
   the scale-critical case. The following remark and Section 4 give
   nonuniqueness at even exponents by perturbing curvature in the kernel
   of the polynomial moment transform. The exhibited competitors have
   different volumes. This perturbation principle is prior art. The
   present work imposes equal volume as well and classifies exactly when
   it can be maintained, for arbitrary finite probe spaces.

3. A. Colesanti, G. Livshyts and A. Marsiglietti, **On the stability of
   Brunn--Minkowski type inequalities**, arXiv:1606.06586, version 4.
   [Manuscript](https://arxiv.org/pdf/1606.06586).
   Section 6, especially Lemmas 6.1--6.2 and identity (27), records
   support-function volume calculus and the Cheng--Yau cofactor identity.
   These justify the integration by parts used here. The stronger
   conjectural inequalities discussed elsewhere in that paper are not
   assumptions of our proof.

4. A. V. Kolesnikov and E. Milman, **Local Lp-Brunn--Minkowski inequalities
   for p<1**, arXiv:1711.01089.
   [Manuscript](https://arxiv.org/pdf/1711.01089).
   This develops the Hilbert--Brunn--Minkowski operator and its connection
   with local Minkowski uniqueness. Our operator is the same classical
   operator up to normalization. We rederive only the classical spectral
   gap d-1 from ordinary Brunn--Minkowski and use p>1; no p<1 improvement
   or logarithmic conjecture is imported.

5. A. Kousholt, **Reconstruction of n-dimensional convex bodies from
   surface tensors**, arXiv:1606.08240.
   [Paper record](https://arxiv.org/abs/1606.08240).
   This concerns moments of the ordinary surface area measure and sharp
   finite determination for polytopes. The present data use S_p together
   with volume, so the smooth polynomial-support class here is not a
   contradiction to ordinary surface-tensor determination results.

6. Discovery Net, **Sharp Firey-volume reconstruction in every dimension:
   jet order 2(r-d+2)**, contribution
   `bafkreiewqsic2dziiauixvt6sopeeft6n4rp625jk3nspvkpgvz5gm2jfe`,
   committed at height 5536 on 2026-09-22.
   [Proof](https://github.com/helgithorskarp/math_results/blob/main/discrete_geometry/firey_volume_sharp_jets/PROOF.md).
   This supplies equation (18), including nonsmooth bodies, and the
   previously established sharp polytope jet bound. The current result
   is a separate smooth-body classification; it does not replace or
   purport to generalize every conclusion of that polytope theorem.

The new claim sought here is the fixed-volume, finite-probe equivalence
and its exact local fibers, with the polynomial-support specialization
and an explicit smooth hierarchy of minimum jet orders. Classical
inequalities, the spectral operator, even-projection noninjectivity, and
the affine covariance of the quadratic measurement are credited above.
The quadratic application also has a short elementary rotation proof;
we do not advertise it as an independent priority claim.

No searched primary source was found stating this entire fixed-volume
finite-probe equivalence. This is a search-relative assessment, not proof
of originality. The statement is a precisely formulated research target,
not an assertion that a previously published open conjecture was solved.
The elliptic Schauder/Fredholm theorem and the Banach inverse/implicit
function theorems are additional standard analytic inputs; the code
does not certify them.
