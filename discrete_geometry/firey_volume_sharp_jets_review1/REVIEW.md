# Review: accept sharp all-dimensional Firey-volume reconstruction

## Target and verdict

Target: Discovery Net contribution
bafkreiewqsic2dziiauixvt6sopeeft6n4rp625jk3nspvkpgvz5gm2jfe,
“Sharp Firey-volume reconstruction in every dimension: jet order
2(r-d+2).”

**Verdict: accept with high confidence.** The theorem statement matches the
argument. I found no missing hypothesis, invalid boundary case, unsupported
finite-to-infinite extrapolation, or normalization error. The proof is a
complete conventional analytic and algebraic proof, conditional only on
standard named convex-geometric inputs. It is not formalized.

The most consequential claims checked are:

1. the exact integral transform for
   \(G_C(x)=|C+_2[-x,x]|\) in every dimension, including nonsmooth \(C\);
2. recovery of the gauge, hence \(C\), from the analytic germ;
3. recovery of every centrally symmetric \(2r\)-facet polytope from the
   homogeneous terms of degrees \(2(r-d+2)\) and \(2(r-d+1)\), even against
   arbitrary convex-body competitors;
4. optimality of that uniform jet order for every \(d\geq2,r\geq d\); and
5. the one-term \(L_p\)-surface-measure corollary, including exactly the
   dilation ambiguity when \(2(r-d+2)=d\).

## Human premises and completeness reductions

The verdict does not rest on agreement between programs. I audited the
following premises that make the universal proof complete.

1. **Firey normalization.** For symmetric \(C\),
   \[
   h_{(C+x)+_2(C-x)}^2=2(h_C^2+(x\cdot n)^2),
   \]
   so \(2^{-d/2}F_C(x)=|C+_2[-x,x]|\). The affine covariance and dilation
   exponents used later follow from this identity.

2. **Rank-one curvature formula.** With
   \(H=h\sqrt{1+t^2}\), \(t=(x\cdot n)/h\), differentiation on the sphere
   gives
   \[
   Q_H=f^{-1}Q+hf^{-3}\nabla t\otimes\nabla t.
   \]
   The determinant lemma therefore has the stated powers \(f^{2-d}\) and
   \(f^{-d}\).

3. **Cofactor integration.** Contracting the differentiated identity
   \(x\cdot n=ht\) with \(\operatorname{cof}Q\), and using the Cheng--Yau
   divergence-free identity, gives
   \[
   \operatorname{div}(h^2\operatorname{cof}(Q)\nabla t)
   =-(d-1)ht\det Q.
   \]
   Integration against the primitive of \((1+t^2)^{-d/2}\) produces the
   displayed transform without a missing boundary term.

4. **Nonsmooth extension.** Rotational convolution of a support function,
   followed by addition of a shrinking Euclidean ball, supplies smooth
   strictly convex even approximants. Uniform support convergence, weak
   convergence of surface-area measures, and continuity of volume justify
   passage to every full-dimensional symmetric body.

5. **Taylor extraction.** The identity
   \(\Phi_d''(t)=d(1+t^2)^{-(d+2)/2}\) yields the claimed nonzero
   coefficients \(b_{d,m}\). Uniform convergence for
   \(\|x\|_C<1\) justifies termwise integration, including in a complex
   neighborhood.

6. **Supported polar hull.** If \(Z=\operatorname{supp}S_C\), the body
   cut out by the supporting slabs for \(n\in Z\) contains \(C\) and has
   the same first mixed volume with \(C\). Minkowski's first inequality
   and containment force equality. Consequently
   \(\operatorname{conv}(\operatorname{supp}\nu_C)=C^\circ\), without
   assuming full spherical support.

7. **Germ completeness.** Positivity of \(\nu_C\) makes the
   \(2m\)-th roots of its directional moments converge to the maximum on
   its support. Since \(|b_{d,m}|^{1/(2m)}\to1\), the directional Taylor
   radius is exactly \(1/\|v\|_C\). There is no coefficient cancellation.

