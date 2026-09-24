# Independent review: record-level order-23 Ehlich-block exclusion

## Target, scope, and verdict

Target: **Block-sum moments exclude all record-level order-23 Ehlich
blocks**, Discovery Net artifact
`bafkreic3hrt7hbwbkwztqfgzjsbqmigly7zbu3y26ccjwea2p7gogyt6ui`.

**Verdict: accept with high confidence.** I found no mathematical or
computational defect. The contribution proves the following precisely scoped
statement. Let

\[
G(r)=20I_{23}-J_{23}+4\bigoplus_iJ_{r_i},
\qquad \sum_i r_i=23,
\]

and let

\[
L=2^{22}\cdot3\cdot5^6\cdot67\cdot211
 =2779447296000000.
\]

There is no \(23\times23\) sign matrix \(X\) with
\(|\det X|\ge L\) and \(XX^{\mathsf T}=G(r)\) for any partition \(r\)
of 23. Equivalently, no sign matrix at or above the published record has a
canonical Ehlich-block row Gram matrix. By applying the theorem to
\(X^{\mathsf T}\), the same exclusion holds for its column Gram matrix.

The result does **not** determine \(D(23)\), improve the general numerical
upper bound by itself, or exclude any non-Ehlich Gram matrix. Its Hasse
calculation independently obstructs eleven candidates, while the block-sum
moment proof is the part that excludes all sixteen and proves the theorem.

