# Primary sources and novelty scope

Checked on 2026-09-26.

1. Masato Konoike, *On the magic positivity of Ehrhart polynomials of
   dilated polytopes*, arXiv:2504.21395v1, 30 April 2025.
   [Abstract and version history](https://arxiv.org/abs/2504.21395),
   [Section 5.2](https://arxiv.org/html/2504.21395v1#S5.SS2).
   Question 5.5 asks whether the index is $n-k$ for
   $1\le k\le\lfloor n/2\rfloor$. Proposition 5.4 gives ranks 1 and 2.
   The arXiv version history listed only v1 at this check.

2. Luis Ferroni, *On the Ehrhart Polynomial of Minimal Matroids*,
   Discrete & Computational Geometry **68** (2022), 255–273;
   [published article](https://doi.org/10.1007/s00454-021-00313-4),
   [arXiv:2003.02679](https://arxiv.org/abs/2003.02679),
   [HTML Section 3](https://arxiv.org/html/2003.02679#S3).
   Proposition 2.2 supplies the graphical realization; Proposition 2.6
   describes its base polytope. Theorem 3.1 gives the binomial-basis
   Ehrhart formula. Lemmas 3.2–3.3 and Corollary 3.4 give the residual
   factorization. This is equation (3.11) in the arXiv HTML and (3.12)
   in the published article. Corollary 4.1 already gives real-rootedness
   of the h*-polynomial, a different polynomial from the Ehrhart
   polynomial studied here.

The new deduction claimed here is the complete sharp magic-index
statement, including its extension to real dilation parameters. The
sign identity and residual-root description provide its short proof.
The binomial identities, minimal-matroid realization, and Ehrhart
factorization are explicitly treated as existing mathematics. We make
no claim to have discovered the known h*-real-rootedness result.

Targeted searches included the exact question number and author,
"minimal matroids" with "magic", "interlacing", "Ehrhart roots",
"real-rooted Ehrhart", and "negative roots", and the related
"pyramid over a product of simplices" terminology. No prior resolution
or equivalent root-location theorem was located. This is a bounded
negative search, not proof of priority or an exhaustive literature review.
The status is therefore **a complete proof apparently new to the
searched sources, awaiting independent review**.

## Informative failed shortcut

The factored Ehrhart formula is a positive sum of binomial polynomials
of different degrees. It is invalid to infer magic positivity by adding
those terms, because magic positivity depends on the degree of the
basis. For instance, $1$ and $x+1$ are magic positive but their sum
$x+2=2(x+1)-x$ is not. The proof instead establishes the real roots
or uses the equal-degree positive interpolation identity (5).

## Next research checkpoint

The selected Question 5.5 has a complete argument. The next pass should
first check reviewer objections and newly overlapping work. If no repair
is needed, return to the literature-first selector; Question 5.7 in
Konoike's paper is an adjacent but separate candidate. The present
argument does not establish any general magic-index formula for
arbitrary matroid or multipartite edge polytopes.