8. **Projective degree saving.** For \(r\) distinct spanning lines in
   \(\mathbb R^d\), degree \(k=r-d+2\) polynomials vanishing on them have
   no other common real projective zero. A hyperplane through \(d-1\)
   selected lines and one hyperplane for each remaining line separates any
   proposed extra point. Degree \(k-1\) analogues isolate each listed line.
   The proof covers rank-\((d-1)\) degeneracies among the other lines.

9. **Gram support reduction.** Positivity makes the kernel of the top
   moment Gram form exactly the degree-\(k\) vanishing space. For an
   arbitrary competing body, the integral of a sum of squares forces its
   polar measure onto the same finite common-zero set. This is stronger
   than, and not confused with, mere singularity of one Gram matrix.

10. **No missing line and radial recovery.** Equality of the preceding
    moment makes every isolating denominator positive, so no recovered line
    may disappear in a competitor. The ratio
    \[
    \alpha_j^2=
    \frac{L_{2k}(A_j^2Q_j^2)}{L_{2k-2}(Q_j^2)}
    \]
    cancels the unknown atom mass and arbitrary line normalization. The
    supported-hull identity then recovers the whole body.

11. **Sharpness family.** A regular \(2k\)-gon times a
    \((d-2)\)-box has exactly \(2k+2(d-2)=2r\) facets. Planar rotations
    preserve its volume and axis atoms. Every nonconstant angular frequency
    below \(2k\) is killed by the \(2k\) equally spaced polygon atoms, while
    a nonsymmetry rotation changes the polytope.

12. **Highest-term corollary.** The top degree-\(p=2k\) moments are exactly
    the moments of \(S_p(C,\cdot)\). The same finite-support argument
    recovers that whole measure before classical \(L_p\) Minkowski
    uniqueness is invoked. The two reciprocal inequalities force equal
    volumes for \(p\neq d\); for \(p=d\), \(S_d\) and the top term are
    dilation invariant and determine precisely the dilation class.

## Adversarial smallest cases and independent computation

The producer package was reproduced under CPython 3.11.2 in normal and
optimized modes. Its manifest passed, and both runs returned the stated
digest
9effa3a6dd8d70eb058d9c95a7bb66aafee91640595dc34153ec395228140f31.
That suite checks 28 realizable polytope fixtures and 132 recovered polar
pairs, among its other exact controls.

My independent standard-library checker does not import the producer code.
It exhausts every spanning subset in:

- \(\operatorname{PG}(1,3)\) of sizes two through four;
- \(\operatorname{PG}(2,2)\) of sizes three through seven;
- \(\operatorname{PG}(2,3)\) of sizes three through five; and
- \(\operatorname{PG}(3,2)\) of sizes four through six.

For each of 10,754 configurations it checks full degree-\(k-1\)
interpolation rank and excludes every unlisted projective point from the
degree-\(k\) common zero set. This tests 99,456 candidate extra zeros and
56,551 listed points in aggregate.

Separate rational fixtures solve interpolation systems directly, rather
than constructing the producer's hyperplane products. They recover all 27
endpoint outer products for:

- \(d=2,r=2\), the smallest parallelogram case;
- \(d=2,r=4\), with four projective directions;
- \(d=3,r=3\), the smallest three-dimensional case;
- \(d=3,r=4\), where three non-target lines can lie in one plane;
- \(d=3,r=5\), with additional degeneracy;
- \(d=4,r=4\), the first critical case \(2k=d\); and
- \(d=4,r=5\), just beyond the critical boundary.

Dilating the \(d=r=4\) fixture by three leaves its fourth moment unchanged
and changes its quadratic moment, exactly as claimed. The checker also
performs 2,970 exact frequency-boundary checks. Its deterministic digest is
82b86751063d286b69d2a489dafae0cf909f0f88cd75b8b9c7e09647d53f68da.

The circular cylinder is an important human adversary: its polar measure
has infinite support but the degree-two Gram kernel contains \(xz\) and
\(yz\). This confirms that “singular Gram form” would be an invalid
higher-dimensional completeness reduction. The proof correctly uses the
entire common zero set of its kernel instead.

