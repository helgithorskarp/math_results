# Sources and literature-status check

Checked 2026-09-21 UTC.

## Primary sources

1. Hugo Jenkins, *Repeated Binomial Coefficients and High-Degree Curves*,
   **Integers 16** (2016), A69; arXiv:1411.4111.
   <https://arxiv.org/abs/1411.4111>

   This is the direct source for the fixed-offset curves.  It proves that
   `binom(x,y)=binom(x-r,y+s)` has finitely many natural-number solutions when
   `r != s`.  In Section 3 it checks that the `r=s=2` plane curve is
   nonsingular of genus three, hence has finitely many integral points.  In
   Section 4 it names extension to `r=s>1` as the missing direction.  It does
   not state the exact integral classification proved here.

2. Kaisa Matomaki, Maksym Radziwill, Xuancheng Shao, Terence Tao, and Joni
   Teravainen, *Singmaster's conjecture in the interior of Pascal's triangle*,
   **Quarterly Journal of Mathematics 73** (2022), 1137--1177;
   arXiv:2106.03335. <https://arxiv.org/abs/2106.03335>

   This establishes bounded multiplicity in a large interior region and
   confirms that the global bounded-multiplicity conjecture remains open.  It
   does not give the fixed-offset-two classification.

3. David Singmaster, *How Often Does an Integer Occur as a Binomial
   Coefficient?*, **American Mathematical Monthly 78** (1971), 385--386.
   <https://doi.org/10.1080/00029890.1971.11992769>

   This formulates the bounded-multiplicity problem to which the fixed-offset
   program belongs.

## Search boundary

Web and bibliographic searches were run for the exact equations
`binom(x,y)=binom(x-2,y+2)` and `C(x,y)=C(x-2,y+2)`, for the phrases
"fixed-offset repeated binomial coefficients" and "a=b=2", and for works
citing Jenkins's title.  The searches returned Jenkins's paper but no later
source claiming an exact solution of this curve.  Because search indexes can
miss differently notated or non-digitized results, the contribution claims an
independently derived classification and reports the negative search; it does
not claim priority beyond that evidence.
