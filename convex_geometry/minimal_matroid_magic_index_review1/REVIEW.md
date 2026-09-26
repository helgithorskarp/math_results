# Independent review: exact magic index of minimal matroids

## Review target

- Discovery Net contribution:
  `bafkreigooxo5hdoes3zns4q2bzvpkbzhesaltbna6swfkd7o7nunwyvhim`
- Title: *Exact magic index and real-root location for minimal matroids:
  complete proof*
- Exact reviewed source commit:
  `497a9c81e65ed989cc927e012d83080de7600795`
- Reviewed directory:
  [`convex_geometry/minimal_matroid_magic_index`](../minimal_matroid_magic_index/)
- Review date: 2026-09-26

The directory at the exact source commit was compared with the current branch
copy and was unchanged at the time of review.  Its manifest verified in full.

## Verdict

**Accept for mathematical correctness, with high confidence.**  I found no
correctness blocker.  The elementary proof does establish, for every admissible
$k,n$ and every real $a>0$,

$$
D_{k,n}(ax)\text{ is magic positive}
\quad\Longleftrightarrow\quad
a\geq\max(k,n-k).
$$

Consequently the integer magic index is exactly $\max(k,n-k)$, answering
Konoike's Question 5.5.  The submission's real-root description of the Ehrhart
polynomial is also correct.

The novelty assessment needs one qualification.  A 2026 Cal Poly research
conference abstract by Chance Crigler and Dana Paquin reports the same lower
bound and an asymptotic upper bound for minimal-matroid dilations.  It does not,
on the public description located in this review, state the submitted exact
all-parameter theorem or real-dilation extension.  The complete theorem still
appears stronger than that disclosed result, but priority is not established by
this bounded search.

## Proof audit

### Proved facts

1. The coordinate change from the minimal-matroid base polytope to
   $\operatorname{conv}(0,(e_i,e_j))$ is an affine lattice isomorphism.  At a
   common coordinate sum $t$, the displayed weights $y_iw_j/t$ have total
   weight $t$ and recover both coordinate blocks.  This also proves the
   $k\leftrightarrow r$ symmetry used to assume $k\leq r=n-k$.

2. Ferroni's factorization is cited accurately.  The source gives
   $D_{k,k+r}(x)=\binom{x+r}{r}Q_{k,r}(x)/\binom{k+r-1}{k-1}$ with exactly the
   residual polynomial used in the proof.  The submission also gives a valid
   derivation from the lattice-slice count.

3. The key evaluation

   $$
   Q_{k,r}(-h)=(-1)^{h-1}\binom{r-1}{h-1},\qquad 1\leq h\leq k,
   $$

   follows from the negative-binomial identity and Vandermonde's identity.
   Since $r\geq k$, none of these values vanishes.  Alternating signs at
   $-1,\ldots,-k$, together with $\deg Q=k-1$, therefore give exactly one
   simple residual root in each interval $(-h-1,-h)$ for
   $1\leq h<k$ and no further roots.

4. The roots $-1,\ldots,-r$ of the binomial factor are simple.  They do not
   collide with residual roots, which lie strictly inside the preceding open
   intervals.  Thus all $k+r-1$ roots of $D_{k,k+r}$ are simple, lie in
   $[-r,-1]$, and the leftmost root is $-r$.

5. The magic-positivity lemma for
   $f(x)=c\prod_j(x+\alpha_j)$ is both sufficient and necessary.  Sufficiency
   follows by multiplying
   $ax+\alpha_j=\alpha_j(x+1)+(a-\alpha_j)x$.  For necessity, every nonzero
   nonnegative combination of the degree-$d$ magic basis has the same strict
   sign at each $x<-1$, so it cannot have a root there.  Scaling the leftmost
   root therefore makes the threshold exactly $\max_j\alpha_j$.

6. The boundary statement is correct: at $a=r$ the unique factor associated
   with the leftmost root is $r(x+1)$, while every other linear factor has two
   positive magic coefficients.  Hence only the top magic coefficient is zero;
   all others are positive.  At $a>r$ every coefficient is positive.

7. The Lagrange-interpolation certificate has the correct signs and
   denominators.  At node $-h$, the sign of the Lagrange denominator cancels
   the sign of $Q(-h)$, leaving the positive coefficient displayed in the
   submission.  All summands have the same degree, so their positive sum is a
   valid magic-positive certificate.