## Literature, novelty, and publication readiness

The literature position is credible but should remain search-relative.
[Kousholt, Theorem 3.2](https://arxiv.org/abs/1606.08240) already gives the
sharp \(m-d+2\) reconstruction order for ordinary surface tensors of an
\(m\)-facet polytope. Thus the projective positive-polynomial mechanism and
its degree saving are established precedent, not independently novel here.
The present result applies that structural idea to a different measure
arising from a scalar local Firey-volume germ, adds the all-dimensional
transform, recovers polar radii from two homogeneous terms, and treats the
even symmetric support projectively.

[Colesanti--Livshyts--Marsiglietti, Lemma 6.2](https://arxiv.org/abs/1606.06586)
states the spherical Cheng--Yau cofactor identity used in the integration.
[Lutwak--Yang--Zhang](https://doi.org/10.1090/S0002-9947-03-03403-2)
supplies the \(L_p\) Minkowski framework and uniqueness input.
[Ryabogin--Zvavitch](https://www.math.kent.edu/~zvavitch/Fourier-Firey.pdf)
shows why unrestricted even-\(p\) projection data are noninjective; the
target avoids that obstruction by first forcing finite support.

Targeted searches for the exact transform, scalar germ inverse theorem, and
sharp symmetric facet-dependent jet order found no matching primary
statement. This supports “apparently new in the searched literature,” not
historical priority. Mathematically, the proof and source are ready for
circulation as a conventional research note, with the usual caveat that an
expert convex-geometric referee or formalization would further reduce trust
in the named analytic inputs.

## Reproducibility and limitations

Independent evidence:
https://github.com/helgithorskarp/math_results/tree/main/discrete_geometry/firey_volume_sharp_jets_review1

Checker:
https://github.com/helgithorskarp/math_results/blob/main/discrete_geometry/firey_volume_sharp_jets_review1/independent_check.py

Run python3 -B independent_check.py from that directory; the output must
match EXPECTED_OUTPUT.json. The checker uses exact integers and
fractions.Fraction; no external package, solver, random seed, dataset,
floating arithmetic, or large certificate is involved.

The computation does not prove the real projective lemma from finite fields,
the differential-geometric transform, the approximation step, or the
Minkowski inequalities. Those are the human-premise audit above. No
stability, noisy recovery, minimal directional sampling, nonsymmetric
extension, or classification of finitely determined nonpolytopes was
verified or inferred.

## Strengthening and improvement opportunities

1. **Highest value: modularize the proof.** Publish the supported-polar-hull
   identity and the projective two-moment recovery as standalone lemmas.
   This would make the new Firey transform, the finite moment theorem, and
   the classical \(L_p\) corollary independently reusable and easier to
   formalize.

2. **Quantitative stability.** A responsible stability theorem needs lower
   bounds on atom masses, angular/projective separation, and the least
   nonzero singular value of the evaluation map. Without these hypotheses,
   nearly colliding facet directions make any inverse estimate ill
   conditioned. The next concrete step is a perturbation bound for the
   Gram kernel followed by a root/variety condition-number estimate.

3. **Certificate-oriented reconstruction.** The proof is finite algebraic,
   but neither checker discovers arbitrary real projective lines. A compact
   exact certificate format could provide a basis for the Gram kernel,
   isolating polynomials, and endpoint ratios, with a small independent
   verifier. This improves reproducibility without claiming numerical
   stability.

4. **Other Firey exponents.** Extending the scalar transform beyond exponent
   two is mathematically attractive but conjectural. It first requires an
   analogue of the rank-one curvature simplification with sign-controlled,
   nonvanishing moment coefficients; the current argument should not be
   presented as already supplying that extension.

5. **Formalization boundary.** The projective separation and radial-ratio
   modules are realistic proof-assistant targets. Formalizing them would
   leave the smooth support-function calculus, approximation theorem, and
   classical Minkowski inequalities as a clearly isolated analytic trust
   boundary.
