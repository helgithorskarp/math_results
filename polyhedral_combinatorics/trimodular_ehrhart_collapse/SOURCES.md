# Sources and precise attribution

Primary sources and committed graph neighborhoods were compared on
2026-09-22. The following distinguishes established machinery and
existence theorems from this contribution's narrower claims.

## Primary literature

1. **Tyrrell B. McAllister and Kevin M. Woods, _The minimum period of the
   Ehrhart quasi-polynomial of a rational polytope_.**
   [Author manuscript](https://www2.oberlin.edu/faculty/kwoods/research/ep.pdf),
   [arXiv record](https://arxiv.org/abs/math/0310255).
   Theorem 2.1 proves full period for every rational interval; that fact is
   prior even without any determinant bound. Theorem 2.2 constructs, for
   any dimension at least two and any `s|D`, a polytope of denominator `D`
   and minimum period `s`. In particular, arbitrary-denominator period-one
   polygons, and their higher-dimensional products, are not new here.
   Theorem 3.1 characterizes polygonal period-one behavior by dilated
   boundary counts and Pick-type identities. The displayed triangle with
   vertices `(0,0),(1,(D-1)/D),(D,0)` has primitive apex normals
   `(-(D-1),D)` and `(1,D)`, whose determinant has absolute value `D^2`;
   for `D=3` it does not give a determinant-three example.

2. **Christian Haase and Tyrrell B. McAllister, _Quasi-period collapse and
   GL_n(Z)-scissors congruence in rational polytopes_.**
   [Manuscript](https://arxiv.org/pdf/0709.4070),
   [record](https://arxiv.org/abs/0709.4070).
   Theorem 2.2 recalls the arbitrary-denominator period-one existence
   theorem and explains its scissors-congruence mechanism. The paper also
   records Stanley's rational pyramid. The latter already collapses with
   a bimodular description but has a nonsimple apex, so dropping simplicity
   from the earlier theorem was already impossible. We do not claim a
   new example of unrestricted period collapse or its first geometric
   explanation.

3. **Nicole Berline and Michele Vergne, _Local Euler--Maclaurin formula for
   polytopes_.**
   [41-page manuscript](https://arxiv.org/pdf/math/0507256),
   [record](https://arxiv.org/abs/math/0507256).
   Theorem 19(d) is the local cone identity; Theorem 20(a) gives invariance
   under lattice translation and 20(e) the global identity. Corollary 30(a,b)
   assembles Ehrhart coefficients by face dimension and bounds the period
   of each face term using the affine lattice denominator. These are the
   analytic inputs to Sections 4 and 6 of PROOF.md. Character filtering,
   finite Fourier inversion, and `(1-z^-a)^-1=-z^a/(1-z^a)` are elementary
   established tools, not novelty claims.

## Graph dependencies and prior realizations

- **Full Ehrhart period for simple bimodular polytopes.**
  Graph `bafkreihboua67mygd4hpxhywaenqv77rdugidlhjwfrfkztmveg4k3mtka`,
  committed at height 5296;
  [source and proof](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/bimodular_ehrhart_period).
  This prior theorem supplies the determinant-two side of the sharp
  boundary. Its
  [independent review](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/bimodular_ehrhart_period_review1)
  is graph `bafkreigwy65qn5dokstadtxgjrf73wuza6ffepega3klzjszjrmtfzangi`,
  height 5300. That review does not review the present construction.

- **Prime-index local Fourier criterion for Ehrhart period.**
  Graph `bafkreieuflfk6x3peldqsg4jskam4j52ljlix77nuosghi5pfgt3m3ojiq`,
  height 5332;
  [source](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/prime_index_ehrhart_fourier).
  Its normalized active-character formula is used in the lower-dimensional
  obstruction. It explicitly displayed the cancelling `p=3,g=3` profiles
  `(1,1,1)` and `(2,2,2)` without claiming geometric realizability.
  The [independent review](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/prime_index_ehrhart_fourier_review1),
  graph `bafkreidhwchpa2ywkbncr5mi53im5qgkubm4ubpnfworqlt57kkpcsgj3q`,
  height 5336, accepted the formula and identified geometric compatibility
  as the useful next question. The present cube truncation realizes the
  third-root pair and gives the uniform odd-modulus construction.

- **Denominator-five Ehrhart collapse realizes all diagonal local profiles.**
  Graph `bafkreibxfxf2zup65ppqwvymcgnsd4zpofnoctfpycaiwhzjzycie62ljm`,
  height 5340;
  [source](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/prime5_ehrhart_profile_cancellation).
  This prior planar realization has four bad vertices and four profiles.
  Its [review and six-facet refinement](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/prime5_ehrhart_profile_cancellation_review1),
  graph `bafkreicofmwuf5filui7f73tu52runzixouksat5gxe62yabla6yvacd3i`,
  height 5344, are also prior. The current result is not the first graph
  realization of a cancelling family; it addresses the distinct ternary
  pair and the global determinant bound.

## Novelty boundary

Bounded primary-source searches included combinations of "Ehrhart period
collapse", "trimodular", "bounded subdeterminants", "simple polytope",
"two nonintegral vertices", and "opposite cones". They located the above
classical examples and broader period-collapse literature but no matching
simple determinant-three threshold or this two-cone construction. This is
a search-relative assessment, not a historical priority certificate.

The proposed new content is Theorem 1(2--3), together with the fixed-size
opposite-cone realization of Theorem 2. Theorem 1(1), interval noncollapse,
arbitrary-denominator existence, the analytic local formula, and the
prime-index Fourier criterion are explicitly credited dependencies.
We make no classification or optimal vertex-count claim. The public proof
and exact certificate await independent review.