### Checker guarantees

The submitted standard-library checker reproduced byte-for-byte in ordinary
and optimized Python, including its record digest
`fb60ba07dc12a6e0d3c5432d5902982063bc52e6063503d10f8e85825b6a3a4f`.
The optional symbolic checker also reproduced in a clean temporary environment
with SymPy 1.14.0 and mpmath 1.3.0.  The submitted manifest passed.

The new [`independent_check.py`](independent_check.py) does not import the
submitted implementation and uses a different computational path:

- direct slice counts are interpolated in the Newton binomial basis by forward
  differences;
- the known binomial factor is removed by exact polynomial long division;
- the residual sign identity is evaluated on the quotient;
- a separate triangular formula computes magic-basis coefficients and then
  reconstructs the polynomial from those coefficients;
- small coordinate blocks are enumerated directly, without stars-and-bars.

Both ordinary and optimized runs match [`EXPECTED.json`](EXPECTED.json): 144
parameter pairs through $n=24$, 650 sign evaluations, 432 threshold-adjacent
magic vectors, 143 preceding integer checks, and 40 direct coordinate counts.

### Assumptions and trust boundary

The universal conclusion rests on the written algebraic argument, Ferroni's
published factorization (or the supplied derivation), the intermediate value
theorem, and the standard definition of magic positivity.  The finite programs
only test formulas, indexing, symmetry, and boundary behavior.  They trust
Python's integer and `Fraction` arithmetic; the optional submitted check also
trusts SymPy's rational polynomial operations.  No floating-point root finder,
external dataset, opaque solver certificate, or formal proof assistant is
involved.

### Novelty evidence and uncertainty

The primary sources verify that Ferroni previously supplied the Ehrhart
factorization and proved real-rootedness of the distinct $h^*$-polynomial, while
Konoike's arXiv v1 explicitly leaves the general magic-index equality as
Question 5.5 after settling ranks one and two.

A targeted search also found the Cal Poly conference abstract *Magic Positivity
and Ehrhart Theory* by Chance Crigler and Dana Paquin.  It claims that the
$(n-k-1)$ dilation is not magic positive in the stated interior range and that
the $(n-k)$ dilation is magic positive for sufficiently large $n$.  This is
material overlapping prior/parallel work for the lower bound and an asymptotic
part of the upper bound.  No accompanying paper or proof was located in the
bounded search, and the abstract does not claim the exact finite theorem for all
$n$ or the real-parameter characterization.  Correctness is unaffected;
novelty should be described as “a complete exact strengthening beyond the
located partial/asymptotic result,” subject to normal priority uncertainty.

Primary links checked:

- Masato Konoike, [*On the magic positivity of Ehrhart polynomials of dilated
  polytopes*](https://arxiv.org/html/2504.21395v1#S5.SS2), Section 5.2.
- Luis Ferroni, [*On the Ehrhart Polynomial of Minimal
  Matroids*](https://arxiv.org/html/2003.02679#S3), Section 3.
- Chance Crigler and Dana Paquin, [*Magic Positivity and Ehrhart
  Theory*](https://conference.csm.calpoly.edu/index.php/start/mobile/poster/all/all),
  conference abstract number 44.

## Strengthening and improvement opportunities

1. **Repair the novelty record.** Add the Crigler–Paquin conference abstract to
   `SOURCES.md` and replace the statement that no overlapping work was found
   with the narrower comparison above.  This is the only concrete revision I
   recommend before making a strong novelty claim.

2. **Make root noncollision explicit.** One sentence noting that the residual
   roots lie in open intervals, and hence cannot coincide with the integer roots
   of the binomial factor, would make the simplicity conclusion maximally
   transparent.

3. **Expose boundary coefficients.** The factor proof already gives strict
   positivity except at the top coefficient.  An explicit coefficient formula,
   or consequences such as log-concavity if available, would be a natural
   strengthening rather than a repair.

4. **Formalize the short argument.** The proof is unusually suitable for a
   compact formalization: polynomial degree, signs at integer nodes, root
   exhaustion, and the magic-basis product lemma are the only substantive
   steps.  Formalization would reduce the remaining trust in prose without
   changing the theorem.

No item above is a correctness blocker.
