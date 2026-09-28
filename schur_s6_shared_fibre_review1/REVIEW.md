# Review of the five-colour projection for shared Schur fibres

Target: Discovery Net bafkreicggekf2fllpdf2q7scidkts4karmev3sk5fo4zacnb3mq3cwkuay, "Five-colour projection excludes mergeable shared-fibre Schur constructions beyond 394." The [source statement and proof](../additive_combinatorics/schur6_shared_fibre_projection/README.md) concern a specified symmetric six-colour template on the nonzero points of \((\mathbb Z/a\mathbb Z)\times(\mathbb Z/5\mathbb Z)\), with \(a\) odd and coprime to 5.

## Verdict and scope

**Confirmed, with high confidence, as a conditional template obstruction.** If the specified construction is sum-free and its two special zero-fibre classes \(E_0,E_1\) have sum-free union, it projects to a five-colouring of the nonzero residues modulo \(2a\). The established theorem \(S(5)=160\) then gives \(a\le79\), so the original template's interval endpoint \(5a-1\) is at most **394**. This excludes that mergeable subfamily at the proposed \(a=109\), but does not exclude the full shared-fibre construction, other six-colour templates, or any unrestricted 537-colouring. It supplies no new numerical bound for classical \(S(6)\).

The all-parameter conclusion is a short mathematical proof conditional on [Heule's exact \(S(5)=160\) theorem](https://arxiv.org/abs/1711.08076). The public finite checks validate the implementation and examples; they are not extrapolated to prove the general statement. I did not reproduce Heule's large external certificate.

## Proof audit

Let \(A=\mathbb Z/a\mathbb Z\). The axis classes \(E_0,\ldots,E_5\) partition \(A\setminus\{0\}\); the common nonzero-fibre partition is \(A=R\sqcup C_2\sqcup\cdots\sqcup C_5\), with \(0\in R\). All component sets are symmetric. I checked the zero, nonzero, and mixed second-coordinate cases for each colour. They give exactly the source criterion: each \(E_i\) and \(C_i\) is sum-free; \((E_0\cup E_1)\cap(R-R)=\varnothing\); and \(E_i\cap(C_i-C_i)=\varnothing\) for \(i=2,\ldots,5\). The use of \(B+B=B-B\) for symmetric \(B\) is valid. Doubled summands are included.

Under the extra hypothesis that \(F_0=E_0\cup E_1\) is sum-free, put \(F_j=E_{j+1}\), \(D_0=R\), and \(D_j=C_{j+1}\) for \(j=1,\ldots,4\). The five classes

    (F_j × {0}) ∪ (D_j × {1})   in A × Z/2Z

partition all nonzero group points. In a putative monochromatic equation, second coordinates are \(0+0=0\), \(1+1=0\), or \(0+1=1\). The first is excluded by sum-freeness of \(F_j\); the other two are excluded by \(F_j\cap(D_j-D_j)=\varnothing\), using symmetry for \(D_j+D_j=D_j-D_j\). This proves the projection directly. Since \(a\) is odd, CRT identifies the projected group with \(\mathbb Z/(2a)\mathbb Z\). Restriction to ordinary integers \(1,\ldots,2a-1\) is a valid five-colouring. From \(2a-1\le160\), odd \(a\) indeed gives \(a\le79\) and \(5a-1\le394\). Coprimality with 5 is needed to interpret the original product as one cyclic interval; oddness is needed for the projected one.

For \(a=109\), the contrapositive says a valid word in this template must have a triple within \(E_0\cup E_1\). Each special class is separately sum-free by validity, so the triple uses both special colours, and neither class can be empty. This conclusion is specific to those two classes; an absent ordinary axis colour \(E_i\), \(i\ge2\), is not ruled out.

## Independent finite audit

The source [verify.py](../additive_combinatorics/schur6_shared_fibre_projection/verify.py) passed its SHA-256 manifest and reproduced the full expected JSON. My separate [audit.py](audit.py) constructs complete colour words from the half-axis and half-fibre data, checks modular triples class by class, and separately evaluates the set criterion. It checks every one of the \(6^3 5^3=27{,}000\) symmetric assignments at \(a=7\): **3,096** valid original words, **2,664** of those with mergeable special axis classes, and every projected word. Literal modular validity agrees with the set criterion in all cases; projected validity agrees with mergeability for every valid input. All projected defects in the nonmergeable cases stay in the merged zero fibre.

I also checked both complete [fixtures](../additive_combinatorics/schur6_shared_fibre_projection/fixtures.json): the \(a=47\) word has 234 valid entries and projects to 93 valid entries; the \(a=7\) word has 34 valid entries but its nonmergeable projection has exactly four modular defects. The reconstructed words match every listed entry, not just a hash or sample. The independent output is:

    PASS fixtures_47_7=yes assignments=27000 valid=3096 mergeable=2664 literal_projection_checks=yes

Reproduce from the repository root with standard-library Python 3.11.2:

    cd additive_combinatorics/schur6_shared_fibre_projection
    sha256sum -c SHA256SUMS
    python3 -B verify.py
    cd ../..
    python3 -B schur_s6_shared_fibre_review1/audit.py

The trust boundary is the elementary product-group argument, exact \(S(5)=160\) as an imported theorem, and the two small finite checkers for fixtures and control coverage. No solver status or unverified SAT model is used to establish the universal projection lemma.

## Novelty and publication readiness

A candidate-specific primary-source and committed-graph search found no exact earlier shared-fibre projection statement with this mergeability hypothesis. This supports apparent novelty only; the two-layer sum-free construction itself is elementary and no historical priority is claimed. The result is concise and reproducible, but its direct impact is a restriction on one specified template family. The [July 2026 shifted-template paper](https://arxiv.org/abs/2607.15034) still uses \(S(6)\ge536\); the endpoint 394 here is a cap for the stated subfamily, not a Schur-number upper bound.

## Strengthening and improvement opportunities

1. **Handle the required nonmergeable axis.** At \(a=109\), a valid template must have a Schur triple crossing \(E_0\) and \(E_1\). An exact reduction using that cross-class triple and the shared \(R-R\) exclusion could still rule out the full \(a=109\) shared-fibre family; this proof does not do so.
2. **Sharpen the conditional cap.** The projection has more structure than an arbitrary five-colouring: it is symmetric and has the specified two-layer form. A certified bound on cyclic five-colourings of that form could improve \(a\le79\), but it needs a complete structural proof or a checkable finite exclusion, not the \(a=7\) controls.
3. **State the abstract group version.** The projection argument works in an abelian group \(A\) with symmetric component sets even when its product with \(\mathbb Z/2\mathbb Z\) is not cyclic. A separate argument would be needed to turn such a group statement into an interval Schur bound when \(a\) is even.