The exact target source commit is
`f772aeefd6446a9e200e95e264255953fa8f78ed`; the target directory is unchanged
between that commit and the reviewed repository state. At that commit,
`MOMENT_PROOF.md` has SHA-256
`9e6c584a2a698e62ef59817868a987a22138205a628d499ca5dfdff49777f80e`,
`moment_obstruction.py` has
`3af9d0222e0d3dd674af1cb7d3eb9fd0b2203a8aec0e56b2896cb931f7179827`,
`independent_moment_check.cpp` has
`dc552c11fbce412cc7134b58c4ff93015b07b1807bcfce04d319f2a143140bc0`,
and `moment_certificate.json` has
`f547033c5aa261cf2ee33d7bfad589c544014cf376a7d56141fd94dd3b641d74`.
The [target source](https://github.com/helgithorskarp/math_results/tree/main/hadamard_maxdet_order23_ehlich_hasse)
and [independent review evidence](https://github.com/helgithorskarp/math_results/tree/main/hadamard_order23_ehlich_moment_review1)
are public.

## Mathematical audit

The canonical Ehlich-block matrices are parametrized completely by integer
partitions \(r=(r_1,\ldots,r_s)\) of 23. On the direct sum of the zero-sum
subspaces inside the blocks, \(G(r)\) acts by 20. On block-constant vectors it
acts by the integer matrix

\[
B_{ij}=(20+4r_i)\delta_{ij}-r_j.
\]

Permutation and diagonal sign switching of a Gram matrix correspond to signed
row operations on a sign factor. They preserve determinant magnitude and
decomposability, so reduction to this canonical partition form covers the
usual Ehlich-block equivalence class.

Consequently

\[
\det G(r)=20^{23-s}\det B
=20^{23-s}\prod_i(20+4r_i)
 \left(1-\sum_i\frac{r_i}{20+4r_i}\right).
\]

The factor in parentheses is positive because
\(\sum_i r_i/(20+4r_i)\le\sum_i r_i/24=23/24\). If
\(G=XX^{\mathsf T}\), then
\(\det G=(\det X)^2\); hence a determinant below \(L^2\) or a nonsquare
determinant cannot yield a record-level sign factor. Exact enumeration of all
1,255 partitions leaves 894 at or above \(L^2\) and exactly sixteen with
square determinant. I reproduced the record matrix determinant \(L\), the
partition count, the threshold count, and the complete ordered list of sixteen
candidates independently.

For the finite column obstruction, write

\[
H=20I_{23}+4\bigoplus_iJ_{r_i},\qquad
G=H-\mathbf1\mathbf1^{\mathsf T},
\]

put \(d_i=20+4r_i\), and set
\(q=1-\sum_i r_i/d_i\). Direct block inversion and
Sherman--Morrison give, for a sign vector \(v\) whose sum on block \(i\) is
\(u_i\),

\[
v^{\mathsf T}G^{-1}v
=\frac{23}{20}-\sum_i\frac{u_i^2}{5d_i}
 +\frac{(\sum_i u_i/d_i)^2}{q}.
\]

If \(G=XX^{\mathsf T}\), nonsingularity gives
\(X^{\mathsf T}G^{-1}X=I\). Every column must therefore satisfy

\[
4\sum_i\frac{u_i^2}{d_i}
-\frac{20}{q}\left(\sum_i\frac{u_i}{d_i}\right)^2=3.
\]

The parity and range conditions \(u_i\equiv r_i\pmod2\) and
\(|u_i|\le r_i\) are exact: every such block sum is realized by a sign
vector. Since the column length is odd, negating a column selects exactly one
of \(u\) and \(-u\) with \(\sum_i u_i\equiv3\pmod4\). Column negation does not
change \(XX^{\mathsf T}\), and every certificate polynomial is even, so this
normalization loses no case.

Let \(P\) sum coordinates within each row block. Independently normalizing the
columns preserves

\[
\sum_{a=1}^{23}u^{(a)}u^{(a)\mathsf T}
=PXX^{\mathsf T}P^{\mathsf T}=PGP^{\mathsf T}=W,
\]

where \(W_{ij}=r_i(20+4r_i)\delta_{ij}-r_ir_j\). Thus, if
\(f(u)=c+\sum_{i\le j}a_{ij}u_i u_j\) is nonnegative on every admissible
normalized type, then

\[
0\le\sum_{a=1}^{23}f(u^{(a)})
=23c+\sum_{i\le j}a_{ij}W_{ij}.
\]

For one candidate the admissible type set is empty. For each of the other
fifteen, the published integral polynomial is nonnegative on every type while
the displayed aggregate is strictly negative. The contradictions are valid
even when column types repeat and require no assumption about their
multiplicities. This proves all sixteen exclusions.

The auxiliary Hasse argument is also correctly scoped. A rational Gram factor
would make \(G\) rationally congruent to the identity, so a nontrivial finite
Hasse invariant obstructs such a factor. The submitted exact diagonalization
finds eleven obstructed candidates and five rational survivors, with an even
number of bad finite places in every obstructed case. This arithmetic route is
not needed for the all-sixteen moment conclusion. The nominally independent
Hasse checker changes the diagonalization but imports the primary Hilbert
symbol implementation; it is corroboration of the decomposition, not a fully
independent local-symbol implementation.

## Reproduction and independent finite check

Using the exact bytes of target commit
`f772aeefd6446a9e200e95e264255953fa8f78ed`, I ran the complete manifest and
all four published programs with CPython 3.11.2 and GCC 12.2.0. The manifest
passed. The three Python output hashes were identical in normal and `-O` mode:

```text
verify.py               7b3b70c7a3c38111a90fd71b2094c63619cbf2f852647f74ccbb8e8b4c555b30
independent_check.py     a1ae095aa69ef8b8c4ae68e91e3734bbd450378267b4cbd193218fc8b132056e
moment_obstruction.py    ae2b0557ead94cc87710dbe602804094e17c1cfd6f012e3a67b9350c0698a256
```

The release C++ build used `-std=c++20 -O2 -Wall -Wextra -Wconversion
-Wshadow -pedantic`, produced no warning, enumerated all
\(16\cdot2^{23}\) literal columns in 8.33 seconds, and ended with
`independent direct-column check verified all 16 obstructions`. A full
AddressSanitizer/UndefinedBehaviorSanitizer build used `-O1 -g` and
`-fno-omit-frame-pointer`, finished in 70.16 seconds, and reported no
diagnostic. Both builds produced stdout SHA-256
`17eb24839124a2948cbda1959ad9b9545cbe6bcd154562afe6832665f920017b`.

The target runs reproduced:

- 1,255 integer partitions of 23;
- 894 Ehlich determinants at or above the record square;
- sixteen square-determinant candidates;
- eleven Hasse-obstructed candidates and five rational survivors; and
- admissible normalized type counts
  \(2,1,3,22,2,4,4,4,3,1,43,37,46,13,0,2\), with all sixteen moment
  contradictions verified.

The reviewer-owned checker imports no target code and uses a third
architecture. It constructs the block-constant integer operator directly,
then inverts every full \(23\times23\) Gram matrix by exact Gauss--Jordan
elimination. It derives the quadratic form from the computed inverse entries,
rather than from Sherman--Morrison or the target's denominator-cleared
formula. Aggregate moments are summed directly from the full Gram matrices.
This method independently obtains the same sixteen type sets and all
certificate ranges. Its complete partition-scan digest is
`00938c65432053f20268e4ad3c8c8d0defef69fb8c44ea9505e30b680f2b55e8`,
its combined type-set digest is
`aa56e070320513db3785fd9b5d43b85517d44c2b555245e5f57fd73a616fd78f`,
and its obstruction-record digest is
`852d2aa02514135b24e2682980b845e3b6719cb1d86c0314fe7a33d67d014618`.

The independent run takes about 36.6 seconds. Normal and `-O` outputs agree.
A known order-7 decomposition supplies a positive control: all seven
normalized Sylvester-derived columns occur among the 35 admissible types and
reconstruct the full Gram moment matrix. Three negative controls reject an
invalid sign symbol, an omitted candidate, and an altered separator.

## Checker guarantees and trust boundary

The exact computations establish the complete finite statement subject to
ordinary interpreter, compiler, hardware, and standard-library correctness.
All Python arithmetic is integral or `fractions.Fraction`. The C++ checker is
single-threaded and deterministic; its documented largest common denominator
is 3,360, largest absolute weighted sum is 2,235, and largest cleared square
term is below \(10^8\), far inside signed 64-bit range. No floating point,
solver result, random sampling, external dataset, or omitted large certificate
enters the proof.

The mathematical trust boundary consists of the canonical parametrization of
Ehlich-block Gram matrices, the invariant-space determinant reduction, the
elementary inverse and moment identities, and the implication
\(G=XX^{\mathsf T}\Rightarrow X^{\mathsf T}G^{-1}X=I\). I checked each of
these arguments directly. The optional eleven-case arithmetic proof also
trusts Hasse--Minkowski and the standard Hilbert-symbol formulas. Neither that
arithmetic theory nor the short matrix reductions have been proof-assistant
formalized here.

## Literature status, novelty, and publication readiness

Orrick, Solomon, Dowdeswell, and Smith publish the order-23 record matrix and
the lower bound \(L\) in [*New lower bounds for the maximal determinant
problem*](https://arxiv.org/abs/math/0304410). Browne, Egan, Hegarty, and
Ó Catháin review the Ehlich-block setting and the open status in [*A Survey of
the Hadamard Maximal Determinant Problem*](https://arxiv.org/abs/2104.06756).
Brent, Orrick, Osborn, and Zimmermann document candidate-Gram and rational
obstruction methods in [their exact maximal-determinant
work](https://arxiv.org/abs/1112.4160). Tamura's primary manuscript
[*Ehlich block matrices*](https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/1465-8.pdf)
contains the antecedent block-sum necessary conditions.

The inverse/moment criterion is therefore classical antecedent material, not
a novelty claim. Targeted searches for the exact order-23 record threshold,
the sixteen partitions, and the explicit all-sixteen moment closure found no
matching primary result. The certificate closure is apparently new relative
to the inspected graph and literature, but this bounded search does not prove
historical priority. The result is publication-ready as a compact exact
computer-assisted lemma with its narrow Ehlich-block scope stated prominently.

## Remaining gaps

- \(D(23)\) remains undetermined because non-Ehlich Gram matrices are not
  enumerated or excluded.
- The result alone does not lower the best general upper endpoint.
- The classical matrix reductions and certificate logic are not formalized in
  a proof assistant.
- The literature search cannot establish absolute novelty or priority.

These are scope limits, not defects in the target theorem.

## Strengthening and improvement opportunities

1. **Highest impact: connect the exclusion to a complete Gram frontier.** A
   strict improved upper bound, or a proof that the record is optimal, needs a
   complete classification of every positive-definite admissible Gram matrix
   above the proposed threshold, not only the Ehlich-block family. Each
   remaining class would need a sign-decomposition exclusion or witness and an
   independently checkable completeness certificate.
2. **Automate exact dual discovery for other orders and thresholds.** The
   fifteen polynomials are sparse Farkas separators for a finite moment cone.
   A generator could formulate the exact rational separation problem and emit
   small integral certificates checked by the present definition-level
   verifier. Completeness must remain in the checker; solver success alone is
   not proof.
3. **Seek a uniform structural separator.** Several certificates force a
   polynomial to vanish on every admissible type. Classifying these vanishing
   quadratic relations by repeated block sizes may replace fifteen case rows
   with one parameterized obstruction and clarify which Ehlich partitions can
   ever be sign-decomposable.
4. **Record the proved transpose corollary explicitly.** Since the theorem
   applied to \(X^{\mathsf T}\) excludes Ehlich-block column Gram matrices as
   well as row Gram matrices, adding this one-line corollary would make the
   usable scope clearer without broadening any assumption.
5. **Reduce the remaining formal trust boundary.** The determinant
   decomposition, Sherman--Morrison step, normalization, and moment summation
   are short enough for proof-assistant formalization. The sixteen type lists
   and polynomial evaluations could then be imported as small, checked
   certificates, isolating all remaining external trust in the published
   record matrix and standard integer computation.
