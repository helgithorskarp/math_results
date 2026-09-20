# Primary sources and attribution

Checked 2026-09-20. Imported mathematical input is distinguished below from
background and graph provenance. Negative literature searches do not establish
exclusive priority.

1. Nicole Berline and Michele Vergne, **Local Euler--Maclaurin formula for
   polytopes**, Moscow Mathematical Journal 7(3) (2007), 355--386.
   [Author manuscript](https://arxiv.org/pdf/math/0507256).
   In the inspected 41-page manuscript, Theorem 19(d) gives the cone
   identity, Theorem 20(a) gives lattice-translation invariance, Theorem
   20(e), equation (18), gives the polyhedral identity, and Corollary 30(a,b)
   gives the Ehrhart face formula and affine-span period bound. These
   results are explicitly imported. Numbering differs in other versions.
   All measures are normalized by the lattice in the face direction;
   transverse cones use quotient lattices and a fixed rational scalar
   product. Analyticity permits evaluation of the local difference at zero.

2. Miklos Bona, Hyeong-Kwan Ju and Ruriko Yoshida, **On the enumeration of
   certain weighted graphs**, Discrete Applied Mathematics 155 (2007),
   1481--1496. [Author manuscript](https://arxiv.org/pdf/math/0606163).
   The bounded graph-polytope model, bipartite polynomiality and denominator
   dividing two are background; see Lemma 3.5 and Theorem 3.6. The theorem
   leaves a nonnegative denominator parameter unspecified. Sections 2.2
   and 2.4 include cycle and complete-graph computations; Example 3.10 is
   consistent with the present formula. These examples and integrality
   facts are not claimed as new here.

3. Feihu Liu, **Proof of a conjecture on graph polytope**, arXiv:2409.11970v2.
   [Current inspected text](https://arxiv.org/html/2409.11970v2).
   Theorem 2.2 records the denominator form with an unspecified parameter
   s. Theorem 2.3 establishes numerator symmetry. In reduced form the
   present theorem identifies s=d-g+1 for nonbipartite graphs. This does
   not claim that the previously posed symmetry question remains open.

4. Ginji Hamano, Takayuki Hibi and Hidefumi Ohsugi, **Ehrhart series of
   fractional stable set polytopes of finite graphs**, arXiv:1603.09613v2.
   [Author manuscript](https://arxiv.org/html/1603.09613v2).
   Lemma 2.2 characterizes half-integral vertices via nonbipartite components
   of their half-coordinate support. That paper excludes isolates; our
   cube bounds include them. Our face-rank proof establishes the affine-span
   condition needed for all faces. Its fixed-numerator properties do not
   supply the odd-girth cancellation calculation used here.

5. Jiang--Yang--Zhong, **Transfer Matrices and Ehrhart Theory for Path and
   Cyclic Block Polytopes**, arXiv:2607.22008v1.
   [Source manuscript](https://arxiv.org/html/2607.22008v1).
   This is the external cyclic-block context of the selected Discovery Net
   problem. Only block width one coincides with a simple graph cycle.
   Independent-vertex blow-ups in our checker are a different construction.

## Committed graph starting point

- Cyclic parity problem:
  `bafkreicvq533h6vmxs5t6uorkhkfz57r5rmb3uo4p76z4ukuq2fr3u5uuu`.
- Weighted odd-cycle parity theorem:
  `bafkreia7gumlppjkchsfox3kmbub2il5km2kgn7cu3d2xd3bajo3kifgju`.
  [Published source](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/odd_cycle_block_parity).
- Independent acceptance of that precursor:
  `bafkreiaphyf4mofpgv5zonbyluvjlbzegv637dero4gp3lotnmbnv6b27q`.
  [Review source](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/odd_cycle_block_parity_review1).

That review concerns the precursor only. The new proof uses the local
Euler--Maclaurin theorem directly and does not import the precursor's
weighted-block theorem as a mathematical premise. Consequently VARIANT_OF,
rather than GENERALIZES, describes the relationship to its full scope.
