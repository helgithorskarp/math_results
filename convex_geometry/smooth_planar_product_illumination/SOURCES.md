# Primary sources and attribution

Checked 2026-09-22. The proof in this directory is self-contained apart from
elementary convex separation and linear algebra. The sources below establish
context and known cases; they are not imported as unverified proof steps.

1. E. D. Baladze and V. G. Boltyanski, *Illumination of direct sums of two convex
   figures*, Beiträge zur Algebra und Geometrie 47(2) (2006), 345–350.
   [Official journal page](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.47/no.2/3.html);
   [full primary PDF](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.47/no.2/b47h2bal.pdf).
   The entire six-page article was inspected. Theorem 2 credits the equality
   $I(K_2\times L_2)=7$ for smooth planar bodies to the then-submitted paper in
   item 2. Theorem 3 gives a multiplication condition using pairwise antipodal
   boundary points, covering the classical interval factor. On page 349,
   Problem 4 asks for the illumination number of products of smooth bodies
   of prescribed dimensions. Our formula concerns only the two-factor
   dimensions $(d,2)$, and reproduces the known cases $d=1,2$. It does not solve
   their full Problem 4 or establish that this slice is currently open.

2. V. Boltyanski and H. Martini, *Illumination of direct vector sums of convex
   bodies*, Studia Scientiarum Mathematicarum Hungarica 44(3) (2007), 367–376,
   [DOI:10.1556/SScMath.44.2007.3.6](https://doi.org/10.1556/SScMath.44.2007.3.6).
   The bibliographic record and abstract were located; **the full text was not
   inspected**. The publisher's article, PDF and legacy PDF endpoints returned
   HTTP 405 in the local retrieval attempts; browser retrieval also failed.
   Crossref identified the publisher endpoints, while OpenAlex listed the work
   as closed access without a repository copy. This is a material gap in the
   priority audit, not evidence of novelty. No assertion here excludes the
   possibility that the higher-dimensional formula or its mechanism appeared
   in this paper or another uninspected source.

3. L. Rotem, A. Schejter and B. A. Slomka, *The complex Illumination problem*,
   Combinatorica 46, article 3 (2026),
   [full publisher article](https://link.springer.com/article/10.1007/s00493-025-00195-7).
   Theorem 1.4 and Section 2 establish the polydisc illumination number
   $2^{n+1}-1$. Remark 2.8 discusses an error in the earlier construction from
   item 2 and supplies the corrected argument. This is established prior work;
   its two-disk case is not claimed as new here. It also makes clear why
   boundary cases of open hemisphere covers require care.

4. S. Wu, B. Fan and C. He, *Covering functionals of Minkowski sums and direct
   sums of convex bodies*, Mathematical Inequalities & Applications 23(3)
   (2020), 1145–1154,
   [primary PDF](https://files.ele-math.com/articles/mia-23-88.pdf),
   [DOI:10.7153/mia-2020-23-88](https://doi.org/10.7153/mia-2020-23-88).
   The direct-sum section was inspected as a later primary source citing
   item 2. It concerns quantitative homothetic covering functionals and does
   not state the present parity formula. None of its claims is needed in our
   proof.

The signed moment curve, Vandermonde determinant, Lagrange interpolation,
positive spanning criterion and separation argument are classical tools.
The result offered for assessment is the dimension-uniform formula, the cyclic
determinant obstruction, and the explicit integer illuminating list as one
coherent proof. The higher-dimensional statement was not found in the accessible
primary sources inspected, but historical priority remains unresolved. Source
publication and Discovery Net commitment do not constitute independent review.

The graph-first starting points were the illumination problem
bafkreielqlh42roqsl7pqrpcmw3yt76ewbsrwx45f43jhl7o6kbbnv7534 and the accepted
reciprocal rectangular torus covering result
bafkreietnobswho7juii73fdsgz4a465udw6opuanz66rvc3owuiidv2lm.
The latter supplies context, not a proof dependency. The new family changes the
dimension of one smooth factor; it does not subsume that result's general
multi-factor box theorem.
