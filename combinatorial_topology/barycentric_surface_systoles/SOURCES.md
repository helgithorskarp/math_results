# Sources and attribution

Accessed 2026-09-22. The claims here concern finite closed simplicial surfaces
and triangle packings in their barycentric graphs. Targeted searches for
barycentric triangle packing, projective-plane essential cycles, and
characteristic homology found no matching sharp `10/9` theorem. That is a
limited novelty check, not a priority certificate.

**S1. Prior campaign theorem and reviews.**
[Orientation-gap source](../barycentric_triangle_orientation_gap/README.md),
[independent review](../barycentric_triangle_orientation_gap_review1/REVIEW.md),
and [the broader 9/8 review](../../graph_theory/barycentric_tuza_nine_eighths_review1/REVIEW.md).
Committed theorem `bafkreigf4yqvaqld565vxev2gl5xj3aivgdntdhoqqrec4rtnepznfj3xu`,
accepted review `bafkreiahcdi47kdgrzhdlxu45kvocp5vmy4criagvordg3ynlgzminrmmu`,
and 9/8 review `bafkreibogz2j6bzydpkxg3dil6amklagt5zrkidvjyb2rc6rrky677s64a`.
The identity `nu=3f-kappa`, exact covering number, and hexagon completion are
prior work. We prove their characteristic-cycle consequence and the sharp
projective-plane specialization. The new result does not settle a general
signed-cubic frustration conjecture or Tuza's conjecture for arbitrary graphs.

**S2. V. Sivaraman, Frustration in signed graphs (2014).**
[Primary manuscript](https://arxiv.org/abs/1403.7212), Theorem 1.
Equality of edge and vertex frustration for subcubic signed graphs is prior
art. Section 1 of our proof includes its elementary majority-insertion
argument in the facet-orientation setting.

**S3. M. Katzman; M. Adamaszek, small flag complexes.**
Katzman, *Characteristic-independence of Betti numbers of graph ideals*,
JCTA 113 (2006), 435–454,
[primary manuscript](https://arxiv.org/abs/math/0408016).
Adamaszek, *Small flag complexes with torsion*, Canadian Mathematical
Bulletin 57 (2014), 225–230,
[primary manuscript](https://arxiv.org/abs/1208.3892), Theorem 1(a,b)
(published Theorem 1.1(i,ii)), credits these two parts to Katzman.
We import absence of torsion through ten vertices and the four-graph
eleven-vertex classification. Four graph6 strings are copied from the
[arXiv TeX source](https://arxiv.org/src/1208.3892), the list after
`end{document}`; only those four data records are redistributed.
Their completeness is trusted as a published computer-assisted theorem;
their surface status and cycle certificates are checked here.

**S4. H. Liu and M. J. Pelsmajer, Dominating sets in triangulations on surfaces.**
Ars Mathematica Contemporanea 4 (2011), 177–204.
[Primary manuscript, version 4](https://arxiv.org/pdf/1006.1879v4).
Theorem 5 supplies `s<=2 sqrt(n)`; our proof explains how its projective-plane
case follows from Lemma 27 with injective projection of the retained levels.
We do not need the sharper Lemma 28. The introductory icosahedral refinement
construction is prior art, but its asserted exact `3k` systole fails at
`k=2`; section 6 provides a five-cycle certificate. We separately prove the
coarse growth needed here and use the correct Euler count `5k^2+1`.

**S5. Classical shortest-cycle algorithms.**
Jeff Erickson's [author notes on shortest interesting cycles](https://jeffe.cs.illinois.edu/teaching/comptop/2023/notes/23-optimal-cycles.html)
describe the classical shortest-cycle and homology-annotation setting.
No new claim is made for BFS, binary homology covers, Gaussian elimination,
or polynomial shortest-cycle optimization. The application is the exact
optimal-packing reconstruction through the characteristic class.

The source countercheck is not an independent review of the whole
Liu–Pelsmajer paper. All current universal proofs remain ordinary mathematical
arguments rather than proof-assistant formalizations.
